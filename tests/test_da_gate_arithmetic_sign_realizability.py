"""Arithmetic sign gate: exact delta split sits; T^{(0)} is not silently live T.

Locked low-tail gates are not altered. Heavy family not invented. NS not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import da_gate_arithmetic_sign_realizability as gate  # noqa: E402


LOCKED = (
    "packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md",
    "packets/DA-GATE-PHI-VS-FROZEN-VARIANCE-2026-09-24.md",
    "packets/DA-GATE-LOW-TAIL-SNAPSHOT-2026-09-24.md",
)


def test_exact_split_and_no_silent_substitution():
    payload = gate.run()
    assert payload["ns_solved"] is False
    assert payload["heavy_neighboring_family_on_this_tree"] is False
    assert payload["B_prim_constructed"] is False
    assert payload["both_signs_obtained"] is False
    assert payload["A_N_plus_saved"] is False
    assert payload["gate_altered"] == {
        "sbp": False,
        "phi_vs_d": False,
        "low_tail_snapshot": False,
    }
    assert payload["all_identities_ok"] is True
    assert payload["static_frontier"] == "arithmetic sign realizability"
    assert payload["dynamic_frontier"] == "dangerous-state persistence"
    assert payload["outcomes"]["NO_NEIGHBOR"] == "own_category_not_sign_depletion"
    assert payload["notation_trap"]["silent_substitution_is_not_first_variation"] is True
    note = payload["exact_split"]["note_triad"]
    assert note["identity_ok"] is True
    assert note["silent_R2_equals_quadratic"] is True


def test_page_does_not_alter_locked_gates_or_claim_ns():
    page = (ROOT / "packets" / "DA-GATE-ARITHMETIC-SIGN-REALIZABILITY-2026-09-24.md").read_text()
    assert page.startswith("# DA gate — arithmetic sign realizability")
    assert r"L_{1,N}" in page
    assert r"R_{2,N}" in page
    assert "BOTH SIGNS" in page
    assert "NO NEIGHBOR" in page
    assert "A_N" in page or r"\mathcal A_N" in page
    assert "not on this tree" in page
    assert "NS is solved" not in page
    for rel in LOCKED:
        text = (ROOT / rel).read_text()
        assert "arithmetic sign realizability" not in text
        assert "NS is solved" not in text
    data = json.loads((ROOT / "results" / "da_gate_arithmetic_sign_realizability.json").read_text())
    assert data["ns_solved"] is False
    assert data["both_signs_obtained"] is False
    assert data["all_identities_ok"] is True
