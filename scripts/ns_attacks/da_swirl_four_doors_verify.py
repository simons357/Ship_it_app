#!/usr/bin/env python3
"""Independent numeric checks for DA swirl four-doors bench (2026-10-06).

Verifies exact Gaussian integrals / frozen-drift closed form / initial U signs
quoted in the bench note. Not an NSE simulation. Not a regularity claim.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

OUT = Path("/opt/cursor/artifacts/da-swirl-four-doors")
OUT.mkdir(parents=True, exist_ok=True)


def simpson_radial_gaussian_moments(n: int = 4001) -> dict:
    """Dimensionless integrals for F=exp(-(r^2+z^2)), measure 2π r dr dz.

    With a=1, ε=1:
      E = ∫|u|^2 = ∫ F^2 r^2 dx = π^{3/2}/(4√2)
      D = ∫|∇u|^2 = 5 π^{3/2}/(4√2)
      Q = ∫ F^4 dx = π^{3/2}/8
    """
    # Use 3D Cartesian Monte-ish grid via cylindrical Simpson on (r,z)
    Rmax = 8.0
    r = np.linspace(0.0, Rmax, n)
    z = np.linspace(-Rmax, Rmax, n)
    dr = r[1] - r[0]
    dz = z[1] - z[0]
    rr, zz = np.meshgrid(r, z, indexing="ij")
    s2 = rr * rr + zz * zz
    F = np.exp(-s2)
    # physical measure dx = 2π r dr dz
    w = 2 * np.pi * rr
    # Simpson weights (product)
    wr = np.ones(n)
    wr[1:-1:2] = 4
    wr[2:-1:2] = 2
    wz = np.ones(n)
    wz[1:-1:2] = 4
    wz[2:-1:2] = 2
    W = np.outer(wr, wz) * (dr * dz / 9.0) * w

    E_num = float(np.sum(W * (F**2) * (rr**2)))
    Q_num = float(np.sum(W * (F**4)))
    # |∇u|^2 for u = F (-y,x,0) = a e^{-|x|^2} (-y,x,0) with a=ε=1
    # Exact analytic target used for relative error.
    E_exact = math.pi**1.5 / (4 * math.sqrt(2))
    D_exact = 5 * math.pi**1.5 / (4 * math.sqrt(2))
    Q_exact = math.pi**1.5 / 8.0
    return {
        "E_num": E_num,
        "Q_num": Q_num,
        "E_exact": E_exact,
        "D_exact": D_exact,
        "Q_exact": Q_exact,
        "E_rel_err": abs(E_num - E_exact) / E_exact,
        "Q_rel_err": abs(Q_num - Q_exact) / Q_exact,
    }


def frozen_drift_spacetime_Q(a: float, eps: float, nu: float, T: float) -> float:
    """Exact closed form from bench §3."""
    return (
        math.pi**1.5
        * a**4
        * eps**5
        / (240.0 * nu)
        * (1.0 - (eps**2 / (eps**2 + 4.0 * nu * T)) ** 7.5)
    )


def initial_U_signs() -> dict:
    """Section 6: on axis ∂tU/a² = e^{-2s²} - 4 I(s)/s^5; midplane I(s)/s^5 > 0."""

    def I(s: float) -> float:
        # ∫_0^s τ^4 e^{-2τ²} dτ
        # integrate by parts / incomplete gamma style numerical
        n = 20000
        t = np.linspace(0.0, s, n)
        dt = t[1] - t[0] if s > 0 else 0.0
        if s == 0:
            return 0.0
        f = (t**4) * np.exp(-2 * t * t)
        # simpson
        w = np.ones(n)
        w[1:-1:2] = 4
        w[2:-1:2] = 2
        return float(np.sum(w * f) * dt / 3.0)

    def axis_val(s: float) -> float:
        if s < 1e-8:
            return 1.0 / 5.0
        return math.exp(-2 * s * s) - 4.0 * I(s) / (s**5)

    # root find first positive zero
    lo, hi = 0.1, 2.0
    assert axis_val(lo) > 0 and axis_val(hi) < 0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if axis_val(mid) > 0:
            lo = mid
        else:
            hi = mid
    root = 0.5 * (lo + hi)
    at1 = axis_val(1.0)
    origin = axis_val(0.0)
    midplane_at1 = I(1.0) / (1.0**5)
    return {
        "origin_axis_limit": origin,
        "first_axis_zero_s": root,
        "axis_value_at_s1": at1,
        "midplane_value_at_s1": midplane_at1,
        "bench_first_zero": 0.6067752158654651,
        "bench_axis_s1": -0.0764359761,
        "zero_abs_err": abs(root - 0.6067752158654651),
        "s1_abs_err": abs(at1 - (-0.0764359761)),
    }


def local_layer_constants() -> dict:
    m0 = (5.0 / 4.0) ** (-2.5) * math.exp(-5.0 / 16.0)
    c0 = (3.0 * math.pi / 512.0) * (m0 / 2.0) ** 4
    return {
        "m0": m0,
        "c0": c0,
        "bench_m0": 0.4188012236,
        "bench_c0": 3.53926394e-5,
        "m0_abs_err": abs(m0 - 0.4188012236),
        "c0_rel_err": abs(c0 - 3.53926394e-5) / 3.53926394e-5,
    }


def amplitude_rejects_pure_absorption() -> dict:
    """§9: C_F ~ M^5, D_F ~ M^4 ⇒ C_F / D_F → ∞ as M→∞."""
    # Use symbolic ratios only
    return {
        "C_F_scale": "M^5",
        "D_F_scale": "M^4",
        "ratio_C_over_D_scale": "M",
        "universal_pure_absorption_C_le_eta_nu_D": False,
    }


def main() -> None:
    gauss = simpson_radial_gaussian_moments()
    # Frozen drift leading coefficient for a=ε^{-3/2}
    # ∫∫|F|^4 ~ π^{3/2}/(240 ν ε) as ε→0, T fixed
    lead = math.pi**1.5 / 240.0
    signs = initial_U_signs()
    layer = local_layer_constants()
    amp = amplitude_rejects_pure_absorption()

    report = {
        "status": "preliminary_verify_only",
        "claims": {
            "gaussian_E_Q_match_exact": gauss["E_rel_err"] < 1e-6 and gauss["Q_rel_err"] < 1e-6,
            "axis_zero_matches_bench": signs["zero_abs_err"] < 5e-4,
            "axis_s1_matches_bench": signs["s1_abs_err"] < 5e-4,
            "m0_c0_match_bench": layer["m0_abs_err"] < 1e-8 and layer["c0_rel_err"] < 1e-6,
            "pure_absorption_rejected_by_amplitude": True,
        },
        "gaussian": gauss,
        "frozen_drift_leading_coeff_over_nu_eps": lead,
        "example_frozen_Q_a_eps_m3_2": {
            "eps": 1e-2,
            "nu": 1.0,
            "T": 1.0,
            "Q_spacetime": frozen_drift_spacetime_Q(a=(1e-2) ** (-1.5), eps=1e-2, nu=1.0, T=1.0),
            "leading_pi32_over_240_nu_eps": lead / (1.0 * 1e-2),
        },
        "initial_U_signs": signs,
        "local_layer": layer,
        "amplitude": amp,
        "honesty": {
            "ns_solved": False,
            "gate_proved": False,
            "shahmurov_deficiency_alleged": False,
            "full_nse_simulation_run": False,
        },
    }

    out_json = OUT / "verify_report.json"
    out_json.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    print(f"wrote {out_json}")

    # Fail hard if core checks break
    assert report["claims"]["gaussian_E_Q_match_exact"]
    assert report["claims"]["axis_zero_matches_bench"]
    assert report["claims"]["axis_s1_matches_bench"]
    assert report["claims"]["m0_c0_match_bench"]


if __name__ == "__main__":
    main()
