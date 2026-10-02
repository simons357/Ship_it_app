"""Low-tail snapshot: Phi moment rewrite sits; separated triad is the on-tree enemy.

TG not run. Snapshot freeze not mixed into SBP. NS not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import da_gate_low_tail_snapshot as snap  # noqa: E402
import da_gate_phi_vs_frozen_variance as cmp  # noqa: E402


def test_polynomial_and_on_tree_split():
    payload = snap.run()
    assert payload["ns_solved"] is False
    assert payload["taylor_green_measured"] is False
    assert payload["snapshot_only"] is True
    assert payload["do_not_mix_with_sbp_identity"] is True
    assert payload["all_identities_ok"] is True
    assert payload["polynomial"]["ok"] is True
    assert abs(snap.phi_poly(0.0, 2.0) - 16.0) < 1e-12
    assert abs(snap.phi_poly(2.0, 2.0)) < 1e-12
    assert abs(snap.phi_poly(1.0, 3.0) - cmp.phi(1.0, 3.0)) < 1e-12
    assert payload["v_n_min_m_equals_n"] is True
    assert payload["v_n_has_no_low_tail_at_a_0p4"] is True
    assert payload["separated_L_ge_4_has_low_tail"] is True
    assert payload["separated_Phi_low_tail_dominated"] is True
    assert payload["separated_L_e_approaches_one_third"] is True
    assert payload["core_bound_C_holds_on_comparable_band"] is True
    assert payload["note_triad"]["has_low_tail"] is False
    assert payload["separated"][-1]["L"] == 16
    assert payload["separated"][-1]["low_tail_share_of_Phi"] > 0.99


def test_page_is_snapshot_not_tg_and_does_not_claim_ns():
    page = (ROOT / "packets" / "DA-GATE-LOW-TAIL-SNAPSHOT-2026-09-24.md").read_text()
    assert page.startswith("# DA gate — low-tail snapshot")
    assert "SNAPSHOT" in page or "Snapshot" in page
    assert "not mixed" in page or "not substituted" in page
    assert "1/3" in page or r"\frac13" in page
    assert "not on this tree" in page
    assert "NS is solved" not in page
    data = json.loads((ROOT / "results" / "da_gate_low_tail_snapshot.json").read_text())
    assert data["ns_solved"] is False
    assert data["taylor_green_measured"] is False
    assert data["all_identities_ok"] is True
    assert data["separated_Phi_low_tail_dominated"] is True
