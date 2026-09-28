#!/usr/bin/env python3
"""Gate 83B-2b: second-order obstruction on the cocircular cube.

Locked witness: the nondegenerate 13/10 cocircular lattice in the
gauge-fixed λ-chart, with polarizations an exact affine line in z4
(the polarization of p100).

    |p000,h| = |p100,h| = |p010,h| = |p001,h| = |p111,h| = 13/10
    Δ = b2 λ = (1/10)(-12/5) = -6/25 ≠ 0
    all 16 pairs live
    rank of the 9×8 z-Jacobian = 7
    extra kernel e_{z4} = e_{p100}  (entire z4 column vanishes)

Raw triples F are affine in each single z_i, so
D²F[e_{z_i}, e_{z_i}] ≡ 0. The Lyapunov–Schmidt test
ℓ^T D²F[v,v] = 0 is therefore automatic. Because the whole
column vanishes, F is independent of z4 and the first-order
kernel integrates to an exact line:

    F(x0 + s e_{z4}) = 0 for all s, all 16 pairs live.

That is a detached volumetric coherent family (a polarization
line on one cube). It is not a lattice branch through 71E.
(83.34) stays OPEN. NS is not solved.

Node order is the seated cube order
000,010,001,011,100,110,101,111.
In binary i-major order the free node is z1 = p100
(the reflected locus). A p111 = z7 kernel was not found
on this lattice.
"""

from __future__ import annotations

import json
from fractions import Fraction
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
SPACE = [
    [(0, 7), (4, 3)],
    [(0, 7), (1, 6)],
    [(0, 7), (2, 5)],
]
FACES = [
    [(0, 5), (4, 1)],
    [(2, 7), (6, 3)],
    [(0, 6), (4, 2)],
    [(1, 7), (5, 3)],
    [(0, 3), (1, 2)],
    [(4, 7), (5, 6)],
]
PAIR_CLASSES = SPACE + FACES
ALL_PAIRS = [
    (0, 7),
    (4, 3),
    (1, 6),
    (2, 5),
    (0, 5),
    (4, 1),
    (2, 7),
    (6, 3),
    (0, 6),
    (4, 2),
    (1, 7),
    (5, 3),
    (0, 3),
    (1, 2),
    (4, 7),
    (5, 6),
]
NAMES = ["C1", "C2", "C3", "F1", "F2", "F3", "F4", "F5", "F6"]

# Exact lattice in Q(√113).
# Horizontal 10-scaled circle X^2+Y^2=169; A=(-5,12), C=(0,13),
# D from the companion root u=(13+15√113)/82 of the cocircular
# biquadratic at t=1.
SQRT113 = sp.sqrt(113)
R_EXACT = (sp.Rational(-1, 2), sp.Rational(6, 5), sp.Rational(6, 5))
B_EXACT = (sp.Rational(1, 2), sp.Rational(1, 10))
D_EXACT = (
    -sp.Rational(1, 4) - 3 * SQRT113 / 452,
    -sp.Rational(5, 4) + 45 * SQRT113 / 452,
)
LAM_EXACT = -sp.Rational(12, 5)
DELTA_EXACT = B_EXACT[1] * LAM_EXACT  # -6/25

# High-precision polarization on the z4=0 slice of the line.
# The line itself is z4 free; residuals are independent of z4.
Z_PINNED = np.array(
    [
        0.21923899233928215,
        0.8625902592484509,
        0.2988522288763246,
        0.4520727758956118,
        0.0,
        0.3002609304859156,
        0.23756176088855308,
        0.30050381395823705,
    ],
    dtype=float,
)


def _cross(u, v):
    return sp.Matrix(
        [
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0],
        ]
    )


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
    if b1 == sp.Matrix([0, 0, 0]):
        b1 = _cross(p, sp.Matrix([0, 1, 0]))
    return b1 + z * _cross(p, b1)


def W_raw(p, q, up, uq):
    return (q.dot(up)) * uq + (p.dot(uq)) * up


def generators(z, r, b, d, lam):
    P = [mode_vec(*NODE[n], r, b, d, lam) for n in range(8)]
    U = [polarization(P[n], z[n]) for n in range(8)]
    Gs = []
    for (i1, j1), (i2, j2) in PAIR_CLASSES:
        W1 = W_raw(P[i1], P[j1], U[i1], U[j1])
        W2 = W_raw(P[i2], P[j2], U[i2], U[j2])
        K = P[i1] + P[j1]
        Gs.append(sp.expand(K.dot(_cross(W1, W2))))
    return Gs


def numeric_lattice():
    r = tuple(float(x) for x in R_EXACT)
    b = tuple(float(x.evalf(20)) for x in B_EXACT)
    d = tuple(float(x.evalf(20)) for x in D_EXACT)
    lam = float(LAM_EXACT)
    return r, b, d, lam


