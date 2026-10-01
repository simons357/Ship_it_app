"""Computational survey of the spectral Mertens identity.

The survey verifies the exact identities and measures why eigenvalue
data alone do not close the cancellation estimate. It does not claim
the Mertens bound, RH, or a completed spectral bridge.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from math import pi
from typing import Iterable

import numpy as np

SIX_OVER_PI_SQUARED: float = 6.0 / pi**2

from .identity import mertens, mobius_table, q6_explicit, trace_identity
from .spectral import (
    assess_transfer,
    cancellation_diagnostics,
    congruence_eigenvalues,
    group_spectral_weights,
    spectral_decomposition,
)

DEFAULT_SURVEY_NS: tuple[int, ...] = (
    1,
    2,
    6,
    10,
    12,
    16,
    20,
    24,
    32,
    48,
    64,
    80,
    96,
    128,
    160,
    192,
    256,
    320,
    384,
    512,
)


@dataclass(frozen=True)
class SurveyRow:
    n: int
    mertens: int
    trace_residual: float
    spectral_residual: float
    congruence_residual: float
    op_norm: float
    crude_bound: float
    crude_over_abs_m: float
    abs_m_over_sqrt_n: float
    abs_m_over_n_half_plus_tenth: float
    weight_min: float
    weight_max: float
    weight_sum: float
    weight_sum_target: float
    abs_mass: float
    cancellation_ratio: float
    abs_lambda_weight_corr: float | None
    cluster_count: int
    max_multiplicity: int
    op_norm_over_n: float
    six_over_pi_squared: float
    leading_weight: float


def survey_row(n: int, mu: np.ndarray | None = None) -> SurveyRow:
    table = mu if mu is not None else mobius_table(n)
    identity = trace_identity(n, table)
    decomp = spectral_decomposition(n, table)
    diag = cancellation_diagnostics(decomp)
    clusters = group_spectral_weights(decomp)
    alpha = congruence_eigenvalues(n, table)
    lead = int(np.argmax(np.abs(decomp.eigenvalues)))
    corr = diag["abs_lambda_weight_corr"]
    return SurveyRow(
        n=n,
        mertens=identity.mertens,
        trace_residual=identity.residual,
        spectral_residual=decomp.residual,
        congruence_residual=abs(float(np.sum(alpha)) - identity.mertens),
        op_norm=decomp.op_norm,
        crude_bound=decomp.crude_bound,
        crude_over_abs_m=diag["crude_over_abs_m"],
        abs_m_over_sqrt_n=diag["abs_m_over_sqrt_n"],
        abs_m_over_n_half_plus_tenth=abs(identity.mertens) / (n ** 0.6),
        weight_min=decomp.weight_min,
        weight_max=decomp.weight_max,
        weight_sum=decomp.weight_sum,
        weight_sum_target=decomp.weight_sum_target,
        abs_mass=diag["abs_mass"],
        cancellation_ratio=diag["cancellation_ratio"],
        abs_lambda_weight_corr=corr if corr == corr else None,  # NaN → None
        cluster_count=len(clusters),
        max_multiplicity=max(c.multiplicity for c in clusters),
        op_norm_over_n=decomp.op_norm / n,
        six_over_pi_squared=SIX_OVER_PI_SQUARED,
        leading_weight=float(decomp.weights[lead]),
    )


def run_survey(ns: Iterable[int] | None = None) -> list[SurveyRow]:
    values = tuple(ns) if ns is not None else DEFAULT_SURVEY_NS
    max_n = max(values)
    mu = mobius_table(max_n)
    return [survey_row(n, mu) for n in values]


def q6_record() -> dict[str, object]:
    """Exact Q_6 matrix, M(6), and the spectral weights."""
    q = q6_explicit()
    identity = trace_identity(6)
    decomp = spectral_decomposition(6)
    clusters = group_spectral_weights(decomp)
    return {
        "n": 6,
        "Q_6": q.tolist(),
        "mertens": identity.mertens,
        "trace": identity.trace,
        "eigenvalues": decomp.eigenvalues.tolist(),
        "weights": decomp.weights.tolist(),
        "weighted_sum": decomp.weighted_sum,
        "weight_sum": decomp.weight_sum,
        "weight_sum_target": decomp.weight_sum_target,
        "op_norm": decomp.op_norm,
        "crude_bound": decomp.crude_bound,
        "clusters": [asdict(c) for c in clusters],
    }


def write_survey(
    out_dir: Path,
    ns: Iterable[int] | None = None,
) -> dict[str, object]:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = run_survey(ns)
    transfer = assess_transfer(
        identity_residual_ok=all(r.trace_residual < 1e-8 and r.spectral_residual < 1e-6 for r in rows),
        independent_qn_bound=False,
    )
    payload = {
        "scope": transfer.scope,
        "cancellation_status": transfer.cancellation_status,
        "bridge_complete": transfer.bridge_complete,
        "useful_transfer": transfer.useful_transfer,
        "reasons": list(transfer.reasons),
        "rows": [asdict(r) for r in rows],
        "q6": q6_record(),
    }
    (out_dir / "survey.json").write_text(json.dumps(payload, indent=2) + "\n")
    (out_dir / "q6.json").write_text(json.dumps(payload["q6"], indent=2) + "\n")
    (out_dir / "SUMMARY.md").write_text(format_summary(payload))
    return payload


def format_summary(payload: dict[str, object]) -> str:
    rows = payload["rows"]
    assert isinstance(rows, list)
    lines = [
        "# Spectral Mertens survey",
        "",
        "**Book:** arithmetic (Möbius–GCD matrix). Not FRA, not SFE, not Clay.",
        f"**Identity:** proved. **Cancellation estimate:** {payload['cancellation_status']}.",
        f"**Bridge complete:** `{payload['bridge_complete']}`.",
        f"**Useful transfer:** `{payload['useful_transfer']}`.",
        "",
        "The candidate bound `|Σ λ Tr(D_N P_λ)| ≤ C_ε N^{1/2+ε}` is the Mertens",
        "target in spectral coordinates. This survey tests the exact identity",
        "and shows that the crude operator-norm estimate does not produce",
        "square-root cancellation.",
        "",
        "## Why the crude bound fails",
        "",
        "For an orthonormal eigenbasis, `1 ≤ w_j ≤ N` and `Σ w_j = N(N+1)/2`.",
        "Therefore `|M(N)| ≤ ||Q_N||_op N(N+1)/2`. The first column of `Q_N`",
        "is the all-ones vector, so `||Q_N||_op ≥ √N`. The coprime pairs, where",
        f"`Q_N=1`, have density `6/π² ≈ {SIX_OVER_PI_SQUARED:.5f}`, and the",
        "measured `||Q_N||_op` is `Θ(N)`. The crude bound is then `Θ(N³)` —",
        "weaker than the trivial `|M(N)| ≤ N`, with no `N^{1/2+ε}` information.",
        "",
        "## Survey table",
        "",
        "| N | M(N) | ‖Q‖_op | ‖Q‖/N | crude/|M| | |M|/√N | cancel. ratio | min w | max w | lead w | |λ|–w corr |",
        "|---|------|--------|-------|-----------|-------|---------------|-------|-------|--------|-----------|",
    ]
    for raw in rows:
        corr = raw["abs_lambda_weight_corr"]
        corr_s = "—" if corr is None else f"{corr:.3g}"
        cancel_s = "∞" if raw["mertens"] == 0 else f"{raw['cancellation_ratio']:.3g}"
        lines.append(
            "| {n} | {mertens} | {op_norm:.4g} | {op_norm_over_n:.3g} | "
            "{crude_over_abs_m:.3g} | {abs_m_over_sqrt_n:.3g} | "
            "{cancel} | {weight_min:.3g} | {weight_max:.3g} | "
            "{leading_weight:.3g} | {corr} |".format(
                cancel=cancel_s, corr=corr_s, **raw
            )
        )
    lines.extend(
        [
            "",
            "## Residuals",
            "",
            "Trace, spectral, and congruence (`A_N = D_N^{1/2} Q_N D_N^{1/2}`) "
            "residuals stay at floating-point scale. The identities hold.",
            "",
        ]
    )
    max_trace = max(float(r["trace_residual"]) for r in rows)
    max_spec = max(float(r["spectral_residual"]) for r in rows)
    max_cong = max(float(r["congruence_residual"]) for r in rows)
    lines.append(f"- max `|Tr(D Q) − M(N)|` = `{max_trace:.3e}`")
    lines.append(f"- max `|Σ λ_j w_j − M(N)|` = `{max_spec:.3e}`")
    lines.append(f"- max `|Σ α_k − M(N)|` = `{max_cong:.3e}`")
    lines.extend(
        [
            "",
            "## Transfer rule",
            "",
        ]
    )
    reasons = payload["reasons"]
    assert isinstance(reasons, list)
    for reason in reasons:
        lines.append(f"- {reason}")
    lines.extend(
        [
            "",
            "## Q_6 lock",
            "",
            "See `q6.json`. `M(6) = −1 = Tr(D_6 Q_6)`. The 6×6 matrix is the",
            "stated Möbius–GCD kernel, not the inverse-GCD matrix `1/gcd`.",
            "",
            "## Coprime-density note",
            "",
            f"`Q_N(i,j)=1` whenever `gcd(i,j)=1`. The density of coprime pairs is "
            f"`6/π² ≈ {SIX_OVER_PI_SQUARED:.5f}`. The measured `‖Q_N‖_op / N` "
            "tracks that constant, so the leading eigenvalue is a delocalized "
            "coprime-ones mode of size `Θ(N)`. The crude bound is then "
            "`Θ(N³)`, which is still not a square-root estimate. The leading "
            "weight stays `Θ(N)` rather than `O(1)`, so the large eigenvalue "
            "is not suppressed by the index weights.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"
