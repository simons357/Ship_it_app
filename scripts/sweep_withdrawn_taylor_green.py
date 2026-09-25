#!/usr/bin/env python3
"""Sweep live artifacts for the withdrawn Taylor–Green fraction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from domain_architect.errata import (
    live_values_block,
    sweep_repository,
    write_sweep_report,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "data" / "process_console" / "errata" / "sweep.json",
    )
    args = parser.parse_args(argv)
    report = sweep_repository(args.root)
    write_sweep_report(report, args.out)
    print(live_values_block())
    print()
    print(f"hits: {len(report.hits)}")
    violations = [
        h for h in report.hits if h.classification == "live_unmarked_withdrawn"
    ]
    print(f"live unmarked withdrawn: {len(violations)}")
    for hit in report.hits:
        print(f"  {hit.classification}: {hit.path}:{hit.line}: {hit.text[:120]}")
    json.dump({"out": str(args.out), "violations": len(violations)}, sys.stdout)
    sys.stdout.write("\n")
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
