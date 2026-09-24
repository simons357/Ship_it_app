#!/usr/bin/env python3
"""20 September 2026 Fourier-triangle audit checks.

Exact algebra and finite rational regressions only.
Equation (17) is not proved here. NS is not solved.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import product
from math import isqrt
from typing import Iterable

# ---------------------------------------------------------------------------
# Complex rationals (Gaussian-rational arithmetic)
# ---------------------------------------------------------------------------


class C:
    """a + b i with a, b rational. Exact."""

    __slots__ = ("re", "im")

    def __init__(self, re=0, im=0):
        self.re = Fraction(re)
        self.im = Fraction(im)

    def __add__(self, other):
        other = _as_c(other)
        return C(self.re + other.re, self.im + other.im)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        other = _as_c(other)
        return C(self.re - other.re, self.im - other.im)

    def __neg__(self):
        return C(-self.re, -self.im)

    def __mul__(self, other):
        other = _as_c(other)
        return C(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def __rmul__(self, other):
        return self * other

    def conjugate(self):
        return C(self.re, -self.im)

    def __eq__(self, other):
        other = _as_c(other)
        return self.re == other.re and self.im == other.im

    def abs2(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def __repr__(self):
        return f"C({self.re}, {self.im})"


def _as_c(z) -> C:
    if isinstance(z, C):
        return z
    return C(z, 0)


Vec = tuple[C, C, C]
KVec = tuple[int, int, int]


def vadd(u: Vec, v: Vec) -> Vec:
    return (u[0] + v[0], u[1] + v[1], u[2] + v[2])


def vscale(s, u: Vec) -> Vec:
    s = _as_c(s)
    return (s * u[0], s * u[1], s * u[2])


def vdot(u: Vec, v: Vec) -> C:
    """Complex bilinear (no conjugation). Wavevectors are real."""
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def vherm(u: Vec, v: Vec) -> C:
    """u · conjugate(v)."""
    return u[0] * v[0].conjugate() + u[1] * v[1].conjugate() + u[2] * v[2].conjugate()


def vabs2(u: Vec) -> Fraction:
    return u[0].abs2() + u[1].abs2() + u[2].abs2()


def kdot(k: KVec, u: Vec) -> C:
    return C(k[0]) * u[0] + C(k[1]) * u[1] + C(k[2]) * u[2]


def kabs2(k: KVec) -> int:
    return k[0] * k[0] + k[1] * k[1] + k[2] * k[2]


def project_k(k: KVec, u: Vec) -> Vec:
    c = kabs2(k)
    if c == 0:
        return u
    t = kdot(k, u) * C(Fraction(1, c))
    return (u[0] - C(k[0]) * t, u[1] - C(k[1]) * t, u[2] - C(k[2]) * t)


# ---------------------------------------------------------------------------
# Hilbert symbol on Q_ℓ  (Serre, Course in Arithmetic)
# ---------------------------------------------------------------------------


def _factor_p(n: int, p: int) -> tuple[int, int]:
    sign = 1 if n > 0 else -1
    n = abs(n)
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v, sign * n


def _legendre(a: int, p: int) -> int:
    r = pow(a % p, (p - 1) // 2, p)
    return -1 if r == p - 1 else r


def hilbert_symbol(a: int, b: int, p: int) -> int:
    """(a, b)_p ∈ {±1} for nonzero integers a, b and prime p."""
    if a == 0 or b == 0:
        raise ValueError("Hilbert symbol on Q_p^*")
    if p == 2:
        va, ua = _factor_p(a, 2)
        vb, ub = _factor_p(b, 2)

        def eps(u: int) -> int:
            return ((u * u - 1) // 8) % 2

        def omega(u: int) -> int:
            return 0 if u % 4 == 1 else 1

        exp = eps(ua) * eps(ub) + va * omega(ub) + vb * omega(ua)
        return -1 if exp % 2 else 1

    va, ua = _factor_p(a, p)
    vb, ub = _factor_p(b, p)
    sign = 1
    if (va * vb * ((p - 1) // 2)) % 2 == 1:
        sign = -1
    if vb % 2:
        sign *= _legendre(ua, p)
    if va % 2:
        sign *= _legendre(ub, p)
    return sign


def primes_dividing(n: int) -> list[int]:
    n = abs(n)
    out: list[int] = []
    if n % 2 == 0:
        out.append(2)
        while n % 2 == 0:
            n //= 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 2
    if n > 1:
        out.append(n)
    return out


def gram_delta(a: int, b: int, s: int) -> int:
    return a * b - s * s


def i3_local_symbols(a: int, delta: int) -> dict[int, int]:
    """Product (a,Δ)_ℓ (a,-1)_ℓ (Δ,-1)_ℓ for every ℓ | 2aΔ."""
    if a == 0 or delta == 0:
        raise ValueError("nondegenerate Gram required")
    out = {}
    for ell in primes_dividing(2 * a * delta):
        out[ell] = (
            hilbert_symbol(a, delta, ell)
            * hilbert_symbol(a, -1, ell)
            * hilbert_symbol(delta, -1, ell)
        )
    return out


def i3_criterion(a: int, b: int, s: int) -> dict:
    """Finite local test (12). Existence only; not amplitudes."""
    delta = gram_delta(a, b, s)
    symbols = i3_local_symbols(a, delta)
    failing = sorted(p for p, val in symbols.items() if val != 1)
    return {
        "a": a,
        "b": b,
        "s": s,
        "delta": delta,
        "symbols": {str(p): val for p, val in symbols.items()},
        "failing": failing,
        "passes": failing == [],
        "real_ok": a > 0 and delta > 0,
    }


I3_REGRESSION = (
    ((96, 96, 0), [2, 3]),
    ((2, 3, 1), [2, 5]),
    ((2, 2, -1), []),
    ((14, 14, -7), []),
)


def i3_regression() -> list[dict]:
    rows = []
    for gram, expected_fail in I3_REGRESSION:
        row = i3_criterion(*gram)
        row["expected_fail"] = list(expected_fail)
        row["matches"] = row["failing"] == list(expected_fail)
        rows.append(row)
    return rows


def monochromatic_s(alpha: int) -> Fraction:
    """a = b = c = α forces s = -α/2."""
    return Fraction(-alpha, 2)


# ---------------------------------------------------------------------------
# Boxed polynomial identities
# ---------------------------------------------------------------------------


def sixteen_ninths_gap(r: Fraction) -> Fraction:
    """16/9 − (3/4) r² (1 − r/4) = (3r+4)(3r−8)² / 144."""
    left = Fraction(16, 9) - Fraction(3, 4) * r * r * (1 - r / 4)
    right = (3 * r + 4) * (3 * r - 8) ** 2 / 144
    if left != right:
        raise AssertionError((left, right))
    return left


def even_output_weighted_sum(a: int) -> Fraction:
    """∑_{b even, 2≤b≤4a} (b−a)² (1 − b/(4a)) = a³ − a²/2."""
    total = Fraction(0)
    for b in range(2, 4 * a + 1, 2):
        total += (b - a) ** 2 * (1 - Fraction(b, 4 * a))
    return total


def even_output_closed(a: int) -> Fraction:
    return Fraction(a**3) - Fraction(a * a, 2)


def young_rep_split(X: Fraction, Y: Fraction, nu: Fraction) -> bool:
    """(√3/2) X √Y ≤ (3ν/4) Y + X²/(4ν), checked by squaring the AM-GM form."""
    # 3ν Y + X²/ν ≥ 2√3 X √Y, i.e. the displayed Young after ×4.
    left = 3 * nu * Y + (X * X) / nu
    # Compare left² ≥ (2√3 X √Y)² = 12 X² Y, avoiding the outer square root.
    return left * left >= 12 * X * X * Y


# ---------------------------------------------------------------------------
# S_pq geometry (float check of boxed identities (1), (3), (4))
# ---------------------------------------------------------------------------


def _cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def _dot3(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def _scale3(s, u):
    return (s * u[0], s * u[1], s * u[2])


def _add3(u, v):
    return (u[0] + v[0], u[1] + v[1], u[2] + v[2])


def triangle_frame(p: KVec, q: KVec):
    k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
    a = float(kabs2(p))
    b = float(kabs2(q))
    c = float(kabs2(k))
    s = (c - a - b) / 2.0
    delta = a * b - s * s
    sc = c**0.5
    e0 = _scale3(1.0 / sc, k)
    x = (c + a - b) / (2.0 * sc)
    y = (c + b - a) / (2.0 * sc)
    h = (delta / c) ** 0.5
    # p = x e0 + h e1  ⇒  e1 = (p − x e0)/h
    e1 = _scale3(1.0 / h, _add3(p, _scale3(-x, e0)))
    e2 = _cross(e0, e1)
    return {
        "p": p,
        "q": q,
        "k": k,
        "a": a,
        "b": b,
        "c": c,
        "s": s,
        "delta": delta,
        "x": x,
        "y": y,
        "h": h,
        "e0": e0,
        "e1": e1,
        "e2": e2,
    }


def polarizations(fr, A1, A2, B1, B2):
    sa, sb = fr["a"] ** 0.5, fr["b"] ** 0.5
    up_in = _add3(_scale3(fr["h"], fr["e0"]), _scale3(-fr["x"], fr["e1"]))
    uq_in = _add3(_scale3(fr["h"], fr["e0"]), _scale3(fr["y"], fr["e1"]))
    up = _add3(_scale3(A1 / sa, up_in), _scale3(A2, fr["e2"]))
    uq = _add3(_scale3(B1 / sb, uq_in), _scale3(B2, fr["e2"]))
    return up, uq


def S_pq_definition(fr, up, uq):
    k = fr["k"]
    q_up = _dot3(fr["q"], up)
    p_uq = _dot3(fr["p"], uq)
    raw = _add3(_scale3(q_up, uq), _scale3(p_uq, up))
    kk = fr["c"]
    t = _dot3(k, raw) / kk
    return _add3(raw, _scale3(-t, k))


def S_pq_boxed(fr, A1, A2, B1, B2):
    sa, sb = fr["a"] ** 0.5, fr["b"] ** 0.5
    term1 = _scale3(fr["h"] * (fr["b"] - fr["a"]) / (sa * sb) * A1 * B1, fr["e1"])
    mix = A1 * B2 / sa + A2 * B1 / sb
    term2 = _scale3((fr["c"] ** 0.5) * fr["h"] * mix, fr["e2"])
    return _add3(term1, term2)


def S_pq_equal_boxed(fr, A1, A2, B1, B2):
    """Equation (3): a = b = α, c = β."""
    factor = (fr["c"] * (1.0 - fr["c"] / (4.0 * fr["a"]))) ** 0.5
    return _scale3(factor * (A1 * B2 + A2 * B1), fr["e2"])


def unequal_defect(fr, up, uq, S):
    """(P_k p) · S  vs  ((b−a)/c) (k·u_p)(k·u_q)."""
    k = fr["k"]
    t = _dot3(fr["p"], k) / fr["c"]
    Pk_p = _add3(fr["p"], _scale3(-t, k))
    left = _dot3(Pk_p, S)
    right = ((fr["b"] - fr["a"]) / fr["c"]) * _dot3(k, up) * _dot3(k, uq)
    return left, right


# ---------------------------------------------------------------------------
# Fourier fields and exact transfer
# ---------------------------------------------------------------------------

Field = dict[KVec, Vec]


def hermitize(modes: Field) -> Field:
    out = dict(modes)
    for k, uk in list(modes.items()):
        mk = (-k[0], -k[1], -k[2])
        conj = (uk[0].conjugate(), uk[1].conjugate(), uk[2].conjugate())
        if mk in out and out[mk] != conj:
            raise ValueError(f"Hermitian clash at {mk}")
        out[mk] = conj
    return out


def moments_field(field: Field) -> dict:
    E = Fraction(0)
    X = Fraction(0)
    Y = Fraction(0)
    Z = Fraction(0)
    for k, uk in field.items():
        m = vabs2(uk)
        lam = kabs2(k)
        E += m
        X += lam * m
        Y += lam * lam * m
        Z += lam * lam * lam * m
    return {"E": E, "X": X, "Y": Y, "Z": Z}


def bilinear_B(field: Field, k: KVec) -> Vec:
    acc: Vec = (C(0), C(0), C(0))
    for p, up in field.items():
        q = (k[0] - p[0], k[1] - p[1], k[2] - p[2])
        uq = field.get(q)
        if uq is None:
            continue
        coeff = kdot(q, up)
        acc = vadd(acc, vscale(coeff, uq))
    projected = project_k(k, acc)
    return vscale(C(0, 1), projected)


def tau_k(field: Field, k: KVec) -> Fraction:
    uk = field.get(k)
    if uk is None:
        return Fraction(0)
    Bk = bilinear_B(field, k)
    # −Re[B · conjugate(u_k)]
    z = vdot(Bk, (uk[0].conjugate(), uk[1].conjugate(), uk[2].conjugate()))
    return -z.re


def energy_transfer(field: Field) -> Fraction:
    return sum((tau_k(field, k) for k in field), Fraction(0))


def enstrophy_transfer(field: Field) -> Fraction:
    return sum((kabs2(k) * tau_k(field, k) for k in field), Fraction(0))


def example_field(kind: str) -> Field:
    """u = (2 cos 2y, 0, 2 cos 3x + f(3x+2y))."""
    e1 = (C(1), C(0), C(0))
    e3 = (C(0), C(0), C(1))
    modes: Field = {
        (0, 2, 0): e1,
        (3, 0, 0): e3,
    }
    if kind == "cos":
        modes[(3, 2, 0)] = e3
    elif kind == "sin":
        modes[(3, 2, 0)] = (C(0), C(0), C(0, -1))
    elif kind == "msin":
        modes[(3, 2, 0)] = (C(0), C(0), C(0, 1))
    else:
        raise ValueError(kind)
    return hermitize(modes)


def odd_triad_field(A: Fraction) -> Field:
    """p=(2,0,0), q=(0,3,0), k=(2,3,0); iA e2, iA e3, iA e3."""
    iA = C(0, A)
    return hermitize(
        {
            (2, 0, 0): (C(0), iA, C(0)),
            (0, 3, 0): (C(0), C(0), iA),
            (2, 3, 0): (C(0), C(0), iA),
        }
    )


def shear_field() -> Field:
    """w = (sin y, sin z, sin x)."""
    half = C(0, Fraction(-1, 2))
    return hermitize(
        {
            (0, 1, 0): (half, C(0), C(0)),
            (0, 0, 1): (C(0), half, C(0)),
            (1, 0, 0): (C(0), C(0), half),
        }
    )


def shear_output_on_beta2(field: Field) -> dict:
    keys = []
    for sx, sy, sz in product((-1, 0, 1), repeat=3):
        k = (sx, sy, sz)
        if kabs2(k) != 2:
            continue
        Bk = bilinear_B(field, k)
        if vabs2(Bk) != 0:
            keys.append((k, Bk))
    norm2 = sum((vabs2(Bk) for _, Bk in keys), Fraction(0))
    return {"n_nonzero": len(keys), "norm2": norm2, "keys": [k for k, _ in keys]}


def generated_mode_B(field: Field, k: KVec) -> Vec:
    return bilinear_B(field, k)


# ---------------------------------------------------------------------------
# Exact-sphere incidence (8), small check
# ---------------------------------------------------------------------------


def lattice_shell(alpha: int) -> list[KVec]:
    pts = []
    r = isqrt(alpha)
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            z2 = alpha - x * x - y * y
            if z2 < 0:
                continue
            z = isqrt(z2)
            if z * z != z2:
                continue
            pts.append((x, y, z))
            if z:
                pts.append((x, y, -z))
    return pts


def exact_sphere_L2(alpha: int, beta: int, weights: dict[KVec, int] | None = None):
    shell = lattice_shell(alpha)
    if weights is None:
        weights = {p: 1 for p in shell}
    F = sum(w * w for w in weights.values())
    L2 = 0
    # outputs on |k|² = β
    seen = set()
    for p in shell:
        for q in shell:
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if kabs2(k) != beta:
                continue
            seen.add(k)
    for k in seen:
        L = 0
        for p in shell:
            q = (k[0] - p[0], k[1] - p[1], k[2] - p[2])
            if q in weights and p in weights:
                L += weights[p] * weights[q]
        L2 += L * L
    return {"F": F, "L2": L2, "bound": 3 * F * F, "ok": L2 <= 3 * F * F}


# ---------------------------------------------------------------------------
# Scalene identity (7) on the odd triad
# ---------------------------------------------------------------------------


def scalene_I_and_T(field: Field, a: int, b: int, c: int) -> dict:
    """Closed-triad convention on p+q+r=0 with those exact radii."""
    by_r: dict[int, list[tuple[KVec, Vec]]] = {a: [], b: [], c: []}
    for k, uk in field.items():
        lam = kabs2(k)
        if lam in by_r:
            by_r[lam].append((k, uk))

    I = {a: Fraction(0), b: Fraction(0), c: Fraction(0)}
    for p, up in by_r[a]:
        for q, uq in by_r[b]:
            r = (-p[0] - q[0], -p[1] - q[1], -p[2] - q[2])
            ur = field.get(r)
            if ur is None or kabs2(r) != c:
                continue
            z = kdot(q, up) * vdot(uq, ur)
            I[a] += z.im
    for q, uq in by_r[b]:
        for r, ur in by_r[c]:
            p = (-q[0] - r[0], -q[1] - r[1], -q[2] - r[2])
            up = field.get(p)
            if up is None or kabs2(p) != a:
                continue
            z = kdot(r, uq) * vdot(ur, up)
            I[b] += z.im
    for r, ur in by_r[c]:
        for p, up in by_r[a]:
            q = (-r[0] - p[0], -r[1] - p[1], -r[2] - p[2])
            uq = field.get(q)
            if uq is None or kabs2(q) != b:
                continue
            z = kdot(p, ur) * vdot(up, uq)
            I[c] += z.im

    T_abc = (c - b) * I[a] + (a - c) * I[b] + (b - a) * I[c]
    return {"I_p": I[a], "I_q": I[b], "I_r": I[c], "T_abc": T_abc}


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def report() -> dict:
    i3 = i3_regression()
    examples = {}
    for kind, expected_T in (("cos", 0), ("sin", 24), ("msin", -24)):
        field = example_field(kind)
        m = moments_field(field)
        T = enstrophy_transfer(field)
        examples[kind] = {
            "E": str(m["E"]),
            "X": str(m["X"]),
            "Y": str(m["Y"]),
            "Z": str(m["Z"]),
            "T": str(T),
            "energy_sum": str(energy_transfer(field)),
            "T_ok": T == expected_T,
            "moments_ok": m == {
                "E": Fraction(6),
                "X": Fraction(52),
                "Y": Fraction(532),
                "Z": Fraction(5980),
            },
        }

    cos = example_field("cos")
    B_gen = generated_mode_B(cos, (3, -2, 0))
    gen_ok = B_gen == (C(0), C(0), C(0, 3))

    odd = odd_triad_field(Fraction(1))
    odd_m = moments_field(odd)
    odd_T = enstrophy_transfer(odd)
    A = Fraction(24)
    odd24 = odd_triad_field(A)
    m24 = moments_field(odd24)
    T24 = enstrophy_transfer(odd24)
    # X' = 2T − 2ν Y at ν = 1
    Xprime = 2 * T24 - 2 * m24["Y"]

    sh = shear_field()
    sh_m = moments_field(sh)
    sh_out = shear_output_on_beta2(sh)
    # normalized ratio |Π_β B|² / ((α²/β) |w|⁴), α=1, β=2
    w4 = sh_m["E"] * sh_m["E"]
    norm_ratio = sh_out["norm2"] / (Fraction(1, 2) * w4)

    even_ok = all(even_output_weighted_sum(a) == even_output_closed(a) for a in range(1, 9))
    poly_ok = all(sixteen_ninths_gap(Fraction(n, 4)) >= 0 for n in range(0, 17))

    sphere = exact_sphere_L2(1, 2)

    fr = triangle_frame((3, 0, 0), (0, 2, 0))
    A1, A2, B1, B2 = 1.0, -0.5, 0.25, 0.75
    up, uq = polarizations(fr, A1, A2, B1, B2)
    Sdef = S_pq_definition(fr, up, uq)
    Sbox = S_pq_boxed(fr, A1, A2, B1, B2)
    dS = max(abs(Sdef[i] - Sbox[i]) for i in range(3))
    dleft, dright = unequal_defect(fr, up, uq, Sdef)
    ddef = abs(dleft - dright)

    fr_eq = triangle_frame((1, 1, 0), (1, -1, 0))
    upe, uqe = polarizations(fr_eq, A1, A2, B1, B2)
    Seq = S_pq_definition(fr_eq, upe, uqe)
    Seqb = S_pq_equal_boxed(fr_eq, A1, A2, B1, B2)
    dEq = max(abs(Seq[i] - Seqb[i]) for i in range(3))
    # in-plane e1 component must vanish
    e1_comp = abs(_dot3(Seq, fr_eq["e1"]))

    sc = scalene_I_and_T(odd, 4, 9, 13)

    return {
        "i3": i3,
        "i3_all_match": all(r["matches"] for r in i3),
        "examples": examples,
        "generated_3i_e3": gen_ok,
        "odd_unit": {
            "X": str(odd_m["X"]),
            "Y": str(odd_m["Y"]),
            "T": str(odd_T),
            "ok": odd_m["X"] == 52 and odd_m["Y"] == 532 and odd_T == 24,
        },
        "odd_A24": {
            "Xprime": str(Xprime),
            "ok": Xprime == 50688,
        },
        "shear": {
            "E": str(sh_m["E"]),
            "n_nonzero": sh_out["n_nonzero"],
            "norm2": str(sh_out["norm2"]),
            "ratio": str(norm_ratio),
            "ok": sh_m["E"] == Fraction(3, 2)
            and sh_out["n_nonzero"] == 12
            and sh_out["norm2"] == Fraction(3, 4)
            and norm_ratio == Fraction(2, 3),
        },
        "even_output_ok": even_ok,
        "sixteen_ninths_ok": poly_ok,
        "sphere": sphere,
        "S_pq_err": dS,
        "defect_err": ddef,
        "equal_S_err": dEq,
        "equal_e1_comp": e1_comp,
        "scalene_7": {k: str(v) for k, v in sc.items()},
        "scalene_7_matches_T": sc["T_abc"] == odd_T,
        "locks": {
            "not_a_close": True,
            "theorem_17_proved": False,
            "i3_is_lattice": True,
            "i3_does_not_fix_amplitudes": True,
            "lemma_A_unaltered": True,
            "sign_gate_unaltered": True,
            "S_reported_not_rerun": True,
        },
    }


def main(argv: Iterable[str] | None = None) -> int:
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    print(json.dumps(report(), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
