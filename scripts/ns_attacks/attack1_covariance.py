#!/usr/bin/env python3
"""Attack 1 — Covariance / Lemma★ amplitude survival.

Shape★ R_star_shape = Tc^2/(Ds E Y) is amp-invariant on fixed shape (canonical).
Post-Young R_post = Tc/(E X Λ) falls as B→∞; pre-Young R_pre = Tc/(√E X Λ)
is amp-invariant. If max |R_star_shape| or |R_pre| → ∞ across shapes, ★ C_geom
is KILLED. Fixed-shape B↑ alone cannot kill shape★ (ν already cancelled).
NS not solved.
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
    probe,
    random_field,
    scale_field,
)


def run(seed: int = 0, n_random: int = 200, B_list=None) -> dict:
    if B_list is None:
        B_list = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0, 500.0, 1000.0]
    rng = np.random.Generator(np.random.PCG64(seed))
    rows = []

    # Fixed-shape high triad amplitude sweep
    base = high_triad_field(amp=1.0)
    triad_ratios = []
    for B in B_list:
        r = probe(scale_field(base, B), label=f"triad_B={B}")
        triad_ratios.append(
            {
                "B": B,
                "ratio_star": r.ratio_star,
                "ratio_preyoung": r.ratio_preyoung,
                "ratio_cstar": r.ratio_cstar,
                "ratio_k0": r.ratio_k0,
                "ratio_R_star_shape": r.ratio_R_star_shape,
                "Tc": r.Tc,
                "E": r.E,
                "X": r.X,
                "Lambda": r.Lambda,
                "Ds": r.Ds,
            }
        )
        print(format_probe(r), flush=True)

    # Phase scan at B=1 — geometric pre-Young constant
    phase_pre = []
    for i in range(64):
        ph = tuple(rng.uniform(0, 2 * np.pi, size=3))
        f = high_triad_field(amp=1.0, phases=ph)
        r = probe(f, label=f"phase_{i}")
        phase_pre.append(r.ratio_preyoung)

    # Random fields
    rand_pre = []
    rand_star = []
    for i in range(n_random):
        f = random_field(rng, kmax=5, n_modes=10, amp=rng.uniform(0.5, 3.0))
        r = probe(f, label=f"rand_{i}")
        if np.isfinite(r.ratio_preyoung):
            rand_pre.append(r.ratio_preyoung)
        if np.isfinite(r.ratio_star):
            rand_star.append(r.ratio_star)

    pre_abs = [abs(x["ratio_preyoung"]) for x in triad_ratios if np.isfinite(x["ratio_preyoung"])]
    phase_abs = [abs(x) for x in phase_pre if np.isfinite(x)]
    rand_abs = [abs(x) for x in rand_pre]
    # Post-Young R★ falls as B↑ on fixed shape (expected)
    star_low = np.mean([abs(x["ratio_star"]) for x in triad_ratios[:3]])
    star_high = np.mean([abs(x["ratio_star"]) for x in triad_ratios[-3:]])
    pre_spread = float(np.max(pre_abs) / max(np.min(pre_abs), 1e-30)) if pre_abs else None

    # Shape★ amp-invariance on fixed triad
    shape_vals = [
        abs(x["ratio_R_star_shape"])
        for x in triad_ratios
        if np.isfinite(x["ratio_R_star_shape"])
    ]
    shape_spread = (
        float(np.max(shape_vals) / max(np.min(shape_vals), 1e-30)) if shape_vals else None
    )

    summary = {
        "attack": 1,
        "name": "covariance_LemmaStar",
        "canonical_form": "shape: R_star_shape = Tc^2/(Ds E Y)",
        "triad_amp_sweep": triad_ratios,
        "triad_abs_ratio_preyoung_max": float(np.max(pre_abs)) if pre_abs else None,
        "triad_abs_ratio_preyoung_min": float(np.min(pre_abs)) if pre_abs else None,
        "triad_preyoung_amp_spread_factor": pre_spread,
        "triad_preyoung_diam": float(np.max(pre_abs) - np.min(pre_abs)) if pre_abs else None,
        "triad_R_star_shape_max": float(np.max(shape_vals)) if shape_vals else None,
        "triad_R_star_shape_amp_spread_factor": shape_spread,
        "phase_abs_preyoung_max": float(np.max(phase_abs)) if phase_abs else None,
        "phase_abs_preyoung_diam": float(np.max(phase_abs) - np.min(phase_abs)) if phase_abs else None,
        "rand_abs_preyoung_max": float(np.max(rand_abs)) if rand_abs else None,
        "rand_abs_preyoung_p95": float(np.percentile(rand_abs, 95)) if rand_abs else None,
        "n_random": len(rand_abs),
        "postYoung_Rstar_falls_as_B_increases": bool(star_high < 0.5 * star_low),
        "amp_trend_star_low_mean_abs": float(star_low),
        "amp_trend_star_high_mean_abs": float(star_high),
        "blows_with_amplitude": False,  # fixed-shape R_post falls; kill needs shape family
        "verdict": (
            "KILL_LemmaStar_C0"
            if (rand_abs and np.max(rand_abs) > 1e3)
            else "SURVIVE_numeric_NOT_proof"
        ),
        "ns_solved": False,
    }
    print("\n=== ATTACK 1 SUMMARY ===", flush=True)
    print(json.dumps({k: v for k, v in summary.items() if k != "triad_amp_sweep"}, indent=2), flush=True)
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n-random", type=int, default=200)
    ap.add_argument("--out", type=str, default="")
    args = ap.parse_args()
    summary = run(seed=args.seed, n_random=args.n_random)
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2))
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
