#!/usr/bin/env python3
"""Attack 7 — the boxed ratio R★. Exact reduction of Lemma★. Not a proof.

R★(v) = (Tc(v)_+)^2 / (Ds(v) ||v||_2^2 Y(v)).
If sup R★ = ∞, Lemma★ is dead.
If Ds=0 and Tc>0, dead immediately.
Numerics are evidence only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ns_attacks.stokes_moments import (  # noqa: E402
    enforce_reality,
    high_triad_field,
    make_divfree_amp,
    probe,
    scale_field,
)


def _py(x):
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, dict):
        return {k: _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    return x


def unishell_field() -> dict:
    """Two modes, same |k|^2. Algebra: Ds=0 ⇒ Tc=0."""
    field = {}
    for k, seed in (((1, 0, 0), (0.0, 1.0, 0.0)), ((0, 1, 0), (1.0, 0.0, 0.0))):
        v = make_divfree_amp(k, seed)
        field[k] = v / np.linalg.norm(v)
    r = probe(enforce_reality(field), label="unishell")
    return {
        "Ds": float(r.Ds),
        "Tc": float(r.Tc),
        "ratio_box": float(r.ratio_box) if np.isfinite(r.ratio_box) else None,
        "Lambda": float(r.Lambda),
    }


def near_mono(eps: float, rng: np.random.Generator) -> dict:
    k_main = (3, 1, 0)
    k_pert = (1, -2, 1)
    f = {}
    v = make_divfree_amp(k_main, (1.0, 0.0, 0.0))
    f[k_main] = v / np.linalg.norm(v)
    vp = make_divfree_amp(k_pert, rng.normal(size=3))
    n = np.linalg.norm(vp)
    if n > 0:
        f[k_pert] = eps * vp / n
    r = probe(enforce_reality(f), label=f"mono_{eps}")
    return {
        "eps": eps,
        "Ds": float(r.Ds),
        "Tc": float(r.Tc),
        "ratio_box": float(r.ratio_box) if np.isfinite(r.ratio_box) else None,
        "Tc_over_Ds": float(r.ratio_k0) if np.isfinite(r.ratio_k0) else None,
    }


def run(seed: int = 3) -> dict:
    rng = np.random.Generator(np.random.PCG64(seed))
    uni = unishell_field()

    base = high_triad_field(amp=1.0)
    r1 = probe(base, label="triad_a=1")
    r10 = probe(scale_field(base, 10.0), label="triad_a=10")

    scales = []
    for s in (1, 2, 4, 8, 16, 32, 64):
        r = probe(
            high_triad_field(amp=1.0, k1=(4 * s, 2 * s, s), k2=(-3 * s, s, s)),
            label=f"sep_{s}",
        )
        scales.append(
            {
                "s": s,
                "ratio_box": float(r.ratio_box) if np.isfinite(r.ratio_box) else None,
                "ratio_preyoung": float(r.ratio_preyoung),
                "Ds": float(r.Ds),
                "Tc": float(r.Tc),
            }
        )
        print(
            f"s={s:3d}  Rbox={r.ratio_box:.4e}  Rpre={r.ratio_preyoung:.4f}  "
            f"Ds={r.Ds:.4e}  Tc={r.Tc:.4e}",
            flush=True,
        )

    monos = []
    for eps in (1e-6, 1e-4, 1e-3, 1e-2, 1e-1):
        best = None
        for _ in range(16):
            row = near_mono(eps, rng)
            if row["ratio_box"] is None:
                continue
            if best is None or row["ratio_box"] > best["ratio_box"]:
                best = row
        if best:
            monos.append(best)
            print(
                f"mono eps={eps:g}  Rbox={best['ratio_box']:.4e}  "
                f"Ds={best['Ds']:.4e}  Tc={best['Tc']:.4e}",
                flush=True,
            )

    boxes = [s["ratio_box"] for s in scales if s["ratio_box"] is not None]
    mono_boxes = [m["ratio_box"] for m in monos if m["ratio_box"] is not None]
    killed = False
    if boxes and max(boxes) > 1e6:
        killed = True
    if mono_boxes and max(mono_boxes) > 1e6:
        killed = True
    if abs(uni["Ds"]) < 1e-12 and abs(uni["Tc"]) > 1e-8:
        killed = True

    summary = {
        "attack": 7,
        "name": "boxed_Rstar_reduction",
        "ns_solved": False,
        "LemmaStar_killed": killed,
        "unishell": uni,
        "unishell_Tc_vanishes": abs(uni["Tc"]) < 1e-8,
        "amplitude_Rbox_a1": float(r1.ratio_box) if np.isfinite(r1.ratio_box) else None,
        "amplitude_Rbox_a10": float(r10.ratio_box) if np.isfinite(r10.ratio_box) else None,
        "scales": scales,
        "near_mono": monos,
        "Rbox_max_scale": max(boxes) if boxes else None,
        "Rbox_max_mono": max(mono_boxes) if mono_boxes else None,
        "verdict": "KILL_LemmaStar" if killed else "REDUCTION_SITS_bound_open",
        "note": (
            "R★ is the exact viscosity-free form of Lemma★. "
            "A bounded sample is not a uniform bound. NS not solved."
        ),
    }
    return _py(summary)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="")
    args = ap.parse_args()
    summary = run()
    print("\n=== ATTACK 7 SUMMARY ===", flush=True)
    slim = {k: v for k, v in summary.items() if k not in ("scales", "near_mono")}
    print(json.dumps(slim, indent=2), flush=True)
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2))
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
