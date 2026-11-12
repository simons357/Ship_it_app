"""Centered spectral drift: exact identities, open remainder.

The centered equation is

    Lambda' = -(2 nu / X) D_s + (2 / X) T_c = 2 (T_c - nu D_s) / X.

That identity is algebra, not an estimate. The drift estimate

    T_c <= theta * nu * D_s + K(t) X,   theta in [0, 1),  K in L^1_loc

is OPEN. Defining K = (T_c - theta nu D_s)_+ / X makes it a tautology.
Ordinary unaugmented 3-D Navier–Stokes is not solved. Lemma-star is
not proved. Do not put K(t) in the PDE.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, Tuple

import numpy as np

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ns_lemma_star_core as core  # noqa: E402

Mode = Tuple[int, int, int]
ROOT = Path(__file__).resolve().parents[2]
OUT_DEFAULT = ROOT / "results" / "centered_drift.json"


def near_scale_triad(closer_amp: float = 1.0) -> core.Field:
    """Section-4 field: p=(1,0,0), q=(0,1,0), r=(1,1,0).

    closer_amp scales only the closing mode on shell |k|^2=2. Amplitude 1
    is the locked note triad. Smaller amplitude is the near-shell
    linearization (T_c ~ eps, D_s ~ eps^2).
    """
    field = core.Field()
    p, q, r = (1, 0, 0), (0, 1, 0), (1, 1, 0)
    a = np.array([0.0, 1.0, 0.0], dtype=complex)
    b = np.array([1.0, 0.0, 1.0], dtype=complex)
    c = np.array([0.0, 0.0, 1.0], dtype=complex)
    field.set_mode(p, a)
    field.set_mode(q, b)
    field.set_mode(r, -1j * float(closer_amp) * c)
    return field


def two_shell_field() -> core.Field:
    """Two exact shells, no triad flux: D_s identity only."""
    field = core.Field()
    field.set_mode((1, 0, 0), [0.0, 1.0, 0.0])
    field.set_mode((2, 0, 0), [0.0, 0.0, 1.0])
    return field


def single_shell_field() -> core.Field:
    field = core.Field()
    field.set_mode((1, 0, 0), [0.0, 1.0, 0.0])
    field.set_mode((0, 1, 0), [1.0, 0.0, 0.0])
    return field


def modal_tau(field: core.Field) -> Dict[Mode, float]:
    out: Dict[Mode, float] = {}
    for k, vk in field.modes.items():
        Bk = core.B_hat_at(field, k)
        out[k] = -float(np.real(np.dot(Bk, np.conj(vk))))
    return out


def occupancy(field: core.Field, X: float) -> Dict[Mode, float]:
    """p_k = lambda_k |v_k|^2 / X. Mean_p(lambda) = Lambda."""
    if X <= 0:
        return {}
    return {
        k: core.lam(k) * float(np.vdot(vk, vk).real) / X
        for k, vk in field.modes.items()
    }


def stretch_density(field: core.Field, tau: Dict[Mode, float]) -> Dict[Mode, float]:
    """t_k = T_k / |v_k|^2 on occupied modes, else 0.

    With p_k as in occupancy, T_c = X Cov_p(lambda, t).
    """
    out: Dict[Mode, float] = {}
    for k, vk in field.modes.items():
        e = float(np.vdot(vk, vk).real)
        out[k] = (tau[k] / e) if e > 1e-15 else 0.0
    return out


def barycenter(field: core.Field, X: float, Lambda: float, Ds: float, Tc: float, tau: Dict[Mode, float]) -> dict:
    p = occupancy(field, X)
    t = stretch_density(field, tau)
    mean_lam = sum(p[k] * core.lam(k) for k in p)
    mean_t = sum(p[k] * t[k] for k in p)
    mean_lam_t = sum(p[k] * core.lam(k) * t[k] for k in p)
    var_lam = sum(p[k] * (core.lam(k) - Lambda) ** 2 for k in p)
    cov = mean_lam_t - Lambda * mean_t
    return {
        "mean_lambda": mean_lam,
        "var_lambda": var_lam,
        "cov_lambda_t": cov,
        "D_s_from_var": X * var_lam,
        "T_c_from_cov": X * cov,
        "mean_lambda_minus_Lambda": mean_lam - Lambda,
        "D_s_check": Ds - X * var_lam,
        "T_c_check": Tc - X * cov,
    }


def two_shell_Ds_closed(alpha: float, beta: float, e_alpha: float, e_beta: float, X: float) -> float:
    return alpha * beta * (alpha - beta) ** 2 * e_alpha * e_beta / X


def record(field: core.Field) -> dict:
    E, X, Y, Z, Lambda = core.moments(field)
    Ds_m = core.D_s_moment_form(X, Y, Z)
    Ds_d = core.D_s_direct_form(field, Lambda)
    tau = modal_tau(field)
    N = 0.0
    M = 0.0
    shell_energy: Dict[float, float] = {}
    for k, tk in tau.items():
        ell = core.lam(k)
        e = float(np.vdot(field.modes[k], field.modes[k]).real)
        N += ell * tk
        M += ell * ell * tk
        shell_energy[ell] = shell_energy.get(ell, 0.0) + e
    Tc = M - Lambda * N
    Tc_direct = core.T_c_direct(field, Lambda)
    bary = barycenter(field, X, Lambda, Ds_m, Tc, tau)
    two_shell = None
    if len(shell_energy) == 2:
        (alpha, e_alpha), (beta, e_beta) = list(shell_energy.items())
        two_shell = {
            "alpha": alpha,
            "beta": beta,
            "e_alpha": e_alpha,
            "e_beta": e_beta,
            "D_s_closed": two_shell_Ds_closed(alpha, beta, e_alpha, e_beta, X),
        }
    return {
        "E": E,
        "X": X,
        "Y": Y,
        "Z": Z,
        "Lambda": Lambda,
        "D_s": Ds_m,
        "D_s_direct": Ds_d,
        "N": N,
        "M": M,
        "T_c": Tc,
        "T_c_direct": Tc_direct,
        "tau": {str(k): v for k, v in tau.items()},
        "shell_energy": {str(k): v for k, v in shell_energy.items()},
        "barycenter": bary,
        "two_shell": two_shell,
        "div_free": all(
            abs(np.dot(np.array(k, dtype=float), vk)) < 1e-12
            for k, vk in field.modes.items()
        ),
        "real": all(
            np.allclose(field.modes[tuple(-x for x in k)], np.conj(vk))
            for k, vk in field.modes.items()
        ),
        "homogeneity": {"T_c_degree": 3, "D_s_degree": 2},
        "ns_solved": False,
        "lemma_star_proved": False,
        "remainder_open": True,
    }


def algebraic_identity(nu: float, X: float, Y: float, Z: float, N: float, M: float) -> dict:
    """Lambda' from (X', Y') equals 2 (T_c - nu D_s) / X."""
    Lambda = Y / X
    Xp = -2.0 * nu * Y + 2.0 * N
    Yp = -2.0 * nu * Z + 2.0 * M
    Lambda_p = (Yp * X - Y * Xp) / (X * X)
    Ds = Z - Y * Y / X
    Tc = M - Lambda * N
    rhs = 2.0 * (Tc - nu * Ds) / X
    return {
        "nu": nu,
        "Lambda_prime": Lambda_p,
        "rhs": rhs,
        "residual": Lambda_p - rhs,
        "log_Lambda_prime": 2.0 * (Tc - nu * Ds) / Y,
    }


