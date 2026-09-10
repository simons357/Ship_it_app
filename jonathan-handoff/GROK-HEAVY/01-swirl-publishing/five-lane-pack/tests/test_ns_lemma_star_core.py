"""Focused unit checks for self-contained ns_lemma_star_core (SoT identities).

NS is NOT solved. Lemma★ remains OPEN. This module locks exact finite-support
numerics; it does not prove or kill ★.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from unittest import mock

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ns_attacks.ns_lemma_star_core import (  # noqa: E402
    D_s_direct_form,
    D_s_moment_form,
    Field,
    R_star,
    moments,
    project_perp,
)


def _two_shell_field() -> Field:
    """Two modes on distinct shells (|k|^2 = 1 and 5)."""
    f = Field()
    f.set_mode((1, 0, 0), np.array([0.0, 1.0, 0.2], dtype=complex))
    f.set_mode((2, 1, 0), np.array([0.3, -0.1, 0.5j], dtype=complex))
    return f


def test_reality_condition_v_neg_k_is_conj():
    f = Field()
    w = np.array([1.0 + 2.0j, -0.5 + 0.1j, 0.3 - 0.7j], dtype=complex)
    f.set_mode((1, 2, 0), w)
    vk = f.get((1, 2, 0))
    vnk = f.get((-1, -2, 0))
    assert np.allclose(vnk, np.conj(vk))
    # set_mode projects first; conj pair uses the projected mode
    assert np.allclose(f.modes[(-1, -2, 0)], np.conj(f.modes[(1, 2, 0)]))


def test_div_free_projection():
    k = (3, 1, -1)
    w = np.array([4.0, -2.0, 1.5], dtype=complex)  # not perp to k
    f = Field()
    f.set_mode(k, w)
    vk = f.get(k)
    kf = np.array(k, dtype=float)
    assert abs(np.dot(kf, vk)) < 1e-12
    # project_perp is idempotent on the stored mode
    assert np.allclose(project_perp(k, vk), vk)


def test_Ds_moment_vs_direct_mismatch_raises():
    f = _two_shell_field()
    E, X, Y, Z, Lambda = moments(f)
    assert abs(D_s_moment_form(X, Y, Z) - D_s_direct_form(f, Lambda)) < 1e-12

    with mock.patch(
        "ns_attacks.ns_lemma_star_core.D_s_direct_form",
        return_value=D_s_moment_form(X, Y, Z) + 1.0,
    ):
        with pytest.raises(RuntimeError, match="D_s cross-check FAILED"):
            R_star(f, verify=True, tol=1e-6)


def test_single_shell_vacuous_R_star_zero_when_Tc_plus_zero():
    f = Field()
    f.set_mode((1, 0, 0), np.array([0.0, 1.0, 0.0], dtype=complex))
    f.set_mode((0, 1, 0), np.array([1.0, 0.0, 0.0], dtype=complex))
    # Both modes on shell |k|^2 = 1
    out = R_star(f)
    assert out["vacuous_single_shell"] is True
    assert out["D_s"] <= 1e-14
    assert max(out["T_c"], 0.0) == 0.0
    assert out["R_star"] == 0.0


def test_R_star_finite_on_two_shell_field():
    f = _two_shell_field()
    out = R_star(f)
    assert out["vacuous_single_shell"] is False
    assert out["D_s"] > 1e-14
    assert math.isfinite(out["R_star"])
    assert out["R_star"] >= 0.0
    # Internal D_s cross-check already passed (no raise)
    E, X, Y, Z, Lambda = moments(f)
    assert abs(out["E"] - E) < 1e-14
    assert abs(out["Lambda"] - Lambda) < 1e-14
