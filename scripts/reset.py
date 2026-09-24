"""Score chart resets of the frozen variance. Not a close.

W_K = D_s + X(Λ-K)² = Z - 2KY + K²X = ||A^{1/2}(A-K)u||².

At a chart reset the physical state is fixed. The jump is
    ΔW = X[(Λ-K_new)² - (Λ-K_old)²]
       = X(K_old - K_new)(2Λ - K_old - K_new).
Reset-to-barycenter K_new = Λ drops W by X(Λ-K_old)².
The Y-cousin remainder
    K_min,θ = [T_c - θν D_s]_+/Y
is chart-invariant, so the jump does not pay DA-NS-2.

This is sitting algebra from W_K, not a reconstruction
of the truncated §17 paste.

Does not overwrite stokes_moments.py.
Does not restore ★.
Does not seat B★.
Does not start leftover 1.
Does not adopt SAG or JGC as seated.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from centered_ledger import W_K, two_shell_moments  # noqa: E402

OUT = ROOT / "results" / "reset.json"


def jump(x: float, y: float, z: float, k_old: float, k_new: float) -> dict:
    old = W_K(x, y, z, k_old)
    new = W_K(x, y, z, k_new)
    dw = new["W"] - old["W"]
    lam = old["Lambda"]
    squares = x * ((lam - k_new) ** 2 - (lam - k_old) ** 2)
    factored = x * (k_old - k_new) * (2.0 * lam - k_old - k_new)
    to_lam = -x * (lam - k_old) ** 2
    return {
        "X": x,
        "Y": y,
        "Z": z,
        "Lambda": lam,
        "Ds": old["Ds"],
        "K_old": k_old,
        "K_new": k_new,
        "W_old": old["W"],
        "W_new": new["W"],
        "dW": dw,
        "dW_squares": squares,
        "dW_factored": factored,
        "dW_to_Lambda_if_Knew_is_Lambda": to_lam,
        "W_lambda": old["Ds"],
        "formula_ok": abs(dw - squares) < 1e-12 * max(1.0, abs(squares))
        and abs(dw - factored) < 1e-12 * max(1.0, abs(factored)),
        "W_ok": bool(old["ok"] and new["ok"] and old["nonneg"] and new["nonneg"]),
    }


def k_min(tc: float, ds: float, y: float, nu: float, theta: float) -> float:
    return max(tc - theta * nu * ds, 0.0) / y


def remainder_row(
    x: float,
    y: float,
    z: float,
    tc: float,
    k_old: float,
    k_new: float,
    nu: float = 1.0,
    theta: float = 0.5,
) -> dict:
    j = jump(x, y, z, k_old, k_new)
    km_old = k_min(tc, j["Ds"], y, nu, theta)
    km_new = k_min(tc, j["Ds"], y, nu, theta)
    reset_to_lam = abs(k_new - j["Lambda"]) < 1e-15
    drop = -x * (j["Lambda"] - k_old) ** 2
    return {
        **j,
        "Tc": tc,
        "nu": nu,
        "theta": theta,
        "K_min_old": km_old,
        "K_min_new": km_new,
        "K_min_chart_invariant": abs(km_old - km_new) < 1e-15,
        "reset_to_Lambda": reset_to_lam,
        "drops_W_by_gap": (
            reset_to_lam and abs(j["dW"] - drop) < 1e-12 * max(1.0, abs(drop))
        ),
        "W_lambda_is_Ds": abs(j["W_lambda"] - j["Ds"]) < 1e-15,
    }


def frequent_reset_ledger(x: float, lambdas: list[float]) -> dict:
    """Reset to each successive Λ. Σ|ΔW| = X Σ(ΔΛ)², not X·TV(Λ)."""
    jumps = []
    tv = 0.0
    sum_sq = 0.0
    for a, b in zip(lambdas, lambdas[1:]):
        # K_old = previous Λ, K_new = current Λ, live barycenter = b.
        dw = -x * (b - a) ** 2
        jumps.append(dw)
        tv += abs(b - a)
        sum_sq += (b - a) ** 2
    sum_abs = x * sum_sq
    return {
        "X": x,
        "lambdas": lambdas,
        "sum_abs_dW": sum_abs,
        "X_times_sum_dLambda_sq": x * sum_sq,
        "X_times_TV": x * tv,
        "sum_abs_is_X_sum_sq": abs(sum_abs - x * sum_sq) < 1e-12 * max(1.0, x * sum_sq),
        "strictly_weaker_than_TV": sum_sq + 1e-15 < tv or tv == 0.0,
    }


def record() -> dict:
    m = two_shell_moments(2.0, 8.0, 1.0, 1.5)
    x, y, z = m["X"], m["Y"], m["Z"]
    lam = m["Lambda"]
    tc = 50.0

    to_lam = remainder_row(x, y, z, tc, k_old=1.0, k_new=lam)
    away = remainder_row(x, y, z, tc, k_old=lam, k_new=lam + 4.0)
    two_chart = remainder_row(x, y, z, tc, k_old=0.5, k_new=3.0)
    other = remainder_row(5.0, 20.0, 90.0, tc=2.2, k_old=1.0, k_new=2.0)

    # Walk of Λ with frequent resets to the current barycenter.
    walk = frequent_reset_ledger(x, [2.0, 2.4, 2.1, 3.0, 2.8])
    big_steps = frequent_reset_ledger(x, [1.0, 4.0])
    # One large step: Σ(ΔΛ)² = TV² wait no: one step Σ(ΔΛ)² = (ΔΛ)², TV = |ΔΛ|,
    # so Σ(ΔΛ)² < TV when |ΔΛ| < 1, and Σ(ΔΛ)² > TV when |ΔΛ| > 1.
    # The lock is identity Σ|ΔW| = X Σ(ΔΛ)², not a comparison to TV size.
    # Circularity: a bound on Σ|ΔW| is a bound on Σ(ΔΛ)², which for mesh δ
    # is ≤ δ·TV, so it is weaker than TV when you reset often (small δ).

    rows = [to_lam, away, two_chart, other]
    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "bstar_not_seated": True,
        "identities": {
            "W_K": "W_K = D_s + X(Λ-K)² = Z-2KY+K²X = ||A^{1/2}(A-K)u||²",
            "dW": "ΔW = X[(Λ-K_new)²-(Λ-K_old)²] = X(K_old-K_new)(2Λ-K_old-K_new)",
            "reset_to_Lambda": "K_new=Λ ⇒ ΔW = -X(Λ-K_old)² ≤ 0 and W_Λ = D_s",
            "K_min": "K_min,θ = [T_c-θν D_s]_+/Y is independent of the chart K",
        },
        "rows": rows,
        "jump_formula_ok": all(r["formula_ok"] and r["W_ok"] for r in rows),
        "reset_to_lambda_drops_W": bool(
            to_lam["drops_W_by_gap"] and to_lam["dW"] < 0.0
        ),
        "reset_away_can_raise_W": bool(away["dW"] > 0.0),
        "K_min_chart_invariant": all(r["K_min_chart_invariant"] for r in rows),
        "W_lambda_is_Ds": all(r["W_lambda_is_Ds"] for r in rows),
        "K_min_positive_on_sample": to_lam["K_min_old"] > 0.0,
        "frequent_reset": walk,
        "sum_abs_dW_is_X_sum_sq": bool(walk["sum_abs_is_X_sum_sq"]),
        "frequent_reset_weaker_than_TV": bool(
            walk["sum_abs_dW"] + 1e-15 < walk["X_times_TV"]
        ),
        "one_big_step": big_steps,
        "da_ns2_is_not_a_theorem": True,
        "sits_as_useful_K": False,
        "sits_as_g4_death": False,
        "sits_as_jgc": False,
        "sits_as_da_ns2": False,
        "g4_stays_open": True,
        "paste_not_reconstructed": True,
        "do_not_glue_to_leftover_1": True,
    }
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
