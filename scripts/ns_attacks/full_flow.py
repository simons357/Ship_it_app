"""Sprint 01 full-flow helical channel: k+p+q=0, conjugation, charge.

Source: DA-NS-SPRINT-01-PHASE-LOCK-AND-FULL-HELICAL-FLOW-2026-09-07.md

Canonical object:

    γ = (Δ, σ),   k+p+q = 0,   σ = (s_k, s_p, s_q) heterochiral.

    (τ_k, τ_p, τ_q) = Θ_{Δ,σ} (b-c, c-a, a-b)

    Θ_{Δ,σ} = Re( g_{Δ,σ}  conj(a_k a_p a_q) )     conjugation is essential

    W_{Δ,σ} = g_{Δ,σ} conj(a_k a_p a_q)

    T_{c,Δ,σ} = 2 C_{Δ,σ} Θ_{Δ,σ}     (real six-mode channel)

    C_{Δ,σ} = -(a-b)(b-c)(c-a)(a²+b²+c²+ab+bc+ca-Λ)

Heterochiral reduction:

    T_c^{het} = R_Λ(i,j;o) Q_abs
    Q_abs = ∑_{m ∈ Δ, ±} |m| τ_m
    Q_abs = 2 Q_3 = 4 o τ_o          (three-mode Q_3 = 2 o τ_o)
    R_Λ = A (H_{ij|o}-Λ),   A = (i+o)(j+o)/(2o)

g_{Δ,σ} is one scalar for the whole signed channel. It is not g_W.

On the flipped p+q=k representative k'=-k, with frames
h_s(-k)=conj(h_s(k)):

    G_0 = (h_p × h_q) · h_k
    G_cross(p,q,k') = (h_p × h_q) · conj(h_{k'}) = G_0
    g_ordered = -i s_p |μ| G_0,    |μ|>0

The operational coefficient in Θ = Re(g conj(aaa)) is the
energy-fitted g. |g_energy| = |G_0| always. The unimodular
ratio U = g_energy / G_0 is a frame/triangle convention, not
identically +1:

    T1:  U = +1
    T2:  U = -1
    T3:  U = ±i
    T4, seed: arg U ∈ {±π/6, ±5π/6}

Do not treat U=1 as universal. Loop-gauge b_γ must use the
energy-fit g, or apply U explicitly to G_0. The map from
either kernel onto g_ordered remains the known iℝ factor.

Q_abs = ∑_{m ∈ Δ, ±} |m| τ_m  (six-mode). Q_3 = 2 o τ_o is
the three-mode reduction; Q_abs = 2 Q_3 on a real six-mode
channel. Do not rename Q_3 as Q_abs.

Not a close. NS is not solved. Do not run v2. DA-NS-2 open.
"""

from __future__ import annotations

import cmath
import math
from typing import Dict, List, Sequence, Tuple

from ns_attacks.channel_coefficient import (
    HETEROCHIRAL_SIGMA,
    PARALLELOGRAM,
    A_coeff,
    H_ijo,
    is_heterochiral,
    mu_factor,
    odd_leg,
)
from ns_attacks.helical import (
    add,
    as_mode,
    helical_basis,
    norm,
    sub,
)

Mode = Tuple[int, int, int]
Sigma = Tuple[int, int, int]
CVec = Tuple[complex, complex, complex]
Vec = Tuple[float, float, float]


def _dot(a: Sequence[complex], b: Sequence[complex]) -> complex:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a: Sequence[complex], b: Sequence[complex]) -> CVec:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _neg(m: Mode) -> Mode:
    return (-m[0], -m[1], -m[2])


def _scale(v: CVec, z: complex) -> CVec:
    return (z * v[0], z * v[1], z * v[2])


def lex_hemisphere(m: Mode) -> bool:
    return m > _neg(m)


