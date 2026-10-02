"""Arithmetic sign-realizability gate: exact delta split and R_2 remainder protocol.

Does not alter the SBP / phi-d / low-tail gates.
Does not invent Heavy's neighboring-shell family or B_prim.
Does not silently substitute live T_m for T^{(0)} in the first-variation object.

Exact identity (any field), with delta_k = lambda_k - Lambda:

    T_c = Lambda <delta, T> + sum_k delta_k^2 T_k.

First-variation object, T^{(0)} supplied separately:

    L_{1,N} = Lambda_N <delta_N, T_N^{(0)}>
    R_{2,N} = T_{c,N} - L_{1,N}

Silent substitution T^{(0)} := T_live recovers only the exact quadratic
remainder sum delta^2 T, which is not the first-variation check.

Outcome tree is ARMED, not executed: neighboring-shell family is not
on this tree. NS is not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import centered_drift_triad_test as cdt  # noqa: E402
import growing_layer_counterexample as gl  # noqa: E402
import ns_lemma_star_core as core  # noqa: E402


def modal_rows(field: core.Field) -> tuple[list[dict], dict]:
    E, X, Y, Z, Lam = core.moments(field)
    rows = []
    Tc = 0.0
    N = 0.0
    sum_T = 0.0
    for k, vk in field.modes.items():
        e = float(np.vdot(vk, vk).real)
        ell = core.lam(k)
        Bk = core.B_hat_at(field, k)
        Tk = -float(np.real(np.dot(Bk, np.conj(vk))))
        delta = ell - Lam
        Tc += ell * delta * Tk
        N += ell * Tk
        sum_T += Tk
        rows.append(
            {
                "k": [int(x) for x in k],
                "lam": ell,
                "e": e,
                "T": Tk,
                "delta": delta,
            }
        )
    return rows, {
        "E": E,
        "X": X,
        "Y": Y,
        "Z": Z,
        "Lambda": Lam,
        "T_c": Tc,
        "N": N,
        "sum_T": sum_T,
    }


def inner_delta_T(rows: list[dict], T_override: list[float] | None = None) -> float:
    total = 0.0
    for i, r in enumerate(rows):
        Tk = r["T"] if T_override is None else T_override[i]
        total += r["delta"] * Tk
    return total


def sum_delta_sq_T(rows: list[dict], T_override: list[float] | None = None) -> float:
    total = 0.0
    for i, r in enumerate(rows):
        Tk = r["T"] if T_override is None else T_override[i]
        total += (r["delta"] ** 2) * Tk
    return total


def L1(Lam: float, rows: list[dict], T0: list[float]) -> float:
    """First-variation object. T0 is required. Do not pass live T silently."""
    if len(T0) != len(rows):
        raise ValueError("T^{(0)} must be aligned with the neighboring-state modes")
    return Lam * inner_delta_T(rows, T0)


def R2(Tc: float, Lam: float, rows: list[dict], T0: list[float]) -> float:
    return Tc - L1(Lam, rows, T0)


def exact_split(field: core.Field) -> dict:
    rows, mom = modal_rows(field)
    Lam = mom["Lambda"]
    inner = inner_delta_T(rows)
    quad = sum_delta_sq_T(rows)
    recon = Lam * inner + quad
    Tc = mom["T_c"]
    return {
        "Lambda": Lam,
        "T_c": Tc,
        "inner_delta_T_live": inner,
        "sum_delta_sq_T_live": quad,
        "reconstructed": recon,
        "identity_ok": abs(Tc - recon) <= 1e-10 * max(1.0, abs(Tc)),
        "silent_R2_equals_quadratic": abs((Tc - Lam * inner) - quad)
        <= 1e-10 * max(1.0, abs(quad), abs(Tc)),
        "n_modes": len(rows),
    }


def seed_schema() -> dict:
    """Canonical A_N^+ payload if BOTH SIGNS appears. Empty until then."""
    return {
        "name": "A_N^+",
        "required": [
            "integer_wavevectors",
            "helicity_labels",
            "polarizations",
            "amplitudes",
            "delta",
            "T_live",
            "T_0",
            "Lambda",
            "T_c",
            "L_1",
            "R_2",
            "rho_plus",
            "rho_minus",
        ],
        "saved": False,
        "reason": "BOTH SIGNS not obtained; neighboring-shell family not on this tree",
    }


def run() -> dict:
    note = exact_split(cdt.near_scale_triad())
    sep = exact_split(cdt.separated_triad(8))
    vn = exact_split(gl.growing_layer(4))
    # Notation trap: L1 with live T is not the first-variation object.
    rows, mom = modal_rows(cdt.near_scale_triad())
    T_live = [r["T"] for r in rows]
    T_zero = [0.0 for _ in rows]
    trap = {
        "L1_with_live_T": L1(mom["Lambda"], rows, T_live),
        "R2_with_live_T": R2(mom["T_c"], mom["Lambda"], rows, T_live),
        "quadratic_live": sum_delta_sq_T(rows),
        "L1_with_T0_zero": L1(mom["Lambda"], rows, T_zero),
        "R2_with_T0_zero": R2(mom["T_c"], mom["Lambda"], rows, T_zero),
        "silent_substitution_is_not_first_variation": True,
    }
    trap_ok = abs(trap["R2_with_live_T"] - trap["quadratic_live"]) <= 1e-10 * max(
        1.0, abs(trap["quadratic_live"])
    )
    outcomes = {
        "BOTH_SIGNS": "ARMED_not_run",
        "ZERO_ONLY_homochiral": "ARMED_not_run",
        "ONE_SIGN_heterochiral": "ARMED_not_run",
        "NO_NEIGHBOR": "own_category_not_sign_depletion",
    }
    return {
        "ns_solved": False,
        "gate_altered": {
            "sbp": False,
            "phi_vs_d": False,
            "low_tail_snapshot": False,
        },
        "heavy_neighboring_family_on_this_tree": False,
        "B_prim_constructed": False,
        "both_signs_obtained": False,
        "A_N_plus_saved": False,
        "seed_schema": seed_schema(),
        "exact_split": {
            "note_triad": note,
            "separated_L8": sep,
            "growing_layer_n4": vn,
        },
        "notation_trap": trap,
        "outcomes": outcomes,
        "static_frontier": "arithmetic sign realizability",
        "dynamic_frontier": "dangerous-state persistence",
        "Theta_N": "nu * kappa_N^2 * tau_U,N  (named; not constructed here)",
        "all_identities_ok": note["identity_ok"]
        and sep["identity_ok"]
        and vn["identity_ok"]
        and note["silent_R2_equals_quadratic"]
        and trap_ok,
        "note": (
            "Exact T_c = Lambda <delta,T> + sum delta^2 T sits. "
            "L_1 requires an explicit T^{(0)}; silent live-T substitution "
            "only recovers the quadratic remainder. "
            "Neighboring-shell sign search is not on this tree and is not invented. "
            "NO NEIGHBOR is not sign depletion. NS not solved."
        ),
    }


def main() -> int:
    payload = run()
    out = Path(__file__).resolve().parents[1] / "results" / "da_gate_arithmetic_sign_realizability.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2), flush=True)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
