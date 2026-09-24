"""Score the full-court press. Lemma A first. Not a close.

Lemma A, unit torus, m≥1, κ≥1:
    ½(m-κ)²(m²+2κm+2κ²) ≤ m²(m²-κ²)²
iff
    m²+2κm+2κ² ≤ 2m²(m+κ)².

P(m,κ)=2m²(m+κ)²-(m²+2κm+2κ²) satisfies
P(1,κ)=1+2κ≥0 and P'≥6m(1+2κ)+2κ(2κ-1)≥0.
So (A) sits. Therefore Φ_e ≤ W_{λ_e}=D_s+X(Λ-λ_e)².

Young L2 sits and is weaker than the sitting W identity.
L3 sharp is Φ_e ≤ D_s+X(Λ-λ_e)². No η.
RESET |Λ-λ_e|=c√Λ is a named chart, not a payment.
Lemma B / charge stay OPEN.

Unit-torus numbers. Not R³. Do not scale |k| below 1.
Does not overwrite stokes_moments.py.
Does not restore ★.
Does not seat DA-NS-2.
Does not start leftover 1.
Does not run Taylor–Green.
Does not mix Heavy scalene loops.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from centered_ledger import W_K, two_shell_moments  # noqa: E402
from sbp import phi_e  # noqa: E402

OUT = ROOT / "results" / "press.json"


def P(m: float, kappa: float) -> float:
    return 2.0 * m * m * (m + kappa) ** 2 - (m * m + 2.0 * kappa * m + 2.0 * kappa * kappa)


def P_prime(m: float, kappa: float) -> float:
    return 8.0 * m**3 + 12.0 * kappa * m * m + 4.0 * kappa * kappa * m - 2.0 * m - 2.0 * kappa


def P_prime_lower(m: float, kappa: float) -> float:
    return 6.0 * m * (1.0 + 2.0 * kappa) + 2.0 * kappa * (2.0 * kappa - 1.0)


def modal_ratio(m: float, kappa: float) -> float:
    """φ_e / (m²(m²-κ²)²) after cancelling (m-κ)², m≠κ."""
    return (m * m + 2.0 * kappa * m + 2.0 * kappa * kappa) / (
        2.0 * m * m * (m + kappa) ** 2
    )


def C_at_one(kappa: float) -> float:
    return (2.0 * kappa * kappa + 2.0 * kappa + 1.0) / (2.0 * (kappa + 1.0) ** 2)


def phi_vs_W_row(alpha: float, beta: float, e_a: float, e_b: float, ke: float) -> dict:
    ma = math.sqrt(alpha)
    mb = math.sqrt(beta)
    mom = two_shell_moments(alpha, beta, e_a, e_b)
    lam_e = ke * ke
    w = W_K(mom["X"], mom["Y"], mom["Z"], lam_e)
    phi = phi_e(ma, ke) * e_a + phi_e(mb, ke) * e_b
    return {
        "alpha": alpha,
        "beta": beta,
        "ke": ke,
        "Phi": phi,
        "W": w["W"],
        "Ds": w["Ds"],
        "W_ok": w["ok"],
        "Phi_le_W": phi <= w["W"] + 1e-9 * max(1.0, abs(w["W"])),
        "gap": w["W"] - phi,
    }


def record() -> dict:
    kappas = (1.0, 1.5, 2.0, 3.0, 8.0, 20.0)
    ms = (1.0, 1.2, math.sqrt(2.0), 2.0, 3.0, 5.0, 10.0)

    p_one_ok = all(abs(P(1.0, k) - (1.0 + 2.0 * k)) < 1e-12 for k in kappas)
    p_nonneg = True
    p_prime_ok = True
    ratio_le_one = True
    ratio_rows = []
    for k in kappas:
        for m in ms:
            p = P(m, k)
            pp = P_prime(m, k)
            low = P_prime_lower(m, k)
            p_nonneg = p_nonneg and p >= -1e-12
            p_prime_ok = p_prime_ok and pp + 1e-12 >= low and low >= -1e-12
            if abs(m - k) > 1e-12:
                r = modal_ratio(m, k)
                ratio_le_one = ratio_le_one and r <= 1.0 + 1e-12
                ratio_rows.append({"m": m, "kappa": k, "ratio": r, "C1": C_at_one(k)})

    # Finite-difference check of P' at a sample.
    k0, m0, eps = 3.0, 2.0, 1e-6
    fd = (P(m0 + eps, k0) - P(m0 - eps, k0)) / (2.0 * eps)
    fd_ok = abs(fd - P_prime(m0, k0)) < 1e-6

    # C_κ at m=1 → 1 as κ→∞, and C_κ < 1 for finite κ.
    c_rows = [{"kappa": k, "C": C_at_one(k)} for k in kappas]
    c_to_one = abs(C_at_one(200.0) - 1.0) < 0.01
    c_finite_lt_one = all(row["C"] < 1.0 for row in c_rows)
    # At m=κ the cancelled ratio is 5/(8κ²).
    shell_formula_ok = abs((5.0 / (8.0 * 9.0)) - (9.0 + 18.0 + 18.0) / (2.0 * 9.0 * 36.0)) < 1e-12
    at_shell = abs(modal_ratio(3.0 + 1e-8, 3.0) - 5.0 / (8.0 * 9.0)) < 1e-6

    # Off-torus kill: m=0.1, κ=0.5.
    off = P(0.1, 0.5)
    off_fails = off < 0.0
    zero_mode = abs(phi_e(0.0, 3.0) - 81.0) < 1e-12  # κ⁴, W-mode = 0

    # Two-shell Φ_e ≤ W on the torus.
    low = phi_vs_W_row(1.0, 16.0, 0.01, 1.0, 4.0)
    high = phi_vs_W_row(4.0, 10000.0, 1.0, 1.0e-6, 2.0)
    core = phi_vs_W_row(4.0, 5.0, 1.0, 1.0, math.sqrt(4.5))
    samples_ok = low["Phi_le_W"] and high["Phi_le_W"] and core["Phi_le_W"]

    # Sharp L3 vs Young L2.
    mom = two_shell_moments(1.0, 16.0, 0.01, 1.0)
    lam_e = 16.0
    w = W_K(mom["X"], mom["Y"], mom["Z"], lam_e)
    delta = mom["Lambda"] - lam_e
    eta = 1.0
    young = (1.0 + eta) * w["Ds"] + (1.0 + 1.0 / eta) * mom["X"] * delta * delta
    young_ok = w["W"] <= young + 1e-9
    young_weaker = young > w["W"] + 1e-9 * max(1.0, abs(w["W"]))
    w_is_exact = w["ok"] and abs(w["W"] - (w["Ds"] + mom["X"] * delta * delta)) < 1e-9

    # L4 numbers: Φ/Y ≤ Ds/Y + ζ².
    zeta2 = (delta * delta) / mom["Lambda"]
    phi_low = low["Phi"]
    l4 = phi_low / mom["Y"] <= w["Ds"] / mom["Y"] + zeta2 + 1e-9

    # Displacement vs BROAD scale: |ΔΛ|~√Λ gives ζ²=c²; BROAD match is Λ^{3/4}.
    # Record both as numbers, not a seating.
    lam = 16.0
    c = 0.5
    reset_abs = c * math.sqrt(lam)
    broad_match = lam**0.75
    reset_not_broad = abs(reset_abs - broad_match) > 1.0

    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "lemma_A_sits": bool(
            p_one_ok and p_nonneg and p_prime_ok and ratio_le_one and samples_ok
        ),
        "lemma_B_open": True,
        "identities": {
            "A": "m²+2κm+2κ² ≤ 2m²(m+κ)² on m≥1, κ≥1",
            "L1": "Φ_e ≤ W_{λ_e} on the unit torus",
            "sharp_L3": "Φ_e ≤ D_s + X(Λ-λ_e)²",
            "L2_young": "W ≤ (1+η)D_s + (1+η^{-1})X(Λ-λ_e)², weaker",
            "L4": "Φ_e/Y ≤ D_s/Y + ζ_e² in torus units",
        },
        "P_at_one_ok": p_one_ok,
        "P_nonneg": p_nonneg,
        "P_prime_lower_ok": p_prime_ok,
        "P_prime_fd_ok": fd_ok,
        "ratio_le_one": ratio_le_one,
        "C_to_one": c_to_one,
        "C_finite_lt_one": c_finite_lt_one,
        "C_rows": c_rows,
        "shell_formula_ok": shell_formula_ok,
        "at_shell_check": at_shell,
        "off_torus_fails": off_fails,
        "off_torus_P": off,
        "zero_mode_is_kappa4": zero_mode,
        "mean_zero_required": True,
        "unit_torus_only": True,
        "not_R3": True,
        "samples": {"low": low, "high": high, "core": core},
        "samples_Phi_le_W": samples_ok,
        "W_identity_ok": w_is_exact,
        "young_ok": young_ok,
        "young_weaker_than_W": young_weaker,
        "L4_ok": l4,
        "reset_abs_at_c": reset_abs,
        "broad_match_abs": broad_match,
        "reset_is_not_broad_scale": reset_not_broad,
        "reset_is_not_a_payment": True,
        "zeta_not_unique_dimensionless": True,
        "charge_different_bill": True,
        "Ds_cannot_pay_Da_narrow": True,
        "lemma_B_not_seated": True,
        "identity_is_not_a_payment": True,
        "da_ns2_is_not_a_theorem": True,
        "sits_as_useful_K": False,
        "sits_as_g4_death": False,
        "sits_as_da_ns2": False,
        "sits_as_jgc": False,
        "sits_as_bprim": False,
        "g4_stays_open": True,
        "do_not_invent_a_bridge": True,
        "do_not_run_taylor_green": True,
        "do_not_mix_heavy": True,
        "do_not_glue_to_leftover_1": True,
        "ratio_rows_head": ratio_rows[:6],
    }
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
