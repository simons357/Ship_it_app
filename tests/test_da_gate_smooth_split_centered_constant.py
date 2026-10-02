"""Smooth-split centered constant: instantaneous, not NSE regularity.

Unrestricted star stays dead. Time budget stays open. Locked gates
are not altered. NS not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import da_gate_smooth_split_centered_constant as gate  # noqa: E402


LOCKED = (
    "packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md",
    "packets/DA-GATE-PHI-VS-FROZEN-VARIANCE-2026-09-24.md",
    "packets/DA-GATE-LOW-TAIL-SNAPSHOT-2026-09-24.md",
    "packets/DA-GATE-ARITHMETIC-SIGN-REALIZABILITY-2026-09-24.md",
    "packets/DA-GATE-EXACT-SHELL-PERTURBATION-STAR-2026-09-26.md",
    "packets/DA-GATE-71E-BRANCH-ELIMINATE-2026-09-27.md",
    "packets/DA-GATE-83-RADICAL-TRAPPING-2026-09-27.md",
    "packets/DA-GATE-83-MINOR-FACTOR-2026-09-27.md",
)


def test_identities_sit_and_regularity_stays_open():
    payload = gate.run()
    assert payload["ns_solved"] is False
    assert payload["time_budget_proved"] is False
    assert payload["unrestricted_star_restored"] is False
    assert payload["crossover_stamped"] is False
    assert payload["optimized_C_computed"] is False
    assert payload["instantaneous_estimate_written"] is True
    assert payload["witness_C_gt_0p4_recomputed"] is False
    assert payload["all_identities_ok"] is True
    assert payload["split_inequalities_ok"] is True
    assert payload["six_mode_N_formula_ok"] is True
    assert payload["six_mode_LambdaN_quotient_decreases"] is True
    assert payload["constant_arithmetic"]["sum_ok"] is True
    assert payload["amgm"]["log_lambda_pack_ok"] is True
    assert payload["Fx"]["classical_implies_Fx"] is True
    six = {r["j"]: r for r in payload["six_mode"]}
    assert abs(six[3]["N"] + 14.0) < 1e-9
    assert abs(six[8]["N"] + 34.0) < 1e-9
    assert six[12]["Lambda_N_over_g_sqrtYDs"] < six[3]["Lambda_N_over_g_sqrtYDs"]
    assert payload["gate_altered"] == {
        "sbp": False,
        "phi_vs_d": False,
        "low_tail_snapshot": False,
        "sign_realizability": False,
        "s_pq": False,
        "local_star": False,
    }


def test_pages_do_not_claim_ns_or_a_time_budget():
    page = (ROOT / "docs" / "ns-recovery" / "SMOOTH-SPLIT-CENTERED-CONSTANT.md").read_text()
    card = (
        ROOT / "packets" / "DA-GATE-SMOOTH-SPLIT-CENTERED-CONSTANT-2026-10-02.md"
    ).read_text()
    assert page.startswith("# Finite universal centered constant")
    assert r"7+6M" in page.replace(" ", "") or r"7+6M_{\mathrm{mult}}" in page
    assert r"M_{\mathrm{mult}}" in page
    assert "not" in page.lower() and "regularity" in page.lower()
    assert "NS is solved" not in page
    assert "NS is solved" not in card
    assert "KILLED" in card
    assert "OPEN" in card
    assert "time budget" in page.lower() or "time budget" in card.lower()
    for rel in LOCKED:
        text = (ROOT / rel).read_text()
        assert "NS is solved" not in text
        assert "smooth-split" not in text
    out = ROOT / "results" / "da_gate_smooth_split_centered_constant.json"
    if not out.exists():
        gate.main()
    data = json.loads(out.read_text())
    assert data["ns_solved"] is False
    assert data["time_budget_proved"] is False
    assert data["unrestricted_star_restored"] is False
    assert data["all_identities_ok"] is True
