"""Focused unit checks for self-contained ns_lemma_star_core (user SoT paste).

NS is NOT solved. These tests lock formulas / invariants only — not a proof of ★.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ns_attacks.ns_lemma_star_core import (
    D_s_direct_form,
    D_s_moment_form,
    Field,
    R_star,
    T_c_direct,
    moments,
    project_onto_shell,
    random_shell_field,
    shell_wavevectors,
)


def _two_shell_field(amp_beta: float = 0.5) -> Field:
    """Finite-support field on Stokes shells |k|^2=1 and |k|^2=5."""
    f = Field()
    f.set_mode((1, 0, 0), np.array([0.0, 1.0, 0.0], dtype=complex))
    f.set_mode((2, 1, 0), amp_beta * np.array([0.0, 0.0, 1.0], dtype=complex))
    return f.normalize(1.0)


def _single_shell_field() -> Field:
    f = Field()
    f.set_mode((1, 0, 0), np.array([0.0, 1.0, 0.0], dtype=complex))
    return f.normalize(1.0)


def test_reality_v_minus_k_is_conj():
    f = _two_shell_field()
    for k in f.support():
        mk = tuple(-x for x in k)
        assert mk in f.modes
        assert np.allclose(f.get(mk), np.conjugate(f.get(k)), atol=1e-12)


def test_div_free_projection():
    f = Field()
    # Intentional parallel component must be killed by set_mode / project_perp.
    f.set_mode((1, 0, 0), np.array([3.0, 1.0, -2.0], dtype=complex))
    for k in f.support():
        kk = np.array(k, dtype=float)
        assert abs(np.dot(kk, f.get(k))) < 1e-12


def test_D_s_moment_vs_direct_agree_or_raise():
    f = _two_shell_field(0.7)
    E, X, Y, Z, Lambda = moments(f)
    Ds_m = D_s_moment_form(X, Y, Z)
    Ds_d = D_s_direct_form(f, Lambda)
    assert abs(Ds_m - Ds_d) <= 1e-9 * max(abs(Ds_m), abs(Ds_d), 1.0)
    # R_star itself raises on mismatch (verify=True).
    out = R_star(f, verify=True)
    assert out["D_s"] == pytest.approx(Ds_m, rel=0, abs=1e-12)


def test_single_shell_vacuous_R_star():
    f = _single_shell_field()
    E, X, Y, Z, Lambda = moments(f)
    assert abs(D_s_moment_form(X, Y, Z)) < 1e-12
    assert abs(T_c_direct(f, Lambda)) < 1e-10
    out = R_star(f)
    assert out["vacuous_single_shell"] is True
    assert out["R_star"] == 0.0  # Tc+ == 0 on pure single shell


def test_R_star_finite_on_two_shell():
    f = _two_shell_field(0.55)
    out = R_star(f)
    assert out["vacuous_single_shell"] is False
    assert math.isfinite(out["R_star"])
    assert out["R_star"] >= 0.0
    assert out["D_s"] > 0.0


def test_amplitude_invariance_of_R_star():
    base = _two_shell_field(0.55)
    r0 = R_star(base)["R_star"]
    for a in (0.2, 3.0, 11.0):
        r = R_star(base.scale(a))["R_star"]
        assert abs(r - r0) < 1e-9


def test_project_onto_shell_not_implemented():
    f = _single_shell_field()
    with pytest.raises(NotImplementedError):
        project_onto_shell(f, 5)


def test_random_shell_and_shell_wavevectors():
    ks = shell_wavevectors(5)
    assert all(sum(x * x for x in k) == 5 for k in ks)
    rng = np.random.default_rng(1390)
    f = random_shell_field(5, rng, target_E=1.0)
    assert abs(f.energy() - 1.0) < 1e-12
    out = R_star(f)
    assert "R_star" in out
