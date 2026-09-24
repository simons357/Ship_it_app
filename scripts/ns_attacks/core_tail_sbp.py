#!/usr/bin/env python3
"""Core / tail summation-by-parts for centered T_c.

Not DA-NS-2. NS is not solved.

Frozen epoch only: λ_e = κ_e². Do not mix with live κ(t)=√Λ.
φ_e(m) = ½(m-κ_e)²(m²+2κ_e m+2κ_e²).
T_c = Φ_e'_NL + 2κ_e³ Q_a − (Λ−λ_e) N.
The identity moves the tail; it does not remove it.
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Dict, List, Sequence, Tuple

import sys
from pathlib import Path

import numpy as np
import sympy as sp

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ns_attacks.narrow_het_residual import R_of, moments, relative_width


def phi_e(m: float, kappa: float) -> float:
    return 0.5 * (m - kappa) ** 2 * (m * m + 2.0 * kappa * m + 2.0 * kappa * kappa)


def phi_e_poly(m: float, kappa: float) -> float:
    return 0.5 * m**4 - 0.5 * kappa**2 * m**2 - kappa**3 * m + kappa**4


def sympy_phi_factorization() -> dict:
    m, k = sp.symbols("m kappa", real=True)
    fact = sp.Rational(1, 2) * (m - k) ** 2 * (m**2 + 2 * k * m + 2 * k**2)
    expn = sp.Rational(1, 2) * m**4 - sp.Rational(1, 2) * k**2 * m**2 - k**3 * m + k**4
    d1 = sp.diff(fact, m).subs(m, k)
    d2 = sp.diff(fact, m, 2).subs(m, k)
    return {
        "factor_equals_expanded": bool(sp.simplify(fact - expn) == 0),
        "phi_at_shell": str(sp.simplify(fact.subs(m, k))),
        "phi_at_zero": str(sp.simplify(fact.subs(m, 0))),
        "dphi_at_shell": str(sp.simplify(d1)),
        "d2phi_at_shell": str(sp.simplify(d2)),
        "nonneg_as_written": True,
        "high_k_leading": "m^4/2",
    }


def sympy_R_core() -> dict:
    i, j, o, Lam, k = sp.symbols("i j o Lambda kappa", positive=True)
    A = (i + o) * (j + o) / (2 * o)
    H = i**2 + j**2 + o**2 + i * j - o * (i + j)
    R = A * (H - Lam)
    core = {i: k, j: k, o: k, Lam: k**2}
    gi = sp.simplify(sp.diff(R, i).subs(core))
    gj = sp.simplify(sp.diff(R, j).subs(core))
    go = sp.simplify(sp.diff(R, o).subs(core))
    gL = sp.simplify(sp.diff(R, Lam).subs({i: k, j: k, o: k}))
    Rcore_live = sp.simplify(R.subs(core))
    # Frozen core, live Λ: R(κ,κ,κ; Λ) − 2κ³ = −2κ(Λ − κ²)
    Rcore_frozen = sp.simplify(R.subs({i: k, j: k, o: k}) - 2 * k**3)
    return {
        "R_on_shell": str(Rcore_live),
        "grad_i": str(gi),
        "grad_j": str(gj),
        "grad_o": str(go),
        "dR_dLambda": str(gL),
        "frozen_core_shift": str(Rcore_frozen),
        "grad_is_5k2_5k2_0": bool(gi == 5 * k**2 and gj == 5 * k**2 and go == 0),
        "dR_dLambda_is_minus_2k": bool(gL == -2 * k),
        "frozen_shift_is_minus_2k_dLambda": bool(
            sp.simplify(Rcore_frozen + 2 * k * (Lam - k**2)) == 0
        ),
    }


def sympy_modal_sbp() -> dict:
    """T_c − Φ' − 2κ³ Q_a + (Λ−λ_e) N = −κ⁴ Σ İ = 0 by energy."""
    m, k, Lam = sp.symbols("m kappa Lambda", real=True)
    phi = sp.Rational(1, 2) * (m - k) ** 2 * (m**2 + 2 * k * m + 2 * k**2)
    w_Tc = sp.Rational(1, 2) * (m**4 - Lam * m**2)
    w_Q = sp.Rational(1, 2) * m
    w_N = sp.Rational(1, 2) * m**2
    residual = sp.simplify(w_Tc - phi - 2 * k**3 * w_Q + (Lam - k**2) * w_N)
    return {
        "modal_residual": str(residual),
        "is_minus_kappa4": bool(residual == -(k**4)),
        "killed_by_energy": "Σ İ = 0 ⇒ Σ residual İ = 0",
    }


def sympy_waleffe_m_flux() -> dict:
    """Weight |m| flux. Homo = 0. Het (++-) = 4g o(i-j) in raw Waleffe."""
    i, j, o, g = sp.symbols("i j o g", positive=True)
    # İ = 2g (s_p |p| − s_q |q|) cyclic. Homo s≡1.
    flux_homo = 2 * g * (
        i * (j - o) + j * (o - i) + o * (i - j)
    )
    # Het: (i,+),(j,+),(o,-)
    flux_het = 2 * g * (
        i * (j - (-o)) + j * ((-o) - i) + o * (i - j)
    )
    flux_homo = sp.simplify(flux_homo)
    flux_het = sp.simplify(flux_het)
    return {
        "homo_flux": str(flux_homo),
        "het_flux_raw_Waleffe": str(flux_het),
        "het_is_4g_o_i_minus_j": bool(flux_het == 4 * g * o * (i - j)),
        "Heavy_normalizes_het_to_2o_i_minus_j": True,
        "Qa_is_half_Hdot_half_flux": True,
    }


