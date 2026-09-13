#!/usr/bin/env python3
"""Route N — shellwise λ_min probe for inverse-GCD blocks.

Assumptions (documented; not a theorem):
  • Ambient operators on {1,...,M}:
      Q̃_M(i,j) = 1/(gcd(i,j)·√(ij))
      H_M = D^{-1/2} Q̃_M D^{-1/2}  (degree-normalized)
  • Dyadic shells: I_j = {n ∈ {1,...,M} : floor(log2 n) = j}
    (n=1 → j=0; then [2,3], [4,7], [8,15], ...)
  • B_{M,j} := principal submatrix of the ambient operator on I_j
    (zero-pad / other lifts are NOT probed here).
  • Route N asks whether min_j λ_min(B_{M,j}) ≥ -1/2 + δ uniformly.

Convexity reminder (not probed numerically):
  For Hermitian B_j of equal size and a_j≥0, Σ a_j=1,
  λ_min(Σ a_j B_j) ≥ Σ a_j λ_min(B_j) ≥ min_j λ_min(B_j).
  Principal submatrices of different sizes need a common lift before
  that sum is defined; this script only reports shellwise floors.

Usage:
  python3 scripts/route_n_shell_floor_probe.py [Mmax]
"""
from __future__ import annotations

import math
import sys
from math import gcd

import numpy as np

FLOOR = -0.5


def mat_norm(N: int) -> np.ndarray:
    A = np.empty((N, N), dtype=float)
    for i in range(1, N + 1):
        for j in range(i, N + 1):
            v = 1.0 / (gcd(i, j) * math.sqrt(i * j))
            A[i - 1, j - 1] = A[j - 1, i - 1] = v
    return A


def mat_h(Qn: np.ndarray) -> np.ndarray:
    d = Qn.sum(axis=1)
    # Degree vector is strictly positive for Q̃.
    inv_sqrt = 1.0 / np.sqrt(d)
    return inv_sqrt[:, None] * Qn * inv_sqrt[None, :]


def shell_index_sets(M: int) -> list[tuple[int, list[int]]]:
    shells: dict[int, list[int]] = {}
    for n in range(1, M + 1):
        j = int(math.floor(math.log2(n))) if n >= 1 else 0
        shells.setdefault(j, []).append(n - 1)  # 0-based
    return sorted(shells.items(), key=lambda t: t[0])


def shell_eigs(A: np.ndarray, shells: list[tuple[int, list[int]]]) -> list[tuple[int, int, float]]:
    out: list[tuple[int, int, float]] = []
    for j, idx in shells:
        if len(idx) == 0:
            continue
        ix = np.array(idx, dtype=int)
        B = A[np.ix_(ix, ix)]
        if B.shape[0] == 1:
            lam = float(B[0, 0])
        else:
            lam = float(np.linalg.eigvalsh(B)[0])
        out.append((j, len(idx), lam))
    return out


def probe_one(M: int) -> dict:
    Qn = mat_norm(M)
    H = mat_h(Qn)
    shells = shell_index_sets(M)
    q_shells = shell_eigs(Qn, shells)
    h_shells = shell_eigs(H, shells)
    q_full = float(np.linalg.eigvalsh(Qn)[0])
    h_full = float(np.linalg.eigvalsh(H)[0])
    q_min_shell = min(t[2] for t in q_shells)
    h_min_shell = min(t[2] for t in h_shells)
    return {
        "M": M,
        "L": len(shells),
        "q_full": q_full,
        "h_full": h_full,
        "q_min_shell": q_min_shell,
        "h_min_shell": h_min_shell,
        "q_shells": q_shells,
        "h_shells": h_shells,
        "q_shell_clear_half": q_min_shell > FLOOR,
        "h_shell_clear_half": h_min_shell > FLOOR,
    }


def main() -> None:
    Mmax = int(sys.argv[1]) if len(sys.argv) > 1 else 256
    Ms = [m for m in [16, 32, 64, 128, 256, 512] if m <= Mmax]
    if not Ms:
        Ms = [Mmax]

    print("Route N shell-floor probe")
    print("Assumption: B_{M,j} = principal submatrix of ambient op on dyadic index shell")
    print(f"Target floor: λ_min > {FLOOR} (= -1/2)\n")

    print(
        f"{'M':>6}  {'L':>3}  {'λmin Q̃':>10}  {'min_j Q̃':>10}  {'Q̃>−½?':>7}  "
        f"{'λmin H':>10}  {'min_j H':>10}  {'H>−½?':>7}"
    )
    results = []
    for M in Ms:
        r = probe_one(M)
        results.append(r)
        print(
            f"{r['M']:6d}  {r['L']:3d}  {r['q_full']:10.6f}  {r['q_min_shell']:10.6f}  "
            f"{str(r['q_shell_clear_half']):>7}  {r['h_full']:10.6f}  {r['h_min_shell']:10.6f}  "
            f"{str(r['h_shell_clear_half']):>7}"
        )

    # Detail worst shells at largest M
    r = results[-1]
    print(f"\nShell detail for M={r['M']} (Q̃ principal blocks):")
    print(f"{'j':>4}  {'|I_j|':>6}  {'λ_min':>12}  {'>−½?':>6}")
    for j, size, lam in r["q_shells"]:
        print(f"{j:4d}  {size:6d}  {lam:12.6f}  {str(lam > FLOOR):>6}")

    print(f"\nShell detail for M={r['M']} (H principal blocks):")
    print(f"{'j':>4}  {'|I_j|':>6}  {'λ_min':>12}  {'>−½?':>6}")
    for j, size, lam in r["h_shells"]:
        print(f"{j:4d}  {size:6d}  {lam:12.6f}  {str(lam > FLOOR):>6}")

    any_q_fail = any(not r["q_shell_clear_half"] for r in results)
    any_h_fail = any(not r["h_shell_clear_half"] for r in results)
    print("\nDA verdict template:")
    print(
        "  • Convexity λ_min(Σ a_j B_j) ≥ Σ a_j λ_min(B_j): TRUE for Hermitian "
        "convex combinations (after common lift)."
    )
    if any_q_fail:
        print(
            "  • Uniform shellwise floor on principal submatrices of Q̃: FAILS in range "
            f"(min_j λ_min ≤ −1/2 for some M≤{Mmax})."
        )
    else:
        print(
            "  • Uniform shellwise floor on principal submatrices of Q̃: holds in probed "
            f"range M≤{Mmax} — NOT a theorem; do not claim."
        )
    if any_h_fail:
        print(
            "  • Uniform shellwise floor on principal submatrices of H: FAILS in range."
        )
    else:
        print(
            "  • Uniform shellwise floor on principal submatrices of H: holds in probed "
            f"range M≤{Mmax} — NOT a theorem; do not claim."
        )
    print(
        "  • Even a proved shellwise floor on these matrices does NOT prove NS regularity "
        "(no PDE bridge)."
    )


if __name__ == "__main__":
    main()
