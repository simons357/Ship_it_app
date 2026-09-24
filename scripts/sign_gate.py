"""Score the first-variation sign gate. Not a close.

Exact, from T_c = Σ λ(λ-Λ)T:
    T_c = Λ⟨δ,T⟩ + Σ δ_m² T_m,  δ_m = λ_m - Λ.

The first-variation object (do not alter) is
    L_{1,N} = Λ_N ⟨δ_N, T_N^{(0)}⟩
on an asymptotic neighboring-shell family.
Do not substitute T^{(0)} into the finite-gap identity.

Remainder check:
    R_{2,N} = T_{c,N} - Λ_N ⟨δ_N, T_N^{(0)}⟩.
Legitimate first variation: R_2 is higher order in the gap.
A hard deformation of T is not the intended gate.

Outcome tree is named. No Heavy print sits here.
BOTH SIGNS / ONE SIGN / ZERO ONLY / NO NEIGHBOR are categories.
Do not invent a family. Do not invent a bridge.
Do not invent A_N^+. Save the seed only if Heavy prints BOTH SIGNS.

Does not overwrite stokes_moments.py.
Does not restore ★.
Does not seat DA-NS-2 or Lemma B.
Does not start leftover 1.
Does not run Taylor–Green.
Does not mix Heavy scalene loops.
Does not alter Lemma A.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from centered_ledger import two_shell_moments  # noqa: E402

OUT = ROOT / "results" / "sign_gate.json"


def two_shell_transfer(alpha: float, beta: float, e_a: float, e_b: float, t_alpha: float) -> dict:
    """Exact two-shell expansion. T_β = -T_α."""
    m = two_shell_moments(alpha, beta, e_a, e_b)
    t_beta = -t_alpha
    d_a = alpha - m["Lambda"]
    d_b = beta - m["Lambda"]
    inner = d_a * t_alpha + d_b * t_beta
    quad = (d_a**2) * t_alpha + (d_b**2) * t_beta
    t_c = m["Lambda"] * inner + quad
    t_c_gap = (alpha - beta) * (alpha + beta - m["Lambda"]) * t_alpha
    return {
        **m,
        "alpha": alpha,
        "beta": beta,
        "T_alpha": t_alpha,
        "T_beta": t_beta,
        "delta_a": d_a,
        "delta_b": d_b,
        "inner": inner,
        "quad": quad,
        "T_c": t_c,
        "T_c_gap": t_c_gap,
        "expansion_ok": abs(t_c - t_c_gap) < 1e-9 * max(1.0, abs(t_c_gap)),
    }


def first_variation(row: dict, t0_alpha: float) -> dict:
    """L_1 uses frozen T^{(0)}; R_2 is T_c minus that."""
    t0_beta = -t0_alpha
    inner0 = row["delta_a"] * t0_alpha + row["delta_b"] * t0_beta
    l1 = row["Lambda"] * inner0
    r2 = row["T_c"] - l1
    gap = abs(row["alpha"] - row["beta"])
    return {
        "L1": l1,
        "R2": r2,
        "gap": gap,
        "R2_over_gap": r2 / gap if gap else None,
        "R2_over_gap2": r2 / (gap * gap) if gap else None,
        "T0_alpha": t0_alpha,
    }


def record() -> dict:
    # Finite-gap exact expansion.
    base = two_shell_transfer(4.0, 9.0, 1.0, 1.0, 2.0)
    frozen = first_variation(base, base["T_alpha"])
    # Frozen T^{(0)}=T makes R_2 exactly the quadratic piece.
    frozen_is_quad = abs(frozen["R2"] - base["quad"]) < 1e-12

    # Shrinking-gap family, T held at T^{(0)}.
    t0 = 2.0
    shrink = []
    shrink_ok = True
    for eta in (1.0, 0.5, 0.25, 0.125, 0.0625):
        row = two_shell_transfer(4.0, 4.0 + eta, 1.0, 1.0, t0)
        fv = first_variation(row, t0)
        shrink.append({"eta": eta, **{k: fv[k] for k in ("L1", "R2", "R2_over_gap2")}})
        shrink_ok = shrink_ok and abs(fv["R2_over_gap2"]) < 10.0

    # Hard amplitude deformation: T = T^{(0)} + O(1), not O(η).
    hard = []
    hard_not_higher_order = True
    t0_hard = 2.0
    d = 1.5
    for eta in (0.5, 0.25, 0.125):
        row = two_shell_transfer(4.0, 4.0 + eta, 1.0, 1.0, t0_hard + d)
        fv = first_variation(row, t0_hard)
        hard.append({"eta": eta, "R2_over_gap": fv["R2_over_gap"], "R2_over_gap2": fv["R2_over_gap2"]})
        # O(η) remainder ⇒ |R2|/η stays order-one, |R2|/η² grows.
        if fv["R2_over_gap2"] is not None:
            hard_not_higher_order = hard_not_higher_order and abs(fv["R2_over_gap2"]) > 10.0

    # Soft deformation d = O(η) stays higher order.
    soft = []
    soft_ok = True
    for eta in (0.5, 0.25, 0.125):
        row = two_shell_transfer(4.0, 4.0 + eta, 1.0, 1.0, t0_hard + 0.4 * eta)
        fv = first_variation(row, t0_hard)
        soft.append({"eta": eta, "R2_over_gap2": fv["R2_over_gap2"]})
        soft_ok = soft_ok and abs(fv["R2_over_gap2"]) < 10.0

    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "gate_unaltered": True,
        "identities": {
            "expansion": "T_c = Λ⟨δ,T⟩ + Σ δ_m² T_m,  δ_m=λ_m-Λ",
            "L1": "L_{1,N}=Λ_N ⟨δ_N, T_N^{(0)}⟩",
            "R2": "R_{2,N}=T_{c,N}-Λ_N ⟨δ_N, T_N^{(0)}⟩",
        },
        "expansion_ok": base["expansion_ok"],
        "frozen_R2_is_quadratic": frozen_is_quad,
        "shrink": shrink,
        "shrink_higher_order": shrink_ok,
        "hard": hard,
        "hard_deformation_not_higher_order": hard_not_higher_order,
        "soft": soft,
        "soft_deformation_higher_order": soft_ok,
        "do_not_sub_T0_into_finite_gap": True,
        "retain_neighbor_T_as_remainder": True,
        "outcomes": {
            "BOTH_SIGNS": "OPEN. Would kill universal first-order one-sided narrow depletion. Not printed.",
            "ZERO_ONLY_HOMO": "OPEN. Vandermonde delay. Does not rescue heterochiral NSE.",
            "ONE_SIGN_HET": "OPEN. Gram/lattice question. Not a seated I_3 bridge.",
            "NO_NEIGHBOR": "OPEN. Arithmetic rigidity. Not sign depletion.",
        },
        "both_signs_not_printed": True,
        "one_sign_not_printed": True,
        "zero_only_not_printed": True,
        "no_neighbor_not_printed": True,
        "no_sign_verdict": True,
        "universal_depletion_not_killed": True,
        "universal_depletion_not_proved": True,
        "A_N_plus_not_invented": True,
        "seed_schema": [
            "integer wavevectors",
            "helicity labels",
            "polarizations",
            "amplitudes",
        ],
        "Theta_N_named_not_computed": True,
        "Theta_N": "ν κ_N² τ_{U,N}",
        "static_frontier": "arithmetic sign realizability",
        "dynamic_frontier": "dangerous-state persistence",
        "no_more_potentials": True,
        "no_clock_reinterpretation": True,
        "lemma_A_unaltered": True,
        "lemma_B_open": True,
        "i3_bridge_not_seated": True,
        "vandermonde_not_locked_as_remainder": True,
        "flux_normalization_not_reproduced": True,
        "da_ns2_is_not_a_theorem": True,
        "sits_as_useful_K": False,
        "sits_as_g4_death": False,
        "sits_as_da_ns2": False,
        "sits_as_jgc": False,
        "sits_as_bprim": False,
        "g4_stays_open": True,
        "do_not_invent_a_bridge": True,
        "do_not_run_taylor_green": True,
        "do_not_mix_heavy": True,
        "do_not_glue_to_leftover_1": True,
        "do_not_run_heavy_search": True,
        "base_sample": {
            "Lambda": base["Lambda"],
            "T_c": base["T_c"],
            "quad": base["quad"],
            "L1": frozen["L1"],
            "R2": frozen["R2"],
        },
    }
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
