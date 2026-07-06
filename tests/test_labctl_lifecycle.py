from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from labctl.lifecycle import LabctlLifecycle
from labctl.core import LabctlError


class FakeCompleted:
    def __init__(self, returncode: int = 0, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class TestLabctlLifecycle(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.state_dir = Path(self.tempdir.name) / ".labctl"
        self.calls: list[list[str]] = []

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _runner(self, command: list[str]) -> FakeCompleted:
        self.calls.append(command)
        if command[:3] == ["docker", "network", "inspect"]:
            return FakeCompleted(returncode=1, stderr="network not found")
        return FakeCompleted(stdout="ok")

    def test_deploy_generates_expected_topology_file(self):
        lifecycle = LabctlLifecycle(state_dir=self.state_dir, runner=self._runner)
        spec_path = REPO_ROOT / "labs/examples/two-node-point-to-point/lab.yaml"
        topology = lifecycle.deploy(
            spec_path,
            profile_path=REPO_ROOT / "profiles/labs/two-node-ptp-fast.yaml",
            output=Path(self.tempdir.name) / "two-node-ptp.clab.yml",
            dry_run=True,
        )
        self.assertTrue(topology.name.endswith(".clab.yml"))
        self.assertEqual(topology.read_text(encoding="utf-8").count("name: two-node-ptp"), 1)

    def test_destroy_requires_known_lab_name(self):
        lifecycle = LabctlLifecycle(state_dir=self.state_dir, runner=self._runner)
        with self.assertRaises(LabctlError):
            lifecycle.destroy("missing-lab")

    def test_destroy_and_status_call_containerlab(self):
        lifecycle = LabctlLifecycle(state_dir=self.state_dir, runner=self._runner)
        spec_path = REPO_ROOT / "labs/examples/two-node-point-to-point/lab.yaml"
        lifecycle.deploy(
            spec_path,
            profile_path=REPO_ROOT / "profiles/labs/two-node-ptp-fast.yaml",
            output=Path(self.tempdir.name) / "two-node-ptp.clab.yml",
            dry_run=True,
        )

        # Seed realistic state to allow status/destroy command generation.
        topology_file = Path(self.tempdir.name) / "two-node-ptp.clab.yml"
        state_file = self.state_dir / "state.json"
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(
            '{"labs":{"two-node-ptp":{"topology_file":"%s","deployed_at":123}}}' % topology_file,
            encoding="utf-8",
        )
        lifecycle = LabctlLifecycle(state_dir=self.state_dir, runner=self._runner)

        lifecycle.status("two-node-ptp")
        self.assertIn(["containerlab", "inspect", "-t", str(topology_file)], self.calls)
        lifecycle.destroy("two-node-ptp")
        self.assertIn(["containerlab", "destroy", "-t", str(topology_file), "--cleanup"], self.calls)

    def test_containerlab_stderr_surfaces_as_labctl_error(self):
        lifecycle = LabctlLifecycle(state_dir=self.state_dir, containerlab_binary=sys.executable)
        with self.assertRaisesRegex(LabctlError, "containerlab failed"):
            lifecycle._run(
                [
                    sys.executable,
                    "-c",
                    "import sys; sys.stderr.write('containerlab failed'); sys.exit(7)",
                ]
            )

    def test_deploy_rejects_stale_mismatched_network_subnet(self):
        def runner(command: list[str]) -> FakeCompleted:
            self.calls.append(command)
            if command == ["docker", "network", "inspect", "clab-two-node-ptp"]:
                return FakeCompleted(
                    stdout='[{"IPAM":{"Config":[{"Subnet":"172.30.20.0/24"}]}}]'
                )
            return FakeCompleted(stdout="ok")

        lifecycle = LabctlLifecycle(state_dir=self.state_dir, runner=runner)
        spec_path = REPO_ROOT / "labs/examples/two-node-point-to-point/lab.yaml"
        with self.assertRaisesRegex(
            LabctlError,
            "Docker network 'clab-two-node-ptp' already exists with subnet 172.30.20.0/24",
        ):
            lifecycle.deploy(
                spec_path,
                profile_path=REPO_ROOT / "profiles/labs/two-node-ptp-fast.yaml",
                output=Path(self.tempdir.name) / "stale-network.clab.yml",
            )

        self.assertFalse(any(command[:2] == ["containerlab", "deploy"] for command in self.calls))

    def test_failed_deploy_removes_its_mgmt_network(self):
        def runner(command: list[str]) -> FakeCompleted:
            self.calls.append(command)
            if command == ["docker", "network", "inspect", "clab-bgp-triangle"]:
                return FakeCompleted(returncode=1, stderr="network not found")
            if command[:2] == ["containerlab", "deploy"]:
                return FakeCompleted(returncode=1, stderr="duplicate endpoint")
            if command == ["docker", "network", "rm", "clab-bgp-triangle"]:
                return FakeCompleted(stdout="clab-bgp-triangle")
            return FakeCompleted(stdout="ok")

        lifecycle = LabctlLifecycle(state_dir=self.state_dir, runner=runner)
        spec_path = REPO_ROOT / "labs/examples/three-node-bgp-triangle/lab.yaml"
        with self.assertRaisesRegex(LabctlError, "duplicate endpoint"):
            lifecycle.deploy(
                spec_path,
                output=Path(self.tempdir.name) / "bgp-triangle.clab.yml",
            )

        self.assertIn(["docker", "network", "rm", "clab-bgp-triangle"], self.calls)


if __name__ == "__main__":
    unittest.main()
