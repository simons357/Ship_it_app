#!/usr/bin/env python3
"""Phase-flow spell: track λ_min/log N and concentration vs N.

Looks for fixed points / attractors in the discrete SFE-BH analogy:
  - spectral coordinate: λ_min / log N  →  -1/(2π) ?
  - concentration of ground modes → 1 ?

Usage:
  python3 scripts/sfe_phase_flow_spell.py [Nmax step]
"""
from __future__ import annotations

import sys
from math import gcd

import numpy as np

TARGET = -1.0 / (2.0 * np.pi)


def q_matrix(N: int) -> np.ndarray:
    a = np.empty((N, N))
    for i in range(1, N + 1):
        for j in range(i, N + 1):
            v = 1.0 / (gcd(i, j) * (i * j) ** 0.5)
            a[i - 1, j - 1] = a[j - 1, i - 1] = v
    return a


def herfindahl(v: np.ndarray) -> float:
    p = np.abs(v)
    p = p / p.sum()
    return float(np.sum(p * p))


def main() -> None:
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    step = int(sys.argv[2]) if len(sys.argv) > 2 else 20

    print(f"{'N':>6}  {'λ/logN':>10}  {'/target':>8}  {'H(v*)':>8}  {'H(v_alt)':>8}  {'<-½?':>6}")
    prev_ratio = None
    for N in range(40, nmax + 1, step):
        q = q_matrix(N)
        evals, evecs = np.linalg.eigh(q)
        lam_min = float(evals[0])
        v_star = evecs[:, 0]
        n = np.arange(1, N + 1, dtype=float)
        v_alt = (-1.0) ** (n + 1) / np.sqrt(n)
        ratio = lam_min / np.log(N) / TARGET
        h_star = herfindahl(v_star)
        h_alt = herfindahl(v_alt)
        print(
            f"{N:6d}  {lam_min / np.log(N):10.6f}  {ratio:8.4f}  {h_star:8.4f}  "
            f"{h_alt:8.4f}  {str(lam_min < -0.5):>6}"
        )
        prev_ratio = ratio

    print(
        "\nSpell hint: if ratio → 1 and H(v*) rises while H(v_alt) falls, "
        "the 'horizon' story is spectral collapse toward one mode — not yet BH physics."
    )


if __name__ == "__main__":
    main()
