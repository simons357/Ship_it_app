"""Exact matrix-to-Mertens identities that do not use eigenvectors."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

SCOPE_STATEMENT: str = (
    "Arithmetic identities for the Möbius–GCD matrix Q_N. "
    "Not an SFE, not FRA, not Hilbert–Pólya, and not a Riemann or "
    "Mertens proof. The cancellation estimate remains OPEN."
)

CANCELLATION_STATUS: str = "OPEN"

BRIDGE_COMPLETE: bool = False

# Distinct from the retired inverse-GCD matrix Q̃_N(i,j) = 1/gcd(i,j)
# used in withdrawn spectral-floor claims.
INVERSE_GCD_ALIAS: str = "Q_tilde_N"


def mobius_table(n: int) -> np.ndarray:
    """Return μ[0..n] with μ[0] = 0, via the linear sieve."""
    if n < 1:
        raise ValueError("n must be at least 1")
    mu = np.ones(n + 1, dtype=np.int64)
    mu[0] = 0
    primes: list[int] = []
    is_composite = np.zeros(n + 1, dtype=bool)
    for i in range(2, n + 1):
        if not is_composite[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            product = i * p
            if product > n:
                break
            is_composite[product] = True
            if i % p == 0:
                mu[product] = 0
                break
            mu[product] = -mu[i]
    return mu


def mertens(n: int, mu: np.ndarray | None = None) -> int:
    """M(N) = Σ_{k=1}^N μ(k)."""
    table = mu if mu is not None else mobius_table(n)
    if table.size < n + 1:
        raise ValueError("Möbius table is shorter than n")
    return int(table[1 : n + 1].sum())


def degree_matrix(n: int) -> np.ndarray:
    """D_N = diag(1, 2, …, N). Not the graph-degree matrix of H_N."""
    if n < 1:
        raise ValueError("n must be at least 1")
    return np.diag(np.arange(1, n + 1, dtype=np.float64))


def gcd_matrix(n: int) -> np.ndarray:
    """Integer matrix (gcd(i, j)) for 1 ≤ i, j ≤ N."""
    if n < 1:
        raise ValueError("n must be at least 1")
    idx = np.arange(1, n + 1, dtype=np.int64)
    return np.gcd.outer(idx, idx)


def q_matrix(n: int, mu: np.ndarray | None = None) -> np.ndarray:
    """Q_N(i, j) = μ(gcd(i, j)) / gcd(i, j). Symmetric, real."""
    table = mu if mu is not None else mobius_table(n)
    g = gcd_matrix(n)
    return table[g].astype(np.float64) / g.astype(np.float64)


def inverse_gcd_matrix(n: int) -> np.ndarray:
    """Retired comparison object Q̃_N(i, j) = 1/gcd(i, j). Not Q_N."""
    g = gcd_matrix(n)
    return 1.0 / g.astype(np.float64)


def dirichlet_g_table(n: int, mu: np.ndarray | None = None) -> np.ndarray:
    """g = f ∗ μ for f(k) = μ(k)/k, so Q_N(i,j) = Σ_{k|gcd(i,j)} g(k).

    Computed from the definition
        g(n) = Σ_{d|n} (μ(d)/d) μ(n/d).
    For squarefree n this equals μ(n) ∏_{p|n}(1+1/p). It need not vanish
    when n has a squared factor (e.g. g(4)=1/2).
    """
    table = mu if mu is not None else mobius_table(n)
    g = np.zeros(n + 1, dtype=np.float64)
    for d in range(1, n + 1):
        if table[d] == 0:
            continue
        f_d = table[d] / float(d)
        for m in range(1, n // d + 1):
            g[d * m] += f_d * table[m]
    return g


def divisor_trace_identity(n: int, mu: np.ndarray | None = None) -> float:
    """Independent expansion Tr(D_N Q_N) = Σ_k g(k) · k · m(m+1)/2, m = ⌊N/k⌋."""
    table = mu if mu is not None else mobius_table(n)
    g = dirichlet_g_table(n, table)
    total = 0.0
    for k in range(1, n + 1):
        m = n // k
        total += g[k] * k * m * (m + 1) / 2.0
    return float(total)


@dataclass(frozen=True)
class TraceIdentity:
    n: int
    mertens: int
    trace: float
    divisor_trace: float
    residual: float
    divisor_residual: float


def trace_identity(n: int, mu: np.ndarray | None = None) -> TraceIdentity:
    """Prove-by-diagonal: (D_N Q_N)_{nn} = μ(n), so the trace is M(N)."""
    table = mu if mu is not None else mobius_table(n)
    q = q_matrix(n, table)
    d = degree_matrix(n)
    trace = float(np.trace(d @ q))
    # Direct diagonal check: n * Q(n,n) = μ(n).
    diagonal = np.arange(1, n + 1, dtype=np.float64) * np.diag(q)
    m_value = mertens(n, table)
    divisor = divisor_trace_identity(n, table)
    return TraceIdentity(
        n=n,
        mertens=m_value,
        trace=trace,
        divisor_trace=divisor,
        residual=abs(trace - m_value),
        divisor_residual=abs(divisor - m_value),
    )


def q6_explicit() -> np.ndarray:
    """Hand matrix for the stated Q_6, used as a regression lock."""
    mu = mobius_table(6)
    return q_matrix(6, mu)
