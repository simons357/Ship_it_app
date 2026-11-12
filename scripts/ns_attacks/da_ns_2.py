"""DA-NS-2: Y-cousin occupation bound. Identities sit. The integral is OPEN.

On Galerkin n and fixed theta in [0, 1),

    K_min,theta = [T_c - theta * nu * D_s]_+ / Y

DA-NS-2 is the cutoff-uniform claim

    sup_n int_0^T K_min,theta^(n)(t) dt  <=  F(nu, T, u0) < infinity

without a continuation norm. If it sits, Lambda stays bounded, then
X <= |u0|_2^2 Lambda, then continuation. That implication is the usual
skeleton. The integral is the hole.

Defining K_Y as that ratio makes the Y-estimate a tautology, not a
theorem. Charge-only, frozen-charge theta=1, and pure absorption do
not close it. Ordinary unaugmented 3-D Navier–Stokes is not solved.
Do not put K(t) in the PDE. Do not glue to Phi-renorm or Clay Statement B.
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
OUT_DEFAULT = ROOT / "results" / "da_ns_2.json"

FORBIDDEN_LAST_LINES = (
    "int D_s/Y",
    "int (N/X)_+",
    "sup Lambda",
    "int Y",
    "Serrin",
    "BKM",
    "continuation norm",
    "H^1 ceiling",
    "L^infty",
    "||u||_H1",
)

JGC_BUDGET_TERMS = (
    "charge",
    "radial covariance",
    "moving-barycenter error",
    "homochiral drift",
    "cross-band flux",
    "phase/far terms",
    "one-use dissipation",
    "summable resets",
)


def near_scale_triad(closer_amp: float = 1.0) -> core.Field:
    """Section-4 field: p=(1,0,0), q=(0,1,0), r=(1,1,0)."""
    field = core.Field()
    p, q, r = (1, 0, 0), (0, 1, 0), (1, 1, 0)
    a = np.array([0.0, 1.0, 0.0], dtype=complex)
    b = np.array([1.0, 0.0, 1.0], dtype=complex)
    c = np.array([0.0, 0.0, 1.0], dtype=complex)
    field.set_mode(p, a)
    field.set_mode(q, b)
    field.set_mode(r, -1j * float(closer_amp) * c)
    return field


def single_shell_field() -> core.Field:
    field = core.Field()
    field.set_mode((1, 0, 0), [0.0, 1.0, 0.0])
    field.set_mode((0, 1, 0), [1.0, 0.0, 0.0])
    return field


def two_shell_field() -> core.Field:
    field = core.Field()
    field.set_mode((1, 0, 0), [0.0, 1.0, 0.0])
    field.set_mode((2, 0, 0), [0.0, 0.0, 1.0])
    return field


def positive_part(x: float) -> float:
    return x if x > 0.0 else 0.0


def occupation(T_c: float, D_s: float, Y: float, nu: float, theta: float) -> float:
    """K_min,theta = [T_c - theta nu D_s]_+ / Y."""
    if Y <= 0.0:
        raise ValueError("Y must be positive to form K_min.")
    return positive_part(T_c - theta * nu * D_s) / Y


def x_cousin(T_c: float, D_s: float, X: float, nu: float, theta: float) -> float:
    """Tautological X-remainder K = [T_c - theta nu D_s]_+ / X (DA-NS-1 packaging)."""
    if X <= 0.0:
        raise ValueError("X must be positive to form the X-cousin.")
    return positive_part(T_c - theta * nu * D_s) / X


def modal_tau(field: core.Field) -> Dict[Mode, float]:
    out: Dict[Mode, float] = {}
    for k, vk in field.modes.items():
        Bk = core.B_hat_at(field, k)
        out[k] = -float(np.real(np.dot(Bk, np.conj(vk))))
    return out


def record(field: core.Field) -> dict:
    E, X, Y, Z, Lambda = core.moments(field)
    Ds_m = core.D_s_moment_form(X, Y, Z)
    Ds_d = core.D_s_direct_form(field, Lambda)
    tau = modal_tau(field)
    N = 0.0
    M = 0.0
    for k, tk in tau.items():
        ell = core.lam(k)
        N += ell * tk
        M += ell * ell * tk
    Tc = M - Lambda * N
    Tc_direct = core.T_c_direct(field, Lambda)
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
        "ns_solved": False,
        "da_ns_2": "OPEN",
        "lemma_star_proved": False,
    }


def k_min_row(rec: dict, nu: float, theta: float) -> dict:
    k_y = occupation(rec["T_c"], rec["D_s"], rec["Y"], nu, theta)
    k_x = x_cousin(rec["T_c"], rec["D_s"], rec["X"], nu, theta)
    leftover = (1.0 - theta) * nu * rec["D_s"] / rec["Y"]
    log_prime = 2.0 * (rec["T_c"] - nu * rec["D_s"]) / rec["Y"]
    return {
        "nu": nu,
        "theta": theta,
        "K_min": k_y,
        "K_X": k_x,
        "Lambda_K_min": rec["Lambda"] * k_y,
        "frozen_theta_leftover": leftover,
        "log_Lambda_prime": log_prime,
        "log_Lambda_prime_le_2_K_min": log_prime <= 2.0 * k_y + 1e-12,
        "gap": 2.0 * k_y - log_prime,
    }


def tautology_identity(rec: dict, nu: float, theta: float) -> dict:
    """T_c <= theta nu D_s + K_min Y is an identity, not a theorem."""
    k_y = occupation(rec["T_c"], rec["D_s"], rec["Y"], nu, theta)
    lhs = rec["T_c"]
    rhs = theta * nu * rec["D_s"] + k_y * rec["Y"]
    return {
        "lhs": lhs,
        "rhs": rhs,
        "residual": lhs - rhs,
        "is_identity_not_theorem": True,
        "reason": "K_min is defined as the positive part over Y.",
    }


def algebraic_log_bound(rec: dict, nu: float, theta: float) -> dict:
    """(log Lambda)' <= 2 K_min always; leftover (1-theta) nu D_s/Y is why theta=1 is not the endpoint."""
    row = k_min_row(rec, nu, theta)
    rewritten = (
        2.0 * (rec["T_c"] - theta * nu * rec["D_s"]) / rec["Y"]
        - 2.0 * (1.0 - theta) * nu * rec["D_s"] / rec["Y"]
    )
    return {
        **row,
        "log_Lambda_prime_rewritten": rewritten,
        "rewrite_residual": row["log_Lambda_prime"] - rewritten,
        "theta_lt_1_leftover_survives": abs(theta - 1.0) > 1e-15,
    }


