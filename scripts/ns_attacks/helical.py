"""Helical polarization frame and cubic geometric couplings.

Convention lock (Waleffe-style, not a new theory):

    p + q = k,   k ≠ 0,   p, q ≠ 0.

A right-handed orthonormal frame of k-hat is built from a
reference axis a. Then

    h_k^s = (e1 + i s e2) / √2,    s ∈ {+1, −1}.

The geometric coupling used on this page is

    g(p,q,k; σp,σq,σk)
        = (1/2)(σp |p| − σq |q|)
          (h_p^{σp} × h_q^{σq}) · conj(h_k^{σk}).

arg g is the preferred interaction offset χ_e once a frame is
chosen. Changing the reference axis is a polarization-frame
gauge; a holonomy that moves when the axis moves is not a
physical loop defect.

Not a T_c bound. NS is not solved.
"""

from __future__ import annotations

import math
from typing import Iterable, Sequence, Tuple

Mode = Tuple[int, int, int]
Vec = Tuple[float, float, float]
CVec = Tuple[complex, complex, complex]

SIGNS: Tuple[int, int] = (1, -1)


def as_mode(v: Sequence[int]) -> Mode:
    if len(v) != 3:
        raise ValueError("mode must be a 3-vector")
    return (int(v[0]), int(v[1]), int(v[2]))


def add(a: Mode, b: Mode) -> Mode:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Mode, b: Mode) -> Mode:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot_int(a: Mode, b: Mode) -> int:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm2(a: Mode) -> int:
    return dot_int(a, a)


def norm(a: Sequence[float]) -> float:
    return math.sqrt(float(a[0]) ** 2 + float(a[1]) ** 2 + float(a[2]) ** 2)


def _cross(a: Sequence[complex], b: Sequence[complex]) -> CVec:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _dot(a: Sequence[complex], b: Sequence[complex]) -> complex:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def unit(v: Sequence[float]) -> Vec:
    n = norm(v)
    if n <= 0.0:
        raise ValueError("zero vector has no unit")
    return (float(v[0]) / n, float(v[1]) / n, float(v[2]) / n)


def perp_frame(k: Sequence[float], axis: Sequence[float] = (0.0, 0.0, 1.0)) -> Tuple[Vec, Vec]:
    """Right-handed (e1, e2) with e1 × e2 = k-hat."""
    kh = unit(k)
    ax = (float(axis[0]), float(axis[1]), float(axis[2]))
    c = _cross(ax, kh)
    if abs(c[0]) + abs(c[1]) + abs(c[2]) < 1e-14:
        ax = (1.0, 0.0, 0.0) if abs(kh[0]) < 0.9 else (0.0, 1.0, 0.0)
        c = _cross(ax, kh)
    e1 = unit((c[0].real, c[1].real, c[2].real))
    e2t = _cross(kh, e1)
    e2 = (e2t[0].real, e2t[1].real, e2t[2].real)
    return e1, e2


def helical_basis(k: Sequence[float], s: int, axis: Sequence[float] = (0.0, 0.0, 1.0)) -> CVec:
    if s not in SIGNS:
        raise ValueError("helicity must be ±1")
    e1, e2 = perp_frame(k, axis)
    sct = float(s)
    inv = 1.0 / math.sqrt(2.0)
    return tuple(inv * (e1[j] + 1j * sct * e2[j]) for j in range(3))  # type: ignore[return-value]


def geometric_coupling(
    p: Sequence[int],
    q: Sequence[int],
    k: Sequence[int],
    sigma_p: int,
    sigma_q: int,
    sigma_k: int,
    axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> complex:
    """g_{pqk}^{σp σq σk}. Requires p+q=k."""
    pm, qm, km = as_mode(p), as_mode(q), as_mode(k)
    if add(pm, qm) != km:
        raise ValueError("triad must satisfy p+q=k")
    if norm2(pm) == 0 or norm2(qm) == 0 or norm2(km) == 0:
        raise ValueError("zero mode is not a helical wave")
    hp = helical_basis(pm, sigma_p, axis)
    hq = helical_basis(qm, sigma_q, axis)
    hk = helical_basis(km, sigma_k, axis)
    hk_bar = (hk[0].conjugate(), hk[1].conjugate(), hk[2].conjugate())
    geo = _dot(_cross(hp, hq), hk_bar)
    return 0.5 * (sigma_p * norm(pm) - sigma_q * norm(qm)) * geo


def all_helical_couplings(
    p: Sequence[int],
    q: Sequence[int],
    k: Sequence[int],
    axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> dict:
    """Eight helical channels and the preferred (max |g|) assignment."""
    rows = []
    best = None
    for sp in SIGNS:
        for sq in SIGNS:
            for sk in SIGNS:
                g = geometric_coupling(p, q, k, sp, sq, sk, axis)
                row = {
                    "sigma": (sp, sq, sk),
                    "g_re": g.real,
                    "g_im": g.imag,
                    "abs_g": abs(g),
                    "arg_g": math.atan2(g.imag, g.real) if abs(g) > 0.0 else 0.0,
                }
                rows.append(row)
                if best is None or row["abs_g"] > best["abs_g"] + 1e-15:
                    best = row
                elif best is not None and abs(row["abs_g"] - best["abs_g"]) <= 1e-15:
                    # Tie: keep the first in (+,+,+)-first scan only if strictly
                    # larger was not seen. Equal |g| is recorded.
                    pass
    assert best is not None
    ties = [r for r in rows if abs(r["abs_g"] - best["abs_g"]) <= 1e-12]
    return {
        "channels": rows,
        "preferred": best,
        "n_ties": len(ties),
        "tied_sigmas": [r["sigma"] for r in ties],
    }


def wrap_pi(theta: float) -> float:
    """Principal value in (−π, π]."""
    x = (float(theta) + math.pi) % (2.0 * math.pi) - math.pi
    if abs(x + math.pi) < 1e-15:
        return math.pi
    return x


AXES: Tuple[Vec, ...] = (
    (0.0, 0.0, 1.0),
    (1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
)
