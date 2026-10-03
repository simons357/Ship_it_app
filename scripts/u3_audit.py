"""Three-gate audit for the ||u||_3 budget. Not a close.

Gate 1 — derivation: (D1)-(D3) cutoff-uniform; (D4) while smooth; pressure unpaid.
Gate 2 — regularity value: Serrin index 2/p+3/q vs ESS L^∞_t L^3.
Gate 3 — novelty: (D1) Ladyzhenskaya; (D2) Sobolev+CS; (D4) standard L^p identity.

Derivation: docs/U3-DERIV.md.
PRESS 'sharp L3' is Φ_e ≤ W_{λ_e}, not ||u||_3.
Do not invent a new mechanism.
Do not start leftover 1.
Do not weld ★.
Do not run Taylor–Green.

Does not overwrite stokes_moments.py.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "u3_audit.json"


def serrin_index(p: float | None, q: float) -> float | None:
    """2/p + 3/q. p=None means p=∞."""
    time_part = 0.0 if p is None else 2.0 / p
    return time_part + 3.0 / q


def interpolation_L4_bound(E0: float, nu: float, C_S: float) -> float:
    """∫ ||u||_3^4 ≤ C_S² E(0)² / (2ν)."""
    return (C_S * C_S * E0 * E0) / (2.0 * nu)


def h12_cs(E: float, X: float) -> float:
    """H_{1/2} ≤ √(E X)."""
    return math.sqrt(E * X)


def split_pieces(E: float, X: float, kappa: float, C_B: float, C_star: float) -> dict:
    """Bernstein low and Sobolev high at a frozen cutoff."""
    low = C_B * math.sqrt(kappa) * math.sqrt(E)
    high = C_star * math.sqrt(X) / math.sqrt(kappa)
    return {"low": low, "high": high, "sum": low + high}


def optimized_split(E: float, X: float, C_B: float, C_star: float) -> dict:
    """κ² = X/E = Λ recovers interpolation scaling."""
    lam = X / E
    kappa = math.sqrt(lam)
    pieces = split_pieces(E, X, kappa, C_B, C_star)
    scale = (E**0.25) * (X**0.25)
    return {
        "kappa": kappa,
        "Lambda": lam,
        "low": pieces["low"],
        "high": pieces["high"],
        "scale": scale,
        "low_over_scale": pieces["low"] / scale,
        "high_over_scale": pieces["high"] / scale,
    }


def record() -> dict:
    energy_l4_l3 = serrin_index(4.0, 3.0)
    energy_l2_l6 = serrin_index(2.0, 6.0)
    serrin_l4_l6 = serrin_index(4.0, 6.0)
    ess = serrin_index(None, 3.0)
    high_l2_l3 = serrin_index(2.0, 3.0)
    finite_p_l3 = {p: serrin_index(float(p), 3.0) for p in (2, 3, 4, 8, 16)}

    energy_owned = abs(energy_l4_l3 - 1.5) < 1e-12
    ess_on_line = abs(ess - 1.0) < 1e-12
    l2_l6_is_floor = abs(energy_l2_l6 - 1.5) < 1e-12
    l4_l6_is_serrin = abs(serrin_l4_l6 - 1.0) < 1e-12
    high_l2_above = high_l2_l3 is not None and high_l2_l3 > 1.0 + 1e-12
    finite_p_above = all(v > 1.0 + 1e-12 for v in finite_p_l3.values())

    h12_embeds_l3 = True
    l3_embeds_h12 = False

    opt = optimized_split(4.0, 16.0, 1.0, 1.0)
    opt_recovers = (
        abs(opt["low_over_scale"] - 1.0) < 1e-12
        and abs(opt["high_over_scale"] - 1.0) < 1e-12
    )
    cs_single_shell = abs(h12_cs(2.0, 8.0) - math.sqrt(16.0)) < 1e-12
    l4_bound_ok = abs(interpolation_L4_bound(2.0, 0.5, 1.0) - 4.0) < 1e-12

    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "derivation_on_desk": True,
        "derivation_page": "docs/U3-DERIV.md",
        "owned_interpolation_sits": True,
        "d1_d2_d3_retained_at_stated_scope": True,
        "subject_to_source_constant_domain_check": True,
        "correction_from_screenshots_not_fresh_verification": True,
        "nse_L3_identity_while_smooth": True,
        "nse_L3_closed_cutoff_uniform": False,
        "pressure_remainder_paid": False,
        "d4_is_unresolved_pressure": True,
        "d5_remainder_must_be_cutoff_uniform": True,
        "d5_does_not_prove_every_estimate_needs_higher_norm": True,
        "L4_L3_stays_outside_Serrin": True,
        "int_X2_supplies_L4_L6_not_L4_L3": True,
        "L3_direction_not_proved_impossible": True,
        "no_budget_derived_in_this_audit": True,
        "no_new_mechanism_is_a_search_result": True,
        "galerkin_commutator_sits_as_obstruction": True,
        "press_L3_is_not_u3": True,
        "gates": {
            "derivation": (
                "(D1)-(D3) cutoff-uniform, named constants, no hidden higher norm. "
                "(D4) identity while smooth. Closed Galerkin pressure payment does not sit."
            ),
            "regularity_value": (
                "Owned L^4_t L^3 index 3/2 is not Serrin. "
                "int X^2 with energy and Sobolev supplies L^4_t L^6, index 1. "
                "Not beyond ESS."
            ),
            "novelty": (
                "(D1) Ladyzhenskaya interpolation. (D2) Sobolev+CS / Λ-weighted H_{1/2}. "
                "(D4) standard L^p identity, closed for p>3, not p=3."
            ),
        },
        "serrin_line": "2/p + 3/q = 1, q>3",
        "ess": "L^∞_t L^3_x. Escauriaza–Seregin–Šverák, Uspekhi 2003. Criterion, not an a priori.",
        "energy_L4_L3_index": energy_l4_l3,
        "energy_L2_L6_index": energy_l2_l6,
        "serrin_L4_L6_index": serrin_l4_l6,
        "ess_index": ess,
        "high_piece_L2_L3_index": high_l2_l3,
        "finite_p_L3_index": finite_p_l3,
        "energy_L4_L3_owned_by_energy": energy_owned,
        "energy_L4_L3_is_not_Serrin": energy_owned and energy_l4_l3 > 1.0,
        "ess_is_the_only_Serrin_L3": ess_on_line and finite_p_above,
        "L2_L6_is_energy_floor": l2_l6_is_floor,
        "L4_L6_is_Serrin": l4_l6_is_serrin,
        "finite_p_L3_is_supercritical": finite_p_above,
        "high_piece_L2_L3_is_supercritical": high_l2_above,
        "H12_embeds_L3": h12_embeds_l3,
        "L3_embeds_H12": l3_embeds_h12,
        "SBP_charge_is_H12_flux": True,
        "u3_is_not_automatically_H12": True,
        "D2cs_is_energy_interpolation": True,
        "optimized_split_recovers_interpolation": opt_recovers,
        "cs_sharp_on_single_shell": cs_single_shell,
        "L4_bound_formula_ok": l4_bound_ok,
        "optimized_split_sample": opt,
        "interesting_outcome": (
            "cutoff-uniform NSE budget on the growth-capable portion of L^3 "
            "without first assuming a Serrin/ESS quantity is finite"
        ),
        "interesting_outcome_sits": False,
        "int_X2_gives_Serrin_via_L4_L6": True,
        "reformulation_if_implies_Serrin_or_ESS": True,
        "literature": {
            "Prodi_1959": "criterion",
            "Serrin_ARMA_1962": "criterion",
            "Ladyzhenskaya": "interpolation / uniqueness in Serrin class. (D1).",
            "ESS_2003": "L^∞_t L^3 criterion. Not an a priori on X.",
            "Tao_2019": "quantitative ESS. Still assumes the L^3 bound.",
            "Giga_1986": "local L^p, p>3.",
            "Robinson_Sadowski_Silva_2014": "L^p identity closes for p>3, not p=3.",
            "energy_L4_L3": "Ladyzhenskaya interpolation from L^∞_t L^2 and L^2_t L^6. Owned.",
            "exact_u3_budget_from_NSE_beyond_D1_D2": "not found as an a priori",
        },
        "implication_chain": "I1-I7 on docs/U3-DERIV.md. Attack that, not only algebra.",
        "lemma_A_unaltered": True,
        "lemma_B_open": True,
        "sign_gate_unaltered": True,
        "no_more_potentials": True,
        "da_ns2_is_not_a_theorem": True,
        "sits_as_useful_K": False,
        "sits_as_g4_death": False,
        "sits_as_da_ns2": False,
        "sits_as_jgc": False,
        "sits_as_bprim": False,
        "sits_as_ess_a_priori": False,
        "sits_as_beyond_ess": False,
        "sits_as_new_mechanism": False,
        "g4_stays_open": True,
        "do_not_invent_a_bridge": True,
        "do_not_run_taylor_green": True,
        "do_not_glue_to_leftover_1": True,
        "do_not_invent_a_new_mechanism": True,
    }
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
