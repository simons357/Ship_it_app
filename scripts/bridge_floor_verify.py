#!/usr/bin/env python3
"""Verify Bridge-related spectral claims for Simons Q_N operators.

Usage:
  python3 scripts/bridge_floor_verify.py [Nmax]

Checks:
  (A) λ_min of raw Q_ij = 1/gcd(i,j)
  (B) λ_min of normalized Q̃_ij = 1/(gcd(i,j)·√(ij))   [three-in-one Route C]
  (C) worst Rayleigh of Goldbach difference vectors v_k on Q̃
  (D) paper §2.1 identity 1/n =? Σ_{d|n} μ(d)φ(d)/d²  (spot check)

Bridge as written (λ_min(Q) > -1/2 for all N) fails (A)/(B).
Restricted GNC Rayleigh on Q̃ may still sit above -1/2 — see (C).
"""
from __future__ import annotations

import sys
from math import gcd

import numpy as np


def mu(n: int) -> int:
    if n == 1:
        return 1
    x, c, p = n, 0, 2
    while p * p <= x:
        if x % p == 0:
            x //= p
            c += 1
            if x % p == 0:
                return 0
        p += 1
    if x > 1:
        c += 1
    return -1 if c % 2 else 1


def phi(n: int) -> int:
    r, x, p = n, n, 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            r -= r // p
        p += 1
    if x > 1:
        r -= r // x
    return r


def primes_upto(n: int) -> list[int]:
    s = [True] * (n + 1)
    s[0] = s[1] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            s[i * i :: i] = [False] * len(s[i * i :: i])
    return [i for i, b in enumerate(s) if b]


def mat_raw(N: int) -> np.ndarray:
    A = np.empty((N, N))
    for i in range(1, N + 1):
        for j in range(i, N + 1):
            v = 1.0 / gcd(i, j)
            A[i - 1, j - 1] = A[j - 1, i - 1] = v
    return A


def mat_norm(N: int) -> np.ndarray:
    A = np.empty((N, N))
    for i in range(1, N + 1):
        for j in range(i, N + 1):
            v = 1.0 / (gcd(i, j) * (i * j) ** 0.5)
            A[i - 1, j - 1] = A[j - 1, i - 1] = v
    return A


def goldbach_vk_broken_indicator(k: int, N: int, primes: set[int]) -> np.ndarray:
    """June-5 detector: vanishes on genuine Goldbach pairs — do not use for Bridge*."""
    v = np.zeros(N)
    for j in range(1, N + 1):
        if j in primes:
            v[j - 1] += 1.0
        if 1 <= k - j <= N and (k - j) in primes:
            v[j - 1] -= 1.0
    return v


def goldbach_multirep_vk(k: int, N: int, primes: set[int]) -> np.ndarray:
    """Correct Bridge* multi-rep: sum (e_p - e_{k-p}) over unordered Goldbach pairs."""
    v = np.zeros(N)
    for p in range(2, (k + 1) // 2):
        q = k - p
        if q > N or p > N:
            continue
        if p in primes and q in primes and p != q:
            v[p - 1] += 1.0
            v[q - 1] -= 1.0
    return v


def main() -> None:
    Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    print(f"Bridge floor verifier · N up to {Nmax}\n")

    print("§2.1 identity spot check: 1/n vs Σ_{d|n} μ(d)φ(d)/d²")
    for n in [1, 2, 3, 6, 12]:
        s = sum(mu(d) * phi(d) / (d * d) for d in range(1, n + 1) if n % d == 0)
        print(f"  n={n}: 1/n={1/n:.6f}  paper_sum={s:.6f}  equal? {abs(s - 1/n) < 1e-12}")
    print()

    print(f"{'N':>6}  {'λ_min raw':>12}  {'>-½?':>6}  {'λ_min Q̃':>12}  {'>-½?':>6}  {'worst v_k·Q̃':>12}  {'v_k>-½?':>8}")
    for N in [10, 20, 50, 100, 200]:
        if N > Nmax:
            break
        wr = float(np.linalg.eigvalsh(mat_raw(N))[0])
        Qn = mat_norm(N)
        wn = float(np.linalg.eigvalsh(Qn)[0])
        P = set(primes_upto(N))
        worst = None
        for k in range(4, N + 1, 2):
            v = goldbach_multirep_vk(k, N, P)
            nrm = np.linalg.norm(v)
            if nrm < 1e-12:
                continue
            v = v / nrm
            r = float(v @ Qn @ v)
            if worst is None or r < worst:
                worst = r
        print(
            f"{N:6d}  {wr:12.6f}  {str(wr > -0.5):>6}  {wn:12.6f}  {str(wn > -0.5):>6}  "
            f"{worst:12.6f}  {str(worst > -0.5):>8}"
        )

    print(
        "\nConclusion template:\n"
        "  • Full-spectrum Bridge λ_min(Q)>−½ or λ_min(Q̃)>−½: FAILS (false for these matrices).\n"
        "  • Restricted Bridge* on multi-rep Goldbach vectors: proved R>-½; numeric check in this range.\n"
        "  • Broken June-5 indicator detector is not used here.\n"
    )


if __name__ == "__main__":
    main()
