"""Exact one-cycle cosine law, plus quadratic/quartic small-holonomy expansions.

Maximize

    ρ(ε) = (1/W) ∑_i w_i cos ε_i,    W = ∑_i w_i,    w_i > 0,

subject to the single primitive cycle constraint

    c^T ε = δ,    δ = wrap_{(−π, π]}(c^T b).

Channels with c_i = 0 align exactly (ε_i = 0) at a maximizer, so
every substantive sum below is over supp c.

Stationarity: w_i sin ε_i = λ c_i, hence |λ| ≤ min_{c_i ≠ 0} w_i/|c_i|.
Each equation has branches

    ε_i = n_i π + (−1)^{n_i} arcsin(λ c_i / w_i).

The exact solver enumerates admissible n and compares ρ. It does
not accept the first root. This is not the polarization optimizer
and is not a scale-decay exponent.
"""

from __future__ import annotations

import itertools
import math
from typing import Iterable, List, Sequence, Tuple

PI = math.pi
TWOPI = 2.0 * PI
SMALL_HOLONOMY_LIMIT = 0.5 * PI  # |δ| ≤ π/2 is the preregistered regime


def wrap_pi(x: float) -> float:
    """Wrap to (−π, π]."""
    y = float(x) - TWOPI * math.floor((float(x) + PI) / TWOPI)
    if y <= -PI:
        y += TWOPI
    return y


def holonomy_delta(c: Sequence[int], b: Sequence[float]) -> float:
    if len(c) != len(b):
        raise ValueError("c and b must have the same length")
    return wrap_pi(sum(int(ci) * float(bi) for ci, bi in zip(c, b)))


def _validate(c: Sequence[int], w: Sequence[float]) -> Tuple[List[int], List[float], List[int]]:
    if len(c) != len(w):
        raise ValueError("c and w must have the same length")
    cc = [int(x) for x in c]
    ww = [float(x) for x in w]
    if any(wi <= 0.0 for wi in ww):
        raise ValueError("weights must be positive")
    support = [i for i, ci in enumerate(cc) if ci != 0]
    if not support:
        raise ValueError("cycle support is empty")
    return cc, ww, support


def cycle_moments(c: Sequence[int], w: Sequence[float]) -> dict:
    """W, S, Q, λ_max. Substantive sums run over supp c."""
    cc, ww, support = _validate(c, w)
    W = float(sum(ww))
    S = 0.0
    Q = 0.0
    lam_max = None
    for i in support:
        ci, wi = float(cc[i]), ww[i]
        S += ci * ci / wi
        Q += (ci ** 4) / (wi ** 3)
        bound = wi / abs(ci)
        lam_max = bound if lam_max is None else min(lam_max, bound)
    return {
        "W": W,
        "S": S,
        "Q": Q,
        "lambda_max": float(lam_max),
        "support": support,
        "c": cc,
        "w": ww,
        "m": len(cc),
    }


def rho_of(eps: Sequence[float], w: Sequence[float]) -> float:
    W = float(sum(w))
    if W <= 0.0:
        raise ValueError("W must be positive")
    return sum(float(wi) * math.cos(float(e)) for wi, e in zip(w, eps)) / W


def cycle_quadratic_weight(c: Sequence[int], w: Sequence[float]) -> float:
    return cycle_moments(c, w)["S"]


