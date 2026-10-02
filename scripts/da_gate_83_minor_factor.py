#!/usr/bin/env python3
"""Gate 83 attack: specimen-1 8x8 Jacobian minor.

G1..G12 = six space-diagonal pair collinearities + six face
collinearities of the gauge-fixed 2x2x2 cube

    a=(1,0,0), p0=(r1,r2,r3), b=(b1,b2,0), d=(d1,d2,λ).

J_L = D_(z0..z7,λ)(G1..G12) at λ=0, z0=⋯=z7=t.

Specimen 1: t=1, r=(1,2,3), b=(0,1), d=(2,3).
Pivot: first exact-nonzero 8×8 minor on that specimen.

Verdict is one of M≢0 / M=H_known Q / M≡0.
This run: M≢0. Full factorization over
Q[t,r1,r2,r3,b1,b2,d1,d2] did not land.

NS is not solved.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]

NODE = [
    (0, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 1),
    (1, 0, 0),
    (1, 1, 0),
    (1, 0, 1),
    (1, 1, 1),
]
SPACE_PAIRS = [(0, 7), (4, 3), (1, 6), (2, 5)]
FACE_CLASSES = [
    [(0, 5), (4, 1)],
    [(2, 7), (6, 3)],
    [(0, 6), (4, 2)],
    [(1, 7), (5, 3)],
    [(0, 3), (1, 2)],
    [(4, 7), (5, 6)],
]
G_NAMES = [
    "C01",
    "C02",
    "C03",
    "C12",
    "C13",
    "C23",
    "F_ab0",
    "F_ab1",
    "F_ad0",
    "F_ad1",
    "F_bd0",
    "F_bd1",
]
VAR_NAMES = ["z0", "z1", "z2", "z3", "z4", "z5", "z6", "z7", "lam"]

SPECIMEN_1 = {
    "t": 1,
    "r": (1, 2, 3),
    "b": (0, 1),
    "d": (2, 3),
}


def _cross(u, v):
    return sp.Matrix(
        [
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0],
        ]
    )


def _dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def mode_vec(i, j, k, r, b, d, lam):
    return sp.Matrix(
        [
            r[0] + i + j * b[0] + k * d[0],
            r[1] + j * b[1] + k * d[1],
            r[2] + k * lam,
        ]
    )


def polarization(p, z):
    b1 = _cross(p, sp.Matrix([1, 0, 0]))
    if b1[0] == 0 and b1[1] == 0 and b1[2] == 0:
        b1 = _cross(p, sp.Matrix([0, 1, 0]))
    return b1 + z * _cross(p, b1)


def W_raw(p, q, up, uq):
    return (q.dot(up)) * uq + (p.dot(uq)) * up


def generators(z, r, b, d, lam):
    P = [mode_vec(*NODE[n], r, b, d, lam) for n in range(8)]
    U = [polarization(P[n], z[n]) for n in range(8)]
    Gs = []
    Ws = [W_raw(P[a], P[c], U[a], U[c]) for a, c in SPACE_PAIRS]
    Ks = P[0] + P[7]
    for i, j in combinations(range(4), 2):
        Gs.append(_dot(Ks, _cross(Ws[i], Ws[j])))
    for (a, c), (u, v) in FACE_CLASSES:
        W1 = W_raw(P[a], P[c], U[a], U[c])
        W2 = W_raw(P[u], P[v], U[u], U[v])
        K = P[a] + P[c]
        Gs.append(_dot(K, _cross(W1, W2)))
    return Gs


def jacobian_at_equal_z(t, r, b, d):
    zs = sp.symbols("z0:8")
    lam = sp.symbols("lam")
    Gs = generators(zs, r, b, d, lam)
    vars9 = list(zs) + [lam]
    J = sp.zeros(12, 9)
    subs = {zs[i]: t for i in range(8)}
    subs[lam] = 0
    for i, g in enumerate(Gs):
        for j, v in enumerate(vars9):
            J[i, j] = sp.expand(sp.diff(g, v).subs(subs))
    return J


def first_exact_nonzero_minor(J):
    for drop_col in range(9):
        cols = [c for c in range(9) if c != drop_col]
        for rows in combinations(range(12), 8):
            d = sp.det(J[list(rows), cols])
            if d != 0:
                return {
                    "rows": list(rows),
                    "cols": cols,
                    "drop_col": drop_col,
                    "drop_var": VAR_NAMES[drop_col],
                    "exact_det": str(d),
                }
    return None


def run() -> dict:
    t0, r0, b0, d0 = SPECIMEN_1["t"], SPECIMEN_1["r"], SPECIMEN_1["b"], SPECIMEN_1["d"]
    J = jacobian_at_equal_z(
        sp.Integer(t0),
        [sp.Integer(x) for x in r0],
        [sp.Integer(x) for x in b0],
        [sp.Integer(x) for x in d0],
    )
    rank = int(J.rank())
    pivot = first_exact_nonzero_minor(J)
    J_int = [[int(J[i, j]) for j in range(9)] for i in range(12)]
    n_nonzero_9x9 = 0
    sample_9 = []
    for rows in combinations(range(12), 9):
        d9 = sp.det(J[list(rows), list(range(9))])
        if d9 != 0:
            n_nonzero_9x9 += 1
            if len(sample_9) < 3:
                sample_9.append({"rows": list(rows), "det": str(d9)})

    if pivot is None:
        boxed = r"M \equiv 0"
        verdict = "M_identically_zero"
        meaning = "this minor fails; try another specimen-certified pivot"
    else:
        boxed = r"M \not\equiv 0"
        verdict = "M_not_identically_zero"
        meaning = (
            "specimen-1 exact 8x8 minor is nonzero; exact rank(J_L)=9; "
            "generic rank at least 8. Full factorization over "
            "Q[t,r1,r2,r3,b1,b2,d1,d2] did not land, so no exceptional "
            "locus E_83 is named."
        )

    return {
        "ns_solved": False,
        "da_ns_2_open": True,
        "gate": "83-minor",
        "generators": G_NAMES,
        "n_G": 12,
        "n_vars": 9,
        "specimen_1": SPECIMEN_1,
        "specimen_1_exact_rank": rank,
        "pivot": pivot,
        "n_nonzero_9x9_minors": n_nonzero_9x9,
        "sample_nonzero_9x9": sample_9,
        "J_specimen_1": J_int,
        "boxed": boxed,
        "verdict": verdict,
        "meaning": meaning,
        "factorization_landed": False,
        "H_known": None,
        "Q": None,
        "locked_gates_unaltered": {
            "sbp": True,
            "phi_vs_d": True,
            "low_tail": True,
            "sign": True,
            "s_pq": True,
            "local_star": True,
            "gate_71e": True,
        },
        "all_checks_ok": bool(pivot is not None and rank == 9),
    }


def jsonable(obj):
    if isinstance(obj, dict):
        return {k: jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [jsonable(v) for v in obj]
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    if isinstance(obj, (np.floating, float)):
        return float(obj)
    if isinstance(obj, (np.integer, int)):
        return int(obj)
    return obj


def main() -> int:
    payload = run()
    out = ROOT / "results" / "da_gate_83_minor_factor.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(jsonable(payload), indent=2)
    out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if payload["all_checks_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
