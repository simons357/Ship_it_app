#!/usr/bin/env python3
"""9B growing-s campaign: combinatorial room + field constructions.

Live lane after the counting lock. Fixed s cannot unbound K (K≤16s).
This file asks whether K stays bounded as the input fan m and the
occupied output support s grow.

Not a proof of ★. Finite max K is not C0. NS is not solved.
Do not merge Attack 12 R_★ ∼ β/α with √K. Do not call this 9D.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ns_attacks.attack9b_exact_shell_K import (  # noqa: E402
    K_of_w,
    build_exact_shell_field,
    normalize_field,
    optimize_K_on_shell,
    random_shell_params,
    shells_up_to,
)
from ns_attacks.attack9b_output_counting import (  # noqa: E402
    cs_rows,
    random_exact_shell_w,
)
from ns_attacks.stokes_moments import ModeKey  # noqa: E402


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


def close_shell(pos: Sequence[ModeKey]) -> List[ModeKey]:
    out = set()
    for k in pos:
        out.add(tuple(k))
        out.add((-k[0], -k[1], -k[2]))
    return sorted(out)


def pair_census(alpha_full: Sequence[ModeKey], beta: int) -> Dict:
    """Representations p+q=k with |k|²=β. Combinatorial, no field."""
    S = [tuple(k) for k in alpha_full]
    Sset = set(S)
    m = len(S)
    counts: Dict[ModeKey, int] = {}
    for p in S:
        for q in S:
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            if k[0] * k[0] + k[1] * k[1] + k[2] * k[2] != beta:
                continue
            counts[k] = counts.get(k, 0) + 1
    s = len(counts)
    max_rep = max(counts.values()) if counts else 0
    total = sum(counts.values())
    return {
        "m": m,
        "s_geom": s,
        "max_rep": int(max_rep),
        "total_pairs": int(total),
        "pairs_le_m": bool(max_rep <= m),
        "K_cs_ceiling": float(16.0 * s) if s else 0.0,
        "mean_rep": float(total / s) if s else 0.0,
        # Heuristic room if every output sat at A(k)~E and s~m: K ≲ 16m.
        "heuristic_s_eq_m_room": float(16.0 * m),
    }


def combinatorial_census(
    kmax: int,
    max_pairs: int = 80,
) -> Dict:
    """Additive room on integer spheres. Cheap. No phases."""
    shells_pos = shells_up_to(kmax)
    shells_full = {a: close_shell(modes) for a, modes in shells_pos.items()}
    betas = sorted(shells_full)
    rows = []
    n_fail = 0
    for alpha, modes in sorted(shells_full.items()):
        if len(modes) < 2:
            continue
        for beta in betas:
            if beta == alpha:
                continue
            if beta > 4 * alpha:
                continue
            rec = pair_census(modes, int(beta))
            if rec["s_geom"] == 0:
                continue
            rec["alpha"] = int(alpha)
            rec["beta"] = int(beta)
            rec["n_pos"] = len(shells_pos[alpha])
            rec["beta_over_alpha"] = float(beta) / float(alpha)
            rows.append(rec)
            if not rec["pairs_le_m"]:
                n_fail += 1
            if len(rows) >= max_pairs and max_pairs > 0:
                # keep collecting a bit more on β=2α, then stop later
                pass

    # Prefer keeping all rows; max_pairs only trims the *reported* top list.
    def key_room(r):
        return (r["s_geom"], r["max_rep"], r["total_pairs"])

    rows_sorted = sorted(rows, key=key_room, reverse=True)
    by_s = defaultdict(list)
    by_m = defaultdict(list)
    for r in rows:
        by_s[r["s_geom"]].append(r["K_cs_ceiling"])
        by_m[r["m"]].append(r["K_cs_ceiling"])
    return {
        "kmax": int(kmax),
        "n_pairs_with_sums": len(rows),
        "n_fail_pairs_le_m": n_fail,
        "max_s_geom": max((r["s_geom"] for r in rows), default=0),
        "max_rep": max((r["max_rep"] for r in rows), default=0),
        "max_m": max((r["m"] for r in rows), default=0),
        "max_cs_ceiling": max((r["K_cs_ceiling"] for r in rows), default=0.0),
        "top": rows_sorted[: min(24, len(rows_sorted))],
        "beta_2alpha": [
            r
            for r in rows_sorted
            if abs(r["beta"] - 2 * r["alpha"]) < 1e-9
        ][:16],
        "note": (
            "s_geom is the number of β-keys that are sums, not the occupied "
            "s of a particular field. CS ceiling 16s_geom is room, not K."
        ),
    }


def plane_pos_modes(pos: Sequence[ModeKey]) -> List[ModeKey]:
    """Modes with a vanishing coordinate — more 2-D additive structure."""
    return [k for k in pos if k[0] == 0 or k[1] == 0 or k[2] == 0]


def high_rep_pos_modes(
    pos: Sequence[ModeKey],
    beta: int,
    m_target: int,
) -> List[ModeKey]:
    """Greedy: keep positive-half modes that participate in the most β-sums."""
    full = close_shell(pos)
    Sset = set(full)
    score = defaultdict(int)
    for p in full:
        for q in full:
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            if k[0] * k[0] + k[1] * k[1] + k[2] * k[2] != beta:
                continue
            score[p] += 1
            score[q] += 1
    ranked = sorted(pos, key=lambda k: (-score.get(k, 0), k))
    take = [k for k in ranked if score.get(k, 0) > 0][: max(m_target, 0)]
    if len(take) < 2:
        return list(pos[: min(m_target, len(pos))])
    return take


def locked_phase_w(modes: Sequence[ModeKey]) -> Dict:
    n = len(modes)
    if n < 2:
        return {}
    amps = np.ones(n)
    thetas = np.full(n, 0.25 * math.pi)
    phis = np.zeros(n)
    return normalize_field(build_exact_shell_field(modes, amps, thetas, phis))


def loglog_slope(pairs: Sequence[Tuple[float, float]]) -> Optional[float]:
    """Least-squares slope of log y vs log x. Needs ≥2 distinct x>0, y>0."""
    cleaned = [(x, y) for x, y in pairs if x > 0 and y > 0 and math.isfinite(y)]
    if len(cleaned) < 2:
        return None
    xs = np.log([p[0] for p in cleaned])
    ys = np.log([p[1] for p in cleaned])
    if float(np.max(xs) - np.min(xs)) < 1e-12:
        return None
    b, _a = np.polyfit(xs, ys, 1)
    return float(b)


def _best_per_x(rows: Sequence[Dict], xkey: str, ykey: str = "K") -> List[Tuple[float, float]]:
    buckets: Dict[float, float] = {}
    for r in rows:
        x = r.get(xkey)
        y = r.get(ykey)
        if x is None or y is None:
            continue
        if not (math.isfinite(x) and math.isfinite(y) and y >= 0 and x > 0):
            continue
        buckets[float(x)] = max(y, buckets.get(float(x), -1.0))
    return sorted(buckets.items())


def score_construction(
    modes: Sequence[ModeKey],
    beta: float,
    rng: np.random.Generator,
    n_random: int,
    n_opt_trials: int,
    n_opt_refine: int,
    tag: str,
) -> List[Dict]:
    rows: List[Dict] = []
    if len(modes) < 2:
        return rows

    def _stamp(rec: Dict, kind: str) -> Dict:
        rec = dict(rec)
        rec["construction"] = kind
        rec["tag"] = tag
        rec["n_pos"] = len(modes)
        rec["efficiency_vs_16s"] = (
            float(rec["K"] / (16.0 * rec["s"])) if rec.get("s") else None
        )
        return rec

    w0 = locked_phase_w(modes)
    if w0:
        rows.append(_stamp(cs_rows(w0, float(beta)), "locked_phase"))

    for t in range(n_random):
        w = random_exact_shell_w(modes, rng)
        rec = _stamp(cs_rows(w, float(beta)), "random")
        rec["trial"] = t
        rows.append(rec)

    if n_opt_trials > 0:
        alphas = {p[0] * p[0] + p[1] * p[1] + p[2] * p[2] for p in modes}
        alpha = int(next(iter(alphas))) if len(alphas) == 1 else None
        if alpha is not None:
            opt = optimize_K_on_shell(
                alpha,
                int(beta),
                modes,
                rng,
                n_trials=n_opt_trials,
                n_refine=n_opt_refine,
                max_modes=None,
            )
            if opt.get("has_params") and opt.get("modes"):
                from ns_attacks.attack9b_exact_shell_K import field_from_shell_params

                use = [tuple(m) for m in opt["modes"]]
                params = {k: np.asarray(v, dtype=float) for k, v in opt["params"].items()}
                w = normalize_field(field_from_shell_params(use, params))
                rec = _stamp(cs_rows(w, float(beta)), "optimized")
                rec["opt_K_reported"] = float(opt["K"])
                rows.append(rec)
    return rows


def field_campaign(
    rng: np.random.Generator,
    kmax: int = 10,
    n_random: int = 6,
    n_opt_trials: int = 16,
    n_opt_refine: int = 8,
    m_list: Sequence[int] = (2, 4, 8, 16),
) -> Dict:
    """Growing m and s on exact shells. Several constructions."""
    shells_pos = shells_up_to(kmax)
    shells_ext = shells_up_to(max(kmax + 4, int(2 * math.sqrt(max(shells_pos) or 1)) + 2))
    # Historic peak + β=2α series + a few high-frequency shells.
    wanted = [
        (1, 2),
        (2, 4),
        (4, 8),
        (5, 10),
        (8, 16),
        (9, 18),
        (10, 20),
        (13, 26),
        (4, 5),
        (5, 8),
        (8, 9),
        (5, 2),
        (8, 4),
        (9, 8),
    ]
    pairs = []
    for a, b in wanted:
        if a in shells_pos and b in shells_ext and len(shells_pos[a]) >= 2:
            pairs.append((a, b, shells_pos[a]))

    rows: List[Dict] = []
    for alpha, beta, pos in pairs:
        n = len(pos)
        m_targets = []
        for m in m_list:
            if 2 <= m <= n:
                m_targets.append(m)
        if n not in m_targets:
            m_targets.append(n)
        for m in m_targets:
            prefix = list(pos[:m])
            rows.extend(
                score_construction(
                    prefix,
                    float(beta),
                    rng,
                    n_random=n_random,
                    n_opt_trials=n_opt_trials,
                    n_opt_refine=n_opt_refine,
                    tag=f"prefix_m{m}_a{alpha}_b{beta}",
                )
            )
            plane = plane_pos_modes(pos)[:m]
            if len(plane) >= 2:
                rows.extend(
                    score_construction(
                        plane,
                        float(beta),
                        rng,
                        n_random=max(2, n_random // 2),
                        n_opt_trials=max(4, n_opt_trials // 2),
                        n_opt_refine=max(4, n_opt_refine // 2),
                        tag=f"plane_m{len(plane)}_a{alpha}_b{beta}",
                    )
                )
            greedy = high_rep_pos_modes(pos, int(beta), m)
            if len(greedy) >= 2:
                rows.extend(
                    score_construction(
                        greedy,
                        float(beta),
                        rng,
                        n_random=max(2, n_random // 2),
                        n_opt_trials=max(4, n_opt_trials // 2),
                        n_opt_refine=max(4, n_opt_refine // 2),
                        tag=f"highrep_m{len(greedy)}_a{alpha}_b{beta}",
                    )
                )

    n_fail_pairs = sum(1 for r in rows if not r.get("pairs_le_m", True))
    n_fail_cs = sum(1 for r in rows if not r.get("cs_ok", True))
    n_fail_16s = sum(1 for r in rows if not r.get("K_le_16s", True))

    def _max(key):
        vals = [r[key] for r in rows if r.get(key) is not None and math.isfinite(r[key])]
        return max(vals) if vals else None

    worst = max(rows, key=lambda r: r.get("K") or -1.0) if rows else {}
    by_s = _best_per_x(rows, "s")
    by_m = _best_per_x(rows, "m")
    slope_s = loglog_slope(by_s)
    slope_m = loglog_slope(by_m)

    constructions = sorted({r.get("construction") for r in rows})
    best_by_c = {}
    for c in constructions:
        sub = [r for r in rows if r.get("construction") == c]
        if not sub:
            continue
        br = max(sub, key=lambda r: r.get("K") or -1.0)
        best_by_c[c] = {
            "K": br.get("K"),
            "s": br.get("s"),
            "m": br.get("m"),
            "alpha": br.get("alpha"),
            "beta": br.get("beta"),
            "tag": br.get("tag"),
            "sqrt_K": br.get("sqrt_K"),
        }

    # Historic (4,8) slice — compare to 0.641 / 0.506.
    hist = [r for r in rows if r.get("alpha") == 4.0 and r.get("beta") == 8.0]
    hist_max = max((r["K"] for r in hist), default=None)

    return {
        "n_fields": len(rows),
        "n_pairs": len(pairs),
        "max_K": _max("K"),
        "max_s": _max("s"),
        "max_m": _max("m"),
        "max_sqrt_K": _max("sqrt_K"),
        "max_pairs_on_one_k": _max("max_pairs_on_one_k"),
        "max_efficiency_vs_16s": _max("efficiency_vs_16s"),
        "n_fail_pairs_le_m": n_fail_pairs,
        "n_fail_cs": n_fail_cs,
        "n_fail_K_le_16s": n_fail_16s,
        "worst": {
            "K": worst.get("K"),
            "s": worst.get("s"),
            "m": worst.get("m"),
            "alpha": worst.get("alpha"),
            "beta": worst.get("beta"),
            "construction": worst.get("construction"),
            "tag": worst.get("tag"),
            "sqrt_K": worst.get("sqrt_K"),
            "efficiency_vs_16s": worst.get("efficiency_vs_16s"),
        },
        "best_by_construction": best_by_c,
        "historic_4_8_max_K": hist_max,
        "best_K_by_s": [{"s": x, "K": y} for x, y in by_s],
        "best_K_by_m": [{"m": x, "K": y} for x, y in by_m],
        "loglog_slope_K_vs_s": slope_s,
        "loglog_slope_K_vs_m": slope_m,
        "rows": rows,
        "verdict": (
            "GROWING_S_SAMPLES_FINITE_NOT_C0"
            if n_fail_16s == 0 and n_fail_pairs == 0
            else "INEQUALITY_FAIL_check_implementation"
        ),
        "extrapolation": (
            "CS ceiling grows like s. Observed max K vs s is a sample "
            "slope, not a seated exponent. Do not cash a finite slope "
            "as C0 and do not cash a positive slope as a kill unless "
            "K is shown unbounded."
        ),
        "ns_solved": False,
        "lemma_star": "OPEN",
        "kill_lane": "LIVE",
    }


def run(
    seed: int = 1390,
    kmax_census: int = 16,
    kmax_fields: int = 10,
    n_random: int = 6,
    n_opt_trials: int = 16,
    n_opt_refine: int = 8,
    m_list: Sequence[int] = (2, 4, 8, 16),
) -> Dict:
    rng = np.random.default_rng(seed)
    census = combinatorial_census(kmax_census)
    fields = field_campaign(
        rng,
        kmax=kmax_fields,
        n_random=n_random,
        n_opt_trials=n_opt_trials,
        n_opt_refine=n_opt_refine,
        m_list=m_list,
    )
    return {
        "attack": "9B-growing-s",
        "seed": seed,
        "census": census,
        "fields": {k: v for k, v in fields.items() if k != "rows"},
        "field_rows": fields["rows"],
        "verdict": fields["verdict"],
        "ns_solved": False,
        "lemma_star": "OPEN",
        "kill_lane": "LIVE",
        "note": (
            "Growing m and s on the same B(w,w) as the exact-shell / HH→L fan. "
            "Not a 9D object. Finite max K is not C0. Attack 12 R_★ is a "
            "different quotient. NS not solved."
        ),
    }


def write_headline(summary: Dict, path: Path) -> None:
    f = summary["fields"]
    c = summary["census"]
    w = f.get("worst") or {}
    lines = [
        "# Attack 9B — growing-s campaign",
        "",
        "**Lane:** 9B uniform target. **Not 9D.**",
        "**NS solved:** false",
        "**Lemma★:** OPEN",
        "**Kill lane:** LIVE",
        f"**verdict:** {summary['verdict']}",
        "",
        "## Combinatorial room (no field)",
        "",
        f"- kmax = {c.get('kmax')}",
        f"- pairs with sums = {c.get('n_pairs_with_sums')}",
        f"- max s_geom = {c.get('max_s_geom')}",
        f"- max representations on one k = {c.get('max_rep')}",
        f"- max CS ceiling 16 s_geom = {c.get('max_cs_ceiling')}",
        f"- pairs-per-output ≤ m failures = {c.get('n_fail_pairs_le_m')}",
        "",
        r"Room is not K. \(K\le 16s\) still sits.",
        "",
        "## Fields",
        "",
        f"- n_fields = {f.get('n_fields')}",
        f"- max K = {f.get('max_K')}",
        f"- max √K = {f.get('max_sqrt_K')}",
        f"- max s = {f.get('max_s')}",
        f"- max m = {f.get('max_m')}",
        f"- max efficiency K/(16s) = {f.get('max_efficiency_vs_16s')}",
        f"- loglog slope K vs s = {f.get('loglog_slope_K_vs_s')}",
        f"- loglog slope K vs m = {f.get('loglog_slope_K_vs_m')}",
        f"- historic (4,8) max K on this sweep = {f.get('historic_4_8_max_K')}",
        f"- worst: {w}",
        "",
        r"Finite max is not \(C_0\). A sample slope is not a seated exponent.",
        r"Do not merge \(\sqrt{K}\) with Attack 12 \(\mathcal R_\star\).",
        "NS not solved.",
        "",
    ]
    path.write_text("\n".join(lines))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--headline", type=str, default="")
    ap.add_argument("--seed", type=int, default=1390)
    ap.add_argument("--kmax-census", type=int, default=16)
    ap.add_argument("--kmax-fields", type=int, default=10)
    ap.add_argument("--n-random", type=int, default=6)
    ap.add_argument("--opt-trials", type=int, default=16)
    ap.add_argument("--opt-refine", type=int, default=8)
    args = ap.parse_args()
    summary = run(
        seed=args.seed,
        kmax_census=args.kmax_census,
        kmax_fields=args.kmax_fields,
        n_random=args.n_random,
        n_opt_trials=args.opt_trials,
        n_opt_refine=args.opt_refine,
    )
    slim = {k: v for k, v in summary.items() if k != "field_rows"}
    print(json.dumps(_py(slim), indent=2), flush=True)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(_py(summary), indent=2))
        print(f"wrote {args.out}", flush=True)
    if args.headline:
        Path(args.headline).parent.mkdir(parents=True, exist_ok=True)
        write_headline(_py(summary), Path(args.headline))
        print(f"wrote {args.headline}", flush=True)
    return 0 if summary["verdict"].startswith("GROWING_S") else 1


if __name__ == "__main__":
    raise SystemExit(main())