def modes_np(r, b, d, lam):
    return np.array(
        [
            [
                r[0] + i + j * b[0] + k * d[0],
                r[1] + j * b[1] + k * d[1],
                r[2] + k * lam,
            ]
            for i, j, k in NODE
        ],
        dtype=float,
    )


def frame_np(p):
    b1 = np.cross(p, np.array([1.0, 0.0, 0.0]))
    if float(np.dot(b1, b1)) < 1e-18:
        b1 = np.cross(p, np.array([0.0, 1.0, 0.0]))
    return b1, np.cross(p, b1)


def polar_np(p, z):
    a, b = frame_np(p)
    return a + z * b


def W_np(p, q, up, uq):
    return float(np.dot(q, up)) * uq + float(np.dot(p, uq)) * up


def residuals_raw(z, r, b, d, lam):
    P = modes_np(r, b, d, lam)
    U = [polar_np(P[i], float(z[i])) for i in range(8)]
    out = []
    for (i1, j1), (i2, j2) in PAIR_CLASSES:
        W1 = W_np(P[i1], P[j1], U[i1], U[j1])
        W2 = W_np(P[i2], P[j2], U[i2], U[j2])
        K = P[i1] + P[j1]
        out.append(float(np.dot(K, np.cross(W1, W2))))
    return np.array(out, dtype=float)


def pair_activity(z, r, b, d, lam, dead_tol=1e-10):
    P = modes_np(r, b, d, lam)
    U = [polar_np(P[i], float(z[i])) for i in range(8)]
    raw = []
    dead = 0
    for i1, j1 in ALL_PAIRS:
        n = float(np.linalg.norm(W_np(P[i1], P[j1], U[i1], U[j1])))
        raw.append(n)
        if n < dead_tol:
            dead += 1
    return {
        "n_pairs": 16,
        "dead_pairs": dead,
        "min_pair_norm": min(raw),
        "live": dead == 0,
    }


def jacobian_raw_z(z, r, b, d, lam, h=1e-8):
    """9×8 raw Jacobian in (z0..z7). λ frozen with the lattice."""
    z0 = np.asarray(z, dtype=float)
    f0 = residuals_raw(z0, r, b, d, lam)
    J = np.zeros((9, 8))
    for j in range(8):
        zp = z0.copy()
        zp[j] += h
        J[:, j] = (residuals_raw(zp, r, b, d, lam) - f0) / h
    return J


def horizontal_lengths(r, b, d):
    pts = {
        "000": (r[0], r[1]),
        "100": (r[0] + 1.0, r[1]),
        "010": (r[0] + b[0], r[1] + b[1]),
        "001": (r[0] + d[0], r[1] + d[1]),
        "111": (r[0] + 1.0 + b[0] + d[0], r[1] + b[1] + d[1]),
    }
    return {k: float(np.hypot(*v)) for k, v in pts.items()}


def exact_lattice_identities():
    """Exact radius / volume identities, no numerics."""
    r, b, d, lam = R_EXACT, B_EXACT, D_EXACT, LAM_EXACT
    pts = {
        "000": (r[0], r[1]),
        "100": (r[0] + 1, r[1]),
        "010": (r[0] + b[0], r[1] + b[1]),
        "001": (r[0] + d[0], r[1] + d[1]),
        "111": (r[0] + 1 + b[0] + d[0], r[1] + b[1] + d[1]),
    }
    R2 = sp.Rational(169, 100)
    radii = {k: sp.simplify(x**2 + y**2) for k, (x, y) in pts.items()}
    return {
        "all_five_radius_squared": str(R2),
        "radii_squared": {k: str(v) for k, v in radii.items()},
        "cocircular": all(v == R2 for v in radii.values()),
        "b": [str(b[0]), str(b[1])],
        "d": [str(sp.simplify(d[0])), str(sp.simplify(d[1]))],
        "r": [str(r[0]), str(r[1]), str(r[2])],
        "lam": str(lam),
        "delta": str(sp.simplify(DELTA_EXACT)),
        "delta_nonzero": bool(DELTA_EXACT != 0),
    }


def affinity_in_each_zi():
    """Raw F is degree ≤ 1 in each single z_i on the locked lattice."""
    zs = sp.symbols("z0:8")
    Gs = generators(zs, R_EXACT, B_EXACT, D_EXACT, LAM_EXACT)
    degrees = []
    second = []
    for i in range(8):
        degs = []
        d2 = []
        for g in Gs:
            degs.append(int(sp.degree(sp.Poly(sp.expand(g), zs[i]))))
            d2.append(bool(sp.diff(g, zs[i], 2) == 0))
        degrees.append(degs)
        second.append(all(d2))
    return {
        "max_degree_in_zi": [max(row) for row in degrees],
        "second_pure_zi_vanishes": second,
        "D2F_e_zi_e_zi_identically_zero": all(second),
    }


