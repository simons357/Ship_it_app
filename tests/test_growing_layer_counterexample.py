"""Growing-layer family on the locked core. Unrestricted ★ is killed as a uniform bound.

NS not solved. Not a singular NSE solution.
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import growing_layer_counterexample as gl  # noqa: E402
import ns_lemma_star_core as core  # noqa: E402


def test_n1_to_n4_match_pr24_table():
    for n, claimed in gl.CLAIMED.items():
        rec = gl.record(n)
        assert rec["div_free"] and rec["real_valued"]
        assert rec["T_c_matches_formula"]
        assert abs(rec["T_c"] - claimed["T_c"]) < 1e-6 * claimed["T_c"]
        assert abs(rec["R_star"] - claimed["R_star"]) < 1e-12
        assert abs(rec["N"]) < 1e-8
        assert rec["D_s"] > 1
        assert rec["E"] == 4 * (2 * n + 1)


def test_R_star_grows_and_beats_elementary_lower():
    r1 = gl.record(1)
    r4 = gl.record(4)
    r8 = gl.record(8)
    assert r4["R_star"] > 3 * r1["R_star"]
    assert r8["R_star"] > 1.8 * r4["R_star"]
    assert r8["R_star"] > r8["elementary_lower"]
    assert r8["R_star"] / 8 > 0.0012


def test_not_a_single_shell_and_not_a_dilation():
    a = gl.growing_layer(1)
    b = gl.growing_layer(2)
    assert len(a.modes) == 18
    assert len(b.modes) == 30
    ra = core.R_star(a)["R_star"]
    rb = core.R_star(b)["R_star"]
    assert rb > ra * 1.5


def test_run_payload_does_not_claim_ns_solved():
    payload = gl.run()
    assert payload["ns_solved"] is False
    assert payload["singular_nse"] is False
    assert payload["unrestricted_lemma_star"] == "KILLED_as_uniform_bound_on_this_family"
    assert payload["claimed_n1_to_n4_match"] is True
