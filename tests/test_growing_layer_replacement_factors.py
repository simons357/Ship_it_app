"""Replacement-factor diagnostics on v_n. Not a theorem.

NS not solved. Not a singular NSE solution.
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import growing_layer_replacement_factors as rf  # noqa: E402


def test_aspect_is_exactly_six_so_bounded_aspect_still_contains_family():
    for n in (1, 2, 3, 4):
        row = rf.factor_row(n)
        assert row["lambda_min_is_n2"]
        assert row["lambda_max_is_6n2"]
        assert row["aspect_is_6"]
        assert row["n_shells"] >= 3
        assert row["R_star"] > 0


def test_sqrt_moment_ratios_do_not_climb_like_R_star():
    r1 = rf.factor_row(1)
    r4 = rf.factor_row(4)
    r8 = rf.factor_row(8)
    assert r8["R_star"] > 6 * r1["R_star"]
    assert r8["R_star_over_sqrt_X_over_E"] < r1["R_star_over_sqrt_X_over_E"]
    assert r8["R_star_over_sqrt_lambda_max"] < r1["R_star_over_sqrt_lambda_max"]
    assert r4["R_star_times_aspect"] > r1["R_star_times_aspect"]


def test_payload_refuses_ns_and_refuses_aspect_repair():
    payload = rf.run(ns=(1, 2, 3, 4))
    assert payload["ns_solved"] is False
    assert payload["singular_nse"] is False
    assert payload["bounded_aspect_excludes_v_n"] is False
    assert payload["all_aspect_6"] is True
    assert payload["R_star_climbs"] is True
    assert payload["R_over_sqrt_XE_does_not_climb_like_R"] is True
