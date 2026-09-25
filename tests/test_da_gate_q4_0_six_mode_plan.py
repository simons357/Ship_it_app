"""Q4-0 is a plan. Nothing runs. DA has not approved.

Locked gates are not altered. NS not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import da_gate_q4_0_six_mode_plan as plan  # noqa: E402


def test_q4_0_is_a_plan_not_a_run():
    payload = plan.run()
    assert payload["ns_solved"] is False
    assert payload["executed"] is False
    assert payload["da_approved"] is False
    assert payload["alpha_c_proxy_stamped"] is False
    assert payload["quartic_named_from_disk"] is False
    assert payload["quartic_54_46_on_this_tree"] is False
    assert payload["admission"] == {
        "alpha_c_near_one": True,
        "T_c_positive": True,
        "six_mode_only": True,
    }
    assert payload["plan_says_do_not_run"] is True
    assert payload["i3_weighted_imported"] is False
    assert payload["kkl_regrouping_imported"] is False
    assert payload["fiber_moved_off_neutral"] is False
    assert payload["gate_altered"] == {
        "sbp": False,
        "phi_vs_d": False,
        "low_tail_snapshot": False,
        "sign_realizability": False,
    }


def test_page_is_plan_only():
    page = (
        ROOT / "packets" / "DA-GATE-Q4-0-SIX-MODE-CALIBRATION-2026-09-25.md"
    ).read_text()
    assert page.startswith("# DA gate — Q4-0 six-mode calibration")
    assert "Do not run" in page
    assert r"\alpha_c\approx 1" in page
    assert r"T_c>0" in page
    assert "nonlinear force rotates against viscosity" in page
    assert "Written approval to execute" in page
    assert "NS is solved" not in page
    out = ROOT / "results" / "da_gate_q4_0_six_mode_plan.json"
    if not out.exists():
        plan.main()
    data = json.loads(out.read_text())
    assert data["executed"] is False
    assert data["da_approved"] is False
    assert data["ns_solved"] is False
