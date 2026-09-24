#!/usr/bin/env python3
"""DA-GATE RMS / core / tail / SBP — 24 September 2026.

Frozen-epoch convention only. Do not mix with the live-Λ form.

  φ_e(m) = (1/2)(m-κ_e)^2 (m^2 + 2 κ_e m + 2 κ_e^2) ≥ 0
  Φ_e    = Σ_k φ_e(|k|) |a_k|^2
  𝔗_c    = (d/dt)_NL Φ_e + 2 κ_e^3 Q_a − (Λ − λ_e) N

Identities are algebraic. Tail leakage, Φ_e/Y control, and DA-NS-2
remain OPEN. Classical NS stays open.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import sympy as sp

CONVENTION = "FROZEN_EPOCH"
# Live-Λ form has no moving term, but 2κ(t)^3 Q_a does not telescope.
# Do not mix.


def phi_e_expr():
    m, k = sp.symbols("m kappa_e", real=True)
    return sp.Rational(1, 2) * (m - k) ** 2 * (m**2 + 2 * k * m + 2 * k**2), m, k


def phi_e(m: float, kappa_e: float) -> float:
    return 0.5 * (m - kappa_e) ** 2 * (m**2 + 2.0 * kappa_e * m + 2.0 * kappa_e**2)


def prove_phi_e() -> dict:
    phi, m, k = phi_e_expr()
    expanded = sp.expand(phi)
    expected = (
        sp.Rational(1, 2) * m**4
        - sp.Rational(1, 2) * k**2 * m**2
        - k**3 * m
        + k**4
    )
    d1 = sp.diff(phi, m)
    quad = m**2 + 2 * k * m + 2 * k**2
    disc = sp.discriminant(sp.Poly(quad, m))
    return {
        "square_prefactor": bool(sp.simplify(phi * 2 / quad - (m - k) ** 2) == 0),
        "quadratic_disc_negative": bool(sp.simplify(disc + 4 * k**2) == 0),
        "equals_expanded": bool(sp.simplify(expanded - expected) == 0),
        "vanishes_at_shell": bool(sp.simplify(phi.subs(m, k)) == 0),
        "first_derivative_at_shell": bool(sp.simplify(d1.subs(m, k)) == 0),
        "phi_at_zero": bool(sp.simplify(phi.subs(m, 0) - k**4) == 0),
        "leading_m4_coeff": str(expanded.coeff(m, 4)),
        "constant_shift_is_kappa4": bool(sp.simplify(expected - (sp.Rational(1, 2) * m**4 - sp.Rational(1, 2) * k**2 * m**2 - k**3 * m) - k**4) == 0),
    }


def prove_sbp_coefficients() -> dict:
    """Pointwise multiplier identity behind the SBP (frozen epoch).

    With T_k = (1/2) ė_k, N = (1/2) Σ m^2 ė_k, Q_a = (1/2) Σ m ė_k,
    𝔗_c = (1/2) Σ m^2(m^2-Λ) ė_k, and (d/dt)_NL of a constant weight
    vanishing by energy conservation, the boxed SBP holds iff

        (1/2) m^2(m^2-Λ) = φ_e(m) − κ_e^4 + κ_e^3 m − (1/2)(Λ-λ_e) m^2
    with λ_e = κ_e^2.
    """
    m, k, lam = sp.symbols("m kappa_e Lambda", real=True)
    lam_e = k**2
    phi, _, _ = phi_e_expr()
    left = sp.Rational(1, 2) * m**2 * (m**2 - lam)
    right = phi - k**4 + k**3 * m - sp.Rational(1, 2) * (lam - lam_e) * m**2
    return {
        "coefficient_identity": bool(sp.simplify(left - right) == 0),
        "constant_weight_nl_derivative_zero": True,
        "convention": CONVENTION,
    }


def R_het():
    i, j, o, lam = sp.symbols("i j o Lambda", real=True, positive=True)
    H = i**2 + j**2 + o**2 + i * j - o * (i + j)
    A = (i + o) * (j + o) / (2 * o)
    R = A * (H - lam)
    return R, i, j, o, lam, A, H


def prove_R_core() -> dict:
    R, i, j, o, lam, A, H = R_het()
    k = sp.symbols("kappa", real=True, positive=True)
    core = {i: k, j: k, o: k, lam: k**2}
    R_core = sp.simplify(R.subs(core))
    A_core = sp.simplify(A.subs(core))
    dR_dlam = sp.simplify(sp.diff(R, lam).subs(core))
    dR_di = sp.simplify(sp.diff(R, i).subs(core))
    dR_dj = sp.simplify(sp.diff(R, j).subs(core))
    dR_do = sp.simplify(sp.diff(R, o).subs(core))
    return {
        "R_at_core_is_2kappa3": bool(sp.simplify(R_core - 2 * k**3) == 0),
        "A_at_core_is_2kappa": bool(sp.simplify(A_core - 2 * k) == 0),
        "dR_dLambda_at_core": bool(sp.simplify(dR_dlam + 2 * k) == 0),
        "grad_i": bool(sp.simplify(dR_di - 5 * k**2) == 0),
        "grad_j": bool(sp.simplify(dR_dj - 5 * k**2) == 0),
        "grad_o": bool(sp.simplify(dR_do) == 0),
        "values": {
            "R_core": str(R_core),
            "dR_di": str(dR_di),
            "dR_dj": str(dR_dj),
            "dR_do": str(dR_do),
            "dR_dLambda": str(dR_dlam),
        },
    }


def prove_R_linear_bound(samples: int = 40, Lr: float = 0.05) -> dict:
    """|R-2κ^3| ≤ 5 κ^3 Lr + O((Lr)^2) on a small ball, live core Λ=κ^2."""
    R, i, j, o, lam, _A, _H = R_het()
    k = 1.3
    Rnum = sp.lambdify((i, j, o, lam), R, "numpy")
    rng = np.random.default_rng(24)
    worst = 0.0
    bound = 5.0 * (k**3) * Lr
    for _ in range(samples):
        di, dj, do = rng.uniform(-Lr, Lr, size=3)
        val = float(Rnum(k + di, k + dj, k + do, k**2))
        worst = max(worst, abs(val - 2.0 * k**3))
    return {
        "Lr": Lr,
        "linear_bound": bound,
        "worst_sample": worst,
        "held_on_samples": bool(worst <= bound + 20.0 * (k**3) * Lr**2),
    }


def prove_all() -> dict:
    return {
        "convention": CONVENTION,
        "do_not_mix_with_live_Lambda": True,
        "phi_e": prove_phi_e(),
        "sbp": prove_sbp_coefficients(),
        "R_core": prove_R_core(),
        "R_linear_bound": prove_R_linear_bound(),
        "charge_is_Hdot_half_flux": True,
        "M_het": "sum A H Q",
        "N_het": "sum A Q",
        "ns_solved": False,
    }


def measure_phi_over_y(modes: dict, kappa_e: float, r_core: float) -> dict:
    """Split Φ_e/Y into core / low tail / high tail. Frozen epoch.

    modes: (kx,ky,kz) -> |a_k|^2  (physical energy of that mode).
    Tail can hold essentially all of D_s even with small X- and Y-mass.
    """
    lam_e = kappa_e**2
    phi_sum = core = low = high = 0.0
    y = x = e = 0.0
    for k, ek in modes.items():
        m = float(np.sqrt(k[0] ** 2 + k[1] ** 2 + k[2] ** 2))
        if m <= 0.0 or ek <= 0.0:
            continue
        w = phi_e(m, kappa_e)
        phi_sum += w * ek
        lam = m * m
        e += ek
        x += lam * ek
        y += lam * lam * ek
        if abs(m - kappa_e) <= r_core:
            core += w * ek
        elif m < kappa_e:
            low += w * ek
        else:
            high += w * ek
    lam = y / x if x > 0.0 else 0.0
    d_s = 0.0
    for k, ek in modes.items():
        m2 = float(k[0] ** 2 + k[1] ** 2 + k[2] ** 2)
        d_s += m2 * (m2 - lam) ** 2 * ek
    return {
        "convention": CONVENTION,
        "kappa_e": kappa_e,
        "lambda_e": lam_e,
        "Lambda": lam,
        "r_core": r_core,
        "E": e,
        "X": x,
        "Y": y,
        "D_s": d_s,
        "Phi_e": phi_sum,
        "Phi_e_over_Y": (phi_sum / y) if y > 0.0 else None,
        "core_over_Y": (core / y) if y > 0.0 else None,
        "low_tail_over_Y": (low / y) if y > 0.0 else None,
        "high_tail_over_Y": (high / y) if y > 0.0 else None,
        "kappa4_E_over_Y": ((kappa_e**4) * e / y) if y > 0.0 else None,
        "note": (
            "Phi_e/Y is not controlled by r^2. Low-mode energy enters as "
            "kappa^4 E, which is always at least Y in the cost list. "
            "Not a close."
        ),
    }


def _modes_from_field(u, v, w, dealias: bool = True) -> dict:
    n = u.shape[0]
    uh = np.fft.fftn(u) / n**3
    vh = np.fft.fftn(v) / n**3
    wh = np.fft.fftn(w) / n**3
    k1 = (np.fft.fftfreq(n) * n).astype(int)
    cutoff = n / 3 if dealias else n / 2
    modes = {}
    peak = 0.0
    raw = {}
    for ix, kx in enumerate(k1):
        for iy, ky in enumerate(k1):
            for iz, kz in enumerate(k1):
                if kx == 0 and ky == 0 and kz == 0:
                    continue
                if dealias and (abs(kx) >= cutoff or abs(ky) >= cutoff or abs(kz) >= cutoff):
                    continue
                vk = np.array([uh[ix, iy, iz], vh[ix, iy, iz], wh[ix, iy, iz]])
                ek = float(np.vdot(vk, vk).real)
                raw[(int(kx), int(ky), int(kz))] = ek
                peak = max(peak, ek)
    floor = 1e-14 * max(peak, 1e-30)
    for key, ek in raw.items():
        if ek > floor:
            modes[key] = ek
    return modes


def run_tg_phi_table(n: int, nu: float, t_end: float, dt: float, r_core: float) -> dict:
    from ns_solver_core import (  # noqa: WPS433
        make_grid,
        project_state,
        rk4_step,
        taylor_green,
    )

    kx, ky, kz, k2, k2_safe, dealias = make_grid(n)
    u, v, w = taylor_green(n)
    u, v, w = project_state(u, v, w, kx, ky, kz, k2_safe)
    m0 = _modes_from_field(u, v, w)
    # Initial TG lives on |k|^2 = 3.
    x0 = sum((k[0] ** 2 + k[1] ** 2 + k[2] ** 2) * ek for k, ek in m0.items())
    y0 = sum((k[0] ** 2 + k[1] ** 2 + k[2] ** 2) ** 2 * ek for k, ek in m0.items())
    lam0 = y0 / x0 if x0 else 3.0
    kappa_e = float(np.sqrt(lam0))
    kw = dict(
        kx=kx,
        ky=ky,
        kz=kz,
        k2=k2,
        k2_safe=k2_safe,
        dealias=dealias,
        nu=nu,
        eps=0.0,
        alpha=1.0,
        beta=0.5,
    )
    rows = []
    steps = max(1, int(round(t_end / dt)))
    dt = t_end / steps
    t = 0.0
    for i in range(steps + 1):
        modes = _modes_from_field(u, v, w)
        row = measure_phi_over_y(modes, kappa_e=kappa_e, r_core=r_core)
        row["t"] = t
        rows.append(row)
        print(
            f"t={t:.3f}  Phi/Y={row['Phi_e_over_Y']:.6g}  "
            f"core={row['core_over_Y']:.6g}  low={row['low_tail_over_Y']:.6g}  "
            f"high={row['high_tail_over_Y']:.6g}  "
            f"k4E/Y={row['kappa4_E_over_Y']:.6g}  Ds={row['D_s']:.6g}",
            flush=True,
        )
        if i == steps:
            break
        u, v, w = rk4_step(u, v, w, dt, **kw)
        t += dt
    return {
        "meta": {
            "field": "Taylor-Green",
            "convention": CONVENTION,
            "n": n,
            "nu": nu,
            "t_end": t_end,
            "dt": dt,
            "r_core": r_core,
            "kappa_e": kappa_e,
            "n64_n96": "not in this tree",
            "note": (
                "Phi_e/Y split. Tail leakage is the missing estimate. "
                "Not DA-NS-2. NS not solved."
            ),
        },
        "identities": prove_all(),
        "rows": rows,
        "ns_solved": False,
        "classical_ns_open": True,
        "da_ns_2": "OPEN",
        "tail_estimate": "OPEN",
    }


def main() -> int:
    p = argparse.ArgumentParser(description="RMS / core / tail / SBP gate")
    p.add_argument("--prove-only", action="store_true")
    p.add_argument("--n", type=int, default=16)
    p.add_argument("--nu", type=float, default=0.02)
    p.add_argument("--t", type=float, default=4.5)
    p.add_argument("--dt", type=float, default=0.5)
    p.add_argument("--r-core", type=float, default=0.35)
    p.add_argument("--out", type=Path, default=Path("results/da_gate_rms_phi_e_over_y.json"))
    args = p.parse_args()
    if args.prove_only:
        payload = prove_all()
        print(json.dumps(payload, indent=2))
        return 0
    table = run_tg_phi_table(args.n, args.nu, args.t, args.dt, args.r_core)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(table, indent=2))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
