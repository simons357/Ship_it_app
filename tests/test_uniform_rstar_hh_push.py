#!/usr/bin/env python3
"""Smoke tests for HH-push lemmas K–M (Cauchy-route block)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "ns_attacks"))

from uniform_rstar_attack import two_shell_field  # noqa: E402
from uniform_rstar_hh_push import (  # noqa: E402
    check_lemma_K_hh_mass,
    face_family_probe,
    face_field,
    Q_B,
    run as run_hh_push,
    safe_R_star,
)


def test_lemma_K_hh_mass_on_two_shell():
    rng = np.random.default_rng(5)
    f = two_shell_field(1, 8, rng, amp2=0.7, per_shell=3)
    for theta in (1.5, 2.0, 3.0):
        row = check_lemma_K_hh_mass(f, theta=theta)
        assert row["ok"], row


def test_face_family_blocks_cauchy_sufficient_scale():
    # Light K_max for CI time; still enough to exceed sparse O(1) folklore.
    face = face_family_probe(K_max=6)
    assert face["monotone_Q_through_Kmax"], face
    assert face["Q_at_Kmax"] > 1.0, face
    assert face["cauchy_sufficient_strategically_blocked"]
    # R_★ / T_c vanish on deterministic e2 face fields
    f = face_field(5)
    rs = safe_R_star(f)
    assert abs(rs["T_c"]) < 1e-12
    assert Q_B(f) > 0.9


def test_hh_push_runner_status_open():
    payload = run_hh_push(seed=11, K_max=5)
    s = payload["summary"]
    assert s["lemma_K_hh_mass_all_ok"]
    assert s["status"]["PRODUCT_BLOCK"] == "OPEN"
    assert s["status"]["Clay_Statement_B"] == "NOT_SOLVED"
    assert s["status"]["HH_bound"] == "OPEN"
    assert s["status"]["publisher_X_gate"] == "CLOSED_until_real_proof"
    assert s["lemma_L_face"]["cauchy_sufficient_strategically_blocked"]
