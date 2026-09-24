"""Exact Fourier-triangle geometry and identities (1)–(4), (6)–(7).

Convention: T^3 = (R/2πZ)^3, characters exp(i k · x), real mean-zero
divergence-free velocity, A = -P Δ with symbol |k|^2, B(v,w) = P[(v·∇)w].
A shell label is a squared radius.

For one interaction p+q = k:

    a = |p|^2,  b = |q|^2,  c = |k|^2,
    s = p·q = (c-a-b)/2,  Δ = ab-s^2 = |p×q|^2.

Frame: e0 = k/√c, e1 in the triangle plane ⊥ k, e2 = e0 × e1.

    p = x e0 + h e1,  q = y e0 - h e1,
    x = (c+a-b)/(2√c),  y = (c+b-a)/(2√c),  h = √(Δ/c).

Identities (1)–(4) are algebra. They do not estimate the sum over
unequal radii, nor the time integral of positive scalene transfer.
NS is not solved.
"""

from __future__ import annotations

import math
from typing import Dict, Iterable, List, Sequence, Tuple

Vec = Tuple[float, float, float]
CVec = Tuple[complex, complex, complex]
Mode = Tuple[int, int, int]


def _dot(u: Sequence[float], v: Sequence[float]) -> float:
    return float(u[0] * v[0] + u[1] * v[1] + u[2] * v[2])


def _cdot(u: Sequence[complex], v: Sequence[complex]) -> complex:
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def _cross(u: Sequence[float], v: Sequence[float]) -> Vec:
    return (
        float(u[1] * v[2] - u[2] * v[1]),
        float(u[2] * v[0] - u[0] * v[2]),
        float(u[0] * v[1] - u[1] * v[0]),
    )


def _scale(s: complex, v: Sequence[complex]) -> CVec:
    return (s * v[0], s * v[1], s * v[2])


def _add(u: Sequence[complex], v: Sequence[complex]) -> CVec:
    return (u[0] + v[0], u[1] + v[1], u[2] + v[2])


def _norm2(v: Sequence[float]) -> float:
    return _dot(v, v)


def _proj_k(k: Sequence[float], v: Sequence[complex]) -> CVec:
    c = _norm2(k)
    if c == 0:
        raise ValueError("k = 0")
    # P_k v = v - k (k·v)/|k|^2 ; bilinear, no conjugation
    kv = k[0] * v[0] + k[1] * v[1] + k[2] * v[2]
    t = kv / c
    return (v[0] - t * k[0], v[1] - t * k[1], v[2] - t * k[2])


def triangle_invariants(p: Sequence[int], q: Sequence[int]) -> dict:
    k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
    a = p[0] * p[0] + p[1] * p[1] + p[2] * p[2]
    b = q[0] * q[0] + q[1] * q[1] + q[2] * q[2]
    c = k[0] * k[0] + k[1] * k[1] + k[2] * k[2]
    s = p[0] * q[0] + p[1] * q[1] + p[2] * q[2]
    s_from_c = (c - a - b) / 2
    cross = _cross(p, q)
    delta = a * b - s * s
    return {
        "p": tuple(int(x) for x in p),
        "q": tuple(int(x) for x in q),
        "k": tuple(int(x) for x in k),
        "a": a,
        "b": b,
        "c": c,
        "s": s,
        "s_from_c": s_from_c,
        "Delta": delta,
        "cross_sq": _norm2(cross),
        "triangle_ineq": (math.sqrt(a) - math.sqrt(b)) ** 2 <= c + 1e-12
        and c <= (math.sqrt(a) + math.sqrt(b)) ** 2 + 1e-12,
        "collinear": delta == 0,
    }


def triangle_frame(p: Sequence[float], q: Sequence[float]) -> dict:
    k = (float(p[0] + q[0]), float(p[1] + q[1]), float(p[2] + q[2]))
    a = _norm2(p)
    b = _norm2(q)
    c = _norm2(k)
    s = _dot(p, q)
    delta = a * b - s * s
    if c <= 0:
        raise ValueError("k = 0")
    if delta <= 0:
        raise ValueError("collinear triangle: no (e0,e1,e2) frame")
    sc = math.sqrt(c)
    e0 = (k[0] / sc, k[1] / sc, k[2] / sc)
    x = (c + a - b) / (2 * sc)
    y = (c + b - a) / (2 * sc)
    h = math.sqrt(delta / c)
    # e1 from p - x e0 = h e1
    raw = (p[0] - x * e0[0], p[1] - x * e0[1], p[2] - x * e0[2])
    nr = math.sqrt(_norm2(raw))
    e1 = (raw[0] / nr, raw[1] / nr, raw[2] / nr)
    e2 = _cross(e0, e1)
    p_rec = (x * e0[0] + h * e1[0], x * e0[1] + h * e1[1], x * e0[2] + h * e1[2])
    q_rec = (y * e0[0] - h * e1[0], y * e0[1] - h * e1[1], y * e0[2] - h * e1[2])
    return {
        "a": a,
        "b": b,
        "c": c,
        "s": s,
        "Delta": delta,
        "x": x,
        "y": y,
        "h": h,
        "e0": e0,
        "e1": e1,
        "e2": e2,
        "p_rec": p_rec,
        "q_rec": q_rec,
        "p_err": math.sqrt(_norm2((p[0] - p_rec[0], p[1] - p_rec[1], p[2] - p_rec[2]))),
        "q_err": math.sqrt(_norm2((q[0] - q_rec[0], q[1] - q_rec[1], q[2] - q_rec[2]))),
        "k": k,
    }


