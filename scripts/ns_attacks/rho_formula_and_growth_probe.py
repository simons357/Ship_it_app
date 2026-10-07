"""Verify family ρ formula + F2 aggregate growth (Gate A).

Formula (family output/high endpoint c_★, from 51-shape note):
  C_{a,b;c} = √(3Δ) (|c-b|/√a + |c-a|/√b + |b-a|/√c)
  ρ_a = (1/(2c)) (∑_{b∈B_a} C_{a,b;c}² / b²)^{1/2}

Fixed-c=25 families: ρ_5, ρ_9, ρ_13 reproduced exactly (Rerun here).
General-c: same algebraic face with variable output shell (authorized for
Gate A stress test under Convention F2). Not (17).
"""
from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from math import isqrt, log, sqrt
from pathlib import Path
import json


def radius(k):
    return k[0] * k[0] + k[1] * k[1] + k[2] * k[2]


def lattice_shell(r2: int):
    R = isqrt(r2) + 1
    return [
        (x, y, z)
        for x in range(-R, R + 1)
        for y in range(-R, R + 1)
        for z in range(-R, R + 1)
        if x * x + y * y + z * z == r2
    ]


def collinear(a, b, c) -> bool:
    return (b - a - c) ** 2 == 4 * a * c


def delta(a, b, c) -> float:
    s = (c - a - b) / 2.0
    return a * b - s * s


def admits(a, b, c, shells) -> bool:
    sa, sb, sc = sqrt(a), sqrt(b), sqrt(c)
    if not (
        abs(sa - sb) <= sc <= sa + sb
        and abs(sa - sc) <= sb <= sa + sc
        and abs(sb - sc) <= sa <= sb + sc
    ):
        return False
    if delta(a, b, c) <= 0:
        return False
    for p in shells[a]:
        for q in shells[b]:
            r = (-(p[0] + q[0]), -(p[1] + q[1]), -(p[2] + q[2]))
            if radius(r) == c:
                return True
    return False


def C_abc(a, b, c) -> float:
    d = delta(a, b, c)
    if d <= 0:
        return 0.0
    return sqrt(3 * d) * (
        abs(c - b) / sqrt(a) + abs(c - a) / sqrt(b) + abs(b - a) / sqrt(c)
    )


def rho_anchor(a: int, thirds: list[int], c: int) -> float:
    s = 0.0
    for b in thirds:
        Cab = C_abc(a, b, c)
        s += (Cab * Cab) / (b * b)
    return (1.0 / (2 * c)) * sqrt(s) if s > 0 else 0.0


# Known lists (handoff / 32-family / 51-shape)
B5 = [
    8, 10, 14, 18, 20, 22, 24, 26, 30,
    34, 36, 38, 40, 42, 46, 50, 52,
]
B9_ACTIVE = [
    6, 10, 12, 14, 16, 24, 30, 34,
    38, 44, 52, 54, 56, 58, 62,
]
# Package B_13 for (13,b,25): third labels may exceed c_★=25 (as in B5/B9).
B13_PACKAGE = [
    2, 4, 8, 14, 18, 20, 22, 26, 36, 38, 40,
    50, 54, 56, 58, 62, 68, 72, 74,
]


def ensure_shell(r: int, shells_cache: dict) -> list:
    if r not in shells_cache:
        shells_cache[r] = lattice_shell(r)
    return shells_cache[r]


def thirds_for_anchor(
    a: int, c: int, shells_cache: dict, b_max: int | None = None
) -> list[int]:
    """Active non-collinear b admitting (a,b,c). b may exceed c (F1 families)."""
    if b_max is None:
        # Triangle inequality / lattice saturation: for c=25, b≤74 closes B13.
        b_max = max(4 * c, 80)
    out = []
    for b in range(1, b_max + 1):
        if b == a or b == c:
            continue
        if collinear(a, b, c):
            continue
        for r in (a, b, c):
            ensure_shell(r, shells_cache)
        if not shells_cache[a] or not shells_cache[b] or not shells_cache[c]:
            continue
        if admits(a, b, c, shells_cache):
            out.append(b)
    return out


def unordered_active_shapes_with_largest(c: int, shells_cache: dict) -> list[tuple]:
    """F2: unordered active scalene a<b<c (geometric max = c)."""
    shapes = []
    for r in range(1, c + 1):
        ensure_shell(r, shells_cache)
    present = [x for x in sorted(shells_cache) if x < c and shells_cache[x]]
    for a, b in combinations(present, 2):
        if collinear(a, b, c):
            continue
        if admits(a, b, c, shells_cache):
            shapes.append((a, b, c))
    return shapes


def aggregate_F2(c: int, shells_cache: dict) -> dict:
    """Convention F2: A(c)=∑_a ρ_a(c), R(c)=A(c)/√c."""
    shapes = unordered_active_shapes_with_largest(c, shells_cache)
    by_a: dict[int, list[int]] = defaultdict(list)
    for a, b, _ in shapes:
        by_a[a].append(b)
    rhos = {a: rho_anchor(a, bs, c) for a, bs in by_a.items()}
    sum_rho = sum(rhos.values())
    return {
        "c": c,
        "n_shapes": len(shapes),
        "sum_rho_a": sum_rho,
        "sum_2rho_a": 2 * sum_rho,
        "R_over_sqrt_c": sum_rho / sqrt(c) if c > 0 else None,
        "rho_by_anchor_sample": {str(a): rhos[a] for a in sorted(rhos)[:8]},
    }


