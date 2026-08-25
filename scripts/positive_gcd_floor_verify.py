#!/usr/bin/env python3
"""Positive-GCD Q checks: Theorems A/B; kill C' on zero-diag; open C on PD.

Usage:
  python3 scripts/positive_gcd_floor_verify.py [Nmax]
"""
from __future__ import annotations

import sys
from math import gcd

import numpy as np


def mat_positive(N: int) -> np.ndarray:
    A = np.empty((N, N))
    for i in range(1, N + 1):
        for j in range(i, N + 1):
            v = gcd(i, j) / (i * j) ** 0.5
            A[i - 1, j - 1] = A[j - 1, i - 1] = v
    return A


def main() -> None:
    Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print("Positive-GCD Q · pair Rayleigh (A) / λ_min(Q) (closed C: PD) / λ_min(Q̂) (kill C')\n")
    print(f"{'a,b':>8}  {'R(ea-eb)':>12}  {'>0?':>5}")
    for a, b in [(1, 2), (2, 3), (3, 6), (6, 15), (10, 25)]:
        g = gcd(a, b) / (a * b) ** 0.5
        R = 1.0 - g
        print(f"{a:3d},{b:<3d}  {R:12.6f}  {str(R > 0):>5}")

    print(f"\n{'N':>6}  {'λ_min(Q)':>12}  {'>0?':>5}  {'λ_min(Q̂)':>12}  {'>-½?':>6}")
    kill_n = None
    for N in [5, 10, 20, 30, 50, 80, 100]:
        if N > Nmax:
            break
        Q = mat_positive(N)
        mn = float(np.linalg.eigvalsh(Q)[0])
        Qh = Q.copy()
        np.fill_diagonal(Qh, 0.0)
        mz = float(np.linalg.eigvalsh(Qh)[0])
        print(f"{N:6d}  {mn:12.6f}  {str(mn > 0):>5}  {mz:12.6f}  {str(mz > -0.5):>6}")
        if kill_n is None and mz < -0.5:
            kill_n = (N, mz)

    if kill_n:
        print(f"\nKill C' certificate: λ_min(Q̂_{kill_n[0]}) = {kill_n[1]:.6f} < -1/2")
    print("Closed C: Q = D^{-1/2} G D^{-1/2} with G=(gcd) PD ⇒ Q ≻ 0.")
print("Kill C': λ_min(Q̂) < -1/2 already at small N.")


if __name__ == "__main__":
    main()