def note_triad_snapshot() -> dict:
    rec = record(near_scale_triad(1.0))
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
    rec["K_min_nu1"] = {
        "theta_0": occupation(rec["T_c"], rec["D_s"], rec["Y"], 1.0, 0.0),
        "theta_half": occupation(rec["T_c"], rec["D_s"], rec["Y"], 1.0, 0.5),
        "locked_theta_0": (16.0 / 5.0) / 14.0,
        "locked_theta_half": (16.0 / 5.0 - 0.5 * 12.0 / 5.0) / 14.0,
    }
    rec["tautology"] = tautology_identity(rec, 1.0, 0.5)
    rec["log_bound"] = algebraic_log_bound(rec, 1.0, 0.5)
    rec["cousin"] = k_min_row(rec, 1.0, 0.5)
    return rec


def amplitude_occupation(base: core.Field, nu: float = 1.0, theta: float = 0.5) -> dict:
    rows = []
    for a in (0.5, 1.0, 2.0, 4.0):
        rec = record(base.scale(a))
        k_y = occupation(rec["T_c"], rec["D_s"], rec["Y"], nu, theta)
        rows.append(
            {
                "a": a,
                "T_c": rec["T_c"],
                "D_s": rec["D_s"],
                "Y": rec["Y"],
                "K_min": k_y,
                "T_c_over_D_s": rec["T_c"] / rec["D_s"],
            }
        )
    return {
        "rows": rows,
        "pure_absorption_T_c_le_theta_nu_Ds": "KILLED",
        "reason": "T_c(au)=a^3 T_c(u), D_s(au)=a^2 D_s(u); Y(au)=a^2 Y(u). Ratio T_c/D_s scales as |a|.",
    }


def near_shell_occupation() -> dict:
    rows = []
    for eps in (1.0, 0.5, 0.25, 0.125, 0.0625):
        rec = record(near_scale_triad(eps))
        rows.append(
            {
                "eps": eps,
                "T_c": rec["T_c"],
                "D_s": rec["D_s"],
                "Y": rec["Y"],
                "T_c_over_D_s": rec["T_c"] / rec["D_s"],
                "K_min_theta0": occupation(rec["T_c"], rec["D_s"], rec["Y"], 1.0, 0.0),
            }
        )
    return {
        "rows": rows,
        "T_c_over_D_s": "blows as 1/eps",
        "K_min_on_this_family": "stays O(eps) because Y stays O(1); snapshot smallness is not the integral bound",
        "not_a_C_geom_theorem": True,
    }


