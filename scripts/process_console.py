#!/usr/bin/env python3
"""Write Process Console v5 static ledger and HTML."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from domain_architect.process_console import ProcessConsole


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest", type=Path, default=None)
    args = parser.parse_args(argv)
    paths = ProcessConsole().write_static(args.dest)
    for key, path in paths.items():
        print(f"{key}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
