"""Sensitivity, local identifiability, conditioning, and global checks.

Jacobian rank is a local test. It does not establish global identifiability
and must not be reported as “the parameters are identifiable.”
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from .schema import FORBIDDEN_IDENTIFIABILITY, IDENTIFIABILITY_FULL_RANK, IDENTIFIABILITY_SENSITIVITY


@dataclass
class IdentifiabilityReport:
    sensitivity: np.ndarray
    jacobian: np.ndarray
    rank: int
    singular_values: np.ndarray
    condition_metric: float | None
    locally_full_rank: bool
    global_status: str
    statement: str
    warnings: list[str] = field(default_factory=list)
    product_ambiguities: list[str] = field(default_factory=list)

    def as_claim(self) -> str:
        return self.statement


def finite_difference_jacobian(
    observable: Callable[[np.ndarray], np.ndarray],
    x0: np.ndarray,
    step: float = 1e-6,
) -> np.ndarray:
    x0 = np.asarray(x0, dtype=float)
    f0 = np.asarray(observable(x0), dtype=float).reshape(-1)
    jac = np.zeros((f0.size, x0.size), dtype=float)
    for j in range(x0.size):
        xp = x0.copy()
        xp[j] += step
        fp = np.asarray(observable(xp), dtype=float).reshape(-1)
        jac[:, j] = (fp - f0) / step
    return jac


def analyze_identifiability(
    jacobian: np.ndarray,
    *,
    parameter_names: list[str] | None = None,
    product_groups: list[list[str]] | None = None,
    global_status: str = "not_tested",
    atol: float = 1e-8,
) -> IdentifiabilityReport:
    j = np.asarray(jacobian, dtype=float)
    if j.ndim == 1:
        j = j.reshape(1, -1)
    names = parameter_names or [f"x{i}" for i in range(j.shape[1])]
    if j.size == 0:
        sv = np.array([])
        rank = 0
        cond = None
    else:
        sv = np.linalg.svd(j, compute_uv=False)
        rank = int(np.sum(sv > atol * max(1.0, sv[0])))
        positive = sv[sv > atol * max(1.0, sv[0] if sv.size else 1.0)]
        cond = float(positive[0] / positive[-1]) if positive.size else None
    locally_full = rank == j.shape[1] and j.shape[1] > 0
    warnings = []
    products = []
    for group in product_groups or []:
        products.append(
            "Parameters "
            + " and ".join(group)
            + " enter only through a product and are not separately "
            "identifiable from the stated observables without additional information."
        )
        locally_full = False
    if locally_full:
        statement = IDENTIFIABILITY_FULL_RANK
    elif j.size:
        statement = IDENTIFIABILITY_SENSITIVITY
    else:
        statement = "No Jacobian was available; identifiability was not assessed."
    if global_status == "not_tested":
        warnings.append(
            "Global identifiability was not tested. Distinct distant "
            "parameter sets may still generate identical observations."
        )
    warnings.append(
        f"Do not report {FORBIDDEN_IDENTIFIABILITY!r} from a local Jacobian."
    )
    return IdentifiabilityReport(
        sensitivity=j,
        jacobian=j,
        rank=rank,
        singular_values=sv,
        condition_metric=cond,
        locally_full_rank=locally_full and not products,
        global_status=global_status,
        statement=statement,
        warnings=warnings,
        product_ambiguities=products,
        # names retained only in products
    )


def product_model_observable(params: np.ndarray, x: np.ndarray) -> np.ndarray:
    """y = a b x. Used by the acceptance test for parameter redundancy."""
    a, b = params
    return a * b * x


def analyze_product_abx(x: np.ndarray, a0: float = 2.0, b0: float = 3.0) -> IdentifiabilityReport:
    def obs(params: np.ndarray) -> np.ndarray:
        return product_model_observable(params, x)

    jac = finite_difference_jacobian(obs, np.array([a0, b0], dtype=float))
    report = analyze_identifiability(
        jac,
        parameter_names=["a", "b"],
        product_groups=[["a", "b"]],
        global_status="product_ambiguity_detected",
    )
    report.warnings.append(
        "y = a b x with only y and x observed cannot separate a from b: "
        "for any nonzero α, (αa, b/α) yields the same observations."
    )
    return report
