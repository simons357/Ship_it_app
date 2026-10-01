#!/usr/bin/env python3
"""α₊ depletion ⇒ (A): light analytic probes (C10 through C6 hinge).

Does NOT revive C1–C5. No BKM shortcut. No ė_j/Ż/Λ' recycling.
No Clay claim. NS is NOT solved.

Pressure this pass:
  - CZ–Sobolev integrable substitute vs νD (λ^{1/2} escape)
  - cubic Young remainder Z^3/D
  - confirm αZ/(νP) kill still live
  - axisym-compatible concentration powers (same ledger)
  - forbidden-slot refuse checklist
  - conditional [α_θ] packaging (does not prove the hypothesis)
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path("/opt/cursor/artifacts/alpha-plus-depletion")
REPO_OUT = ROOT / "results" / "alpha-plus-depletion"
OUT.mkdir(parents=True, exist_ok=True)
REPO_OUT.mkdir(parents=True, exist_ok=True)

FORBIDDEN = (r"\dot e_j", r"\dot Z", r"\dot Z_j", r"\Lambda'")


def concentration_ledger(lambdas: np.ndarray) -> dict:
    """u^λ = λ^{3/2} φ(λx) prototype powers (also for axisym φ)."""
    E = np.ones_like(lambdas)
    Z = lambdas**2
    D = lambdas**4
    P = lambdas**4
    alpha = lambdas**2.5
    T = lambdas**4.5
    return {
        "lambdas": lambdas.tolist(),
        "E": E.tolist(),
        "Z": Z.tolist(),
        "D": D.tolist(),
        "P": P.tolist(),
        "alpha": alpha.tolist(),
        "T": T.tolist(),
        "alpha_Z": (alpha * Z).tolist(),
        "Z_pow_34_D_pow_34": ((Z**0.75) * (D**0.75)).tolist(),
        "Z_cubed": (Z**3).tolist(),
    }


def probe_absolute_sobolev_vs_P() -> dict:
    lambdas = np.array([4.0, 16.0, 64.0, 256.0, 1024.0])
    L = concentration_ledger(lambdas)
    nu = 1.0
    alpha_Z = np.array(L["alpha_Z"])
    P = np.array(L["P"])
    ratio = alpha_Z / (nu * P)  # ~ λ^{1/2}
    return {
        "name": "sobolev_alpha_Z_vs_nu_P",
        "verdict": "KILLED",
        "note": "Absolute Sobolev α₊Z ≤ θνP + … still escapes (λ^{1/2}). Not revived.",
        "ratio": ratio.tolist(),
        "growth": float(ratio[-1] / ratio[0]),
        "expected_growth": float((1024.0 / 4.0) ** 0.5),
    }


def probe_cz_integrable_substitute() -> dict:
    """∫(α)_+|ω|² ≲ Z^{3/4} D^{3/4} ≤ εD + C_ε Z^3."""
    lambdas = np.array([4.0, 16.0, 64.0, 256.0, 1024.0])
    L = concentration_ledger(lambdas)
    nu = 1.0
    cz = np.array(L["Z_pow_34_D_pow_34"])
    D = np.array(L["D"])
    Z3 = np.array(L["Z_cubed"])
    vs_D = cz / (nu * D)  # ~ λ^{1/2}
    cubic_over_D = Z3 / D  # ~ λ^2
    return {
        "name": "cz_sobolev_integrable_substitute",
        "verdict": "KILLED_AS_ABSOLUTE",
        "survives_as": "STANDARD_sketch_plus_cubic_wall",
        "note": (
            "Avoids ||α₊||_∞ for the main stretch, but Z^{3/4}D^{3/4}/(νD)~λ^{1/2} "
            "and Young remainder Z^3/D~λ^2 → ∞. Classical enstrophy cubic wall; "
            "not allowed R for closing (A)."
        ),
        "cz_over_nu_D": vs_D.tolist(),
        "cz_over_nu_D_growth": float(vs_D[-1] / vs_D[0]),
        "Z3_over_D": cubic_over_D.tolist(),
        "Z3_over_D_growth": float(cubic_over_D[-1] / cubic_over_D[0]),
        "same_escape_as_alpha_Z_over_P": True,
    }


def probe_axisym_compatible_scaling() -> dict:
    """Axisym test function with same concentration powers — ledger unchanged."""
    lambdas = np.array([4.0, 16.0, 64.0, 256.0, 1024.0])
    L = concentration_ledger(lambdas)
    nu = 1.0
    alpha_Z = np.array(L["alpha_Z"])
    P = np.array(L["P"])
    ratio = alpha_Z / (nu * P)
    return {
        "name": "axisym_compatible_concentration",
        "label": "AXISYM-CONDITIONAL_CLASS_BUT_SCALING_UNCHANGED",
        "verdict": "NO_REPAIR",
        "note": (
            "Restricting φ to axisymmetric-with-swirl does not change the "
            "λ-powers of Z, D, α, T. Axisym alone does not kill the λ^{1/2} escape."
        ),
        "alpha_Z_over_P_growth": float(ratio[-1] / ratio[0]),
        "axisym_changes_ledger": False,
    }


def probe_forbidden_slots() -> dict:
    drafts = [
        {
            "name": "smuggle_Zdot",
            "claim": r"(T)_+ ≤ |Ż_j| + ν D_j",
            "verdict": "REFUSED",
            "slot": r"\dot Z_j",
        },
        {
            "name": "smuggle_Lambda",
            "claim": r"sign(Λ') ⇒ α₊ depletion",
            "verdict": "REFUSED",
            "slot": r"\Lambda'",
        },
        {
            "name": "smuggle_ej_dot",
            "claim": r"|T| ≤ C|ė_j|",
            "verdict": "REFUSED",
            "slot": r"\dot e_j",
        },
        {
            "name": "bkm_shortcut",
            "claim": r"BKM ||ω||_∞ ⇒ (A) free",
            "verdict": "REFUSED_STRONGER_OBJECT",
            "slot": r"\|\omega\|_\infty",
        },
        {
            "name": "phi_as_depletion",
            "claim": r"Φ-renorm ⇒ α₊ controlled",
            "verdict": "KILLED_AS_STANDALONE",
            "note": "KEEP algebra; not α₊ / T^mm bound",
        },
        {
            "name": "pointwise_cz_Linf",
            "claim": r"|α|≲|ω| pointwise ⇒ L^∞ from L²",
            "verdict": "KILLED",
            "note": "Not revived from harder-run",
        },
    ]
    return {
        "name": "forbidden_and_dead_shortcuts",
        "forbidden_slots": list(FORBIDDEN),
        "drafts": drafts,
        "all_refused_or_killed": all(
            d["verdict"].startswith(("REFUSED", "KILLED")) for d in drafts
        ),
    }


def probe_conditional_alpha_theta() -> dict:
    return {
        "name": "conditional_alpha_theta_packaging",
        "hypothesis": (
            r"[α_θ]: ∫(α_loc,j)_+ |Δ_j ω|² ≤ θ ν D_j + R(E,{Z_k},direction) a.e. t"
        ),
        "theorem": (
            "Under [α_θ], main stretch enters (A). Commutators still open "
            "(Bernstein / ||u_loc||_∞)."
        ),
        "verdict": "CONDITIONAL_PROVED_AS_PACKAGING",
        "dynamics_produce_hypothesis": "OPEN_EMPTY",
        "geometric_CF_fill": "ABSENT_IN_REPO",
        "ns_solved": False,
        "clay_claim": False,
        "note": (
            "Honest C6 hinge. Conditional theorem ≠ absolute depletion from NS."
        ),
    }


def probe_geometric_G_delta() -> dict:
    return {
        "name": "geometric_G_delta_CF_style",
        "verdict": "ABSENT",
        "status": "CONDITIONAL_PACKAGING_ONLY",
        "note": (
            "Constantin–Fefferman-style direction hypothesis is named as [G_δ] "
            "but not seated as a theorem on this shell face. Import+line-match "
            "not done. Do not claim CF ⇒ (A)."
        ),
        "fills_alpha_theta_if_imported": True,
        "imported": False,
    }


def probe_axisym_alpha_split() -> dict:
    return {
        "name": "axisym_alpha_mm_ss_cross",
        "label": "AXISYM-CONDITIONAL",
        "verdict": "IDENTITY_ONLY_NO_BOUND",
        "proved": [
            "TJJ-pure: pure swirl ⇒ T=0 (subclass)",
            "bilinear α = α^mm + α^ss + α^cross (identity-level)",
        ],
        "killed_or_false": [
            "Φ-renorm controls α_+ / T^mm",
            "2D regularity frees α^mm on mixed fields",
            "SO(2) ⇒ α_+ small as class bound",
        ],
        "open_remainder": "mixed swirl+meridional α^mm / T^mm geometric control",
        "ns_solved": False,
    }


def main() -> int:
    payload = {
        "title": "alpha_plus_depletion_C10_through_C6",
        "date": "2026-10-01",
        "branch": "cursor/alpha-plus-depletion-0cc5",
        "parent": "cursor/tj-candidates-9083 / PR #102",
        "ns_solved": False,
        "clay_claim": False,
        "forbidden_slots": list(FORBIDDEN),
        "not_revived": [
            "C1",
            "C2",
            "C3",
            "C4",
            "C5",
            "sobolev_alpha_vs_P",
            "cz_pointwise_Linf",
            "phi_as_depletion",
            "bkm_shortcut",
            "naive_energy_HH",
        ],
        "probes": {
            "absolute_sobolev": probe_absolute_sobolev_vs_P(),
            "cz_integrable": probe_cz_integrable_substitute(),
            "axisym_scaling": probe_axisym_compatible_scaling(),
            "forbidden": probe_forbidden_slots(),
            "conditional_alpha_theta": probe_conditional_alpha_theta(),
            "geometric_G_delta": probe_geometric_G_delta(),
            "axisym_alpha_split": probe_axisym_alpha_split(),
        },
        "blunt_verdict": "OPEN_absolute__CONDITIONAL_best",
        "best_statement": (
            "Under explicit [α_θ], main stretch enters (A). CZ integrable "
            "substitute avoids ||α₊||_∞ but hits cubic wall and λ^{1/2} escape "
            "— not absolute (A). Geometric CF and axisym mixed-α still open. "
            "Commutators open. NS not solved."
        ),
        "scoreboard": {
            "TJJ_identities": "PROVED",
            "C10_implication_tautology": "PROVED",
            "alpha_CZ_sketch": "STANDARD_seated_not_a_close",
            "absolute_alpha_plus": "OPEN_false_on_concentration",
            "cz_as_absolute_A": "KILLED",
            "conditional_alpha_theta": "CONDITIONAL_PROVED_packaging",
            "dynamics_to_alpha_theta": "OPEN_EMPTY",
            "geometric_CF": "ABSENT",
            "commutators_allowed_R": "OPEN",
            "axisym_mixed_alpha": "OPEN_axisym_conditional",
            "T_j_controlled": "OPEN",
        },
    }

    out_json = OUT / "alpha_plus_depletion_results.json"
    repo_json = REPO_OUT / "alpha_plus_depletion_results.json"
    text = json.dumps(payload, indent=2) + "\n"
    out_json.write_text(text)
    repo_json.write_text(text)

    sob = payload["probes"]["absolute_sobolev"]
    cz = payload["probes"]["cz_integrable"]
    ax = payload["probes"]["axisym_scaling"]
    cond = payload["probes"]["conditional_alpha_theta"]

    lines = [
        "=== α₊ DEPLETION ⇒ (A) — C10 through C6 (2026-10-01) ===",
        "NS not solved. No Clay claim. C1–C5 not revived. Forbidden slots empty.",
        "",
        f"Sobolev αZ/(νP): {sob['verdict']} growth={sob['growth']:.3g}",
        f"CZ substitute Z^{{3/4}}D^{{3/4}}/(νD): {cz['verdict']} "
        f"growth={cz['cz_over_nu_D_growth']:.3g} "
        f"Z3/D growth={cz['Z3_over_D_growth']:.3g}",
        f"Axisym scaling repair: {ax['verdict']} "
        f"(changes_ledger={ax['axisym_changes_ledger']})",
        f"Forbidden checklist ok: "
        f"{payload['probes']['forbidden']['all_refused_or_killed']}",
        f"[α_θ] packaging: {cond['verdict']} "
        f"(dynamics⇒hyp={cond['dynamics_produce_hypothesis']})",
        f"[G_δ] CF: {payload['probes']['geometric_G_delta']['verdict']}",
        f"Axisym α-split: {payload['probes']['axisym_alpha_split']['verdict']}",
        "",
        f"BLUNT: {payload['blunt_verdict']}",
        payload["best_statement"],
        "",
        f"Wrote {out_json}",
        f"Wrote {repo_json}",
    ]
    log = "\n".join(lines) + "\n"
    (OUT / "alpha_plus_depletion.log").write_text(log)
    (REPO_OUT / "alpha_plus_depletion.log").write_text(log)
    print(log, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
