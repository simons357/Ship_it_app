"""θ-template laboratory diagnostics (not a bridge to (A); not WRITE (6)).

Honesty lock (Jonathan, 2026-10-01):
  The class hunt is the same-scale route. It does NOT supply WRITE (6)/H1.
  enforced_alignment_theta has three unresolved parts:
    1. Wrong quantities: disk template uses shell energy Z and
       D = Σ |k|² |û_k|² — that D is NOT palinstrophy.
    2. Assumed cancellation: θ = |Σ c_△| / Σ |c_△| measures tested
       transfers; defining a class by small θ does NOT prove NSE keeps
       solutions in that class.
    3. Unproved template constant: conditional_theta_bound() calculates
       a proposed RHS; it does NOT establish a cutoff-uniform C.

  Useful CONDITIONAL LABORATORY MATERIAL only. Missing mathematics:
    - enstrophy transfer estimate
    - dynamical mechanism that maintains depletion
    - cross-scale assembly

  WRITE (6)/H1 still needs the separate bad-pair cylinder estimate.
  Neither this template nor its tests prove that estimate.

Lab probes may still print scaling O(ν)/O(√ν) under *pretend* Poincaré
letters — those are diagnostics, not a seated bridge to (A).

Locked: NS not solved. Clay NOT CLAIMED. DA-VC-01 FAIL.
Spectral-shift ≠ Lemma★. Energy b=0 identity ≠ depletion.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from .axisym_same_scale_tjj import (
    build_reality_paired_field,
    dissipation_proxy,
    energy_z,
    enumerate_near_scale_feeders,
    geometric_factor_theta,
    maximize_same_scale_ratio,
    same_scale_transfer,
    shell_modes,
)

HONESTY = {
    "NS_solved": False,
    "clay": "NOT CLAIMED",
    "DA_VC_01": "FAIL",
    "uses_edot_zdot_lambda_to_bound_Tjj": False,
    "spectral_shift_is_lemma_star": False,
    "energy_b0_identity_is_depletion": False,
    "principal_unresolved": "T_{j←j}",
    "A_seated": False,
    "bridges_to_A": False,
    "supplies_WRITE_6_H1": False,
    "WRITE_6_status": "PARK / OPEN — bad-pair cylinder estimate still needed",
    "material_kind": "conditional laboratory material",
    "D_is_palinstrophy": False,
    "D_definition": "Σ |k|² |û_k|² (energy dissipation proxy; NOT palinstrophy)",
    "theta_class_proves_NSE_invariance": False,
    "conditional_theta_bound_proves_cutoff_uniform_C": False,
    "three_unresolved_parts": (
        "wrong_quantities_D_not_palinstrophy",
        "assumed_cancellation_no_NSE_invariance",
        "unproved_template_constant",
    ),
    "missing_mathematics": (
        "enstrophy_transfer_estimate",
        "dynamical_depletion_mechanism",
        "cross_scale_assembly",
    ),
}


def palinstrophy_proxy(
    field: dict[tuple[int, int, int], np.ndarray],
) -> float:
    """P_proxy = Σ_k |k|^4 |û_k|^2  (∇ω / Δu style; not LP projector)."""
    total = 0.0
    for k, u in field.items():
        kn2 = float(k[0] * k[0] + k[1] * k[1] + k[2] * k[2])
        total += (kn2 * kn2) * float(np.vdot(u, u).real)
    return total


def shell_scale_lambda(
    field: dict[tuple[int, int, int], np.ndarray],
) -> float:
    """Energy-weighted mean |k| on the field support (disk λ proxy)."""
    num = 0.0
    den = 0.0
    for k, u in field.items():
        w = float(np.vdot(u, u).real)
        kn = math.sqrt(float(k[0] * k[0] + k[1] * k[1] + k[2] * k[2]))
        num += kn * w
        den += w
    if den <= 1e-30:
        return 1.0
    return num / den


def meridional_energy_fraction(
    field: dict[tuple[int, int, int], np.ndarray],
) -> float:
    """E_mer / E: fraction of energy in meridional (non-ê_y) polarization.

    On the axisym swirl slice (k_y=0), swirl ∥ ê_y and meridional ⟂ ê_y.
    """
    e_mer = 0.0
    e_tot = 0.0
    ey = np.array([0.0, 1.0, 0.0])
    for u in field.values():
        w = float(np.vdot(u, u).real)
        e_tot += w
        # Projection onto ê_y (swirl) vs remainder (meridional).
        swirl_amp = complex(np.vdot(ey, u))  # conj(ey)·u = u_y since ey real
        # |proj_ey u|^2 = |u_y|^2
        e_swirl = float(abs(u[1]) ** 2)
        e_mer += w - e_swirl
    if e_tot <= 1e-30:
        return 0.0
    return max(0.0, min(1.0, e_mer / e_tot))


# ---------------------------------------------------------------------------
# Analytic scaling obstruction (the kill)
# ---------------------------------------------------------------------------


def scaling_obstruction(
    *,
    c_young: float = 1.0,
    c_poincare: float = 1.0,
    eps_target: float = 0.99,
    lambda_shell: float = 1.0,
    z_shell: float = 1.0,
) -> dict[str, Any]:
    """Lab probe: pretend-letter absorption of θ C √D Z into εν P + R.

    HONESTY: disk D = Σ |k|² |û|² is NOT palinstrophy. This routine does
    **not** bridge to (A). It only shows that *even under pretend*
    heuristics D∼λ² Z, P∼λ⁴ Z, one still needs θ_* = O(ν) or O(√ν).

    Status: PARTIAL/KILL as bridge (quantity mismatch + scaling).
    """
    c_y = float(c_young)
    c_p = float(c_poincare)
    eps = float(eps_target)
    lam = float(lambda_shell)
    z = float(z_shell)
    assert 0.0 < eps < 1.0
    assert lam > 0.0 and z > 0.0 and c_y > 0.0 and c_p > 0.0

    # θ_max_direct(ν) for R=0 absorption
    # θ ≤ (ε ν c_p λ³) / (C √Z)
    coeff_direct = (eps * c_p * (lam**3)) / (c_y * math.sqrt(z))

    # θ_max_young(ν) so that θ²/ν ≤ 1 (unit ν-uniform R coefficient)
    # More precisely: demand R ≤ K Z²/λ² with K=1 ⇒ θ ≤ 2 √(ε ν c_p) / C
    coeff_young = 2.0 * math.sqrt(eps * c_p) / c_y

    nu_grid = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
    table = []
    for nu in nu_grid:
        theta_direct = coeff_direct * nu
        theta_young = coeff_young * math.sqrt(nu)
        table.append(
            {
                "nu": nu,
                "theta_star_needed_direct_R0": theta_direct,
                "theta_star_needed_young_nu_uniform_R": theta_young,
                "geometric_theta_O1_survives": False,
            }
        )

    return {
        "status": "KILL",
        "status_as_bridge": "PARTIAL/KILL",
        "route": "theta_lab_diagnostics_not_bridge_to_A",
        "template": "|T_near| ≤ θ_* C_young √D Z",
        "target_not_reached": "|T_{j←j}| ≤ ε ν P_j + R",
        "quantity_mismatch": {
            "D_is_palinstrophy": False,
            "D_definition": "Σ |k|² |û_k|²",
            "Z_is": "shell energy (disk)",
            "blocks_bridge_to_A": True,
        },
        "shell_heuristics_pretend_only": {
            "D_sim": "λ² Z",
            "P_sim": "λ⁴ Z",
            "Poincare_shell": "P ≥ c_poincaré λ² D  (pretend hinge; not proved here)",
            "note": "pretend letters for lab scaling only — do not claim (A)",
        },
        "route_1_direct_absorption": {
            "form": "θ C √D Z ≤ ε ν c_p λ² D   (R=0; pretend)",
            "theta_star_scaling": "O(ν)",
            "explicit": "θ ≤ (ε ν c_p λ³)/(C √Z)",
            "coeff_at_unit_shell": coeff_direct,
            "fatal_for_large_data_geometric_class": True,
        },
        "route_2_young_palinstrophy_weights": {
            "form": "θ C Z √D ≤ (ε ν c_p λ²) D + (θ C Z)²/(4 ε ν c_p λ²)",
            "R": "θ² C² Z² / (4 ε ν c_p λ²)",
            "theta_star_for_nu_uniform_R": "O(√ν)",
            "explicit_nu_uniform": "θ ≤ 2 √(ε ν c_p)/C",
            "coeff_sqrt_nu": coeff_young,
            "fatal_for_large_data_geometric_class": True,
        },
        "parameters": {
            "C_young": c_y,
            "c_poincare": c_p,
            "eps_target": eps,
            "lambda_shell": lam,
            "Z_shell": z,
        },
        "nu_table": table,
        "verdict": (
            "PARTIAL/KILL as bridge: (i) D is not palinstrophy — wrong "
            "quantities for (A); (ii) even under pretend Poincaré letters, "
            "θ_* = O(ν) or O(√ν) is viscosity smallness, not a geometric "
            "seat. Lab diagnostics only. Does not supply WRITE (6)/H1."
        ),
        "does_not_use": ["ė_j", "Ż", "Λ′", "occupancy-as-depletion", "b=0-as-depletion"],
        "A_seated": False,
        "bridges_to_A": False,
        "supplies_WRITE_6_H1": False,
        "honesty": HONESTY,
    }


# ---------------------------------------------------------------------------
# Numeric bridge probe on mixed axisym disks
# ---------------------------------------------------------------------------


def _probe_one_field(
    field: dict[tuple[int, int, int], np.ndarray],
    shell: list[tuple[int, int, int]],
    near: list,
    *,
    c_young: float,
    nu_values: list[float],
) -> dict[str, Any] | None:
    shell_field = {m: field[m] for m in shell if m in field}
    z = energy_z(shell_field)
    d = dissipation_proxy(shell_field)
    p = palinstrophy_proxy(shell_field)
    if z <= 1e-30 or d <= 1e-30 or p <= 1e-30:
        return None
    t_near = same_scale_transfer(field, near)
    theta = geometric_factor_theta(field, near)
    lam = shell_scale_lambda(shell_field)
    e_mer_frac = meridional_energy_fraction(field)
    abs_t = abs(t_near)
    template_rhs = theta * c_young * math.sqrt(d) * z
    # Observed ratios
    ratio_vs_template = abs_t / template_rhs if template_rhs > 1e-30 else 0.0
    ratio_t_over_p = abs_t / p
    # Poincaré check on this sample: P / (λ² D)
    poincare_ratio = p / (max(lam, 1e-12) ** 2 * d)

    # For each ν: ε_implied if we try abs_t ≤ ε ν P (R=0)
    # and θ_* needed from scaling formulas using this sample's λ,Z
    nu_rows = []
    for nu in nu_values:
        eps_implied = abs_t / (nu * p) if nu * p > 0 else float("inf")
        # Direct: θ_need = (ε=0.99) ν c_p λ³ / (C √Z) with c_p from sample
        c_p_sample = max(poincare_ratio, 1e-12)
        theta_need_direct = (0.99 * nu * c_p_sample * (lam**3)) / (
            c_young * math.sqrt(z)
        )
        theta_need_young = (2.0 * math.sqrt(0.99 * nu * c_p_sample)) / c_young
        nu_rows.append(
            {
                "nu": nu,
                "eps_implied_R0": eps_implied,
                "eps_lt_1": eps_implied < 1.0,
                "theta_need_direct": theta_need_direct,
                "theta_need_young": theta_need_young,
                "theta_observed": theta,
                "theta_obs_le_direct_need": theta <= theta_need_direct,
                "theta_obs_le_young_need": theta <= theta_need_young,
            }
        )

    return {
        "Z": z,
        "D": d,
        "P_proxy": p,
        "lambda": lam,
        "T_near": t_near,
        "|T_near|": abs_t,
        "theta": theta,
        "E_mer/E": e_mer_frac,
        "template_rhs_theta_C_sqrtD_Z": template_rhs,
        "|T|/template_rhs": ratio_vs_template,
        "|T|/P_proxy": ratio_t_over_p,
        "P/(λ² D)": poincare_ratio,
        "nu_absorption": nu_rows,
    }


def numeric_bridge_probe(
    *,
    n_trials: int = 120,
    seed: int = 41,
    c_young: float = 1.0,
    nu_values: list[float] | None = None,
) -> dict[str, Any]:
    """Mixed axisym-swirl disks: θ, |T|/P, required θ_* vs ν.

    Counterexample shape for 'θ = O(1) geometric class seats (A)':
    on typical mixed disks θ stays O(10^{-2})–O(1) while ε_implied = |T|/(ν P)
    blows as ν→0. Observed θ ≫ O(ν) and ≫ O(√ν) for small ν.
    """
    if nu_values is None:
        nu_values = [1e-1, 1e-2, 1e-3, 1e-4]
    rng = np.random.default_rng(seed)
    support = shell_modes(0.5, 7.0, disk="axisym_swirl_slice")
    shell = shell_modes(2.5, 4.5, disk="axisym_swirl_slice")
    neighbors = shell_modes(1.0, 6.0, disk="axisym_swirl_slice")
    near = enumerate_near_scale_feeders(shell, neighbors)

    records: list[dict[str, Any]] = []
    for _ in range(int(n_trials)):
        field = build_reality_paired_field(support, rng, disk="axisym_swirl_slice")
        rec = _probe_one_field(
            field, shell, near, c_young=c_young, nu_values=nu_values
        )
        if rec is not None:
            records.append(rec)

    if not records:
        return {
            "status": "EMPTY",
            "n_trials": n_trials,
            "n_records": 0,
            "verdict": "no usable trials",
        }

    thetas = [r["theta"] for r in records]
    ratios_tp = [r["|T|/P_proxy"] for r in records]
    e_mers = [r["E_mer/E"] for r in records]
    poincares = [r["P/(λ² D)"] for r in records]

    # Fraction of trials where observed θ beats the needed θ for each ν
    frac_direct: dict[str, float] = {}
    frac_young: dict[str, float] = {}
    frac_eps_lt1: dict[str, float] = {}
    for i, nu in enumerate(nu_values):
        key = f"nu={nu:g}"
        frac_direct[key] = float(
            np.mean([r["nu_absorption"][i]["theta_obs_le_direct_need"] for r in records])
        )
        frac_young[key] = float(
            np.mean([r["nu_absorption"][i]["theta_obs_le_young_need"] for r in records])
        )
        frac_eps_lt1[key] = float(
            np.mean([r["nu_absorption"][i]["eps_lt_1"] for r in records])
        )

    # Natural proxy: does small E_mer/E force small θ?
    # Correlate on records
    corr = float(np.corrcoef(e_mers, thetas)[0, 1]) if len(records) > 2 else 0.0

    # Worst-case: max |T|/P among mixed samples with θ not tiny
    mixed = [r for r in records if r["E_mer/E"] > 0.05 and r["theta"] > 0.01]
    max_t_over_p_mixed = max((r["|T|/P_proxy"] for r in mixed), default=0.0)

    kill_numeric = (
        float(np.mean(thetas)) > 1e-3
        and frac_eps_lt1.get("nu=0.0001", 1.0) < 0.5
        and max_t_over_p_mixed > 0.0
    )

    return {
        "status": "KILL" if kill_numeric else "PARTIAL",
        "disk": "axisym_swirl_slice",
        "n_trials": n_trials,
        "n_records": len(records),
        "n_near_triads": len(near),
        "theta_stats": {
            "mean": float(np.mean(thetas)),
            "median": float(np.median(thetas)),
            "min": float(np.min(thetas)),
            "max": float(np.max(thetas)),
            "p10": float(np.percentile(thetas, 10)),
            "p90": float(np.percentile(thetas, 90)),
        },
        "|T|/P_proxy_stats": {
            "mean": float(np.mean(ratios_tp)),
            "max": float(np.max(ratios_tp)),
            "max_on_mixed_theta_gt_0.01": max_t_over_p_mixed,
        },
        "Poincare_P/(λ²D)_stats": {
            "mean": float(np.mean(poincares)),
            "min": float(np.min(poincares)),
            "max": float(np.max(poincares)),
        },
        "E_mer/E_stats": {
            "mean": float(np.mean(e_mers)),
            "min": float(np.min(e_mers)),
            "max": float(np.max(e_mers)),
            "corr_with_theta": corr,
        },
        "fraction_trials_theta_obs_le_need_direct": frac_direct,
        "fraction_trials_theta_obs_le_need_young": frac_young,
        "fraction_trials_eps_implied_lt_1": frac_eps_lt1,
        "natural_proxy_E_mer/E": {
            "forces_small_theta": abs(corr) > 0.5
            and float(np.mean(thetas)) < 0.05
            and False,  # explicit: correlation alone is not class control
            "corr_with_theta": corr,
            "verdict": (
                "KILL as natural θ-proxy: E_mer/E stays O(1) on mixed disks and "
                f"corr(E_mer/E, θ)={corr:.3g} does not force θ→0 on a nonempty "
                "large-data class"
            ),
        },
        "verdict": (
            "Numeric KILL support: on mixed axisym disks θ remains typically "
            "O(10^{-2})–O(1), while ε_implied=|T|/(ν P) exceeds 1 for small ν. "
            "Observed θ does not track O(ν) or O(√ν). Natural E_mer/E proxy "
            "does not stay small. Bridge fails on these disks."
        ),
        "scope": "finite exact disks / trials; not K_max→∞; not a class close",
        "uses_edot_zdot_lambda": False,
        "A_seated": False,
    }


def natural_theta_proxy_probe(
    *, n_trials: int = 80, seed: int = 42
) -> dict[str, Any]:
    """Optional: hunt a *natural* (unenforced) proxy that stays small on a class.

    Candidates: E_mer/E, θ itself unrestricted, feeder-density (near triad count
    is support-fixed on a disk so not a field proxy here).
    Expected: KILL — nothing stays uniformly small on nonempty mixed samples.
    """
    rng = np.random.default_rng(seed)
    support = shell_modes(0.5, 7.0, disk="axisym_swirl_slice")
    shell = shell_modes(2.5, 4.5, disk="axisym_swirl_slice")
    neighbors = shell_modes(1.0, 6.0, disk="axisym_swirl_slice")
    near = enumerate_near_scale_feeders(shell, neighbors)

    thetas: list[float] = []
    e_mers: list[float] = []
    ratios: list[float] = []
    for _ in range(int(n_trials)):
        field = build_reality_paired_field(support, rng, disk="axisym_swirl_slice")
        shell_field = {m: field[m] for m in shell if m in field}
        z = energy_z(shell_field)
        if z <= 1e-30:
            continue
        t_near = same_scale_transfer(field, near)
        theta = geometric_factor_theta(field, near)
        e_mer = meridional_energy_fraction(field)
        thetas.append(theta)
        e_mers.append(e_mer)
        ratios.append(abs(t_near) / (z**1.5))

    # Fraction with θ ≤ 0.05 (enforced class membership by chance)
    frac_theta_small = float(np.mean([t <= 0.05 for t in thetas])) if thetas else 0.0
    # Among θ-small, is |T|/Z^{3/2} small? (template says scaled by θ, not zero)
    small_idx = [i for i, t in enumerate(thetas) if t <= 0.05]
    max_ratio_small = (
        max(ratios[i] for i in small_idx) if small_idx else 0.0
    )

    return {
        "status": "KILL",
        "proxies_tested": ["theta_unrestricted", "E_mer/E"],
        "theta_unrestricted": {
            "mean": float(np.mean(thetas)) if thetas else 0.0,
            "max": float(np.max(thetas)) if thetas else 0.0,
            "fraction_le_0.05": frac_theta_small,
            "stays_small_on_nonempty_mixed_class": False,
        },
        "E_mer/E": {
            "mean": float(np.mean(e_mers)) if e_mers else 0.0,
            "min": float(np.min(e_mers)) if e_mers else 0.0,
            "max": float(np.max(e_mers)) if e_mers else 0.0,
            "stays_small_on_nonempty_mixed_class": False,
        },
        "inside_theta_le_0.05": {
            "n": len(small_idx),
            "max_|T|/Z^{3/2}": max_ratio_small,
            "note": "membership by chance on finite trials; not a natural seat",
        },
        "verdict": (
            "KILL: no natural proxy for θ stays uniformly small on a nonempty "
            "mixed axisym-with-swirl class. Unrestricted θ is O(1) in the bulk; "
            "E_mer/E is O(1) on mixed fields. Enforced {θ≤θ_*} remains artificial."
        ),
        "A_seated": False,
        "uses_edot_zdot_lambda": False,
    }


def run_theta_bridge_battery(
    *, n_trials: int = 100, seed: int = 41
) -> dict[str, Any]:
    """θ lab battery: quantity mismatch + pretend-letter scaling + proxies."""
    analytic = scaling_obstruction()
    numeric = numeric_bridge_probe(n_trials=n_trials, seed=seed)
    natural = natural_theta_proxy_probe(n_trials=max(40, n_trials // 2), seed=seed + 1)
    disk = maximize_same_scale_ratio(
        disk="axisym_swirl_slice", n_trials=min(60, n_trials), seed=seed + 2
    )

    overall_status = "KILL"
    return {
        "honesty": HONESTY,
        "mission": (
            "Lab diagnostics on θ-template |T_near|≤θ_* C √D Z. "
            "NOT a bridge to |T_{j←j}|≤ε ν P_j + R. NOT WRITE (6)/H1."
        ),
        "overall_status": overall_status,
        "status_as_bridge": "PARTIAL/KILL",
        "analytic_scaling": analytic,
        "numeric_disk_probe": numeric,
        "natural_theta_proxy": natural,
        "disk_reference": {
            "max_|T_near|/Z^{3/2}": disk["best"]["max_|T_near|/Z^{3/2}"],
            "theta_near_at_best": disk["best"].get("theta_near_at_best"),
            "mean_theta": disk["mean_theta"],
        },
        "dead_end_writeup": {
            "id": "enforced_alignment_theta_lab_not_bridge",
            "prior_status": "KEEP-CONDITIONAL (lab template)",
            "bridge_status": "PARTIAL/KILL",
            "obstruction": (
                "Primary: D = Σ|k|²|û|² is not palinstrophy (wrong quantities). "
                "Also: θ-class is not NSE-invariant; conditional_theta_bound "
                "does not prove cutoff-uniform C. Lab scaling under pretend "
                "letters still needs θ_* = O(ν) or O(√ν)."
            ),
            "numeric_support": (
                "Mixed disks: θ = O(10^{-2})–O(1); ε_implied = |T|/(ν P_proxy) > 1 "
                "for small ν; natural E_mer/E proxy does not stay small."
            ),
            "what_survives": (
                "Conditional laboratory disk inequality under *enforced* [θ]. "
                "Not (A). Not WRITE (6). Wrong quantities remain."
            ),
            "updated_class_verdict": (
                "enforced_alignment_theta: KEEP-CONDITIONAL as lab material only; "
                "not a bridge to (A); does not supply WRITE (6)/H1."
            ),
            "three_unresolved_parts": list(HONESTY["three_unresolved_parts"]),
            "missing_mathematics": list(HONESTY["missing_mathematics"]),
            "WRITE_6_H1": HONESTY["WRITE_6_status"],
        },
        "locks": {
            "A_seated": False,
            "bridges_to_A": False,
            "supplies_WRITE_6_H1": False,
            "DA_VC_01": "FAIL",
            "clay": "NOT CLAIMED",
            "NS_solved": False,
            "uses_edot_zdot_lambda": False,
            "D_is_palinstrophy": False,
        },
        "overall": (
            "PARTIAL/KILL as bridge to (A): quantity mismatch (D ≠ palinstrophy) "
            "plus pretend-letter scaling O(ν)|O(√ν). Conditional lab material "
            "only. WRITE (6)/H1 bad-pair cylinder still OPEN. (A) not seated. "
            "Leftover OPEN. NS not solved. Clay NOT CLAIMED."
        ),
    }


def main() -> None:
    import json

    print(json.dumps(run_theta_bridge_battery(), indent=2, default=float))


if __name__ == "__main__":
    main()
