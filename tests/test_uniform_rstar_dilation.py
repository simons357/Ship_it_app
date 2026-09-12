#!/usr/bin/env python3
"""Smoke tests for dilation-invariant uniform R_★ structure lemmas."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "ns_attacks"))

from ns_lemma_star_core import R_star  # noqa: E402
from uniform_rstar_attack import triad_packet_field  # noqa: E402
from uniform_rstar_dilation import (  # noqa: E402
    dilate_field,
    naive_lambda_power_not_invariant,
    run as run_dilation,
    scaling_ledger,
    signed_weight_structure,
    two_shell_dichotomy,
)


def test_dilation_preserves_R_star_and_Q():
    rng = np.random.default_rng(7)
    f = triad_packet_field((1, 0, 0), (2, 1, 0), rng, amp_r=0.9)
    rec0 = R_star(f, verify=True)
    assert not rec0.get("vacuous_single_shell")
    led = scaling_ledger(f, 3)
    assert led["ok_moment_powers"], led
    assert led["ok_R_star_invariant"], led
    assert led["ok_Q_invariant"], led
    f3 = dilate_field(f, 3)
    rec3 = R_star(f3, verify=True)
    assert abs(float(rec0["R_star"]) - float(rec3["R_star"])) < 1e-10


def test_two_shell_dichotomy_and_signed_weights():
    rng = np.random.default_rng(9)
    d = two_shell_dichotomy(1, 5, rng, theta=1.0)
    assert d["dichotomy_ok"], d
    assert d["only_high_child_feeds_Tc_plus"], d
    assert d["weight_alpha"] < 0 < d["weight_beta"]
    signed = signed_weight_structure(rng)
    assert signed["ok"], signed


def test_naive_lambda_route_not_invariant():
    rng = np.random.default_rng(11)
    out = naive_lambda_power_not_invariant(rng)
    assert out["ok"], out
    assert out["rho_not_invariant"]
    assert out["R_star_invariant"]


def test_dilation_runner_status_open():
    payload = run_dilation(seed=13)
    s = payload["summary"]
    assert s["lemma_G_dilation_ledger_ok"]
    assert s["lemma_H_I_J_two_shell_signed_ok"]
    assert s["lemma_I_naive_lambda_route_killed"]
    assert s["status"]["PRODUCT_BLOCK"] == "OPEN"
    assert s["status"]["Clay_Statement_B"] == "NOT_SOLVED"
    assert s["status"]["HH_bound"] == "OPEN"
    assert s["status"]["HL_LL_geometric_bound"] == "OPEN"


if __name__ == "__main__":
    test_dilation_preserves_R_star_and_Q()
    test_two_shell_dichotomy_and_signed_weights()
    test_naive_lambda_route_not_invariant()
    test_dilation_runner_status_open()
    print("ok")