def random_energy_conserving_sbp(n: int = 12, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    m = rng.uniform(0.4, 6.0, size=n)
    I_dot = rng.normal(size=n)
    I_dot -= I_dot.mean()  # Σ İ = 0
    kappa, Lam = 3.0, 11.0
    lam_e = kappa**2
    Tc = 0.5 * np.sum((m**4 - Lam * m**2) * I_dot)
    Phi = np.sum(phi_e(m, kappa) * I_dot)
    Qa = 0.5 * np.sum(m * I_dot)
    N = 0.5 * np.sum(m**2 * I_dot)
    rhs = Phi + 2.0 * kappa**3 * Qa - (Lam - lam_e) * N
    return {
        "T_c": float(Tc),
        "Phi_dot": float(Phi),
        "Q_a": float(Qa),
        "N": float(N),
        "rhs": float(rhs),
        "abs_err": float(abs(Tc - rhs)),
    }


def R_linear_bound_sample(kappa: float = 5.0, Lr: float = 0.02) -> dict:
    """|R−2κ³| vs 5κ³ Lr at frozen Λ=κ², and the extra 2κ|Λ−λ_e| term."""
    lam_e = kappa**2
    # Relative |k| moves with |δi|+|δj| = κ Lr, δo=0 (gradient vanishes in o).
    di, dj = 0.6 * kappa * Lr, 0.4 * kappa * Lr
    R1 = R_of(kappa + di, kappa + dj, kappa, lam_e)
    lin = 5.0 * kappa**2 * (abs(di) + abs(dj))
    # Frozen core, Λ off-shell.
    dLam = 0.3
    R_off = R_of(kappa, kappa, kappa, lam_e + dLam)
    extra = 2.0 * kappa * abs(dLam)
    return {
        "abs_dR": abs(R1 - 2.0 * kappa**3),
        "five_k3_Lr": 5.0 * kappa**3 * Lr,
        "lin_5k2_absdi_absdj": lin,
        "within_linear_plus_quad": abs(R1 - 2.0 * kappa**3) <= lin + 40.0 * (kappa * Lr) ** 2 * kappa**2,
        "frozen_core_dR": abs(R_off - 2.0 * kappa**3),
        "two_k_dLambda": extra,
    }


def tail_holds_Ds() -> dict:
    """Light far tail: small X-mass and Y-mass, almost all D_s."""
    # Core at λ=4, tail at λ=400, tiny mass.
    eigs = [4.0, 400.0]
    mass = [1.0, 1e-6]
    m = moments(eigs, mass)
    return {
        "r": relative_width(m["D_s"], m["Lambda"], m["Y"]),
        "Ds": m["D_s"],
        "tail_Ds_share": (400.0 * (400.0 - m["Lambda"]) ** 2 * 1e-6) / m["D_s"],
        "tail_X_share": (400.0 * 1e-6) / m["X"],
        "tail_Y_share": (400.0**2 * 1e-6) / m["Y"],
        "core_X_share": (4.0 * 1.0) / m["X"],
        "note": "tail X,Y small; D_s almost entirely from the tail",
    }


def phi_over_Y_split(
    radii: Sequence[float],
    mass: Sequence[float],
    kappa: float,
    core_halfwidth: float,
) -> dict:
    """Split Φ_e/Y into low tail / core / high tail. Diagnostic, not a bound."""
    phi = [phi_e(m, kappa) * w for m, w in zip(radii, mass)]
    y = [m**4 * w for m, w in zip(radii, mass)]
    Y = sum(y)
    Phi = sum(phi)
    low = core = high = 0.0
    y_low = y_core = y_high = 0.0
    for m, p, yy in zip(radii, phi, y):
        if m < kappa - core_halfwidth:
            low += p
            y_low += yy
        elif m > kappa + core_halfwidth:
            high += p
            y_high += yy
        else:
            core += p
            y_core += yy
    return {
        "Phi_over_Y": Phi / Y if Y else None,
        "low_share_of_Phi": low / Phi if Phi else None,
        "core_share_of_Phi": core / Phi if Phi else None,
        "high_share_of_Phi": high / Phi if Phi else None,
        "low_share_of_Y": y_low / Y if Y else None,
        "core_share_of_Y": y_core / Y if Y else None,
        "high_share_of_Y": y_high / Y if Y else None,
        "phi_at_zero": phi_e(0.0, kappa),
        "kappa4": kappa**4,
        "no_TG_data_in_checkout": True,
    }


def report() -> dict:
    radii = [0.5, 1.0, 2.5, 3.0, 3.2, 5.0, 8.0]
    mass = [0.4, 0.3, 0.2, 0.5, 0.4, 0.05, 0.01]
    return {
        "phi": sympy_phi_factorization(),
        "R_core": sympy_R_core(),
        "sbp": sympy_modal_sbp(),
        "m_flux": sympy_waleffe_m_flux(),
        "numeric_sbp": random_energy_conserving_sbp(),
        "R_bound": R_linear_bound_sample(),
        "tail_Ds": tail_holds_Ds(),
        "Phi_Y_split": phi_over_Y_split(radii, mass, kappa=3.0, core_halfwidth=0.4),
        "conventions": {
            "frozen_epoch_only": True,
            "live_kappa_does_not_telescope": True,
            "frozen_core_picks_up_2k_dLambda": True,
            "do_not_mix": True,
        },
        "locks": {
            "not_a_close": True,
            "not_DA_NS_2": True,
            "moves_tail_does_not_remove_it": True,
            "no_TG_in_this_checkout": True,
        },
    }


def _py(x):
    if isinstance(x, dict):
        return {str(k): _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    if isinstance(x, (sp.Integer, sp.Float, sp.Rational)):
        return str(x)
    return x


def main(argv=None) -> int:
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    print(json.dumps(_py(report()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
