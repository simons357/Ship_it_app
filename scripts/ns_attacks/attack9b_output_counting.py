#!/usr/bin/env python3
"""9B output counting: Θ(m²) on one k is impossible; K ≤ 16s.

Analytic lock, plus a growing-s complex-pol sweep on exact shells.
Does not prove ★. NS is not solved. Kill lane stays LIVE if s grows
and K stays bounded on samples — that is not a uniform C0.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ns_attacks.attack9b_exact_shell_K import (  # noqa: E402
    K_of_w,
    build_exact_shell_field,
    field_l2,
    normalize_field,
    project_B_to_shell,
    random_shell_params,
    shells_up_to,
)
from ns_attacks.stokes_moments import (  # noqa: E402
    Field,
    ModeKey,
    k_norm2,
    nonlinear_B,
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


def ordered_pairs_onto_k(support: Sequence[ModeKey], k: ModeKey) -> int:
    """Number of ordered (p,q) in supp×supp with p+q=k. At most m, not Θ(m²)."""
    S = set(support)
    n = 0
    for p in S:
        q = (k[0] - p[0], k[1] - p[1], k[2] - p[2])
        if q in S:
            n += 1
    return n


def max_pairs_per_output(support: Sequence[ModeKey]) -> Tuple[int, int]:
    S = list(support)
    m = len(S)
    best = 0
    for p in S:
        for q in S:
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            best = max(best, ordered_pairs_onto_k(S, k))
    return best, m


def cs_rows(w: Field, beta: float, tol: float = 1e-14) -> Dict:
    """Check |B̂_k| ≤ |k| ||w||₂² on shell β; count occupied outputs s."""
    w = normalize_field(w)
    e = field_l2(w) ** 2
    Buu = nonlinear_B(w)
    PiB = project_B_to_shell(Buu, beta)
    occupied = []
    max_ratio = 0.0
    cs_ok = True
    for k, vec in PiB.items():
        amp = float(np.linalg.norm(vec))
        if amp <= tol:
            continue
        kn = math.sqrt(k_norm2(k))
        bound = kn * e
        ratio = amp / bound if bound > 0 else float("inf")
        max_ratio = max(max_ratio, ratio)
        if amp > bound + 1e-9:
            cs_ok = False
        occupied.append(
            {
                "k": list(k),
                "B_abs": amp,
                "pairs": ordered_pairs_onto_k(list(w.keys()), k),
            }
        )
    s = len(occupied)
    max_pairs = max((row["pairs"] for row in occupied), default=0)
    alphas = {k_norm2(k) for k in w}
    if len(alphas) != 1:
        alpha = float("nan")
    else:
        alpha = float(next(iter(alphas)))
    info = K_of_w(w, float(alpha), beta) if alpha == alpha else {"K": float("nan"), "PiB_L2": 0.0}
    s_bound = s * (beta ** 2) / (alpha ** 2) if alpha > 0 else float("nan")
    return {
        "alpha": float(alpha),
        "beta": float(beta),
        "m": len(w),
        "s": s,
        "max_pairs_on_one_k": int(max_pairs),
        "pairs_le_m": bool(max_pairs <= len(w) + 0),
        "K": float(info["K"]),
        "PiB_L2": float(info["PiB_L2"]),
        "K_le_s_beta2_over_alpha2": bool(
            not math.isfinite(info["K"]) or info["K"] <= s_bound + 1e-8
        ),
        "K_le_16s": bool(not math.isfinite(info["K"]) or info["K"] <= 16.0 * s + 1e-8),
        "s_beta2_over_alpha2": float(s_bound) if math.isfinite(s_bound) else None,
        "cs_max_|B|/(|k|E)": float(max_ratio),
        "cs_ok": bool(cs_ok and max_ratio <= 1.0 + 1e-9),
        "correct_target_ratio": (
            float(info["PiB_L2"] * math.sqrt(beta) / alpha)
            if alpha > 0
            else None
        ),
        # ||ΠB||₂ / (α/√β ||w||₂²) = √K when ||w||₂=1
        "sqrt_K": float(math.sqrt(max(info["K"], 0.0))),
    }


def random_exact_shell_w(
    modes: Sequence[ModeKey],
    rng: np.random.Generator,
) -> Field:
    params = random_shell_params(len(modes), rng)
    return normalize_field(
        build_exact_shell_field(modes, params["amps"], params["thetas"], params["phis"])
    )


def growing_sweep(
    rng: np.random.Generator,
    n_trials: int = 12,
    m_list: Sequence[int] = (2, 4, 8, 12),
) -> Dict:
    """Complex pol, growing input fan on α, measure s and K on β=2α when present."""
    shells = shells_up_to(8)
    shells_ext = shells_up_to(12)
    pairs = []
    for alpha, modes in sorted(shells.items()):
        beta = 2 * alpha
        if beta not in shells_ext:
            continue
        if len(modes) < 2:
            continue
        pairs.append((alpha, beta, modes))
        if len(pairs) >= 6:
            break

    rows = []
    worst = {"K": -1.0}
    for alpha, beta, modes_pos in pairs:
        if beta not in shells_ext:
            continue
        for m in m_list:
            use = list(modes_pos[: min(m, len(modes_pos))])
            if len(use) < 2:
                continue
            for t in range(n_trials):
                w = random_exact_shell_w(use, rng)
                rec = cs_rows(w, float(beta))
                rec["trial"] = t
                rec["m_requested"] = int(m)
                rec["n_pos"] = len(use)
                rows.append(rec)
                if rec["K"] > worst["K"]:
                    worst = {
                        "K": rec["K"],
                        "alpha": rec["alpha"],
                        "beta": rec["beta"],
                        "s": rec["s"],
                        "m": rec["m"],
                        "sqrt_K": rec["sqrt_K"],
                    }

    def _max(key, pred=None):
        vals = [
            r[key]
            for r in rows
            if r.get(key) is not None and math.isfinite(r[key]) and (pred is None or pred(r))
        ]
        return max(vals) if vals else None

    n_fail_pairs = sum(1 for r in rows if not r["pairs_le_m"])
    n_fail_cs = sum(1 for r in rows if not r["cs_ok"])
    n_fail_16s = sum(1 for r in rows if not r["K_le_16s"])
    return {
        "n_fields": len(rows),
        "max_K": _max("K"),
        "max_s": _max("s"),
        "max_sqrt_K": _max("sqrt_K"),
        "max_pairs_on_one_k": _max("max_pairs_on_one_k"),
        "max_cs_ratio": _max("cs_max_|B|/(|k|E)"),
        "n_fail_pairs_le_m": n_fail_pairs,
        "n_fail_cs": n_fail_cs,
        "n_fail_K_le_16s": n_fail_16s,
        "worst": worst,
        "rows": rows,
        "analytic": {
            "pairs_per_output_at_most_m": True,
            "K_le_16s_if_beta_le_4alpha": True,
            "fixed_s_cannot_unbound_K": True,
            "correct_target": "||Π_β B||_2 ≤ C (α/√β) ||w||_2^2  iff  sup K < ∞",
            "wrong_target": "||Π_β B||_2 ≤ C α ||w||_2^2 leaves K ≲ β",
        },
        "verdict": (
            "FIXED_S_EXCLUDED_growing_s_samples_finite_NOT_proof"
            if n_fail_16s == 0 and n_fail_pairs == 0
            else "INEQUALITY_FAIL_check_implementation"
        ),
        "ns_solved": False,
        "lemma_star": "OPEN",
        "kill_lane": "LIVE",
    }


def run(seed: int = 1390, n_trials: int = 12) -> Dict:
    rng = np.random.default_rng(seed)
    # Unit identities on the original 9B peak shell pair α=4, β=8, 3-axis modes
    modes = [(2, 0, 0), (0, 2, 0), (0, 0, 2)]
    w = random_exact_shell_w(modes, rng)
    ident = cs_rows(w, 8.0)
    pairs_max, m = max_pairs_per_output(list(w.keys()))
    sweep = growing_sweep(rng, n_trials=n_trials)
    return {
        "attack": "9B-counting",
        "seed": seed,
        "identity_check_alpha4_beta8": ident,
        "max_pairs_global_on_that_field": pairs_max,
        "m_on_that_field": m,
        "pairs_at_most_m": bool(pairs_max <= m),
        "growing": {k: v for k, v in sweep.items() if k != "rows"},
        "growing_rows": sweep["rows"],
        "verdict": sweep["verdict"],
        "ns_solved": False,
        "lemma_star": "OPEN",
        "note": (
            "Fixed-s 9D excluded: K≤16s. Growing s remains the 9B kill shape. "
            "Finite max √K on this sweep is not C0. NS not solved."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--seed", type=int, default=1390)
    ap.add_argument("--n-trials", type=int, default=12)
    args = ap.parse_args()
    summary = run(seed=args.seed, n_trials=args.n_trials)
    slim = {k: v for k, v in summary.items() if k != "growing_rows"}
    print(json.dumps(_py(slim), indent=2), flush=True)
    if args.out:
        Path(args.out).write_text(json.dumps(_py(summary), indent=2))
        print(f"wrote {args.out}", flush=True)
    return 0 if summary["verdict"].startswith("FIXED_S") else 1


if __name__ == "__main__":
    raise SystemExit(main())
