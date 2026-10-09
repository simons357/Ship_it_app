#!/usr/bin/env python3
"""Run the independent Domain Architect Gate B trilinear audit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from domain_architect.trilinear_audit import audit_gate_b_trilinear  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(
        description="Independent DA audit of the Gate B trilinear claim"
    )
    p.add_argument(
        "--out",
        type=Path,
        default=Path("scripts/ns_attacks/GATE-B-TRILINEAR-DA-AUDIT.json"),
    )
    p.add_argument("--json", action="store_true", help="print JSON to stdout")
    args = p.parse_args()
    audit = audit_gate_b_trilinear()
    payload = audit.as_dict()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2))
    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(audit.narrative())
        print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