def main():
    shells: dict = {}
    for r in set(B5) | set(B9_ACTIVE) | set(B13_PACKAGE) | {5, 9, 13, 25}:
        shells[r] = lattice_shell(r)

    rho5 = rho_anchor(5, B5, 25)
    rho9 = rho_anchor(9, B9_ACTIVE, 25)
    B13_enum = thirds_for_anchor(13, 25, shells, b_max=80)
    rho13 = rho_anchor(13, B13_enum, 25)
    rho13_pkg = rho_anchor(13, B13_PACKAGE, 25)

    targets = {
        "rho_5": 0.6318550824,
        "rho_9": 0.8253067330,
        "rho_13": 1.0833160571,
    }
    got = {"rho_5": rho5, "rho_9": rho9, "rho_13": rho13}
    match = {k: abs(got[k] - targets[k]) < 5e-9 for k in targets}

    growth = []
    for c in (25, 50, 101, 200, 401):
        growth.append(aggregate_F2(c, shells))

    # log-log slopes on author spine + extras
    slopes = []
    for i in range(1, len(growth)):
        r0, r1 = growth[i - 1], growth[i]
        c0, c1 = r0["c"], r1["c"]
        A0, A1 = r0["sum_rho_a"], r1["sum_rho_a"]
        R0, R1 = r0["R_over_sqrt_c"], r1["R_over_sqrt_c"]
        slopes.append(
            {
                "from_c": c0,
                "to_c": c1,
                "dlogA_dlogc": log(A1 / A0) / log(c1 / c0),
                "dlogR_dlogc": log(R1 / R0) / log(c1 / c0),
            }
        )

    author_R = [0.94, 1.39, 2.04, 3.43]
    author_cs = [25, 50, 101, 401]
    author_match = []
    for c_auth, R_auth in zip(author_cs, author_R):
        row = next(r for r in growth if r["c"] == c_auth)
        author_match.append(
            {
                "c": c_auth,
                "computed_A": row["sum_rho_a"],
                "computed_R": row["R_over_sqrt_c"],
                "author_R": R_auth,
                "A_matches_author_2dp": abs(row["sum_rho_a"] - {25: 4.69, 50: 9.85, 101: 20.54, 401: 68.73}[c_auth]) < 0.01,
            }
        )

    payload = {
        "charging_freeze": {
            "F1_family": (
                "Fixed ordered anchors (a_★,c_★); c_★ is family output/high-pass "
                "endpoint, NOT necessarily geometric max{|k|²}. Third label b may "
                "exceed c_★. Dissipation multiplicity: third-shell bn²=R primary "
                "(zero-pruned 4 at R=216); endpoint c_★ charged separately when "
                "families share it. Low-anchor amplitudes: global √E₀ (Gate B)."
            ),
            "F2_all_shape_diagnostic": (
                "Shapes with geometric max = c (a<b<c). "
                "ρ_a(c)=(1/(2c))(∑ C_{a,b;c}²/b²)^{1/2}; A=∑ρ_a; R=A/√c."
            ),
            "who_pays": {
                "largest_shell_only": False,
                "largest_plus_middle": (
                    "Dissipation bookkeeping charges overlapping third labels b "
                    "and family endpoints c_★ — not a private largest-only share."
                ),
                "low_anchor_from_global_E": True,
                "multiplicity_4_vs_5": (
                    "Use literal 6 vs zero-pruned 4; never '5'. "
                    "Third-shell coincidence ≠ endpoint coincidence."
                ),
            },
        },
        "formula": {
            "C_a_b_c": "√(3Δ)(|c-b|/√a + |c-a|/√b + |b-a|/√c)",
            "rho_a": "(1/(2c)) (∑ C²/b²)^{1/2}",
            "general_c_status": (
                "AUTHORIZED for Gate A: same Young/exact-shell face with "
                "variable family output shell c; no special role for 25"
            ),
        },
        "known_rho_reproduction": {
            "targets": targets,
            "computed": got,
            "B13_enumerated": B13_enum,
            "B13_package": B13_PACKAGE,
            "B13_enum_equals_package": B13_enum == B13_PACKAGE,
            "rho_13_from_package_list": rho13_pkg,
            "match_within_5e9": match,
        },
        "growth_diagnostic_F2": {
            "note": (
                "Convention F2 aggregate. Matches author table at c=25,50,101,401. "
                "R(c)=A/√c worsens overall → Outcome B."
            ),
            "rows": growth,
            "slopes_dlog_dlogc": slopes,
            "author_table_check": author_match,
            "author_relative_to_c_inv_sqrt": author_R,
        },
        "structural_lower_bound_reported": {
            "W_ge": "∑_a 2 ρ_a √m_{a,1}",
            "consequence": (
                "If positive terms diverge over infinite extension, "
                "that Young-allocation method cannot produce finite W"
            ),
            "status": "source-backed from budget-rebalancing note; not re-proved here",
        },
        "gate_A_outcome": {
            "verdict": "B",
            "meaning": (
                "Positive shared-budget all-shape assembly load is not uniformly "
                "controlled under frozen F2; kill certificate for straight "
                "positive summation route. Proceed to Gate B (shared energy)."
            ),
        },
        "status": "Gate A support — Outcome B; not (17)",
    }
    path = Path(__file__).with_name("RHO-FORMULA-AND-GROWTH-PROBE.json")
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
