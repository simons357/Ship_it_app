"""Symmetrized triad split: identities sit; K(t) not written.

NS not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import centered_drift_triad_split as split  # noqa: E402
import centered_drift_triad_test as cdt  # noqa: E402


def test_note_triad_is_all_comparable_and_gamma_is_tau_r():
    rec = split.split_Tc(cdt.near_scale_triad())
    assert rec["split_residual"] < 1e-12
    assert abs(rec["T_comparable"] - 16 / 5) < 1e-12
    assert abs(rec["T_separated"]) < 1e-12
    assert abs(rec["T_hh_to_l"]) < 1e-12
    p, q = (1, 0, 0), (0, 1, 0)
    A = __import__("numpy").array([0.0, 1.0, 0.0], dtype=complex)
    B = __import__("numpy").array([1.0, 0.0, 1.0], dtype=complex)
    C = __import__("numpy").array([0.0, 0.0, 1.0], dtype=complex) * (-1j)
    assert abs(split.coupling_gamma(p, q, A, B, C) - 1.0) < 1e-12


def test_phase_sweep_max_is_the_note_triad():
    sweep = split.phase_sweep_near_scale(16)
    assert abs(sweep["max_Tc"] - 16 / 5) < 1e-12
    assert abs(sweep["min_Tc"] + 16 / 5) < 1e-12
    assert abs(sweep["max_Tc_over_Ds"] - 4 / 3) < 1e-12


def test_near_shell_ratio_blows_while_R_star_stays():
    summary = split.run()
    rows = summary["near_shell_eps"]
    assert len(rows) >= 3
    ratios = [r["ratio"] for r in rows]
    rstars = [r["R_star"] for r in rows]
    assert ratios[-1] > 2 * ratios[0]
    assert ratios[-1] > 8
    assert max(rstars) < 0.02
    assert abs(rstars[-1] - rstars[0]) < 0.002


def test_separated_is_not_the_obstruction():
    rec = split.split_Tc(cdt.separated_triad(8))
    assert rec["T_c"] / rec["D_s"] < 0.25
    assert abs(rec["T_separated"]) > abs(rec["T_comparable"])


def test_page_and_json_do_not_claim_a_K_or_ns():
    root = Path(__file__).resolve().parents[1]
    page = (root / "docs" / "ns-recovery" / "CENTERED-DRIFT-TRIAD-SPLIT.md").read_text()
    assert page.startswith("# Centered drift: symmetrized coefficient and channel split")
    assert "Not a closure theorem" in page
    assert "Tautological" in page
    assert "NS is solved" not in page
    data = json.loads((root / "results" / "centered_drift_triad_split.json").read_text())
    assert data["ns_solved"] is False
    assert "not written" in data["K_formula"]
