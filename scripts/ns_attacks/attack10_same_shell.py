#!/usr/bin/env python3
"""Attack 10 — same-shell coherent packet. Not a proof.

P,Q on one eigenvalue N, R on the most popular sum shell T.
Ds is the shell gap, not AP width. Eigenvalues do not spread with m.

If Tc ~ m^{1/2} with Ds Y staying O(1) (in m), Lemma★ is in trouble.
NS is not solved.
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
    integer_shell,
    probe,
    same_shell_packet_field,
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


def best_same_shell(N: int, m, rng: np.random.Generator, n_try: int = 6) -> dict:
    best = None
    shifts = (0.0, 0.5 * np.pi, np.pi, -0.5 * np.pi)
    configs = [(True, (0.2, 1.0, -0.3))]
    for i in range(n_try):
        seed = (0.2, 1.0, -0.3) if i == 0 else tuple(float(x) for x in rng.normal(size=3))
        configs.append((False, seed))
    for aligned, seed in configs:
        for sh in shifts:
            f, meta = same_shell_packet_field(
                N,
                m=m,
                pol_seed=seed,
                phase_r_shift=float(sh),
                aligned_pol=aligned,
            )
            r = probe(f, label=f"ss_{N}_{m}")
            rec = {
                **meta,
                "m": meta["n_P"],
                "aligned_pol": aligned,
                "ratio_box": float(r.ratio_box) if np.isfinite(r.ratio_box) else None,
                "Tc": float(r.Tc),
                "Ds": float(r.Ds),
                "E": float(r.E),
                "Y": float(r.Y),
                "Lambda": float(r.Lambda),
                "denom": float(r.Ds * r.E * r.Y) if r.Ds > 0 and r.E > 0 and r.Y > 0 else None,
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


def run(seed: int = 10, n_try: int = 6) -> dict:
    rng = np.random.Generator(np.random.PCG64(seed))
    N = 54  # |S|=96, rich same-shell
    S = integer_shell(N)
    print(f"shell N={N}  |S|={len(S)}", flush=True)

    m_rows = []
    for m in (6, 12, 18, 24, 36, 48, 72, None):
        row = best_same_shell(N, m, rng, n_try=n_try)
        if row:
            m_rows.append(row)
            print(
                f"N={N} m={row['m']:3d} shells={row['shells']} pairs={row['n_pairs']:4d}  "
                f"R★={row['ratio_box']:.4e} Tc={row['Tc']:.3e} Ds={row['Ds']:.3e} Y={row['Y']:.3e}",
                flush=True,
            )

    N_rows = []
    for Nv in (2, 5, 14, 18, 26, 41, 54, 90):
        row = best_same_shell(Nv, None, rng, n_try=max(3, n_try // 2))
        if row:
            N_rows.append(row)
            print(
                f"full N={Nv:3d} m={row['m']:3d} shells={row['shells']}  "
                f"R★={row['ratio_box']:.4e} Ds={row['Ds']:.3e}",
                flush=True,
            )

    f_rand, meta_rand = same_shell_packet_field(
        N, m=None, random_phases=True, aligned_pol=False, rng=rng
    )
    r_rand = probe(f_rand, label="ss_rand")
    random_row = {
        **meta_rand,
        "m": meta_rand["n_P"],
        "ratio_box": float(r_rand.ratio_box) if np.isfinite(r_rand.ratio_box) else None,
        "Tc": float(r_rand.Tc),
        "Ds": float(r_rand.Ds),
        "Y": float(r_rand.Y),
    }
    print(
        f"N={N} random-phase  R★={random_row['ratio_box']} Tc={random_row['Tc']:.3e}",
        flush=True,
    )

    rmax = 0.0
    for block in (m_rows, N_rows):
        for row in block:
            if row.get("ratio_box"):
                rmax = max(rmax, row["ratio_box"])

    ds_vals = [r["Ds"] for r in m_rows if r.get("Ds")]
    ds_flat = (
        max(ds_vals) / min(ds_vals) < 4.0 if len(ds_vals) >= 3 else None
    )

    return _py(
        {
            "attack": 10,
            "name": "same_shell_coherent_packet",
            "ns_solved": False,
            "LemmaStar_killed": bool(rmax > 1e3),
            "N_fixed": N,
            "m_sweep": m_rows,
            "N_sweep_full": N_rows,
            "random_phase_control": random_row,
            "m_exponents": log_exponents(m_rows, "m"),
            "Ds_exponents_in_m": log_exponents(m_rows, "m", "Ds"),
            "Tc_exponents_in_m": log_exponents(m_rows, "m", "Tc"),
            "Ds_roughly_flat_in_m": ds_flat,
            "Rbox_max": rmax,
            "verdict": "KILL_LemmaStar" if rmax > 1e3 else "SAME_SHELL_OPEN_bound_open",
            "note": (
                "Same-shell packet: Ds is the shell gap. AP width is off. "
                "Finite m is not a kill. NS not solved."
            ),
        }
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--n-try", type=int, default=6)
    args = ap.parse_args()
    summary = run(n_try=args.n_try)
    print("\n=== ATTACK 10 SUMMARY ===", flush=True)
    slim = {k: v for k, v in summary.items() if k not in ("m_sweep", "N_sweep_full")}
    print(json.dumps(slim, indent=2), flush=True)
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2))
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
