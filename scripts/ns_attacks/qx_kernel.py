"""Shared kernel for Gate B Q_x tests.

September 20 C_abc majorant and the explicit nonnegative
Q_x of Dish #3. Not (17). NS is not solved.
"""

from __future__ import annotations

from math import sqrt
from typing import Iterable, Sequence


Vec = tuple[int, int, int]


def delta(a: float, b: float, c: float) -> float:
    s = (c - a - b) / 2.0
    return a * b - s * s


def collinear(a: int, b: int, c: int) -> bool:
    return (b - a - c) ** 2 == 4 * a * c


def C_abc(a: float, b: float, c: float) -> float:
    """Nonnegative September 20 majorant. Upper bound, not a cost."""
    d = delta(a, b, c)
    if d <= 0:
        return 0.0
    return sqrt(3.0 * d) * (
        abs(c - b) / sqrt(a) + abs(c - a) / sqrt(b) + abs(b - a) / sqrt(c)
    )


def radius2(k: Sequence[int]) -> int:
    return int(k[0] * k[0] + k[1] * k[1] + k[2] * k[2])


def add(p: Vec, q: Vec) -> Vec:
    return (p[0] + q[0], p[1] + q[1], p[2] + q[2])


def neg(p: Vec) -> Vec:
    return (-p[0], -p[1], -p[2])


def dot(p: Sequence[float], q: Sequence[complex]) -> complex:
    return p[0] * q[0] + p[1] * q[1] + p[2] * q[2]


def vdot(u: Sequence[complex], v: Sequence[complex]) -> complex:
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def subnet_triads(n: int) -> list[tuple[Vec, Vec, Vec, int, int, int]]:
    """Diagnostic subnet of Gate A/B.

    u=(k,0,ℓ), v=(n-k,n,-ℓ), w=(-n,-n,0), c=2n².
    Rectangle: k/n ∈ [0.3, 0.7], ℓ/n ∈ [0, 0.4].
    """
    c = 2 * n * n
    k_lo = int(0.3 * n)
    k_hi = int(0.7 * n)
    ell_hi = int(0.4 * n)
    out: list[tuple[Vec, Vec, Vec, int, int, int]] = []
    for k in range(k_lo, k_hi + 1):
        for ell in range(0, ell_hi + 1):
            u: Vec = (k, 0, ell)
            v: Vec = (n - k, n, -ell)
            w: Vec = (-n, -n, 0)
            a = radius2(u)
            b = radius2(v)
            if not (a < b < c):
                continue
            if collinear(a, b, c) or delta(a, b, c) <= 0:
                continue
            if add(u, add(v, w)) != (0, 0, 0):
                continue
            out.append((u, v, w, a, b, c))
    return out


