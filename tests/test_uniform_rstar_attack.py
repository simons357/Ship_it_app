#!/usr/bin/env python3
"""Smoke tests for uniform R_★ identities + channel split (close attempt)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "ns_attacks"))

from ns_lemma_star_core import R_star, moments  # noqa: E402
from uniform_rstar_attack import (  # noqa: E402
    T_c_lambda_channels,
    amplitude_scaling_false_product_check,
    triad_packet_field,
    two_shell_field,
)
from uniform_rstar_identities import (  # noqa: E402
    check_cauchy,
    check_two_shell_Ds,
    run as run_identities,
)


def test_channel_sum_matches_Tc():
    rng = np.random.default_rng(0)
    f = triad_packet_field((1, 0, 0), (2, 1, 0), rng, amp_r=1.0)
    ch = T_c_lambda_channels(f, theta=1.0)
    assert ch["channel_sum_err"] < 1e-10, ch


def test_cauchy_and_two_shell_Ds():
    rng = np.random.default_rng(3)
    f = triad_packet_field((1, 0, 0), (2, 1, 0), rng, amp_r=0.6)
    c = check_cauchy(f)
    assert c["cauchy_ok"], c
    d = check_two_shell_Ds(1, 2, rng)
    assert d["ok"], d


def test_identities_runner_status_open():
    payload = run_identities(seed=11)
    s = payload["summary"]
    assert s["lemma_A_cauchy_all_ok"]
    assert s["lemma_B_channel_all_ok"]
    assert s["lemma_C_two_shell_Ds_all_ok"]
    assert s["status"]["PRODUCT_BLOCK"] == "OPEN"
    assert s["status"]["Clay_Statement_B"] == "NOT_SOLVED"
    assert s["status"]["HL_LL_classical"] == "OPEN_not_filed"


def test_R_star_amplitude_invariant_and_false_product_scales():
    rng = np.random.default_rng(1)
    fp = amplitude_scaling_false_product_check(rng)
    rs = [r["R_star"] for r in fp["rows"] if r["R_star"] is not None]
    assert rs, "expected finite R_star rows"
    assert fp["R_star_relative_spread"] is not None
    assert fp["R_star_relative_spread"] < 1e-8
    prods = [r["abs_Tc_over_v2_X32"] for r in fp["rows"] if r["abs_Tc_over_v2_X32"]]
    assert prods and max(prods) > 0
    # If T_c ≠ 0, false product tracks ~1/a (a=0.25 vs a=8 → factor 32).
    # If the seed has T_c=0, ratios may be 0; require nontrivial abs(T_c) seed.
    assert any(abs(r["T_c"]) > 1e-12 for r in fp["rows"])
    assert fp["false_product_ratio_max_over_min"] > 10


def test_R_star_finite_on_triad_and_two_shell():
    rng = np.random.default_rng(2)
    f = triad_packet_field((1, 0, 0), (2, 1, 0), rng)
    rec = R_star(f, verify=True)
    assert not rec.get("vacuous_single_shell")
    assert rec["R_star"] != float("inf")
    assert rec["R_star"] >= 0.0
    f2 = two_shell_field(1, 2, rng, amp2=1.0, per_shell=3)
    E, X, Y, Z, Lam = moments(f2)
    assert E > 0 and X > 0


if __name__ == "__main__":
    test_channel_sum_matches_Tc()
    test_cauchy_and_two_shell_Ds()
    test_identities_runner_status_open()
    test_R_star_amplitude_invariant_and_false_product_scales()
    test_R_star_finite_on_triad_and_two_shell()
    print("ok")
