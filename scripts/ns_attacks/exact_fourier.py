"""Exact Fourier arithmetic for T_c, Y, D_s on finite-support fields.

Convention
----------
Unit-measure torus T^3 = (R/2πZ)^3, orthonormal characters e^{ik·x}.
Mean-zero, divergence-free, real-valued fields:

    u(x) = sum_k v_k e^{ik·x},  k·v_k = 0,  v_{-k} = conj(v_k).

Stokes eigenvalues λ_k = |k|^2.  All linear moments and the complete
signed cascade T_c are Gaussian-rational (coefficients in Q(i)).

This module certifies those algebraic identities.  It does not evaluate
||∇u||_3 by sampled quadrature; see certified_grad_l3().
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, Iterator, List, Optional, Sequence, Tuple

KVec = Tuple[int, int, int]
Vec3 = Tuple["GQ", "GQ", "GQ"]


def _as_frac(x) -> Fraction:
    if isinstance(x, Fraction):
        return x
    if isinstance(x, GQ):
        if x.im != 0:
            raise TypeError("cannot coerce non-real Gaussian rational to Fraction")
        return x.re
    return Fraction(x)


@dataclass(frozen=True)
class GQ:
    """Gaussian rational a + b i, a, b ∈ Q."""

    re: Fraction
    im: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        object.__setattr__(self, "re", _as_frac(self.re))
        object.__setattr__(self, "im", _as_frac(self.im))

    @staticmethod
    def from_int(n: int) -> "GQ":
        return GQ(Fraction(n), Fraction(0))

    def __add__(self, other: object) -> "GQ":
        o = other if isinstance(other, GQ) else GQ(_as_frac(other))
        return GQ(self.re + o.re, self.im + o.im)

    def __radd__(self, other: object) -> "GQ":
        return self + other

    def __sub__(self, other: object) -> "GQ":
        o = other if isinstance(other, GQ) else GQ(_as_frac(other))
        return GQ(self.re - o.re, self.im - o.im)

    def __rsub__(self, other: object) -> "GQ":
        return GQ(_as_frac(other)) - self

    def __neg__(self) -> "GQ":
        return GQ(-self.re, -self.im)

    def __mul__(self, other: object) -> "GQ":
        o = other if isinstance(other, GQ) else GQ(_as_frac(other))
        return GQ(
            self.re * o.re - self.im * o.im,
            self.re * o.im + self.im * o.re,
        )

    def __rmul__(self, other: object) -> "GQ":
        return self * other

    def __truediv__(self, other: object) -> "GQ":
        o = other if isinstance(other, GQ) else GQ(_as_frac(other))
        denom = o.abs2()
        if denom == 0:
            raise ZeroDivisionError("Gaussian rational division by zero")
        conj = o.conj()
        num = self * conj
        return GQ(num.re / denom, num.im / denom)

    def conj(self) -> "GQ":
        return GQ(self.re, -self.im)

    def abs2(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def is_zero(self) -> bool:
        return self.re == 0 and self.im == 0


ZERO = GQ(0)
ONE = GQ(1)
I = GQ(0, 1)


def vadd(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vscale(c: GQ, a: Vec3) -> Vec3:
    return (c * a[0], c * a[1], c * a[2])


def vdot_bilinear(a: Vec3, b: Vec3) -> GQ:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vdot_k(k: KVec, a: Vec3) -> GQ:
    return GQ(k[0]) * a[0] + GQ(k[1]) * a[1] + GQ(k[2]) * a[2]


def vabs2(a: Vec3) -> Fraction:
    return a[0].abs2() + a[1].abs2() + a[2].abs2()


def vconj(a: Vec3) -> Vec3:
    return (a[0].conj(), a[1].conj(), a[2].conj())


def vneg(a: Vec3) -> Vec3:
    return (-a[0], -a[1], -a[2])


def lam(k: KVec) -> int:
    return k[0] * k[0] + k[1] * k[1] + k[2] * k[2]


def kneg(k: KVec) -> KVec:
    return (-k[0], -k[1], -k[2])


def kadd(p: KVec, q: KVec) -> KVec:
    return (p[0] + q[0], p[1] + q[1], p[2] + q[2])


def kdot(p: KVec, q: KVec) -> int:
    return p[0] * q[0] + p[1] * q[1] + p[2] * q[2]


def project_perp(k: KVec, w: Vec3) -> Vec3:
    """Leray plane: w - ((k·w)/λ_k) k.  Stays in Q(i)^3."""
    lmb = lam(k)
    if lmb == 0:
        raise ValueError("k=0 has no perpendicular plane")
    coeff = vdot_k(k, w) / GQ(lmb)
    return (
        w[0] - coeff * GQ(k[0]),
        w[1] - coeff * GQ(k[1]),
        w[2] - coeff * GQ(k[2]),
    )


def integer_perp(k: KVec) -> KVec:
    """A nonzero integer vector orthogonal to k."""
    if k[1] != 0 or k[2] != 0:
        return (0, k[2], -k[1])
    return (0, 1, 0)


def gq_vec(xyz: Sequence) -> Vec3:
    out = []
    for component in xyz:
        if isinstance(component, GQ):
            out.append(component)
        else:
            out.append(GQ(_as_frac(component)))
    if len(out) != 3:
        raise ValueError("need a 3-vector")
    return (out[0], out[1], out[2])


class Field:
    """Finite-support, divergence-free, reality-enforced Fourier field."""

    def __init__(self) -> None:
        self.modes: Dict[KVec, Vec3] = {}

    def set_mode(self, k: KVec, w: Sequence) -> None:
        k = (int(k[0]), int(k[1]), int(k[2]))
        if k == (0, 0, 0):
            raise ValueError("mean-zero: cannot set the k=0 mode")
        vk = project_perp(k, gq_vec(w))
        self.modes[k] = vk
        self.modes[kneg(k)] = vconj(vk)

    def add_mode(self, k: KVec, w: Sequence) -> None:
        k = (int(k[0]), int(k[1]), int(k[2]))
        existing = self.modes.get(k, (ZERO, ZERO, ZERO))
        self.set_mode(k, vadd(existing, project_perp(k, gq_vec(w))))

    def scale(self, a) -> "Field":
        c = a if isinstance(a, GQ) else GQ(_as_frac(a))
        out = Field()
        for k, vk in self.modes.items():
            out.modes[k] = vscale(c, vk)
        return out

    def support(self) -> List[KVec]:
        return list(self.modes.keys())

    def energy(self) -> Fraction:
        return sum((vabs2(vk) for vk in self.modes.values()), Fraction(0))

    def check_invariants(self) -> None:
        for k, vk in self.modes.items():
            if vdot_k(k, vk).abs2() != 0:
                raise RuntimeError(f"divergence-free failed at {k}")
            nk = kneg(k)
            if nk not in self.modes:
                raise RuntimeError(f"reality missing conjugate of {k}")
            diff = vadd(self.modes[nk], vneg(vconj(vk)))
            if vabs2(diff) != 0:
                raise RuntimeError(f"reality failed at {k}")


@dataclass(frozen=True)
class Moments:
    E: Fraction
    X: Fraction
    Y: Fraction
    Z: Fraction
    Lambda: Fraction
    Ds_moment: Fraction
    Ds_variance: Fraction
    Ds_pairwise: Fraction

    @property
    def D_s(self) -> Fraction:
        return self.Ds_moment


def moments(field: Field) -> Moments:
    E = X = Y = Z = Fraction(0)
    energies: Dict[KVec, Fraction] = {}
    lambdas: Dict[KVec, int] = {}
    for k, vk in field.modes.items():
        e = vabs2(vk)
        lmb = lam(k)
        energies[k] = e
        lambdas[k] = lmb
        E += e
        X += lmb * e
        Y += lmb * lmb * e
        Z += lmb * lmb * lmb * e
    if X == 0:
        return Moments(
            E=E,
            X=X,
            Y=Y,
            Z=Z,
            Lambda=Fraction(0),
            Ds_moment=Fraction(0),
            Ds_variance=Fraction(0),
            Ds_pairwise=Fraction(0),
        )
    Lambda = Y / X
    Ds_moment = Z - (Y * Y) / X
    Ds_var = Fraction(0)
    for k, e in energies.items():
        lmb = lambdas[k]
        Ds_var += lmb * (lmb - Lambda) ** 2 * e
    pair = Fraction(0)
    keys = list(energies)
    for k in keys:
        for ell in keys:
            lk, le = lambdas[k], lambdas[ell]
            pair += lk * le * (lk - le) ** 2 * energies[k] * energies[ell]
    Ds_pair = pair / (2 * X)
    return Moments(
        E=E,
        X=X,
        Y=Y,
        Z=Z,
        Lambda=Lambda,
        Ds_moment=Ds_moment,
        Ds_variance=Ds_var,
        Ds_pairwise=Ds_pair,
    )


def two_shell_D_s(alpha: int, beta: int, e_alpha: Fraction, e_beta: Fraction) -> Fraction:
    if alpha == beta:
        return Fraction(0)
    X = alpha * e_alpha + beta * e_beta
    if X == 0:
        return Fraction(0)
    return Fraction(alpha * beta * (alpha - beta) ** 2) * e_alpha * e_beta / X


def shell_energy(field: Field, n: int) -> Fraction:
    return sum((vabs2(vk) for k, vk in field.modes.items() if lam(k) == n), Fraction(0))


def triad_S_at(field: Field, k: KVec) -> Vec3:
    """S_k = sum_{p+q=k} (q·v_p) v_q, both parents occupied."""
    total = (ZERO, ZERO, ZERO)
    for p, vp in field.modes.items():
        q = (k[0] - p[0], k[1] - p[1], k[2] - p[2])
        if q == (0, 0, 0):
            continue
        vq = field.modes.get(q)
        if vq is None:
            continue
        coeff = vdot_k(q, vp)
        total = vadd(total, vscale(coeff, vq))
    return total


def T_k_from_S(S: Vec3, vk: Vec3) -> Fraction:
    """T_k = Im(S · conj(v_k)) = -Re(i S · conj(v_k))."""
    prod = vdot_bilinear(S, vconj(vk))
    return prod.im


def transfer_map(field: Field) -> Dict[KVec, Fraction]:
    out: Dict[KVec, Fraction] = {}
    for k, vk in field.modes.items():
        out[k] = T_k_from_S(triad_S_at(field, k), vk)
    return out


def T_c_from_transfers(transfers: Dict[KVec, Fraction], Lambda: Fraction) -> Fraction:
    total = Fraction(0)
    for k, Tk in transfers.items():
        lmb = lam(k)
        total += lmb * (lmb - Lambda) * Tk
    return total


def N_M_from_transfers(transfers: Dict[KVec, Fraction]) -> Tuple[Fraction, Fraction]:
    N = Fraction(0)
    M = Fraction(0)
    for k, Tk in transfers.items():
        lmb = lam(k)
        N += lmb * Tk
        M += lmb * lmb * Tk
    return N, M


@dataclass(frozen=True)
class Cascade:
    transfers: Dict[KVec, Fraction]
    N: Fraction
    M: Fraction
    T_c: Fraction
    T_c_from_MN: Fraction
    sum_T: Fraction


def cascade(field: Field, Lambda: Fraction) -> Cascade:
    transfers = transfer_map(field)
    N, M = N_M_from_transfers(transfers)
    Tc = T_c_from_transfers(transfers, Lambda)
    Tc_mn = M - Lambda * N
    sum_T = sum(transfers.values(), Fraction(0))
    return Cascade(
        transfers=transfers,
        N=N,
        M=M,
        T_c=Tc,
        T_c_from_MN=Tc_mn,
        sum_T=sum_T,
    )


def abs2_grad_spectrum(field: Field) -> Dict[KVec, GQ]:
    """Fourier coefficients of |∇u|_F^2.

    c_m = -sum_{p+q=m} (p·q) (v_p · v_q)  (bilinear dot).
    Then c_0 = X and ||∇u||_4^4 = sum_m |c_m|^2 on the unit-measure torus.
    """
    coeffs: Dict[KVec, GQ] = {}
    keys = list(field.modes)
    for p in keys:
        vp = field.modes[p]
        for q in keys:
            m = kadd(p, q)
            contrib = GQ(-kdot(p, q)) * vdot_bilinear(vp, field.modes[q])
            coeffs[m] = coeffs.get(m, ZERO) + contrib
    return coeffs


@dataclass(frozen=True)
class GradL3Certificate:
    """Certified bounds for ||∇u||_3.  No sampled quadrature.

    On the unit-measure torus, ||·||_p is nondecreasing in p, so
    √X = ||∇u||_2 ≤ ||∇u||_3.  Riesz–Thorin interpolation gives

        ||∇u||_3 ≤ ||∇u||_2^{1/3} ||∇u||_4^{2/3} = (X · ||∇u||_4^4)^{1/6}.

    ||∇u||_4^4 is an exact Fraction (Parseval on |∇u|^2).  Sixth-power
    comparisons therefore stay in Q.  The triangle / L^∞ bound is a
    coarser rational upper bound, recorded only as a check.
    """

    X: Fraction
    Y: Fraction
    D_s: Fraction
    T_c: Fraction
    L4_fourth: Fraction
    L3_ub_sixth: Fraction
    Q_ub_sq: Optional[Fraction]
    Q_lb_sixth: Optional[Fraction]
    c0_minus_X: Fraction
    vacuous: bool

    def l3_lower_sq(self) -> Fraction:
        """(||∇u||_3 lower bound)^2 = X."""
        return self.X

    def display(self) -> dict:
        import math

        def f(x: Optional[Fraction]):
            if x is None:
                return None
            return float(x)

        L3_lb = math.sqrt(float(self.X)) if self.X >= 0 else None
        L3_ub = (float(self.L3_ub_sixth) ** (1.0 / 6.0)) if self.L3_ub_sixth >= 0 else None
        Q_ub = math.sqrt(float(self.Q_ub_sq)) if self.Q_ub_sq is not None else None
        Q_lb = (float(self.Q_lb_sixth) ** (1.0 / 6.0)) if self.Q_lb_sixth is not None else None
        return {
            "X": f(self.X),
            "Y": f(self.Y),
            "D_s": f(self.D_s),
            "T_c": f(self.T_c),
            "||∇u||_3_lb": L3_lb,
            "||∇u||_3_ub": L3_ub,
            "Q_ub": Q_ub,
            "Q_lb": Q_lb,
            "vacuous": self.vacuous,
        }


def certified_grad_l3(field: Field, mom: Optional[Moments] = None, cas: Optional[Cascade] = None) -> GradL3Certificate:
    mom = mom if mom is not None else moments(field)
    cas = cas if cas is not None else cascade(field, mom.Lambda)
    spec = abs2_grad_spectrum(field)
    L4_fourth = sum((c.abs2() for c in spec.values()), Fraction(0))
    c0 = spec.get((0, 0, 0), ZERO)
    if c0.im != 0:
        raise RuntimeError("|∇u|^2 zero-mode is not real")
    c0_minus_X = c0.re - mom.X
    L3_ub_sixth = mom.X * L4_fourth
    vacuous = mom.D_s == 0 or mom.Y == 0
    if vacuous:
        Q_ub_sq = None
        Q_lb_sixth = None
    else:
        Tc2 = cas.T_c * cas.T_c
        Q_ub_sq = Tc2 / (mom.X * mom.Y * mom.D_s)
        Q_lb_sixth = (Tc2 ** 3) / (L3_ub_sixth * (mom.Y * mom.D_s) ** 3)
    return GradL3Certificate(
        X=mom.X,
        Y=mom.Y,
        D_s=mom.D_s,
        T_c=cas.T_c,
        L4_fourth=L4_fourth,
        L3_ub_sixth=L3_ub_sixth,
        Q_ub_sq=Q_ub_sq,
        Q_lb_sixth=Q_lb_sixth,
        c0_minus_X=c0_minus_X,
        vacuous=vacuous,
    )


@dataclass
class IdentityReport:
    ok: bool
    failures: List[str]

    def raise_if_failed(self) -> None:
        if not self.ok:
            raise RuntimeError("identity failures: " + "; ".join(self.failures))


def verify_identities(field: Field) -> IdentityReport:
    """Exact identities.  A successful check is not the uniform estimate."""
    failures: List[str] = []
    try:
        field.check_invariants()
    except RuntimeError as exc:
        failures.append(str(exc))
        return IdentityReport(ok=False, failures=failures)

    mom = moments(field)
    if mom.Ds_moment != mom.Ds_variance:
        failures.append(
            f"D_s moment vs variance: {mom.Ds_moment} != {mom.Ds_variance}"
        )
    if mom.Ds_moment != mom.Ds_pairwise:
        failures.append(
            f"D_s moment vs pairwise: {mom.Ds_moment} != {mom.Ds_pairwise}"
        )
    cas = cascade(field, mom.Lambda)
    if cas.T_c != cas.T_c_from_MN:
        failures.append(f"T_c vs M-ΛN: {cas.T_c} != {cas.T_c_from_MN}")
    if cas.sum_T != 0:
        failures.append(f"energy conservation sum T_k = {cas.sum_T} != 0")
    cert = certified_grad_l3(field, mom, cas)
    if cert.c0_minus_X != 0:
        failures.append(f"|∇u|^2 zero-mode {cert.c0_minus_X + mom.X} != X={mom.X}")
    if cert.L4_fourth < 0:
        failures.append("||∇u||_4^4 negative")
    if not cert.vacuous and cert.Q_lb_sixth is not None and cert.Q_ub_sq is not None:
        # Q_lb ≤ Q_ub  iff  Q_lb^6 ≤ Q_ub^6 = (Q_ub_sq)^3
        if cert.Q_lb_sixth > cert.Q_ub_sq ** 3:
            failures.append("certified Q_lb exceeds Q_ub (bound bug)")
    return IdentityReport(ok=not failures, failures=failures)


def iterate_phase_locks() -> Iterator[GQ]:
    for z in (ONE, -ONE, I, -I):
        yield z
