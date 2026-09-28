"""Coefficient identity for the signed helical channel γ=(Δ,σ).

Canonical object (this page):

    γ = (Δ, σ),   σ = (s_k, s_p, s_q) ∈ {±1}^3 heterochiral.

Frozen geometric representative of Δ: one ordered triad p+q=k.
Six heterochiral sign triples, not three cyclic output rewrites.

Kernels on that representative:

    G_cross   = (h_p^{s_p} × h_q^{s_q}) · conj(h_k^{s_k})
    g_ordered = (q · h_p^{s_p}) (h_q^{s_q} · conj(h_k^{s_k}))
    g_W       = (1/2)(s_p |p| − s_q |q|) G_cross

g_{Δ,σ} is G_cross: one scalar for the whole signed channel.
g_W folds the k-leg Vandermonde into the coefficient and is not
the channel object. Cyclically reevaluating g_W would treat one
physical channel as three independently phased interactions.

Identity (EXACT, certified):

    g_ordered = −i s_p |μ| G_cross,    |μ| > 0.

The phase offset is the helicity-label convention −s_p π/2.
Shape enters only |μ|. Axis changes do not move the ratio.
A uniform π/2 drops out of every cycle holonomy because
c ∈ ker(B^T) ⇒ ∑_e c_e = 0. Swapping arg(g_ordered) for
arg(G_cross) without the −s_p π/2 correction would shift
Ω_c by −(π/2) ∑ c_e s_{p_e}; that shift is known, not a
new geometric defect.

Not a close. NS is not solved. Do not run v2 from this page.
"""

from __future__ import annotations

import cmath
import math
from typing import Dict, List, Sequence, Tuple

from ns_attacks.helical import (
    AXES,
    add,
    as_mode,
    geometric_coupling,
    helical_basis,
    norm,
    wrap_pi,
)

Mode = Tuple[int, int, int]
Sigma = Tuple[int, int, int]  # (s_k, s_p, s_q)
CVec = Tuple[complex, complex, complex]

# User-frozen heterochiral list, σ = (s_k, s_p, s_q).
# Three choices of odd-helicity leg × two overall signs.
HETEROCHIRAL_SIGMA: Tuple[Sigma, ...] = (
    (1, 1, -1),  # odd q
    (-1, -1, 1),  # odd q, overall flip
    (1, -1, 1),  # odd p
    (-1, 1, -1),  # odd p, overall flip
    (-1, 1, 1),  # odd k
    (1, -1, -1),  # odd k, overall flip
)

# Locked parallelogram from LOOP-GAUGE: four geometric Δ, p+q=k.
# 4 Δ × 6 σ = 24 signed channels.
P_PAR: Mode = (1, 0, 0)
Q_PAR: Mode = (0, 1, 0)
R_PAR: Mode = (0, 0, 1)
K_PAR: Mode = (1, 1, 0)
M_PAR: Mode = (1, 0, 1)
N_PAR: Mode = (1, 1, 1)

PARALLELOGRAM: Tuple[Tuple[str, Mode, Mode, Mode], ...] = (
    ("T1", P_PAR, Q_PAR, K_PAR),
    ("T2", P_PAR, R_PAR, M_PAR),
    ("T3", K_PAR, R_PAR, N_PAR),
    ("T4", M_PAR, Q_PAR, N_PAR),
)

PARALLELOGRAM_CYCLE: Tuple[int, ...] = (1, -1, 1, -1)

# Extra scalene probes (identity only; not in the 24-channel payload).
PROBE_TRIADS: Tuple[Tuple[Mode, Mode, Mode], ...] = (
    ((2, -1, 0), (0, 2, 1), (2, 1, 1)),
    ((3, 1, 1), (-1, 2, 2), (2, 3, 3)),
    ((1, 2, 2), (2, -1, 2), (3, 1, 4)),
    ((4, 1, 0), (1, 3, 2), (5, 4, 2)),
    ((2, 3, 1), (-1, 1, 4), (1, 4, 5)),
)


def _dot(a: Sequence[complex], b: Sequence[complex]) -> complex:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a: Sequence[complex], b: Sequence[complex]) -> CVec:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def is_heterochiral(sigma: Sequence[int]) -> bool:
    sk, sp, sq = (int(sigma[0]), int(sigma[1]), int(sigma[2]))
    if {sk, sp, sq} <= {1, -1} and len({sk, sp, sq}) == 2:
        return True
    return False


