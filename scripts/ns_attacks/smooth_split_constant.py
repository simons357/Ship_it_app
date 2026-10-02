#!/usr/bin/env python3
"""Checks for the 2 Oct 2026 smooth-split centered-constant derivation.

The written argument is the reviewable proof of existence of a finite C in

    |T_c| ≤ (7 + 6 M_mult) C_s g √(Y D_s)

for real mean-zero divergence-free finite Fourier fields on the fixed
2π-torus (normalized Haar). This module does not prove that estimate.
It checks the algebraic identities, coefficient bounds, the six-mode
family, and the degenerate D_s=0 case.

Honesty lock
------------
Instantaneous estimate only. ★ NOT proved. NS NOT solved. Kill lane LIVE.
The cutoff-uniform ∫ g² dt budget is OPEN. Global NSE regularity is NOT
established. No optimized decimal C is claimed.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Dict, Tuple

import numpy as np

from ns_attacks.centered_flux_q3 import (
    Field,
    Mode,
    flux_moments,
    grad_L3,
    k_norm2,
    moments,
    near_shell_triad,
    scale_field,
)

NPField = Dict[Mode, np.ndarray]


def field_to_numpy(field: Field) -> NPField:
    return {k: np.array([c.to_complex() for c in v], dtype=np.complex128) for k, v in field.items()}


def enforce_reality_np(field: NPField) -> NPField:
    out: NPField = {}
    for k, v in field.items():
        if k == (0, 0, 0):
            continue
        mk = (-k[0], -k[1], -k[2])
        out[k] = np.asarray(v, dtype=np.complex128)
        out[mk] = np.conjugate(out[k])
    return out


def moments_np(field: NPField) -> Dict[str, float]:
    E = X = Y = Z = 0.0
    for k, v in field.items():
        lam = float(k_norm2(k))
        if lam == 0:
            continue
        amp2 = float(np.vdot(v, v).real)
        E += amp2
        X += lam * amp2
        Y += lam * lam * amp2
        Z += lam * lam * lam * amp2
    Lam = Y / X
    return {"E": E, "X": X, "Y": Y, "Z": Z, "Lambda": Lam, "Ds": Z - Lam * Y}


def advect(a: NPField, b: NPField) -> NPField:
    """((a·∇)b)_m = Σ_{p+q=m} i (q·a_p) b_q."""
    out: NPField = {}
    for p, ap in a.items():
        for q, bq in b.items():
            m = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if m == (0, 0, 0):
                continue
            coeff = 1j * np.dot(np.array(q, dtype=np.float64), ap)
            out[m] = out.get(m, np.zeros(3, dtype=np.complex128)) + coeff * bq
    return out


def scale_modes(field: NPField, weight) -> NPField:
    out: NPField = {}
    for k, v in field.items():
        out[k] = weight(k) * v
    return out


def inner(a: NPField, b: NPField) -> float:
    """Parseval ⟨a,b⟩ = Σ a_k · conj(b_k), real part."""
    keys = set(a) | set(b)
    acc = 0.0 + 0.0j
    zero = np.zeros(3, dtype=np.complex128)
    for k in keys:
        acc += np.dot(a.get(k, zero), np.conjugate(b.get(k, zero)))
    return float(acc.real)


def flux_np(field: NPField) -> Dict[str, float]:
    m = moments_np(field)
    Lam = m["Lambda"]
    B = advect(field, field)
    # Leray: not needed against divergence-free test fields.
    Au = scale_modes(field, lambda k: float(k_norm2(k)))
    A2u = scale_modes(field, lambda k: float(k_norm2(k)) ** 2)
    N = -inner(Au, B)
    M = -inner(A2u, B)
    return {**m, "N": N, "M": M, "Tc": M - Lam * N}


def product_rule_rhs(field: NPField, Lam: float) -> float:
    """−⟨w,(Au·∇)u⟩ + 2 Σ_j ⟨w,(∂_j u·∇)∂_j u⟩."""
    w = scale_modes(field, lambda k: float(k_norm2(k)) - Lam)
    Au = scale_modes(field, lambda k: float(k_norm2(k)))
    first = -inner(w, advect(Au, field))
    second = 0.0
    for j in range(3):
        dj_u = scale_modes(field, lambda k, j=j: 1j * k[j])
        second += inner(w, advect(dj_u, dj_u))
    return first + 2.0 * second


def F_trilinear(a: NPField, b: NPField, c: NPField) -> float:
    """F(a,b,c) = −Σ_{i,j,ℓ} ∫ (∂_j a_i)(∂_j b_ℓ)(∂_ℓ c_i) dμ."""
    acc = 0.0 + 0.0j
    keys_a = list(a)
    keys_b = list(b)
    keys_c = list(c)
    for p in keys_a:
        ap = a[p]
        for q in keys_b:
            bq = b[q]
            r = (-p[0] - q[0], -p[1] - q[1], -p[2] - q[2])
            cr = c.get(r)
            if cr is None:
                continue
            # ∫ (∂_j a_i)(∂_j b_ℓ)(∂_ℓ c_i) = Σ (i p_j a_i(p))(i q_j b_ℓ(q))(i r_ℓ c_i(r))
            # i³ = −i
            for i in range(3):
                for j in range(3):
                    for ell in range(3):
                        acc += (
                            (-1j)
                            * (p[j] * ap[i])
                            * (q[j] * bq[ell])
                            * (r[ell] * cr[i])
                        )
    return float((-acc).real)


def chi_cutoff(s: float) -> float:
    """C¹ cutoff: 1 on [0,1/4], 0 on [1/2,∞). Support only; M_mult uses C^∞."""
    if s <= 0.25:
        return 1.0
    if s >= 0.5:
        return 0.0
    t = 4.0 * s - 1.0
    return 1.0 - t * t * (3.0 - 2.0 * t)


def split_field(field: NPField, Lam: float) -> Tuple[NPField, NPField]:
    v: NPField = {}
    h: NPField = {}
    for k, vec in field.items():
        s = float(k_norm2(k)) / Lam
        c = chi_cutoff(s)
        v[k] = c * vec
        h[k] = (1.0 - c) * vec
    return v, h


def split_coefficient_bounds(field: NPField) -> Dict[str, float]:
    m = moments_np(field)
    Lam = m["Lambda"]
    Ds = m["Ds"]
    Y = m["Y"]
    v, h = split_field(field, Lam)
    grad_v2 = 0.0
    h2 = 0.0
    Ah2 = 0.0
    grad_ALh2 = 0.0
    for k, vec in v.items():
        lam = float(k_norm2(k))
        amp2 = float(np.vdot(vec, vec).real)
        grad_v2 += lam * amp2
    for k, vec in h.items():
        lam = float(k_norm2(k))
        amp2 = float(np.vdot(vec, vec).real)
        h2 += amp2
        Ah2 += (lam * lam) * amp2
        grad_ALh2 += lam * (lam - Lam) ** 2 * amp2
    return {
        "Lambda": Lam,
        "Ds": Ds,
        "Y": Y,
        "Lambda_grad_v": Lam * math.sqrt(max(grad_v2, 0.0)),
        "two_sqrt_Ds": 2.0 * math.sqrt(max(Ds, 0.0)),
        "Lambda_h": Lam * math.sqrt(max(h2, 0.0)),
        "four_sqrt_Y": 4.0 * math.sqrt(max(Y, 0.0)),
        "Ah": math.sqrt(max(Ah2, 0.0)),
        "sqrt_Y": math.sqrt(max(Y, 0.0)),
        "grad_ALh": math.sqrt(max(grad_ALh2, 0.0)),
        "sqrt_Ds": math.sqrt(max(Ds, 0.0)),
    }


def bounds_hold(b: Dict[str, float], atol: float = 1e-9) -> bool:
    return (
        b["Lambda_grad_v"] <= b["two_sqrt_Ds"] + atol
        and b["Lambda_h"] <= b["four_sqrt_Y"] + atol
        and b["Ah"] <= b["sqrt_Y"] + atol
        and b["grad_ALh"] <= b["sqrt_Ds"] + atol
    )


def six_mode_family(j: int) -> NPField:
    """DA interacting six-mode family, integer j≥3."""
    if j < 3:
        raise ValueError("j must be >= 3")
    inv = j ** -0.5
    field: NPField = {
        (1, 0, 0): np.array([0.0, 1.0, 0.0], dtype=np.complex128),
        (j, j, 0): np.array([0.0, 0.0, inv], dtype=np.complex128),
        (j + 1, j, 0): np.array([0.0, 0.0, 1j * inv], dtype=np.complex128),
    }
    return enforce_reality_np(field)


def claimed_six_mode_N(j: int) -> float:
    return -2.0 * (2 * j + 1)


def spread_triad() -> Field:
    """Shells λ=1,9,16 so the smooth split is genuinely mixed."""
    from ns_attacks.centered_flux_q3 import C, I, ZERO, enforce_reality

    field: Field = {
        (1, 0, 0): (ZERO, C(1), ZERO),
        (3, 0, 0): (ZERO, ZERO, I),
        (4, 0, 0): (ZERO, ZERO, C(1)),
    }
    return enforce_reality(field)


def single_shell_field() -> Field:
    from ns_attacks.centered_flux_q3 import C, ZERO, enforce_reality

    return enforce_reality({(1, 0, 0): (ZERO, C(1), ZERO)})


def grad_Lp_np(field: NPField, p: float, n_grid: int = 32) -> float:
    N = int(n_grid)
    kx = np.fft.fftfreq(N) * N
    KX, KY, KZ = np.meshgrid(kx, kx, kx, indexing="ij")
    wave = [KX, KY, KZ]
    uhat = [np.zeros((N, N, N), dtype=np.complex128) for _ in range(3)]
    for (a, b, c), v in field.items():
        if max(abs(a), abs(b), abs(c)) >= N // 2:
            raise ValueError("mode exceeds grid Nyquist")
        uhat[0][a % N, b % N, c % N] = v[0]
        uhat[1][a % N, b % N, c % N] = v[1]
        uhat[2][a % N, b % N, c % N] = v[2]
    jac2 = np.zeros((N, N, N), dtype=np.float64)
    scale = float(N) ** 3
    for i in range(3):
        for j in range(3):
            phys = np.fft.ifftn(1j * wave[j] * uhat[i]) * scale
            jac2 += np.abs(phys) ** 2
    return float(np.mean(np.sqrt(jac2) ** p) ** (1.0 / p))


def probe_six_mode(j: int, n_grid: int | None = None) -> dict:
    field = six_mode_family(j)
    flux = flux_np(field)
    N = flux["N"]
    Lam = flux["Lambda"]
    Ds = flux["Ds"]
    Y = flux["Y"]
    E = flux["E"]
    Tc = flux["Tc"]
    grid = n_grid if n_grid is not None else max(32, 4 * (j + 2))
    g = grad_Lp_np(field, 3.0, n_grid=grid)
    denom = g * math.sqrt(max(Y * Ds, 0.0))
    rho = abs(Tc) / denom if denom > 0 else float("nan")
    rho_LN = abs(Lam * N) / denom if denom > 0 else float("nan")
    Rstar = (max(Tc, 0.0) ** 2) / (Ds * E * Y) if Ds > 0 else float("nan")
    spread = (Ds / (Lam * Y)) if (Lam * Y) > 0 else float("nan")
    return {
        "j": j,
        "N": N,
        "N_claimed": claimed_six_mode_N(j),
        "N_abs_err": abs(N - claimed_six_mode_N(j)),
        "Lambda": Lam,
        "Ds": Ds,
        "Y": Y,
        "E": E,
        "Tc": Tc,
        "g": g,
        "rho_q3Y": rho,
        "rho_Lambda_N": rho_LN,
        "Ds_over_Lambda_Y": spread,
        "R_star": Rstar,
        "Lambda_N_over_j": (Lam * N) / j,
    }


def check_product_rule(field: Field, atol: float = 1e-9) -> dict:
    flux = flux_moments(field)
    lhs = float(flux["Tc"] - flux["Lambda"] * flux["N"])
    npf = field_to_numpy(field)
    rhs = product_rule_rhs(npf, float(flux["Lambda"]))
    return {"lhs": lhs, "rhs": rhs, "abs_err": abs(lhs - rhs), "ok": abs(lhs - rhs) < atol}


def check_F_equals_N(field: Field, atol: float = 1e-8) -> dict:
    flux = flux_moments(field)
    npf = field_to_numpy(field)
    Fuuu = F_trilinear(npf, npf, npf)
    return {
        "N": float(flux["N"]),
        "F": Fuuu,
        "abs_err": abs(float(flux["N"]) - Fuuu),
        "ok": abs(float(flux["N"]) - Fuuu) < atol,
    }


def check_F_grouping(field: NPField, atol: float = 1e-8) -> dict:
    m = moments_np(field)
    v, h = split_field(field, m["Lambda"])
    Nu = F_trilinear(field, field, field)
    Nh = F_trilinear(h, h, h)
    grouped = (
        F_trilinear(v, field, field)
        + F_trilinear(h, v, field)
        + F_trilinear(h, h, v)
    )
    return {
        "N_minus_Nh": Nu - Nh,
        "grouped": grouped,
        "abs_err": abs((Nu - Nh) - grouped),
        "ok": abs((Nu - Nh) - grouped) < atol,
    }


def estimate_Mmult(n: int = 48, xi_max: float = 1.6) -> dict:
    """Numerical illustration that ∫|K| < ∞ for the cubic cutoff.

    Not the official C^∞ kernel and not an optimized M_mult.
    """
    dxi = 2.0 * xi_max / n
    xi = np.linspace(-xi_max, xi_max, n, endpoint=False)
    XI, YI, ZI = np.meshgrid(xi, xi, xi, indexing="ij")
    s = XI * XI + YI * YI + ZI * ZI
    phi = np.vectorize(chi_cutoff)(s)
    # K = (2π)^{-3} ∫ φ e^{ixξ} dξ ≈ (2π)^{-3} (n dxi)^3 ifftn(ifftshift φ)
    Kn = np.fft.ifftn(np.fft.ifftshift(phi)) * (n * dxi / (2.0 * math.pi)) ** 3
    dx = 2.0 * math.pi / (n * dxi)
    l1 = float(np.sum(np.abs(Kn)) * dx**3)
    return {
        "n": n,
        "xi_max": xi_max,
        "K_L1_estimate": l1,
        "Mmult_estimate": 1.0 + l1,
        "note": "cubic C¹ cutoff; illustration of finiteness only",
    }


def am_gm_log_Lambda(C: float, g: float, nu: float) -> float:
    """(log Λ)' ≤ C² g² / (2ν) if |T_c| ≤ C g √(Y D_s)."""
    return (C * C * g * g) / (2.0 * nu)