def polarizations(
    frame: dict,
    A1: complex,
    A2: complex,
    B1: complex,
    B2: complex,
) -> Tuple[CVec, CVec]:
    a, b = frame["a"], frame["b"]
    x, y, h = frame["x"], frame["y"], frame["h"]
    e0, e1, e2 = frame["e0"], frame["e1"], frame["e2"]
    in_p = ((h * e0[0] - x * e1[0]) / math.sqrt(a), (h * e0[1] - x * e1[1]) / math.sqrt(a), (h * e0[2] - x * e1[2]) / math.sqrt(a))
    in_q = ((h * e0[0] + y * e1[0]) / math.sqrt(b), (h * e0[1] + y * e1[1]) / math.sqrt(b), (h * e0[2] + y * e1[2]) / math.sqrt(b))
    up = _add(_scale(A1, in_p), _scale(A2, e2))
    uq = _add(_scale(B1, in_q), _scale(B2, e2))
    return up, uq


def S_pq_direct(p: Sequence[float], q: Sequence[float], up: CVec, uq: CVec) -> CVec:
    k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
    q_up = q[0] * up[0] + q[1] * up[1] + q[2] * up[2]
    p_uq = p[0] * uq[0] + p[1] * uq[1] + p[2] * uq[2]
    raw = (q_up * uq[0] + p_uq * up[0], q_up * uq[1] + p_uq * up[1], q_up * uq[2] + p_uq * up[2])
    return _proj_k(k, raw)


def S_pq_formula(frame: dict, A1: complex, A2: complex, B1: complex, B2: complex) -> CVec:
    """Identity (1)."""
    a, b, c = frame["a"], frame["b"], frame["c"]
    h = frame["h"]
    e1, e2 = frame["e1"], frame["e2"]
    coeff1 = h * (b - a) / math.sqrt(a * b) * A1 * B1
    coeff2 = math.sqrt(c) * h * (A1 * B2 / math.sqrt(a) + A2 * B1 / math.sqrt(b))
    return _add(_scale(coeff1, e1), _scale(coeff2, e2))


def S_pq_equal_formula(alpha: float, beta: float, A1: complex, A2: complex, B1: complex, B2: complex, e2: Vec) -> CVec:
    """Identity (3): a=b=α, c=β."""
    if beta <= 0 or beta >= 4 * alpha:
        # collinear endpoints vanish
        return (0j, 0j, 0j)
    coeff = math.sqrt(beta * (1.0 - beta / (4.0 * alpha))) * (A1 * B2 + A2 * B1)
    return _scale(coeff, e2)


def unequal_defect(p: Sequence[float], q: Sequence[float], up: CVec, uq: CVec) -> dict:
    """Identity (4): (P_k p) · S_pq = ((b-a)/c) (k·u_p)(k·u_q)."""
    k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
    a = _norm2(p)
    b = _norm2(q)
    c = _norm2(k)
    Pk_p = _proj_k(k, (p[0], p[1], p[2]))
    S = S_pq_direct(p, q, up, uq)
    left = _cdot(Pk_p, S)
    k_up = k[0] * up[0] + k[1] * up[1] + k[2] * up[2]
    k_uq = k[0] * uq[0] + k[1] * uq[1] + k[2] * uq[2]
    right = ((b - a) / c) * k_up * k_uq
    t = _dot(p, k) / c
    return {
        "left": left,
        "right": right,
        "err": abs(left - right),
        "t": t,
        "one_minus_2t": 1 - 2 * t,
        "b_minus_a_over_c": (b - a) / c,
    }


def check_incompressibility(p: Sequence[float], q: Sequence[float], up: CVec, uq: CVec) -> dict:
    k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
    p_up = p[0] * up[0] + p[1] * up[1] + p[2] * up[2]
    q_uq = q[0] * uq[0] + q[1] * uq[1] + q[2] * uq[2]
    q_up = q[0] * up[0] + q[1] * up[1] + q[2] * up[2]
    p_uq = p[0] * uq[0] + p[1] * uq[1] + p[2] * uq[2]
    k_up = k[0] * up[0] + k[1] * up[1] + k[2] * up[2]
    k_uq = k[0] * uq[0] + k[1] * uq[1] + k[2] * uq[2]
    return {
        "p_up": p_up,
        "q_uq": q_uq,
        "q_up_minus_k_up": q_up - k_up,
        "p_uq_minus_k_uq": p_uq - k_uq,
    }


def T_abc(a: int, b: int, c: int, I_p: float, I_q: float, I_r: float) -> float:
    """Identity (7). Closed-triad convention: no extra conjugation or 2."""
    return (c - b) * I_p + (a - c) * I_q + (b - a) * I_r


def T_aab(a: int, b: int, tau_b_from_aa: float) -> float:
    """Identity (6)."""
    return (b - a) * tau_b_from_aa


def even_output_sum(a: int) -> dict:
    """Exact even-output polynomial after (6):

        Σ_{2 ≤ b ≤ 4a, b even} (b-a)^2 (1 - b/(4a)) = a^3 - a^2/2.
    """
    acc = 0.0
    for b in range(2, 4 * a + 1, 2):
        acc += (b - a) ** 2 * (1.0 - b / (4.0 * a))
    closed = a ** 3 - (a ** 2) / 2.0
    return {"a": a, "sum": acc, "closed": closed, "err": abs(acc - closed)}


def sixteen_ninths_gap(r: float) -> float:
    """16/9 − (3/4) r^2 (1 − r/4) = (3r+4)(3r−8)^2 / 144 ≥ 0."""
    left = 16.0 / 9.0 - 0.75 * r * r * (1.0 - r / 4.0)
    right = (3.0 * r + 4.0) * (3.0 * r - 8.0) ** 2 / 144.0
    return left - right
