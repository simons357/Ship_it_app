#!/usr/bin/env python3
"""Attack 5 — Route 2 / alternate remainder forms + Lemma★ kill drill.

Goal: try to KILL Lemma★ uniform C0 by maximizing |Tc|/(E X Λ) over a large
family (random fields, triads, scale separations, near-mono-chromatic, etc.).
If the empirical max stays O(1), document strongest numeric bound and the
exact analytic gap that remains.
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
    make_divfree_amp,
    moments,
    probe,
    random_field,
    scale_field,
    two_shell_field,
    enforce_reality,
)


def mono_plus_perturbation(rng, k_main=(3, 1, 0), k_pert=(1, -2, 1), eps=1e-2):
    """Nearly single-mode field (Ds small) + tiny perturbation — stress Rk0 / R★."""
    f = {}
    v = make_divfree_amp(k_main, (1.0, 0.0, 0.0))
    f[k_main] = v / np.linalg.norm(v)
    vp = make_divfree_amp(k_pert, rng.normal(size=3))
    n = np.linalg.norm(vp)
    if n > 0:
        f[k_pert] = eps * vp / n
    return enforce_reality(f)


def run(seed: int = 11, n_random: int = 500) -> dict:
    rng = np.random.Generator(np.random.PCG64(seed))
    best = {"abs_ratio_preyoung": 0.0}
    samples = []

    def consider(r, tag):
        nonlocal best
        if not np.isfinite(r.ratio_preyoung):
            return
        samples.append(
            {
                "tag": tag,
                "ratio_star": r.ratio_star,
                "ratio_preyoung": r.ratio_preyoung,
                "ratio_cstar": r.ratio_cstar,
                "ratio_k0": r.ratio_k0,
                "E": r.E,
                "X": r.X,
                "Lambda": r.Lambda,
                "Ds": r.Ds,
                "Tc": r.Tc,
            }
        )
        if abs(r.ratio_preyoung) > best["abs_ratio_preyoung"]:
            best = {
                "abs_ratio_preyoung": abs(r.ratio_preyoung),
                "ratio_preyoung": r.ratio_preyoung,
                "ratio_star": r.ratio_star,
                "tag": tag,
                "ratio_cstar": r.ratio_cstar,
                "E": r.E,
                "X": r.X,
                "Lambda": r.Lambda,
                "Ds": r.Ds,
                "Tc": r.Tc,
            }

    # Random barrage
    for i in range(n_random):
        f = random_field(
            rng,
            kmax=int(rng.integers(3, 8)),
            n_modes=int(rng.integers(4, 20)),
            amp=float(rng.uniform(0.1, 50.0)),
        )
        consider(probe(f), f"rand_{i}")

    # Triad amplitude + phase
    for B in np.geomspace(0.01, 1e4, 16):
        for j in range(8):
            ph = tuple(rng.uniform(0, 2 * np.pi, size=3))
            f = high_triad_field(amp=float(B), phases=ph)
            consider(probe(f), f"triad_B={B:g}_p{j}")

    # Scale-separated triads
    for s in [1, 2, 4, 8, 16]:
        f = high_triad_field(amp=1.0, k1=(4 * s, 2 * s, s), k2=(-3 * s, s, s))
        consider(probe(f), f"sep_{s}")

    # Two-shell families
    for al in [0.1, 1.0, 10.0]:
        for ah in [0.1, 1.0, 10.0, 100.0]:
            f = two_shell_field(al, ah)
            consider(probe(f), f"shell_{al}_{ah}")

    # Near-monochromatic (small Ds)
    for eps in [1e-4, 1e-3, 1e-2, 1e-1]:
        for j in range(20):
            f = mono_plus_perturbation(rng, eps=eps)
            r = probe(f, label=f"mono_eps={eps}")
            consider(r, f"mono_eps={eps}_{j}")

    # Route-2 alternate remainders on best / triad sample
    base = high_triad_field(amp=1.0)
    r = probe(base)
    alt = {
        "Tc_over_E_X_Lambda_postYoung": r.ratio_star,
        "Tc_over_sqrtE_X_Lambda_preYoung": r.ratio_preyoung,
        "Tc_over_X32_Lambda": r.ratio_cstar,
        "Tc_over_Ds": r.ratio_k0,
        "Tc_over_E_Y": r.Tc / (r.E * r.Y) if r.E * r.Y else None,
        "Tc_over_B_L2_Y": r.Tc / (r.B_L2 * r.Y) if r.B_L2 * r.Y else None,
        "Young_gap_note": (
            "Lemma★ remainder is the Young lift of a degree-3 bound |Tc|≤C||u||_2 X Λ; "
            "C* form uses |Tc|≤C* X^{3/2} Λ. HH→L blocks standard 3D product close."
        ),
    }
    print(format_probe(r), flush=True)
    print(f"best so far: {best}", flush=True)

    abs_pre = [abs(s["ratio_preyoung"]) for s in samples]
    abs_cstar = [abs(s["ratio_cstar"]) for s in samples if np.isfinite(s["ratio_cstar"])]
    # Kill if geometric pre-Young constant blows on smooth Galerkin family
    killed = bool(abs_pre) and max(abs_pre) > 1e3

    summary = {
        "attack": 5,
        "name": "route2_LemmaStar_kill_drill",
        "n_samples": len(samples),
        "abs_ratio_preyoung_max": float(np.max(abs_pre)) if abs_pre else None,
        "abs_ratio_preyoung_p50": float(np.percentile(abs_pre, 50)) if abs_pre else None,
        "abs_ratio_preyoung_p95": float(np.percentile(abs_pre, 95)) if abs_pre else None,
        "abs_ratio_preyoung_p99": float(np.percentile(abs_pre, 99)) if abs_pre else None,
        "abs_ratio_cstar_max": float(np.max(abs_cstar)) if abs_cstar else None,
        "best": best,
        "alternate_remainders_on_unit_triad": alt,
        "LemmaStar_C0_killed": killed,
        "verdict": "KILL_LemmaStar" if killed else "SURVIVE_numeric_gap_remains",
        "analytic_gap": (
            "Pre-Young target |Tc| ≤ C ||u||_2 X Λ (amp-invariant C), which Young-lifts to "
            "Lemma★'s ν^{-1}||u||_2^2 X Λ remainder; or weaker |Tc| ≤ C* X^{3/2} Λ. "
            "Numerics support bounded ratios on tested families; standard 3D product/Agmon "
            "do not close HH→L. NOT A PROOF. NS NOT SOLVED."
        ),
        "ns_solved": False,
    }
    print("\n=== ATTACK 5 SUMMARY ===", flush=True)
    print(json.dumps({k: v for k, v in summary.items() if k != "best"}, indent=2), flush=True)
    print("best=", json.dumps(best, indent=2), flush=True)
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--n-random", type=int, default=500)
    args = ap.parse_args()
    summary = run(seed=args.seed, n_random=args.n_random)
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2))
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
