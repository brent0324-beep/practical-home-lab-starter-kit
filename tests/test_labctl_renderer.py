from __future__ import annotations

import sys
from pathlib import Path
import tempfile
import unittest

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from labctl.core import (
    LabctlPathError,
    LabctlValidationError,
    load_lab_spec,
    render_lab_topology,
)


class TestLabctlRenderer(unittest.TestCase):
    def test_renderer_matches_expected_topology(self):
        spec_path = REPO_ROOT / "labs/examples/two-node-point-to-point/lab.yaml"
        profile_path = REPO_ROOT / "profiles/labs/two-node-ptp-fast.yaml"
        expected_path = REPO_ROOT / "tests/fixtures/two-node-point-to-point.expected.clab.yml"

        actual = render_lab_topology(spec_path, profile_path)
        expected = yaml.safe_load(expected_path.read_text(encoding="utf-8"))

        self.assertEqual(actual, expected)
        self.assertIn("io.labctl.managed", actual["topology"]["defaults"]["labels"])
        self.assertEqual(actual["mgmt"]["ipv4-subnet"], "172.30.90.0/24")
        for node in actual["topology"]["nodes"].values():
            self.assertNotIn("/", node["mgmt-ipv4"])
            self.assertEqual(node["image"], "docker.io/nicolaka/netshoot:v0.16")

    def test_profile_variable_replacement(self):
        spec_path = REPO_ROOT / "labs/examples/two-node-point-to-point/lab.yaml"
        actual = render_lab_topology(spec_path, REPO_ROOT / "profiles/labs/two-node-ptp-fast.yaml")
        self.assertEqual("172.30.90.111", actual["topology"]["nodes"]["router-a"]["mgmt-ipv4"])
        self.assertEqual("172.30.90.112", actual["topology"]["nodes"]["router-b"]["mgmt-ipv4"])
        self.assertEqual("172.30.90.0/24", actual["mgmt"]["ipv4-subnet"])


class TestLabctlSpecValidation(unittest.TestCase):
    def test_schema_rejects_invalid_spec(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".yaml", delete=False) as handle:
            handle.write(
                """
name: bad-lab
variables:
  mgmt_prefix: "10.1.1."
nodes:
  router-a:
    kind: linux
links:
  - endpoints:
      - router-a:eth1
      - router-a:eth2
"""
            )
            handle.flush()
            with self.assertRaises(LabctlValidationError):
                load_lab_spec(Path(handle.name))

    def test_path_traversal_rejected(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".yaml", delete=False) as handle:
            handle.write(
                """
name: traversal-test
nodes:
  router-a:
    kind: linux
    image: alpine:3
    startup_config: ../unsafe.cfg
  router-b:
    kind: linux
    image: alpine:3
    startup_config: startup/router-b.cfg
links:
  - endpoints:
      - router-a:eth1
      - router-b:eth1
"""
            )
            handle.flush()
            with self.assertRaises(LabctlPathError):
                render_lab_topology(Path(handle.name))

    def test_bind_path_traversal_rejected(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".yaml", delete=False) as handle:
            handle.write(
                """
name: bind-traversal-test
nodes:
  router-a:
    kind: linux
    image: alpine:3
    startup_config: startup/router-a.cfg
    binds:
      - ../unsafe.cfg:/tmp/unsafe.cfg
  router-b:
    kind: linux
    image: alpine:3
    startup_config: startup/router-b.cfg
links:
  - endpoints:
      - router-a:eth1
      - router-b:eth1
"""
            )
            handle.flush()
            with self.assertRaises(LabctlPathError):
                render_lab_topology(Path(handle.name))

    def test_mgmt_host_outside_subnet_rejected(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".yaml", delete=False) as handle:
            handle.write(
                """
name: subnet-test
mgmt_ipv4_subnet: 172.30.90.0/24
nodes:
  router-a:
    kind: linux
    image: docker.io/nicolaka/netshoot:v0.16
    mgmt_ipv4: 172.30.91.111
  router-b:
    kind: linux
    image: docker.io/nicolaka/netshoot:v0.16
    mgmt_ipv4: 172.30.90.112
links:
  - endpoints:
      - router-a:eth1
      - router-b:eth1
"""
            )
            handle.flush()
            with self.assertRaisesRegex(LabctlValidationError, "outside mgmt subnet"):
                render_lab_topology(Path(handle.name))


if __name__ == "__main__":
    unittest.main()
