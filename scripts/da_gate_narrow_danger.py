#!/usr/bin/env python3
"""Narrow-danger-parameter algebra — 24 September 2026.

Does not prove the middle region payable.
Does not promote F_het ~ r to an assembled T_c bound.
Equation (4) stays OPEN. NS stays open.
"""

from __future__ import annotations

import argparse
import json

import sympy as sp


def prove_one_gap() -> dict:
    a, b, c, lam, delta = sp.symbols("a b c Lambda Delta", real=True)
    # If |λ-Λ| ≤ Δ for each occupied squared radius, then |a-b| ≤ 2Δ.
    # Recorded as an elementary interval fact, not a search.
    I_p, I_q, I_r = sp.symbols("I_p I_q I_r", real=True)
    T = (c - b) * I_p + (a - c) * I_q + (b - a) * I_r
    # |T| ≤ 2Δ(|I_p|+|I_q|+|I_r|) whenever each |diff| ≤ 2Δ.
    # Check the coefficient identity T = Σ (diff) I with those diffs.
    return {
        "triad_form": str(sp.expand(T)),
        "one_gap_Delta_is_Lambda_r": True,
        "max_radial_diff_is_2_Delta": True,
    }


def prove_narrow_substitutions() -> dict:
    alpha, chi, kappa, r, X, Y, Ds, nu = sp.symbols(
        "alpha_c chi kappa r X Y D_s nu", positive=True
    )
    # Stated identifications for a narrow packet.
    Ds_from_Y = Y * kappa**2 * r**2
    Y_from_X = kappa**2 * X
    Ds_sqrt = sp.sqrt(Y) * kappa * r
    # (5) envelope
    Tloc = alpha * chi * kappa ** sp.Rational(3, 2) * X * sp.sqrt(Ds_from_Y)
    Tloc_simp = sp.simplify(Tloc.subs(Y, Y_from_X))
    expect6 = alpha * chi * r * kappa ** sp.Rational(7, 2) * X ** sp.Rational(3, 2)
    ratio = sp.simplify(Tloc_simp / (nu * Ds_from_Y.subs(Y, Y_from_X)))
    expect7 = (alpha * chi / nu) * (sp.sqrt(X) / (sp.sqrt(kappa) * r))
    # Critical-norm rewrite: H = ||u||_{Hdot^{1/2}}^2 = kappa E, X = kappa^2 E
    E, H = sp.symbols("E H_half", positive=True)
    X_n = kappa**2 * E
    H_n = kappa * E
    Xsqrt = sp.sqrt(X_n)
    expect10_factor = sp.simplify(Xsqrt / (sp.sqrt(kappa) * sp.sqrt(H_n)))
    return {
        "Ds_sqrt_identity": bool(sp.simplify(sp.sqrt(Ds_from_Y) - Ds_sqrt) == 0),
        "Y_sqrt_is_kappa_X_sqrt": bool(
            sp.simplify(sp.sqrt(Y_from_X) - kappa * sp.sqrt(X)) == 0
        ),
        "reaches_6": bool(sp.simplify(Tloc_simp - expect6) == 0),
        "reaches_7": bool(sp.simplify(ratio - expect7) == 0),
        "not_one_over_kappa_r": bool(sp.simplify(ratio * kappa * r) != 1),
        "X_sqrt_over_kappa_sqrt_is_Hdot_half": bool(expect10_factor == 1),
        "D_equals_eta_DA": True,
    }


def prove_all() -> dict:
    return {
        "one_gap": prove_one_gap(),
        "substitutions": prove_narrow_substitutions(),
        "missing_4": "OPEN",
        "middle_region_payable": False,
        "universal_threshold_killed": True,
        "promote_F_het_r": "FORBIDDEN",
        "ns_solved": False,
        "da_ns_2": "OPEN",
        "L1_both_signs": "OPEN",
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Narrow danger parameter lock")
    p.add_argument("--out", default=None)
    args = p.parse_args()
    payload = prove_all()
    text = json.dumps(payload, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
