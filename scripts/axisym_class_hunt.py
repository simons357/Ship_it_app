#!/usr/bin/env python3
"""Run axisymmetric-with-swirl class hunt (Door-1 / (A) candidates).

Class: unaugmented axisymmetric-with-swirl. Remainder: T_{j←j}.
Assumed: [exact disks; signed Im; no ė_j/Ż/Λ′; NS not solved].
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from domain_architect.axisym_class_hunt import run_class_hunt_battery


def main() -> int:
    payload = run_class_hunt_battery()
    print(json.dumps(payload, indent=2, sort_keys=False, default=float))
    print("---")
    print("summary_table:")
    for row in payload["summary_table"]:
        print(
            f"  {row['class_id']}: {row['verdict']} | "
            f"A_seats={row['A_seats']} | Tjj={row['Tjj_controlled']} | "
            f"millennium={row['millennium_relevant']}"
        )
    print("overall:", payload["overall"])
    print("honesty: NS not solved; Clay NOT CLAIMED; leftover T_{j←j} OPEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
