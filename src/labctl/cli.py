from __future__ import annotations

from pathlib import Path
import argparse
import sys

from .core import (
    LabctlError,
    LabctlPathError,
    LabctlTemplateError,
    LabctlValidationError,
    dump_topology_yaml,
    render_lab_topology,
)
from .lifecycle import LabctlLifecycle


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--state-dir",
        default=".labctl",
        help="Directory for labctl managed state.",
    )
    parser.add_argument(
        "--profile",
        help="Optional profile document with variable overrides.",
    )


def _validate(args: argparse.Namespace) -> int:
    render_lab_topology(args.spec, args.profile)
    print(f"Validated lab spec: {args.spec}")
    return 0


def _render(args: argparse.Namespace) -> int:
    topology = render_lab_topology(args.spec, args.profile)
    content = dump_topology_yaml(topology)
    if args.output:
        Path(args.output).write_text(content, encoding="utf-8")
        print(f"Wrote topology: {args.output}")
        return 0
    print(content, end="")
    return 0


def _deploy(args: argparse.Namespace) -> int:
    lifecycle = LabctlLifecycle(state_dir=args.state_dir)
    topo_file = lifecycle.deploy(
        args.spec,
        profile_path=args.profile,
        output=args.output,
        dry_run=args.dry_run,
    )
    if args.dry_run:
        print(f"Rendered topology for dry-run: {topo_file}")
    else:
        print(f"Deployed lab using topology {topo_file}")
    return 0


def _status(args: argparse.Namespace) -> int:
    lifecycle = LabctlLifecycle(state_dir=args.state_dir)
    output = lifecycle.status(args.name)
    if output:
        print(output, end="" if output.endswith("\n") else "\n")
    return 0


def _destroy(args: argparse.Namespace) -> int:
    lifecycle = LabctlLifecycle(state_dir=args.state_dir)
    message = lifecycle.destroy(args.name, dry_run=args.dry_run)
    print(message)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="labctl",
        description="LabForge labctl for Containerlab-first workflows.",
    )
    parser.add_argument("--version", action="version", version="labctl 0.1.0")

    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate a lab spec and profile.")
    validate.add_argument("spec", help="Path to lab specification file.")
    _add_common_args(validate)
    validate.set_defaults(func=_validate)

    render = subparsers.add_parser("render", help="Render a Containerlab topology file.")
    render.add_argument("spec", help="Path to lab specification file.")
    render.add_argument("--output", help="Output file for rendered topology.")
    _add_common_args(render)
    render.set_defaults(func=_render)

    deploy = subparsers.add_parser("deploy", help="Deploy a lab spec through containerlab.")
    deploy.add_argument("spec", help="Path to lab specification file.")
    deploy.add_argument("--output", help="Override output path for rendered topology.")
    deploy.add_argument(
        "--dry-run",
        action="store_true",
        help="Render topology only; do not call containerlab.",
    )
    _add_common_args(deploy)
    deploy.set_defaults(func=_deploy)

    status = subparsers.add_parser("status", help="Show lab status by explicit name.")
    status.add_argument("name", help="Lab name from a managed deploy.")
    status.add_argument("--state-dir", default=".labctl")
    status.set_defaults(func=_status)

    destroy = subparsers.add_parser("destroy", help="Destroy a managed lab by explicit name.")
    destroy.add_argument("name", help="Explicit managed lab name; no bulk destroy.")
    destroy.add_argument(
        "--dry-run",
        action="store_true",
        help="Print destroy intent without calling containerlab.",
    )
    destroy.add_argument("--state-dir", default=".labctl")
    destroy.set_defaults(func=_destroy)

    return parser


def run(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (LabctlError, LabctlValidationError, LabctlTemplateError, LabctlPathError) as err:
        print(f"labctl error: {err}", file=sys.stderr)
        return 1
    except FileNotFoundError as err:
        print(f"labctl error: {err}", file=sys.stderr)
        return 1


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
