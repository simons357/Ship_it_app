"""Helical frames, Leray projection, and torus modes.

Convention lock:

    k + p + q = 0,   k, p, q ≠ 0.

Default frame: h_s(-k) = conj(h_s(k)), so a real field has
a^s(-k) = conj(a^s(k)). Planar 2D3C gauge is separate:

    h_s(k) = (n × k̂ + i s n) / √2.

Not a T_c bound. NS is not solved.
"""

from __future__ import annotations

import math
from itertools import product
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

Mode = Tuple[int, int, int]
Sigma = Tuple[int, int, int]
SIGNS: Tuple[int, int] = (1, -1)

_H_CACHE: Dict[Tuple[Mode, int, Optional[Tuple[float, float, float]]], np.ndarray] = {}


def as_mode(v: Sequence[int]) -> Mode:
    if len(v) != 3:
        raise ValueError("mode must be a 3-vector")
    return (int(v[0]), int(v[1]), int(v[2]))


def add(a: Mode, b: Mode) -> Mode:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def neg(a: Mode) -> Mode:
    return (-a[0], -a[1], -a[2])


def nrm2(a: Sequence[int]) -> int:
    return int(a[0]) * int(a[0]) + int(a[1]) * int(a[1]) + int(a[2]) * int(a[2])


def nrm(a: Sequence[float]) -> float:
    return math.sqrt(float(a[0]) ** 2 + float(a[1]) ** 2 + float(a[2]) ** 2)


def is_pos(k: Mode) -> bool:
    for x in k:
        if x > 0:
            return True
        if x < 0:
            return False
    return False


def unit(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v))
    if n <= 0.0:
        raise ValueError("zero vector has no unit")
    return v / n


def perp_frame(k: Sequence[float], axis: Sequence[float] = (0.0, 0.0, 1.0)) -> Tuple[np.ndarray, np.ndarray]:
    kh = unit(np.array(k, dtype=float))
    ax = np.array(axis, dtype=float)
    c = np.cross(ax, kh)
    if float(np.linalg.norm(c)) < 1e-14:
        ax = np.array([1.0, 0.0, 0.0]) if abs(kh[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
        c = np.cross(ax, kh)
    e1 = unit(c)
    e2 = np.cross(kh, e1)
    return e1, e2


def helical(
    k: Sequence[int],
    s: int,
    planar_n: Optional[Sequence[float]] = None,
) -> np.ndarray:
    """Return h_s(k). Cached. s ∈ {±1}."""
    if s not in SIGNS:
        raise ValueError("helicity must be ±1")
    km = as_mode(k)
    if nrm2(km) == 0:
        raise ValueError("zero mode is not a helical wave")
    nkey: Optional[Tuple[float, float, float]]
    if planar_n is None:
        nkey = None
    else:
        nkey = (float(planar_n[0]), float(planar_n[1]), float(planar_n[2]))
    key = (km, int(s), nkey)
    cached = _H_CACHE.get(key)
    if cached is not None:
        return cached
    if planar_n is not None:
        kh = unit(np.array(km, dtype=float))
        n = unit(np.array(planar_n, dtype=float))
        h = (np.cross(n, kh) + 1j * float(s) * n) / math.sqrt(2.0)
        _H_CACHE[key] = h
        return h
    if is_pos(km):
        e1, e2 = perp_frame(km)
        h = (e1 + 1j * float(s) * e2) / math.sqrt(2.0)
        _H_CACHE[key] = h
        _H_CACHE[(neg(km), int(s), None)] = np.conjugate(h)
        return h
    h = np.conjugate(helical(neg(km), s, None))
    _H_CACHE[key] = h
    return h


def clear_helical_cache() -> None:
    _H_CACHE.clear()


def leray(k: Sequence[int], v: np.ndarray) -> np.ndarray:
    kf = np.array(k, dtype=float)
    n2 = float(np.dot(kf, kf))
    if n2 == 0.0:
        return np.zeros(3, dtype=complex)
    return v - kf * (np.dot(kf, v) / n2)


def cube_modes(radius: int) -> List[Mode]:
    if radius < 1:
        raise ValueError("radius >= 1")
    return [k for k in product(range(-radius, radius + 1), repeat=3) if nrm2(k)]


def wrap_pi(theta: float) -> float:
    x = (float(theta) + math.pi) % (2.0 * math.pi) - math.pi
    if abs(x + math.pi) < 1e-15:
        return math.pi
    return x


def dist_to_real_ray(theta: float) -> float:
    """Distance of an argument to the nearest of {0, π}, in [0, π/2]."""
    t = abs(wrap_pi(theta))
    return min(t, math.pi - t)


def channel_id(k: Mode, p: Mode, q: Mode) -> frozenset:
    return frozenset((k, neg(k), p, neg(p), q, neg(q)))
