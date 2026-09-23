"""K-candidate score sheet: uniform slots die; no proved K.

NS not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import centered_drift_k_candidates as kcand  # noqa: E402


def test_uniform_slots_grow_on_v_n_and_young_is_packaging():
    payload = kcand.run()
    assert payload["ns_solved"] is False
    assert payload["K_formula_proved"] is None
    assert payload["K_formula"] == "not written"
    assert payload["comparable_class_contains_v_n"] is True
    assert payload["v_n_aspect"] == 6
    assert payload["all_uniform_slots_grow_on_v_n"] is True
    assert payload["all_young_covers"] is True
    note = payload["note_triad"]
    assert abs(note["T_c"] - 16 / 5) < 1e-12
    assert abs(note["K_taut"] - 0.2) < 1e-12
    assert note["young_covers"] is True
    vn = {row["n"]: row for row in payload["growing_layer"]}
    assert vn[1]["K_taut"] == 0.0
    assert vn[8]["K_taut"] == 0.0
    assert vn[8]["T_c_over_E"] > 2 * vn[1]["T_c_over_E"]
    assert vn[8]["T_c_over_EY"] > 2 * vn[1]["T_c_over_EY"]
    assert vn[8]["K_inst"] > 2 * vn[1]["K_inst"]
    rows = payload["near_shell"]
    assert rows[-1]["T_c_over_Ds"] > 2 * rows[0]["T_c_over_Ds"]
    assert abs(rows[-1]["R_star"] - rows[0]["R_star"]) < 0.002


def test_page_and_json_do_not_claim_a_K_or_ns():
    page = (ROOT / "docs" / "ns-recovery" / "CENTERED-DRIFT-K-CANDIDATES.md").read_text()
    assert page.startswith("# Centered drift: \(K\)-candidate score sheet")
    assert "Not a closure theorem" in page
    assert "No non-tautological" in page
    assert "NS is solved" not in page
    assert "Clay is solved" not in page
    data = json.loads((ROOT / "results" / "centered_drift_k_candidates.json").read_text())
    assert data["ns_solved"] is False
    assert data["K_formula_proved"] is None
    assert data["K_formula"] == "not written"
    assert data["all_uniform_slots_grow_on_v_n"] is True