def phase_twin_occupation(nu: float = 1.0, theta: float = 0.0) -> dict:
    plus = record(near_scale_triad(1.0))
    minus = record(near_scale_triad(1.0).scale(-1.0))
    k_plus = occupation(plus["T_c"], plus["D_s"], plus["Y"], nu, theta)
    k_minus = occupation(minus["T_c"], minus["D_s"], minus["Y"], nu, theta)
    return {
        "same_X": plus["X"] == minus["X"],
        "same_Y": plus["Y"] == minus["Y"],
        "same_Z": plus["Z"] == minus["Z"],
        "same_D_s": abs(plus["D_s"] - minus["D_s"]) < 1e-12,
        "T_c_plus": plus["T_c"],
        "T_c_minus": minus["T_c"],
        "K_min_plus": k_plus,
        "K_min_minus": k_minus,
        "quadratic_moments_see_the_sign": False,
        "kill": "phase twins share X,Y,Z,Lambda,D_s and flip T_c, so K_min is not a function of quadratic data",
    }


def classify_last_line(text: str) -> dict:
    """Joint Gap-Charge epoch budget: refuse continuation-norm last lines."""
    lowered = text.lower().replace("λ", "lambda").replace("Λ", "lambda")
    lowered = lowered.replace("∫", "int ").replace("≤", "<=")
    hits = [item for item in FORBIDDEN_LAST_LINES if item.lower() in lowered]
    jgc_hits = [item for item in JGC_BUDGET_TERMS if item.lower() in lowered]
    if hits:
        status = "REJECTED"
        reason = "last line is a continuation norm or a renamed hole"
    elif jgc_hits:
        status = "SPEC_ONLY"
        reason = "named Joint Gap-Charge terms; budget is not seated"
    else:
        status = "UNSCORED"
        reason = "not a recognized DA-NS-2 last line"
    return {
        "text": text,
        "status": status,
        "forbidden_hits": hits,
        "jgc_hits": jgc_hits,
        "da_ns_2": "OPEN",
        "reason": reason,
    }


def package() -> dict:
    note = note_triad_snapshot()
    one = record(single_shell_field())
    two = record(two_shell_field())
    return {
        "object": "DA-NS-2",
        "claim": "sup_n int_0^T K_min,theta^(n) dt <= F(nu, T, u0) < infinity",
        "K_min": "[T_c - theta nu D_s]_+ / Y",
        "status": "OPEN",
        "identity": "EXACT",
        "integral_bound": "OPEN",
        "jgc_epoch_budget": "NOT_SEATED",
        "ns_solved": False,
        "lemma_star_proved": False,
        "do_not_put_K_in_the_PDE": True,
        "cousin": {
            "DA-NS-1": "T_c <= theta nu D_s + K(t) X",
            "DA-NS-2": "T_c <= theta nu D_s + K_Y(t) Y",
            "tautological_relation": "K_X = Lambda K_min",
        },
        "note_triad": note,
        "single_shell": {
            "D_s": one["D_s"],
            "T_c": one["T_c"],
            "vacuous": abs(one["D_s"]) < 1e-12 and abs(one["T_c"]) < 1e-12,
        },
        "two_shell_D_s_positive": two["D_s"] > 0.0,
        "amplitude_kill": amplitude_occupation(near_scale_triad(1.0)),
        "near_shell": near_shell_occupation(),
        "phase_twin": phase_twin_occupation(),
        "inherited_kills": {
            "charge_only_net_coercivity": "KILLED",
            "frozen_log_charge_theta_lt_1": "KILLED",
            "automatic_dephasing": "KILLED",
            "one_channel_ODE_as_vector_NS": "KILLED",
            "source": "Sprint 01 / PR #142; not re-swept as a close",
        },
        "forbidden_last_lines": list(FORBIDDEN_LAST_LINES),
        "last_line_examples": [
            classify_last_line("int D_s/Y"),
            classify_last_line("sup Lambda"),
            classify_last_line(
                "Joint Gap-Charge Epoch Budget: charge, radial covariance, "
                "moving-barycenter error, homochiral drift, cross-band flux, "
                "phase/far terms, one-use dissipation, summable resets"
            ),
        ],
        "next_write": "Joint Gap-Charge Epoch Budget, cutoff-uniform, theta<1 directly",
    }


def main() -> None:
    payload = package()
    OUT_DEFAULT.parent.mkdir(parents=True, exist_ok=True)
    OUT_DEFAULT.write_text(json.dumps(payload, indent=2, default=float) + "\n", encoding="utf-8")
    note = payload["note_triad"]
    print("DA-NS-2")
    print(f"  claim: {payload['claim']}")
    print(f"  status: {payload['status']}")
    print(f"  note triad T_c = {note['T_c']:.12f}  (locked 16/5)")
    print(f"  note triad Y   = {note['Y']:.12f}  (locked 14)")
    print(f"  K_min(theta=0) = {note['K_min_nu1']['theta_0']:.12f}")
    print(f"  tautology residual = {note['tautology']['residual']:.3e}")
    print(f"  (log Lambda)' <= 2 K_min : {note['log_bound']['log_Lambda_prime_le_2_K_min']}")
    print(f"  ns_solved: {payload['ns_solved']}")
    print(f"  wrote {OUT_DEFAULT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