def F_X(Cs: float, g: float, Lam: float, nu: float) -> float:
    return 2.0 * max(Cs * g * math.sqrt(Lam) - nu * Lam, 0.0)


def run(n_grid: int = 32) -> dict:
    from fractions import Fraction

    near = near_shell_triad(Fraction(1, 8))
    near_eps1 = near_shell_triad(1)
    spread = spread_triad()
    product = check_product_rule(near)
    product_spread = check_product_rule(spread)
    F_check = check_F_equals_N(near)
    F_spread = check_F_equals_N(spread)
    grouping = check_F_grouping(field_to_numpy(spread))
    grouping_six = check_F_grouping(six_mode_family(4))

    split_near = split_coefficient_bounds(field_to_numpy(near_eps1))
    split_spread = split_coefficient_bounds(field_to_numpy(spread))
    split_six = split_coefficient_bounds(six_mode_family(5))

    shell = flux_moments(single_shell_field())
    six_rows = [probe_six_mode(j, n_grid=max(32, 4 * (j + 2))) for j in (3, 4, 5, 6, 8)]
    rho_LN = [abs(r["rho_Lambda_N"]) for r in six_rows]
    decreasing = all(rho_LN[i] >= rho_LN[i + 1] for i in range(len(rho_LN) - 1))

    from ns_attacks.centered_flux_q3 import probe_near_shell

    ns_row = probe_near_shell(Fraction(1, 8), n_grid=n_grid)

    summary = {
        "harness": "smooth_split_centered_constant",
        "date": "2026-10-02",
        "ns_solved": False,
        "lemma_star_proved": False,
        "global_regularity": False,
        "kill_lane": "LIVE",
        "claimed_estimate": "|T_c| ≤ (7+6 M_mult) C_s g √(Y D_s)",
        "claimed_Lambda_N": "|Λ N| ≤ (4+6 M_mult) C_s g √(Y D_s)",
        "status": "CLAIMED_existence_of_finite_C",
        "optimized_decimal_C": None,
        "identities": {
            "product_rule_near_shell": product,
            "product_rule_spread": product_spread,
            "F_equals_N_near": F_check,
            "F_equals_N_spread": F_spread,
            "F_grouping_spread": grouping,
            "F_grouping_six_j4": grouping_six,
        },
        "split_bounds": {
            "near_shell_eps1": {**split_near, "hold": bounds_hold(split_near)},
            "spread_triad": {**split_spread, "hold": bounds_hold(split_spread)},
            "six_mode_j5": {**split_six, "hold": bounds_hold(split_six)},
        },
        "degenerate_single_shell": {
            "Ds": str(shell["Ds"]),
            "N": str(shell["N"]),
            "Tc": str(shell["Tc"]),
        },
        "six_mode_rows": six_rows,
        "six_mode_Lambda_N_quotient_decreases": decreasing,
        "near_shell_rho_q3Y": ns_row.rho_q3Y,
        "witness_lower_bound_note": (
            "Earlier exact witness C>0.4 is a necessary lower bound. "
            "Near-shell ε=1/8 gives |T_c|/(g√(Y D_s))≈0.24; six-mode rows below."
        ),
        "Mmult_illustration": estimate_Mmult(),
        "budget": {
            "log_Lambda_prime": "(log Λ)' = 2(T_c−ν D_s)/Y ≤ C² g²/(2ν)  (if the estimate holds)",
            "F_X": "F_X=2(C_s g √Λ − ν Λ)_+ ; (log X)' ≤ F_X",
            "cutoff_uniform_integral": "OPEN",
        },
        "does_not_imply": [
            "Lemma★ / sup R_★ < ∞",
            "cutoff-uniform ∫ g² dt",
            "global NSE regularity",
            "Clay Statement B",
        ],
        "caution": (
            "Machine checks identities and witnesses. They do not replace the "
            "analytic argument and they do not close the time budget."
        ),
    }
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--n-grid", type=int, default=32)
    args = ap.parse_args()
    summary = run(n_grid=args.n_grid)
    print(json.dumps(summary, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2) + "\n")
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
