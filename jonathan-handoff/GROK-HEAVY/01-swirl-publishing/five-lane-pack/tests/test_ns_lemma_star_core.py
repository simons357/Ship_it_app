"""Unit checks for preferred self-contained Lemma★ core (ns_lemma_star_core).

NS is NOT solved. These tests lock formulas / invariants only — not a proof of ★.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ns_attacks.ns_lemma_star_core import (
    D_s_cross_check,
    D_s_moment,
    D_s_variance_sum,
    R_star,
    T_c_direct,
    T_c_from_NM,
    enforce,
    field_energy,
    max_div_residual,
    max_reality_residual,
    moments,
    scale_field,
    single_shell_field,
    two_shell_field,
)


def test_D_s_moment_vs_direct_agree():
    f = two_shell_field(alpha=1, beta=5, amp_alpha=1.2, amp_beta=0.7)
    cross = D_s_cross_check(f)
    assert cross["agree_moment_variance"]
    assert abs(D_s_moment(f) - D_s_variance_sum(f)) < 1e-10
    assert abs(cross["D_s_moment"] - moments(f)["Ds"]) < 1e-12


def test_single_shell_vacuous():
    """Pure single shell: D_s≈0 and T_c≈0 (vacuous ★ case); R_star nan/undefined."""
    f = single_shell_field(alpha=2, amp=1.0)
    m = moments(f)
    assert abs(m["Ds"]) < 1e-12
    tc = T_c_from_NM(f)
    assert abs(tc) < 1e-10
    assert abs(T_c_direct(f)) < 1e-10
    r = R_star(f)
    assert not math.isfinite(r)  # D_s≈0 → undefined / vacuous handling


def test_amplitude_invariance_of_R_star():
    base = two_shell_field(alpha=1, beta=5, amp_alpha=1.0, amp_beta=0.55)
    r0 = R_star(base)
    assert math.isfinite(r0)
    for a in (0.2, 3.0, 11.0, 1e-2):
        r = R_star(scale_field(base, a))
        assert math.isfinite(r)
        assert abs(r - r0) < 1e-9


def test_reality_v_minus_k_is_conj():
    f = enforce(two_shell_field(alpha=1, beta=5))
    assert max_reality_residual(f) < 1e-12
    for k, v in f.items():
        mk = (-k[0], -k[1], -k[2])
        assert mk in f
        assert np.allclose(f[mk], np.conjugate(v), atol=1e-12)


def test_div_free_k_dot_v():
    f = enforce(two_shell_field(alpha=1, beta=5, amp_alpha=1.1, amp_beta=0.4))
    assert max_div_residual(f) < 1e-12
    for k, v in f.items():
        kk = np.array(k, dtype=np.float64)
        assert abs(np.dot(kk, v)) < 1e-10 * (1.0 + np.linalg.norm(v))


def test_T_c_direct_matches_NM():
    f = two_shell_field(alpha=1, beta=5, amp_alpha=1.0, amp_beta=0.8)
    assert abs(T_c_direct(f) - T_c_from_NM(f)) < 1e-9
