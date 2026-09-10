#!/usr/bin/env python3
"""Attack 2 — Triad / K=0 kill / C* X^{3/2} Λ survivor.

Hard hit already claimed: K=0 (pure viscous absorption Tc ≤ θν Ds) is DEAD
because Tc/Ds grows like amplitude B→∞ on fixed-shape high triad.

Survivor candidate: Tc ≤ θν Ds + C* X^{3/2} Λ  (K ∼ √X), Leray-integrable via ∫X < ∞.

This script re-confirms K=0 death and measures C* = Tc / (X^{3/2} Λ) amplitude invariance.
Also probes X≈1 slices and scale-separated triads.
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
    scale_field,
)


def normalize_to_X(field, X_target: float = 1.0):
    m = moments(field)
    if m["X"] <= 0:
        return field
    return scale_field(field, np.sqrt(X_target / m["X"]))


def run() -> dict:
    B_list = [0.1, 1.0, 10.0, 100.0, 1000.0, 1e4]
    base = high_triad_field(amp=1.0)
    k0_ratios = []
    cstar_ratios = []
    rows = []
    for B in B_list:
        r = probe(scale_field(base, B), label=f"triad_B={B:g}")
        print(format_probe(r), flush=True)
        k0_ratios.append(abs(r.ratio_k0) if np.isfinite(r.ratio_k0) else float("inf"))
        cstar_ratios.append(r.ratio_cstar)
        rows.append(
            {
                "B": B,
                "ratio_k0": r.ratio_k0,
                "ratio_cstar": r.ratio_cstar,
                "ratio_star": r.ratio_star,
                "Tc": r.Tc,
                "Ds": r.Ds,
                "X": r.X,
            }
        )

    # X=1 slice: scale field so X=1, vary shape via different triad wavevectors
    triad_shapes = [
        ((4, 2, 1), (-3, 1, 1)),
        ((8, 1, 1), (-5, 2, 1)),
        ((16, 4, 2), (-12, 3, 1)),
        ((3, 3, 1), (-2, -2, 1)),
        ((7, 0, 1), (-4, 2, 1)),
    ]
    x1_rows = []
    for k1, k2 in triad_shapes:
        f = normalize_to_X(high_triad_field(amp=1.0, k1=k1, k2=k2), 1.0)
        r = probe(f, label=f"X1_{k1}_{k2}")
        print(format_probe(r), flush=True)
        x1_rows.append(
            {
                "k1": k1,
                "k2": k2,
                "X": r.X,
                "Tc_over_Lambda": r.Tc / r.Lambda if r.Lambda else None,
                "ratio_cstar": r.ratio_cstar,
                "ratio_star": r.ratio_star,
                "ratio_k0": r.ratio_k0,
            }
        )

    # Scale separation: low+high mixed triad-like (use high triad with stretched k)
    sep_rows = []
    for scale in [1, 2, 4, 8]:
        k1 = (4 * scale, 2 * scale, 1 * scale)
        k2 = (-3 * scale, 1 * scale, 1 * scale)
        f = normalize_to_X(high_triad_field(amp=1.0, k1=k1, k2=k2), 1.0)
        r = probe(f, label=f"sep_s={scale}")
        print(format_probe(r), flush=True)
        sep_rows.append({"scale": scale, "ratio_cstar": r.ratio_cstar, "ratio_star": r.ratio_star})

    # K=0 blows if |Rk0| grows ~ linearly (or worse) with B
    # On fixed shape: X ~ B^2, Ds ~ B^2, Tc ~ B^3 (cubic nonlinearity) => Rk0 ~ B
    finite_k0 = [x for x in k0_ratios if np.isfinite(x)]
    k0_killed = len(finite_k0) >= 2 and finite_k0[-1] > 50 * finite_k0[0]

    cstar_abs = [abs(x) for x in cstar_ratios if np.isfinite(x)]
    cstar_spread = float(np.max(cstar_abs) / max(np.min(cstar_abs), 1e-30)) if cstar_abs else None

    summary = {
        "attack": 2,
        "name": "triad_K0_Cstar",
        "rows": rows,
        "x1_rows": x1_rows,
        "sep_rows": sep_rows,
        "K0_killed": bool(k0_killed),
        "K0_ratio_abs_by_B": k0_ratios,
        "Cstar_abs_max": float(np.max(cstar_abs)) if cstar_abs else None,
        "Cstar_abs_min": float(np.min(cstar_abs)) if cstar_abs else None,
        "Cstar_amplitude_spread_factor": cstar_spread,
        "Cstar_amplitude_invariant_approx": bool(cstar_spread is not None and cstar_spread < 1.5),
        "x1_max_abs_Tc_over_Lambda": float(
            max(abs(x["Tc_over_Lambda"]) for x in x1_rows if x["Tc_over_Lambda"] is not None)
        ),
        "verdict": (
            "K0_DEAD_Cstar_SURVIVES_numeric"
            if k0_killed and cstar_spread is not None and cstar_spread < 2.0
            else "K0_DEAD_Cstar_UNCLEAR"
            if k0_killed
            else "UNEXPECTED_K0_ALIVE"
        ),
        "ns_solved": False,
    }
    print("\n=== ATTACK 2 SUMMARY ===", flush=True)
    print(
        json.dumps({k: v for k, v in summary.items() if k not in ("rows", "x1_rows", "sep_rows")}, indent=2),
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
