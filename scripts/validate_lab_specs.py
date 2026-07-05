#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
SRC_DIR = SCRIPT_DIR.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from labctl.core import load_lab_spec


def discover_examples(root: Path) -> list[Path]:
    return sorted(
        [
            path
            for path in root.glob("**/lab.yaml")
            if path.is_file()
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--examples-dir",
        default=str(Path.cwd() / "labs" / "examples"),
        help="Directory containing lab example specs.",
    )
    args = parser.parse_args(argv)

    examples_root = Path(args.examples_dir)
    if not examples_root.exists():
        print(f"Examples root does not exist: {examples_root}", file=sys.stderr)
        return 2

    errors = 0
    for spec_path in discover_examples(examples_root):
        try:
            load_lab_spec(spec_path)
            print(f"OK {spec_path}")
        except Exception as exc:  # noqa: BLE001
            errors += 1
            print(f"FAIL {spec_path}: {exc}", file=sys.stderr)

    if errors:
        print(f"Validation failed: {errors} invalid spec(s).", file=sys.stderr)
        return 1
    print(f"Validated {len(discover_examples(examples_root))} lab specs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
