"""Fourier-triangle geometry: identities, not a close.

Reconstructs the cubic vertex I3, Leray-idle pairing, equal-length
cancel, unequal-length defect, and phase-signed transfer.

Does not overwrite stokes_moments.py.
Does not restore ★.
Does not seat B★.
Does not start leftover 1.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_lemma_star_core import (  # noqa: E402
    B_hat_at,
    Field,
    T_c_direct,
    T_k_map,
    lam,
    moments,
    project_perp,
    sum_Tk,
)

OUT = ROOT / "results" / "fourier_triangle.json"


def _unit_divfree(k, seed):
    k = tuple(int(x) for x in k)
    v = project_perp(k, np.asarray(seed, dtype=complex))
    nrm = float(np.linalg.norm(v))
    if nrm < 1e-15:
        v = project_perp(k, np.array([seed[1], seed[2], seed[0]], dtype=complex))
        nrm = float(np.linalg.norm(v))
    if nrm < 1e-15:
        raise ValueError(f"no transverse seed at {k}")
    return v / nrm


def closed_triad(p, q, amps, phases, seeds) -> Field:
    """Conjugate-closed resonant triad p + q = k."""
    p = tuple(int(x) for x in p)
    q = tuple(int(x) for x in q)
    k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
    if k == (0, 0, 0) or p == (0, 0, 0) or q == (0, 0, 0):
        raise ValueError("triangle keys must be nonzero")
    f = Field()
    for key, amp, phase, seed in zip((p, q, k), amps, phases, seeds):
        v = _unit_divfree(key, seed) * amp * np.exp(1j * phase)
        f.set_mode(key, v)
    return f


def isosceles_hh_l(amp=1.0, phase_q=0.5) -> Field:
    """Attack-8 / LEMMA-STAR-E triangle: |p|^2=|q|^2=2, |k|^2=4.

    Seeds must have an in-plane leg. Pure-z on both inputs makes
    q·v_p=0 (Leray-idle *and* vertex-idle). That is a polarization
    cancel, not the two-shell identity.
    """
    return closed_triad(
        (1, 1, 0),
        (1, -1, 0),
        (amp, amp, amp),
        (0.0, phase_q, -0.3),
        ((1.0, -1.0, 0.4), (1.0, 1.0, 0.4), (0.0, 1.0, 0.7)),
    )


def three_shell_unequal(amp=(1.0, 0.4, 0.3), phase_mid=0.4) -> Field:
    """k0 + (k0+e) = 2k0+e with three distinct |·|^2: 4, 5, 17."""
    k0 = (2, 0, 0)
    e = (0, 1, 0)
    p = k0
    q = (k0[0] + e[0], k0[1] + e[1], k0[2] + e[2])
    return closed_triad(
        p,
        q,
        amp,
        (0.0, phase_mid, -0.2),
        ((0.0, 1.0, 0.2), (1.0, 0.0, 0.3), (0.2, 0.5, 1.0)),
    )


def one_shell_field(n=2) -> Field:
    f = Field()
    f.set_mode((n, 0, 0), (0.0, 1.0, 0.0))
    f.set_mode((0, n, 0), (0.0, 0.0, 1.0))
    return f


def vertex_I3(field: Field, p, q, k) -> complex:
    """Raw cubic vertex (q·v_p)(v_q · conj(v_k)). Signed transfer is Im."""
    vp = field.get(p)
    vq = field.get(q)
    vk = field.get(k)
    qf = np.array(q, dtype=float)
    return np.dot(qf, vp) * np.dot(vq, np.conj(vk))


def T_k_without_leray(field: Field, k) -> float:
    """Energy pairing with P_k omitted. Must match T_k: Leray is idle."""
    k = tuple(int(x) for x in k)
    vk = field.get(k)
    total = np.zeros(3, dtype=complex)
    for p, vp in field.modes.items():
        q = (k[0] - p[0], k[1] - p[1], k[2] - p[2])
        if q == (0, 0, 0):
            continue
        vq = field.modes.get(q)
        if vq is None:
            continue
        total += np.dot(np.array(q, dtype=float), vp) * vq
    Bk = 1j * total
    return -float(np.real(np.dot(Bk, np.conj(vk))))


def two_shell_reduction(field: Field) -> dict:
    """On exactly two eigenvalues, T_c reduces to one signed T times a gap."""
    shells: dict[float, list] = {}
    Tk = T_k_map(field)
    for k, vk in field.modes.items():
        shells.setdefault(lam(k), []).append((k, float(np.vdot(vk, vk).real), Tk[k]))
    if len(shells) != 2:
        return {"two_shell": False}
    (alpha, a_items), (beta, b_items) = sorted(shells.items())
    e_a = sum(e for _, e, _ in a_items)
    e_b = sum(e for _, e, _ in b_items)
    T_a = sum(t for _, _, t in a_items)
    T_b = sum(t for _, _, t in b_items)
    E, X, Y, Z, Lambda = moments(field)
    Tc = T_c_direct(field, Lambda)
    pred = (alpha - beta) * (alpha * beta * E / X) * T_a
    pred_b = -(alpha - beta) * (alpha * beta * E / X) * T_b
    Ds = alpha * beta * (alpha - beta) ** 2 * e_a * e_b / X
    return {
        "two_shell": True,
        "alpha": alpha,
        "beta": beta,
        "e_a": e_a,
        "e_b": e_b,
        "T_a": T_a,
        "T_b": T_b,
        "T_a_plus_T_b": T_a + T_b,
        "Tc": Tc,
        "pred_from_Ta": pred,
        "pred_from_Tb": pred_b,
        "Ds_two_shell": Ds,
        "Ds_moment": Z - Y * Y / X,
        "gap_in_Rstar_cancels": True,
    }


def three_shell_defect(field: Field) -> dict:
    """Three distinct λ: T_c is not a single T_k times one gap."""
    Tk = T_k_map(field)
    by = {}
    for k, t in Tk.items():
        by.setdefault(lam(k), 0.0)
        by[lam(k)] += t
    E, X, Y, Z, Lambda = moments(field)
    Tc = T_c_direct(field, Lambda)
    weights = {l: l * (l - Lambda) for l in by}
    # If it reduced, Tc / T_λ would be the same gap for every shell. It is not.
    ratios = {}
    for l, t in by.items():
        ratios[l] = (Tc / t) if abs(t) > 1e-14 else float("nan")
    return {
        "n_shells": len(by),
        "T_by_shell": by,
        "weights": weights,
        "Tc": Tc,
        "Tc_over_T_shell": ratios,
        "reducible_to_one_gap": False,
    }


def phase_scan(builder, n=21) -> dict:
    phases = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    tcs = []
    for ph in phases:
        f = builder(ph)
        _E, _X, _Y, _Z, Lam = moments(f)
        tcs.append(T_c_direct(f, Lam))
    tcs = np.array(tcs)
    return {
        "n": n,
        "min": float(tcs.min()),
        "max": float(tcs.max()),
        "changes_sign": bool(tcs.min() < -1e-10 and tcs.max() > 1e-10),
        "not_identically_zero": bool(np.max(np.abs(tcs)) > 1e-10),
    }


def record() -> dict:
    iso = isosceles_hh_l()
    uneq = three_shell_unequal()
    one = one_shell_field()
    idle = closed_triad(
        (1, 1, 0),
        (1, -1, 0),
        (1.0, 1.0, 1.0),
        (0.0, 0.5, -0.3),
        ((0.0, 0.0, 1.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0)),
    )

    iso_Tk = T_k_map(iso)
    uneq_Tk = T_k_map(uneq)
    one_mom = moments(one)
    iso_mom = moments(iso)
    uneq_mom = moments(uneq)

    leray_idle = []
    for field, Tk in ((iso, iso_Tk), (uneq, uneq_Tk)):
        for k, t in Tk.items():
            raw = T_k_without_leray(field, k)
            leray_idle.append(abs(t - raw))

    iso_red = two_shell_reduction(iso)
    uneq_def = three_shell_defect(uneq)

    def iso_at(ph):
        return isosceles_hh_l(phase_q=ph)

    def uneq_at(ph):
        return three_shell_unequal(phase_mid=ph)

    scan_iso = phase_scan(iso_at)
    scan_uneq = phase_scan(uneq_at)

    # I3 on the isosceles closer: p+q=k and the swapped order.
    p, q, k = (1, 1, 0), (1, -1, 0), (2, 0, 0)
    I_pq = vertex_I3(iso, p, q, k)
    I_qp = vertex_I3(iso, q, p, k)

    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "bstar_not_seated": True,
        "identities": {
            "energy_sum_iso": float(sum_Tk(iso)),
            "energy_sum_uneq": float(sum_Tk(uneq)),
            "energy_sum_one": float(sum_Tk(one)),
            "leray_idle_max_abs": float(max(leray_idle)),
            "one_shell_Tc": float(T_c_direct(one, one_mom[4])),
            "one_shell_Ds": float(one_mom[3] - one_mom[2] ** 2 / one_mom[1]),
            "iso_two_shell": iso_red,
            "uneq_three_shell": uneq_def,
            "iso_I3_pq_im": float(I_pq.imag),
            "iso_I3_qp_im": float(I_qp.imag),
            "idle_z_pol_Tc": float(T_c_direct(idle, moments(idle)[4])),
            "idle_z_pol_I3_im": float(vertex_I3(idle, p, q, k).imag),
        },
        "numerical": {
            "iso_Tc": float(T_c_direct(iso, iso_mom[4])),
            "uneq_Tc": float(T_c_direct(uneq, uneq_mom[4])),
            "iso_phase_scan": scan_iso,
            "uneq_phase_scan": scan_uneq,
            "iso_reduction_residual": float(
                abs(iso_red["Tc"] - iso_red["pred_from_Ta"])
            ),
            "iso_energy_shell_residual": float(abs(iso_red["T_a_plus_T_b"])),
            "uneq_n_shells": uneq_def["n_shells"],
        },
        "illustrative": {
            "motion": "phase of one leg rotates T_c through both signs; not a trajectory",
            "not_NSE": True,
        },
        "I3_prime": {
            "sit": [
                "lattice triangle p+q=k",
                "transverse polarizations",
                "Leray idle in the energy pairing",
                "reality v_{-k}=conj(v_k)",
                "cyclic energy T_p+T_q+T_k=0",
                "equal-length kills the T_c weight",
                "two-shell gap-cancel of (alpha-beta) in R_star",
            ],
            "not_prime": [
                "prime |k|^2 shells only",
                "primitive gcd=1 triangles as a bound",
                "leftover 3 / H3 absorb",
                "Q-matrix prime block",
                "unsigned |I3|",
                "HH->L only",
            ],
        },
        "first_missing": (
            "exact signed triad sum does not imply "
            "T_c <= theta nu D_s + K(t) X with useful K"
        ),
    }
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
