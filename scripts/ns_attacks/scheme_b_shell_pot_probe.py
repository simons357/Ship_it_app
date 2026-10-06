"""SCHEME B probe: once-per-shell pot vs SCHEME A shape charging.

Frequency shells = exact |k|^2 sets (not physical).
Not a proof of (17). Standard library only.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
from math import isqrt, sqrt
from pathlib import Path
import json


def radius(k):
    return k[0] * k[0] + k[1] * k[1] + k[2] * k[2]


def lattice_shell(r2: int):
    R = isqrt(r2) + 1
    out = []
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            for z in range(-R, R + 1):
                if x * x + y * y + z * z == r2:
                    out.append((x, y, z))
    return out


def scalene_shapes_and_mode_incidence(rmax: int):
    """Enumerate admissible a<b<c and mode-level completion counts.

    For each oriented mode p on shell a, count distinct q on some shell b
    such that r=-(p+q) lands on a third distinct shell c, with a,b,c ≤ rmax
    and {a,b,c} pairwise distinct (scalene radius multiset).
    """
    shells = {r: lattice_shell(r) for r in range(1, rmax + 1)}
    shell_of = {}
    for r, pts in shells.items():
        for p in pts:
            shell_of[p] = r

    shapes = []
    shape_set = set()
    # shape-level touch counts
    touch = Counter()
    # mode-level: for each p, number of q giving a scalene completion
    mode_completion = {}
    # for fixed (a,c), how many partner shells b occur
    partners_ac = defaultdict(set)
    # oriented triple count per shape (finite incidence)
    oriented_per_shape = Counter()

    all_pts = [p for r in range(1, rmax + 1) for p in shells[r]]

    for a, b, c in combinations(range(1, rmax + 1), 3):
        sa, sb, sc = sqrt(a), sqrt(b), sqrt(c)
        if not (abs(sa - sb) <= sc <= sa + sb):
            continue
        if not (abs(sa - sc) <= sb <= sa + sc):
            continue
        if not (abs(sb - sc) <= sa <= sb + sc):
            continue
        found = 0
        for p in shells[a]:
            for q in shells[b]:
                r = (-(p[0] + q[0]), -(p[1] + q[1]), -(p[2] + q[2]))
                if radius(r) == c:
                    found += 1
        if found:
            shapes.append((a, b, c))
            shape_set.add((a, b, c))
            touch[a] += 1
            touch[b] += 1
            touch[c] += 1
            oriented_per_shape[(a, b, c)] = found

    # Mode completions: scan all ordered pairs of modes with distinct shells
    for p in all_pts:
        a = shell_of[p]
        count = 0
        partner_shells = set()
        for q in all_pts:
            b = shell_of[q]
            if b == a:
                continue
            r = (-(p[0] + q[0]), -(p[1] + q[1]), -(p[2] + q[2]))
            c = radius(r)
            if c < 1 or c > rmax or c == a or c == b:
                continue
            # enforce unordered a<b<c membership in shape_set
            triple = tuple(sorted((a, b, c)))
            if triple not in shape_set:
                continue
            count += 1
            partner_shells.add(b)
            partners_ac[(a, c)].add(b)
        mode_completion[p] = {
            "shell": a,
            "completions": count,
            "partner_shells": len(partner_shells),
        }

    return {
        "shapes": shapes,
        "touch": touch,
        "oriented_per_shape": oriented_per_shape,
        "mode_completion": mode_completion,
        "partners_ac": partners_ac,
        "shells": shells,
    }


def summarize(rmax: int):
    data = scalene_shapes_and_mode_incidence(rmax)
    shapes = data["shapes"]
    touch = data["touch"]
    oriented = data["oriented_per_shape"]
    mode_completion = data["mode_completion"]
    shells = data["shells"]

    # SCHEME A proxy: sum_shapes 1 (diverges) and sum_shapes 1/(a+b+c)
    sum_one = len(shapes)
    sum_inv_rate = sum(1.0 / (a + b + c) for a, b, c in shapes)
    sum_inv_rate2 = sum(1.0 / (a + b + c) ** 2 for a, b, c in shapes)
    sum_sqrtc_inv = sum(sqrt(c) / (a + b + c) for a, b, c in shapes)

    # SCHEME B proxy: charge each shell once with weight φ(a)=a^{3/2}
    # Compare "shape-charged" mass vs "shell-charged" mass under unit e_a=1.
    # Shape-charged cubic mass ~ sum_shapes √c (each e=1)
    shape_cubic = sum(sqrt(c) for a, b, c in shapes)
    # Degree-inflated shell charge (what SCHEME A secretly does if e_a=1):
    # sum_a touch(a) * a^{3/2}
    degree_inflated = sum(touch[a] * (a ** 1.5) for a in touch)
    # Once-per-shell pot: sum_a a^{3/2}
    once_shell = sum((a ** 1.5) for a in range(1, rmax + 1) if a in touch)
    # Energy-moment proxies with e_a=1/a^2 (heat-like / high-pass decay)
    e = {a: 1.0 / (a * a) for a in range(1, rmax + 1)}
    shape_cubic_decayed = sum(
        sqrt(c) * sqrt(e[a] * e[b] * e[c]) for a, b, c in shapes
    )
    once_shell_decayed = sum((a ** 1.5) * (e[a] ** 1.5) for a in touch)
    # Young shell pot: for each shape, split √(e_a e_b e_c) → (e^{3/2})/3 each
    young_shell = Counter()
    for a, b, c in shapes:
        w = sqrt(c) * sqrt(e[a] * e[b] * e[c])
        young_shell[a] += w / 3.0
        young_shell[b] += w / 3.0
        young_shell[c] += w / 3.0
    young_total = sum(young_shell.values())
    # Max multiplicity: how much one shell is over-asked vs its once pot face
    # once face for shell a under this e: a^{3/2} e_a^{3/2}
    overask = []
    for a in touch:
        face = (a ** 1.5) * (e[a] ** 1.5)
        asked = young_shell[a]
        overask.append((a, asked / face if face else None, touch[a]))

    # Mode incidence stats
    comps = [v["completions"] for v in mode_completion.values()]
    partner_shell_counts = [v["partner_shells"] for v in mode_completion.values()]
    # per-shell max mode completion
    max_comp_by_shell = {}
    for p, v in mode_completion.items():
        a = v["shell"]
        max_comp_by_shell[a] = max(max_comp_by_shell.get(a, 0), v["completions"])

    # Oriented triples: finite per shape — max / median
    ori_vals = list(oriented.values())

    most_shared = touch.most_common(8)
    busiest_modes = sorted(
        (
            (v["completions"], p, v["shell"], v["partner_shells"])
            for p, v in mode_completion.items()
        ),
        reverse=True,
    )[:8]

    return {
        "rmax": rmax,
        "scalene_shape_count": sum_one,
        "shells_touched": len(touch),
        "scheme_A_proxies": {
            "sum_shapes_1": sum_one,
            "sum_1_over_a_plus_b_plus_c": sum_inv_rate,
            "sum_1_over_rate_squared": sum_inv_rate2,
            "sum_sqrtc_over_rate": sum_sqrtc_inv,
            "shape_cubic_unit_e": shape_cubic,
            "degree_inflated_shell_mass_unit_e": degree_inflated,
            "status": (
                "These grow with #shapes / touch degrees — SCHEME A path."
            ),
        },
        "scheme_B_proxies": {
            "once_shell_mass_unit_e": once_shell,
            "ratio_degree_inflated_over_once_shell": (
                degree_inflated / once_shell if once_shell else None
            ),
            "shape_cubic_e_eq_1_over_a2": shape_cubic_decayed,
            "once_shell_pot_e_eq_1_over_a2": once_shell_decayed,
            "young_split_total_equals_shape_cubic_decayed": young_total,
            "young_equals_shape_check": abs(young_total - shape_cubic_decayed) < 1e-9,
            "note": (
                "Young split moves mass onto shells but still accumulates "
                "touch(a) contributions into young_shell[a]; without an "
                "exact-sphere regrouping, Young alone does NOT kill "
                "degree inflation. SCHEME B needs mode-level incidence, "
                "not post-hoc Young on shape sum."
            ),
            "worst_young_overask_vs_once_face": sorted(
                (
                    {
                        "shell": a,
                        "asked_over_once_face": ratio,
                        "shape_degree": deg,
                    }
                    for a, ratio, deg in overask
                    if ratio is not None
                ),
                key=lambda d: d["asked_over_once_face"],
                reverse=True,
            )[:8],
        },
        "shape_vs_mode_incidence": {
            "most_shared_shells_by_shape_degree": [
                {"shell": a, "shape_degree": d} for a, d in most_shared
            ],
            "mode_completions_max": max(comps) if comps else 0,
            "mode_completions_mean": (sum(comps) / len(comps) if comps else 0),
            "partner_shells_per_mode_max": (
                max(partner_shell_counts) if partner_shell_counts else 0
            ),
            "max_mode_completions_by_shell_top": sorted(
                (
                    {"shell": a, "max_mode_completions": m, "shape_degree": touch[a]}
                    for a, m in max_comp_by_shell.items()
                ),
                key=lambda d: d["max_mode_completions"],
                reverse=True,
            )[:8],
            "busiest_modes": [
                {
                    "completions": c,
                    "mode": list(p),
                    "shell": sh,
                    "partner_shells": ps,
                }
                for c, p, sh, ps in busiest_modes
            ],
            "oriented_triples_per_shape_max": max(ori_vals) if ori_vals else 0,
            "oriented_triples_per_shape_mean": (
                sum(ori_vals) / len(ori_vals) if ori_vals else 0
            ),
            "shell_cardinalities_sample": {
                str(a): len(shells[a]) for a in (1, 2, 5, 8, 9, 10, 13, 14, 17, 25)
                if a <= rmax
            },
        },
        "verdict": {
            "SCHEME_A": "FAILED — shape sums and degree-inflated shell mass grow with rmax",
            "naive_Young_split": (
                "INSUFFICIENT alone — still deposits touch(a) mass on each shell"
            ),
            "SCHEME_B_target": (
                "Regroup signed transfer at mode/exact-sphere level so each "
                "frequency shell e_a is charged O(1) times (like repeated-radius "
                "(11)), then Young against νY/4. Shape-degree charging forbidden."
            ),
            "status": "PROBE — not a proof of (17)",
        },
    }


def main():
    # Two cutoffs to see growth
    out = {
        "terminology": (
            "shell = exact |k|^2 Fourier set; not a physical shell or hole"
        ),
        "runs": [summarize(20), summarize(30)],
    }
    # Growth ratios 30 vs 20
    a, b = out["runs"][0], out["runs"][1]
    out["growth_20_to_30"] = {
        "shapes": b["scalene_shape_count"] / a["scalene_shape_count"],
        "sum_1_over_rate": (
            b["scheme_A_proxies"]["sum_1_over_a_plus_b_plus_c"]
            / a["scheme_A_proxies"]["sum_1_over_a_plus_b_plus_c"]
        ),
        "once_shell_unit_e": (
            b["scheme_B_proxies"]["once_shell_mass_unit_e"]
            / a["scheme_B_proxies"]["once_shell_mass_unit_e"]
        ),
        "degree_inflated": (
            b["scheme_A_proxies"]["degree_inflated_shell_mass_unit_e"]
            / a["scheme_A_proxies"]["degree_inflated_shell_mass_unit_e"]
        ),
        "mode_completions_max": (
            b["shape_vs_mode_incidence"]["mode_completions_max"]
            / max(1, a["shape_vs_mode_incidence"]["mode_completions_max"])
        ),
        "reading": (
            "If mode_completions_max grows much slower than shapes / "
            "degree_inflated, exact-sphere regrouping is the right SCHEME B "
            "lever. If it tracks shape degree, need a stronger weight."
        ),
    }
    path = Path(__file__).with_name("SCHEME-B-SHELL-POT-PROBE.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
