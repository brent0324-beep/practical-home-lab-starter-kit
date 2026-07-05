from __future__ import annotations

from copy import deepcopy
from json import JSONDecodeError
from jsonschema import Draft202012Validator
from pathlib import Path
from typing import Any, Dict, Mapping
import json
import posixpath
import re
import yaml


_TEMPLATE_RE = re.compile(r"{{\s*([A-Za-z_][A-Za-z0-9_]*)\s*}}")


class LabctlError(RuntimeError):
    """Base exception for labctl runtime errors."""


class LabctlValidationError(LabctlError):
    """Raised when a lab spec or profile fails schema validation."""


class LabctlTemplateError(LabctlError):
    """Raised when profile variable substitutions cannot be completed."""


class LabctlPathError(LabctlValidationError):
    """Raised when a startup-config or bind path is unsafe."""


_REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_SCHEMA_PATH = _REPO_ROOT / "schemas" / "lab_spec.schema.json"
PROFILE_SCHEMA_PATH = _REPO_ROOT / "schemas" / "lab_profile.schema.json"


def _load_document(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise LabctlError(f"File does not exist: {path}")
    suffix = path.suffix.lower()
    try:
        if suffix in {".yaml", ".yml"}:
            with path.open("r", encoding="utf-8") as stream:
                data = yaml.safe_load(stream)
        elif suffix == ".json":
            with path.open("r", encoding="utf-8") as stream:
                data = json.load(stream)
        else:
            raise LabctlError(f"Unsupported file format: {path.suffix}")
    except UnicodeDecodeError as err:
        raise LabctlValidationError(f"Unable to read {path}: {err}") from err
    except JSONDecodeError as err:
        raise LabctlValidationError(f"Invalid JSON in {path}: {err}") from err
    except yaml.YAMLError as err:
        raise LabctlValidationError(f"Invalid YAML in {path}: {err}") from err

    if not isinstance(data, dict):
        raise LabctlValidationError(f"Top-level document in {path} must be a mapping")
    return data


def _load_schema(schema_path: Path) -> Dict[str, Any]:
    if not schema_path.exists():
        raise LabctlError(f"Schema file missing: {schema_path}")
    return _load_document(schema_path)


def _validate_json_schema(document: Mapping[str, Any], schema_path: Path, *, label: str) -> None:
    schema = _load_schema(schema_path)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document), key=lambda error: error.path
    )
    if errors:
        details = "\n".join(
            f"{label}: {error.message} (path: {'/'.join(str(p) for p in error.path) or '<root>'})"
            for error in errors
        )
        raise LabctlValidationError(details)


def load_lab_spec(path: Path | str) -> Dict[str, Any]:
    spec_path = Path(path)
    spec = _load_document(spec_path)
    _validate_json_schema(spec, SPEC_SCHEMA_PATH, label="lab spec")
    return spec


def load_lab_profile(path: Path | str | None) -> Dict[str, Any]:
    if path is None:
        return {}
    profile_path = Path(path)
    if not profile_path.exists():
        raise LabctlValidationError(f"Profile not found: {profile_path}")
    profile = _load_document(profile_path)
    _validate_json_schema(profile, PROFILE_SCHEMA_PATH, label="lab profile")
    return profile


def _apply_template(value: Any, variables: Mapping[str, Any]) -> Any:
    if isinstance(value, str):
        placeholders = _TEMPLATE_RE.findall(value)
        if not placeholders:
            return value
        for name in placeholders:
            if name not in variables:
                raise LabctlTemplateError(
                    f"Unknown profile variable '{name}' in value '{value}'"
                )
        def _replace(match: re.Match[str]) -> str:
            key = match.group(1)
            return str(variables[key])
        return _TEMPLATE_RE.sub(_replace, value)
    if isinstance(value, list):
        return [_apply_template(item, variables) for item in value]
    if isinstance(value, dict):
        return {key: _apply_template(item, variables) for key, item in value.items()}
    return value


def _ensure_safe_relative_path(path: str, field_name: str) -> str:
    if not isinstance(path, str):
        raise LabctlPathError(f"{field_name} must be a string")
    if path.startswith("~"):
        raise LabctlPathError(f"{field_name} cannot start with ~: {path}")
    if path.startswith("/"):
        raise LabctlPathError(f"{field_name} cannot be absolute: {path}")
    if "\\" in path:
        raise LabctlPathError(f"{field_name} cannot contain parent traversal markers: {path}")
    normalized = posixpath.normpath(path.replace("\\", "/"))
    if normalized == ".." or normalized.startswith("../") or "/../" in normalized:
        raise LabctlPathError(f"{field_name} cannot use parent traversal: {path}")
    return path