def note_triad_snapshot() -> dict:
    rec = record(near_scale_triad(1.0))
    rec["algebra"] = algebraic_identity(1.0, rec["X"], rec["Y"], rec["Z"], rec["N"], rec["M"])
    rec["T_c_over_D_s"] = rec["T_c"] / rec["D_s"]
    rec["locked"] = {
        "X": 10.0,
        "Y": 14.0,
        "Z": 22.0,
        "Lambda": 7.0 / 5.0,
        "D_s": 12.0 / 5.0,
        "N": 2.0,
        "M": 6.0,
        "T_c": 16.0 / 5.0,
        "T_c_over_D_s": 4.0 / 3.0,
    }
    return rec


def amplitude_kill(base: core.Field) -> dict:
    rows = []
    for a in (0.5, 1.0, 2.0, 4.0):
        rec = record(base.scale(a))
        rows.append(
            {
                "a": a,
                "T_c": rec["T_c"],
                "D_s": rec["D_s"],
                "T_c_over_D_s": rec["T_c"] / rec["D_s"],
            }
        )
    ratios = [row["T_c_over_D_s"] / row["a"] for row in rows]
    return {
        "rows": rows,
        "ratio_over_a_constant": ratios,
        "pure_absorption_T_c_le_C_nu_Ds": "KILLED",
        "reason": "T_c(au)=a^3 T_c(u), D_s(au)=a^2 D_s(u), so T_c/D_s scales as |a|.",
    }


