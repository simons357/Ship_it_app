#!/usr/bin/env python3
"""Gate 83D: emit the exact √113 cube spec for Heavy.

No search. No new witness. Proves the generic fifth-radius
identity R_111 - R_000 = (R_100-R_000)+(R_010-R_000)+(R_001-R_000)+2G
and writes the seated lattice in a machine-readable packet.

NS is not solved. (83.34) stays open.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]

SEATED_NODE = [
    {"index": 0, "ijk": [0, 0, 0], "name": "p000"},
    {"index": 1, "ijk": [0, 1, 0], "name": "p010"},
    {"index": 2, "ijk": [0, 0, 1], "name": "p001"},
    {"index": 3, "ijk": [0, 1, 1], "name": "p011"},
    {"index": 4, "ijk": [1, 0, 0], "name": "p100"},
    {"index": 5, "ijk": [1, 1, 0], "name": "p110"},
    {"index": 6, "ijk": [1, 0, 1], "name": "p101"},
    {"index": 7, "ijk": [1, 1, 1], "name": "p111"},
]
BINARY_I_MAJOR = [
    {"index": 0, "ijk": [0, 0, 0], "name": "p000"},
    {"index": 1, "ijk": [1, 0, 0], "name": "p100"},
    {"index": 2, "ijk": [0, 1, 0], "name": "p010"},
    {"index": 3, "ijk": [1, 1, 0], "name": "p110"},
    {"index": 4, "ijk": [0, 0, 1], "name": "p001"},
    {"index": 5, "ijk": [1, 0, 1], "name": "p101"},
    {"index": 6, "ijk": [0, 1, 1], "name": "p011"},
    {"index": 7, "ijk": [1, 1, 1], "name": "p111"},
]

# 12 generators of Gate 83 specimen/minor (Heavy's 12 equations).
SPACE_PAIRS = [[0, 7], [4, 3], [1, 6], [2, 5]]
FACE_CLASSES = [
    [[0, 5], [4, 1]],
    [[2, 7], [6, 3]],
    [[0, 6], [4, 2]],
    [[1, 7], [5, 3]],
    [[0, 3], [1, 2]],
    [[4, 7], [5, 6]],
]
I_ACT_CLASSES = [
    [[0, 7], [4, 3]],
    [[0, 7], [1, 6]],
    [[0, 7], [2, 5]],
    [[0, 5], [4, 1]],
    [[2, 7], [6, 3]],
    [[0, 6], [4, 2]],
    [[1, 7], [5, 3]],
    [[0, 3], [1, 2]],
    [[4, 7], [5, 6]],
]


def fifth_radius_identity():
    """Exact generic identity. No specimen required."""
    r1, r2, b1, b2, d1, d2 = sp.symbols("r1 r2 b1 b2 d1 d2")
    a = (sp.Integer(1), sp.Integer(0))
    b = (b1, b2)
    d = (d1, d2)
    p0 = (r1, r2)

    def add(u, v):
        return (u[0] + v[0], u[1] + v[1])

    def R(p):
        return p[0] ** 2 + p[1] ** 2

    R000 = R(p0)
    R100 = R(add(p0, a))
    R010 = R(add(p0, b))
    R001 = R(add(p0, d))
    R111 = R(add(add(add(p0, a), b), d))
    gram = a[0] * b[0] + a[1] * b[1] + a[0] * d[0] + a[1] * d[1] + b[0] * d[0] + b[1] * d[1]
    residual = sp.expand(R111 - R000 - (R100 - R000) - (R010 - R000) - (R001 - R000) - 2 * gram)
    return {
        "G": str(gram),
        "identity": "R111-R000 = (R100-R000)+(R010-R000)+(R001-R000)+2G",
        "residual": str(residual),
        "holds_identically": bool(residual == 0),
    }


def sqrt113_lattice():
    s = sp.sqrt(113)
    r = (sp.Rational(-1, 2), sp.Rational(6, 5), sp.Rational(6, 5))
    b = (sp.Rational(1, 2), sp.Rational(1, 10))
    d = (
        -sp.Rational(1, 4) - 3 * s / 452,
        -sp.Rational(5, 4) + 45 * s / 452,
    )
    lam = -sp.Rational(12, 5)
    a_h = (sp.Integer(1), sp.Integer(0))

    def R(x, y):
        return sp.simplify(x**2 + y**2)

    radii = {
        "R000": R(r[0], r[1]),
        "R100": R(r[0] + 1, r[1]),
        "R010": R(r[0] + b[0], r[1] + b[1]),
        "R001": R(r[0] + d[0], r[1] + d[1]),
        "R111": R(r[0] + 1 + b[0] + d[0], r[1] + b[1] + d[1]),
    }
    gram = sp.simplify(
        a_h[0] * b[0] + a_h[1] * b[1] + a_h[0] * d[0] + a_h[1] * d[1] + b[0] * d[0] + b[1] * d[1]
    )
    return {
        "field": "Q(sqrt(113))",
        "gauge": {"a": ["1", "0", "0"], "b3": "0", "d3": "lam"},
        "r": [str(x) for x in r],
        "b": [str(x) for x in b],
        "d": [str(sp.simplify(x)) for x in d],
        "lam": str(lam),
        "delta": str(sp.simplify(b[1] * lam)),
        "companion_root_u": "(13 + 15*sqrt(113))/82",
        "ten_scaled_circle": "X^2 + Y^2 = 169, A=(-5,12), C=(0,13)",
        "radii_squared": {k: str(v) for k, v in radii.items()},
        "G": str(gram),
        "five_radii_equal": all(v == sp.Rational(169, 100) for v in radii.values()),
        "G_zero": bool(gram == 0),
        "polarization_chart": "U(p,z)=(p×e1)+z(p×(p×e1)); fallback e2 if p×e1=0",
        "W": "W(p,q;Up,Uq)=(q·Up)Uq+(p·Uq)Up  (raw, no Leray)",
        "z_pinned_z4_eq_0_float": [
            0.21923899233928215,
            0.8625902592484509,
            0.2988522288763246,
            0.4520727758956118,
            0.0,
            0.3002609304859156,
            0.23756176088855308,
            0.30050381395823705,
        ],
        "z_order_for_pinned": "seated 000,010,001,011,100,110,101,111",
        "free_node_on_I_act": "seated z4 = p100",
        "I_act_vanishes_at_pinned": True,
        "G12_space_C12_C13_C23_do_not_vanish_at_pinned": True,
    }


def run() -> dict:
    ident = fifth_radius_identity()
    lat = sqrt113_lattice()
    return {
        "ns_solved": False,
        "da_ns_2_open": True,
        "gate": "83D-spec",
        "purpose": "send the √113 cube to Heavy; not a new witness hunt",
        "heavy_83D": {
            "status": "PROVED_REPORTED",
            "recomputed_here": False,
            "statement": (
                "Reduced modulo the three radius conditions plus G, "
                "the hinge-mode column is exactly zero in all 12 "
                "equations. Each hinge equation factors as "
                "-r3^3 L^2 (R111-Ri). Saturation removes only r3=0 "
                "and six activity factors. No new geometry."
            ),
            "fifth_radius": "redundant: three radius differences plus 2G",
        },
        "fifth_radius_identity": ident,
        "seated_node_order": SEATED_NODE,
        "binary_i_major_node_order": BINARY_I_MAJOR,
        "space_pairs_seated": SPACE_PAIRS,
        "face_classes_seated": FACE_CLASSES,
        "I_act_classes_seated": I_ACT_CLASSES,
        "sqrt113_cube": lat,
        "what_heavy_should_run": (
            "Instantiate G1..G12 on this lattice. Reduce the z-column "
            "of the hinge mode modulo (R100-R000, R010-R000, R001-R000, G). "
            "Report which seated index is the hinge (p100 vs p111). "
            "Do not search for another cube."
        ),
        "all_checks_ok": bool(ident["holds_identically"] and lat["five_radii_equal"] and lat["G_zero"]),
    }


def main() -> int:
    payload = run()
    out = ROOT / "results" / "da_gate_83d_sqrt113_spec.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2)
    out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if payload["all_checks_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
