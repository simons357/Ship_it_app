#!/usr/bin/env python3
"""Attack 8 — three-shell closing triad. Exponents in e. Not a proof.

Family: k0 (carrier), k0+e, 2k0+e with k0+(k0+e)=2k0+e.
Two-shell (k0 and k0+e only) is not this test.

Hunt with |k0|^2 comparable to Λ. Additive e at large |k0| is not
the Attack-6 dilation (that one scales e too, and Λ scales as n^2).
Subleading Λ corrections are where a kill is most likely to hide.

NS is not solved. A bounded sample is not a uniform bound.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ns_attacks.stokes_moments import (  # noqa: E402
    k_norm2,
    probe,
    scale_field,
    three_shell_field,
    three_shell_keys,
    two_shell_shift_field,
)

ModeKey = Tuple[int, int, int]


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


def _rand_seed(rng: np.random.Generator) -> Tuple[float, float, float]:
    v = rng.normal(size=3)
    n = np.linalg.norm(v)
    if n < 1e-15:
        return (0.0, 1.0, 0.0)
    return tuple(float(x) for x in v / n)


def best_three_shell(
    k0: ModeKey,
    e: ModeKey,
    rng: np.random.Generator,
    n_phase: int = 16,
    amps: Sequence[float] = (0.05, 0.15, 0.4, 1.0),
) -> Optional[dict]:
    """Max R★ over relative off-shell amplitudes, phases, polarizations."""
    best = None
    phase_list: List[Tuple[float, float, float]] = [(0.0, 0.3, -0.2)]
    seeds_list = [
        ((0.0, 1.0, 0.2), (1.0, 0.0, 0.3), (0.2, 0.5, 1.0)),
    ]
    for _ in range(n_phase):
        phase_list.append(tuple(float(x) for x in rng.uniform(0, 2 * np.pi, size=3)))
        seeds_list.append((_rand_seed(rng), _rand_seed(rng), _rand_seed(rng)))
    a0 = 1.0
    k0k, k1, k2 = three_shell_keys(k0, e)
    kn0 = k_norm2(k0k)
    for amp1 in amps:
        for amp2 in amps:
            for ph, seeds in zip(phase_list, seeds_list):
                f = three_shell_field(
                    k0, e, amp0=a0, amp1=amp1, amp2=amp2, phases=ph, pol_seeds=seeds
                )
                r = probe(f, label=f"3s_{k0}_{e}")
                if not np.isfinite(r.ratio_box) or r.Ds <= 0:
                    continue
                rel_lam = abs(r.Lambda - kn0) / kn0 if kn0 > 0 else float("nan")
                rec = {
                    "k0": list(k0),
                    "e": list(e),
                    "k1": list(k1),
                    "k2": list(k2),
                    "|e|": float(math.sqrt(k_norm2(e))),
                    "|k0|": float(math.sqrt(kn0)),
                    "amp1": float(amp1),
                    "amp2": float(amp2),
                    "ratio_box": float(r.ratio_box),
                    "Tc": float(r.Tc),
                    "Ds": float(r.Ds),
                    "Lambda": float(r.Lambda),
                    "k0_shell": float(kn0),
                    "rel_Lambda_gap": float(rel_lam),
                    "near_threshold": bool(rel_lam < 0.35),
                    "E": float(r.E),
                    "Y": float(r.Y),
                }
                if best is None or rec["ratio_box"] > best["ratio_box"]:
                    best = rec
                # also track best among near-threshold samples
    return best


def best_three_shell_near_threshold(
    k0: ModeKey,
    e: ModeKey,
    rng: np.random.Generator,
    n_phase: int = 16,
    amps: Sequence[float] = (0.05, 0.15, 0.4, 1.0),
) -> Optional[dict]:
    """Same search, restricted to Λ within 35% of |k0|^2."""
    best = None
    phase_list: List[Tuple[float, float, float]] = [(0.0, 0.3, -0.2)]
    seeds_list = [
        ((0.0, 1.0, 0.2), (1.0, 0.0, 0.3), (0.2, 0.5, 1.0)),
    ]
    for _ in range(n_phase):
        phase_list.append(tuple(float(x) for x in rng.uniform(0, 2 * np.pi, size=3)))
        seeds_list.append((_rand_seed(rng), _rand_seed(rng), _rand_seed(rng)))
    kn0 = k_norm2(k0)
    for amp1 in amps:
        for amp2 in amps:
            for ph, seeds in zip(phase_list, seeds_list):
                f = three_shell_field(
                    k0, e, amp0=1.0, amp1=amp1, amp2=amp2, phases=ph, pol_seeds=seeds
                )
                r = probe(f)
                if not np.isfinite(r.ratio_box) or r.Ds <= 0:
                    continue
                rel_lam = abs(r.Lambda - kn0) / kn0 if kn0 > 0 else float("inf")
                if rel_lam >= 0.35:
                    continue
                rec = {
                    "k0": list(k0),
                    "e": list(e),
                    "amp1": float(amp1),
                    "amp2": float(amp2),
                    "ratio_box": float(r.ratio_box),
                    "Tc": float(r.Tc),
                    "Ds": float(r.Ds),
                    "Lambda": float(r.Lambda),
                    "rel_Lambda_gap": float(rel_lam),
                    "|e|": float(math.sqrt(k_norm2(e))),
                    "|k0|": float(math.sqrt(kn0)),
                }
                if best is None or rec["ratio_box"] > best["ratio_box"]:
                    best = rec
    return best


def two_shell_control(
    k0: ModeKey, e: ModeKey, rng: np.random.Generator, n_phase: int = 12
) -> dict:
    best_tc = 0.0
    best_box = None
    for _ in range(n_phase):
        ph = tuple(float(x) for x in rng.uniform(0, 2 * np.pi, size=2))
        seeds = (_rand_seed(rng), _rand_seed(rng))
        f = two_shell_shift_field(k0, e, amp0=1.0, amp1=0.2, phases=ph, pol_seeds=seeds)
        r = probe(f)
        if abs(r.Tc) > abs(best_tc):
            best_tc = float(r.Tc)
        if np.isfinite(r.ratio_box):
            if best_box is None or r.ratio_box > best_box:
                best_box = float(r.ratio_box)
    return {
        "k0": list(k0),
        "e": list(e),
        "max_|Tc|": abs(best_tc),
        "ratio_box": best_box,
    }


def frozen_three_shell(
    k0: ModeKey,
    e: ModeKey,
    amp1: float = 0.2,
    amp2: float = 0.05,
    phases: Tuple[float, float, float] = (0.0, 0.3, -0.2),
    pol_seeds: Tuple[Sequence[float], Sequence[float], Sequence[float]] = (
        (0.0, 1.0, 0.2),
        (1.0, 0.0, 0.3),
        (0.2, 0.5, 1.0),
    ),
) -> dict:
    """Fixed relative amplitudes and polarization. Only (k0, e) move."""
    f = three_shell_field(
        k0, e, amp0=1.0, amp1=amp1, amp2=amp2, phases=phases, pol_seeds=pol_seeds
    )
    r = probe(f)
    kn0 = k_norm2(k0)
    rel_lam = abs(r.Lambda - kn0) / kn0 if kn0 > 0 else float("nan")
    return {
        "k0": list(k0),
        "e": list(e),
        "|e|": float(math.sqrt(k_norm2(e))),
        "|k0|": float(math.sqrt(kn0)),
        "amp1": float(amp1),
        "amp2": float(amp2),
        "ratio_box": float(r.ratio_box) if np.isfinite(r.ratio_box) else None,
        "Tc": float(r.Tc),
        "Ds": float(r.Ds),
        "Lambda": float(r.Lambda),
        "k0_shell": float(kn0),
        "rel_Lambda_gap": float(rel_lam),
        "Y": float(r.Y),
        "E": float(r.E),
    }


def log_exponents(rows: List[dict], xkey: str, ykey: str = "ratio_box") -> List[dict]:
    out = []
    usable = [r for r in rows if r and r.get(ykey) and r[ykey] > 0 and r.get(xkey, 0) > 0]
    usable = sorted(usable, key=lambda r: r[xkey])
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
    out = []
    usable = [r for r in rows if r and r.get(ykey) and r[ykey] > 0 and r.get(xkey, 0) > 0]
    usable = sorted(usable, key=lambda r: r[xkey])
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


def run(seed: int = 8, n_phase: int = 12) -> dict:
    rng = np.random.Generator(np.random.PCG64(seed))
    k0_fixed: ModeKey = (6, 0, 0)

    two = two_shell_control(k0_fixed, (0, 1, 0), rng, n_phase=n_phase)

    e_rows = []
    e_thr = []
    for j in (1, 2, 3, 4, 6, 8):
        e: ModeKey = (0, j, 0)
        row = best_three_shell(k0_fixed, e, rng, n_phase=n_phase)
        thr = best_three_shell_near_threshold(k0_fixed, e, rng, n_phase=n_phase)
        if row:
            e_rows.append(row)
            print(
                f"e=(0,{j},0)  |e|={row['|e|']:.1f}  R★={row['ratio_box']:.4e}  "
                f"Λ-gap={row['rel_Lambda_gap']:.3f}  amp1={row['amp1']} amp2={row['amp2']}",
                flush=True,
            )
        if thr:
            e_thr.append(thr)
            print(
                f"  threshold  R★={thr['ratio_box']:.4e}  Λ-gap={thr['rel_Lambda_gap']:.3f}",
                flush=True,
            )

    # Additive e: k0 = (N,0,0), e = (0,1,0) fixed. Λ-dilation does not apply.
    add_rows = []
    add_thr = []
    for n in (2, 3, 4, 6, 8, 12, 16):
        k0: ModeKey = (n, 0, 0)
        e = (0, 1, 0)
        row = best_three_shell(k0, e, rng, n_phase=n_phase)
        thr = best_three_shell_near_threshold(k0, e, rng, n_phase=n_phase)
        if row:
            add_rows.append(row)
            print(
                f"additive N={n:2d}  R★={row['ratio_box']:.4e}  "
                f"Λ-gap={row['rel_Lambda_gap']:.3f}  |k0|={row['|k0|']:.1f}",
                flush=True,
            )
        if thr:
            add_thr.append(thr)

    # Dilated e: e = (0,N,0) with k0=(N,0,0). Whole configuration scales.
    dil_rows = []
    for n in (2, 3, 4, 6, 8):
        k0 = (n, 0, 0)
        e = (0, n, 0)
        row = best_three_shell(k0, e, rng, n_phase=n_phase)
        if row:
            dil_rows.append(row)
            print(
                f"dilated  N={n:2d}  R★={row['ratio_box']:.4e}  "
                f"Λ-gap={row['rel_Lambda_gap']:.3f}",
                flush=True,
            )

    # Frozen shape: exponents in e, not a fresh amp search at each e.
    frozen_e = []
    for j in (1, 2, 3, 4, 6, 8):
        row = frozen_three_shell(k0_fixed, (0, j, 0))
        frozen_e.append(row)
        print(
            f"frozen e=(0,{j},0)  R★={row['ratio_box']}  "
            f"Tc={row['Tc']:.3e} Ds={row['Ds']:.3e} Λ-gap={row['rel_Lambda_gap']:.3f}",
            flush=True,
        )
    frozen_par = []
    for j in (1, 2, 3, 4):
        row = frozen_three_shell(k0_fixed, (j, 0, 0))
        frozen_par.append(row)
        print(
            f"frozen e=({j},0,0)  R★={row['ratio_box']}  "
            f"Tc={row['Tc']:.3e} Λ-gap={row['rel_Lambda_gap']:.3f}",
            flush=True,
        )
    frozen_add = []
    for n in (2, 3, 4, 6, 8, 12, 16):
        row = frozen_three_shell((n, 0, 0), (0, 1, 0))
        frozen_add.append(row)
        print(
            f"frozen additive N={n:2d}  R★={row['ratio_box']}  "
            f"Λ-gap={row['rel_Lambda_gap']:.3f}",
            flush=True,
        )
    frozen_dil = []
    for n in (2, 3, 4, 6, 8, 12):
        row = frozen_three_shell((n, 0, 0), (0, n, 0))
        frozen_dil.append(row)
        print(
            f"frozen dilated  N={n:2d}  R★={row['ratio_box']}  "
            f"Λ-gap={row['rel_Lambda_gap']:.3f}",
            flush=True,
        )

    # Amplitude invariance on one three-shell field.
    f = three_shell_field((6, 0, 0), (0, 1, 0), amp0=1.0, amp1=0.2, amp2=0.2)
    r1 = probe(f)
    r10 = probe(scale_field(f, 10.0))

    e_exp = log_exponents(e_thr if e_thr else e_rows, "|e|")
    add_exp = log_exponents(add_thr if add_thr else add_rows, "|k0|")
    dil_exp = log_exponents(dil_rows, "|k0|")
    frozen_e_exp = log_exponents(
        [r for r in frozen_e if r.get("ratio_box")], "|e|"
    )
    frozen_par_exp = log_exponents(
        [r for r in frozen_par if r.get("ratio_box")], "|e|"
    )
    frozen_add_exp = log_exponents(
        [r for r in frozen_add if r.get("ratio_box")], "|k0|"
    )
    frozen_dil_exp = log_exponents(
        [r for r in frozen_dil if r.get("ratio_box")], "|k0|"
    )

    rmax = 0.0
    for block in (
        e_rows,
        e_thr,
        add_rows,
        add_thr,
        dil_rows,
        frozen_e,
        frozen_par,
        frozen_add,
        frozen_dil,
    ):
        for row in block:
            val = row.get("ratio_box")
            if val:
                rmax = max(rmax, val)

    killed = rmax > 1e6
    summary = {
        "attack": 8,
        "name": "three_shell_exponents_in_e",
        "ns_solved": False,
        "LemmaStar_killed": killed,
        "two_shell_control": two,
        "e_sweep_k0=(6,0,0)": e_rows,
        "e_sweep_near_threshold": e_thr,
        "e_exponents": e_exp,
        "additive_e_vs_N": add_rows,
        "additive_near_threshold": add_thr,
        "additive_exponents_in_|k0|": add_exp,
        "dilated_e_vs_N": dil_rows,
        "dilated_exponents_in_|k0|": dil_exp,
        "frozen_e_perp": frozen_e,
        "frozen_e_perp_exponents": frozen_e_exp,
        "frozen_e_parallel": frozen_par,
        "frozen_e_parallel_exponents": frozen_par_exp,
        "frozen_additive": frozen_add,
        "frozen_additive_exponents": frozen_add_exp,
        "frozen_dilated": frozen_dil,
        "frozen_dilated_exponents": frozen_dil_exp,
        "Rbox_max": rmax,
        "amplitude_Rbox_a1": float(r1.ratio_box) if np.isfinite(r1.ratio_box) else None,
        "amplitude_Rbox_a10": float(r10.ratio_box) if np.isfinite(r10.ratio_box) else None,
        "verdict": "KILL_LemmaStar" if killed else "FAMILY_BOUNDED_bound_open",
        "note": (
            "Three-shell closing triad is the first non-trivial family. "
            "Two-shell is not this test. Additive e at large |k0| is not "
            "Attack-6 dilation. Samples are evidence only. NS not solved."
        ),
    }
    return _py(summary)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--n-phase", type=int, default=12)
    args = ap.parse_args()
    summary = run(n_phase=args.n_phase)
    print("\n=== ATTACK 8 SUMMARY ===", flush=True)
    slim = {
        k: v
        for k, v in summary.items()
        if k
        not in (
            "e_sweep_k0=(6,0,0)",
            "e_sweep_near_threshold",
            "additive_e_vs_N",
            "additive_near_threshold",
            "dilated_e_vs_N",
            "frozen_e_perp",
            "frozen_e_parallel",
            "frozen_additive",
            "frozen_dilated",
        )
    }
    print(json.dumps(slim, indent=2), flush=True)
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2))
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
