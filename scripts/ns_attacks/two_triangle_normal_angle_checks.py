"""Two-triangle snapshot: ρ₂ vs angle between triangle normals e₂.

Asks whether the 1/√2 assembled-vs-absolute improvement on a genuine
HH→L sharing pair is robust, or specific to orthogonal e₂ geometry.

Standard library only. Exact fractions for the geometric model;
integer-lattice scans for concrete HH→L pairs. Not a class bound.
Not (17). Not Need★ as a proved estimate.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from math import acos, cos, isqrt, pi, sqrt
from pathlib import Path
import json


def rho_geometric(cos_theta: F) -> F:
    """Equal-amplitude aligned phases: |n+n'|/(2) with unit normals, n·n'=cos θ.
    ρ = sqrt((1+cos θ)/2) = |cos(θ/2)|.
    """
    return (F(1) + cos_theta) / 2  # return ρ² for exactness; caller takes sqrt


def unit_cross(p, q):
    c = (
        p[1] * q[2] - p[2] * q[1],
        p[2] * q[0] - p[0] * q[2],
        p[0] * q[1] - p[1] * q[0],
    )
    n2 = c[0] * c[0] + c[1] * c[1] + c[2] * c[2]
    if n2 == 0:
        return None, 0
    return c, n2


def cos_between(n, n2, m, m2) -> float:
    dot = n[0] * m[0] + n[1] * m[1] + n[2] * m[2]
    # oriented normals: take absolute cosine (undirected plane angle)
    return abs(dot) / sqrt(n2 * m2)


def lattice_hh_to_l_pairs(alpha_max: int = 40, beta_max: int = 40):
    """Equal-input HH→L: |p|²=|q|²=α, |k|²=β, p+q=k, 0<β<4α.
    Group by output k; for each pair of distinct input legs, record e₂ angle
    and assembled ρ = |e₂+e₂'| / 2 for unit normals (equal channel weights).
    """
    # precompute lattice points by radius squared
    by_r: dict[int, list[tuple[int, int, int]]] = {}
    R = isqrt(max(alpha_max, beta_max)) + 2
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            for z in range(-R, R + 1):
                r2 = x * x + y * y + z * z
                if 0 < r2 <= max(alpha_max, beta_max):
                    by_r.setdefault(r2, []).append((x, y, z))

    rows = []
    for beta, ks in by_r.items():
        if beta > beta_max:
            continue
        for alpha, ps in by_r.items():
            if alpha > alpha_max or not (0 < beta < 4 * alpha):
                continue
            # For each k, collect admissible p with |p|²=α, |k-p|²=α
            for k in ks:
                legs = []
                for p in ps:
                    q = (k[0] - p[0], k[1] - p[1], k[2] - p[2])
                    if q[0] * q[0] + q[1] * q[1] + q[2] * q[2] != alpha:
                        continue
                    # ordered pair: keep p lexicographic ≤ q to avoid double
                    if p > q:
                        continue
                    n, n2 = unit_cross(p, q)
                    if n is None:
                        continue
                    legs.append({"p": p, "q": q, "n": n, "n2": n2})
                if len(legs) < 2:
                    continue
                for a, b in combinations(legs, 2):
                    # skip if same unordered leg set
                    if {a["p"], a["q"]} == {b["p"], b["q"]}:
                        continue
                    cth = cos_between(a["n"], a["n2"], b["n"], b["n2"])
                    # equal weights: V = n_hat + n_hat'
                    # |V| = sqrt(2+2 cos φ) where cos φ = n·n' (signed);
                    # use undirected plane angle via |cos|
                    rho = sqrt(max(0.0, (1.0 + cth) / 2.0))  # |cos(θ/2)| with cosθ=|n·n'|
                    # Also the signed-normal version (oriented e₂):
                    dot_s = (
                        a["n"][0] * b["n"][0]
                        + a["n"][1] * b["n"][1]
                        + a["n"][2] * b["n"][2]
                    )
                    cos_signed = dot_s / sqrt(a["n2"] * b["n2"])
                    rho_signed = sqrt(max(0.0, (1.0 + cos_signed) / 2.0))
                    rows.append(
                        {
                            "alpha": alpha,
                            "beta": beta,
                            "k": k,
                            "leg_a": [a["p"], a["q"]],
                            "leg_b": [b["p"], b["q"]],
                            "cos_abs": cth,
                            "rho_undirected_planes": rho,
                            "cos_oriented": cos_signed,
                            "rho_oriented_normals": rho_signed,
                            "theta_abs_deg": acos(min(1.0, max(0.0, cth))) * 180.0 / pi,
                        }
                    )
    return rows


def main():
    # Exact geometric model: ρ² = (1+cos θ)/2
    geo = []
    samples = [
        ("orthogonal", F(0)),
        ("cos=1/2 (60°)", F(1, 2)),
        ("cos=3/4", F(3, 4)),
        ("cos=15/16", F(15, 16)),
        ("cos=255/256", F(255, 256)),
        ("parallel", F(1)),
    ]
    for name, cth in samples:
        r2 = rho_geometric(cth)
        geo.append(
            {
                "case": name,
                "cos_theta": str(cth),
                "rho_squared": str(r2),
                "rho": sqrt(float(r2)),
                "one_over_sqrt2": 1.0 / sqrt(2.0),
            }
        )

    rows = lattice_hh_to_l_pairs(alpha_max=50, beta_max=40)
    # classify by undirected plane angle ( |n·n'| )
    orth = [r for r in rows if abs(r["cos_abs"]) < 1e-12]
    near_par_planes = [r for r in rows if r["cos_abs"] >= 0.95]
    mid = [r for r in rows if 0.2 < r["cos_abs"] < 0.8]
    # oriented: nearly parallel vs nearly antiparallel channel normals
    near_par_oriented = [r for r in rows if r["cos_oriented"] >= 0.95]
    near_anti_oriented = [r for r in rows if r["cos_oriented"] <= -0.95]

    near_par_sorted = sorted(rows, key=lambda r: -r["cos_abs"])[:12]
    near_par_oriented_top = sorted(rows, key=lambda r: -r["cos_oriented"])[:8]
    near_anti_oriented_top = sorted(rows, key=lambda r: r["cos_oriented"])[:8]
    orth_examples = orth[:8]
    orth_oriented = [r for r in rows if abs(r["cos_oriented"]) < 1e-12][:8]

    payload = {
        "scope": (
            "Two-triangle HH→L snapshot: assembled equal-weight channel "
            "ρ=|e2+e2'|/2 vs angle between triangle normals. "
            "Not Need★ proved. Not (17). Not occupancy census."
        ),
        "geometric_identity": {
            "formula": "rho = sqrt((1+cos θ)/2) = |cos(θ/2)| for equal amplitudes, phases that align the channel scalars",
            "samples": geo,
            "conclusion": (
                "At orthogonal normals (θ=π/2) one gets exactly 1/√2. "
                "As oriented normals become parallel (θ→0), ρ→1 and the 1/√2 improvement disappears. "
                "As oriented normals become antiparallel (θ→π), ρ→0 (stronger cancellation)."
            ),
        },
        "lattice_scan": {
            "alpha_max": 50,
            "beta_max": 40,
            "pair_count": len(rows),
            "orthogonal_undirected_count": len(orth),
            "near_parallel_planes_cos_abs_ge_0.95_count": len(near_par_planes),
            "near_parallel_oriented_cos_ge_0.95_count": len(near_par_oriented),
            "near_antiparallel_oriented_cos_le_-0.95_count": len(near_anti_oriented),
            "mid_angle_count": len(mid),
            "orthogonal_examples": orth_examples,
            "orthogonal_oriented_examples": orth_oriented,
            "near_parallel_planes_top": near_par_sorted,
            "near_parallel_oriented_top": near_par_oriented_top,
            "near_antiparallel_oriented_top": near_anti_oriented_top,
        },
        "verdict": {
            "rho_1_over_sqrt2_is": "specific to orthogonal e2 geometry under equal weights",
            "near_parallel_oriented_normals": "ρ→1; the 1/√2 vector-sum improvement is lost",
            "near_antiparallel_oriented_normals": "ρ→0; signed assembly can cancel harder than 1/√2",
            "lattice_witness": (
                "e.g. α=50, β=2, k=(-1,-1,0): undirected planes ~11.5° apart (cos|·|≈0.980) "
                "with oriented cos≈-0.980 ⇒ ρ_oriented≈0.101 (antiparallel cancellation), "
                "while the parallel-oriented alignment case pushes ρ toward 1."
            ),
            "does_not_kill_signed_route": (
                "The signed sum still uses Im and receiver compensation; "
                "only stamping 1/√2 as a universal two-triangle constant is unsupported."
            ),
            "next": "Keep signed assembly; treat 1/√2 as the orthogonal special case, not a robust universal factor",
        },
    }
    out = Path(__file__).with_name("TWO-TRIANGLE-NORMAL-ANGLE-CHECKS.json")
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