def quadratic_minimizer(
    c: Sequence[int],
    w: Sequence[float],
    delta: float,
) -> dict:
    """Quadratic (order-δ²) channel law and 1−ρ.

    ε_i^{(2)} = (c_i / w_i) (δ / S),    1 − ρ^{(2)} = δ² / (2 W S).
    Off-cycle channels have c_i = 0 ⇒ ε_i^{(2)} = 0.
    """
    mom = cycle_moments(c, w)
    S, W = mom["S"], mom["W"]
    delta = float(delta)
    eps = [delta * (float(ci) / float(wi)) / S for ci, wi in zip(mom["c"], mom["w"])]
    unnormalized = 0.5 * sum(wi * e * e for wi, e in zip(mom["w"], eps))
    one_minus_rho = (delta * delta) / (2.0 * W * S)
    return {
        "eps": eps,
        "eps_label": "ε_i^{(2)} = c_i δ / (w_i S)",
        "loss_unnormalized": unnormalized,
        "one_minus_objective": unnormalized,  # (1/2) ∑ w ε² = δ² / (2S)
        "one_minus_rho": one_minus_rho,
        "W": W,
        "S": S,
        "Q": mom["Q"],
        "delta": delta,
        "formula": "δ² / (2 W S)",
        "constraint": sum(float(ci) * e for ci, e in zip(mom["c"], eps)),
        "off_cycle_zero": all(
            abs(e) < 1e-15 for e, ci in zip(eps, mom["c"]) if ci == 0
        ),
    }


def quartic_prediction(c: Sequence[int], w: Sequence[float], delta: float) -> dict:
    """Order-δ⁴ expansion on the alignment-connected branch. No numerical work.

    λ = δ/S − (Q / 6 S⁴) δ³ + O(δ⁵)

    1 − ρ_max = δ² / (2 W S) − (Q / 24 W S⁴) δ⁴ + O(δ⁶)
    """
    mom = cycle_moments(c, w)
    S, Q, W = mom["S"], mom["Q"], mom["W"]
    d = float(delta)
    d2 = d * d
    d3 = d2 * d
    d4 = d2 * d2
    S4 = S ** 4
    lam = (d / S) - (Q / (6.0 * S4)) * d3
    one_minus_rho = (d2 / (2.0 * W * S)) - (Q / (24.0 * W * S4)) * d4
    rho_max = 1.0 - (d2 / (2.0 * W * S)) + (Q * d4) / (24.0 * W * S4)
    return {
        "lambda_series": lam,
        "one_minus_rho": one_minus_rho,
        "rho_max": rho_max,
        "quadratic_term": d2 / (2.0 * W * S),
        "quartic_correction": -(Q / (24.0 * W * S4)) * d4,
        "W": W,
        "S": S,
        "Q": Q,
        "delta": d,
        "formula": "δ²/(2WS) − Q δ⁴/(24 W S⁴)",
        "note": "negative quartic: the quadratic slightly overestimates true loss",
    }


def _eps_on_branch(
    c: Sequence[int],
    w: Sequence[float],
    lam: float,
    n: Sequence[int],
    support: Sequence[int],
) -> List[float]:
    eps = [0.0] * len(c)
    for i in support:
        x = lam * float(c[i]) / float(w[i])
        x = max(-1.0, min(1.0, x))
        ni = int(n[i])
        eps[i] = ni * PI + ((-1) ** ni) * math.asin(x)
    return eps


def _rho_on_branch(
    c: Sequence[int],
    w: Sequence[float],
    lam: float,
    n: Sequence[int],
    support: Sequence[int],
    W: float,
) -> float:
    """ρ from cos ε_i = (−1)^{n_i} √(1 − (λ c_i/w_i)²) on support, 1 off-cycle."""
    acc = 0.0
    for i, wi in enumerate(w):
        if c[i] == 0:
            acc += float(wi)
            continue
        x = lam * float(c[i]) / float(w[i])
        x = max(-1.0, min(1.0, x))
        acc += float(wi) * ((-1) ** int(n[i])) * math.sqrt(max(0.0, 1.0 - x * x))
    return acc / W


def _constraint_on_branch(
    c: Sequence[int],
    w: Sequence[float],
    lam: float,
    n: Sequence[int],
    support: Sequence[int],
) -> float:
    s = 0.0
    for i in support:
        x = lam * float(c[i]) / float(w[i])
        x = max(-1.0, min(1.0, x))
        ni = int(n[i])
        s += float(c[i]) * (ni * PI + ((-1) ** ni) * math.asin(x))
    return s


def _bisect_root(f, lo: float, hi: float, flo: float, fhi: float, tol: float) -> float:
    a, b, fa, fb = lo, hi, flo, fhi
    for _ in range(80):
        mid = 0.5 * (a + b)
        fm = f(mid)
        if fa * fm <= 0:
            b, fb = mid, fm
        else:
            a, fa = mid, fm
        if b - a < tol:
            break
    return 0.5 * (a + b)


