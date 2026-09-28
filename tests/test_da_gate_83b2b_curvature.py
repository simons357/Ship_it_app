"""Gate 83B-2b curvature. Polarization line on the 13/10 cube.

NS not solved. 71E packets and locked gates are not altered.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import da_gate_83b2b_curvature as gate  # noqa: E402
import sympy as sp


LOCKED = (
    "packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md",
    "packets/DA-GATE-71E-BRANCH-ELIMINATE-2026-09-27.md",
    "packets/DA-GATE-EXACT-SHELL-PERTURBATION-STAR-2026-09-26.md",
    "packets/DA-GATE-83-RADICAL-TRAPPING-2026-09-27.md",
    "packets/DA-GATE-83-MINOR-FACTOR-2026-09-27.md",
)


def test_exact_lattice_is_cocircular_and_volumetric():
    lat = gate.exact_lattice_identities()
    assert lat["cocircular"] is True
    assert lat["delta"] == "-6/25"
    assert lat["delta_nonzero"] is True
    assert lat["lam"] == "-12/5"
    assert lat["r"] == ["-1/2", "6/5", "6/5"]
    assert lat["b"] == ["1/2", "1/10"]
    for key in ("000", "100", "010", "001", "111"):
        assert lat["radii_squared"][key] == "169/100"


def test_raw_F_is_affine_in_each_zi():
    aff = gate.affinity_in_each_zi()
    assert aff["D2F_e_zi_e_zi_identically_zero"] is True
    assert aff["max_degree_in_zi"] == [1] * 8


def test_witness_line_has_rank_7_and_live_pairs():
    payload = gate.run()
    assert payload["ns_solved"] is False
    assert payload["da_ns_2_open"] is True
    assert payload["unrestricted_star_restored"] is False
    assert payload["global_rank8_trap"] == "FALSIFIED"
    assert payload["question_83_34"] == "OPEN"
    wit = payload["witness"]
    assert wit["activity"]["live"] is True
    assert wit["activity"]["dead_pairs"] == 0
    assert wit["activity"]["n_pairs"] == 16
    assert wit["rank_9x8"] == 7
    assert wit["z4_column_vanishes"] is True
    assert wit["z7_column_vanishes"] is False
    assert wit["line_is_exact_coherent"] is True
    assert wit["max_abs_raw"] < 1e-10
    assert abs(wit["ell_dot_d2"]) < 1e-10
    assert payload["all_checks_ok"] is True
    assert payload["boxed_obstruction"] == r"\ell^T D^2F[v,v] = 0"


def test_pages_do_not_claim_ns_or_close_83_34():
    proof = (ROOT / "docs" / "ns-recovery" / "GATE-83B2B-CURVATURE.md").read_text()
    card = (ROOT / "packets" / "DA-GATE-83B2B-CURVATURE-2026-09-28.md").read_text()
    assert proof.startswith("# Gate 83B-2b")
    assert r"\ell^T\mathrm{D}^2F[v,v]=0" in proof or r"\ell^T D^2F[v,v]=0" in card
    assert "NOT YET ESTABLISHED" in proof
    assert "83.34" in proof
    assert "NS is solved" not in proof
    assert "NS is solved" not in card
    for rel in LOCKED:
        text = (ROOT / rel).read_text()
        assert "83B-2b" not in text
        assert "NS is solved" not in text
    out = ROOT / "results" / "da_gate_83b2b_curvature.json"
    if not out.exists():
        gate.main()
    data = json.loads(out.read_text())
    assert data["ns_solved"] is False
    assert data["question_83_34"] == "OPEN"
    assert data["witness"]["rank_9x8"] == 7


def test_delta_is_exactly_minus_six_twenty_fifths():
    assert sp.simplify(gate.DELTA_EXACT) == -sp.Rational(6, 25)
