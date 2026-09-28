"""One-cycle loss law. Direct prediction → measurement test for Heavy.

If the phase errors on a rank-one cycle obey

    sum_i c_i ε_i = δ

and the local objective loss is (1/2) sum_i w_i ε_i², the constrained
minimizer is

    ε_i = δ (c_i / w_i) / sum_j c_j² / w_j

hence

    1 - objective  ∼  δ² / (2 sum_j c_j² / w_j)

under the normalization that the unconstrained (TREE) objective is 1.
The exact nonlinear stationarity of the cosine objective,

    w_i sin ε_i = λ c_i,

is solved in one dimension. This is not the big polarization optimizer
and is not a scale-decay exponent.
"""

from __future__ import annotations

import math
from typing import Sequence


def cycle_quadratic_weight(c: Sequence[int], w: Sequence[float]) -> float:
    if len(c) != len(w):
        raise ValueError("c and w must have the same length")
    s = 0.0
    for ci, wi in zip(c, w):
        if wi <= 0.0:
            raise ValueError("weights must be positive")
        s += float(ci) * float(ci) / float(wi)
    if s <= 0.0:
        raise ValueError("cycle support is empty")
    return s


def quadratic_minimizer(
    c: Sequence[int],
    w: Sequence[float],
    delta: float,
) -> dict:
    """Constrained minimizer of (1/2) sum w_i ε_i² s.t. c·ε = δ."""
    s = cycle_quadratic_weight(c, w)
    eps = [float(delta) * (float(ci) / float(wi)) / s for ci, wi in zip(c, w)]
    loss = 0.5 * sum(float(wi) * e * e for wi, e in zip(w, eps))
    predicted = (float(delta) ** 2) / (2.0 * s)
    return {
        "eps": eps,
        "loss": loss,
        "one_minus_objective": predicted,
        "S": s,
        "delta": float(delta),
        "formula": "δ² / (2 ∑ c_j² / w_j)",
        "constraint": sum(float(ci) * e for ci, e in zip(c, eps)),
    }


def nonlinear_stationarity(
    c: Sequence[int],
    w: Sequence[float],
    delta: float,
    *,
    tol: float = 1e-12,
) -> dict:
    """Solve w_i sin ε_i = λ c_i with ∑ c_i ε_i = δ, |ε_i| ≤ π/2.

    This is the stationarity condition for maximizing ∑ w_i cos ε_i
    (TREE objective normalized as ∑ w_i when δ = 0) subject to the
    cycle constraint. No polarization optimizer.
    """
    if len(c) != len(w):
        raise ValueError("c and w must have the same length")
    target = float(delta)

    def residual(lam: float) -> float:
        s = 0.0
        for ci, wi in zip(c, w):
            if ci == 0:
                continue
            x = lam * float(ci) / float(wi)
            x = max(-1.0, min(1.0, x))
            s += float(ci) * math.asin(x)
        return s - target

    support_w = [float(wi) for ci, wi in zip(c, w) if ci != 0]
    if not support_w:
        raise ValueError("cycle support is empty")
    # |λ| ≤ min_i w_i / |c_i| keeps |sin| ≤ 1.
    hi = min(float(wi) / abs(float(ci)) for ci, wi in zip(c, w) if ci != 0)
    lo = -hi
    rlo, rhi = residual(lo), residual(hi)
    reachable = rlo * rhi <= 0
    if not reachable:
        # Saturate at the endpoint with smaller |residual|.
        lam = lo if abs(rlo) < abs(rhi) else hi
        method = "clipped-endpoint"
    else:
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            rm = residual(mid)
            if rlo * rm <= 0:
                hi, rhi = mid, rm
            else:
                lo, rlo = mid, rm
            if hi - lo < tol:
                break
        lam = 0.5 * (lo + hi)
        method = "stationarity-bisection"

    eps = []
    objective = 0.0
    wsum = 0.0
    for ci, wi in zip(c, w):
        wsum += float(wi)
        if ci == 0:
            eps.append(0.0)
            objective += float(wi)
            continue
        x = max(-1.0, min(1.0, lam * float(ci) / float(wi)))
        e = math.asin(x)
        eps.append(e)
        objective += float(wi) * math.cos(e)

    # Normalization: TREE (δ=0) objective is ∑ w_i.
    one_minus = 1.0 - (objective / wsum if wsum else 1.0)
    quad = quadratic_minimizer(c, w, delta)
    # Local cosine loss ∑ w (1-cos ε) ≈ (1/2) ∑ w ε²; divide by ∑ w.
    predicted_norm = quad["one_minus_objective"] / wsum if wsum else quad["one_minus_objective"]
    return {
        "lambda": lam,
        "eps": eps,
        "objective_raw": objective,
        "objective_normalized": objective / wsum if wsum else 0.0,
        "one_minus_objective": one_minus,
        "quadratic_prediction": predicted_norm,
        "quadratic_loss_unnormalized": quad["one_minus_objective"],
        "method": method,
        "reachable": reachable,
        "constraint": sum(float(ci) * e for ci, e in zip(c, eps)),
        "delta": float(delta),
        "weights": [float(x) for x in w],
        "c": [int(x) for x in c],
        "not_optimizer_evidence": True,
    }


def prediction_measurement_test(
    c: Sequence[int],
    w: Sequence[float],
    delta: float,
    *,
    rel_tol: float = 0.05,
) -> dict:
    """Heavy's test: quadratic prediction vs nonlinear measurement.

    For small δ the relative gap must be below rel_tol. This is a
    finite-cycle law. It does not produce a decay exponent.
    """
    meas = nonlinear_stationarity(c, w, delta)
    pred = meas["quadratic_prediction"]
    got = meas["one_minus_objective"]
    denom = max(abs(pred), 1e-16)
    rel = abs(got - pred) / denom
    return {
        "delta": float(delta),
        "prediction": pred,
        "measurement": got,
        "relative_gap": rel,
        "pass_small_delta": rel <= rel_tol,
        "rel_tol": rel_tol,
        "boxed": "1 - objective ∼ δ² / (2 ∑ c_j² / w_j)",
        "scale_rate": "OPEN",
    }
