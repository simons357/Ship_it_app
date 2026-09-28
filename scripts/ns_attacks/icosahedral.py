"""Centered icosahedron: exact geometry, not a torus Fourier orbit.

Abstract vertices in Q(φ) have a zero center, common radius, and
isotropic second moment. Distinct-vertex pair sums leave the shell,
so the twelve golden vertices are not convolution-closed on T³.

The torus-compatible stress test is the rational one-shell family
S_{a,b} with 1 < a/b < √3. Integer example (a,b)=(3,2).

NS is not solved.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Dict, List, Sequence, Tuple

import numpy as np

from ns_attacks.fourier import Mode, add, leray, nrm2
from ns_attacks.galerkin import Field, flux_stats, nonlinear


class PhiNum:
    """a + b φ with φ² = φ + 1, a,b ∈ Q."""

    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    def __add__(self, other: "PhiNum") -> "PhiNum":
        other = other if isinstance(other, PhiNum) else PhiNum(other)
        return PhiNum(self.a + other.a, self.b + other.b)

    def __sub__(self, other: "PhiNum") -> "PhiNum":
        other = other if isinstance(other, PhiNum) else PhiNum(other)
        return PhiNum(self.a - other.a, self.b - other.b)

    def __mul__(self, other: "PhiNum") -> "PhiNum":
        other = other if isinstance(other, PhiNum) else PhiNum(other)
        # (a+bφ)(c+dφ) = ac + bd + (ad+bc+bd)φ
        return PhiNum(self.a * other.a + self.b * other.b, self.a * other.b + self.b * other.a + self.b * other.b)

    def __neg__(self) -> "PhiNum":
        return PhiNum(-self.a, -self.b)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PhiNum):
            return NotImplemented
        return self.a == other.a and self.b == other.b

    def __repr__(self) -> str:
        return f"({self.a}+{self.b}*phi)"

    def is_zero(self) -> bool:
        return self.a == 0 and self.b == 0

    def as_float(self) -> float:
        phi = (1.0 + 5.0 ** 0.5) / 2.0
        return float(self.a) + float(self.b) * phi


PHI = PhiNum(0, 1)
ONE = PhiNum(1, 0)
ZERO = PhiNum(0, 0)


def icosa_vertices() -> List[Tuple[PhiNum, PhiNum, PhiNum]]:
    verts: List[Tuple[PhiNum, PhiNum, PhiNum]] = []
    for s1, s2 in product((-1, 1), repeat=2):
        verts.append((ZERO, PhiNum(s1), PhiNum(0, s2)))  # (0, ±1, ±φ)
        verts.append((PhiNum(s1), PhiNum(0, s2), ZERO))  # (±1, ±φ, 0)
        verts.append((PhiNum(0, s1), ZERO, PhiNum(s2)))  # (±φ, 0, ±1)
    return verts


def icosa_geometry() -> Dict[str, object]:
    verts = icosa_vertices()
    sx = sy = sz = ZERO
    acc = [[ZERO, ZERO, ZERO] for _ in range(3)]
    r2 = None
    for v in verts:
        sx = sx + v[0]
        sy = sy + v[1]
        sz = sz + v[2]
        rr = v[0] * v[0] + v[1] * v[1] + v[2] * v[2]
        if r2 is None:
            r2 = rr
        elif rr != r2:
            raise AssertionError("radius not common")
        for i in range(3):
            for j in range(3):
                acc[i][j] = acc[i][j] + v[i] * v[j]
    # |v|² = 1 + φ² = 1 + (φ+1) = 2+φ
    expected_r2 = PhiNum(2, 1)
    # Σ v⊗v = 4 R² I
    expected_diag = PhiNum(4, 0) * expected_r2
    pair_sums = set()
    leaves = True
    for i, v in enumerate(verts):
        for w in verts[i + 1 :]:
            s = (v[0] + w[0], v[1] + w[1], v[2] + w[2])
            ss = s[0] * s[0] + s[1] * s[1] + s[2] * s[2]
            pair_sums.add((ss.a, ss.b))
            if ss == expected_r2:
                leaves = False
    return {
        "n_vertices": len(verts),
        "sum_zero": sx.is_zero() and sy.is_zero() and sz.is_zero(),
        "R2": expected_r2,
        "radius_ok": r2 == expected_r2,
        "second_moment_isotropic": all(
            (acc[i][j] == (expected_diag if i == j else ZERO)) for i in range(3) for j in range(3)
        ),
        "pair_sum_R2_values": sorted(pair_sums),
        "pair_sums_leave_shell": leaves,
        "not_a_Z3_orbit": True,
        "not_convolution_closed": True,
    }


def rational_shell(a: int = 3, b: int = 2) -> List[Mode]:
    if not (1.0 < a / b < 3.0 ** 0.5):
        raise ValueError("need 1 < a/b < √3")
    verts = []
    for s1, s2 in product((-1, 1), repeat=2):
        verts.append((0, s1 * b, s2 * a))
        verts.append((s1 * b, s2 * a, 0))
        verts.append((s1 * a, 0, s2 * b))
    return verts


def one_shell_field(shell: Sequence[Mode], rng: np.random.Generator | None = None) -> Field:
    """Real divergence-free field supported on one eigenshell."""
    f = Field()
    rng = rng or np.random.default_rng(3)
    seen = set()
    for k in shell:
        nk = (-k[0], -k[1], -k[2])
        if k in seen or nk in seen:
            continue
        seen.add(k)
        seen.add(nk)
        v = rng.normal(size=3) + 1j * rng.normal(size=3)
        f.set(k, v)
    f.enforce_reality()
    return f


def quadratic_output_modes(shell: Sequence[Mode]) -> List[Mode]:
    out = set()
    for p in shell:
        for q in shell:
            k = add(p, q)
            if nrm2(k):
                out.add(k)
    return sorted(out)


def taylor_identities(field: Field, K: int, cutoff: Sequence[Mode]) -> Dict[str, float]:
    """One-shell identities at t=0: T_c=D_s=0, T_c' = Σ |q|²(|q|²−K)|B̂|²."""
    stats0 = flux_stats(field, cutoff)
    NL = nonlinear(field, cutoff)
    analytic_Tc_prime = 0.0
    analytic_Ds_dd = 0.0
    B_energy = 0.0
    for q, bq in NL.items():
        # B = −NL, |B̂|² = |NL|²
        eb = float(np.vdot(bq, bq).real)
        B_energy += eb
        q2 = float(nrm2(q))
        w = q2 * (q2 - float(K))
        analytic_Tc_prime += w * eb
        analytic_Ds_dd += 2.0 * q2 * (q2 - float(K)) ** 2 * eb
    outward = all(
        (nrm2(q) >= K or float(np.vdot(NL[q], NL[q]).real) < 1e-18)
        for q in NL
    )
    return {
        "T_c0": stats0["T_c"],
        "D_s0": stats0["D_s"],
        "Lambda0": stats0["Lambda"],
        "K": float(K),
        "analytic_Tc_prime": analytic_Tc_prime,
        "analytic_Ds_second": analytic_Ds_dd,
        "B_energy": B_energy,
        "outward_active": float(outward),
        "X0": stats0["X"],
    }


def finite_difference_check(field: Field, cutoff: Sequence[Mode], K: int, dt: float = 1e-5, nu: float = 0.0) -> Dict[str, float]:
    from ns_attacks.galerkin import rk4_step

    s0 = taylor_identities(field, K, cutoff)
    f1 = rk4_step(field, cutoff, nu, dt)
    f2 = rk4_step(f1, cutoff, nu, dt)
    t1 = flux_stats(f1, cutoff)
    t2 = flux_stats(f2, cutoff)
    Tc_p_fd = t1["T_c"] / dt
    Ds_pp_fd = (t2["D_s"] - 2.0 * t1["D_s"] + s0["D_s0"]) / (dt * dt)
    return {
        **s0,
        "Tc_prime_fd": Tc_p_fd,
        "Ds_second_fd": Ds_pp_fd,
        "Tc_prime_err": abs(Tc_p_fd - s0["analytic_Tc_prime"]),
        "Ds_second_rel_err": abs(Ds_pp_fd - s0["analytic_Ds_second"]) / max(1.0, abs(s0["analytic_Ds_second"])),
        "dt": dt,
    }
