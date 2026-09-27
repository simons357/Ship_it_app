"""Gate 71E: isolated tuned active coherence on the 2x4 patch.

Locked gates are not altered. NS not solved.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import da_gate_71e_branch_eliminate as gate  # noqa: E402


LOCKED = (
    "packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md",
    "packets/DA-GATE-PHI-VS-FROZEN-VARIANCE-2026-09-24.md",
    "packets/DA-GATE-LOW-TAIL-SNAPSHOT-2026-09-24.md",
    "packets/DA-GATE-ARITHMETIC-SIGN-REALIZABILITY-2026-09-24.md",
    "packets/DA-GATE-EXACT-SHELL-PERTURBATION-STAR-2026-09-26.md",
)


def test_exact_star_is_fully_active_over_rationals():
    cert = gate.exact_star_certificate()
    assert cert["n_equations"] == 11
    assert cert["n_repeated_outputs"] == 7
    assert cert["n_live_pairs"] == 18
    assert cert["all_triples_exactly_zero"] is True
    assert cert["max_abs_triple"] == "0"
    assert cert["dead_pairs"] == 0
    assert cert["fully_active"] is True
    assert cert["on_branch_B"] is True
    assert cert["on_branch_A"] is False
    assert cert["cubic_holds"] is True
    assert cert["A"] == "182/19"
    assert cert["B"] == "0"
    assert Fraction(cert["min_W_norm2"]) > 0
    assert cert["z_star"] == [
        "3",
        "3/2",
        "1",
        "3/4",
        "9/11",
        "15/19",
        "21/31",
        "27/47",
    ]


def test_harmonic_first_row_satisfies_cubic_for_every_scale():
    alg = gate.algebraic_cubic_and_factors()
    assert alg["harmonic_first_row_satisfies_cubic"] is True
    modes = gate.patch_modes()
    groups = gate.repeated_outputs(modes)
    assert sum(g["m"] - 1 for g in groups) == 11
    # t=3 with the certified second row is the only scanned solution
    iso = gate.isolation_evidence(modes, groups)
    assert iso["t3_machine_zero"] is True
    assert iso["nearby_t_not_solutions"] is True
    assert iso["quadratic_departure"] is True
    assert iso["isolated"] is True


def test_projected_normal_is_not_a_solution():
    modes = gate.patch_modes()
    groups = gate.repeated_outputs(modes)
    pn = gate.projected_normal_point(modes, groups)
    assert pn["active"] is False
    act = gate.activity_from_z(gate.Z_STAR_FLOAT, modes, groups)
    assert act["active"] is True
    assert act["dead_pairs"] == 0
    assert act["min_unit_pair_norm"] > 1e-2


def test_pages_do_not_claim_ns_or_restore_unrestricted():
    proof = (ROOT / "docs" / "ns-recovery" / "GATE-71E-BRANCH-ELIMINATE.md").read_text()
    card = (
        ROOT / "packets" / "DA-GATE-71E-BRANCH-ELIMINATE-2026-09-27.md"
    ).read_text()
    assert proof.startswith("# Gate 71E")
    assert "Outcome B" in proof
    assert r"z^\star" in proof or "z^*" in proof
    assert "NS is solved" not in proof
    assert "NS is solved" not in card
    assert "KILLED" in card
    assert "isolated" in card.lower()
    for rel in LOCKED:
        text = (ROOT / rel).read_text()
        assert "Gate 71E" not in text
        assert "NS is solved" not in text


def test_run_classifies_outcome_b_and_writes_json():
    payload = gate.run(n_search_starts=8)
    assert payload["ns_solved"] is False
    assert payload["da_ns_2_open"] is True
    assert payload["unrestricted_star_restored"] is False
    assert payload["outcome"] == "B"
    assert payload["classification"] == "isolated_tuned_active"
    assert payload["empty_active"] is False
    assert payload["positive_dimensional_active"] is False
    assert payload["isolated_active"] is True
    assert payload["n_equations"] == 11
    assert payload["n_variables"] == 8
    assert payload["exact_star"]["fully_active"] is True
    assert payload["isolation"]["isolated"] is True
    assert payload["all_checks_ok"] is True
    assert payload["locked_gates_unaltered"]["local_exact_shell_star"] is True
    out = ROOT / "results" / "da_gate_71e_branch_eliminate.json"
    if not out.exists():
        gate.main()
    data = json.loads(out.read_text())
    assert data["ns_solved"] is False
    assert data["outcome"] == "B"
    assert data["all_checks_ok"] is True