def _roots_of(
    f,
    lo: float,
    hi: float,
    *,
    n_grid: int = 256,
    tol: float = 1e-12,
) -> List[float]:
    """Find zeros of a continuous f on [lo, hi] by grid sign-changes."""
    if hi < lo:
        lo, hi = hi, lo
    xs = [lo + (hi - lo) * k / n_grid for k in range(n_grid + 1)]
    fs = [f(x) for x in xs]
    roots: List[float] = []
    for x, fx in zip(xs, fs):
        if abs(fx) <= tol:
            if not roots or abs(x - roots[-1]) > 10.0 * tol:
                roots.append(x)
    for a, b, fa, fb in zip(xs, xs[1:], fs, fs[1:]):
        if fa * fb < 0:
            roots.append(_bisect_root(f, a, b, fa, fb, tol))
    # Dedup
    roots.sort()
    uniq: List[float] = []
    for r in roots:
        if not uniq or abs(r - uniq[-1]) > 1e-10:
            uniq.append(r)
    return uniq


def _branch_vectors(m: int, support: Sequence[int], n_values: Sequence[int]) -> Iterable[Tuple[int, ...]]:
    k = len(support)
    for choice in itertools.product(n_values, repeat=k):
        n = [0] * m
        for idx, ni in zip(support, choice):
            n[idx] = int(ni)
        yield tuple(n)


def exact_one_cycle_optimum(
    c: Sequence[int],
    w: Sequence[float],
    delta: float,
    *,
    n_values: Sequence[int] = (-1, 0, 1),
    tol: float = 1e-12,
) -> dict:
    """Enumerate admissible branches; return the maximizer of ρ.

    Distinct geometric branches are n_i ∈ {−1, 0, 1}: n and n+2
    differ by 2π and are the same torus point. The solver still
    enumerates every admissible short n and compares ρ; it does
    not accept the first root. Off-cycle channels are locked at
    ε_i = 0. Ties keep the smallest ∑|n_i| (the alignment branch).
    """
    mom = cycle_moments(c, w)
    cc, ww, support = mom["c"], mom["w"], mom["support"]
    W, lam_max = mom["W"], mom["lambda_max"]
    target = float(delta)
    candidates = []

    for n in _branch_vectors(len(cc), support, n_values):
        def residual(lam: float, n=n) -> float:
            return _constraint_on_branch(cc, ww, lam, n, support) - target

        for lam in _roots_of(residual, -lam_max, lam_max, tol=tol):
            if abs(lam) > lam_max + 1e-12:
                continue
            rho = _rho_on_branch(cc, ww, lam, n, support, W)
            eps = _eps_on_branch(cc, ww, lam, n, support)
            constraint = _constraint_on_branch(cc, ww, lam, n, support)
            if abs(constraint - target) > 1e-8:
                continue
            candidates.append(
                {
                    "n": list(n),
                    "lambda": lam,
                    "rho": rho,
                    "eps": eps,
                    "constraint": constraint,
                    "principal": all(n[i] == 0 for i in support),
                }
            )

    if not candidates:
        return {
            "reachable": False,
            "rho": None,
            "one_minus_rho": None,
            "eps": None,
            "lambda": None,
            "n": None,
            "delta": target,
            "lambda_max": lam_max,
            "method": "branch-enumeration",
            "n_candidates": 0,
            "boxed_stationarity": "w_i sin ε_i = λ c_i",
        }

    best = max(
        candidates,
        key=lambda row: (
            round(row["rho"], 12),
            -sum(abs(v) for v in row["n"]),
            row["principal"],
        ),
    )
    off_cycle_zero = all(
        abs(best["eps"][i]) < 1e-12 for i in range(len(cc)) if cc[i] == 0
    )
    return {
        "reachable": True,
        "rho": best["rho"],
        "one_minus_rho": 1.0 - best["rho"],
        "eps": best["eps"],
        "lambda": best["lambda"],
        "n": best["n"],
        "principal_branch": best["principal"],
        "constraint": best["constraint"],
        "delta": target,
        "lambda_max": lam_max,
        "lambda_bound_ok": abs(best["lambda"]) <= lam_max + 1e-12,
        "off_cycle_zero": off_cycle_zero,
        "n_candidates": len(candidates),
        "method": "branch-enumeration",
        "boxed_stationarity": "w_i sin ε_i = λ c_i",
        "W": W,
        "S": mom["S"],
        "Q": mom["Q"],
        "c": cc,
        "w": ww,
        "not_optimizer_evidence": True,
    }


