#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_METADATA = REPO_ROOT / "config/repository_bootstrap.yml"
DEFAULT_TEMPLATE = REPO_ROOT / "templates/repository_bootstrap_template.md"
DEFAULT_OUTPUT = REPO_ROOT / "docs/bootstrap/BOOTSTRAP.md"
GENERATED_NOTICE = "> Generated file. Source of truth: `config/repository_bootstrap.yml`"
REQUIRED_KEYS = [
    "repository_identity",
    "repository_purpose",
    "repository_classification",
    "governance_model",
    "safety_boundaries",
    "privacy_boundaries",
    "architecture_summary",
    "important_directories",
    "validation_commands",
    "smcpp_status",
    "major_capabilities",
    "major_decisions",
    "current_constraints",
    "known_technical_debt",
    "outstanding_governance_work",
    "warnings_inconsistencies",
    "live_session_state",
    "central_standard_references",
]


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a top-level mapping")
    return data


def ensure_required_keys(data, path: Path):
    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        raise ValueError(f"{path} missing required keys: {', '.join(missing)}")


def ensure_public_safe(data):
    rendered = yaml.safe_dump(data, sort_keys=False)
    prohibited = [r"BEGIN [A-Z ]*PRIVATE KEY"]
    for pattern in prohibited:
        if re.search(pattern, rendered):
            raise ValueError(f"metadata contains prohibited content matching {pattern}")


def bullet_list(items):
    if not items:
        return "- none"
    return "\n".join(f"- {item}" for item in items)


def directory_list(items):
    if not items:
        return "- none"
    return "\n".join(f"- `{item['path']}`: {item['purpose']}" for item in items)


def command_list(items):
    if not items:
        return "- none"
    return "\n".join(f"- {item['label']}: `{item['command']}`" for item in items)


def render_sections(data):
    identity = data["repository_identity"]
    purpose = data["repository_purpose"]
    classification = data["repository_classification"]
    governance = data["governance_model"]
    smcpp = data["smcpp_status"]
    live_state = data["live_session_state"]
    return {
        "repository_identity": "\n".join(
            [
                f"- Name: `{identity['name']}`",
                f"- Root: `{identity['root']}`",
                f"- Default branch: `{identity['default_branch']}`",
                f"- Working branch rule: {identity['working_branch_rule']}",
            ]
        ),
        "repository_purpose": "\n".join(
            [
                f"- Summary: {purpose['summary']}",
                f"- Scope: {purpose['scope']}",
            ]
        ),
        "repository_classification": "\n".join(
            [
                f"- Repo class: {classification['repo_class']}",
                f"- Posture: {classification['posture']}",
            ]
        ),
        "governance_model": "\n".join(
            [
                "- Hierarchy:",
                bullet_list(governance["hierarchy"]),
                f"- Local mode: {governance['local_mode']}",
                f"- Operator approval: {governance['operator_approval']}",
            ]
        ),
        "safety_boundaries": bullet_list(data["safety_boundaries"]),
        "privacy_boundaries": bullet_list(data["privacy_boundaries"]),
        "architecture_summary": bullet_list(data["architecture_summary"]),
        "important_directories": directory_list(data["important_directories"]),
        "validation_commands": command_list(data["validation_commands"]),
        "smcpp_status": "\n".join(
            [
                f"- Mode: {smcpp['mode']}",
                f"- Readiness profile: {smcpp['readiness_profile']}",
                "- Notes:",
                bullet_list(smcpp["notes"]),
            ]
        ),
        "major_capabilities": bullet_list(data["major_capabilities"]),
        "major_decisions": bullet_list(data["major_decisions"]),
        "current_constraints": bullet_list(data["current_constraints"]),
        "known_technical_debt": bullet_list(data["known_technical_debt"]),
        "outstanding_governance_work": bullet_list(data["outstanding_governance_work"]),
        "warnings_inconsistencies": bullet_list(data["warnings_inconsistencies"]),
        "live_session_state": "\n".join(
            [
                f"- Path: `{live_state['path']}`",
                "- Guidance:",
                bullet_list(live_state["guidance"]),
            ]
        ),
        "central_standard_references": bullet_list([f"`{item}`" for item in data["central_standard_references"]]),
    }


def render_template(template_text: str, sections):
    rendered = template_text
    for key, value in sections.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    unresolved = re.findall(r"{{[^}]+}}", rendered)
    if unresolved:
        raise ValueError(f"template contains unresolved placeholders: {', '.join(sorted(set(unresolved)))}")
    return rendered.rstrip() + "\n"


def check_output(output_path: Path, rendered_text: str):
    if not output_path.is_file():
        raise ValueError(f"{output_path} does not exist")
    current = output_path.read_text(encoding="utf-8")
    if GENERATED_NOTICE not in current:
        raise ValueError(f"{output_path} missing generated-file notice")
    if current != rendered_text:
        raise ValueError(f"{output_path} is out of sync with metadata and template")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", default=str(DEFAULT_METADATA))
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    metadata_path = Path(args.metadata)
    template_path = Path(args.template)
    output_path = Path(args.output)

    data = load_yaml(metadata_path)
    ensure_required_keys(data, metadata_path)
    ensure_public_safe(data)
    template_text = template_path.read_text(encoding="utf-8")
    rendered_text = render_template(template_text, render_sections(data))

    if args.check:
        check_output(output_path, rendered_text)
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered_text, encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"render_repository_bootstrap.py: {exc}", file=sys.stderr)
        sys.exit(1)
