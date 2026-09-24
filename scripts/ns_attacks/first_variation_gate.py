#!/usr/bin/env python3
"""First-variation neighboring-shell gate. Do not alter Lemma A.

Not DA-NS-2. NS is not solved.

Exact finite-gap: T_c = Λ⟨δ,T⟩ + Σ δ_m² T_m,  δ_m = λ_m − Λ.
First variation uses the reference transfer T^{(0)}:
  L_{1,N} = Λ_N ⟨δ_N, T_N^{(0)}⟩
  R_{2,N} = T_{c,N} − L_{1,N}
Do not silently put T^{(0)} into the full finite-gap identity.
"""

from __future__ import annotations

import argparse
import json
from typing import Sequence

import numpy as np

BOTH_SIGNS = "BOTH_SIGNS"
ZERO_ONLY = "ZERO_ONLY"
ONE_SIGN = "ONE_SIGN"
NO_NEIGHBOR = "NO_NEIGHBOR"
CATEGORIES = (BOTH_SIGNS, ZERO_ONLY, ONE_SIGN, NO_NEIGHBOR)


def deltas(lams: Sequence[float], Lambda: float) -> np.ndarray:
    return np.asarray(lams, dtype=float) - float(Lambda)


def T_c_from_weights(lams: Sequence[float], T: Sequence[float], Lambda: float) -> float:
    """T_c = Σ λ(λ−Λ) T, exact."""
    lam = np.asarray(lams, dtype=float)
    t = np.asarray(T, dtype=float)
    return float(np.dot(lam * (lam - Lambda), t))


def finite_gap_split(lams: Sequence[float], T: Sequence[float], Lambda: float) -> dict:
    """Exact: T_c = Λ⟨δ,T⟩ + Σ δ² T. Live T on both terms."""
    d = deltas(lams, Lambda)
    t = np.asarray(T, dtype=float)
    lin = float(Lambda * np.dot(d, t))
    quad = float(np.dot(d * d, t))
    tc = T_c_from_weights(lams, t, Lambda)
    return {
        "T_c": tc,
        "Lambda_dot_delta_T": lin,
        "delta2_dot_T": quad,
        "sum": lin + quad,
        "abs_err": abs(tc - lin - quad),
    }


def L1_N(Lambda: float, delta: Sequence[float], T0: Sequence[float]) -> float:
    """First-variation linear term: Λ ⟨δ, T^{(0)}⟩."""
    return float(Lambda * np.dot(np.asarray(delta, dtype=float), np.asarray(T0, dtype=float)))


def R2_N(T_c: float, Lambda: float, delta: Sequence[float], T0: Sequence[float]) -> float:
    """Remainder vs the first-variation object, not vs live-T finite-gap."""
    return float(T_c - L1_N(Lambda, delta, T0))


def first_variation_check(
    lams: Sequence[float],
    T: Sequence[float],
    T0: Sequence[float],
    Lambda: float,
) -> dict:
    d = deltas(lams, Lambda)
    tc = T_c_from_weights(lams, T, Lambda)
    exact = finite_gap_split(lams, T, Lambda)
    L1 = L1_N(Lambda, d, T0)
    R2 = tc - L1
    dnorm = float(np.linalg.norm(d))
    return {
        "T_c": tc,
        "L1": L1,
        "R2": R2,
        "exact_live_T": exact,
        "delta_norm": dnorm,
        "R2_over_delta2": (R2 / (dnorm**2)) if dnorm else None,
        "used_T0_in_L1_only": True,
    }


def synthetic_family(eps: float, scramble: bool = False, seed: int = 0) -> dict:
    """Asymptotic neighboring-shell family.

    T = T^{(0)} + eps S. Then R2 = Λ⟨δ, eps S⟩ + ⟨δ², T⟩ = O(eps²)
    if δ = O(eps). Scramble replaces T by an O(1) unrelated field.
    """
    rng = np.random.default_rng(seed)
    T0 = rng.normal(size=6)
    T0 -= T0.mean()
    S = rng.normal(size=6)
    S -= S.mean()
    direction = rng.normal(size=6)
    direction -= direction.mean()
    Lambda = 9.0
    d = eps * direction
    lams = Lambda + d
    if scramble:
        T = rng.normal(size=6)
        T -= T.mean()
    else:
        T = T0 + eps * S
    row = first_variation_check(lams, T, T0, Lambda)
    row["eps"] = eps
    row["scrambled"] = scramble
    return row


def classify_signs(rho_plus: float | None, rho_minus: float | None, c: float, neighbor: bool) -> str:
    """Outcome tree. NO_NEIGHBOR is not sign depletion."""
    if not neighbor:
        return NO_NEIGHBOR
    if rho_plus is None or rho_minus is None:
        return NO_NEIGHBOR
    plus = abs(rho_plus) >= c
    minus = abs(rho_minus) >= c
    if plus and minus:
        return BOTH_SIGNS
    if plus or minus:
        return ONE_SIGN
    return ZERO_ONLY


def seed_A_plus(
    N: int,
    modes: Sequence[tuple],
    helicities: Sequence[int],
    polarizations: Sequence[tuple],
    amplitudes: Sequence[complex],
    delta: Sequence[float],
    T0: Sequence[float],
) -> dict:
    """Canonical adversarial seed. Keep the field, not only δ and T^{(0)}."""
    return {
        "tag": "A_N^+",
        "N": N,
        "modes": [list(m) for m in modes],
        "helicities": list(helicities),
        "polarizations": [list(p) for p in polarizations],
        "amplitudes": [{"re": complex(a).real, "im": complex(a).imag} for a in amplitudes],
        "delta": list(map(float, delta)),
        "T0": list(map(float, T0)),
        "note": "Save the field. Then NSE gets the next move.",
    }


def report() -> dict:
    exact = finite_gap_split([8.0, 9.0, 11.0], [0.4, -0.1, -0.3], 9.0)
    legit = [synthetic_family(eps) for eps in (1e-1, 5e-2, 2.5e-2)]
    bad = synthetic_family(5e-2, scramble=True)
    return {
        "exact_split": exact,
        "legit_R2_over_eps2": [row["R2"] / (row["eps"] ** 2) for row in legit],
        "scrambled": {"R2": bad["R2"], "R2_over_delta2": bad["R2_over_delta2"]},
        "categories": {
            "both": classify_signs(0.4, -0.5, 0.2, True),
            "one": classify_signs(0.4, 0.01, 0.2, True),
            "zero": classify_signs(0.01, -0.01, 0.2, True),
            "none": classify_signs(0.4, -0.5, 0.2, False),
        },
        "verdicts": {
            BOTH_SIGNS: "universal first-order one-sided narrow depletion is false",
            ZERO_ONLY: "Vandermonde delay; does not rescue NSE",
            ONE_SIGN: "Gram/lattice realization; I_3 into centered dynamics",
            NO_NEIGHBOR: "arithmetic rigidity; not sign depletion",
        },
        "locks": {
            "lemma_A_unaltered": True,
            "no_new_potential": True,
            "no_clock_reinterpretation": True,
            "not_DA_NS_2": True,
            "not_a_close": True,
        },
    }


def main(argv=None) -> int:
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    print(json.dumps(report(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
