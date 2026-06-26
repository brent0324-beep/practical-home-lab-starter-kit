#!/usr/bin/env python3

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "generated/repository_context.md"
DEFAULT_TEMPLATE = REPO_ROOT / "templates/repository_context_template.md"
BOOTSTRAP_METADATA = REPO_ROOT / "config/repository_bootstrap.yml"
SESSION_STATE_PATH = REPO_ROOT / "docs/bootstrap/SESSION_STATE.md"
PROMPT_TEMPLATE_PATH = REPO_ROOT / "templates/implementation_prompt.yaml"
GENERATED_NOTICE = [
    "> Generated file. Source inputs: local Git state, `config/repository_bootstrap.yml`, and `docs/bootstrap/SESSION_STATE.md` when present.",
    "> Template: `templates/repository_context_template.md`",
    "> Builder: `scripts/build_repository_context.py`",
    "> Intended consumers: Prompt Renderer inputs and migration bundles.",
    "> Do not hand-edit `generated/repository_context.md` except emergency repair.",
]


def run_git(args):
    result = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def load_yaml(path: Path):
    if not path.is_file():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data or {}


def load_sections(path: Path):
    if not path.is_file():
        return {}
    sections = {}
    current = None
    buffer = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = line[3:].strip()
            buffer = []
            continue
        if current is not None:
            buffer.append(line.rstrip())
    if current is not None:
        sections[current] = "\n".join(buffer).strip()
    return sections


def bullet_lines(lines, fallback):
    cleaned = [line.strip() for line in lines if line.strip()]
    if not cleaned:
        return f"- {fallback}"
    output = []
    for line in cleaned:
        output.append(line if line.startswith("- ") else f"- {line}")
    return "\n".join(output)


def extract_section(sections, name, fallback):
    return bullet_lines(sections.get(name, "").splitlines(), fallback)


def status_lines(excluded_output: Path):
    raw = run_git(["status", "--short", "--untracked-files=all"])
    lines = []
    excluded = excluded_output.relative_to(REPO_ROOT).as_posix()
    for line in raw.splitlines():
        if not line.strip():
            continue
        path_text = line[3:] if len(line) > 3 else ""
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        if path_text == excluded:
            continue
        lines.append(line.rstrip())
    return lines


def format_markdown_list(items, fallback):
    if not items:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in items)


def compute_timestamp():
    candidates = []
    head = run_git(["log", "-1", "--format=%cI"])
    if head:
        candidates.append(datetime.fromisoformat(head.replace("Z", "+00:00")))
    for path in [BOOTSTRAP_METADATA, SESSION_STATE_PATH]:
        if path.exists():
            candidates.append(datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc))
    if not candidates:
        candidates.append(datetime.now(timezone.utc))
    return max(candidates).astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def render_context(output_path: Path):
    metadata = load_yaml(BOOTSTRAP_METADATA)
    prompt_template = load_yaml(PROMPT_TEMPLATE_PATH)
    session_sections = load_sections(SESSION_STATE_PATH)
    branch = run_git(["branch", "--show-current"]) or "unknown"
    dirty_lines = status_lines(output_path)
    working_tree = "clean" if not dirty_lines else "dirty"
    default_branch = metadata.get("repository_identity", {}).get("default_branch", "main")

    recent_commits = []
    for line in run_git(["log", "-5", "--pretty=format:%h\t%s"]).splitlines():
        if not line.strip():
            continue
        commit_hash, subject = (line.split("\t", 1) + [""])[:2]
        recent_commits.append(f"`{commit_hash}`: {subject}")

    feature_branches = []
    for line in run_git(["for-each-ref", "--format=%(refname:short)\t%(objectname:short)\t%(contents:subject)", "refs/heads/feature"]).splitlines():
        if not line.strip():
            continue
        name, commit_hash, subject = (line.split("\t", 2) + ["", ""])[:3]
        feature_branches.append(f"`{name}`: `{commit_hash}` {subject}".strip())

    warnings = []
    if not SESSION_STATE_PATH.is_file():
        warnings.append("`docs/bootstrap/SESSION_STATE.md` is missing.")
    if working_tree == "dirty":
        warnings.append("Working tree is dirty; review `git status --short --branch` before handoff.")
    if branch == default_branch and working_tree == "dirty":
        warnings.append("Protected branch is dirty.")

    context = {
        "generated_notice": "\n".join(GENERATED_NOTICE),
        "repository": "\n".join(
            [
                f"- Name: `{metadata.get('repository_identity', {}).get('name', REPO_ROOT.name)}`",
                f"- Root: `{metadata.get('repository_identity', {}).get('root', 'project root')}`",
                f"- Default branch: `{default_branch}`",
                f"- Classification: {metadata.get('repository_classification', {}).get('repo_class', 'unknown')}",
                f"- Posture: {metadata.get('repository_classification', {}).get('posture', 'unknown')}",
            ]
        ),
        "current_branch": "\n".join(
            [
                f"- Branch: `{branch}`",
                f"- Branch role: {'protected integration branch' if branch == default_branch else 'scoped working branch'}",
            ]
        ),
        "working_tree_status": "\n".join(
            [
                f"- Status: `{working_tree}`",
                f"- Changed entries: `{len(dirty_lines)}`",
            ]
        ),
        "protected_branch_status": "\n".join(
            [
                f"- Integration branch: `{default_branch}`",
                f"- Current branch protected: {'yes' if branch == default_branch else 'no'}",
            ]
        ),
        "recent_commits": format_markdown_list(recent_commits, "none"),
        "active_feature_branches": format_markdown_list(feature_branches, "none"),
        "repository_validation_status": extract_section(session_sections, "Validation Status", "unknown"),
        "current_release_target": extract_section(session_sections, "Current Release Target", "unknown"),
        "current_mvp": extract_section(session_sections, "Current MVP Definition", "unknown"),
        "outstanding_governance_work": format_markdown_list(metadata.get("outstanding_governance_work", []), "none"),
        "known_technical_debt": format_markdown_list(metadata.get("known_technical_debt", []), "none"),
        "current_roadmap": extract_section(session_sections, "Roadmap", "unknown"),
        "current_session_state_reference": "\n".join(
            [
                "- Path: `docs/bootstrap/SESSION_STATE.md`",
                "- Purpose: bounded live context for branch, validation, roadmap, and handoff state",
            ]
        ),
        "bootstrap_version": f"- Version: `{metadata.get('version', 'unknown')}`",
        "prompt_standard_version": f"- Version: `{prompt_template.get('version', 'unknown')}`",
        "important_validation_commands": format_markdown_list(
            [f"{item['label']}: `{item['command']}`" for item in metadata.get("validation_commands", [])],
            "unknown",
        ),
        "current_repository_warnings": format_markdown_list(warnings, "none"),
        "timestamp": f"- Generated: `{compute_timestamp()}`",
    }

    template_text = DEFAULT_TEMPLATE.read_text(encoding="utf-8")
    rendered = template_text
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered.rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    output_path = Path(args.output)
    rendered = render_context(output_path)
    if args.check:
        if not output_path.is_file():
            raise ValueError(f"{output_path} does not exist")
        if output_path.read_text(encoding="utf-8") != rendered:
            raise ValueError(f"{output_path} is out of sync")
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"build_repository_context.py: {exc}", file=sys.stderr)
        sys.exit(1)
