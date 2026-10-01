"""Möbius–GCD matrix Q_N and the spectral Mertens identity.

This is a separate arithmetic book. It is not Functional Role Analysis,
not a Simons Field Equation, not Hilbert–Pólya, and not a proof of the
Riemann hypothesis or the Mertens conjecture.

Exact objects, kept as stated:

    Q_N(i, j) = μ(gcd(i, j)) / gcd(i, j),
    D_N = diag(1, 2, …, N).

Proved identities (diagonal, then spectral):

    M(N) = Tr(D_N Q_N) = Σ_j λ_j w_j,    w_j = v_jᵀ D_N v_j,

and, for a repeated eigenvalue, the basis-independent weight
Tr(D_N P_λ).

The cancellation estimate

    |Σ_λ λ Tr(D_N P_λ)| ≤ C_ε N^{1/2+ε}

is OPEN. As written it is only the Mertens target in spectral
coordinates. A useful transfer would derive it from independently
established properties of Q_N. Eigenvalue information alone, a spectral
floor, and a gap do not close the estimate.
"""

from .identity import (
    BRIDGE_COMPLETE,
    CANCELLATION_STATUS,
    SCOPE_STATEMENT,
    degree_matrix,
    mertens,
    mobius_table,
    q_matrix,
    trace_identity,
)
from .spectral import (
    TransferAssessment,
    assess_transfer,
    group_spectral_weights,
    spectral_decomposition,
    spectral_identity,
)

__all__ = [
    "BRIDGE_COMPLETE",
    "CANCELLATION_STATUS",
    "SCOPE_STATEMENT",
    "TransferAssessment",
    "assess_transfer",
    "degree_matrix",
    "group_spectral_weights",
    "mertens",
    "mobius_table",
    "q_matrix",
    "spectral_decomposition",
    "spectral_identity",
    "trace_identity",
]

__version__ = "0.1.0"
