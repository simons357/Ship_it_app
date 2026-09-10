"""Counting and Cauchy–Schwarz bounds for exact-shell B(w,w) (Attack 9B/9D).

Locks the fixed-output exclusion:

  p+q=k  ⇒  q=k-p   (at most m ordered pairs per output)
  |B̂_k| ≤ |k| ||w||₂²   (incompressibility + CS; all phases/pols)
  K_{α,β}(w) ≤ s (β/α)² ≤ 16 s   (s = occupied output keys on shell β)

Does not prove Lemma★. NS is not solved.
"""

from __future__ import annotations

import math
from typing import Iterable, Set

import numpy as np

from ns_attacks.stokes_moments import Field, ModeKey, k_norm2, leray_project, nonlinear_B


def ordered_pairs_onto_k(support: Iterable[ModeKey], k: ModeKey) -> int:
    """Number of ordered pairs (p,q) in support with p+q=k. At most |support|."""
    S: Set[ModeKey] = set(support)
    n = 0
    for p in S:
        q = (k[0] - p[0], k[1] - p[1], k[2] - p[2])
        if q in S:
            n += 1
    return n


def max_ordered_pairs_per_output(support: Iterable[ModeKey], outputs: Iterable[ModeKey]) -> int:
    S = list(support)
    if not S:
        return 0
    return max((ordered_pairs_onto_k(S, k) for k in outputs), default=0)


def occupied_output_count(field: Field, tol: float = 1e-14) -> int:
    return sum(1 for v in field.values() if float(np.vdot(v, v).real) > tol)


def cs_mode_bound(k: ModeKey, energy: float) -> float:
    """|k| ||w||₂²."""
    return math.sqrt(k_norm2(k)) * energy


def beta_from_two_alpha_inputs_max(alpha: float) -> float:
    """|p+q|² ≤ 4α when |p|²=|q|²=α."""
    return 4.0 * alpha


def K_cs_fixed_s(s: int, alpha: float, beta: float) -> float:
    """K ≤ s (β/α)² ≤ 16s."""
    if alpha <= 0:
        return float("nan")
    return s * (beta / alpha) ** 2


def check_cs_pointwise(w: Field, Buu: Field | None = None, rtol: float = 1e-9, atol: float = 1e-12) -> bool:
    """|B̂_k| ≤ |k| ||w||₂² on occupied outputs of B(w,w)."""
    if Buu is None:
        Buu = nonlinear_B(w)
    energy = sum(float(np.vdot(v, v).real) for v in w.values())
    for k, bk in Buu.items():
        nrm = float(np.linalg.norm(bk))
        cap = cs_mode_bound(k, energy)
        if nrm > cap * (1.0 + rtol) + atol:
            return False
    return True


def occupied_shell_keys(PiB: Field, beta: float, tol: float = 1e-12) -> list[ModeKey]:
    keys = []
    for k, v in PiB.items():
        if abs(k_norm2(k) - beta) > 1e-9:
            continue
        if float(np.vdot(v, v).real) > tol:
            keys.append(k)
    return keys


def observed_C_alpha_over_sqrt_beta(PiB_L2: float, alpha: float, beta: float, energy: float) -> float:
    """C such that ||Π_β B||₂ = C (α/√β) ||w||₂². Uniform target is sup C < ∞."""
    if energy <= 0 or alpha <= 0 or beta <= 0:
        return float("nan")
    return PiB_L2 * math.sqrt(beta) / (alpha * energy)
