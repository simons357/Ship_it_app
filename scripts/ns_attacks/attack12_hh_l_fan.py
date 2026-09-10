#!/usr/bin/env python3
"""Attack 12 — HH→L fan, one low key or whole low shell. Not a proof.

Partners of k on a high sphere α. Pair counts 2–12.
R★ largest when α∼β and falls as α/β grows, tracking ∼β/α.
The vertex carries √β, not √α. Multiplicity does not flip it.

Designed Θ(m^2) subset is Freiman-AP: already dead.
NS is not solved.
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
    hh_l_one_key_field,
    hh_l_whole_shell_field,
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


def best_one_key(k, alpha, rng, n_try=4):
    best = None
    shifts = (0.0, 0.5 * np.pi, np.pi, -0.5 * np.pi)
    configs = [(True, (0.2, 1.0, -0.3))]
    for i in range(n_try):
        seed = (0.2, 1.0, -0.3) if i == 0 else tuple(float(x) for x in rng.normal(size=3))
        configs.append((False, seed))
    for aligned, seed in configs:
        for sh in shifts:
            f, meta = hh_l_one_key_field(
                k, alpha, phase_high=float(sh), pol_seed=seed, aligned_pol=aligned
            )
            if not f:
                continue
            r = probe(f, label=f"hhl1_{alpha}")
            rec = {
                **meta,
                "k_low": list(meta["k_low"]),
                "ratio_box": float(r.ratio_box) if np.isfinite(r.ratio_box) else None,
                "Tc": float(r.Tc),
                "Ds": float(r.Ds),
                "Y": float(r.Y),
                "beta_over_alpha": meta["beta"] / alpha,
            }
            if rec["ratio_box"] is None:
                continue
            if best is None or rec["ratio_box"] > best["ratio_box"]:
                best = rec
    return best


def best_whole(beta, alpha, rng, n_try=3):
    best = None
    shifts = (0.0, 0.5 * np.pi, np.pi, -0.5 * np.pi)
    configs = [(True, (0.2, 1.0, -0.3))]
    for i in range(n_try):
        seed = (0.2, 1.0, -0.3) if i == 0 else tuple(float(x) for x in rng.normal(size=3))
        configs.append((False, seed))
    for aligned, seed in configs:
        for sh in shifts:
            f, meta = hh_l_whole_shell_field(
                beta, alpha, phase_high=float(sh), pol_seed=seed, aligned_pol=aligned
            )
            if not f:
                continue
            r = probe(f, label=f"hhlw_{alpha}")
            rec = {
                **meta,
                "ratio_box": float(r.ratio_box) if np.isfinite(r.ratio_box) else None,
                "Tc": float(r.Tc),
                "Ds": float(r.Ds),
                "Y": float(r.Y),
                "beta_over_alpha": beta / alpha,
            }
            if rec["ratio_box"] is None:
                continue
            if best is None or rec["ratio_box"] > best["ratio_box"]:
                best = rec
    return best


def run(seed: int = 12, n_try: int = 4) -> dict:
    rng = np.random.Generator(np.random.PCG64(seed))
    k = (2, 0, 0)
    one = []
    for alpha in (5, 9, 10, 17, 41):
        row = best_one_key(k, alpha, rng, n_try=n_try)
        if row:
            one.append(row)
            rb = row["ratio_box"]
            print(
                f"one-key β=4 α={alpha:3d} pairs={row['n_pairs']:2d}  "
                f"R★={rb:.4e}  β/α={row['beta_over_alpha']:.3f}",
                flush=True,
            )

    whole = []
    for alpha in (9, 17, 41, 50, 85):
        row = best_whole(2, alpha, rng, n_try=max(2, n_try - 1))
        if row:
            whole.append(row)
            rb = row["ratio_box"]
            print(
                f"whole  β=2 α={alpha:3d} pairs={row['n_pairs']:3d} high={row['n_high']:3d}  "
                f"R★={rb:.4e}  β/α={row['beta_over_alpha']:.4f}",
                flush=True,
            )

    rmax = 0.0
    for block in (one, whole):
        for row in block:
            if row.get("ratio_box"):
                rmax = max(rmax, row["ratio_box"])

    return _py(
        {
            "attack": 12,
            "name": "hh_l_sphere_fan",
            "ns_solved": False,
            "LemmaStar_killed": bool(rmax > 1e3),
            "one_key": one,
            "whole_shell": whole,
            "Rbox_max": rmax,
            "verdict": "KILL_LemmaStar" if rmax > 1e3 else "HH_L_FAN_OPEN_bound_open",
            "note": (
                "HH→L fan: R★ tracks β/α. More pairs do not flip it. "
                "Freiman-AP subset already dead. Finite sample is not a kill. "
                "NS not solved."
            ),
        }
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--n-try", type=int, default=4)
    args = ap.parse_args()
    summary = run(n_try=args.n_try)
    print("\n=== ATTACK 12 SUMMARY ===", flush=True)
    slim = {k: v for k, v in summary.items() if k not in ("one_key", "whole_shell")}
    print(json.dumps(slim, indent=2), flush=True)
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2))
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
