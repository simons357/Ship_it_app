"""Coplanar half-turn 2D3C fixed-point space.

n = (0, 1, −1)/√2,  P = n⊥ = {k : k_y = k_z},
R = 2nnᵀ − I.

S = {u : supp û ⊂ P,  û_k = R conj(û_k)} is invariant for NS
and every symmetric Galerkin cube. It is a separately regular
2D3C sector, not a dangerous genuinely 3-D lock.

NS is not solved.
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

import numpy as np

from ns_attacks.fourier import Mode, leray
from ns_attacks.galerkin import Field
from ns_attacks.phase_network import SEED_K, SEED_P, SEED_Q, SEED_SIGMA, monomial

N_VEC = np.array([0.0, 1.0, -1.0]) / math.sqrt(2.0)
R_MAT = np.array([[-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, -1.0, 0.0]])


def in_plane(k: Mode) -> bool:
    return int(k[1]) == int(k[2])


def rotate_wave(k: Mode) -> Mode:
    """Rk. On P this is −k."""
    v = R_MAT @ np.array(k, dtype=float)
    return (int(round(v[0])), int(round(v[1])), int(round(v[2])))


def project_to_S(vec: np.ndarray, k: Mode) -> np.ndarray:
    v = leray(k, np.array(vec, dtype=complex))
    for _ in range(8):
        v = 0.5 * (v + R_MAT @ np.conjugate(v))
        v = leray(k, v)
    return v


def s_residual(field: Field) -> float:
    worst = 0.0
    for k, uk in field.u.items():
        if not in_plane(k):
            worst = max(worst, float(np.linalg.norm(uk)))
            continue
        worst = max(worst, float(np.linalg.norm(uk - R_MAT @ np.conjugate(uk))))
    return worst


def off_plane_energy(field: Field) -> float:
    e = 0.0
    for k, uk in field.u.items():
        if not in_plane(k):
            e += float(np.vdot(uk, uk).real)
    return e


def locked_seed(
    ak: complex = 1.0j,
    ap: complex = 0.7j,
    aq: complex = -1.2j,
) -> Field:
    """Tracked (++−) channel in the planar gauge; already lies in S."""
    amps: Dict[Tuple[Mode, int], complex] = {
        (SEED_K, SEED_SIGMA[0]): ak,
        (SEED_P, SEED_SIGMA[1]): ap,
        (SEED_Q, SEED_SIGMA[2]): aq,
    }
    f = Field().from_amplitudes(amps, planar_n=N_VEC, reality=True)
    # Project in case a caller passes non-imaginary amplitudes.
    for k in list(f.u):
        f.set(k, project_to_S(f.get(k), k))
    f.enforce_reality()
    return f


def all_raw_W_imaginary_parts(field: Field, modes: Sequence[Mode]) -> List[float]:
    """Im W for every signed planar channel. Must vanish on S."""
    from ns_attacks.phase_network import enumerate_triads

    out: List[float] = []
    planar = [k for k in modes if in_plane(k)]
    for k, p, q in enumerate_triads(planar):
        for sk in (1, -1):
            for sp in (1, -1):
                for sq in (1, -1):
                    mon = monomial(field, k, p, q, (sk, sp, sq), planar_n=N_VEC)
                    out.append(abs(mon["W"].imag))
    return out


def tracked_W(field: Field) -> complex:
    mon = monomial(field, SEED_K, SEED_P, SEED_Q, SEED_SIGMA, planar_n=N_VEC)
    return mon["W"]


def signed_subspace_energy(field: Field, sigma: Sequence[int] = SEED_SIGMA) -> Tuple[float, float]:
    """Energy in the tracked signed-helicity pair vs the rest, on the seed six modes."""
    keep = {
        (SEED_K, sigma[0]),
        (SEED_P, sigma[1]),
        (SEED_Q, sigma[2]),
        ((-SEED_K[0], -SEED_K[1], -SEED_K[2]), sigma[0]),
        ((-SEED_P[0], -SEED_P[1], -SEED_P[2]), sigma[1]),
        ((-SEED_Q[0], -SEED_Q[1], -SEED_Q[2]), sigma[2]),
    }
    inside = 0.0
    total = field.total_energy()
    for (k, s) in keep:
        a = field.amplitude(k, s, planar_n=N_VEC)
        inside += abs(a) ** 2
    return inside, total