def nonlinear_stationarity(
    c: Sequence[int],
    w: Sequence[float],
    delta: float,
    *,
    tol: float = 1e-12,
) -> dict:
    """Exact one-cycle maximizer (branch-enumerated), with principal diagnostics."""
    exact = exact_one_cycle_optimum(c, w, delta, n_values=(-1, 0, 1), tol=tol)
    mom = cycle_moments(c, w)
    if not exact["reachable"]:
        return {
            "lambda": None,
            "eps": [0.0] * len(c),
            "objective_raw": None,
            "objective_normalized": None,
            "one_minus_objective": None,
            "rho": None,
            "method": "branch-enumeration",
            "reachable": False,
            "delta": float(delta),
            "lambda_max": mom["lambda_max"],
            "not_optimizer_evidence": True,
        }
    W = mom["W"]
    objective_raw = exact["rho"] * W
    return {
        "lambda": exact["lambda"],
        "eps": exact["eps"],
        "objective_raw": objective_raw,
        "objective_normalized": exact["rho"],
        "one_minus_objective": exact["one_minus_rho"],
        "rho": exact["rho"],
        "n": exact["n"],
        "principal_branch": exact["principal_branch"],
        "quadratic_prediction": (float(delta) ** 2) / (2.0 * W * mom["S"]),
        "method": "branch-enumeration",
        "reachable": True,
        "constraint": exact["constraint"],
        "delta": float(delta),
        "lambda_max": mom["lambda_max"],
        "lambda_bound_ok": exact["lambda_bound_ok"],
        "off_cycle_zero": exact["off_cycle_zero"],
        "n_candidates": exact["n_candidates"],
        "weights": mom["w"],
        "c": mom["c"],
        "not_optimizer_evidence": True,
    }


def small_holonomy_regime(delta: float) -> bool:
    return abs(float(delta)) <= SMALL_HOLONOMY_LIMIT + 1e-15


