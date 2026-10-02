"""Half-spread candidate |T_c| <= C ||∇u||_3 √(Y D_s) is an attack, not a proof.

Unrestricted star stays dead. Locked gates are not altered. NS not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import da_gate_tc_l3_sqrt_yds as gate  # noqa: E402
import ns_lemma_star_core as core  # noqa: E402
import centered_drift_triad_test as cdt  # noqa: E402


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


def test_candidate_is_open_and_near_shell_obstructs_linear():
    payload = gate.run()
    assert payload["ns_solved"] is False
    assert payload["candidate_proved"] is False
    assert payload["unrestricted_star_restored"] is False
    assert payload["crossover_stamped"] is False
    assert payload["localized_bump_on_this_tree"] is False
    assert payload["all_identities_ok"] is True
    assert payload["parseval_ok"] is True
    assert payload["homogeneity_ratio_invariant"] is True
    assert payload["linear_in_Ds_obstructed_by_near_shell"] is True
    assert payload["sqrt_Ds_scale_finite_on_near_shell"] is True
    assert payload["new_ratio_bounded_on_near_shell"] is True
    assert payload["new_ratio_grows_on_v_n"] is False
    assert payload["v_n_kills_new_slot"] is False
    assert payload["uniform_C_proved"] is False
    assert payload["old_star_grows_on_v_n"] is True
    assert payload["quadrature_cannot_certify_kill"] is True
    assert payload["uniform_inequality_is_separate_obligation"] is True
    assert payload["small_case"]
    assert payload["certified_counterexample"] is False
    lanes = payload["small_case_lanes"]
    assert set(lanes) == {"near_single_shell", "separated_varied", "dense_packet"}
    for lane in lanes.values():
        assert lane["n"] >= 2
        assert lane["certified_counterexample"] is False
        assert lane["max_ratio_cert_upper"] is not None
    names = {row["name"] for row in payload["small_case"]}
    assert any(n.startswith("two_shell") or "near_shell" in n for n in names)
    assert any(n.startswith("separated_") for n in names)
    assert any("packet" in n or n.startswith("clustered_") or n.startswith("growing_layer") for n in names)
    note_l = payload["note_triad"]["ratio_cert_lower"]
    note_u = payload["note_triad"]["ratio_cert_upper"]
    note_q = payload["note_triad"]["ratio_l3"]
    assert note_l <= note_q + 1e-12 <= note_u + 1e-12
    assert payload["gate_altered"] == {
        "sbp": False,
        "phi_vs_d": False,
        "low_tail_snapshot": False,
        "sign_realizability": False,
        "s_pq": False,
        "local_star": False,
    }
    note = payload["note_triad"]
    assert abs(note["T_c"] - 16 / 5) < 1e-12
    assert note["grad_L2_matches_sqrt_X"] is True
    assert note["ratio_l3"] is not None and note["ratio_l3"] > 0
    ns = [r for r in payload["near_shell"] if not r.get("empty_closer")]
    assert ns[-1]["T_c_over_Ds"] > 2 * ns[0]["T_c_over_Ds"]
    assert abs(ns[-1]["T_c_over_sqrt_Ds"] / ns[0]["T_c_over_sqrt_Ds"] - 1) < 0.2
    vn = {row["n"]: row for row in payload["growing_layer"]}
    assert vn[8]["ratio_star"] > 2 * vn[1]["ratio_star"]


def test_grad_l2_recovers_X_on_note_triad():
    field = cdt.near_scale_triad()
    rec = core.R_star(field)
    grid = gate.physical_grad_norms(field, n=32)
    assert abs(grid["grad_L2"] ** 2 - rec["X"]) <= 1e-10 * max(1.0, rec["X"])
    assert abs(grid["E_phys"] - rec["E"]) <= 1e-10 * max(1.0, rec["E"])


def test_pages_do_not_claim_ns_or_a_proof():
    page = (ROOT / "docs" / "ns-recovery" / "TC-L3-SQRT-YDS.md").read_text()
    card = (ROOT / "packets" / "DA-GATE-TC-L3-SQRT-YDS-2026-10-01.md").read_text()
    assert page.startswith("# ")
    assert r"\|\nabla u\|_3" in page or r"\nabla u\|_3" in page
    assert r"\sqrt{YD_s}" in page or r"\sqrt{Y D_s}" in page
    assert "OPEN" in page
    assert "not unrestricted" in page.lower() or "not** unrestricted" in page.lower()
    assert "cannot certify" in page.lower()
    assert "does not establish" in page.lower() or "does not prove" in page.lower()
    assert "Nearly single-shell" in page or "near-single-shell" in page.lower() or "nearly single-shell" in page.lower()
    assert "separated" in page.lower()
    assert "coordinated" in page.lower() or "packet" in page.lower()
    assert "time budget" in page.lower() or "proof obligation" in page.lower()
    assert "NS is solved" not in page
    assert "NS is solved" not in card
    assert "cannot certify" in card.lower()
    assert "proved" not in card.lower() or "not proved" in card.lower()
    for rel in LOCKED:
        text = (ROOT / rel).read_text()
        assert "NS is solved" not in text
        assert r"|T_c|\le C\|\nabla u\|_3" not in text
    out = ROOT / "results" / "da_gate_tc_l3_sqrt_yds.json"
    if not out.exists():
        gate.main()
    data = json.loads(out.read_text())
    assert data["ns_solved"] is False
    assert data["candidate_proved"] is False
    assert data["unrestricted_star_restored"] is False
    assert data["all_identities_ok"] is True
