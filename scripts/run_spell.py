#!/usr/bin/env python3
"""CLI wrapper for platform spell runner.

Usage:
  python3 scripts/run_spell.py list
  python3 scripts/run_spell.py sfe_bh_overlay --Nmax 200
  python3 scripts/run_spell.py bridge_floor_verify 100
  python3 scripts/run_spell.py sfe_bh_overlay 500 1000
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from packages.shared_core.spell_runner import list_spells, run_spell  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a registered PFPI spell")
    parser.add_argument("spell", help="Spell id or 'list'")
    parser.add_argument("extra", nargs="*", help="Positional args (e.g. N sizes)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--Nmax", type=int, default=None, help="Max lattice size")
    args = parser.parse_args()

    if args.spell == "list":
        spells = list_spells()
        if args.json:
            print(json.dumps(spells, indent=2))
        else:
            for sid, entry in spells.items():
                print(f"{sid:20s}  {entry.get('name')}  → {entry.get('script')}")
        return

    run_args: dict = {}
    if args.Nmax is not None:
        run_args["Nmax"] = args.Nmax
    if args.extra:
        if args.spell in ("sfe_bh_overlay", "route_c_gap_a"):
            run_args["sizes"] = [int(x) for x in args.extra]
        elif args.spell == "bridge_floor_verify" and args.extra:
            run_args["Nmax"] = int(args.extra[0])
        else:
            run_args["positional"] = args.extra

    result = run_spell(args.spell, run_args or None)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["stdout"])
        if result["stderr"]:
            print(result["stderr"], file=sys.stderr)
        if result["artifact_path"]:
            print(f"\nArtifact: {result['artifact_path']}")
    sys.exit(result["returncode"])


if __name__ == "__main__":
    main()
