#!/usr/bin/env python3

import argparse
import io
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "generated/migration_bundles/bootstrap_chat_session_v2.zip"
BOOTSTRAP_PATH = REPO_ROOT / "docs/bootstrap/BOOTSTRAP.md"
SESSION_STATE_PATH = REPO_ROOT / "docs/bootstrap/SESSION_STATE.md"
REPOSITORY_CONTEXT_PATH = REPO_ROOT / "generated/repository_context.md"
SESSION_HISTORY_PATH = REPO_ROOT / "generated/session_history.md"
REQUIRED_FILES = [
    Path("docs/bootstrap/BOOTSTRAP.md"),
    Path("docs/bootstrap/SESSION_STATE.md"),
    Path("config/repository_bootstrap.yml"),
    Path("generated/repository_context.md"),
    Path("generated/session_history.md"),
    Path("templates/implementation_prompt.yaml"),
    Path("profiles/governance.yaml"),
    Path("schemas/prompt_schema.json"),
    Path("docs/governance/codex_prompt_standard.md"),
    Path("docs/governance/codex_prompt_checklist.md"),
    Path("docs/governance/engineering_session_workflow.md"),
]
OPTIONAL_FILES = [
    Path("generated/prompts/governance_smoke.md"),
]
ZIP_NAME = "bootstrap_chat_session_v2"


def run_git(args):
    result = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def ensure_artifacts():
    bootstrap_check = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts/render_repository_bootstrap.py"), "--check"],
        cwd=REPO_ROOT,
        check=False,
    )
    if bootstrap_check.returncode != 0:
        subprocess.run([sys.executable, str(REPO_ROOT / "scripts/render_repository_bootstrap.py")], cwd=REPO_ROOT, check=True)
    context_check = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts/build_repository_context.py"), "--output", str(REPOSITORY_CONTEXT_PATH), "--check"],
        cwd=REPO_ROOT,
        check=False,
    )
    if context_check.returncode != 0:
        subprocess.run([sys.executable, str(REPO_ROOT / "scripts/build_repository_context.py")], cwd=REPO_ROOT, check=True)
    history_check = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts/build_session_history.py"), "--output", str(SESSION_HISTORY_PATH), "--check"],
        cwd=REPO_ROOT,
        check=False,
    )
    if history_check.returncode != 0:
        subprocess.run([sys.executable, str(REPO_ROOT / "scripts/build_session_history.py")], cwd=REPO_ROOT, check=True)


def validation_summary():
    if not REPOSITORY_CONTEXT_PATH.is_file():
        return ["Validation status: unknown"]
    text = REPOSITORY_CONTEXT_PATH.read_text(encoding="utf-8")
    marker = "## Repository Validation Status"
    if marker not in text:
        return ["Validation status: unknown"]
    section = text.split(marker, 1)[1].split("\n## ", 1)[0]
    lines = []
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(">"):
            continue
        if line.startswith("- "):
            lines.append(line[2:].strip())
    return lines or ["Validation status: unknown"]


def parse_session_goal():
    if not SESSION_STATE_PATH.is_file():
        return "unknown"
    text = SESSION_STATE_PATH.read_text(encoding="utf-8")
    marker = "## Current Sprint/Session Goal"
    if marker not in text:
        return "unknown"
    section = text.split(marker, 1)[1].split("\n## ", 1)[0]
    lines = []
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if line.startswith("- "):
            lines.append(line[2:].strip())
    return "; ".join(lines) if lines else "unknown"


def compute_timestamp():
    head = run_git(["log", "-1", "--format=%cI"])
    if head:
        return datetime.fromisoformat(head.replace("Z", "+00:00")).astimezone(timezone.utc).replace(microsecond=0)
    return datetime.now(timezone.utc).replace(microsecond=0)


def start_here_text(snapshot_timestamp: str):
    return (
        "# START_HERE\n\n"
        "Use this bundle for maintainership re-entry in the following order:\n\n"
        "1. `BUNDLE_SNAPSHOT.md`\n"
        "2. `manifest.yaml`\n"
        "3. `docs/bootstrap/BOOTSTRAP.md`\n"
        "4. `docs/bootstrap/SESSION_STATE.md`\n"
        "5. `generated/repository_context.md`\n"
        "6. `generated/session_history.md`\n\n"
        "Source precedence:\n\n"
        "- `BUNDLE_SNAPSHOT.md` is authoritative for bundle build time state.\n"
        "- `manifest.yaml` describes the bundle contents.\n"
        "- `docs/bootstrap/BOOTSTRAP.md` is durable repository bootstrap context.\n"
        "- `docs/bootstrap/SESSION_STATE.md` is bounded live session context.\n"
        "- Generated repository context and session history support deterministic re-entry.\n\n"
        f"Bundle snapshot timestamp: `{snapshot_timestamp}`\n"
    )