def _validate_path_references(spec: Mapping[str, Any]) -> None:
    nodes = spec.get("nodes", {})
    if not isinstance(nodes, dict):
        raise LabctlValidationError("nodes must be a mapping")

    for node_name, node_data in nodes.items():
        if not isinstance(node_data, dict):
            raise LabctlValidationError(f"Node '{node_name}' must be an object")

        startup_config = node_data.get("startup_config")
        if startup_config is not None:
            if not isinstance(startup_config, str):
                raise LabctlValidationError(
                    f"startup_config for '{node_name}' must be a string"
                )
            node_data["startup_config"] = _ensure_safe_relative_path(
                startup_config, f"startup_config ({node_name})"
            )

        binds = node_data.get("binds", [])
        if not isinstance(binds, list):
            raise LabctlValidationError(f"binds for '{node_name}' must be a list")
        for index, bind in enumerate(binds):
            if not isinstance(bind, str):
                raise LabctlValidationError(
                    f"binds[{index}] for '{node_name}' must be a string"
                )
            parts = bind.split(":", 2)
            if len(parts) < 2:
                raise LabctlValidationError(f"bind '{bind}' in '{node_name}' is invalid")
            source_path = parts[0]
            _ensure_safe_relative_path(source_path, f"bind source ({node_name}#{index})")

    links = spec.get("links", [])
    if not isinstance(links, list):
        raise LabctlValidationError("links must be a list")
    node_keys = set(nodes.keys())
    for index, link in enumerate(links):
        if not isinstance(link, dict):
            raise LabctlValidationError(f"links[{index}] must be an object")
        endpoints = link.get("endpoints")
        if not isinstance(endpoints, list) or len(endpoints) != 2:
            raise LabctlValidationError(f"links[{index}] must have exactly two endpoints")
        for endpoint in endpoints:
            if not isinstance(endpoint, str) or ":" not in endpoint:
                raise LabctlValidationError(
                    f"links[{index}] endpoint '{endpoint}' is invalid"
                )
            node_name = endpoint.split(":", 1)[0]
            if node_name not in node_keys:
                raise LabctlValidationError(
                    f"links[{index}] references unknown node '{node_name}'"
                )


def _merge_variables(
    spec: Mapping[str, Any], profile: Mapping[str, Any] | None
) -> Dict[str, Any]:
    merged = deepcopy(spec)
    profile_vars = {}
    if profile:
        profile_vars = dict(profile.get("variables", {}))
    merged_vars = deepcopy(merged.get("variables", {}))
    merged_vars.update(profile_vars)
    merged["variables"] = merged_vars
    merged["variables"].setdefault("lab_name", merged.get("name"))
    return _apply_template(merged, merged_vars)


def _normalize_topology(spec: Mapping[str, Any]) -> Dict[str, Any]:
    topology_nodes: Dict[str, Dict[str, Any]] = {}
    for node_name, node_spec in spec["nodes"].items():
        node_config: Dict[str, Any] = {}
        for key, value in node_spec.items():
            if value is None:
                continue
            if key == "startup_config":
                node_config["startup-config"] = value
            elif key == "mgmt_ipv4":
                node_config["mgmt-ipv4"] = value
            else:
                node_config[key] = value
        topology_nodes[node_name] = node_config

    return {
        "name": spec["name"],
        "topology": {
            "defaults": {
                "labels": {
                    "io.labctl.managed": "true",
                    "io.labctl.engine": "labctl",
                }
            },
            "nodes": topology_nodes,
            "links": list(spec["links"]),
        },
    }


def render_lab_topology(
    spec_path: Path | str,
    profile_path: Path | str | None = None,
) -> Dict[str, Any]:
    spec = load_lab_spec(spec_path)
    profile = load_lab_profile(profile_path)
    merged = _merge_variables(spec, profile)
    _validate_path_references(merged)
    return _normalize_topology(merged)


def dump_topology_yaml(topology: Mapping[str, Any], *, comment: bool = True) -> str:
    if comment:
        header = "# Rendered by labctl\n"
    else:
        header = ""
    return header + yaml.safe_dump(
        dict(topology),
        sort_keys=True,
        default_flow_style=False,
    )


def repo_root() -> Path:
    return _REPO_ROOT
