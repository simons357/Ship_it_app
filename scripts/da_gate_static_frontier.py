#!/usr/bin/env python3
"""DA-GATE static frontier — 24 September 2026.

Arithmetic sign realizability. Frozen board, not a close.

  L_{1,N} = Λ_N ⟨δ_N, T_N^{(0)}⟩
  R_{2,N} := T_{c,N} − Λ_N ⟨δ_N, T_N^{(0)}⟩

The neighboring T_m varies with the deformation. Silently substituting
T^{(0)} into the full finite-gap identity is FORBIDDEN.

Does not alter the 24 Sep RMS/core/tail/SBP gate.
Classical NS stays open. DA-NS-2 stays OPEN.
"""

from __future__ import annotations

import argparse
import json
from typing import Sequence

import numpy as np

OUTCOMES = ("BOTH_SIGNS", "ZERO_ONLY", "ONE_SIGN", "NO_NEIGHBOR")
SEED_REQUIRED = (
    "integer_wavevectors",
    "helicity_labels",
    "polarizations",
    "amplitudes",
)
SEED_NOT_SUFFICIENT = ("delta", "T^{(0)}")


def inner(delta: Sequence[float], transfer: Sequence[float]) -> float:
    d = np.asarray(delta, dtype=float)
    t = np.asarray(transfer, dtype=float)
    if d.shape != t.shape:
        raise ValueError("delta and transfer must have the same shape")
    return float(np.dot(d, t))


def L1_N(lambda_n: float, delta_n: Sequence[float], t0_n: Sequence[float]) -> float:
    """First-variation object. Uses the unperturbed neighboring-shell transfer."""
    return float(lambda_n) * inner(delta_n, t0_n)


def R2_N(
    t_c_n: float,
    lambda_n: float,
    delta_n: Sequence[float],
    t0_n: Sequence[float],
) -> float:
    """Remainder after subtracting the first-variation object from T_{c,N}."""
    return float(t_c_n) - L1_N(lambda_n, delta_n, t0_n)


def finite_gap_remainder_check(
    t_c_n: float,
    lambda_n: float,
    delta_n: Sequence[float],
    t0_n: Sequence[float],
    neighboring_t_m: Sequence[float],
) -> dict:
    """Keep neighboring T_m separate. Refuse a silent T^{(0)} substitution.

    This does not evaluate the finite-gap identity. It only records the
    remainder check and whether the neighboring transfer was retained.
    """
    t0 = np.asarray(t0_n, dtype=float)
    neigh = np.asarray(neighboring_t_m, dtype=float)
    if t0.shape != neigh.shape:
        raise ValueError("T^{(0)} and neighboring T_m must have the same shape")
    substituted = bool(np.allclose(t0, neigh) and t0.size > 0)
    return {
        "L_1_N": L1_N(lambda_n, delta_n, t0_n),
        "R_2_N": R2_N(t_c_n, lambda_n, delta_n, t0_n),
        "neighboring_T_retained": True,
        "silent_T0_substitution": substituted,
        "forbidden_if_used_as_finite_gap_T": substituted,
        "note": (
            "Retain neighboring T_m as a remainder check. "
            "Do not substitute T^{(0)} into the full finite-gap identity. "
            "Predicted higher-order behaviour of R_{2,N} is not invented here."
        ),
    }


def classify_outcome(
    *,
    has_neighbor: bool,
    family: str,
    signs: Sequence[str] | None = None,
    rho_abs_min: float | None = None,
    c: float = 0.0,
) -> dict:
    """Locked outcome tree. Does not search. Does not invent a family."""
    if not has_neighbor:
        return {
            "outcome": "NO_NEIGHBOR",
            "own_category": True,
            "arithmetic_rigidity_is_not_sign_depletion": True,
            "stop_static_closure": False,
        }
    fam = family.strip().lower()
    sign_set = {s.upper() for s in (signs or ())}
    if fam == "homochiral" and sign_set == {"ZERO"}:
        return {
            "outcome": "ZERO_ONLY",
            "family": "homochiral",
            "verdict": "consistent with Vandermonde delay",
            "does_not_rescue_NSE": True,
            "stop_static_closure": False,
        }
    if fam == "heterochiral" and sign_set == {"PLUS", "MINUS"}:
        persistent = rho_abs_min is not None and rho_abs_min >= c > 0.0
        return {
            "outcome": "BOTH_SIGNS",
            "family": "heterochiral",
            "criterion_held": persistent,
            "verdict": (
                "universal first-order one-sided narrow depletion is false"
                if persistent
                else "BOTH SIGNS seen but |rho_N^pm| threshold not met"
            ),
            "stop_static_closure": persistent,
            "next": "positive branch to evolution; keep Theta_N" if persistent else None,
            "save_adversarial_seed": persistent,
        }
    if fam == "heterochiral" and sign_set in ({"PLUS"}, {"MINUS"}):
        return {
            "outcome": "ONE_SIGN",
            "family": "heterochiral",
            "next": "determine whether the restriction is Gram/lattice realization",
            "I_3_bridge": "prospective; not seated here",
            "stop_static_closure": False,
        }
    raise ValueError(
        "unclassified: need NO NEIGHBOR, homochiral ZERO ONLY, "
        "or heterochiral BOTH SIGNS / ONE SIGN"
    )


def seed_is_canonical(seed: dict) -> bool:
    return all(field in seed and seed[field] not in (None, [], {}) for field in SEED_REQUIRED)


def lock_payload() -> dict:
    return {
        "frontiers": {
            "static": "arithmetic sign realizability",
            "dynamic": "dangerous-state persistence",
        },
        "L_1_N": "Lambda_N <delta_N, T_N^{(0)}>",
        "R_2_N": "T_{c,N} - Lambda_N <delta_N, T_N^{(0)}>",
        "outcomes": list(OUTCOMES),
        "forbidden_silent_T0_substitution": True,
        "adversarial_seed": {
            "name": "A_N^+",
            "required": list(SEED_REQUIRED),
            "not_sufficient": list(SEED_NOT_SUFFICIENT),
        },
        "no_more_potentials": True,
        "sbp_gate_unaltered": True,
        "I_3_seated_here": False,
        "ns_solved": False,
        "da_ns_2": "OPEN",
        "sign_realizability_search": "OPEN",
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Static frontier lock")
    p.add_argument(
        "--out",
        default=None,
        help="optional JSON path; prints to stdout if omitted",
    )
    args = p.parse_args()
    payload = lock_payload()
    text = json.dumps(payload, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
