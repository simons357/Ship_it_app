"""Score the incoming centered ledger. Not a close.

Locks the two-shell product against the sitting gap
formula, shows α+β=Λ is empty on two positive shells,
locks |k_⊥|² and W_K, and refuses DA-NS-2 as a theorem.

Does not overwrite stokes_moments.py.
Does not restore ★.
Does not seat B★.
Does not start leftover 1.
Does not adopt SAG Γ_star=1 or JGC as seated.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from centered_barycenter import two_triad_strike  # noqa: E402

OUT = ROOT / "results" / "centered_ledger.json"


def two_shell_moments(alpha: float, beta: float, e_a: float, e_b: float) -> dict:
    x = alpha * e_a + beta * e_b
    y = (alpha**2) * e_a + (beta**2) * e_b
    z = (alpha**3) * e_a + (beta**3) * e_b
    e = e_a + e_b
    lam = y / x
    d_s = z - lam * y
    gap_ds = alpha * beta * (alpha - beta) ** 2 * e_a * e_b / x
    return {
        "X": x,
        "Y": y,
        "Z": z,
        "E": e,
        "Lambda": lam,
        "Ds": d_s,
        "Ds_gap": gap_ds,
        "alpha_plus_beta_minus_Lambda": alpha + beta - lam,
        "abE_over_X": alpha * beta * e / x,
    }


def two_shell_product(alpha: float, beta: float, e_a: float, e_b: float, t_alpha: float) -> dict:
    """T_c = (α-β)(α+β-Λ) T_α  and  T_c = (α-β)(αβ E/X) T_α."""
    m = two_shell_moments(alpha, beta, e_a, e_b)
    t_c_product = (alpha - beta) * m["alpha_plus_beta_minus_Lambda"] * t_alpha
    t_c_gap = (alpha - beta) * m["abE_over_X"] * t_alpha
    return {
        **m,
        "T_alpha": t_alpha,
        "T_c_product": t_c_product,
        "T_c_gap": t_c_gap,
        "product_matches_gap": abs(t_c_product - t_c_gap) < 1e-12 * max(1.0, abs(t_c_gap)),
    }


def k_perp2(alpha: float, beta: float) -> float:
    """|k_⊥|² = β(1-β/(4α)) for equal-input |p|²=|q|²=α, |k|²=β."""
    return beta * (1.0 - beta / (4.0 * alpha))


def W_K(x: float, y: float, z: float, k: float) -> dict:
    lam = y / x
    d_s = z - lam * y
    w = d_s + x * (lam - k) ** 2
    w_expand = z - 2.0 * k * y + (k**2) * x
    return {
        "Lambda": lam,
        "Ds": d_s,
        "W": w,
        "W_expand": w_expand,
        "ok": abs(w - w_expand) < 1e-12 * max(1.0, abs(w_expand)),
        "nonneg": w >= -1e-12,
    }


def unequal_defect(a: float, b: float, c: float, lam: float, tau_p: float, tau_q: float) -> dict:
    """T_c = [f(a)-f(c)] τ_p + [f(b)-f(c)] τ_q  with f(λ)=λ(λ-Λ)."""

    def f(lam_i: float) -> float:
        return lam_i * (lam_i - lam)

    tau_k = -tau_p - tau_q
    t_direct = f(a) * tau_p + f(b) * tau_q + f(c) * tau_k
    t_defect = (f(a) - f(c)) * tau_p + (f(b) - f(c)) * tau_q
    t_fact = (a - c) * (a + c - lam) * tau_p + (b - c) * (b + c - lam) * tau_q
    return {
        "T_direct": t_direct,
        "T_defect": t_defect,
        "T_fact": t_fact,
        "ok": abs(t_direct - t_defect) < 1e-12 * max(1.0, abs(t_direct))
        and abs(t_direct - t_fact) < 1e-12 * max(1.0, abs(t_direct)),
    }


def record() -> dict:
    rows = []
    for alpha, beta, e_a, e_b, t_a in (
        (2.0, 4.0, 1.0, 1.0, 0.3),
        (1.0, 5.0, 0.4, 0.7, -1.2),
        (3.0, 12.0, 2.0, 0.5, 0.8),
    ):
        rows.append(two_shell_product(alpha, beta, e_a, e_b, t_a))

    two_shell_never_centered = all(
        r["alpha_plus_beta_minus_Lambda"] > 1e-12 for r in rows
    )
    # Λ is a convex combination of α,β, so Λ ≤ max(α,β) < α+β.
    convex_gap = all(
        r["Lambda"] <= max(2.0, 4.0, 1.0, 5.0, 3.0, 12.0) + 1e-12 for r in rows
    )
    # tighter: Λ between the two eigenvalues
    between = True
    for alpha, beta, e_a, e_b, _ in (
        (2.0, 4.0, 1.0, 1.0, 0.3),
        (1.0, 5.0, 0.4, 0.7, -1.2),
        (3.0, 12.0, 2.0, 0.5, 0.8),
    ):
        m = two_shell_moments(alpha, beta, e_a, e_b)
        lo, hi = min(alpha, beta), max(alpha, beta)
        between = between and (lo - 1e-12 <= m["Lambda"] <= hi + 1e-12)

    flat = k_perp2(1.0, 4.0)
    perp_ok = abs(k_perp2(2.0, 4.0) - 4.0 * (1.0 - 4.0 / 8.0)) < 1e-15

    w = W_K(3.0, 8.0, 30.0, 1.5)
    uneq = unequal_defect(1.0, 4.0, 2.0, 2.2, 0.4, -0.15)
    strike = two_triad_strike()

    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "bstar_not_seated": True,
        "da_ns2_is_not_a_theorem": True,
        "identities": {
            "two_shell_product": "T_c = (α-β)(α+β-Λ) T_α = (α-β)(αβ E/X) T_α",
            "k_perp2": "|k_⊥|² = β(1-β/(4α))",
            "W_K": "W_K = D_s + X(Λ-K)² = Z - 2KY + K²X",
            "unequal_defect": "T_c = [f(a)-f(c)]τ_p + [f(b)-f(c)]τ_q",
        },
        "two_shell": rows,
        "product_matches_gap": all(r["product_matches_gap"] for r in rows),
        "two_shell_centered_zero_empty": bool(two_shell_never_centered and between and convex_gap),
        "flat_kills_perp": abs(flat) < 1e-15,
        "k_perp2_ok": bool(perp_ok),
        "W_K_ok": bool(w["ok"] and w["nonneg"]),
        "unequal_defect_ok": bool(uneq["ok"]),
        "charge_only_dead": bool(
            abs(strike["Q_sum"]) < 1e-12 and strike["T_sum"] > 0.0
        ),
        "sits_as_useful_K": False,
        "sits_as_g4_death": False,
        "sits_as_da_ns2": False,
        "sits_as_sag_gamma": False,
        "sits_as_jgc": False,
        "g4_stays_open": True,
        "paste_truncated_at_17": True,
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
