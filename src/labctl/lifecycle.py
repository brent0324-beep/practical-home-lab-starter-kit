from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Optional, Protocol
import json
import subprocess
import time
from shutil import which

from .core import LabctlError, dump_topology_yaml, render_lab_topology


class CommandResult(Protocol):
    returncode: int
    stdout: str
    stderr: str


CommandRunner = Callable[[list[str]], CommandResult]


@dataclass
class LabRecord:
    topology_file: str
    deployed_at: int


class LabctlState:
    def __init__(self, state_dir: Path | str = ".labctl") -> None:
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.state_dir / "state.json"
        self._state: Dict[str, Dict[str, object]] = self._load()

    def _load(self) -> Dict[str, Dict[str, object]]:
        if not self.path.exists():
            return {}
        try:
            text = self.path.read_text(encoding="utf-8")
            loaded = json.loads(text)
            if not isinstance(loaded, dict):
                return {}
            return loaded.get("labs", {})
        except (json.JSONDecodeError, OSError):
            return {}

    def save(self) -> None:
        payload = {"labs": self._state}
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def get_lab(self, name: str) -> Optional[LabRecord]:
        data = self._state.get(name)
        if not data:
            return None
        return LabRecord(
            topology_file=data["topology_file"],
            deployed_at=data["deployed_at"],
        )

    def set_lab(self, name: str, topology_file: Path) -> None:
        self._state[name] = {
            "topology_file": str(topology_file),
            "deployed_at": int(time.time()),
        }
        self.save()

    def remove_lab(self, name: str) -> None:
        if self._state.pop(name, None) is not None:
            self.save()

    def all_labs(self) -> Dict[str, Dict[str, object]]:
        return dict(self._state)


class LabctlLifecycle:
    def __init__(
        self,
        state_dir: Path | str = ".labctl",
        *,
        containerlab_binary: str = "containerlab",
        runner: Optional[CommandRunner] = None,
    ) -> None:
        self.state = LabctlState(state_dir=state_dir)
        self.containerlab_binary = containerlab_binary
        self.runner = runner

    def _run(self, args: list[str], *, check: bool = True, capture_output: bool = True) -> CommandResult:
        if self.runner:
            return self.runner(args)
        if check and which(self.containerlab_binary) is None:
            raise LabctlError(
                f"containerlab binary not found: {self.containerlab_binary}. Install and retry."
            )
        try:
            return subprocess.run(
                args,
                check=check,
                text=True,
                capture_output=capture_output,
            )
        except subprocess.CalledProcessError as err:
            detail = (err.stderr or err.stdout or str(err)).strip()
            raise LabctlError(detail) from err

    def _topology_path(self, spec_path: Path, output: Path | None) -> Path:
        if output:
            return output
        return spec_path.with_suffix(".clab.yml")

    def deploy(
        self,
        spec_path: Path | str,
        *,
        profile_path: Path | str | None = None,
        output: Path | str | None = None,
        dry_run: bool = False,
    ) -> Path:
        spec_path = Path(spec_path)
        output_path = Path(self._topology_path(spec_path, Path(output) if output else None))
        topology = render_lab_topology(spec_path, profile_path)
        topology_yaml = dump_topology_yaml(topology)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(topology_yaml, encoding="utf-8")

        if dry_run:
            return output_path

        cmd = [self.containerlab_binary, "deploy", "-t", str(output_path)]
        self._run(cmd, check=True, capture_output=True)
        self.state.set_lab(topology["name"], output_path)
        return output_path

    def status(self, name: str) -> str:
        record = self.state.get_lab(name)
        if record is None:
            raise LabctlError(
                f"Lab '{name}' is not tracked in {self.state.path}. "
                "Deploy this lab first or pass an explicit managed path."
            )
        topology_file = Path(record.topology_file)
        cmd = [self.containerlab_binary, "inspect", "-t", str(topology_file)]
        result = self._run(cmd, check=True, capture_output=True)
        return result.stdout

    def destroy(self, name: str, *, dry_run: bool = False) -> str:
        record = self.state.get_lab(name)
        if record is None:
            raise LabctlError(
                f"Lab '{name}' is not tracked in {self.state.path}. "
                "Destroy requires an explicit managed lab name."
            )
        topology_file = Path(record.topology_file)
        if dry_run:
            return f"DRY-RUN would destroy lab '{name}' using {topology_file}"

        cmd = [self.containerlab_binary, "destroy", "-t", str(topology_file)]
        self._run(cmd, check=True, capture_output=True)
        self.state.remove_lab(name)
        return f"Destroyed lab '{name}' and removed managed resources from {topology_file}"
