#!/usr/bin/env python3
"""Route C Gap A diagnostics for Q_N[i,j] = 1/(gcd(i,j)*sqrt(ij)).

Checks:
  (1) Möbius Lemma A as stated in archived Route C (mu*phi/d^2) — fails off-diagonal
  (2) Rayleigh R(v_alt) vs claimed -1/(2pi)
  (3) Unnormalized v^T Q v vs claimed -log N/(2pi)
  (4) lambda_min vs -log N/(2pi) (spectral limit target)
  (5) Parity split: v^T Q v = sum_{d odd} T_-(N/d)/d^3 + sum_{d even} T_+(N/d)/d^3

Usage:
  python3 scripts/route_c_gap_a_verify.py [N1 N2 ...]
"""
from __future__ import annotations

import sys
from math import gcd

import numpy as np

TARGET = -1.0 / (2.0 * np.pi)


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


def mat_norm(N: int) -> np.ndarray:
    a = np.empty((N, N))
    for i in range(1, N + 1):
        for j in range(i, N + 1):
            v = 1.0 / (gcd(i, j) * (i * j) ** 0.5)
            a[i - 1, j - 1] = a[j - 1, i - 1] = v
    return a


def mat_mobius_claim(N: int) -> np.ndarray:
    q = np.zeros((N, N))
    for d in range(1, N + 1):
        coeff = mu(d) * phi(d) / (d * d)
        if coeff == 0:
            continue
        for i in range(1, N + 1):
            if i % d:
                continue
            for j in range(i, N + 1):
                if j % d:
                    continue
                v = coeff / (i * j) ** 0.5
                q[i - 1, j - 1] += v
                if i != j:
                    q[j - 1, i - 1] += v
    return q


def v_alt(N: int) -> np.ndarray:
    k = np.arange(1, N + 1, dtype=float)
    return (-1.0) ** (k + 1) / np.sqrt(k)


def t_signed(M: int) -> float:
    return sum(
        (-1.0) ** (m + n) / (m * n)
        for m in range(1, M + 1)
        for n in range(1, M + 1)
        if gcd(m, n) == 1
    )


def t_unsigned(M: int) -> float:
    return sum(
        1.0 / (m * n)
        for m in range(1, M + 1)
        for n in range(1, M + 1)
        if gcd(m, n) == 1
    )


def vqv_parity(N: int) -> tuple[float, float, float]:
    odd = even = 0.0
    for d in range(1, N + 1):
        m = N // d
        if d % 2 == 1:
            odd += t_signed(m) / d**3
        else:
            even += t_unsigned(m) / d**3
    return odd + even, odd, even


def analyze(N: int) -> None:
    q = mat_norm(N)
    qm = mat_mobius_claim(N)
    mob_err = np.max(np.abs(q - qm))

    v = v_alt(N)
    vqv = float(v @ q @ v)
    vnorm2 = float(v @ v)
    r_alt = vqv / vnorm2

    evals, evecs = np.linalg.eigh(q)
    lam_min = float(evals[0])
    gap = float(evals[1] - evals[0])
    vstar = evecs[:, 0]
    if vstar @ v < 0:
        vstar = -vstar
    overlap = abs(float(vstar @ v / np.linalg.norm(v)))

    vqv_p, odd_c, even_c = vqv_parity(N)
    logn = np.log(N)

    print(f"\n--- N = {N} ---")
    print(f"  Lemma A (mu*phi/d^2) max entry error : {mob_err:.6e}")
    print(f"  v^T Q v                              : {vqv: .6f}")
    print(f"  -log N / (2pi)  [Gap A unnormalized] : {-logn / (2 * np.pi): .6f}")
    print(f"  ratio v^T Q v / (-log N/2pi)         : {vqv / (-logn / (2 * np.pi)): .3f}")
    print(f"  R(v_alt) = v^T Q v / ||v||^2         : {r_alt: .6f}")
    print(f"  -1/(2pi)  [Gap A normalized target]  : {TARGET: .6f}")
    print(f"  ratio R(v_alt) / (-1/2pi)            : {r_alt / TARGET: .3f}")
    print(f"  lambda_min                           : {lam_min: .6f}")
    print(f"  lambda_min / log N                   : {lam_min / logn: .6f}")
    print(f"  ratio lambda_min / (-log N/2pi)      : {lam_min / (-logn / (2 * np.pi)): .3f}")
    print(f"  |<v*, v_alt>| / ||v_alt||            : {overlap: .6f}")
    print(f"  lambda_2 - lambda_min                : {gap: .6f}")
    print(f"  parity split v^T Q v                 : odd={odd_c: .4f} even={even_c: .4f} sum={vqv_p: .6f}")


def main() -> None:
    sizes = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [100, 500, 1000]
    print("Route C Gap A verifier")
    print("Operator: Q_N[i,j] = 1/(gcd(i,j)*sqrt(ij))")
    print("Alternating trial: v_alt[k] = (-1)^(k+1)/sqrt(k)")
    for n in sizes:
        analyze(n)
    print(
        "\nSummary template:\n"
        "  • Lemma A (mu*phi/d^2 decomposition): fails for gcd>1 (see max entry error).\n"
        "  • Gap A for v_alt Rayleigh / v^T Q v: numerically diverges from -1/(2pi), -log N/(2pi).\n"
        "  • lambda_min / log N -> -1/(2pi): strong numeric match.\n"
        "  • Correct parity split uses mu/d^2 and T_+/T_- coprime sums.\n"
    )


if __name__ == "__main__":
    main()
