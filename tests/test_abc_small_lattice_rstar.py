"""Small-lattice ABC envelope vs locked D_s, T_c, R★.

NS not solved. Lemma★ OPEN. Not a kill.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import abc_small_lattice_rstar as abc  # noqa: E402
import ns_lemma_star_core as core  # noqa: E402


def test_pure_abc_is_one_shell_vacuous():
    f = abc.localized_abc_truncated(lam=2, R=0)
    rec = core.R_star(f)
    assert rec["vacuous_single_shell"]
    assert abs(rec["D_s"]) < 1e-12
    assert abs(rec["T_c"]) < 1e-12
    assert rec["R_star"] == 0.0


def test_envelope_is_div_free_and_real():
    f = abc.localized_abc_truncated(lam=2, R=1)
    h = abc.hygiene(f)
    assert h["div_free"]
    assert h["real_valued"]
    assert h["n_modes"] > 6


def test_locked_R_star_and_odd_Tc():
    rec = abc.record(abc.localized_abc_truncated(lam=1, R=1))
    assert rec["odd_Tc"]
    assert rec["E"] > 0.999 and rec["E"] < 1.001
    # Canonical R★ is (Tc)_+; signed matches the reverse when Tc<0.
    if rec["T_c"] < 0:
        assert rec["R_star"] == 0.0
        assert rec["R_star_reversed"] == rec["R_signed"] or math.isclose(
            rec["R_star_reversed"], rec["R_signed"], rel_tol=1e-10, abs_tol=1e-15
        )
    else:
        assert rec["R_star"] == rec["R_signed"] or math.isclose(
            rec["R_star"], rec["R_signed"], rel_tol=1e-10, abs_tol=1e-15
        )


def test_dilation_leaves_signed_R_flat():
    f = abc.localized_abc_truncated(lam=1, R=1)
    r1 = abc.record(f)["R_signed"]
    r2 = abc.record(abc.dilate(f, 2))["R_signed"]
    assert abs(r1 - r2) <= 1e-12 * max(abs(r1), 1.0)


def test_run_does_not_stamp_kill():
    payload = abc.run()
    assert payload["ns_solved"] is False
    assert payload["lemma_star"] == "OPEN"
    assert payload["evaluator_not_proof"] is True
    assert all(r["div_free"] and r["real_valued"] for r in payload["rows"])
    # Finite values only. A climb flag is a clue, not a kill.
    assert "Not a kill" in payload["verdict"]
