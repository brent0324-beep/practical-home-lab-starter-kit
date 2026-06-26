#!/usr/bin/env python3

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "generated/session_history.md"
DEFAULT_TEMPLATE = REPO_ROOT / "templates/session_history_template.md"
SESSION_STATE_PATH = REPO_ROOT / "docs/bootstrap/SESSION_STATE.md"
GENERATED_NOTICE = [
    "> Generated file. Source inputs: local Git state and `docs/bootstrap/SESSION_STATE.md` when present.",
    "> Template: `templates/session_history_template.md`",
    "> Builder: `scripts/build_session_history.py`",
    "> Intended consumers: `./scripts/session` and migration bundles.",
    "> Do not hand-edit `generated/session_history.md` except emergency repair.",
]


def run_git(args):
    result = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


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


def section_items(text):
    items = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- "):
            items.append(line[2:].strip())
        else:
            items.append(line)
    return items


def compute_timestamp():
    head = run_git(["log", "-1", "--format=%cI"])
    if head:
        return head
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def branch_status():
    raw = run_git(["status", "--short", "--branch", "--untracked-files=all"])
    lines = [line.rstrip() for line in raw.splitlines() if line.strip()]
    branch = "unknown"
    status_lines = []
    if lines and lines[0].startswith("## "):
        branch = lines[0][3:].split("...", 1)[0].strip()
        status_lines = lines[1:]
    else:
        status_lines = lines
    return branch, ("clean" if not status_lines else "dirty")


def render_entries():
    sections = load_sections(SESSION_STATE_PATH)
    branch, working_tree = branch_status()
    current_goal = "; ".join(section_items(sections.get("Current Sprint/Session Goal", ""))) or "unknown"
    validation = "; ".join(section_items(sections.get("Validation Status", ""))) or "unknown"
    next_action = "; ".join(section_items(sections.get("Next Action", ""))) or "unknown"
    entries = [
        {
            "title": "Current active session",
            "date": compute_timestamp(),
            "branch": branch,
            "goal": current_goal,
            "outcome": "In progress" if working_tree == "dirty" else "Ready for governed re-entry",
            "commit": run_git(["rev-parse", "--short", "HEAD"]) or "unknown",
            "validation": validation,
            "next_action": next_action,
            "warnings": "Working tree is dirty." if working_tree == "dirty" else "None",
        }
    ]

    raw_commits = run_git(["log", "--skip=1", "-4", "--pretty=format:%cI\t%h\t%s"])
    for index, line in enumerate(raw_commits.splitlines(), start=1):
        if not line.strip():
            continue
        commit_time, short_hash, subject = (line.split("\t", 2) + ["", "", ""])[:3]
        entries.append(
            {
                "title": f"Recent committed session {index}",
                "date": commit_time or "unknown",
                "branch": "main",
                "goal": subject or "unknown",
                "outcome": f"Committed repository change: {subject or 'unknown'}",
                "commit": short_hash or "unknown",
                "validation": "unknown",
                "next_action": "unknown",
                "warnings": "Derived from Git commit history; full session transcript not stored.",
            }
        )

    blocks = []
    for entry in entries:
        blocks.extend(
            [
                f"### {entry['title']}",
                "",
                f"- Date: `{entry['date']}`",
                f"- Branch: `{entry['branch']}`",
                f"- Goal: {entry['goal']}",
                f"- Outcome: {entry['outcome']}",
                f"- Commit: `{entry['commit']}`",
                f"- Validation: {entry['validation']}",
                f"- Next action: {entry['next_action']}",
                f"- Warnings / Missing context: {entry['warnings']}",
                "",
            ]
        )
    return "\n".join(blocks).strip()


def render_history():
    branch, working_tree = branch_status()
    warnings = []
    if not SESSION_STATE_PATH.is_file():
        warnings.append("`docs/bootstrap/SESSION_STATE.md` is missing.")
    if working_tree == "dirty":
        warnings.append("Working tree is dirty; current session may still be in progress.")
    if branch == "main":
        warnings.append("Current session is on the integration branch.")

    context = {
        "generated_notice": "\n".join(GENERATED_NOTICE),
        "purpose": "- Compact recent engineering-session history for public-safe maintainer re-entry.",
        "session_entries": render_entries(),
        "warnings": "\n".join(f"- {warning}" for warning in warnings) if warnings else "- none",
        "timestamp": f"- Generated: `{compute_timestamp()}`",
    }
    template = DEFAULT_TEMPLATE.read_text(encoding="utf-8")
    rendered = template
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered.rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    output_path = Path(args.output)
    rendered = render_history()
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
        print(f"build_session_history.py: {exc}", file=sys.stderr)
        sys.exit(1)
