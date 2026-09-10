#!/usr/bin/env python3
"""Attack 6 — scale law and coherent HH→L fan. Not a proof.

Idea: geometry-only C_0 cannot grow with wavenumber. The five-lane
max sat on a scale-separated triad (sep_32). Sweep s and a coherent
fan of high pairs feeding one low mode. If |R_pre| grows without
bound, Lemma★ is killed. If it saturates, that is still not a proof.

NS is not solved. Do not cash a bounded ratio as C_0.
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
)


def _py(x):
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, dict):
        return {k: _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    return x


def best_phase_on_scaled_triad(s: int, rng: np.random.Generator, n_phase: int) -> dict:
    k1 = (4 * s, 2 * s, s)
    k2 = (-3 * s, s, s)
    best = None
    # default phases from the calculator, then random
    phase_list = [(0.0, 0.3, -0.2)]
    for _ in range(n_phase):
        phase_list.append(tuple(rng.uniform(0, 2 * np.pi, size=3)))
    for ph in phase_list:
        r = probe(high_triad_field(amp=1.0, k1=k1, k2=k2, phases=ph), label=f"sep_{s}")
        if not np.isfinite(r.ratio_preyoung):
            continue
        rec = {
            "s": s,
            "ratio_preyoung": float(r.ratio_preyoung),
            "abs_pre": float(abs(r.ratio_preyoung)),
            "ratio_cstar": float(r.ratio_cstar),
            "Lambda": float(r.Lambda),
            "Tc": float(r.Tc),
            "X": float(r.X),
            "E": float(r.E),
            "phases": [float(x) for x in ph],
        }
        if best is None or rec["abs_pre"] > best["abs_pre"]:
            best = rec
    return best


def coherent_fan(n_pairs: int, amp: float = 1.0) -> dict:
    """N high pairs with p+q = (1,0,0). HH→L stress. Not a close."""
    k_low = (1, 0, 0)
    field = {}
    used = 0
    n = 2
    while used < n_pairs and n < 80:
        p = (n, n, 1)
        q = (k_low[0] - p[0], k_low[1] - p[1], k_low[2] - p[2])
        n += 1
        if p == (0, 0, 0) or q == (0, 0, 0) or p == q:
            continue
        if p == tuple(-x for x in q):
            continue
        vp = make_divfree_amp(p, (1.0, 0.3, -0.4))
        vq = make_divfree_amp(q, (0.2, 1.0, 0.1))
        np_ = np.linalg.norm(vp)
        nq_ = np.linalg.norm(vq)
        if np_ < 1e-14 or nq_ < 1e-14:
            continue
        field[p] = (amp / np_) * vp
        field[q] = (amp / nq_) * vq
        used += 1
    f = enforce_reality(field)
    r = probe(f, label=f"fan_{n_pairs}")
    return {
        "n_pairs": n_pairs,
        "n_modes": len(f),
        "ratio_preyoung": float(r.ratio_preyoung) if np.isfinite(r.ratio_preyoung) else None,
        "abs_pre": float(abs(r.ratio_preyoung)) if np.isfinite(r.ratio_preyoung) else None,
        "ratio_cstar": float(r.ratio_cstar) if np.isfinite(r.ratio_cstar) else None,
        "Lambda": float(r.Lambda),
        "Tc": float(r.Tc),
        "X": float(r.X),
        "E": float(r.E),
    }


def run(seed: int = 17, n_phase: int = 24) -> dict:
    rng = np.random.Generator(np.random.PCG64(seed))
    scales = [1, 2, 4, 8, 16, 32, 48, 64]
    scale_rows = []
    for s in scales:
        row = best_phase_on_scaled_triad(s, rng, n_phase=n_phase)
        if row is not None:
            scale_rows.append(row)
            print(
                f"s={s:3d}  |Rpre|={row['abs_pre']:.4f}  "
                f"Rpre={row['ratio_preyoung']:.4f}  Λ={row['Lambda']:.1f}  "
                f"Rc*={row['ratio_cstar']:.4e}",
                flush=True,
            )

    fans = []
    for n_pairs in (2, 4, 8, 12, 16):
        row = coherent_fan(n_pairs)
        fans.append(row)
        print(
            f"fan N={n_pairs:2d}  |Rpre|={row['abs_pre']}  Λ={row['Lambda']:.1f}",
            flush=True,
        )

    abs_s = [r["abs_pre"] for r in scale_rows]
    # crude growth: |Rpre|(s) / s  and  |Rpre|(s)*s  vs the s=1 value
    growth = []
    if scale_rows:
        r1 = scale_rows[0]["abs_pre"]
        for r in scale_rows:
            s = r["s"]
            growth.append(
                {
                    "s": s,
                    "abs_pre": r["abs_pre"],
                    "abs_pre_over_s": r["abs_pre"] / s,
                    "abs_pre_times_s": r["abs_pre"] * s,
                    "vs_s1": r["abs_pre"] / r1 if r1 else None,
                }
            )

    killed = bool(abs_s and max(abs_s) > 1e3)
    # If |Rpre| keeps rising with s on this family, C_0 is not scale-free
    # even if it has not yet crossed the crude 1e3 kill line.
    rising = False
    if len(abs_s) >= 3:
        rising = abs_s[-1] > 1.5 * abs_s[0] and abs_s[-1] >= max(abs_s[:-1]) * 0.8

    summary = {
        "attack": 6,
        "name": "scale_law_and_coherent_fan",
        "ns_solved": False,
        "LemmaStar_C0_killed": killed,
        "scale_family_rising": rising,
        "scale_rows": scale_rows,
        "scale_growth": growth,
        "fans": fans,
        "abs_pre_max_scale": max(abs_s) if abs_s else None,
        "abs_pre_max_fan": max((f["abs_pre"] or 0.0) for f in fans) if fans else None,
        "verdict": (
            "KILL_LemmaStar"
            if killed
            else (
                "SCALE_FAMILY_GROWS_gap_remains"
                if rising
                else "SURVIVE_numeric_gap_remains"
            )
        ),
        "analytic_gap": (
            "Same door: |Tc| ≤ C ||u||_2 X Λ with geometry-only C, or the "
            "weaker C* X^{3/2} Λ form. HH→L is still the gap. A scale law "
            "on one triad family is not a proof and not a Clay close."
        ),
    }
    return _py(summary)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--seed", type=int, default=17)
    ap.add_argument("--n-phase", type=int, default=24)
    args = ap.parse_args()
    summary = run(seed=args.seed, n_phase=args.n_phase)
    print("\n=== ATTACK 6 SUMMARY ===", flush=True)
    slim = {k: v for k, v in summary.items() if k not in ("scale_rows", "fans")}
    print(json.dumps(slim, indent=2), flush=True)
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2))
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
