"""First adversarial triad test for centered drift.

Exact finite-triad checkpoint. Not a closure theorem.
NS is not solved.
"""

from __future__ import annotations

import math
from typing import Dict, Tuple

import numpy as np

import ns_lemma_star_core as core

Mode = Tuple[int, int, int]


def near_scale_triad() -> core.Field:
    """Section 4 field: p=(1,0,0), q=(0,1,0), r=(1,1,0)."""
    field = core.Field()
    p, q, r = (1, 0, 0), (0, 1, 0), (1, 1, 0)
    a = np.array([0.0, 1.0, 0.0], dtype=complex)
    b = np.array([1.0, 0.0, 1.0], dtype=complex)
    c = np.array([0.0, 0.0, 1.0], dtype=complex)
    field.set_mode(p, a)
    field.set_mode(q, b)
    field.set_mode(r, -1j * c)
    return field


def separated_triad(L: int) -> core.Field:
    """Section 5 field: same a,b; unit c_L along P_r((q·a)b+(p·b)a)."""
    if L < 2:
        raise ValueError("L must be >= 2")
    field = core.Field()
    p, q, r = (1, 0, 0), (0, L, 0), (1, L, 0)
    a = np.array([0.0, 1.0, 0.0], dtype=complex)
    b = np.array([1.0, 0.0, 1.0], dtype=complex)
    q_dot_a = float(np.dot(np.array(q, dtype=float), a.real))
    p_dot_b = float(np.dot(np.array(p, dtype=float), b.real))
    raw = q_dot_a * b + p_dot_b * a
    c = core.project_perp(r, raw)
    nrm = float(np.linalg.norm(c))
    if nrm < 1e-15:
        raise ValueError("vanishing closing polarization")
    field.set_mode(p, a)
    field.set_mode(q, b)
    field.set_mode(r, -1j * (c / nrm))
    return field


def modal_tau(field: core.Field) -> Dict[Mode, float]:
    out: Dict[Mode, float] = {}
    for k, vk in field.modes.items():
        Bk = core.B_hat_at(field, k)
        out[k] = -float(np.real(np.dot(Bk, np.conj(vk))))
    return out


def record(field: core.Field) -> dict:
    E, X, Y, Z, Lambda = core.moments(field)
    Ds = core.D_s_moment_form(X, Y, Z)
    tau = modal_tau(field)
    N = 0.0
    M = 0.0
    for k, tk in tau.items():
        ell = core.lam(k)
        N += ell * tk
        M += ell * ell * tk
    Tc = M - Lambda * N
    Tc_direct = core.T_c_direct(field, Lambda)
    return {
        "E": E,
        "X": X,
        "Y": Y,
        "Z": Z,
        "Lambda": Lambda,
        "D_s": Ds,
        "N": N,
        "M": M,
        "T_c": Tc,
        "T_c_direct": Tc_direct,
        "tau": tau,
        "div_free": all(
            abs(np.dot(np.array(k, dtype=float), vk)) < 1e-12
            for k, vk in field.modes.items()
        ),
        "real": all(
            np.allclose(field.modes[tuple(-x for x in k)], np.conj(vk))
            for k, vk in field.modes.items()
        ),
        "ns_solved": False,
    }


def f_lambda(a: float, Lambda: float) -> float:
    return a * (a - Lambda)


def spectral_gap_factor(a: float, b: float, Lambda: float) -> float:
    return (a - b) * (a + b - Lambda)