def heavy_one_cycle_test(
    c: Sequence[int],
    w: Sequence[float],
    delta: float,
    *,
    rel_tol_quad: float = 0.05,
    rel_tol_quart: float = 0.01,
) -> dict:
    """What Heavy should test on every genuine one-cycle instance.

    Predict ε_i^{(2)} and 1−ρ^{(2)}. Compare to the exact branch-enumerated
    optimum. For |δ| ≤ π/2 also compare 1−ρ^{(4)}. For |δ| > π/2 report
    the exact optimum and stamp the expansions OUTSIDE PREREGISTERED
    SMALL-HOLONOMY REGIME.
    """
    mom = cycle_moments(c, w)
    d = float(delta)
    in_regime = small_holonomy_regime(d)
    quad = quadratic_minimizer(c, w, d)
    quart = quartic_prediction(c, w, d)
    exact = exact_one_cycle_optimum(c, w, d)

    def _rel(pred: float, got: float) -> float:
        return abs(got - pred) / max(abs(pred), 1e-16)

    out = {
        "delta": d,
        "in_small_holonomy_regime": in_regime,
        "regime_limit": SMALL_HOLONOMY_LIMIT,
        "W": mom["W"],
        "S": mom["S"],
        "Q": mom["Q"],
        "lambda_max": mom["lambda_max"],
        "eps2": quad["eps"],
        "one_minus_rho2": quad["one_minus_rho"],
        "one_minus_rho4": quart["one_minus_rho"],
        "rho4": quart["rho_max"],
        "lambda_series": quart["lambda_series"],
        "exact": exact,
        "boxed_quadratic": "1 − ρ_max = δ² / (2 W S) + O(δ⁴)",
        "boxed_quartic": "1 − ρ_max = δ² / (2 W S) − Q δ⁴ / (24 W S⁴) + O(δ⁶)",
        "boxed_channel": "ε_i = (c_i / w_i) (δ / S) + O(δ³)",
        "boxed_off_cycle": "c_i = 0 ⇒ ε_i = 0",
        "scale_rate": "OPEN",
        "not_optimizer_evidence": True,
    }

    if not exact["reachable"]:
        out.update(
            {
                "pass_quadratic": False,
                "pass_quartic": False,
                "pass_channels": False,
                "stamp": "EXACT BRANCH INADMISSIBLE",
            }
        )
        return out

    got = exact["one_minus_rho"]
    rel2 = _rel(quad["one_minus_rho"], got)
    rel4 = _rel(quart["one_minus_rho"], got)
    channel_err = [
        abs(exact["eps"][i] - quad["eps"][i]) for i in range(len(c))
    ]
    # Off-cycle exact zeros.
    off_ok = exact["off_cycle_zero"]
    if not in_regime:
        out.update(
            {
                "measurement": got,
                "relative_gap_quadratic": rel2,
                "relative_gap_quartic": rel4,
                "channel_abs_err": channel_err,
                "pass_quadratic": False,
                "pass_quartic": False,
                "pass_channels": False,
                "pass_off_cycle": off_ok,
                "pass_small_delta": False,
                "stamp": "OUTSIDE PREREGISTERED SMALL-HOLONOMY REGIME",
                "note": "report the exact optimum; do not score quadratic/quartic",
            }
        )
        return out

    # Channel-by-channel: O(δ³) remainder. For |δ|≤π/2 this is a
    # sanity bound, not a derived NS exponent.
    chan_tol = 8.0 * abs(d) ** 3 + 1e-9
    pass_channels = all(err <= chan_tol for err in channel_err)
    pass_quad = rel2 <= rel_tol_quad
    pass_quart = rel4 <= rel_tol_quart
    # Quartic must not be worse than quadratic at small δ, up to roundoff.
    quart_helps = rel4 <= rel2 + 1e-12
    out.update(
        {
            "measurement": got,
            "relative_gap_quadratic": rel2,
            "relative_gap_quartic": rel4,
            "channel_abs_err": channel_err,
            "channel_tol": chan_tol,
            "pass_quadratic": pass_quad,
            "pass_quartic": pass_quart,
            "pass_channels": pass_channels,
            "pass_off_cycle": off_ok,
            "quartic_closer_than_quadratic": quart_helps,
            "pass_small_delta": bool(
                pass_quad and pass_quart and pass_channels and off_ok
            ),
            "stamp": "SMALL-HOLONOMY REGIME",
            "rel_tol_quad": rel_tol_quad,
            "rel_tol_quart": rel_tol_quart,
        }
    )
    return out


def prediction_measurement_test(
    c: Sequence[int],
    w: Sequence[float],
    delta: float,
    *,
    rel_tol: float = 0.05,
) -> dict:
    """Heavy prediction → measurement on the local law. Scale-rate stays OPEN."""
    test = heavy_one_cycle_test(c, w, delta, rel_tol_quad=rel_tol)
    return {
        "delta": test["delta"],
        "prediction": test["one_minus_rho2"],
        "prediction_quartic": test["one_minus_rho4"],
        "measurement": test.get("measurement"),
        "relative_gap": test.get("relative_gap_quadratic"),
        "relative_gap_quartic": test.get("relative_gap_quartic"),
        "pass_small_delta": test.get("pass_small_delta", False),
        "stamp": test["stamp"],
        "in_small_holonomy_regime": test["in_small_holonomy_regime"],
        "rel_tol": rel_tol,
        "boxed": test["boxed_quadratic"],
        "scale_rate": "OPEN",
        "off_cycle_zero": test.get("pass_off_cycle"),
    }
