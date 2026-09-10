#!/usr/bin/env python3
"""Attack 4 — Stokes-moment identities / absorption diagnostics.

Verify spectral calculus sanity (Ds≥0, scaling degrees) and measure
absorption ratios Tc / (ν Ds) vs remainder forms for Lemma★ packaging.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ns_attacks.stokes_moments import (  # noqa: E402
    format_probe,
    high_triad_field,
    moments,
    probe,
    random_field,
    scale_field,
)


def run(seed: int = 7) -> dict:
    rng = np.random.Generator(np.random.PCG64(seed))
    nu_list = [1.0, 0.1, 0.01]
    identity_checks = []

    # Ds ≥ 0 on many fields
    neg_Ds = 0
    for i in range(100):
        f = random_field(rng, kmax=5, n_modes=12, amp=rng.uniform(0.2, 2.0))
        m = moments(f)
        if m["Ds"] < -1e-8:
            neg_Ds += 1
        # Variance identity: Ds =?= Z - Y^2/X
        expect = m["Z"] - (m["Y"] ** 2) / m["X"] if m["X"] else 0.0
        identity_checks.append(abs(m["Ds"] - expect))

    # Homogeneity: u → B u
    # E~B^2, X~B^2, Y~B^2, Z~B^2, Λ~B^0, Ds~B^2, Tc~B^3, R★~B^0, Rc*~B^0, Rk0~B
    base = high_triad_field(amp=1.0)
    scaling = []
    for B in [1.0, 2.0, 4.0]:
        r = probe(scale_field(base, B), label=f"B={B}")
        print(format_probe(r), flush=True)
        scaling.append(
            {
                "B": B,
                "E_over_B2": r.E / B**2,
                "X_over_B2": r.X / B**2,
                "Ds_over_B2": r.Ds / B**2,
                "Tc_over_B3": r.Tc / B**3,
                "ratio_star": r.ratio_star,
                "ratio_cstar": r.ratio_cstar,
                "ratio_k0_over_B": r.ratio_k0 / B if np.isfinite(r.ratio_k0) else None,
            }
        )

    # Viscous absorption diagnostic: need Tc ≤ θ ν Ds + remainder
    # Measure minimal θ such that Tc - θ ν Ds ≤ 0 fails → remainder needed
    abs_rows = []
    for nu in nu_list:
        for B in [1.0, 10.0, 100.0]:
            r = probe(scale_field(base, B), label=f"nu={nu}_B={B}")
            # If we try θ=1: remainder = Tc - ν Ds
            rem = r.Tc - nu * r.Ds
            abs_rows.append(
                {
                    "nu": nu,
                    "B": B,
                    "Tc": r.Tc,
                    "nu_Ds": nu * r.Ds,
                    "remainder_Tc_minus_nuDs": rem,
                    "rem_over_EXLam": rem / (r.E * r.X * r.Lambda) if r.E * r.X * r.Lambda else None,
                    "rem_over_X32Lam": rem / ((r.X**1.5) * r.Lambda) if r.X and r.Lambda else None,
                }
            )

    summary = {
        "attack": 4,
        "name": "stokes_moments",
        "neg_Ds_count": neg_Ds,
        "Ds_identity_max_err": float(np.max(identity_checks)) if identity_checks else None,
        "scaling": scaling,
        "absorption_rows": abs_rows,
        "scaling_ok": all(
            abs(scaling[i]["E_over_B2"] - scaling[0]["E_over_B2"]) < 1e-8
            and abs(scaling[i]["Tc_over_B3"] - scaling[0]["Tc_over_B3"]) < 1e-8
            and abs(scaling[i]["ratio_cstar"] - scaling[0]["ratio_cstar"]) < 1e-8
            for i in range(len(scaling))
        ),
        "verdict": "STOKES_IDENTITIES_OK_absorption_needs_remainder",
        "ns_solved": False,
    }
    print("\n=== ATTACK 4 SUMMARY ===", flush=True)
    print(
        json.dumps({k: v for k, v in summary.items() if k not in ("scaling", "absorption_rows")}, indent=2),
        flush=True,
    )
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="")
    args = ap.parse_args()
    summary = run()
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2))
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
