#!/usr/bin/env python3
"""Gate D — INITIAL static sweep (not episode evolution).

Produces GATE-D-INITIAL-SWEEP-2026-10-08.json for the six-box Signed-Gate
adversary. This measures only t=0 diagnostics and a local clock estimate.
It does NOT compute I_H or B_IH and must not be scored as episode cost.

Protocol (author-stated initial sweep):
  - adversary: verify_signed_packet six-box (no Gaussian)
  - normalize E=1
  - fixed viscosity nu = 1e-5
  - Galerkin / high-pass bookkeeping cutoff scale 8H (k_max = 8H)
  - report X0, D0, D0/X0, tau_local = D0 / |D'(0)|, and height*clock

Numerical evidence only. No theorem stamp.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from verify_signed_gate import box, packet, polarization

# Reuse the sparse RHS / transfer kernels from the evolution driver when present.
from gate_d_adversarial_run import (
    build_packet_arrays,
    hermitize,
    merge_axpy,
    moments,
    normalize_E,
    rhs_sparse,
    transfer_scalene,
)


NU_SWEEP = 1.0e-5


def fit_log_log(Hs, vals):
    """Least-squares exponent for val ~ C * H^p."""
    x = np.log(np.asarray(Hs, dtype=float))
    y = np.log(np.asarray(vals, dtype=float))
    A = np.vstack([x, np.ones_like(x)]).T
    p, b = np.linalg.lstsq(A, y, rcond=None)[0]
    return float(p), float(math.exp(b))


def one_n(n: int, nu: float = NU_SWEEP):
    meta = packet(n)
    H = int(meta["H"])
    k_high2 = H * H
    # Author sweep: cutoff 8H (ball |k| <= 8H)
    k_max = 8 * H
    k_max2 = k_max * k_max

    k, u = build_packet_arrays(n)
    u = normalize_E(u, 1.0)
    k, u = hermitize(k, u)

    E0, X0, Y0, X_H0, Y_H0, U0, W0 = moments(k, u, float(k_high2))
    T0, n_act = transfer_scalene(k, u, float(k_high2))
    D0 = T0 - nu * Y_H0 / 4.0

    fk, fu = rhs_sparse(k, u, nu, k_max2, 0.0)
    eps = 1e-8
    be_k, be_u = merge_axpy(k, u, fk, fu, eps, k_max2, 0.0)
    Te, _ = transfer_scalene(be_k, be_u, float(k_high2))
    _, _, _, _, YHe, _, _ = moments(be_k, be_u, float(k_high2))
    Dp = ((Te - nu * YHe / 4.0) - D0) / eps

    height = D0 / max(X_H0, 1e-300)
    tau_local = D0 / abs(Dp) if Dp != 0 else None
    product = height * tau_local if tau_local is not None else None

    T_expected = float(meta["T_scalene"]) / (float(meta["E"]) ** 1.5)
    return {
        "n": n,
        "H": H,
        "nu": nu,
        "E": 1.0,
        "k_high": H,
        "k_max_cutoff": k_max,
        "cutoff_rule": "8H",
        "modes": int(meta["modes"]),
        "active_high_modes": int(n_act),
        "X0": float(X_H0),
        "Y0": float(Y_H0),
        "T_sc0": float(T0),
        "T_sc0_verifier": float(T_expected),
        "T_sc_rel_err": float((T0 - T_expected) / abs(T_expected)),
        "D0": float(D0),
        "D0_prime": float(Dp),
        "D0_over_X0": float(height),
        "tau_local_D_over_abs_Dprime": None if tau_local is None else float(tau_local),
        "height_times_tau_local": None if product is None else float(product),
        "U0": float(U0),
        "W0": float(W0),
        "is_episode_cost_B_IH": False,
        "note": "Static t=0 sweep only. Not B_IH.",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="+", default=[1, 2, 3, 4])
    ap.add_argument("--nu", type=float, default=NU_SWEEP)
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).with_name("GATE-D-INITIAL-SWEEP-2026-10-08.json"),
    )
    args = ap.parse_args()

    rows = [one_n(n, args.nu) for n in args.n]
    Hs = [r["H"] for r in rows]
    fits = {
        "X0_exponent": fit_log_log(Hs, [r["X0"] for r in rows]),
        "D0_exponent": fit_log_log(Hs, [r["D0"] for r in rows]),
        "D0_over_X0_exponent": fit_log_log(Hs, [r["D0_over_X0"] for r in rows]),
        "tau_local_exponent": fit_log_log(
            Hs, [r["tau_local_D_over_abs_Dprime"] for r in rows]
        ),
        "height_times_tau_local_exponent": fit_log_log(
            Hs, [r["height_times_tau_local"] for r in rows]
        ),
    }
    # store as {exponent, prefactor}
    fits = {k: {"exponent": v[0], "prefactor": v[1]} for k, v in fits.items()}

    payload = {
        "title": "Gate D initial static sweep — 8 October 2026",
        "adversary": "Signed-Gate-B-Sharp-Band-Exponent-2026-10-07 six-box",
        "nu": args.nu,
        "cutoff": "8H",
        "theorem_stamp": False,
        "gaussian_substituted": False,
        "computes_B_IH": False,
        "warning": (
            "This JSON is a t=0 / local-clock diagnostic. "
            "It is not I_H, not B_IH, and must not be scored as episode cost."
        ),
        "fits_log_log": fits,
        "rows": rows,
    }
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"out": str(args.out), "fits": fits, "products": [r["height_times_tau_local"] for r in rows]}, indent=2))


if __name__ == "__main__":
    main()
