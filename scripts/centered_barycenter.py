"""Centered spectral-barycenter identities. Algebra only. Not DA-NS-2."""

from __future__ import annotations

import math


def modes_to_moments(a: list[float], mass: list[float]) -> dict[str, float]:
    """a_m = eigenvalue of A; mass_m = |u_m|^2."""
    if len(a) != len(mass):
        raise ValueError("a and mass must match")
    x = sum(ai * mi for ai, mi in zip(a, mass))
    y = sum(ai * ai * mi for ai, mi in zip(a, mass))
    z = sum(ai**3 * mi for ai, mi in zip(a, mass))
    if x <= 0:
        raise ValueError("X must be positive")
    lam = y / x
    d_s = z - lam * y
    d_s_fact = sum(ai * (ai - lam) ** 2 * mi for ai, mi in zip(a, mass))
    p = [(ai * mi) / x for ai, mi in zip(a, mass)]
    lam_from_p = sum(pi * ai for pi, ai in zip(p, a))
    var = sum(pi * (ai - lam) ** 2 for pi, ai in zip(p, a))
    return {
        "X": x,
        "Y": y,
        "Z": z,
        "Lambda": lam,
        "D_s": d_s,
        "D_s_fact": d_s_fact,
        "Lambda_from_p": lam_from_p,
        "D_s_over_X": var,
    }


def log_lambda_prime(t_c: float, nu: float, d_s: float, y: float) -> float:
    """(log Λ)' = 2/Y (T_c − ν D_s). Identity, not a bound."""
    if y <= 0:
        raise ValueError("Y must be positive")
    return 2.0 * (t_c - nu * d_s) / y


def two_triad_strike() -> dict[str, float]:
    """Dossier §12 arithmetic: Q_a,Γ = 0 and T_c,Γ^het > 0."""
    sqrt2 = math.sqrt(2.0)
    sqrt3 = math.sqrt(3.0)
    sqrt6 = math.sqrt(6.0)
    q1 = 2.0 * (sqrt2 - 1.0)
    q2 = -2.0 * (sqrt2 - 1.0)
    r1 = (3.0 + 3.0 * sqrt2 + 5.0 * sqrt3 + sqrt6) / 6.0
    r2 = 1.0 + sqrt2
    t1 = 1.0 - sqrt3 + 4.0 * sqrt6 / 3.0
    t2 = -2.0
    lam = 2.0
    kappa = math.sqrt(lam)
    two_k3 = 2.0 * kappa**3
    rho = (r1 - two_k3) * q1 + (r2 - two_k3) * q2
    return {
        "Q1": q1,
        "Q2": q2,
        "Q_sum": q1 + q2,
        "R1": r1,
        "R2": r2,
        "T1": t1,
        "T2": t2,
        "T_sum": t1 + t2,
        "T_from_RQ": r1 * q1 + r2 * q2,
        "rho": rho,
        "boxed": (4.0 * sqrt6 - 3.0 * sqrt3 - 3.0) / 3.0,
        "two_k3": two_k3,
    }


def mobius_claimed_sum(g: int) -> float:
    """Claimed identity: sum_{d|g} μ(d) φ(d) / d^2  =?  1/g."""
    total = 0.0
    d = 1
    while d * d <= g:
        if g % d == 0:
            total += _mu(d) * _phi(d) / (d * d)
            other = g // d
            if other != d:
                total += _mu(other) * _phi(other) / (other * other)
        d += 1
    return total


def _mu(n: int) -> int:
    if n < 1:
        raise ValueError("n >= 1")
    if n == 1:
        return 1
    factors = 0
    x = n
    p = 2
    while p * p <= x:
        if x % p == 0:
            x //= p
            if x % p == 0:
                return 0
            factors += 1
        p += 1
    if x > 1:
        factors += 1
    return -1 if factors % 2 else 1


def _phi(n: int) -> int:
    result = n
    x = n
    p = 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            result = result * (p - 1) // p
        p += 1
    if x > 1:
        result = result * (x - 1) // x
    return result
