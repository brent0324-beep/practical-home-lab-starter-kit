#!/usr/bin/env python3

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_SECTION_ORDER = [
    "MODEL RECOMMENDATION",
    "Repository",
    "Current Known State",
    "Goal",
    "Non-negotiable Constraints",
    "Agentic Loop Scope",
    "SMCPP LIFECYCLE",
    "Builder Scope",
    "Explicit Non-goals",
    "Validation",
    "Release History",
    "Brent Usefulness Evaluator",
    "Final Report",
    "END OF CODEX PROMPT",
]
REQUIRED_FILES = [
    "docs/governance/codex_prompt_standard.md",
    "docs/governance/codex_prompt_checklist.md",
    "docs/governance/engineering_session_workflow.md",
    "templates/implementation_prompt.yaml",
    "templates/task_prompt_spec.example.yaml",
    "profiles/governance.yaml",
    "schemas/prompt_schema.json",
    "scripts/render_codex_prompt.py",
]

failures = 0


def fail(message):
    global failures
    print(f"FAIL prompt-standard: {message}")
    failures += 1


def ensure_file(path_text):
    path = REPO_ROOT / path_text
    if not path.is_file() or path.stat().st_size == 0:
        fail(f"missing or empty {path_text}")
        return None
    return path


def validate_docs():
    standard_doc = ensure_file("docs/governance/codex_prompt_standard.md")
    checklist_doc = ensure_file("docs/governance/codex_prompt_checklist.md")
    if standard_doc:
        text = standard_doc.read_text(encoding="utf-8")
        for phrase in [
            "Markdown:",
            "YAML:",
            "JSON:",
            "Generated prompts are preferred over manually repeated boilerplate.",
            "SMCPP = governed feature completion into the configured integration branch.",
        ]:
            if phrase not in text:
                fail(f"docs/governance/codex_prompt_standard.md missing phrase: {phrase}")
    if checklist_doc:
        text = checklist_doc.read_text(encoding="utf-8")
        for phrase in [
            "templates/implementation_prompt.yaml",
            "profiles/governance.yaml",
            "END OF CODEX PROMPT",
            "Brent Usefulness Evaluator",
        ]:
            if phrase not in text:
                fail(f"docs/governance/codex_prompt_checklist.md missing phrase: {phrase}")


def validate_template_and_profile():
    template_path = ensure_file("templates/implementation_prompt.yaml")
    profile_path = ensure_file("profiles/governance.yaml")
    task_path = ensure_file("templates/task_prompt_spec.example.yaml")
    schema_path = ensure_file("schemas/prompt_schema.json")
    if not all([template_path, profile_path, task_path, schema_path]):
        return None, None, None
    template = yaml.safe_load(template_path.read_text(encoding="utf-8"))
    profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    task = yaml.safe_load(task_path.read_text(encoding="utf-8"))
    try:
        json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"schemas/prompt_schema.json is invalid JSON: {exc}")
    if template.get("section_order") != REQUIRED_SECTION_ORDER:
        fail("templates/implementation_prompt.yaml has unexpected section order")
    lifecycle = template.get("lifecycle", {}).get("smcpp", {})
    if not lifecycle.get("enabled"):
        fail("templates/implementation_prompt.yaml must enable SMCPP for the lite workflow")
    if lifecycle.get("canonical_definition") != "SMCPP = governed feature completion into the configured integration branch.":
        fail("templates/implementation_prompt.yaml has unexpected canonical SMCPP definition")
    if profile.get("profile_name") != "governance":
        fail("profiles/governance.yaml must declare profile_name: governance")
    if task.get("repository", {}).get("path") != "project root":
        fail("templates/task_prompt_spec.example.yaml must use the public-safe repository path placeholder")
    return template_path, profile_path, task_path


def validate_renderer(template_path, profile_path, task_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "prompt.md"
        cmd = [
            sys.executable,
            str(REPO_ROOT / "scripts/render_codex_prompt.py"),
            "--template",
            str(template_path),
            "--profile",
            str(profile_path),
            "--task",
            str(task_path),
            "--output",
            str(output_path),
        ]
        result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            fail(result.stderr.strip() or result.stdout.strip() or "prompt renderer failed")
            return
        text = output_path.read_text(encoding="utf-8")
        for section in REQUIRED_SECTION_ORDER[:-1]:
            marker = f"## {section}"
            if marker not in text:
                fail(f"rendered prompt missing section: {section}")
        if "## SMCPP LIFECYCLE" not in text:
            fail("rendered prompt missing SMCPP lifecycle section")
        if not text.rstrip().endswith("END OF CODEX PROMPT"):
            fail("rendered prompt must end with END OF CODEX PROMPT")


def main():
    for path_text in REQUIRED_FILES:
        ensure_file(path_text)
    validate_docs()
    paths = validate_template_and_profile()
    if all(paths):
        validate_renderer(*paths)
    if failures:
        raise SystemExit(1)
    print("prompt-standard: PASS")


if __name__ == "__main__":
    main()