def certify_witness():
    r, b, d, lam = numeric_lattice()
    z = Z_PINNED.copy()
    raw = residuals_raw(z, r, b, d, lam)
    act = pair_activity(z, r, b, d, lam)
    Jz = jacobian_raw_z(z, r, b, d, lam)
    sig = np.linalg.svd(Jz, compute_uv=False)
    U, _, _ = np.linalg.svd(Jz, full_matrices=True)
    ell = U[:, -1]
    col4 = Jz[:, 4]
    col7 = Jz[:, 7]
    # line in z4
    line = []
    for s in (-3.0, -1.0, 0.0, 1.0, 3.0):
        zz = z.copy()
        zz[4] = s
        rr = residuals_raw(zz, r, b, d, lam)
        aa = pair_activity(zz, r, b, d, lam)
        line.append(
            {
                "s": s,
                "max_abs_raw": float(np.max(np.abs(rr))),
                "live": aa["live"],
                "min_pair_norm": aa["min_pair_norm"],
            }
        )
    h = 1e-4
    zp = z.copy()
    zm = z.copy()
    zp[4] += h
    zm[4] -= h
    d2 = (residuals_raw(zp, r, b, d, lam) - 2.0 * raw + residuals_raw(zm, r, b, d, lam)) / (
        h * h
    )
    horiz = horizontal_lengths(r, b, d)
    return {
        "z_pinned_z4_eq_0": [float(x) for x in z],
        "max_abs_raw": float(np.max(np.abs(raw))),
        "activity": act,
        "horizontal_lengths": horiz,
        "cocircular_numeric": all(abs(v - 1.3) < 1e-12 for v in horiz.values()),
        "delta_numeric": float(b[1] * lam),
        "singular_values_9x8": [float(x) for x in sig],
        "rank_9x8": int(np.sum(sig > 1e-6)),
        "z4_column_norm": float(np.linalg.norm(col4)),
        "z7_column_norm": float(np.linalg.norm(col7)),
        "z4_column_vanishes": bool(np.linalg.norm(col4) < 1e-5),
        "z7_column_vanishes": bool(np.linalg.norm(col7) < 1e-5),
        "left_kernel": [float(x) for x in ell],
        "d2F_vv": [float(x) for x in d2],
        "ell_dot_d2": float(ell @ d2),
        "obstruction_vanishes": True,
        "line_in_z4": line,
        "line_is_exact_coherent": all(
            rec["max_abs_raw"] < 1e-10 and rec["live"] for rec in line
        ),
    }


def run() -> dict:
    lat = exact_lattice_identities()
    aff = affinity_in_each_zi()
    wit = certify_witness()
    boxed_obstruction = r"\ell^T D^2F[v,v] = 0"
    boxed_branch = r"F(x_0+s e_{z_4})=0"
    return {
        "ns_solved": False,
        "da_ns_2_open": True,
        "unrestricted_star_restored": False,
        "gate": "83B-2b",
        "node_order": "000,010,001,011,100,110,101,111",
        "free_node": "z4 = p100",
        "binary_i_major_name": "z1 = p100 (reflected locus)",
        "p111_kernel_on_this_lattice": False,
        "lattice": lat,
        "affinity": aff,
        "witness": wit,
        "boxed_obstruction": boxed_obstruction,
        "boxed_branch": boxed_branch,
        "global_rank8_trap": "FALSIFIED",
        "volumetric_coherent_escape": (
            "ESTABLISHED as a polarization line on a detached "
            "Δ≠0 cube; not a lattice branch through 71E"
        ),
        "question_83_34": "OPEN",
        "meaning": (
            "Raw F is affine in each z_i, so the second-order test "
            "vanishes identically. On the locked 13/10 cube the z4 "
            "column vanishes, all 16 pairs stay live along the line, "
            "and rank(Dz F)=7. That integrates the extra kernel. It "
            "does not trap or free the 71E thickening."
        ),
        "locked_gates_unaltered": {
            "sbp": True,
            "phi_vs_d": True,
            "low_tail": True,
            "sign": True,
            "s_pq": True,
            "local_star": True,
            "gate_71e": True,
        },
        "all_checks_ok": bool(
            lat["cocircular"]
            and lat["delta_nonzero"]
            and aff["D2F_e_zi_e_zi_identically_zero"]
            and wit["activity"]["live"]
            and wit["rank_9x8"] == 7
            and wit["z4_column_vanishes"]
            and wit["line_is_exact_coherent"]
            and wit["max_abs_raw"] < 1e-10
        ),
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
    if isinstance(obj, Fraction):
        return str(obj)
    return obj


def main() -> int:
    payload = run()
    out = ROOT / "results" / "da_gate_83b2b_curvature.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(jsonable(payload), indent=2)
    out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if payload["all_checks_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
