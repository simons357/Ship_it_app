#!/usr/bin/env python3
"""Run (A)–(C) / occupancy / conditional-Gronwall diagnostics.

Class: unaugmented axisymmetric-with-swirl. Remainder: T_{j←j}.
Assumed: [small disks / restricted classes; NS not solved].
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from domain_architect.axisym_ac_tests import run_ac_occupancy_battery


def main() -> int:
    payload = run_ac_occupancy_battery()
    print(json.dumps(payload, indent=2, sort_keys=False))
    print("---")
    print("summary:")
    for k, v in payload["summary"].items():
        print(f"  {k}: {v}")
    print("honesty: NS not solved; Clay NOT CLAIMED; leftover T_{j←j} OPEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