def bundle_snapshot_text(snapshot_timestamp: str):
    branch = run_git(["branch", "--show-current"]) or "unknown"
    commit_hash = run_git(["rev-parse", "--short", "HEAD"]) or "unknown"
    working_tree = "clean" if not run_git(["status", "--short"]) else "dirty"
    validation_lines = "\n".join(f"- {item}" for item in validation_summary())
    return (
        "# BUNDLE_SNAPSHOT\n\n"
        f"- Repository: `Practical Home Lab Starter Kit`\n"
        f"- Branch: `{branch}`\n"
        f"- Commit: `{commit_hash}`\n"
        f"- Working tree: `{working_tree}`\n"
        f"- Lifecycle posture: `Governance v2 Lite`\n"
        f"- Session purpose: {parse_session_goal()}\n"
        f"- Snapshot timestamp: `{snapshot_timestamp}`\n"
        "- Source precedence: `BUNDLE_SNAPSHOT.md` is authoritative for current state at bundle build time.\n\n"
        "## Validation Summary\n\n"
        f"{validation_lines}\n"
    )


def manifest_text(snapshot_timestamp: str, included_files, optional_missing):
    branch = run_git(["branch", "--show-current"]) or "unknown"
    commit_hash = run_git(["rev-parse", "--short", "HEAD"]) or "unknown"
    manifest = {
        "version": 2,
        "artifact_kind": "migration_bundle_manifest",
        "bundle_name": ZIP_NAME,
        "timestamp": snapshot_timestamp,
        "source_repository": {
            "name": "Practical Home Lab Starter Kit",
            "root": "project root",
            "branch": branch,
            "commit": commit_hash,
        },
        "included_files": included_files,
        "optional_missing_files": optional_missing,
        "excluded_categories": [
            "secrets",
            "credentials",
            ".env_values",
            "private_notes",
            "runtime_media",
            "generated_zip_artifacts",
        ],
        "validation_summary": validation_summary(),
    }
    return yaml.safe_dump(manifest, sort_keys=False)


def bundle_bytes():
    ensure_artifacts()
    missing = []
    included = []
    optional_missing = []
    files = []

    for relative in REQUIRED_FILES:
        absolute = REPO_ROOT / relative
        if absolute.is_file():
            files.append((relative.as_posix(), absolute))
            included.append(relative.as_posix())
        else:
            missing.append(relative.as_posix())
    if missing:
        raise ValueError(f"missing required bundle files: {', '.join(missing)}")

    for relative in OPTIONAL_FILES:
        absolute = REPO_ROOT / relative
        if absolute.is_file():
            files.append((relative.as_posix(), absolute))
            included.append(relative.as_posix())
        else:
            optional_missing.append(relative.as_posix())

    timestamp = compute_timestamp()
    snapshot_timestamp = timestamp.isoformat().replace("+00:00", "Z")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        def writestr(name: str, content: str):
            info = zipfile.ZipInfo(name)
            info.date_time = timestamp.timetuple()[:6]
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, content)

        writestr("START_HERE.md", start_here_text(snapshot_timestamp))
        writestr("BUNDLE_SNAPSHOT.md", bundle_snapshot_text(snapshot_timestamp))
        writestr("manifest.yaml", manifest_text(snapshot_timestamp, included, optional_missing))

        for archive_name, absolute_path in sorted(files):
            info = zipfile.ZipInfo(archive_name)
            info.date_time = timestamp.timetuple()[:6]
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, absolute_path.read_bytes())
    return buffer.getvalue()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output_path = Path(args.output)
    rendered = bundle_bytes()
    if args.check:
        if not output_path.is_file():
            raise ValueError(f"{output_path} does not exist")
        if output_path.read_bytes() != rendered:
            raise ValueError(f"{output_path} is out of sync")
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(rendered)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"build_migration_bundle.py: {exc}", file=sys.stderr)
        sys.exit(1)
