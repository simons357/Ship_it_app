#!/usr/bin/env python3
"""DA script for Fourier-triangle identity (1): the S_pq decomposition.

This file exists so an auditor cannot fail-closed for "formula / DA script
not on disk." The identity is the 20 September reconstruction, equation (1).
It is algebra. It does not prove the scalene time estimate. NS is not solved.

EQUATION_1
    S_pq = [h(b-a)/√(ab)] A1 B1 e1
         + √c h (A1 B2/√a + A2 B1/√b) e2

with S_pq = P_k[(q·u_p) u_q + (p·u_q) u_p], the frame of the 20 Sep note,
and arbitrary complex divergence-free polarizations.
"""

from __future__ import annotations

import json
import math
from typing import Sequence

import sympy as sp

EQUATION_1 = (
    "S_pq = (h(b-a)/sqrt(a*b)) A1 B1 e1 "
    "+ sqrt(c) h (A1 B2/sqrt(a) + A2 B1/sqrt(b)) e2"
)

Vec = tuple[float, float, float]
CVec = tuple[complex, complex, complex]


def _dot(u: Sequence[float], v: Sequence[float]) -> float:
    return float(u[0] * v[0] + u[1] * v[1] + u[2] * v[2])


def _cross(u: Sequence[float], v: Sequence[float]) -> Vec:
    return (
        float(u[1] * v[2] - u[2] * v[1]),
        float(u[2] * v[0] - u[0] * v[2]),
        float(u[0] * v[1] - u[1] * v[0]),
    )


def _norm2(v: Sequence[float]) -> float:
    return _dot(v, v)


def _proj_k(k: Sequence[float], v: Sequence[complex]) -> CVec:
    c = _norm2(k)
    kv = k[0] * v[0] + k[1] * v[1] + k[2] * v[2]
    t = kv / c
    return (v[0] - t * k[0], v[1] - t * k[1], v[2] - t * k[2])


def S_pq_direct(p: Sequence[float], q: Sequence[float], up: CVec, uq: CVec) -> CVec:
    k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
    q_up = q[0] * up[0] + q[1] * up[1] + q[2] * up[2]
    p_uq = p[0] * uq[0] + p[1] * uq[1] + p[2] * uq[2]
    raw = (
        q_up * uq[0] + p_uq * up[0],
        q_up * uq[1] + p_uq * up[1],
        q_up * uq[2] + p_uq * up[2],
    )
    return _proj_k(k, raw)


def S_pq_formula(frame: dict, A1: complex, A2: complex, B1: complex, B2: complex) -> CVec:
    a, b, c, h = frame["a"], frame["b"], frame["c"], frame["h"]
    e1, e2 = frame["e1"], frame["e2"]
    c1 = h * (b - a) / math.sqrt(a * b) * A1 * B1
    c2 = math.sqrt(c) * h * (A1 * B2 / math.sqrt(a) + A2 * B1 / math.sqrt(b))
    return (
        c1 * e1[0] + c2 * e2[0],
        c1 * e1[1] + c2 * e2[1],
        c1 * e1[2] + c2 * e2[2],
    )


def triangle_frame(p: Sequence[float], q: Sequence[float]) -> dict:
    k = (float(p[0] + q[0]), float(p[1] + q[1]), float(p[2] + q[2]))
    a, b, c = _norm2(p), _norm2(q), _norm2(k)
    s = _dot(p, q)
    delta = a * b - s * s
    sc = math.sqrt(c)
    e0 = (k[0] / sc, k[1] / sc, k[2] / sc)
    x = (c + a - b) / (2 * sc)
    y = (c + b - a) / (2 * sc)
    h = math.sqrt(delta / c)
    raw = (p[0] - x * e0[0], p[1] - x * e0[1], p[2] - x * e0[2])
    nr = math.sqrt(_norm2(raw))
    e1 = (raw[0] / nr, raw[1] / nr, raw[2] / nr)
    e2 = _cross(e0, e1)
    return {"a": a, "b": b, "c": c, "h": h, "x": x, "y": y, "e0": e0, "e1": e1, "e2": e2}


def polarizations(frame: dict, A1: complex, A2: complex, B1: complex, B2: complex):
    a, b = frame["a"], frame["b"]
    x, y, h = frame["x"], frame["y"], frame["h"]
    e0, e1, e2 = frame["e0"], frame["e1"], frame["e2"]
    sa, sb = math.sqrt(a), math.sqrt(b)
    in_p = ((h * e0[0] - x * e1[0]) / sa, (h * e0[1] - x * e1[1]) / sa, (h * e0[2] - x * e1[2]) / sa)
    in_q = ((h * e0[0] + y * e1[0]) / sb, (h * e0[1] + y * e1[1]) / sb, (h * e0[2] + y * e1[2]) / sb)
    up = (A1 * in_p[0] + A2 * e2[0], A1 * in_p[1] + A2 * e2[1], A1 * in_p[2] + A2 * e2[2])
    uq = (B1 * in_q[0] + B2 * e2[0], B1 * in_q[1] + B2 * e2[1], B1 * in_q[2] + B2 * e2[2])
    return up, uq


def prove_equation_1_symbolic() -> dict:
    from fourier_triangles_audit import prove_S_decomposition

    return prove_S_decomposition()


def prove_equation_1_numeric() -> dict:
    samples = [
        ((2, 0, 0), (0, 3, 0), 1 + 0.2j, 0.3j, -0.4, 0.7 - 0.1j),
        ((1, 1, 0), (1, -1, 1), 0.5, -0.2j, 0.8, 1.1),
        ((3, 1, 0), (-1, 2, 1), 0.2 - 0.3j, 0.4, 0.1j, -0.6),
    ]
    worst = 0.0
    for p, q, A1, A2, B1, B2 in samples:
        fr = triangle_frame(p, q)
        up, uq = polarizations(fr, A1, A2, B1, B2)
        direct = S_pq_direct(p, q, up, uq)
        formula = S_pq_formula(fr, A1, A2, B1, B2)
        err = math.sqrt(sum(abs(direct[i] - formula[i]) ** 2 for i in range(3)))
        worst = max(worst, err)
    return {"samples": len(samples), "worst_err": worst, "held": worst < 1e-12}


def prove_all() -> dict:
    return {
        "EQUATION_1": EQUATION_1,
        "da_script": "scripts/fourier_triangle_eq1_S_pq.py",
        "symbolic": prove_equation_1_symbolic(),
        "numeric": prove_equation_1_numeric(),
        "ns_solved": False,
        "missing_theorem_17": "OPEN",
    }


def main() -> int:
    print(json.dumps(prove_all(), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
