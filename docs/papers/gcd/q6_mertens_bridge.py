"""Inverse-GCD probes for a Q6 → Mertens transfer.

Not live Domain Architect. Clay is NOT CLAIMED. This module does not
prove the Riemann hypothesis. It records identities, one-sided Rayleigh
bounds, and numeric obstructions to the June 8 Gap 1 Step F close.

Locked operator (August Q6 PDF): ẽQ_N(i,j) = 1 / (gcd(i,j) √(ij)).
Operator B is the Gap 1 patch kernel; it is a different matrix.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np

MINUS_ONE_OVER_TWO_PI = -1.0 / (2.0 * math.pi)
MINUS_ONE_OVER_PI_SQ = -1.0 / (math.pi**2)


def mobius_table(n: int) -> np.ndarray:
    """μ(1), …, μ(n) by linear sieve. μ(0) is unused."""
    if n < 1:
        raise ValueError("n must be ≥ 1")
    mu = np.ones(n + 1, dtype=np.int8)
    primes: list[int] = []
    is_comp = np.zeros(n + 1, dtype=bool)
    for i in range(2, n + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            ip = i * p
            if ip > n:
                break
            is_comp[ip] = True
            if i % p == 0:
                mu[ip] = 0
                break
            mu[ip] = -mu[i]
    mu[1] = 1
    return mu


def mertens(n: int, mu: np.ndarray | None = None) -> int:
    table = mobius_table(n) if mu is None else mu
    return int(table[1 : n + 1].sum())


def gcd_matrix(n: int) -> np.ndarray:
    idx = np.arange(1, n + 1, dtype=np.int32)
    return np.gcd.outer(idx, idx).astype(np.int32)


def operator_a(n: int) -> np.ndarray:
    """August ẽQ_N: 1 / (gcd √(ij)). All entries positive."""
    g = gcd_matrix(n).astype(np.float64)
    idx = np.arange(1, n + 1, dtype=np.float64)
    return 1.0 / (g * np.sqrt(np.outer(idx, idx)))


def operator_b(n: int, mu: np.ndarray | None = None) -> np.ndarray:
    """Gap 1 patch: μ(i/g) μ(j/g) g / √(ij), g = gcd(i,j)."""
    table = mobius_table(n) if mu is None else mu
    g = gcd_matrix(n)
    i = np.arange(1, n + 1)
    ii = np.broadcast_to(i[:, None], (n, n))
    jj = np.broadcast_to(i[None, :], (n, n))
    a = ii // g
    b = jj // g
    return (table[a] * table[b] * g.astype(np.float64)) / np.sqrt(
        ii.astype(np.float64) * jj.astype(np.float64)
    )


def rayleigh(matrix: np.ndarray, vec: np.ndarray) -> float:
    nrm = float(vec @ vec)
    if nrm == 0.0:
        raise ValueError("zero trial vector")
    return float(vec @ matrix @ vec) / nrm


def lambda_min(matrix: np.ndarray) -> float:
    return float(np.min(np.linalg.eigvalsh(matrix)))


def trial_mu_over_sqrt(n: int, mu: np.ndarray | None = None) -> np.ndarray:
    table = mobius_table(n) if mu is None else mu
    idx = np.arange(1, n + 1, dtype=np.float64)
    return table[1 : n + 1].astype(np.float64) / np.sqrt(idx)


def trial_one_over_sqrt(n: int) -> np.ndarray:
    return 1.0 / np.sqrt(np.arange(1, n + 1, dtype=np.float64))


def sum_mu_over_n(n: int, mu: np.ndarray | None = None) -> float:
    table = mobius_table(n) if mu is None else mu
    idx = np.arange(1, n + 1, dtype=np.float64)
    return float(np.dot(table[1 : n + 1].astype(np.float64), 1.0 / idx))


def gap1_written_squarefree_sum(n: int, mu: np.ndarray | None = None) -> float:
    """The Gap 1 Task 2 display: (36/π⁴) Σ_{squarefree d≤N} (log N − log d)² / d.

    Every term is nonnegative. The claimed −log N / (2π) target is negative.
    """
    table = mobius_table(n) if mu is None else mu
    total = 0.0
    log_n = math.log(n)
    for d in range(1, n + 1):
        if table[d] * table[d] != 1:
            continue
        total += (log_n - math.log(d)) ** 2 / d
    return (36.0 / math.pi**4) * total


def frobenius_diff(n: int) -> float:
    mu = mobius_table(n)
    return float(np.linalg.norm(operator_a(n) - operator_b(n, mu)))


def probe_row(n: int) -> dict[str, float | int]:
    mu = mobius_table(n)
    a = operator_a(n)
    b = operator_b(n, mu)
    v_mu = trial_mu_over_sqrt(n, mu)
    v_one = trial_one_over_sqrt(n)
    lam_a = lambda_min(a)
    log_n = math.log(n)
    m_n = mertens(n, mu)
    return {
        "N": n,
        "lambda_min_A": lam_a,
        "lambda_min_A_over_logN": lam_a / log_n,
        "lambda_min_B": lambda_min(b),
        "rayleigh_A_mu": rayleigh(a, v_mu),
        "rayleigh_A_one": rayleigh(a, v_one),
        "rayleigh_B_one": rayleigh(b, v_one),
        "squarefree_U": gap1_written_squarefree_sum(n, mu),
        "target_two_pi": MINUS_ONE_OVER_TWO_PI * log_n,
        "target_pi_sq": MINUS_ONE_OVER_PI_SQ * log_n,
        "M": m_n,
        "abs_M_over_sqrtN": abs(m_n) / math.sqrt(n),
        "sum_mu_over_n": sum_mu_over_n(n, mu),
        "A_11": float(a[0, 0]),
        "frobenius_A_minus_B": float(np.linalg.norm(a - b)),
    }


def probe_table(sizes: Sequence[int] = (20, 30, 50, 80, 100)) -> list[dict[str, float | int]]:
    return [probe_row(int(n)) for n in sizes]
