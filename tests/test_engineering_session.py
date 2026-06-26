import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class EngineeringSessionTests(unittest.TestCase):
    def test_prompt_renderer_includes_smcpp_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "prompt.md"
            cmd = [
                sys.executable,
                str(REPO_ROOT / "scripts/render_codex_prompt.py"),
                "--template",
                str(REPO_ROOT / "templates/implementation_prompt.yaml"),
                "--profile",
                str(REPO_ROOT / "profiles/governance.yaml"),
                "--task",
                str(REPO_ROOT / "templates/task_prompt_spec.example.yaml"),
                "--output",
                str(output_path),
            ]
            subprocess.run(cmd, cwd=REPO_ROOT, check=True)
            text = output_path.read_text(encoding="utf-8")
            self.assertIn("## SMCPP LIFECYCLE", text)
            self.assertTrue(text.rstrip().endswith("END OF CODEX PROMPT"))

    def test_migration_bundle_contains_required_entries(self):
        subprocess.run([sys.executable, str(REPO_ROOT / "scripts/render_repository_bootstrap.py")], cwd=REPO_ROOT, check=True)
        subprocess.run([sys.executable, str(REPO_ROOT / "scripts/build_repository_context.py")], cwd=REPO_ROOT, check=True)
        subprocess.run([sys.executable, str(REPO_ROOT / "scripts/build_session_history.py")], cwd=REPO_ROOT, check=True)
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle_path = Path(tmpdir) / "bundle.zip"
            subprocess.run(
                [sys.executable, str(REPO_ROOT / "scripts/build_migration_bundle.py"), "--output", str(bundle_path)],
                cwd=REPO_ROOT,
                check=True,
            )
            with zipfile.ZipFile(bundle_path) as archive:
                names = set(archive.namelist())
            required = {
                "START_HERE.md",
                "BUNDLE_SNAPSHOT.md",
                "manifest.yaml",
                "docs/bootstrap/BOOTSTRAP.md",
                "docs/bootstrap/SESSION_STATE.md",
                "generated/repository_context.md",
                "generated/session_history.md",
            }
            self.assertTrue(required.issubset(names))


if __name__ == "__main__":
    unittest.main()