def consistent_helical(
    m: Sequence[int],
    s: int,
    axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> CVec:
    """Waleffe partner: h_s(-k) := conj(h_s(k)) on a lex hemisphere."""
    mm = as_mode(m)
    if lex_hemisphere(mm) or mm == _neg(mm):
        return helical_basis(mm, s, axis)
    hpos = helical_basis(_neg(mm), s, axis)
    return (hpos[0].conjugate(), hpos[1].conjugate(), hpos[2].conjugate())


def assert_sum0(k: Mode, p: Mode, q: Mode) -> None:
    if add(add(k, p), q) != (0, 0, 0):
        raise ValueError(f"need k+p+q=0, got {k}+{p}+{q}")


# Locked parallelogram rewritten as k+p+q=0: k = -k_out of p+q=k_out.
PARALLELOGRAM_SUM0: Tuple[Tuple[str, Mode, Mode, Mode], ...] = tuple(
    (name, _neg(k_out), p, q) for name, p, q, k_out in PARALLELOGRAM
)

# Sprint 01 §4.3 seed.
SEED_SUM0: Tuple[str, Mode, Mode, Mode] = (
    "seed",
    (1, 0, 0),
    (0, 1, 1),
    (-1, -1, -1),
)


def g_Delta_sigma(
    k: Sequence[int],
    p: Sequence[int],
    q: Sequence[int],
    sigma: Sigma,
    axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> complex:
    """G_0 = (h_p^{s_p} × h_q^{s_q}) · h_k^{s_k} on k+p+q=0."""
    km, pm, qm = as_mode(k), as_mode(p), as_mode(q)
    assert_sum0(km, pm, qm)
    sk, sp, sq = (int(sigma[0]), int(sigma[1]), int(sigma[2]))
    hp = consistent_helical(pm, sp, axis)
    hq = consistent_helical(qm, sq, axis)
    hk = consistent_helical(km, sk, axis)
    return _dot(_cross(hp, hq), hk)


def g_ordered_flip(
    k: Sequence[int],
    p: Sequence[int],
    q: Sequence[int],
    sigma: Sigma,
    axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> Dict[str, complex]:
    """g_ordered on the frozen p+q=k' representative, k'=-k, s_{k'}=s_k."""
    km, pm, qm = as_mode(k), as_mode(p), as_mode(q)
    assert_sum0(km, pm, qm)
    sk, sp, sq = (int(sigma[0]), int(sigma[1]), int(sigma[2]))
    kflip = _neg(km)
    hp = consistent_helical(pm, sp, axis)
    hq = consistent_helical(qm, sq, axis)
    hk = consistent_helical(kflip, sk, axis)
    hk_bar = (hk[0].conjugate(), hk[1].conjugate(), hk[2].conjugate())
    qv = (float(qm[0]), float(qm[1]), float(qm[2]))
    g_ordered = _dot(qv, hp) * _dot(hq, hk_bar)
    g_cross = _dot(_cross(hp, hq), hk_bar)
    return {"g_ordered": g_ordered, "g_cross": g_cross, "s_p": sp}


def C_coeff(a: float, b: float, c: float, Lambda: float) -> float:
    return (
        -(a - b)
        * (b - c)
        * (c - a)
        * (a * a + b * b + c * c + a * b + b * c + c * a - Lambda)
    )


def R_Lambda(i: float, j: float, o: float, Lambda: float) -> float:
    return A_coeff(i, j, o) * (H_ijo(i, j, o) - Lambda)


def signed_radii_sum0(k: Mode, p: Mode, q: Mode, sigma: Sigma) -> Tuple[float, float, float]:
    sk, sp, sq = sigma
    return (sk * norm(k), sp * norm(p), sq * norm(q))


def modal_transfer(field: Dict[Mode, CVec], k: Mode) -> float:
    """T_k = Im ∑_{p+q=k} (q·u_p)(u_q·conj(u_k))."""
    uk = field[k]
    ukb = (uk[0].conjugate(), uk[1].conjugate(), uk[2].conjugate())
    acc = 0j
    for p in field:
        q = sub(k, p)
        if q not in field:
            continue
        vp, vq = field[p], field[q]
        qv = (float(q[0]), float(q[1]), float(q[2]))
        acc += _dot(qv, vp) * _dot(vq, ukb)
    return float(acc.imag)


def real_six_mode_field(
    k: Mode,
    p: Mode,
    q: Mode,
    sigma: Sigma,
    ak: complex,
    ap: complex,
    aq: complex,
    axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> Dict[Mode, CVec]:
    sk, sp, sq = sigma
    field: Dict[Mode, CVec] = {}
    for m, s, a in ((k, sk, ak), (p, sp, ap), (q, sq, aq)):
        h = consistent_helical(m, s, axis)
        u = _scale(h, a)
        field[m] = u
        field[_neg(m)] = (u[0].conjugate(), u[1].conjugate(), u[2].conjugate())
    return field


def energy_fit_g(
    k: Mode,
    p: Mode,
    q: Mode,
    sigma: Sigma,
    axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> complex:
    """Unique g such that Θ = Re(g conj(aaa)) reproduces τ_k/(b-c).

    Two samples: aaa=1 gives Re(g); aaa=i³=-i gives Im(g).
    """
    a, b, c = signed_radii_sum0(k, p, q, sigma)
    bc = b - c
    if abs(bc) <= 1e-14:
        raise ZeroDivisionError("k-leg Vandermonde vanishes; g still |G_0|")

    def theta_from(ak: complex, ap: complex, aq: complex) -> float:
        field = real_six_mode_field(k, p, q, sigma, ak, ap, aq, axis)
        return modal_transfer(field, k) / bc

    th_real = theta_from(1 + 0j, 1 + 0j, 1 + 0j)  # aaa=1, conj=1, Re(g)=Θ
    th_imag = theta_from(1j, 1j, 1j)  # aaa=-i, conj=i, Re(i g)=Θ
    # Re(g)=th_real.
    # g*(i) = i gr - gi, Re = -gi = th_imag ⇒ gi = -th_imag.
    return complex(th_real, -th_imag)


def channel_transfers(
    k: Mode,
    p: Mode,
    q: Mode,
    sigma: Sigma,
    ak: complex,
    ap: complex,
    aq: complex,
    axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> dict:
    field = real_six_mode_field(k, p, q, sigma, ak, ap, aq, axis)
    modes = (k, p, q, _neg(k), _neg(p), _neg(q))
    T = {m: modal_transfer(field, m) for m in modes}
    e = {
        m: abs(field[m][0]) ** 2 + abs(field[m][1]) ** 2 + abs(field[m][2]) ** 2
        for m in modes
    }
    X = sum(norm(m) ** 2 * e[m] for m in modes)
    Y = sum(norm(m) ** 4 * e[m] for m in modes)
    Lambda = Y / X if X else 0.0
    a, b, c = signed_radii_sum0(k, p, q, sigma)
    Tc6 = sum(norm(m) ** 2 * (norm(m) ** 2 - Lambda) * T[m] for m in modes)
    Q6 = sum(norm(m) * T[m] for m in modes)
    Q3 = norm(k) * T[k] + norm(p) * T[p] + norm(q) * T[q]
    return {
        "T": T,
        "Lambda": Lambda,
        "Tc6": Tc6,
        "Q6": Q6,
        "Q3": Q3,
        "a": a,
        "b": b,
        "c": c,
        "aaa": ak * ap * aq,
    }


def certify_full_flow_one(
    k: Mode,
    p: Mode,
    q: Mode,
    sigma: Sigma,
    axis: Sequence[float] = (0.0, 0.0, 1.0),
    tol: float = 1e-10,
) -> dict:
    assert_sum0(k, p, q)
    if not is_heterochiral(sigma):
        raise ValueError("heterochiral only")
    G0 = g_Delta_sigma(k, p, q, sigma, axis)
    flip = g_ordered_flip(k, p, q, sigma, axis)
    a, b, c = signed_radii_sum0(k, p, q, sigma)
    bc = b - c
    g0_flip_err = abs(flip["g_cross"] - G0)
    aligned = None
    if abs(G0) > 0.0:
        aligned = mu_factor(flip["g_ordered"], G0, sigma[1])
    amps = (0.3 + 0.4j, 0.5 - 0.2j, -0.1 + 0.7j)
    ch = channel_transfers(k, p, q, sigma, *amps, axis=axis)
    Tk, Tp, Tq = ch["T"][k], ch["T"][p], ch["T"][q]
    ca, ab = c - a, a - b
    thetas = []
    if abs(bc) > 1e-14:
        thetas.append(Tk / bc)
    if abs(ca) > 1e-14:
        thetas.append(Tp / ca)
    if abs(ab) > 1e-14:
        thetas.append(Tq / ab)
    Theta = thetas[0] if thetas else 0.0
    split = max(abs(x - Theta) for x in thetas) if thetas else 0.0
    C = C_coeff(a, b, c, ch["Lambda"])
    Tc_err = abs(ch["Tc6"] - 2.0 * C * Theta) if thetas else 0.0
    odd = odd_leg(sigma)
    radii = {"k": norm(k), "p": norm(p), "q": norm(q)}
    o = radii[odd]
    ij = [radii[leg] for leg in ("k", "p", "q") if leg != odd]
    To = {"k": Tk, "p": Tp, "q": Tq}[odd]
    Q3_err = abs(ch["Q3"] - 2.0 * o * To)
    Q6_err = abs(ch["Q6"] - 2.0 * ch["Q3"])
    R = R_Lambda(ij[0], ij[1], o, ch["Lambda"])
    het_err = abs(ch["Tc6"] - R * ch["Q6"])
    U = 0j
    fit_err = 0.0
    abs_err = 0.0
    no_conj_err = 0.0
    if abs(bc) > 1e-14:
        g_fit = energy_fit_g(k, p, q, sigma, axis)
        U = g_fit / G0 if abs(G0) else 0j
        abs_err = abs(abs(g_fit) - abs(G0))
        # conjugation formula on the mixed sample
        Theta_pred = (g_fit * ch["aaa"].conjugate()).real
        fit_err = abs(Theta_pred - Theta)
        no_conj_err = abs((g_fit * ch["aaa"]).real - Theta)
    t_sym_err = max(
        abs(ch["T"][m] - ch["T"][_neg(m)]) for m in (k, p, q)
    )
    return {
        "g0_flip_err": g0_flip_err,
        "mu_phase_err": abs(math.atan2(aligned.imag, aligned.real)) if aligned is not None else 0.0,
        "mu_real": aligned.real if aligned is not None else 0.0,
        "split": split,
        "Tc_err": Tc_err,
        "Q3_err": Q3_err,
        "Q6_err": Q6_err,
        "het_err": het_err,
        "U_abs": abs(U),
        "U_arg": float(cmath.phase(U)) if abs(U) else 0.0,
        "abs_g_err": abs_err,
        "Theta_conj_err": fit_err,
        "Theta_no_conj_err": no_conj_err,
        "T_sym_err": t_sym_err,
        "vandermonde_zero": abs(bc) <= 1e-14,
        "odd_leg": odd,
        "A_gamma": A_coeff(ij[0], ij[1], o),
        "R_Lambda": R,
        "Q_abs": ch["Q6"],
        "Q3": ch["Q3"],
    }


def full_flow_report(tol: float = 1e-10) -> dict:
    rows = []
    keys = [
        "g0_flip_err",
        "mu_phase_err",
        "split",
        "Tc_err",
        "Q3_err",
        "Q6_err",
        "het_err",
        "abs_g_err",
        "Theta_conj_err",
        "T_sym_err",
    ]
    maxima = {k: 0.0 for k in keys}
    max_U_arg = 0.0
    max_no_conj = 0.0
    n = 0
    u_by_delta: Dict[str, List[float]] = {}
    triads: List[Tuple[str, Mode, Mode, Mode]] = [SEED_SUM0] + list(PARALLELOGRAM_SUM0)
    for name, k, p, q in triads:
        for sigma in HETEROCHIRAL_SIGMA:
            cert = certify_full_flow_one(k, p, q, sigma)
            n += 1
            for key in keys:
                maxima[key] = max(maxima[key], cert[key])
            if not cert["vandermonde_zero"]:
                max_U_arg = max(max_U_arg, abs(cert["U_arg"]))
                u_by_delta.setdefault(name, []).append(cert["U_arg"])
                max_no_conj = max(max_no_conj, cert["Theta_no_conj_err"])
            rows.append({"delta": name, "k": list(k), "p": list(p), "q": list(q), "sigma_kpq": list(sigma), **cert})
    passed = all(maxima[k] < tol for k in keys)
    # When g is real, Re(g aaa)=Re(g conj(aaa)), so some channels (T2)
    # give a false-negative no-conj residual. The max over mixed
    # samples is the honest essential-conjugation check.
    return {
        "source": "DA-NS-SPRINT-01 k+p+q=0 with conjugation",
        "n_certified": n,
        "maxima": maxima,
        "max_U_arg_nonvanishing": max_U_arg,
        "max_Theta_no_conj_err_live": max_no_conj,
        "conjugation_essential": max_no_conj > 1e-3 and maxima["Theta_conj_err"] < tol,
        "U_frame": {
            "statement": "|g_energy|=|G_0|; U=g_energy/G_0 is unimodular and triangle/frame dependent",
            "do_not_treat_U_as_1": True,
            "observed_on_default_axis": {
                "T1": "arg 0 (+1)",
                "T2": "arg pi (-1)",
                "T3": "arg ±pi/2 (±i)",
                "T4": "arg ±pi/6, ±5pi/6",
                "seed": "arg ±pi/6, ±5pi/6",
            },
            "args_by_delta": {name: args for name, args in u_by_delta.items()},
        },
        "passed": passed,
        "identities": {
            "three_transfer": "(tau_k,tau_p,tau_q)=Theta (b-c,c-a,a-b)",
            "Theta": "Re(g conj(aaa))",
            "six_mode_Tc": "Tc = 2 C Theta",
            "Q3": "Q3 = 2 o tau_o  (three-mode reduction)",
            "Q_abs": "Q_abs = sum_{m in Delta, ±} |m| tau_m = 2 Q3",
            "heterochiral": "Tc_het = R_Lambda Q_abs",
            "g_modulus": "|g_energy| = |G_0| = |(hp × hq)·hk|",
            "flip": "G_cross(p,q,-k)=(hp×hq)·hk",
            "g_ordered": "g_ordered = -i s_p |mu| G_0",
            "U": "U = g_energy/G_0 unimodular, not identically +1",
        },
        "rows": rows,
        "DA_NS_2_open": True,
        "v2_not_run": True,
        "not_a_close": True,
    }


def canonical_24_payload_sum0(axis: Sequence[float] = (0.0, 0.0, 1.0)) -> dict:
    """Same 24 channels, official representative k+p+q=0."""
    from ns_attacks.channel_coefficient import _cpx

    channels = []
    for name, k, p, q in PARALLELOGRAM_SUM0:
        for sigma in HETEROCHIRAL_SIGMA:
            G0 = g_Delta_sigma(k, p, q, sigma, axis)
            flip = g_ordered_flip(k, p, q, sigma, axis)
            a, b, c = signed_radii_sum0(k, p, q, sigma)
            odd = odd_leg(sigma)
            radii = {"k": norm(k), "p": norm(p), "q": norm(q)}
            o = radii[odd]
            ij = [radii[leg] for leg in ("k", "p", "q") if leg != odd]
            rec = {
                "gamma": {
                    "delta_id": name,
                    "k": list(k),
                    "p": list(p),
                    "q": list(q),
                    "sigma_kpq": list(sigma),
                    "convention": "k+p+q=0",
                },
                "odd_leg": odd,
                "radii": {"i": ij[0], "j": ij[1], "o": o},
                "signed_radii": {"a": a, "b": b, "c": c},
                "A_gamma": A_coeff(ij[0], ij[1], o),
                "H_ijo": H_ijo(ij[0], ij[1], o),
                "g_frame_G0": _cpx(G0),
                "g_Delta_sigma": _cpx(G0),
                "g_ordered": _cpx(flip["g_ordered"]),
                "G_cross_flip": _cpx(flip["g_cross"]),
                "vandermonde_k_leg": b - c,
                "vandermonde_zero": abs(b - c) <= 1e-14,
                "channel_phase_invariant": float(cmath.phase(G0)) if abs(G0) else 0.0,
                "notes": {
                    "Q_abs_is_sum_pm_abs_m_tau_m": True,
                    "Q3_equals_2_o_tau_o_three_mode": True,
                    "conjugation_essential": True,
                    "operational_g_is_energy_fit": True,
                    "U_is_frame_convention_not_always_1": True,
                },
            }
            if abs(b - c) > 1e-14 and abs(G0) > 0.0:
                g_fit = energy_fit_g(k, p, q, sigma, axis)
                U = g_fit / G0
                rec["g_energy"] = _cpx(g_fit)
                rec["U"] = _cpx(U)
            channels.append(rec)
    return {
        "stamp": "gamma = (Delta, sigma)",
        "convention": "k+p+q=0",
        "sigma_convention": "(s_k, s_p, s_q)",
        "n_geometric_delta": 4,
        "n_heterochiral_sigma": 6,
        "n_channels": len(channels),
        "representative": "locked parallelogram rewritten as k+p+q=0",
        "source": "DA-NS-SPRINT-01-PHASE-LOCK-AND-FULL-HELICAL-FLOW-2026-09-07.md",
        "U_frame": {
            "statement": "|g_energy|=|G_0|; U=g_energy/G_0 is unimodular and triangle/frame dependent",
            "do_not_treat_U_as_1": True,
            "observed_on_default_axis": {
                "T1": "arg 0 (+1)",
                "T2": "arg pi (-1)",
                "T3": "arg ±pi/2 (±i)",
                "T4": "arg ±pi/6, ±5pi/6",
            },
        },
        "channels": channels,
        "DA_NS_2_open": True,
        "not_a_close": True,
        "v2_not_run": True,
    }
