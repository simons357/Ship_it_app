"""phi_kappa / d_kappa comparison: (A)(B)(C) sit; low tail is the enemy.

TG not run. NS not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import da_gate_phi_vs_frozen_variance as gate  # noqa: E402


def test_ratio_identities_and_low_tail_enemy():
    payload = gate.run()
    assert payload["ns_solved"] is False
    assert payload["convention"] == "FROZEN_epoch"
    assert payload["do_not_mix_with_live_Lambda"] is True
    assert payload["taylor_green_measured"] is False
    assert payload["enemy"] == "LOW-FREQUENCY TAIL"
    assert payload["rally"] == "LOW-TAIL CAPACITY + CHARGE + EPOCH MOTION"
    assert payload["all_elementary_ok"] is True
    assert payload["ratio_identities"]["ok"] is True
    assert payload["f_decreasing"]["ok"] is True
    assert payload["asymptotics"]["ok"] is True
    assert payload["core_bound"]["ok"] is True
    assert payload["energy_does_not_pay"]["Phi_is_low_tail_dominated"] is True
    assert payload["energy_does_not_pay"]["energy_bound_forces_L_e_small"] is False
    kappa = 3.0
    assert abs(gate.ratio_B(1.0, kappa) - 5.0 / (8.0 * kappa * kappa)) < 1e-12
    assert abs(gate.C_ab(1.0) - 5.0 / 8.0) < 1e-12
    assert abs(gate.phi(0.0, 2.0) - 16.0) < 1e-12


def test_page_is_comparison_not_tg_and_does_not_claim_ns():
    page = (ROOT / "packets" / "DA-GATE-PHI-VS-FROZEN-VARIANCE-2026-09-24.md").read_text()
    assert page.startswith("# DA gate —")
    assert r"\tag{A}" in page
    assert r"\tag{B}" in page
    assert r"\tag{C}" in page
    assert "LOW-FREQUENCY TAIL" in page
    assert r"L_e" in page
    assert "Those data are not on this tree" in page or "not on this tree" in page
    assert "NS is solved" not in page
    data = json.loads((ROOT / "results" / "da_gate_phi_vs_frozen_variance.json").read_text())
    assert data["ns_solved"] is False
    assert data["taylor_green_measured"] is False
    assert data["all_elementary_ok"] is True
    assert data["enemy"] == "LOW-FREQUENCY TAIL"
