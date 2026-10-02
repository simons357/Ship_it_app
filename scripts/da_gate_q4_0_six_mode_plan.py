#!/usr/bin/env python3
"""Q4-0 six-mode calibration: plan contract only.

Does not evolve NS. Does not measure rotation. Does not stamp alpha_c.
DA must approve the packet before anything runs.
NS is not solved.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "packets" / "DA-GATE-Q4-0-SIX-MODE-CALIBRATION-2026-09-25.md"


def run() -> dict:
    text = PLAN.read_text(encoding="utf-8")
    return {
        "ns_solved": False,
        "executed": False,
        "da_approved": False,
        "alpha_c_proxy_stamped": False,
        "quartic_named_from_disk": False,
        "quartic_54_46_on_this_tree": False,
        "admission": {
            "alpha_c_near_one": True,
            "T_c_positive": True,
            "six_mode_only": True,
        },
        "measures": "nonlinear-force rotation against viscosity",
        "plan_says_do_not_run": "Do not run" in text,
        "plan_keeps_nu": r"Do not drop \(\nu\)" in text or "Do not drop" in text,
        "i3_weighted_imported": False,
        "kkl_regrouping_imported": False,
        "fiber_moved_off_neutral": False,
        "gate_altered": {
            "sbp": False,
            "phi_vs_d": False,
            "low_tail_snapshot": False,
            "sign_realizability": False,
        },
        "da_ns_2": "OPEN",
    }


def main() -> int:
    payload = run()
    out = ROOT / "results" / "da_gate_q4_0_six_mode_plan.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
