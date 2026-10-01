"""Orthonormal spectral form of the Mertens identity, and transfer rules."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

from .identity import (
    BRIDGE_COMPLETE,
    CANCELLATION_STATUS,
    SCOPE_STATEMENT,
    mertens,
    mobius_table,
    q_matrix,
)


@dataclass(frozen=True)
class SpectralDecomposition:
    n: int
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray
    weights: np.ndarray
    weighted_sum: float
    mertens: int
    residual: float
    op_norm: float
    crude_bound: float
    weight_min: float
    weight_max: float
    weight_sum: float
    weight_sum_target: float


@dataclass(frozen=True)
class SpectralCluster:
    eigenvalue: float
    multiplicity: int
    projector_weight: float
    contribution: float


@dataclass(frozen=True)
class TransferAssessment:
    """Whether the spectral rewrite is a useful bound, or only a rewrite."""

    identity_proved: bool
    cancellation_status: str
    bridge_complete: bool
    useful_transfer: bool
    scope: str
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _weights_from_basis(eigenvectors: np.ndarray, diag: np.ndarray) -> np.ndarray:
    """w_j = v_jᵀ D v_j = Σ_i i (v_j)_i² for an orthonormal eigenbasis."""
    return np.einsum("ij,i,ij->j", eigenvectors, diag, eigenvectors)


def spectral_decomposition(n: int, mu: np.ndarray | None = None) -> SpectralDecomposition:
    """Q_N v_j = λ_j v_j, then M(N) = Σ λ_j w_j with w_j = v_jᵀ D_N v_j."""
    table = mu if mu is not None else mobius_table(n)
    q = q_matrix(n, table)
    diag = np.arange(1, n + 1, dtype=np.float64)
    eigenvalues, eigenvectors = np.linalg.eigh(q)
    weights = _weights_from_basis(eigenvectors, diag)
    weighted_sum = float(np.dot(eigenvalues, weights))
    m_value = mertens(n, table)
    op_norm = float(np.max(np.abs(eigenvalues)))
    weight_sum_target = n * (n + 1) / 2.0
    return SpectralDecomposition(
        n=n,
        eigenvalues=eigenvalues,
        eigenvectors=eigenvectors,
        weights=weights,
        weighted_sum=weighted_sum,
        mertens=m_value,
        residual=abs(weighted_sum - m_value),
        op_norm=op_norm,
        crude_bound=op_norm * weight_sum_target,
        weight_min=float(np.min(weights)),
        weight_max=float(np.max(weights)),
        weight_sum=float(np.sum(weights)),
        weight_sum_target=weight_sum_target,
    )


def group_spectral_weights(
    decomp: SpectralDecomposition,
    *,
    rel_tol: float = 1e-8,
    abs_tol: float = 1e-10,
) -> list[SpectralCluster]:
    """Basis-independent weights Tr(D_N P_λ) for clustered eigenvalues."""
    order = np.argsort(decomp.eigenvalues)
    evals = decomp.eigenvalues[order]
    weights = decomp.weights[order]
    clusters: list[SpectralCluster] = []
    start = 0
    while start < evals.size:
        end = start + 1
        scale = max(1.0, abs(float(evals[start])))
        while end < evals.size and abs(evals[end] - evals[start]) <= max(
            abs_tol, rel_tol * scale
        ):
            end += 1
        projector_weight = float(np.sum(weights[start:end]))
        eigenvalue = float(np.mean(evals[start:end]))
        clusters.append(
            SpectralCluster(
                eigenvalue=eigenvalue,
                multiplicity=end - start,
                projector_weight=projector_weight,
                contribution=eigenvalue * projector_weight,
            )
        )
        start = end
    return clusters


def spectral_identity(n: int, mu: np.ndarray | None = None) -> SpectralDecomposition:
    """Public alias: orthonormal-eigenbasis form of the identity."""
    return spectral_decomposition(n, mu)


def congruence_eigenvalues(n: int, mu: np.ndarray | None = None) -> np.ndarray:
    """Eigenvalues of A_N = D_N^{1/2} Q_N D_N^{1/2}. Their sum is M(N).

    This is an alternative packaging, not an independent cancellation proof.
    """
    table = mu if mu is not None else mobius_table(n)
    q = q_matrix(n, table)
    scale = np.sqrt(np.arange(1, n + 1, dtype=np.float64))
    a = (scale[:, None] * q) * scale[None, :]
    return np.linalg.eigvalsh(a)


def assess_transfer(
    *,
    identity_residual_ok: bool,
    independent_qn_bound: bool = False,
) -> TransferAssessment:
    """Refuse to declare the bridge complete from a tractable spectrum.

    A useful transfer argument requires a cancellation bound derived from
    independently established properties of Q_N, not from an equivalent
    restatement of |M(N)| ≤ C_ε N^{1/2+ε}.
    """
    reasons = [
        "M(N) = Tr(D_N Q_N) is proved from the diagonal.",
        "M(N) = Σ λ_j w_j is the same identity in an orthonormal eigenbasis.",
        "1 ≤ w_j ≤ N and Σ w_j = N(N+1)/2, so weights carry the index distribution.",
        "The crude bound |M(N)| ≤ ||Q_N||_op N(N+1)/2 supplies no square-root cancellation.",
        "A lower spectral floor or a gap does not replace the missing weight estimate.",
        "The candidate |Σ λ Tr(D_N P_λ)| ≤ C_ε N^{1/2+ε} is the Mertens target "
        "in spectral coordinates and remains OPEN.",
    ]
    if not independent_qn_bound:
        reasons.append(
            "No independently established Q_N property was supplied, so "
            "the rewrite is not a transfer argument."
        )
    useful = bool(identity_residual_ok and independent_qn_bound)
    return TransferAssessment(
        identity_proved=identity_residual_ok,
        cancellation_status=CANCELLATION_STATUS,
        bridge_complete=BRIDGE_COMPLETE and useful,
        useful_transfer=useful,
        scope=SCOPE_STATEMENT,
        reasons=tuple(reasons),
    )


def cancellation_diagnostics(decomp: SpectralDecomposition) -> dict[str, float]:
    """Unsigned mass versus signed sum: why |Σ λ w| can be far below Σ |λ w|."""
    contrib = decomp.eigenvalues * decomp.weights
    abs_mass = float(np.sum(np.abs(contrib)))
    signed = float(np.sum(contrib))
    pos = float(np.sum(contrib[contrib > 0]))
    neg = float(np.sum(contrib[contrib < 0]))
    denom = max(abs(signed), 1e-15)
    corr = _abs_lambda_weight_corr(decomp.eigenvalues, decomp.weights)
    return {
        "signed_sum": signed,
        "abs_mass": abs_mass,
        "cancellation_ratio": abs_mass / denom,
        "positive_mass": pos,
        "negative_mass": neg,
        "op_norm": decomp.op_norm,
        "crude_bound": decomp.crude_bound,
        "crude_over_abs_m": decomp.crude_bound / max(abs(decomp.mertens), 1.0),
        "abs_m_over_sqrt_n": abs(decomp.mertens) / np.sqrt(decomp.n),
        "abs_lambda_weight_corr": corr,
        "weight_min": decomp.weight_min,
        "weight_max": decomp.weight_max,
        "weight_sum": decomp.weight_sum,
    }


def _abs_lambda_weight_corr(eigenvalues: np.ndarray, weights: np.ndarray) -> float:
    x = np.abs(eigenvalues)
    y = weights
    if x.size < 2:
        return float("nan")
    x = x - x.mean()
    y = y - y.mean()
    denom = float(np.linalg.norm(x) * np.linalg.norm(y))
    if denom == 0.0:
        return float("nan")
    return float(np.dot(x, y) / denom)
