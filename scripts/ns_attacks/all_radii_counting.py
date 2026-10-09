"""All-radii geometric counting for Gate B.

Euclidean fact (all radii): two independent affine planes and a sphere
in R^3 determine at most two points.

That fact is not the same as a uniform multiplicity bound on Fourier
triads, and it does not by itself give a trilinear norm bound.

Not (17). NS is not solved.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Sequence

Vec = tuple[int, int, int]


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return float(a[0] * b[0] + a[1] * b[1] + a[2] * b[2])


def cross(a: Sequence[float], b: Sequence[float]) -> tuple[float, float, float]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def radius2(v: Sequence[int]) -> int:
    return int(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def lin_indep(a: Sequence[float], b: Sequence[float], atol: float = 1e-12) -> bool:
    c = cross(a, b)
    return abs(c[0]) + abs(c[1]) + abs(c[2]) > atol


def two_planes_sphere(
    n1: Sequence[float],
    c1: float,
    n2: Sequence[float],
    c2: float,
    r2: float,
    atol: float = 1e-10,
) -> dict:
    """Solve n1·x = c1, n2·x = c2, |x|² = r2.

    Returns at most two real solutions when n1, n2 are linearly independent.
    Parallel normals are recorded as a degeneracy, not as μ ≤ 2.
    """
    if not lin_indep(n1, n2, atol=atol):
        return {
            "independent_normals": False,
            "n_real": None,
            "solutions": [],
            "degeneracy": "parallel_planes",
        }
    g11 = dot(n1, n1)
    g22 = dot(n2, n2)
    g12 = dot(n1, n2)
    det = g11 * g22 - g12 * g12
    a = (c1 * g22 - c2 * g12) / det
    b = (c2 * g11 - c1 * g12) / det
    x0 = (a * n1[0] + b * n2[0], a * n1[1] + b * n2[1], a * n1[2] + b * n2[2])
    d = cross(n1, n2)
    nd = math.sqrt(dot(d, d))
    uhat = (d[0] / nd, d[1] / nd, d[2] / nd)
    # |x0 + t uhat|² = r2, |uhat|=1
    qa = 1.0
    qb = 2.0 * dot(x0, uhat)
    qc = dot(x0, x0) - r2
    disc = qb * qb - 4.0 * qa * qc
    sols: list[tuple[float, float, float]] = []
    if disc > atol:
        root = math.sqrt(disc)
        for t in ((-qb + root) / 2.0, (-qb - root) / 2.0):
            sols.append((x0[0] + t * uhat[0], x0[1] + t * uhat[1], x0[2] + t * uhat[2]))
    elif abs(disc) <= atol:
        t = -qb / 2.0
        sols.append((x0[0] + t * uhat[0], x0[1] + t * uhat[1], x0[2] + t * uhat[2]))
    return {
        "independent_normals": True,
        "n_real": len(sols),
        "solutions": sols,
        "degeneracy": None,
        "discriminant": disc,
    }


def common_closer_planes(
    p: Vec, q: Vec, rho: float, gamma: float, delta: float
) -> dict:
    """Two-input common closer.

    r satisfies |r|² = ρ, |r+p|² = γ, |r+q|² = δ.
    Equivalent to two plane constraints and a sphere:

        2 p·r = γ − ρ − |p|²
        2 q·r = δ − ρ − |q|²
        |r|² = ρ
    """
    n1 = (2.0 * p[0], 2.0 * p[1], 2.0 * p[2])
    n2 = (2.0 * q[0], 2.0 * q[1], 2.0 * q[2])
    c1 = gamma - rho - radius2(p)
    c2 = delta - rho - radius2(q)
    out = two_planes_sphere(n1, c1, n2, c2, rho)
    out["p"] = p
    out["q"] = q
    out["distinct_shells"] = radius2(p) != radius2(q)
    out["linearly_independent"] = lin_indep(p, q)
    return out


def lattice_one_input_two_shell(
    p: Vec, beta: int, gamma: int, box: int
) -> list[Vec]:
    """Partners q of a fixed input p with |q|²=β and |p+q|²=γ.

    Locus in R^3 is a circle (one radical plane and a sphere). Lattice
    occupancy can exceed two.
    """
    out: list[Vec] = []
    for x in range(-box, box + 1):
        for y in range(-box, box + 1):
            for z in range(-box, box + 1):
                if x * x + y * y + z * z != beta:
                    continue
                sx, sy, sz = p[0] + x, p[1] + y, p[2] + z
                if sx * sx + sy * sy + sz * sz == gamma:
                    out.append((x, y, z))
    return out


def lattice_common_closers(
    p: Vec, q: Vec, rho: int, gamma: int, delta: int, box: int
) -> list[Vec]:
    out: list[Vec] = []
    for x in range(-box, box + 1):
        for y in range(-box, box + 1):
            for z in range(-box, box + 1):
                if x * x + y * y + z * z != rho:
                    continue
                sx, sy, sz = p[0] + x, p[1] + y, p[2] + z
                tx, ty, tz = q[0] + x, q[1] + y, q[2] + z
                if sx * sx + sy * sy + sz * sz == gamma and tx * tx + ty * ty + tz * tz == delta:
                    out.append((x, y, z))
    return out


def circle_counterexample() -> dict:
    """One fixed input, two shells: four lattice closers.

    p = (0,0,2), |q|² = 5, |p+q|² = 5.
    Plane: q_z = -1. Sphere: q_x² + q_y² = 4. Four lattice points.
    """
    p = (0, 0, 2)
    partners = lattice_one_input_two_shell(p, beta=5, gamma=5, box=4)
    return {
        "p": p,
        "beta": 5,
        "gamma": 5,
        "n_lattice": len(partners),
        "partners": partners,
        "exceeds_two": len(partners) > 2,
    }


def parallel_distinct_shell_degeneracy() -> dict:
    """Distinct shells are not enough: p=(1,0,0), q=(2,0,0) are parallel."""
    p = (1, 0, 0)
    q = (2, 0, 0)
    geo = common_closer_planes(p, q, rho=5.0, gamma=6.0, delta=9.0)
    return {
        "p": p,
        "q": q,
        "distinct_shells": True,
        "linearly_independent": False,
        "independent_normals": geo["independent_normals"],
        "degeneracy": geo["degeneracy"],
    }


def finite_radius_scan(box: int = 6) -> dict:
    """Brute-force finite-radius checks.

    (i) Two-input common closers with independent p, q: lattice count ≤ 2.
    (ii) One-input two-shell: record the maximum occupancy (circle).
    """
    vectors = [
        (x, y, z)
        for x in range(-box, box + 1)
        for y in range(-box, box + 1)
        for z in range(-box, box + 1)
        if (x, y, z) != (0, 0, 0)
    ]
    max_common = 0
    common_fail = 0
    pairs_checked = 0
    # A thin deterministic sample: first vector vs a stride of later ones.
    sample_p = [(1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 1, 0), (2, 1, 1), (3, 1, 1)]
    sample_q = [(0, 1, 0), (0, 2, 0), (1, 0, 2), (0, 1, 2), (2, 0, 1), (1, 2, 2)]
    for p in sample_p:
        for q in sample_q:
            if p == q or not lin_indep(p, q):
                continue
            for rho in (1, 2, 4, 5, 6, 9, 10, 13):
                for gamma in (1, 2, 4, 5, 6, 9, 13):
                    for delta in (1, 2, 4, 5, 9, 13):
                        pts = lattice_common_closers(p, q, rho, gamma, delta, box=5)
                        pairs_checked += 1
                        max_common = max(max_common, len(pts))
                        if len(pts) > 2:
                            common_fail += 1
    max_circle = 0
    circle_examples = []
    for p in sample_p:
        a = radius2(p)
        for beta in range(1, 26):
            for gamma in range(1, 26):
                pts = lattice_one_input_two_shell(p, beta, gamma, box=5)
                if len(pts) > max_circle:
                    max_circle = len(pts)
                if len(pts) > 2 and len(circle_examples) < 8:
                    circle_examples.append(
                        {"p": p, "a": a, "beta": beta, "gamma": gamma, "n": len(pts)}
                    )
    return {
        "two_input_pairs_checked": pairs_checked,
        "two_input_max_lattice": max_common,
        "two_input_failures_gt_2": common_fail,
        "one_input_max_lattice": max_circle,
        "one_input_circle_examples": circle_examples,
        "vectors_enumerated_box": box,
    }


def report() -> dict:
    circle = circle_counterexample()
    parallel = parallel_distinct_shell_degeneracy()
    scan = finite_radius_scan()
    # Independent-normal Euclidean bound on a few random-looking floats.
    euclidean_n = []
    trials = [
        ((1.0, 0.0, 0.0), 0.3, (0.0, 1.0, 0.0), -0.2, 2.0),
        ((1.0, 1.0, 0.0), 1.0, (0.0, 1.0, 1.0), 0.5, 4.0),
        ((2.0, -1.0, 0.5), 0.0, (0.25, 3.0, 1.0), 1.2, 9.0),
        ((0.0, 0.0, 1.0), 1.0, (1.0, 1.0, 0.0), 0.0, 1.0),
        ((3.0, 1.0, 1.0), 2.0, (1.0, -2.0, 0.0), -1.0, 16.0),
    ]
    for n1, c1, n2, c2, r2 in trials:
        euclidean_n.append(two_planes_sphere(n1, c1, n2, c2, r2)["n_real"])
    return {
        "lemma_two_planes_sphere": {
            "statement": (
                "Two linearly independent affine planes and a sphere in R^3 "
                "meet in at most two points."
            ),
            "euclidean_n_real": euclidean_n,
            "max_n_real": max(n for n in euclidean_n if n is not None),
            "status": "pass",
        },
        "distinct_shell_not_enough": parallel,
        "one_input_two_shell_circle": circle,
        "finite_radius_scan": scan,
        "verdicts": {
            "euclidean_two_planes_sphere_le_2": True,
            "distinct_shell_implies_independent_normals": False,
            "one_input_two_shell_multiplicity_le_2": False,
            "two_input_common_closer_le_2_when_independent": scan["two_input_failures_gt_2"]
            == 0,
            "counting_implies_trilinear_norm_bound": False,
        },
        "ns_solved": False,
        "theorem_17_proved": False,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="All-radii geometric counting checks")
    p.add_argument(
        "--out",
        type=Path,
        default=Path("scripts/ns_attacks/ALL-RADII-COUNTING.json"),
    )
    args = p.parse_args()
    payload = report()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2))
    v = payload["verdicts"]
    print("euclidean ≤2:", v["euclidean_two_planes_sphere_le_2"])
    print(
        "distinct-shell ⇒ independent normals:",
        v["distinct_shell_implies_independent_normals"],
    )
    print(
        "one-input two-shell μ≤2:",
        v["one_input_two_shell_multiplicity_le_2"],
        "counterexample n=",
        payload["one_input_two_shell_circle"]["n_lattice"],
    )
    print(
        "two-input common closer μ≤2 on sample:",
        v["two_input_common_closer_le_2_when_independent"],
        "max",
        payload["finite_radius_scan"]["two_input_max_lattice"],
    )
    print("counting ⇒ trilinear bound:", v["counting_implies_trilinear_norm_bound"])
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
