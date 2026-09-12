#!/usr/bin/env python3
"""Growing input and output support on the 9B family.

Same B as 9B. Target ||Π_β B||₂ ≤ C (α/√β) ||w||₂²  iff  sup K < ∞.
Fixed-output Θ(m²) excluded (K ≤ 16s). Designed 9D stub is not this script.

Full complex polarizations. Frequency factors kept.
A finite max K is not C0. R_★ → ∞ would kill ★.
NS is not solved. Lemma★ OPEN. Kill lane LIVE.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ns_attacks.attack9b_exact_shell_K import shells_up_to  # noqa: E402
from ns_attacks.attack9b_output_counting import (  # noqa: E402
    cs_rows,
    random_exact_shell_w,
)
from ns_attacks.stokes_moments import k_norm2, nonlinear_B  # noqa: E402


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


def input_sizes(n_pos: int) -> List[int]:
    out: List[int] = []
    for m in (2, 4, 8, 16, 24, n_pos):
        if 2 <= m <= n_pos and m not in out:
            out.append(m)
    return out


def occupied_betas(Buu: Dict, alpha: int, tol: float = 1e-14) -> List[int]:
    """Output shells that B actually hits. β ≤ 4α, β ≠ α. Empty shells skipped."""
    seen = set()
    for k, vec in Buu.items():
        if float(np.linalg.norm(vec)) <= tol:
            continue
        beta = int(k_norm2(k))
        if beta != alpha and beta <= 4 * alpha:
            seen.add(beta)
    return sorted(seen)


def grow_sweep(
    rng: np.random.Generator,
    kmax: int = 8,
    n_trials: int = 4,
) -> Dict:
    shells = shells_up_to(kmax)
    rows = []
    worst = {"K": -1.0}
    n_fields_w = 0

    for alpha, modes_pos in sorted(shells.items()):
        n_pos = len(modes_pos)
        if n_pos < 2:
            continue
        for m in input_sizes(n_pos):
            for t in range(n_trials):
                if m == n_pos:
                    use = list(modes_pos)
                else:
                    pick = rng.choice(n_pos, size=m, replace=False)
                    use = [modes_pos[int(i)] for i in pick]
                w = random_exact_shell_w(use, rng)
                Buu = nonlinear_B(w)
                n_fields_w += 1
                betas = occupied_betas(Buu, int(alpha))
                if not betas:
                    continue
                for beta in betas:
                    rec = cs_rows(w, float(beta), Buu=Buu)
                    rec["trial"] = t
                    rec["m_requested"] = int(m)
                    rec["n_pos_shell"] = n_pos
                    rec["kmax"] = kmax
                    rows.append(rec)
                    if rec["K"] == rec["K"] and rec["K"] > worst["K"]:
                        worst = {
                            "K": rec["K"],
                            "sqrt_K": rec["sqrt_K"],
                            "alpha": rec["alpha"],
                            "beta": rec["beta"],
                            "s": rec["s"],
                            "m": rec["m"],
                        }

    def _vals(key):
        return [
            r[key]
            for r in rows
            if r.get(key) is not None and isinstance(r[key], (int, float)) and math.isfinite(r[key])
        ]

    def _max(key):
        v = _vals(key)
        return max(v) if v else None

    by_s: Dict[int, float] = {}
    for r in rows:
        if not math.isfinite(r.get("K", float("nan"))):
            continue
        s = int(r["s"])
        by_s[s] = max(by_s.get(s, -1.0), float(r["K"]))
    s_curve = [{"s": s, "max_K": by_s[s]} for s in sorted(by_s)]

    n_fail_pairs = sum(1 for r in rows if not r["pairs_le_m"])
    n_fail_cs = sum(1 for r in rows if not r["cs_ok"])
    n_fail_16s = sum(1 for r in rows if not r["K_le_16s"])
    ks = [r["K"] / r["s"] for r in rows if r["s"] > 0 and math.isfinite(r["K"])]
    return {
        "n_fields": len(rows),
        "n_input_fields": n_fields_w,
        "kmax": kmax,
        "n_trials": n_trials,
        "max_K": _max("K"),
        "max_s": _max("s"),
        "max_m": _max("m"),
        "max_sqrt_K": _max("sqrt_K"),
        "max_K_over_s": max(ks) if ks else None,
        "max_pairs_on_one_k": _max("max_pairs_on_one_k"),
        "max_cs_ratio": _max("cs_max_|B|/(|k|E)"),
        "n_fail_pairs_le_m": n_fail_pairs,
        "n_fail_cs": n_fail_cs,
        "n_fail_K_le_16s": n_fail_16s,
        "worst": worst,
        "K_vs_s": s_curve,
        "analytic": {
            "pairs_per_output_at_most_m": True,
            "K_le_16s_if_beta_le_4alpha": True,
            "fixed_s_cannot_unbound_K": True,
            "designed_theta_m2_9d": "DEAD",
            "correct_target": "||Π_β B||_2 ≤ C (α/√β) ||w||_2^2  iff  sup K < ∞",
        },
        "verdict": (
            "GROW_S_SAMPLES_FINITE_NOT_C0"
            if n_fail_16s == 0 and n_fail_pairs == 0 and n_fail_cs == 0
            else "INEQUALITY_FAIL_check_implementation"
        ),
        "ns_solved": False,
        "lemma_star": "KILLED",
        "kill_lane": "CLOSED_BY_V_N",
        "rows": rows,
    }


def run(seed: int = 1390, kmax: int = 8, n_trials: int = 4) -> Dict:
    rng = np.random.default_rng(seed)
    sweep = grow_sweep(rng, kmax=kmax, n_trials=n_trials)
    return {
        "attack": "9B-grow-s",
        "name": "growing input and output support on the 9B family",
        "not": "designed Θ(m²) 9D / attack9d_theta_m2_locked_phase.py",
        "seed": seed,
        "growing": {k: v for k, v in sweep.items() if k != "rows"},
        "growing_rows": sweep["rows"],
        "verdict": sweep["verdict"],
        "ns_solved": False,
        "lemma_star": "KILLED",
        "kill_lane": "CLOSED_BY_V_N",
        "note": (
            "Fixed-s excluded: K≤16s. Designed 9D dead. "
            "Growing m and s, complex pol, |k| kept. "
            "Finite max K is not C0. This sweep is historical. "
            "Unrestricted ★ killed by v_n. NS not solved."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--seed", type=int, default=1390)
    ap.add_argument("--kmax", type=int, default=8)
    ap.add_argument("--n-trials", type=int, default=4)
    args = ap.parse_args()
    summary = run(seed=args.seed, kmax=args.kmax, n_trials=args.n_trials)
    slim = {k: v for k, v in summary.items() if k != "growing_rows"}
    print(json.dumps(_py(slim), indent=2), flush=True)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(_py(slim), indent=2))
        print(f"wrote {args.out}", flush=True)
    return 0 if summary["verdict"].startswith("GROW_S") else 1


if __name__ == "__main__":
    raise SystemExit(main())
