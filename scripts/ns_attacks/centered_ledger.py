#!/usr/bin/env python3
"""Centered-ledger algebra checks. Not DA-NS-2. NS is not solved."""

from __future__ import annotations

import argparse
import json


def f_weight(lam: float, Lambda: float) -> float:
    return lam * (lam - Lambda)


def two_shell_gap(alpha: float, beta: float, Lambda: float) -> float:
    """f(β) − f(α) = (β − α)(α + β − Λ)."""
    return (beta - alpha) * (alpha + beta - Lambda)


def kperp2(alpha: float, beta: float) -> float:
    return beta * (1.0 - beta / (4.0 * alpha))


def W_K(D_s: float, X: float, Lambda: float, K: float) -> float:
    return D_s + X * (Lambda - K) ** 2


def reset_dW(X: float, Lambda: float, K_old: float, K_new: float) -> float:
    return X * ((Lambda - K_new) ** 2 - (Lambda - K_old) ** 2)


def moments(eigs: list[float], mass: list[float]) -> dict:
    x = sum(a * m for a, m in zip(eigs, mass))
    y = sum(a * a * m for a, m in zip(eigs, mass))
    z = sum(a**3 * m for a, m in zip(eigs, mass))
    lam = y / x
    d_s = z - lam * y
    d_s_var = sum(a * (a - lam) ** 2 * m for a, m in zip(eigs, mass))
    return {"X": x, "Y": y, "Z": z, "Lambda": lam, "D_s": d_s, "D_s_var": d_s_var}


def W_K_modal(eigs: list[float], mass: list[float], K: float) -> float:
    """∑ λ(λ−K)² m = D_s + X(Λ−K)²."""
    return sum(a * (a - K) ** 2 * m for a, m in zip(eigs, mass))


def two_shell_zeros(alpha: float, Lambda: float) -> dict:
    """Three structural zeros of the two-shell product."""
    return {
        "gap": two_shell_gap(alpha, alpha, Lambda),
        "flat_kperp2": kperp2(alpha, 4.0 * alpha),
        "centered": two_shell_gap(alpha, Lambda - alpha, Lambda),
    }


def circle_tangent(rho, khat, x, y):
    """w = 2 ρ×(x×y) = 2σ(ρ×k̂) when x,y ∈ k⊥ and x×y = σ k̂."""
    cx = (
        x[1] * y[2] - x[2] * y[1],
        x[2] * y[0] - x[0] * y[2],
        x[0] * y[1] - x[1] * y[0],
    )
    w = (
        2.0 * (rho[1] * cx[2] - rho[2] * cx[1]),
        2.0 * (rho[2] * cx[0] - rho[0] * cx[2]),
        2.0 * (rho[0] * cx[1] - rho[1] * cx[0]),
    )
    sigma = cx[0] * khat[0] + cx[1] * khat[1] + cx[2] * khat[2]
    w_from_sigma = (
        2.0 * sigma * (rho[1] * khat[2] - rho[2] * khat[1]),
        2.0 * sigma * (rho[2] * khat[0] - rho[0] * khat[2]),
        2.0 * sigma * (rho[0] * khat[1] - rho[1] * khat[0]),
    )
    return {"w": w, "sigma": sigma, "w_from_sigma": w_from_sigma}


def moving_center(R_minus_2k3: list[float], A: list[float], Q: list[float],
                  Lambda: float, lam_e: float) -> dict:
    """T_c^het = 2κ_e³ Q_Γ + ρ^rad + ρ^mov, ρ^mov = −(Λ−λ_e)S_Γ."""
    Q_gamma = sum(Q)
    S = sum(a * q for a, q in zip(A, Q))
    rho_rad = sum(r * q for r, q in zip(R_minus_2k3, Q))
    rho_mov = -(Lambda - lam_e) * S
    return {"Q_Gamma": Q_gamma, "S_Gamma": S, "rho_rad": rho_rad, "rho_mov": rho_mov}


def report() -> dict:
    alpha, beta, lam = 5.0, 2.0, 3.0
    a, b, c = 5.0, 3.0, 2.0
    eigs = [1.0, 2.0, 5.0]
    mass = [0.4, 0.3, 0.2]
    m = moments(eigs, mass)
    k_old, k_new = 1.0, 4.0
    return {
        "two_shell": {
            "f_diff": f_weight(beta, lam) - f_weight(alpha, lam),
            "factored": two_shell_gap(alpha, beta, lam),
        },
        "kperp2": {
            "value": kperp2(6.0, 4.0),
            "flat": kperp2(1.0, 4.0),
        },
        "unequal": {
            "left": (f_weight(a, lam) - f_weight(c, lam), f_weight(b, lam) - f_weight(c, lam)),
            "right": ((a - c) * (a + c - lam), (b - c) * (b + c - lam)),
        },
        "W_K": {
            "from_def": W_K(m["D_s"], m["X"], m["Lambda"], m["Lambda"]),
            "D_s": m["D_s"],
            "D_s_var": m["D_s_var"],
            "reset": reset_dW(m["X"], m["Lambda"], k_old, k_new),
            "reset_expand": m["X"]
            * (k_old - k_new)
            * (2.0 * m["Lambda"] - k_old - k_new),
        },
        "zeros": two_shell_zeros(alpha, lam),
        "locks": {"not_a_close": True, "not_DA_NS_2": True},
    }


def _py(x):
    if isinstance(x, dict):
        return {str(k): _py(v) for k, v in x.items()}
    if isinstance(x, tuple):
        return [_py(v) for v in x]
    return x


def main(argv=None) -> int:
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    print(json.dumps(_py(report()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
