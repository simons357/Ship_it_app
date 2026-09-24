"""I3 integer realizability: Gram matrices and Hilbert symbols.

I3 is the cubic lattice (Z^3, x1^2+x2^2+x3^2). A triangle with
prescribed squared radii a,b,c exists iff the binary Gram

    G = [[a, s], [s, b]],    s = (c-a-b)/2,

has an integer realization G = V^T V with V a 3-by-2 integer
matrix. This is a test on wavevectors, not on velocity
coefficients.

For a>0, Delta = ab-s^2 > 0 and integer a,b,s, ordinary
integral representation by I3 is equivalent to representation
over every Q_ℓ and every Z_ℓ. Finite criterion (positive-
definite real place already granted):

    (a, Delta)_ℓ (a, -1)_ℓ (Delta, -1)_ℓ = 1

for every prime ℓ | 2a Delta.

Application of classical quadratic-form local theory
(Schulze-Pillot). Not a census. Not time evolution.
Not a T_c bound. NS is not solved.
"""

from __future__ import annotations

import math
from typing import Dict, Iterable, List, Sequence, Tuple


def primes_dividing(n: int) -> List[int]:
    n = abs(int(n))
    if n == 0:
        raise ValueError("0 has infinitely many prime divisors")
    out: List[int] = []
    if n % 2 == 0:
        out.append(2)
        while n % 2 == 0:
            n //= 2
    p = 3
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 2
    if n > 1:
        out.append(n)
    return out


def _legendre(a: int, p: int) -> int:
    """Legendre symbol (a/p) for odd prime p."""
    a %= p
    if a == 0:
        return 0
    # Euler criterion
    return pow(a, (p - 1) // 2, p) == 1 and 1 or -1


def _odd_unit_part(n: int) -> Tuple[int, int]:
    """n = 2^v * u with u odd. Sign stays on u."""
    if n == 0:
        raise ValueError("zero has no 2-adic valuation in this use")
    sign = -1 if n < 0 else 1
    n = abs(n)
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v, sign * n


def hilbert_odd(a: int, b: int, p: int) -> int:
    """Hilbert symbol (a,b)_p for odd prime p."""
    if p == 2:
        raise ValueError("use hilbert_2")
    va, ua = 0, a
    vb, ub = 0, b
    # factor p-valuation
    def split(n: int) -> Tuple[int, int]:
        sign = -1 if n < 0 else 1
        n = abs(n)
        v = 0
        while n % p == 0:
            n //= p
            v += 1
        return v, sign * n

    va, ua = split(a)
    vb, ub = split(b)
    exp = (va * vb * ((p - 1) // 2)) % 2
    val = 1
    if exp:
        val = -val
    if vb % 2:
        val *= _legendre(ua, p)
    if va % 2:
        val *= _legendre(ub, p)
    return val


def hilbert_2(a: int, b: int) -> int:
    """Hilbert symbol (a,b)_2."""
    va, ua = _odd_unit_part(a)
    vb, ub = _odd_unit_part(b)

    def eps(u: int) -> int:
        # (u^2-1)/8 mod 2
        return ((u * u - 1) // 8) % 2

    def omega(u: int) -> int:
        # (u-1)/2 mod 2
        return ((u - 1) // 2) % 2

    e = (eps(ua) * eps(ub) + omega(ua) * vb + omega(ub) * va) % 2
    return -1 if e else 1


def hilbert(a: int, b: int, ell: int) -> int:
    if a == 0 or b == 0:
        raise ValueError("Hilbert symbol not used at 0 here")
    if ell == 2:
        return hilbert_2(a, b)
    return hilbert_odd(a, b, ell)


def gram_data(a: int, b: int, s: int) -> dict:
    delta = a * b - s * s
    c = a + b + 2 * s
    return {
        "a": a,
        "b": b,
        "s": s,
        "c": c,
        "Delta": delta,
        "positive_definite": a > 0 and delta > 0,
    }


def local_factors(a: int, delta: int, ell: int) -> dict:
    ha = hilbert(a, delta, ell)
    hm = hilbert(a, -1, ell)
    hd = hilbert(delta, -1, ell)
    prod = ha * hm * hd
    return {
        "ell": ell,
        "(a,Delta)": ha,
        "(a,-1)": hm,
        "(Delta,-1)": hd,
        "product": prod,
        "passes": prod == 1,
    }


def criterion_12(a: int, b: int, s: int) -> dict:
    """Finite local-to-global test (12)."""
    g = gram_data(a, b, s)
    if not g["positive_definite"]:
        return {**g, "applicable": False, "passes": False, "reason": "not positive definite"}
    moduli = 2 * a * g["Delta"]
    primes = primes_dividing(moduli)
    factors = [local_factors(a, g["Delta"], ell) for ell in primes]
    return {
        **g,
        "applicable": True,
        "primes": primes,
        "factors": factors,
        "passes": all(f["passes"] for f in factors),
        "failed_primes": [f["ell"] for f in factors if not f["passes"]],
    }


# Locked September 20 regressions.
REGRESSIONS: Tuple[dict, ...] = (
    {"a": 96, "b": 96, "s": 0, "expect_pass": False, "expect_fail": (2, 3)},
    {"a": 2, "b": 3, "s": 1, "expect_pass": False, "expect_fail": (2, 5)},
    {"a": 2, "b": 2, "s": -1, "expect_pass": True, "expect_fail": ()},
    {"a": 14, "b": 14, "s": -7, "expect_pass": True, "expect_fail": ()},
)


def monochromatic_necessary(alpha: int) -> dict:
    """a=b=c=alpha forces s=-alpha/2. Odd alpha is impossible."""
    odd_impossible = (alpha % 2 == 1)
    even_necessary = (alpha % 2 == 0)
    sufficient = False
    detail = None
    if even_necessary:
        s = -alpha // 2
        detail = criterion_12(alpha, alpha, s)
        sufficient = bool(detail["passes"])
    return {
        "alpha": alpha,
        "odd_impossible": odd_impossible,
        "even_necessary_not_sufficient": even_necessary,
        "even_passes_12": sufficient if even_necessary else False,
        "detail": detail,
    }


def report() -> dict:
    rows = []
    for spec in REGRESSIONS:
        got = criterion_12(spec["a"], spec["b"], spec["s"])
        failed = tuple(got.get("failed_primes") or [])
        rows.append(
            {
                **spec,
                "got_pass": got["passes"],
                "got_fail": failed,
                "match": got["passes"] == spec["expect_pass"]
                and (not spec["expect_fail"] or set(failed) >= set(spec["expect_fail"])),
                "result": got,
            }
        )
    return {
        "criterion": "(a,Delta)_ell (a,-1)_ell (Delta,-1)_ell = 1 for ell | 2a Delta",
        "regressions": rows,
        "all_match": all(r["match"] for r in rows),
        "odd_alpha_9": monochromatic_necessary(9),
        "even_alpha_2": monochromatic_necessary(2),
        "even_alpha_6": monochromatic_necessary(6),
        "locks": {
            "wavevectors_not_coefficients": True,
            "not_time_evolution": True,
            "not_a_census_only": True,
            "not_a_close": True,
        },
    }
