"""Gate 83 radical lock. 71E packets and locked gates are not altered.

NS not solved. Gate 81 census is not recomputed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import da_gate_83_radical_trapping as gate  # noqa: E402


LOCKED = (
    "packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md",
    "packets/DA-GATE-PHI-VS-FROZEN-VARIANCE-2026-09-24.md",
    "packets/DA-GATE-LOW-TAIL-SNAPSHOT-2026-09-24.md",
    "packets/DA-GATE-ARITHMETIC-SIGN-REALIZABILITY-2026-09-24.md",
    "packets/DA-GATE-EXACT-SHELL-PERTURBATION-STAR-2026-09-26.md",
    "packets/DA-GATE-71E-BRANCH-ELIMINATE-2026-09-27.md",
)


def test_gauge_volume_is_b2_lambda():
    g = gate.gauge_identity_check()
    assert g["identity_V_eq_b2_lambda"] is True
    assert abs(g["seated_det_abn"] - 3.0) < 1e-12


def test_71e_point_is_an_active_cube_zero():
    star = gate.exact_star_on_cube()
    assert star["vanishes"] is True
    assert star["activity"]["live"] is True
    assert star["activity"]["n_pairs"] == 16
    assert star["activity"]["dead_pairs"] == 0


def test_pages_lock_the_radical_question_and_do_not_claim_ns():
    proof = (ROOT / "docs" / "ns-recovery" / "GATE-83-RADICAL-TRAPPING.md").read_text()
    card = (
        ROOT / "packets" / "DA-GATE-83-RADICAL-TRAPPING-2026-09-27.md"
    ).read_text()
    assert proof.startswith("# Gate 83")
    assert "83.34" in proof
    assert "83.35" in card or r"h\lambda" in card or "h\\lambda" in card
    assert "Nullstellensatz" in proof
    assert "REPORTED" in proof
    assert "NS is solved" not in proof
    assert "NS is solved" not in card
    for rel in LOCKED:
        text = (ROOT / rel).read_text()
        assert "Gate 83" not in text
        assert "NS is solved" not in text


def test_run_does_not_invent_a_certificate_or_recompute_81():
    payload = gate.run(n_starts=8)
    assert payload["ns_solved"] is False
    assert payload["da_ns_2_open"] is True
    assert payload["unrestricted_star_restored"] is False
    assert payload["gate"] == "83"
    assert payload["cube_equations"]["n_I_act"] == 9
    assert payload["star_on_cube"]["vanishes"] is True
    assert payload["gate_81_census"]["recomputed_here"] is False
    assert payload["gate_81_census"]["status"] == "REPORTED"
    assert payload["decision"]["question_83_34"] in ("OPEN", "YES", "NO")
    if payload["decision"]["question_83_34"] != "YES":
        assert payload["decision"]["explicit_certificate"] is False
    assert payload["locked_gates_unaltered"]["gate_71e"] is True
    assert payload["all_checks_ok"] is True
    out = ROOT / "results" / "da_gate_83_radical_trapping.json"
    if not out.exists():
        gate.main()
    data = json.loads(out.read_text())
    assert data["ns_solved"] is False
    assert data["gate_81_census"]["recomputed_here"] is False
