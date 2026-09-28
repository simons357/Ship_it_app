"""Exact helical phase network for the centered drift.

Geometric triad Δ = (k, p, q) with k+p+q=0. Helicity σ = (s_k, s_p, s_q).

The k-equation of a real field is fed by (−p, −q), so

    g_{Δ,σ} = (h_{-p}^{s_p} × h_{-q}^{s_q}) · conj(h_k^{s_k}),
    W = g conj(a_k^{s_k} a_p^{s_p} a_q^{s_q}),
    Θ = Re(W),
    C = −(a−b)(b−c)(c−a)(a²+b²+c²+ab+bc+ca−Λ),
    T_{c,Δ,σ} = 2 C Θ.

This is the finite algebra. It is not DA-NS-2.
"""

from __future__ import annotations

import math
from itertools import product
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

from ns_attacks.fourier import (
    Mode,
    Sigma,
    add,
    channel_id,
    helical,
    neg,
    nrm,
    nrm2,
)
from ns_attacks.galerkin import Field, flux_stats, moments

SEED_K: Mode = (1, 0, 0)
SEED_P: Mode = (0, 1, 1)
SEED_Q: Mode = (-1, -1, -1)
SEED_SIGMA: Sigma = (1, 1, -1)


def g_channel(
    k: Mode,
    p: Mode,
    q: Mode,
    sigma: Sigma,
    planar_n: Optional[Sequence[float]] = None,
) -> complex:
    sk, sp, sq = (int(sigma[0]), int(sigma[1]), int(sigma[2]))
    hp = helical(neg(p), sp, planar_n)
    hq = helical(neg(q), sq, planar_n)
    hk = helical(k, sk, planar_n)
    # Overall minus: T_c = M−ΛN uses B=−P(u·∇u), matching (log Λ)' = 2(T_c−νD_s)/Y.
    return complex(-np.dot(np.cross(hp, hq), np.conjugate(hk)))


def signed_radii(k: Mode, p: Mode, q: Mode, sigma: Sigma) -> Tuple[float, float, float]:
    sk, sp, sq = sigma
    return (sk * nrm(k), sp * nrm(p), sq * nrm(q))


def C_multiplier(a: float, b: float, c: float, Lam: float) -> float:
    return -(a - b) * (b - c) * (c - a) * (a * a + b * b + c * c + a * b + b * c + c * a - Lam)


def H_ijo(i: float, j: float, o: float) -> float:
    return i * i + j * j + o * o + i * j - o * (i + j)


def R_lambda(i: float, j: float, o: float, Lam: float) -> float:
    return (i + o) * (j + o) * (H_ijo(i, j, o) - Lam) / (2.0 * o)


def odd_leg(sigma: Sigma) -> str:
    sk, sp, sq = sigma
    if len({sk, sp, sq}) != 2:
        raise ValueError("homochiral σ has no unique odd-helicity leg")
    if sk != sp and sk != sq:
        return "k"
    if sp != sk and sp != sq:
        return "p"
    return "q"


def is_heterochiral(sigma: Sigma) -> bool:
    return len(set(sigma)) == 2 and set(sigma) <= {1, -1}


def enumerate_triads(modes: Sequence[Mode]) -> List[Tuple[Mode, Mode, Mode]]:
    mode_set = set(modes)
    seen = set()
    triads: List[Tuple[Mode, Mode, Mode]] = []
    for k in modes:
        for p in modes:
            q = neg(add(k, p))
            if nrm2(q) == 0 or q not in mode_set:
                continue
            if k in (p, q) or p == q:
                continue
            cid = channel_id(k, p, q)
            if cid in seen:
                continue
            seen.add(cid)
            cands = [
                (k, p, q),
                (p, q, k),
                (q, k, p),
                (neg(k), neg(p), neg(q)),
                (neg(p), neg(q), neg(k)),
                (neg(q), neg(k), neg(p)),
            ]
            triads.append(min(cands))
    return triads


def monomial(
    field: Field,
    k: Mode,
    p: Mode,
    q: Mode,
    sigma: Sigma,
    planar_n: Optional[Sequence[float]] = None,
) -> Dict[str, complex]:
    sk, sp, sq = sigma
    g = g_channel(k, p, q, sigma, planar_n)
    ak = field.amplitude(k, sk, planar_n)
    ap = field.amplitude(p, sp, planar_n)
    aq = field.amplitude(q, sq, planar_n)
    W = g * np.conjugate(ak * ap * aq)
    return {"g": g, "a_k": ak, "a_p": ap, "a_q": aq, "W": complex(W)}