def odd_leg(sigma: Sigma) -> str:
    sk, sp, sq = sigma
    if not is_heterochiral(sigma):
        raise ValueError("homochiral σ has no unique odd-helicity leg")
    if sk != sp and sk != sq:
        return "k"
    if sp != sk and sp != sq:
        return "p"
    return "q"


def signed_radii(p: Mode, q: Mode, k: Mode, sigma: Sigma) -> Tuple[float, float, float]:
    """a = s_k |k|, b = s_p |p|, c = s_q |q|."""
    sk, sp, sq = sigma
    return (sk * norm(k), sp * norm(p), sq * norm(q))


def channel_radii(p: Mode, q: Mode, k: Mode, sigma: Sigma) -> Dict[str, float]:
    odd = odd_leg(sigma)
    radii = {"k": norm(k), "p": norm(p), "q": norm(q)}
    o = radii[odd]
    others = [radii[leg] for leg in ("k", "p", "q") if leg != odd]
    return {"odd": odd, "o": o, "i": others[0], "j": others[1]}


def A_coeff(i: float, j: float, o: float) -> float:
    return (i + o) * (j + o) / (2.0 * o)


def H_ijo(i: float, j: float, o: float) -> float:
    return i * i + j * j + o * o + i * j - o * (i + j)


def kernels(
    p: Sequence[int],
    q: Sequence[int],
    k: Sequence[int],
    sigma: Sigma,
    axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> Dict[str, complex]:
    """G_cross, g_ordered, g_W on the frozen p+q=k representative."""
    pm, qm, km = as_mode(p), as_mode(q), as_mode(k)
    if add(pm, qm) != km:
        raise ValueError("triad must satisfy p+q=k")
    sk, sp, sq = (int(sigma[0]), int(sigma[1]), int(sigma[2]))
    hp = helical_basis(pm, sp, axis)
    hq = helical_basis(qm, sq, axis)
    hk = helical_basis(km, sk, axis)
    hk_bar = (hk[0].conjugate(), hk[1].conjugate(), hk[2].conjugate())
    g_cross = _dot(_cross(hp, hq), hk_bar)
    qv = (float(qm[0]), float(qm[1]), float(qm[2]))
    pv = (float(pm[0]), float(pm[1]), float(pm[2]))
    g_ordered = _dot(qv, hp) * _dot(hq, hk_bar)
    g_alt = _dot(pv, hq) * _dot(hp, hk_bar)
    g_w = geometric_coupling(pm, qm, km, sp, sq, sk, axis)
    return {
        "g_cross": g_cross,
        "g_ordered": g_ordered,
        "g_alt": g_alt,
        "g_W": g_w,
        "q_dot_hp": _dot(qv, hp),
        "hq_dot_hkbar": _dot(hq, hk_bar),
        "p_hat_cross_q_dot_hp": _rotated_real_pairing(pm, qm, hp),
    }


def _rotated_real_pairing(p: Mode, q: Mode, hp: CVec) -> complex:
    """(p̂ × q) · h_p. Exact identity: this equals i s_p (q · h_p)."""
    pn = norm(p)
    p_hat = (p[0] / pn, p[1] / pn, p[2] / pn)
    pxq = _cross(p_hat, (float(q[0]), float(q[1]), float(q[2])))
    return _dot(pxq, hp)


def mu_factor(g_ordered: complex, g_cross: complex, s_p: int) -> complex:
    """μ_aligned = g_ordered / (−i s_p G_cross). Must be real and positive."""
    if abs(g_cross) == 0.0:
        raise ZeroDivisionError("G_cross vanished")
    return g_ordered / ((-1j * float(s_p)) * g_cross)


def arg_delta_ordered_minus_cross(s_p: int) -> float:
    """arg(g_ordered) − arg(G_cross) = −s_p π/2  (principal)."""
    return wrap_pi(-float(s_p) * math.pi / 2.0)


def certify_one(
    p: Sequence[int],
    q: Sequence[int],
    k: Sequence[int],
    sigma: Sigma,
    axes: Sequence[Sequence[float]] = AXES,
    tol: float = 1e-12,
) -> Dict[str, float]:
    """Certify the coefficient identity on one (Δ,σ), all reference axes."""
    sk, sp, sq = (int(sigma[0]), int(sigma[1]), int(sigma[2]))
    a_rad, b_rad, c_rad = signed_radii(as_mode(p), as_mode(q), as_mode(k), sigma)
    bc = b_rad - c_rad  # s_p |p| − s_q |q|
    aligned_vals: List[complex] = []
    phase_errs: List[float] = []
    w_recon_errs: List[float] = []
    rot_errs: List[float] = []
    abs_mu: List[float] = []
    for axis in axes:
        kn = kernels(p, q, k, sigma, axis)
        g_cross = kn["g_cross"]
        g_ordered = kn["g_ordered"]
        g_w = kn["g_W"]
        if abs(g_cross) <= tol:
            raise AssertionError("G_cross vanished on a live heterochiral channel")
        aligned = mu_factor(g_ordered, g_cross, sp)
        aligned_vals.append(aligned)
        phase_errs.append(abs(math.atan2(aligned.imag, aligned.real)))
        if aligned.real <= 0.0:
            raise AssertionError("aligned μ is not positive")
        abs_mu.append(aligned.real)
        recon = 0.5 * bc * g_cross
        w_recon_errs.append(abs(g_w - recon))
        # 90° identity: (p̂ × q) · h_p = i s_p (q · h_p)
        rot_errs.append(abs(kn["p_hat_cross_q_dot_hp"] - 1j * sp * kn["q_dot_hp"]))
        # Corollary: g_W / g_ordered = i (b-c) / (2 s_p |μ|) ∈ iℝ.
        if abs(g_ordered) > 1e-14 and abs(g_w) > 1e-14:
            predicted_wo = 1j * bc / (2.0 * float(sp) * aligned.real)
            if abs(g_w / g_ordered - predicted_wo) > 1e-9:
                raise AssertionError("g_W/g_ordered is not i(b-c)/(2 s_p |μ|)")
    spread = max(abs(z - aligned_vals[0]) for z in aligned_vals)
    return {
        "max_phase_err": max(phase_errs),
        "min_aligned_real": min(z.real for z in aligned_vals),
        "axis_spread": spread,
        "max_gW_recon_err": max(w_recon_errs),
        "max_rot_err": max(rot_errs),
        "abs_mu": sum(abs_mu) / len(abs_mu),
        "b_minus_c": bc,
        "gW_vanishes": abs(bc) <= 1e-12,
    }


def _cpx(z: complex) -> Dict[str, float]:
    return {
        "re": float(z.real),
        "im": float(z.imag),
        "abs": float(abs(z)),
        "arg": float(cmath.phase(z)) if abs(z) else 0.0,
    }


def channel_record(
    delta_id: str,
    p: Mode,
    q: Mode,
    k: Mode,
    sigma: Sigma,
    axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> dict:
    """One signed channel γ=(Δ,σ) on the frozen representative."""
    sk, sp, sq = sigma
    rad = channel_radii(p, q, k, sigma)
    a_s, b_s, c_s = signed_radii(p, q, k, sigma)
    kn = kernels(p, q, k, sigma, axis)
    g_cross = kn["g_cross"]
    g_ordered = kn["g_ordered"]
    g_w = kn["g_W"]
    aligned = mu_factor(g_ordered, g_cross, sp)
    A = A_coeff(rad["i"], rad["j"], rad["o"])
    return {
        "gamma": {
            "delta_id": delta_id,
            "p": list(p),
            "q": list(q),
            "k": list(k),
            "sigma_kpq": [sk, sp, sq],
        },
        "odd_leg": rad["odd"],
        "radii": {"i": rad["i"], "j": rad["j"], "o": rad["o"]},
        "signed_radii": {"a": a_s, "b": b_s, "c": c_s},
        "A_gamma": A,
        "H_ijo": H_ijo(rad["i"], rad["j"], rad["o"]),
        "g_Delta_sigma": _cpx(g_cross),
        "g_ordered": _cpx(g_ordered),
        "g_W": _cpx(g_w),
        "mu_aligned": _cpx(aligned),
        "phase_offset_ordered_minus_cross": arg_delta_ordered_minus_cross(sp),
        "channel_phase_invariant": float(cmath.phase(g_cross)),
        "vandermonde_k": b_s - c_s,
        "notes": {
            "g_gamma_is_G_cross": True,
            "g_W_is_k_leg_fold": True,
            "Q_a_gamma_is_2_o_tau_o": True,
        },
    }


def canonical_24_payload(axis: Sequence[float] = (0.0, 0.0, 1.0)) -> dict:
    channels = []
    for delta_id, p, q, k in PARALLELOGRAM:
        for sigma in HETEROCHIRAL_SIGMA:
            channels.append(channel_record(delta_id, p, q, k, sigma, axis))
    cycle = list(PARALLELOGRAM_CYCLE)
    # Per-σ holonomy correction if one swapped args without the −s_p π/2.
    # Assign the same σ-slot across the 4 geometric Δ, then form c·(s_p).
    s_p_by_slot = [sig[1] for sig in HETEROCHIRAL_SIGMA]
    # For a loop of 4 triads using one common σ-slot, ∑ c_e s_{p_e} = s_p ∑ c_e = 0.
    # Mixed σ around the loop is not the 24-channel catalog (each γ is independent).
    return {
        "stamp": "gamma = (Delta, sigma)",
        "sigma_convention": "(s_k, s_p, s_q)",
        "n_geometric_delta": len(PARALLELOGRAM),
        "n_heterochiral_sigma": len(HETEROCHIRAL_SIGMA),
        "n_channels": len(channels),
        "representative": "locked parallelogram p+q=k from LOOP-GAUGE",
        "cycle_vector": cycle,
        "cycle_sum": int(sum(cycle)),
        "uniform_phase_drops_from_holonomy": int(sum(cycle)) == 0,
        "heterochiral_sigma_kpq": [list(s) for s in HETEROCHIRAL_SIGMA],
        "same_sigma_slot_sp_weighted_cycle": {
            "s_p_by_slot": s_p_by_slot,
            "c_dot_1": int(sum(cycle)),
            "comment": (
                "A common σ-slot around the parallelogram gives "
                "∑ c_e s_{p_e} = s_p ∑ c_e = 0. The −s_p π/2 translation "
                "does not move Ω_c on this catalog. Mixed-σ loops must "
                "track the correction explicitly."
            ),
        },
        "channels": channels,
        "not_a_close": True,
        "v2_not_run": True,
    }


def identity_report(tol: float = 1e-12) -> dict:
    rows = []
    max_phase = 0.0
    max_spread = 0.0
    max_w = 0.0
    max_rot = 0.0
    triads: List[Tuple[str, Mode, Mode, Mode]] = [
        (name, p, q, k) for name, p, q, k in PARALLELOGRAM
    ]
    for i, (p, q, k) in enumerate(PROBE_TRIADS):
        triads.append((f"probe{i+1}", p, q, k))
    n_cert = 0
    n_gW_zero = 0
    for name, p, q, k in triads:
        for sigma in HETEROCHIRAL_SIGMA:
            cert = certify_one(p, q, k, sigma, AXES, tol)
            n_cert += 1
            max_phase = max(max_phase, cert["max_phase_err"])
            max_spread = max(max_spread, cert["axis_spread"])
            max_w = max(max_w, cert["max_gW_recon_err"])
            max_rot = max(max_rot, cert["max_rot_err"])
            if cert["gW_vanishes"]:
                n_gW_zero += 1
            rows.append(
                {
                    "delta": name,
                    "p": list(p),
                    "q": list(q),
                    "k": list(k),
                    "sigma_kpq": list(sigma),
                    "odd_leg": odd_leg(sigma),
                    **cert,
                }
            )
    passed = (
        max_phase < 1e-10
        and max_spread < 1e-10
        and max_w < 1e-10
        and max_rot < 1e-10
    )
    return {
        "identity": "g_ordered = -i s_p |μ| G_cross",
        "g_W_identity": "g_W = (1/2)(s_p|p|-s_q|q|) G_cross",
        "rotation_identity": "(p-hat × q) · h_p = i s_p (q · h_p)",
        "n_certified": n_cert,
        "n_heterochiral_sigma": 6,
        "n_gW_zero_channels": n_gW_zero,
        "max_phase_err": max_phase,
        "max_axis_spread_of_mu": max_spread,
        "max_gW_recon_err": max_w,
        "max_rotation_err": max_rot,
        "passed": passed,
        "rows": rows,
        "stamp_ready": passed,
        "v2_not_run": True,
        "not_a_close": True,
    }
