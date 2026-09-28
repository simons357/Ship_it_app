"""Frozen logarithmic charge identities.

C_e = log(X / (κ_e H_a))

    C_e' = 2N/X − 2 Q_a / H_a + 2ν (D_a/H_a − Λ)

    G_θ = T_c/Y − θ ν D_s/Y
        = C_e' + R_lock + ν R_{ν,θ}

R_lock = T_c/Y − 2N/X + 2 Q_a/H_a
R_{ν,θ} = 2(Λ − D_a/H_a) − θ D_s/Y
R_{ν,θ} = R_{ν,1} + (1−θ) D_s/Y

Certified algebra. The fixed-(θ<1) route to DA-NS-2 is rejected.
NS is not solved.
"""

from __future__ import annotations

import math
from typing import Dict, Sequence

import numpy as np

from ns_attacks.galerkin import Field, flux_stats


def charge_split(stats: Dict[str, float], nu: float, theta: float, kappa_e: float) -> Dict[str, float]:
    X, Y, Lam = stats["X"], stats["Y"], stats["Lambda"]
    Ds, N, Tc = stats["D_s"], stats["N"], stats["T_c"]
    Ha, Da, Qa = stats["H_a"], stats["D_a"], stats["Q_a"]
    if min(X, Y, Ha, kappa_e) <= 0.0:
        raise ValueError("X, Y, H_a, kappa_e must be positive")
    Ce = math.log(X / (kappa_e * Ha))
    Ce_prime = 2.0 * N / X - 2.0 * Qa / Ha + 2.0 * nu * (Da / Ha - Lam)
    R_lock = Tc / Y - 2.0 * N / X + 2.0 * Qa / Ha
    R_nu_theta = 2.0 * (Lam - Da / Ha) - theta * Ds / Y
    R_nu_1 = 2.0 * (Lam - Da / Ha) - Ds / Y
    G = (Tc - theta * nu * Ds) / Y
    recon = Ce_prime + R_lock + nu * R_nu_theta
    return {
        "C_e": Ce,
        "C_e_prime": Ce_prime,
        "R_lock": R_lock,
        "R_nu_theta": R_nu_theta,
        "R_nu_1": R_nu_1,
        "G_theta": G,
        "recon": recon,
        "recon_err": abs(G - recon),
        "poison": (1.0 - theta) * Ds / Y,
        "kappa_e": kappa_e,
        "theta": theta,
        "nu": nu,
    }


def R_nu1_bound(radii: Sequence[float], masses: Sequence[float]) -> Dict[str, float]:
    """Random positive spectra on radii in [a,b]. No vector field required."""
    r = np.array(radii, dtype=float)
    m = np.array(masses, dtype=float)
    if np.any(r <= 0.0) or np.any(m < 0.0) or float(m.sum()) <= 0.0:
        raise ValueError("positive radii and nonnegative masses")
    e = m  # standing in for |û|²
    X = float(np.sum((r ** 2) * e))
    Y = float(np.sum((r ** 4) * e))
    Z = float(np.sum((r ** 6) * e))
    Ha = float(np.sum(r * e))
    Da = float(np.sum((r ** 3) * e))
    Lam = Y / X
    Ds = Z - Lam * Y
    R1 = 2.0 * (Lam - Da / Ha) - Ds / Y
    a, b = float(r.min()), float(r.max())
    bound = ((b / a) ** 3 - 1.0) * (Ds / Y) if a > 0.0 else float("inf")
    return {
        "R_nu_1": R1,
        "abs_R": abs(R1),
        "bound": bound,
        "ok": abs(R1) <= bound + 1e-12,
        "a": a,
        "b": b,
        "D_s_over_Y": Ds / Y,
        "Lambda": Lam,
    }


def nearly_equilateral_failfast() -> Dict[str, object]:
    """Near-core heterochiral lock: G_θ > 0 while C_e' < 0 for listed θ<1.

    Integer triad k=(−12,−11,−1), p=(0,11,12), q=(12,0,−11)
    with radii √266, √265, √265 (gap ≈ 3.07×10^{-2}). Locked (++−)
    ray, ν just above T_c/D_s so every tested θ<1 still has positive
    DA occupation while the frozen charge decreases. Not a close.
    """
    from ns_attacks.galerkin import Field

    k = (-12, -11, -1)
    p = (0, 11, 12)
    q = (12, 0, -11)
    f = Field().from_amplitudes(
        {(k, 1): 1.0j, (p, 1): 1.0j, (q, -1): -1.0j},
        reality=True,
    )
    stats = flux_stats(f, f.modes())
    nu = 7.06
    kappa = math.sqrt(stats["Lambda"])
    r = sorted(
        [
            math.sqrt(k[0] ** 2 + k[1] ** 2 + k[2] ** 2),
            math.sqrt(p[0] ** 2 + p[1] ** 2 + p[2] ** 2),
            math.sqrt(q[0] ** 2 + q[1] ** 2 + q[2] ** 2),
        ]
    )
    out: Dict[str, object] = {
        "Lambda": stats["Lambda"],
        "T_c": stats["T_c"],
        "D_s": stats["D_s"],
        "Y": stats["Y"],
        "nu": nu,
        "radius_gap": r[2] - r[0],
        "radii": r,
        "triad": (k, p, q),
    }
    for theta in (0.0, 0.5, 0.99, 0.999):
        split = charge_split(stats, nu=nu, theta=theta, kappa_e=kappa)
        out[f"theta_{theta}"] = {
            "G": split["G_theta"],
            "C_e_prime": split["C_e_prime"],
            "poison": split["poison"],
            "G_positive": split["G_theta"] > 0.0,
            "Ce_negative": split["C_e_prime"] < 0.0,
            "strike": split["G_theta"] > 0.0 and split["C_e_prime"] < 0.0,
        }
    return out