def similar_seed_triad(n: int) -> tuple[Vec, Vec, Vec, int, int, int]:
    """One similar triad at scale n.

    Base n=4: u=(2,0,1), v=(2,4,-1), w=(-4,-4,0), interior to the
    diagnostic rectangle. For n=4t the lattice vectors are exact
    dilations, so C-homogeneity can be checked rather than fitted.
    """
    t = max(1, n // 4)
    u: Vec = (2 * t, 0, t)
    v: Vec = (2 * t, 4 * t, -t)
    w: Vec = (-4 * t, -4 * t, 0)
    a, b, c = radius2(u), radius2(v), radius2(w)
    if not (a < b < c) or collinear(a, b, c) or delta(a, b, c) <= 0:
        u = (2 * t, 0, 0)
        v = (2 * t, 4 * t, 0)
        w = (-4 * t, -4 * t, 0)
        a, b, c = radius2(u), radius2(v), radius2(w)
    return u, v, w, a, b, c


def occupied_shells(triads: Iterable[tuple[Vec, Vec, Vec, int, int, int]]) -> list[int]:
    shells: set[int] = set()
    for _u, _v, _w, a, b, c in triads:
        shells.update((a, b, c))
    return sorted(shells)


def energy_enstrophy(f: dict[int, float]) -> tuple[float, float, int]:
    E = sum(val * val for val in f.values())
    Omega = sum(x * val * val for x, val in f.items())
    Lam = max((x for x, val in f.items() if val > 0), default=0)
    return E, Omega, Lam


def nonnegative_Q(
    triads: Iterable[tuple[Vec, Vec, Vec, int, int, int]],
    f: dict[int, float],
) -> dict[int, float]:
    """Dish #3 grouping: low vertex x=a pays, Q_a = Σ C_abc f_b f_c."""
    Q: dict[int, float] = {x: 0.0 for x in f}
    for _u, _v, _w, a, b, c in triads:
        Q[a] = Q.get(a, 0.0) + C_abc(a, b, c) * f.get(b, 0.0) * f.get(c, 0.0)
    return Q


def l2(values: Iterable[float]) -> float:
    return sqrt(sum(v * v for v in values))


def equal_energy_amplitudes(shells: Sequence[int]) -> dict[int, float]:
    if not shells:
        return {}
    amp = 1.0 / sqrt(len(shells))
    return {x: amp for x in shells}


def theta_hat(ratio0: float, ratio1: float, Lam0: int, Lam1: int) -> float:
    """Effective power in ||Q||_2 / Ω  ∼  Λ^θ."""
    from math import log

    if ratio0 <= 0 or ratio1 <= 0 or Lam0 <= 0 or Lam1 <= 0 or Lam0 == Lam1:
        return float("nan")
    return log(ratio1 / ratio0) / log(Lam1 / Lam0)


def triad_T_signed(
    p: Vec,
    q: Vec,
    r: Vec,
    up: Sequence[complex],
    uq: Sequence[complex],
    ur: Sequence[complex],
) -> float:
    """Exact signed receiver form used in the Fourier-triangle audit.

    T_abc = (c-b) Im I_p + (a-c) Im I_q + (b-a) Im I_r
    with I_p = (q·u_p)(u_q·u_r) and cyclic. p+q+r=0.
    """
    a = radius2(p)
    b = radius2(q)
    c = radius2(r)
    Ip = dot(q, up) * vdot(uq, ur)
    Iq = dot(r, uq) * vdot(ur, up)
    Ir = dot(p, ur) * vdot(up, uq)
    return (c - b) * Ip.imag + (a - c) * Iq.imag + (b - a) * Ir.imag


def orthonormal_perp(k: Vec) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    kx, ky, kz = float(k[0]), float(k[1]), float(k[2])
    if abs(kx) + abs(ky) < 1e-15:
        a = (1.0, 0.0, 0.0)
    else:
        nrm = sqrt(ky * ky + kx * kx)
        a = (-ky / nrm, kx / nrm, 0.0)
    # e2 = k × e1
    e2 = (
        ky * 0.0 - kz * a[1],
        kz * a[0] - kx * 0.0,
        kx * a[1] - ky * a[0],
    )
    n2 = sqrt(e2[0] * e2[0] + e2[1] * e2[1] + e2[2] * e2[2])
    if n2 < 1e-15:
        # k parallel to e1 fallback
        e2 = (0.0, 0.0, 1.0) if abs(kz) < 0.9 * sqrt(kx * kx + ky * ky + kz * kz) else (1.0, 0.0, 0.0)
        n2 = 1.0
    e2 = (e2[0] / n2, e2[1] / n2, e2[2] / n2)
    return a, e2


def df_mode(
    k: Vec, amp: float, phase: float, pol: float
) -> tuple[complex, complex, complex]:
    """Divergence-free mode: amp e^{iφ} (cosψ e1 + sinψ e2)."""
    from math import cos, sin

    e1, e2 = orthonormal_perp(k)
    cph = complex(cos(phase), sin(phase))
    cp, sp = cos(pol), sin(pol)
    vec = (
        amp * cph * (cp * e1[0] + sp * e2[0]),
        amp * cph * (cp * e1[1] + sp * e2[1]),
        amp * cph * (cp * e1[2] + sp * e2[2]),
    )
    return vec


def df_residual(k: Vec, u: Sequence[complex]) -> float:
    return abs(dot(k, u))
