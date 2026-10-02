"""Three-gate audit for a ||u||_3 budget. Not a close.

Gate 1 — derivation: cutoff-uniform, constants, no hidden higher norm.
Gate 2 — regularity value: Serrin index 2/p+3/q vs ESS L^∞_t L^3.
Gate 3 — novelty: algebraic reduction to energy / H_{1/2} / a known criterion.

The ||u||_3 derivation is not on this desk.
PRESS 'sharp L3' is Φ_e ≤ W_{λ_e}, not ||u||_3.
Do not invent the inequality.
Do not start leftover 1.
Do not weld ★.
Do not run Taylor–Green.

Does not overwrite stokes_moments.py.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "u3_audit.json"


def serrin_index(p: float | None, q: float) -> float | None:
    """2/p + 3/q. p=None means p=∞."""
    time_part = 0.0 if p is None else 2.0 / p
    return time_part + 3.0 / q


def record() -> dict:
    energy_l4_l3 = serrin_index(4.0, 3.0)
    energy_l2_l6 = serrin_index(2.0, 6.0)
    serrin_l4_l6 = serrin_index(4.0, 6.0)
    ess = serrin_index(None, 3.0)
    finite_p_l3 = {p: serrin_index(float(p), 3.0) for p in (2, 3, 4, 8, 16)}

    energy_owned = abs(energy_l4_l3 - 1.5) < 1e-12
    ess_on_line = abs(ess - 1.0) < 1e-12
    l2_l6_is_floor = abs(energy_l2_l6 - 1.5) < 1e-12
    l4_l6_is_serrin = abs(serrin_l4_l6 - 1.0) < 1e-12
    finite_p_above = all(v > 1.0 + 1e-12 for v in finite_p_l3.values())

    # One-way Sobolev on R^3 / torus: Ḣ^{1/2} ↪ L^3. Converse false.
    h12_embeds_l3 = True
    l3_embeds_h12 = False

    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "derivation_not_on_desk": True,
        "press_L3_is_not_u3": True,
        "gates": {
            "derivation": "cutoff-uniform, constants, no hidden higher norm. Not written.",
            "regularity_value": "Serrin 2/p+3/q≤1, q>3; ESS is L^∞_t L^3. Implication chain, not just algebra.",
            "novelty": "exact inequality or algebraic reduction to energy / H_{1/2} / a known criterion.",
        },
        "serrin_line": "2/p + 3/q = 1, q>3",
        "ess": "L^∞_t L^3_x. Escauriaza–Seregin–Šverák, Uspekhi 2003. Criterion, not an a priori.",
        "energy_L4_L3_index": energy_l4_l3,
        "energy_L2_L6_index": energy_l2_l6,
        "serrin_L4_L6_index": serrin_l4_l6,
        "ess_index": ess,
        "finite_p_L3_index": finite_p_l3,
        "energy_L4_L3_owned_by_energy": energy_owned,
        "energy_L4_L3_is_not_Serrin": energy_owned and energy_l4_l3 > 1.0,
        "ess_is_the_only_Serrin_L3": ess_on_line and finite_p_above,
        "L2_L6_is_energy_floor": l2_l6_is_floor,
        "L4_L6_is_Serrin": l4_l6_is_serrin,
        "finite_p_L3_is_supercritical": finite_p_above,
        "H12_embeds_L3": h12_embeds_l3,
        "L3_embeds_H12": l3_embeds_h12,
        "SBP_charge_is_H12_flux": True,
        "u3_is_not_automatically_H12": True,
        "interesting_outcome": (
            "cutoff-uniform NSE budget on the growth-capable portion of L^3 "
            "without first assuming a Serrin/ESS quantity is finite"
        ),
        "reformulation_if_implies_Serrin_or_ESS": True,
        "literature": {
            "Prodi_1959": "criterion",
            "Serrin_ARMA_1962": "criterion",
            "Ladyzhenskaya": "criterion / uniqueness in Serrin class",
            "ESS_2003": "L^∞_t L^3 criterion. Not an a priori on X.",
            "Tao_2019": "quantitative ESS. Still assumes the L^3 bound.",
            "energy_L4_L3": "Ladyzhenskaya interpolation from L^∞_t L^2 and L^2_t L^6. Owned.",
            "exact_u3_budget_from_NSE": "not found as an a priori on this desk or as a seated theorem",
        },
        "when_derivation_returns": "score implication chain, not only algebra",
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
        "g4_stays_open": True,
        "do_not_invent_a_bridge": True,
        "do_not_run_taylor_green": True,
        "do_not_glue_to_leftover_1": True,
        "do_not_invent_the_u3_inequality": True,
    }
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
