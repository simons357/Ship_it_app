#!/usr/bin/env python3
"""Attack 11 — full adjacent lattice spheres. Not a proof.

Two shells n and n+d, energy split, m = #keys grows with n.
Ds is the gap, not AP width. Landings scale like O(m), not O(m^2).

If R★ tracked m^{1/2} here, Lemma★ would be in trouble.
It does not. NS is not solved.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import List

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ns_attacks.stokes_moments import (  # noqa: E402
    adjacent_sphere_landings,
    adjacent_spheres_field,
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


def best_adjacent(n: int, d: int, rng: np.random.Generator, n_try: int = 4) -> dict | None:
    A, B, pairs = adjacent_sphere_landings(n, d)
    if not A or not B:
        return {
            "n": n,
            "d": d,
            "n_A": len(A),
            "n_B": len(B),
            "m": len(A) + len(B),
            "n_landings": 0,
            "ratio_box": None,
            "note": "empty partner shell",
        }
    if not pairs:
        return {
            "n": n,
            "d": d,
            "n_A": len(A),
            "n_B": len(B),
            "m": len(A) + len(B),
            "n_landings": 0,
            "ratio_box": None,
            "note": "no landings",
        }
    best = None
    shifts = (0.0, 0.5 * np.pi, np.pi, -0.5 * np.pi)
    configs = [(True, (0.2, 1.0, -0.3))]
    for i in range(n_try):
        seed = (0.2, 1.0, -0.3) if i == 0 else tuple(float(x) for x in rng.normal(size=3))
        configs.append((False, seed))
    for aligned, seed in configs:
        for sh in shifts:
            f, meta = adjacent_spheres_field(
                n, d, phase_npd=float(sh), pol_seed=seed, aligned_pol=aligned
            )
            if not f:
                continue
            r = probe(f, label=f"adj_{n}_{d}")
            rec = {
                **meta,
                "aligned_pol": aligned,
                "ratio_box": float(r.ratio_box) if np.isfinite(r.ratio_box) else None,
                "Tc": float(r.Tc),
                "Ds": float(r.Ds),
                "E": float(r.E),
                "Y": float(r.Y),
                "Lambda": float(r.Lambda),
            }
            if rec["ratio_box"] is None:
                continue
            if best is None or rec["ratio_box"] > best["ratio_box"]:
                best = rec
    return best


def log_exponents(rows: List[dict], xkey: str, ykey: str = "ratio_box") -> List[dict]:
    usable = [r for r in rows if r and r.get(ykey) and r[ykey] > 0 and r.get(xkey, 0) > 0]
    usable = sorted(usable, key=lambda r: r[xkey])
    out = []
    for a, b in zip(usable, usable[1:]):
        lx = math.log(b[xkey] / a[xkey])
        ly = math.log(b[ykey] / a[ykey])
        out.append(
            {
                "from": a[xkey],
                "to": b[xkey],
                "exponent": float(ly / lx) if abs(lx) > 1e-12 else None,
                "R_from": a[ykey],
                "R_to": b[ykey],
            }
        )
    return out


def run(seed: int = 11, n_try: int = 4) -> dict:
    rng = np.random.Generator(np.random.PCG64(seed))
    ns = (9, 17, 25, 41, 57, 73, 89)
    d1 = []
    for n in ns:
        row = best_adjacent(n, 1, rng, n_try=n_try)
        if row:
            d1.append(row)
            rb = row.get("ratio_box")
            rbs = f"{rb:.4e}" if rb else "none"
            print(
                f"d=1 n={n:3d} m={row['m']:3d} A={row['n_A']:3d} B={row['n_B']:3d} "
                f"land={row['n_landings']:4d}  R★={rbs}  "
                f"Ds={row.get('Ds', float('nan'))}",
                flush=True,
            )

    d2 = []
    for n in (9, 17, 41, 89):
        row = best_adjacent(n, 2, rng, n_try=1)
        d2.append(row)
        print(
            f"d=2 n={n:3d} m={row['m']:3d} land={row['n_landings']}  {row.get('note', '')}",
            flush=True,
        )

    d3 = []
    for n in (9, 17, 25, 41, 89):
        row = best_adjacent(n, 3, rng, n_try=max(2, n_try // 2))
        d3.append(row)
        rb = row.get("ratio_box")
        rbs = f"{rb:.4e}" if rb else "none"
        print(
            f"d=3 n={n:3d} m={row['m']:3d} land={row['n_landings']:4d}  R★={rbs}",
            flush=True,
        )

    live = [r for r in d1 if r.get("ratio_box")]
    rmax = max((r["ratio_box"] for r in live), default=0.0)
    ds_over_n = [
        r["Ds"] / r["n"] for r in live if r.get("Ds") and r.get("n")
    ]
    land_over_m = [
        r["n_landings"] / r["m"] for r in d1 if r.get("m") and r["n_landings"]
    ]

    return _py(
        {
            "attack": 11,
            "name": "adjacent_lattice_spheres",
            "ns_solved": False,
            "LemmaStar_killed": bool(rmax > 1e3),
            "d1": d1,
            "d2": d2,
            "d3": d3,
            "R_exponents_in_m": log_exponents(live, "m"),
            "Ds_exponents_in_n": log_exponents(live, "n", "Ds"),
            "land_exponents_in_m": log_exponents(
                [r for r in d1 if r.get("n_landings")], "m", "n_landings"
            ),
            "Rbox_max": rmax,
            "Ds_over_n": ds_over_n,
            "land_over_m": land_over_m,
            "verdict": "KILL_LemmaStar" if rmax > 1e3 else "ADJACENT_SPHERES_OPEN_bound_open",
            "note": (
                "Full spheres n, n+d. Ds is the gap. Landings O(m) not O(m^2). "
                "R★ falls. Finite n is not a kill. NS not solved."
            ),
        }
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--n-try", type=int, default=4)
    args = ap.parse_args()
    summary = run(n_try=args.n_try)
    print("\n=== ATTACK 11 SUMMARY ===", flush=True)
    slim = {k: v for k, v in summary.items() if k not in ("d1", "d2", "d3")}
    print(json.dumps(slim, indent=2), flush=True)
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2))
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
