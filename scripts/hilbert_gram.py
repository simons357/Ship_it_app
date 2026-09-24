#!/usr/bin/env python3
"""hilbert_gram — source of relevant_primes.

Fix the helper here, not around it. A wrapper that calls sympy while
this function still returns 20 for Gram (2,3,1) will poison every
other importer.

relevant_primes(a, Δ) is the set of primes ℓ | 2aΔ.
It must factor. The product 2aΔ is not itself a prime.

    Gram (2,3,1): Δ = 6-1 = 5, 2aΔ = 20 → {2, 5}, never {20}.

Callers in this tree: scripts/fourier_triangles_audit.py,
tests/test_fourier_triangles_heavy_board.py. Grep if you add more.
"""

from __future__ import annotations


def _legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    r = pow(a, (p - 1) // 2, p)
    return -1 if r == p - 1 else r


def _odd_unit_val(n: int, p: int) -> tuple[int, int]:
    if n == 0:
        raise ValueError("Hilbert symbol is undefined at 0")
    sign = -1 if n < 0 else 1
    n = abs(n)
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v, sign * n


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    p = 3
    while p * p <= n:
        if n % p == 0:
            return False
        p += 2
    return True


def primes_dividing(n: int) -> list[int]:
    """Prime factors of |n|. Raises if a composite would be emitted."""
    n = abs(n)
    out: list[int] = []
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
    bad = [q for q in out if not is_prime(q)]
    if bad:
        raise RuntimeError(f"primes_dividing would return composites {bad} from {out}")
    return out


def relevant_primes(a: int, delta: int) -> list[int]:
    """Primes ℓ | 2aΔ. Factors first. Never returns 20 for (2,3,1)."""
    if a == 0 or delta == 0:
        raise ValueError("relevant_primes is undefined at a=0 or Δ=0")
    return primes_dividing(2 * a * delta)


def hilbert_symbol(a: int, b: int, ell: int) -> int:
    """(a, b)_ℓ for nonzero integers a, b and prime ℓ."""
    if a == 0 or b == 0:
        raise ValueError("Hilbert symbol is undefined at 0")
    if not is_prime(ell):
        raise ValueError(f"Hilbert symbol requires a prime ℓ, got {ell}")
    if ell == 2:
        va, ua = _odd_unit_val(a, 2)
        vb, ub = _odd_unit_val(b, 2)
        exp = ((ua - 1) * (ub - 1)) // 4 + (va * (ub * ub - 1)) // 8 + (vb * (ua * ua - 1)) // 8
        return -1 if exp % 2 else 1
    va, ua = _odd_unit_val(a, ell)
    vb, ub = _odd_unit_val(b, ell)
    sign = -1 if (va * vb * ((ell - 1) // 2)) % 2 else 1
    if vb % 2:
        sign *= _legendre(ua, ell)
    if va % 2:
        sign *= _legendre(ub, ell)
    return sign
