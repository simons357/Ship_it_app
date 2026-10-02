"""Local exact-shell perturbation star. Unrestricted star stays dead.

Locked gates are not altered. NS not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import da_gate_exact_shell_perturbation_star as gate  # noqa: E402


LOCKED = (
    "packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md",
    "packets/DA-GATE-PHI-VS-FROZEN-VARIANCE-2026-09-24.md",
    "packets/DA-GATE-LOW-TAIL-SNAPSHOT-2026-09-24.md",
    "packets/DA-GATE-ARITHMETIC-SIGN-REALIZABILITY-2026-09-24.md",
)


def test_local_star_sits_and_unrestricted_stays_dead():
    payload = gate.run()
    assert payload["ns_solved"] is False
    assert payload["unrestricted_star_restored"] is False
    assert payload["local_star_proved"] is True
    assert payload["crossover_stamped"] is False
    assert payload["attainment_asserted"] is False
    assert abs(payload["C_beta_inv_half"] - 4.0 / 3.0) < 1e-15
    assert abs(payload["K_ceiling"] - 16.0 / 9.0) < 1e-15
    assert payload["polynomial"]["identity_ok"] is True
    assert payload["polynomial"]["bound_is_16_over_9"] is True
    assert payload["polynomial"]["C_is_4_over_3"] is True
    assert payload["incidence"]["fiber_at_most_two"] is True
    assert payload["incidence"]["sum_L2_le_3_F2"] is True
    assert payload["three_shear"]["covers_9"] is True
    assert abs(payload["three_shear"]["K"] - 2.0 / 3.0) < 1e-12
    assert payload["extreme_satellites"]["r_near_0"] is True
    assert payload["extreme_satellites"]["r_at_4"] is True
    assert payload["perturbation"]["leading_matches_K"] is True
    assert payload["unrestricted"]["unrestricted_star_killed"] is True
    assert payload["all_identities_ok"] is True
    assert payload["gate_altered"] == {
        "sbp": False,
        "phi_vs_d": False,
        "low_tail_snapshot": False,
        "sign_realizability": False,
        "s_pq": False,
    }


def test_pages_do_not_claim_ns_or_restore_unrestricted():
    proof = (ROOT / "docs" / "ns-recovery" / "EXACT-SHELL-PERTURBATION-STAR.md").read_text()
    card = (
        ROOT / "packets" / "DA-GATE-EXACT-SHELL-PERTURBATION-STAR-2026-09-26.md"
    ).read_text()
    assert proof.startswith("# Exact-shell perturbation")
    assert r"\frac43" in proof
    assert r"\beta^{-1/2}" in proof
    assert "not unrestricted" in proof.lower() or "not** unrestricted" in proof.lower()
    assert "NS is solved" not in proof
    assert "NS is solved" not in card
    assert "KILLED" in card
    for rel in LOCKED:
        text = (ROOT / rel).read_text()
        assert "exact-shell perturbation ★" not in text
        assert "NS is solved" not in text
    out = ROOT / "results" / "da_gate_exact_shell_perturbation_star.json"
    if not out.exists():
        gate.main()
    data = json.loads(out.read_text())
    assert data["ns_solved"] is False
    assert data["unrestricted_star_restored"] is False
    assert data["all_identities_ok"] is True
