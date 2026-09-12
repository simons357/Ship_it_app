#!/usr/bin/env python3
"""Smoke tests for uniform_rstar_attack (channel split + R_★ sanity)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "ns_attacks"))
from ns_lemma_star_core import R_star  # noqa: E402
from uniform_rstar_attack import (  # noqa: E402
    T_c_lambda_channels,
    amplitude_scaling_false_product_check,
    triad_packet_field,
)


def test_channel_sum_matches_Tc():
    rng = np.random.default_rng(0)
    f = triad_packet_field((1, 0, 0), (2, 1, 0), rng, amp_r=1.0)
    ch = T_c_lambda_channels(f, theta=1.0)
    assert ch["channel_sum_err"] < 1e-10, ch


def test_R_star_amplitude_invariant_and_false_product_scales():
    rng = np.random.default_rng(1)
    fp = amplitude_scaling_false_product_check(rng)
    rs = [r["R_star"] for r in fp["rows"] if r["R_star"] is not None]
    assert rs, "expected finite R_star rows"
    assert fp["R_star_relative_spread"] is not None
    assert fp["R_star_relative_spread"] < 1e-8
    prods = [r["abs_Tc_over_v2_X32"] for r in fp["rows"] if r["abs_Tc_over_v2_X32"]]
    assert prods and max(prods) > 0
    assert any(abs(r["T_c"]) > 1e-12 for r in fp["rows"])
    # a=0.25 vs a=8 → factor 32 if T_c≠0 (1/a scaling of false product)
    assert fp["false_product_ratio_max_over_min"] > 10


def test_R_star_finite_on_triad():
    rng = np.random.default_rng(2)
    f = triad_packet_field((1, 0, 0), (2, 1, 0), rng)
    rec = R_star(f, verify=True)
    assert not rec.get("vacuous_single_shell")
    assert rec["R_star"] != float("inf")
    assert rec["R_star"] >= 0.0


if __name__ == "__main__":
    test_channel_sum_matches_Tc()
    test_R_star_amplitude_invariant_and_false_product_scales()
    test_R_star_finite_on_triad()
    print("ok")
