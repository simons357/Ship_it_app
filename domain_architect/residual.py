"""Residual analysis and missing-mechanism discovery.

R = y − ŷ   or, for an incomplete operator L̂,   R = L̂[y_obs]

Large structured residuals are treated as a missing-role problem, which
restricts subsequent mathematical search.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from .schema import FunctionalRole, ValidationGate


@dataclass
class ResidualAnalysis:
    residual: np.ndarray
    missing_role: FunctionalRole
    confidence: float
    rationale: str
    correlations: dict[str, float]
    recovered_parameter: dict[str, float] = field(default_factory=dict)
    operator_class: str = "unresolved"
    validation_gate: ValidationGate = ValidationGate.COMPUTATIONAL
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "missing_role": self.missing_role.value,
            "confidence": self.confidence,
            "rationale": self.rationale,
            "correlations": dict(self.correlations),
            "recovered_parameter": dict(self.recovered_parameter),
            "operator_class": self.operator_class,
            "validation_gate": self.validation_gate.value,
            "warnings": list(self.warnings),
            "residual_norm": float(np.linalg.norm(self.residual)),
        }


def _corr(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float).reshape(-1)
    b = np.asarray(b, dtype=float).reshape(-1)
    if a.size < 3 or float(np.std(a)) < 1e-12 or float(np.std(b)) < 1e-12:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def equation_residual(x: np.ndarray, v: np.ndarray, acc: np.ndarray, omega: float) -> np.ndarray:
    """R = ẍ + ω² x  of the incomplete undamped operator."""
    return np.asarray(acc, dtype=float) + (omega**2) * np.asarray(x, dtype=float)


def finite_difference_accel(x: np.ndarray, dt: float) -> np.ndarray:
    return np.gradient(np.gradient(np.asarray(x, dtype=float), dt), dt)


def classify_missing_mechanism(
    residual: np.ndarray,
    *,
    x: np.ndarray,
    v: np.ndarray,
    omega: float | None = None,
) -> ResidualAnalysis:
    """Correlate R with {1, x, ẋ} and assign a missing-role class."""
    r = np.asarray(residual, dtype=float).reshape(-1)
    ones = np.ones_like(r)
    corr = {
        "const": _corr(r, ones) if float(np.std(r)) > 1e-12 else (1.0 if abs(float(np.mean(r))) > 1e-8 else 0.0),
        "x": _corr(r, x),
        "v": _corr(r, v),
    }
    mean_r = float(np.mean(r))
    abs_corr = {k: abs(val) for k, val in corr.items()}
    # A near-constant residual is forcing even if corrcoef with 1 is undefined.
    if abs(mean_r) > 0.25 * (float(np.std(r)) + abs(mean_r) + 1e-12) and abs_corr["v"] < 0.5 and abs_corr["x"] < 0.5:
        amp = mean_r
        return ResidualAnalysis(
            residual=r,
            missing_role=FunctionalRole.FORCING,
            confidence=0.8,
            rationale=(
                "Residual is approximately constant and uncorrelated with x and ẋ. "
                "Missing-role class: forcing. Operator search is restricted to "
                "a constant input."
            ),
            correlations=corr,
            recovered_parameter={"A": amp},
            operator_class="constant_forcing",
        )
    if abs_corr["v"] >= max(abs_corr["x"], 0.55):
        gamma = -float(np.dot(r, v) / max(np.dot(v, v), 1e-18))
        recovered = {"gamma": gamma}
        if omega and omega > 0:
            recovered["zeta"] = gamma / (2.0 * omega)
        return ResidualAnalysis(
            residual=r,
            missing_role=FunctionalRole.DISSIPATION,
            confidence=min(0.95, 0.5 + 0.5 * abs_corr["v"]),
            rationale=(
                "Residual correlates with −ẋ. Missing-role class: dissipation. "
                "Operator search is restricted to linear damping γ ẋ, with "
                "γ̂ = −⟨R, ẋ⟩ / ⟨ẋ, ẋ⟩."
            ),
            correlations=corr,
            recovered_parameter=recovered,
            operator_class="linear_damping",
        )
    if abs_corr["x"] >= 0.55:
        return ResidualAnalysis(
            residual=r,
            missing_role=FunctionalRole.INTERACTION,
            confidence=min(0.9, 0.45 + 0.5 * abs_corr["x"]),
            rationale=(
                "Residual correlates with x. Missing-role class: interaction / "
                "restoring. Operator search is restricted to a multiple of x."
            ),
            correlations=corr,
            recovered_parameter={"delta_k": float(np.dot(r, x) / max(np.dot(x, x), 1e-18))},
            operator_class="restoring_mismatch",
        )
    return ResidualAnalysis(
        residual=r,
        missing_role=FunctionalRole.UNRESOLVED,
        confidence=0.2,
        rationale="Residual structure did not match forcing, dissipation, or restoring templates.",
        correlations=corr,
        operator_class="unresolved",
        warnings=["Retain multiple missing-role hypotheses; do not invent an equation."],
    )


def recover_missing_damping(
    x: np.ndarray,
    v: np.ndarray,
    *,
    omega: float,
    dt: float | None = None,
    acc: np.ndarray | None = None,
) -> ResidualAnalysis:
    if acc is None:
        if dt is None:
            raise ValueError("acc or dt is required")
        acc = finite_difference_accel(x, dt)
    residual = equation_residual(x, v, acc, omega)
    return classify_missing_mechanism(residual, x=x, v=v, omega=omega)
