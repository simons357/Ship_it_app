"""Symmetric Fourier–Galerkin Navier–Stokes on T³.

Equation: ∂t û_k = −ν |k|² û_k − NL(k),
NL(k) = i P_k Σ_{p+q=k} (û(p)·q) û(q).

Moments use ⟨u,v⟩ = Σ_k û(k)·conj(v̂(k)), so
X = |A^{1/2}u|_2² = Σ |k|² |û_k|².

Not DA-NS-2. NS is not solved.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

from ns_attacks.fourier import (
    Mode,
    add,
    cube_modes,
    helical,
    is_pos,
    leray,
    nrm,
    nrm2,
)

AmpKey = Tuple[Mode, int]


class Field:
    def __init__(self, data: Optional[Dict[Mode, np.ndarray]] = None):
        self.u: Dict[Mode, np.ndarray] = {}
        if data:
            for k, v in data.items():
                self.set(k, v)

    def copy(self) -> "Field":
        out = Field()
        out.u = {k: v.copy() for k, v in self.u.items()}
        return out

    def get(self, k: Mode) -> np.ndarray:
        return self.u.get(k, np.zeros(3, dtype=complex))

    def set(self, k: Mode, v: np.ndarray) -> None:
        v = np.array(v, dtype=complex)
        if nrm2(k) == 0 or float(np.linalg.norm(v)) < 1e-18:
            self.u.pop(k, None)
            return
        self.u[k] = leray(k, v)

    def enforce_reality(self) -> None:
        pos: Dict[Mode, np.ndarray] = {}
        for k, uk in list(self.u.items()):
            if nrm2(k) == 0:
                continue
            uk = leray(k, uk)
            if is_pos(k):
                pos[k] = uk
            else:
                pk = (-k[0], -k[1], -k[2])
                if pk not in pos:
                    pos[pk] = np.conjugate(uk)
        self.u = {}
        for k, uk in pos.items():
            self.u[k] = leray(k, uk)
            nk = (-k[0], -k[1], -k[2])
            self.u[nk] = np.conjugate(self.u[k])

    def amplitude(self, k: Mode, s: int, planar_n: Optional[Sequence[float]] = None) -> complex:
        h = helical(k, s, planar_n)
        return complex(np.vdot(h, self.get(k)))

    def from_amplitudes(
        self,
        amps: Dict[AmpKey, complex],
        planar_n: Optional[Sequence[float]] = None,
        reality: bool = True,
    ) -> "Field":
        acc: Dict[Mode, np.ndarray] = {}
        for (k, s), a in amps.items():
            acc[k] = acc.get(k, np.zeros(3, dtype=complex)) + a * helical(k, s, planar_n)
        self.u = {k: leray(k, v) for k, v in acc.items() if nrm2(k)}
        if reality:
            self.enforce_reality()
        return self

    def modes(self) -> List[Mode]:
        return list(self.u.keys())

    def energy_outside(self, keep: Iterable[Mode]) -> float:
        keep_set = set(keep)
        e = 0.0
        for k, uk in self.u.items():
            if k not in keep_set:
                e += float(np.vdot(uk, uk).real)
        return e

    def total_energy(self) -> float:
        return sum(float(np.vdot(uk, uk).real) for uk in self.u.values())


def moments(field: Field) -> Dict[str, float]:
    X = Y = Z = E = 0.0
    Ha = Da = 0.0
    for k, uk in field.u.items():
        e = float(np.vdot(uk, uk).real)
        lam = float(nrm2(k))
        r = math_sqrt(lam)
        E += e
        X += lam * e
        Y += lam * lam * e
        Z += lam * lam * lam * e
        Ha += r * e
        Da += r * r * r * e
    Lam = Y / X if X > 0.0 else 0.0
    return {
        "E": E,
        "X": X,
        "Y": Y,
        "Z": Z,
        "Lambda": Lam,
        "D_s": Z - Lam * Y,
        "H_a": Ha,
        "D_a": Da,
    }


def math_sqrt(x: float) -> float:
    return float(np.sqrt(x))


def nonlinear(field: Field, cutoff: Sequence[Mode]) -> Dict[Mode, np.ndarray]:
    cut = set(cutoff)
    NL: Dict[Mode, np.ndarray] = {k: np.zeros(3, dtype=complex) for k in cut if nrm2(k)}
    keys = list(field.u.keys())
    for p in keys:
        up = field.get(p)
        for q in keys:
            k = add(p, q)
            if nrm2(k) == 0 or k not in NL:
                continue
            qf = np.array(q, dtype=float)
            NL[k] += complex(np.dot(up, qf)) * field.get(q)
    for k in NL:
        NL[k] = 1j * leray(k, NL[k])
    return NL


def energy_pairing(field: Field, NL: Dict[Mode, np.ndarray]) -> float:
    s = 0.0j
    zero = np.zeros(3, dtype=complex)
    for k, uk in field.u.items():
        s += np.vdot(uk, NL.get(k, zero))
    return float(s.real)


def flux_stats(field: Field, cutoff: Sequence[Mode]) -> Dict[str, float]:
    m = moments(field)
    NL = nonlinear(field, cutoff)
    N = 0.0j
    M = 0.0j
    Qa = 0.0
    zero = np.zeros(3, dtype=complex)
    for k, uk in field.u.items():
        nl = NL.get(k, zero)
        lam = float(nrm2(k))
        # B = −NL, so N = −⟨B, Au⟩ = ⟨NL, Au⟩ flipped to match
        # (log Λ)' = 2/Y (T_c − ν D_s): take N,M from −NL.
        pair = complex(np.vdot(uk, -nl))
        N += lam * pair
        M += lam * lam * pair
        r = math_sqrt(lam)
        for s in (1, -1):
            a = field.amplitude(k, s)
            nl_amp = complex(np.vdot(helical(k, s), nl))
            # Q_a = ½ Ḣ_a^{NL} = Σ |k| Re(conj(a) (-NL_amp))
            Qa += r * (np.conjugate(a) * (-nl_amp)).real
    N_r, M_r = float(N.real), float(M.real)
    Tc = M_r - m["Lambda"] * N_r
    return {
        **m,
        "N": N_r,
        "M": M_r,
        "T_c": Tc,
        "Q_a": Qa,
        "energy_pairing": energy_pairing(field, NL),
    }


def rhs(field: Field, cutoff: Sequence[Mode], nu: float) -> Dict[Mode, np.ndarray]:
    NL = nonlinear(field, cutoff)
    out: Dict[Mode, np.ndarray] = {}
    for k in cutoff:
        if nrm2(k) == 0:
            continue
        uk = field.get(k)
        out[k] = -float(nu) * float(nrm2(k)) * uk - NL.get(k, np.zeros(3, dtype=complex))
    return out


def _axpy(field: Field, du: Dict[Mode, np.ndarray], dt: float) -> Field:
    out = Field()
    keys = set(field.u) | set(du)
    for k in keys:
        out.set(k, field.get(k) + dt * du.get(k, 0.0))
    out.enforce_reality()
    return out


def rk4_step(field: Field, cutoff: Sequence[Mode], nu: float, dt: float) -> Field:
    k1 = rhs(field, cutoff, nu)
    y2 = _axpy(field, k1, 0.5 * dt)
    k2 = rhs(y2, cutoff, nu)
    y3 = _axpy(field, k2, 0.5 * dt)
    k3 = rhs(y3, cutoff, nu)
    y4 = _axpy(field, k3, dt)
    k4 = rhs(y4, cutoff, nu)
    out = Field()
    keys = set(field.u) | set(cutoff)
    for k in keys:
        incr = (k1.get(k, 0.0) + 2.0 * k2.get(k, 0.0) + 2.0 * k3.get(k, 0.0) + k4.get(k, 0.0)) / 6.0
        out.set(k, field.get(k) + dt * incr)
    out.enforce_reality()
    return out


def random_cube(radius: int, rng: np.random.Generator) -> Field:
    f = Field()
    for k in cube_modes(radius):
        if not is_pos(k):
            continue
        v = rng.normal(size=3) + 1j * rng.normal(size=3)
        f.set(k, v)
    f.enforce_reality()
    return f


def six_mode_cutoff(k: Mode, p: Mode, q: Mode) -> List[Mode]:
    return [k, p, q, (-k[0], -k[1], -k[2]), (-p[0], -p[1], -p[2]), (-q[0], -q[1], -q[2])]