def near_shell_scan() -> dict:
    rows = []
    for eps in (1.0, 0.5, 0.25, 0.125, 0.0625):
        rec = record(near_scale_triad(eps))
        rows.append(
            {
                "eps": eps,
                "T_c": rec["T_c"],
                "D_s": rec["D_s"],
                "T_c_over_D_s": rec["T_c"] / rec["D_s"],
                "T_c_over_eps": rec["T_c"] / eps,
                "D_s_over_eps2": rec["D_s"] / (eps * eps),
            }
        )
    return {
        "rows": rows,
        "obstruction": "near-shell linearization as eps->0: T_c ~ eps, D_s ~ eps^2, ratio -> inf",
        "not_a_C_geom_theorem": True,
    }


def package() -> dict:
    note = note_triad_snapshot()
    one = record(single_shell_field())
    two = record(two_shell_field())
    flipped = record(near_scale_triad(1.0).scale(-1.0))
    return {
        "object": "centered spectral drift",
        "centered_equation": "Lambda' = 2 (T_c - nu D_s) / X",
        "identity": "EXACT",
        "drift_estimate": "OPEN",
        "uniform_remainder": "KILLED",
        "need_star": "MISSING",
        "ns_solved": False,
        "lemma_star_proved": False,
        "remainder_open": True,
        "do_not_put_K_in_the_PDE": True,
        "note_triad": note,
        "single_shell": {
            "D_s": one["D_s"],
            "T_c": one["T_c"],
            "vacuous": abs(one["D_s"]) < 1e-12 and abs(one["T_c"]) < 1e-12,
        },
        "two_shell": two,
        "sign_flip_T_c": flipped["T_c"],
        "amplitude_kill": amplitude_kill(near_scale_triad(1.0)),
        "near_shell_scan": near_shell_scan(),
        "smooth_split_citation": "PR #149 instantaneous |T_c| <= C g sqrt(Y D_s); not a time budget",
        "open_target": "T_c <= theta nu D_s + K(t) X with theta < 1 and non-tautological K in L^1_loc from admissible data",
    }


def main() -> None:
    payload = package()
    OUT_DEFAULT.parent.mkdir(parents=True, exist_ok=True)
    OUT_DEFAULT.write_text(json.dumps(payload, indent=2, default=float) + "\n", encoding="utf-8")
    note = payload["note_triad"]
    print("centered drift")
    print(f"  identity: {payload['centered_equation']}  [{payload['identity']}]")
    print(f"  note triad T_c = {note['T_c']:.12f}  (locked 16/5)")
    print(f"  note triad D_s = {note['D_s']:.12f}  (locked 12/5)")
    print(f"  T_c/D_s        = {note['T_c_over_D_s']:.12f}  (locked 4/3)")
    print(f"  algebra residual = {note['algebra']['residual']:.3e}")
    print(f"  drift estimate: {payload['drift_estimate']}")
    print(f"  ns_solved: {payload['ns_solved']}")
    print(f"  wrote {OUT_DEFAULT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