def channel_record(
    field: Field,
    k: Mode,
    p: Mode,
    q: Mode,
    sigma: Sigma,
    Lam: float,
    planar_n: Optional[Sequence[float]] = None,
) -> Dict[str, float]:
    mon = monomial(field, k, p, q, sigma, planar_n)
    W = mon["W"]
    a, b, c = signed_radii(k, p, q, sigma)
    C = C_multiplier(a, b, c, Lam)
    Theta = float(W.real)
    Z = C * W
    A = 2.0 * abs(Z)
    contrib = 2.0 * C * Theta
    tau = (Theta * (b - c), Theta * (c - a), Theta * (a - b))
    Q_one = nrm(k) * tau[0] + nrm(p) * tau[1] + nrm(q) * tau[2]
    Q_abs = 2.0 * Q_one  # ± modes
    rec: Dict[str, float] = {
        "C": C,
        "Theta": Theta,
        "T_c": contrib,
        "A": A,
        "Q_abs": Q_abs,
        "W_re": float(W.real),
        "W_im": float(W.imag),
        "psi": math.atan2(W.imag, W.real) if abs(W) > 0.0 else 0.0,
        "abs_W": abs(W),
        "tau_k": tau[0],
        "tau_p": tau[1],
        "tau_q": tau[2],
        "factor_resid": abs(contrib - (A * math.cos(math.atan2(Z.imag, Z.real)) if A > 0.0 else 0.0)),
    }
    rec["g_re"] = float(mon["g"].real)
    rec["g_im"] = float(mon["g"].imag)
    rec["abs_ak"] = abs(mon["a_k"])
    rec["abs_ap"] = abs(mon["a_p"])
    rec["abs_aq"] = abs(mon["a_q"])
    if is_heterochiral(sigma):
        odd = odd_leg(sigma)
        radii = {"k": nrm(k), "p": nrm(p), "q": nrm(q)}
        o = radii[odd]
        ij = [radii[leg] for leg in ("k", "p", "q") if leg != odd]
        R = R_lambda(ij[0], ij[1], o, Lam)
        rec["R_lambda"] = R
        rec["het_resid"] = abs(contrib - R * Q_abs)
    else:
        rec["R_lambda"] = float("nan")
        rec["het_resid"] = abs(Q_abs)
    rec["homochiral"] = 0.0 if is_heterochiral(sigma) else 1.0
    return rec


def network_sum(
    field: Field,
    modes: Sequence[Mode],
    planar_n: Optional[Sequence[float]] = None,
) -> Dict[str, float]:
    Lam = moments(field)["Lambda"]
    triads = enumerate_triads(modes)
    total = 0.0
    cap = 0.0
    n_ch = 0
    max_fact = 0.0
    max_het = 0.0
    max_hom_Q = 0.0
    n_het = 0
    n_hom = 0
    for k, p, q in triads:
        for sigma in product((1, -1), repeat=3):
            rec = channel_record(field, k, p, q, sigma, Lam, planar_n)
            total += rec["T_c"]
            cap += rec["A"]
            n_ch += 1
            max_fact = max(max_fact, rec["factor_resid"])
            if rec["homochiral"]:
                n_hom += 1
                max_hom_Q = max(max_hom_Q, rec["het_resid"])
            else:
                n_het += 1
                max_het = max(max_het, rec["het_resid"])
    stats = flux_stats(field, modes)
    return {
        "n_triads": float(len(triads)),
        "n_signed": float(n_ch),
        "n_het": float(n_het),
        "n_hom": float(n_hom),
        "phase_sum": total,
        "direct_T_c": stats["T_c"],
        "recon_err": abs(total - stats["T_c"]),
        "cap_sum": cap,
        "alignment": (stats["T_c"] / cap) if cap > 0.0 else 0.0,
        "max_factor_resid": max_fact,
        "max_het_resid": max_het,
        "max_hom_Q": max_hom_Q,
        "energy_pairing": stats["energy_pairing"],
        "Lambda": stats["Lambda"],
        "X": stats["X"],
        "Y": stats["Y"],
        "Z": stats["Z"],
        "D_s": stats["D_s"],
        "N": stats["N"],
        "Q_a": stats["Q_a"],
        "H_a": stats["H_a"],
        "D_a": stats["D_a"],
    }


def angular_current(
    field: Field,
    k: Mode,
    p: Mode,
    q: Mode,
    sigma: Sigma,
    cutoff: Sequence[Mode],
    nu: float,
    planar_n: Optional[Sequence[float]] = None,
) -> Dict[str, float]:
    """J^W = Im(conj(W) Ẇ). Viscosity contributes no rotation."""
    from ns_attacks.galerkin import rhs as galerkin_rhs

    du = galerkin_rhs(field, cutoff, nu)
    sk, sp, sq = sigma
    g = g_channel(k, p, q, sigma, planar_n)
    ak = field.amplitude(k, sk, planar_n)
    ap = field.amplitude(p, sp, planar_n)
    aq = field.amplitude(q, sq, planar_n)
    W = g * np.conjugate(ak * ap * aq)

    def amp_dot(kk: Mode, s: int) -> complex:
        h = helical(kk, s, planar_n)
        return complex(np.vdot(h, du.get(kk, np.zeros(3, dtype=complex))))

    d_prod = amp_dot(k, sk) * ap * aq + ak * amp_dot(p, sp) * aq + ak * ap * amp_dot(q, sq)
    dW = g * np.conjugate(d_prod)
    JW = float((np.conjugate(W) * dW).imag)
    absW2 = abs(W) ** 2
    return {
        "J_W": JW,
        "abs_W": abs(W),
        "psi_dot": (JW / absW2) if absW2 > 0.0 else 0.0,
        "W_re": float(W.real),
        "W_im": float(W.imag),
    }
