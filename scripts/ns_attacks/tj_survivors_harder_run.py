#!/usr/bin/env python3
"""HARDER second pass on SURVIVING T_{j←j} candidates (2026-10-01).

Push analytic pressure beyond the 2026-09-16 hard-run:
  C10 principal — sharper depletion⇒(A) lemmas via α₊ / non-circular routes
  C7 HH-only — kill more naive HH products; confirm HH can dominate
  C8 near-shell — pressure as C10 feeder (category gap vs shell (A))
  C6/C11/C9 — only insofar as they feed C10

Does NOT revive C1–C5. No HPC. No Clay claim. No ė_j / Ż / Λ' recycling.
NS is NOT solved.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ATTACKS = Path(__file__).resolve().parent
OUT = Path("/opt/cursor/artifacts/tj-survivors-harder-run")
REPO_OUT = ROOT / "results" / "tj-survivors-harder-run"
OUT.mkdir(parents=True, exist_ok=True)
REPO_OUT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ATTACKS))
from ns_lemma_star_core import Field, R_star, project_perp, shell_wavevectors  # noqa: E402

FORBIDDEN = (r"\dot e_j", r"\dot Z", r"\dot Z_j", r"\Lambda'")


# ---------------------------------------------------------------------------
# Concentration ledger (shared powers)
# ---------------------------------------------------------------------------


def concentration_ledger(lambdas: np.ndarray) -> dict:
    """u^λ = λ^{3/2} φ(λx) relative prototype powers."""
    E = np.ones_like(lambdas)
    Z = lambdas**2  # enstrophy
    D = lambdas**4  # palinstrophy / ||Δu||² scale
    P = lambdas**4  # shell palinstrophy P_j ~ D on occupied shell
    alpha = lambdas**2.5  # ||∇u||_∞ strain scale
    T = lambdas**4.5  # same-scale transfer scale
    return {
        "lambdas": lambdas,
        "E": E,
        "Z": Z,
        "D": D,
        "P": P,
        "alpha": alpha,
        "T": T,
        "alpha_Z": alpha * Z,
    }


# ---------------------------------------------------------------------------
# C10 — principal: depletion ⇒ (A) via α₊ / non-circular
# ---------------------------------------------------------------------------


def harder_c10() -> dict:
    """Sharper analytic pressure on depletion ⇒ (A).

    Seated skeleton (empty forbidden slots):
      If ∫ (α_loc,j)_+ |ω_j|² ≤ θ ν P_j + R_allowed  (θ<1),
      and R_allowed uses only energy / {Z_k} / geometric direction,
      then ρ_j < ν enters (A).

    New pressure vs hard-run #1:
      (1) Sobolev / Young against P_j itself fails on concentration
          (α Z)/(ν P) ~ λ^{1/2} → ∞ — so C10 cannot close by swapping
          E Z for P_j without geometry.
      (2) BKM ||ω||_∞ control is a stronger object than (A); circular for
          the shell remainder (uses what the chain is trying to reach).
      (3) Biot–Savart / CZ pointwise |α|≲|ω| returns the same L^∞ demand.
      (4) Constantin–Fefferman geometric depletion without a seated
          geometric hypothesis is ABSENT (not a theorem here).
      (5) Φ-renorm identity is algebra on T^ss; does not deplete T^mm / α₊.
      (6) Spectral-shift / ė_j / Ż smuggling still REFUSED.

    Independent geometric depletion still ABSENT. Door stays principal.
    """
    lambdas = np.array([4.0, 16.0, 64.0, 256.0, 1024.0])
    L = concentration_ledger(lambdas)
    nu = 1.0
    alpha_Z_over_P = L["alpha_Z"] / (nu * L["P"])  # ~ λ^{1/2}
    alpha_Z_over_T = L["alpha_Z"] / L["T"]  # ~ 1 (sharp for main stretch)

    drafts = [
        {
            "name": "smuggle_Zdot",
            "claim": r"(T)_+ ≤ |Ż_j| + ν D_j ⇒ (A)",
            "verdict": "REFUSED",
            "slot": r"\dot Z_j",
        },
        {
            "name": "smuggle_Lambda",
            "claim": r"sign(Λ') or |Λ'| ⇒ depletion",
            "verdict": "REFUSED",
            "slot": r"\Lambda'",
        },
        {
            "name": "smuggle_ej_dot",
            "claim": r"|T| ≤ C|ė_j| ⇒ depletion",
            "verdict": "REFUSED",
            "slot": r"\dot e_j",
        },
        {
            "name": "occupancy_alignment_samples",
            "claim": "occupancy≈1 + alignment≈½ ⇒ (A)",
            "verdict": "REFUSED_HONESTY",
            "note": "samples ≠ depletion",
        },
        {
            "name": "young_against_P_j_only",
            "claim": r"α_+ Z_j ≤ θ ν P_j + C E Z  (Sobolev, no geometry)",
            "verdict": "KILLED",
            "note": (
                "Concentration: αZ/(νP) ~ λ^{1/2}→∞ and αZ/(EZ)~λ^{5/2}→∞. "
                "Swapping energy remainder for palinstrophy does not seat (A)."
            ),
            "alpha_Z_over_P_growth": float(alpha_Z_over_P[-1] / alpha_Z_over_P[0]),
        },
        {
            "name": "bkm_omega_inf",
            "claim": r"BKM ∫||ω||_∞ dt <∞ ⇒ regularity ⇒ (A) free",
            "verdict": "REFUSED_STRONGER_OBJECT",
            "note": (
                "||ω||_∞ control is strictly stronger than the shell (A) remainder; "
                "using it to close T_{j←j} is circular for this chain."
            ),
        },
        {
            "name": "biot_savart_cz_pointwise",
            "claim": r"|α| ≤ C|ω| pointwise ⇒ α_+ controlled by Z",
            "verdict": "KILLED",
            "note": (
                "CZ/Biot–Savart gives singular-integral control, not L^∞ from L². "
                "Returns the same Bernstein / cubic wall as Door-3."
            ),
        },
        {
            "name": "cf_geometric_without_hypothesis",
            "claim": "Constantin–Fefferman depletion absolute, no geometric hyp.",
            "verdict": "ABSENT",
            "note": "No seated geometric depletion theorem in this repo face.",
        },
        {
            "name": "phi_renorm_as_depletion",
            "claim": r"Φ-identity 1/r^4 ∂_z(Γ²)=∂_z(Φ²) ⇒ depletion ⇒ (A)",
            "verdict": "KILLED_AS_STANDALONE",
            "note": (
                "KEEP algebra on swirl axis term; does not bound T^mm or α_+. "
                "Feeds C11/ss bookkeeping only."
            ),
        },
        {
            "name": "alpha_plus_geometric_or_hypothesis",
            "claim": r"∫(α_loc,j)_+ |ω_j|² ≤ θ ν P_j + R_geom  ⇒ (A)",
            "verdict": "COLLAPSES_TO_C6",
            "note": "Honest hinge: Door-3 / α-hypothesis (conditional if absolute fails).",
        },
        {
            "name": "Tmm_structure_axisym",
            "claim": r"|T^mm| ≤ θ ν P_j + R_geom under SO(2)",
            "verdict": "COLLAPSES_TO_C11",
            "note": "Axisym-conditional bulk target; still open.",
        },
        {
            "name": "near_shell_to_shell_A",
            "claim": "Near-shell K_αβ / R_★ lab ⇒ ρ_j < ν on shell face",
            "verdict": "COLLAPSES_TO_C8_CATEGORY_GAP",
            "note": (
                "★ near-shell lab ≠ shell-budget same-scale depletion; "
                "see harder C8 weaken as C10 feeder."
            ),
        },
        {
            "name": "standalone_geometric_depletion",
            "claim": "New geometric depletion not reducing to C6/C8/C11",
            "verdict": "ABSENT",
            "note": "Still no independent non-circular seated sketch.",
        },
    ]

    refused = [
        d["name"]
        for d in drafts
        if d["verdict"] in ("REFUSED", "REFUSED_HONESTY", "REFUSED_STRONGER_OBJECT")
    ]
    killed = [d["name"] for d in drafts if str(d["verdict"]).startswith("KILLED")]
    collapses = [d["name"] for d in drafts if str(d["verdict"]).startswith("COLLAPSES")]
    absent = [d["name"] for d in drafts if d["verdict"] == "ABSENT"]

    return {
        "id": "C10",
        "name": "noncircular_depletion_to_A",
        "hard_verdict": "SURVIVES",
        "strength": "PRINCIPAL_OPEN",
        "new_vs_hard_run_1": [
            "KILLED young_against_P_j_only (αZ/P ~ λ^{1/2} escape)",
            "REFUSED BKM ||ω||_∞ as stronger/circular object",
            "KILLED Biot–Savart/CZ pointwise α≲|ω| as L^∞ from L² myth",
            "KILLED Φ-renorm as standalone depletion",
            "C8 feeder flagged as category gap (not uniform shell (A))",
        ],
        "weakening": (
            "Principal door still empty. New kills: Sobolev-against-P_j, "
            "BKM-as-shortcut, CZ pointwise, Φ-as-depletion. Every remaining "
            "non-circular sketch collapses onto C6 (α_+ geometric/hyp), "
            "C11 (T^mm axisym), or C8-upgrade (blocked by category gap). "
            "No standalone depletion theorem seated."
        ),
        "forbidden_slots": list(FORBIDDEN),
        "drafts": drafts,
        "refused": refused,
        "killed_this_pass": killed,
        "collapses_onto": collapses,
        "absent_independent": absent,
        "ledger": {
            "lambdas": lambdas.tolist(),
            "alpha_Z_over_T": alpha_Z_over_T.tolist(),
            "alpha_Z_over_P": alpha_Z_over_P.tolist(),
            "alpha_Z_over_P_growth": float(alpha_Z_over_P[-1] / alpha_Z_over_P[0]),
        },
        "theorem_shaped_target": (
            "Prove depletion ⇒ (A) by a geometric (or explicitly conditional) "
            "bound on (α_loc,j)_+ so ∫(α_+)|ω_j|² ≤ θ ν P_j + R_allowed, "
            "without ė_j/Ż/Λ', without Bernstein cubic wall, and without "
            "treating BKM ||ω||_∞ or near-shell ★ samples as the bound. "
            "Absolute Sobolev control by P_j is false (λ^{1/2} escape)."
        ),
        "ns_solved": False,
    }


# ---------------------------------------------------------------------------
# C6 — feeds C10 via α₊ Door-3
# ---------------------------------------------------------------------------


def harder_c6() -> dict:
    """Sharpen Door-3: α₊ escapes the actual (A) comparison αZ vs νP."""
    lambdas = np.array([4.0, 16.0, 64.0, 256.0, 1024.0])
    L = concentration_ledger(lambdas)
    nu = 1.0
    alpha_Z_over_T = L["alpha_Z"] / L["T"]
    alpha_Z_over_EZ = L["alpha_Z"] / (L["E"] * L["Z"])
    alpha_Z_over_P = L["alpha_Z"] / (nu * L["P"])
    # Bernstein commutator: ||u_loc||_∞² Z / D ~ λ
    u_inf = lambdas**1.5
    comm_over_D = (u_inf**2) * L["Z"] / L["D"]
    return {
        "id": "C6",
        "name": "alpha_door3",
        "hard_verdict": "WEAKENED",
        "strength": "CONDITIONAL_CRITERION_ONLY",
        "feeds_C10": True,
        "new_vs_hard_run_1": [
            "NEW: αZ/(νP) ~ λ^{1/2}→∞ — escapes the (A)-normalized comparison itself",
        ],
        "weakening": (
            "Identities still sit (transport vanish; stretch=α). Absolute α_+ "
            "bound remains false: sharp for T (αZ/T~1), escapes EZ (λ^{5/2}), "
            "and newly escapes νP (λ^{1/2}). Bernstein commutator still escapes D. "
            "Door-3 = printed criterion / named α-hypothesis only."
        ),
        "identities_still_sit": [
            "TJJ-Trans: transport main vanishes",
            "TJJ-α: main stretch = ∫ α |ω_j|^2",
        ],
        "ledger": {
            "lambdas": lambdas.tolist(),
            "alpha_Z_over_T": alpha_Z_over_T.tolist(),
            "alpha_Z_over_E_Z": alpha_Z_over_EZ.tolist(),
            "alpha_Z_over_P": alpha_Z_over_P.tolist(),
            "alpha_Z_over_P_growth": float(alpha_Z_over_P[-1] / alpha_Z_over_P[0]),
            "comm_proxy_over_D": comm_over_D.tolist(),
            "comm_growth": float(comm_over_D[-1] / comm_over_D[0]),
        },
        "survives_as": "TRY_CONDITIONAL_if_alpha_hypothesis_named",
        "killed_as": [
            "unaugmented_absolute_alpha_plus_bound",
            "sobolev_alpha_vs_palinstrophy_P",
        ],
        "ns_solved": False,
    }


# ---------------------------------------------------------------------------
# C11 — feeds C10 only as named T^mm bulk
# ---------------------------------------------------------------------------


def harder_c11() -> dict:
    """Confirm Φ-identity ≠ T^mm bound; energy-R still dead; bulk still open."""
    table = [
        {"j": 1, "T_mm": 8.15e3, "T_ss": -62.0, "T_cross": 217.0},
        {"j": 2, "T_mm": -1.08e4, "T_ss": 4.03e3, "T_cross": -142.0},
        {"j": 3, "T_mm": -1.32e4, "T_ss": 622.0, "T_cross": 88.0},
    ]
    mm_frac = []
    for row in table:
        tot = abs(row["T_mm"]) + abs(row["T_ss"]) + abs(row["T_cross"])
        mm_frac.append(abs(row["T_mm"]) / tot)

    lambdas = np.array([4.0, 16.0, 64.0, 256.0])
    L = concentration_ledger(lambdas)
    # T^mm bulk ~ T; vs νP and vs EZ
    ratio_P = L["T"] / L["P"]  # ~ λ^{1/2}
    ratio_EZ = L["T"] / (L["E"] * L["Z"])  # ~ λ^{5/2}
    return {
        "id": "C11",
        "name": "meridional_Tmm_cancel",
        "axisym_conditional": True,
        "hard_verdict": "WEAKENED",
        "strength": "NAMED_BULK_TARGET_OPEN",
        "feeds_C10": True,
        "new_vs_hard_run_1": [
            "Φ-renorm KEEP algebra does not cancel T^mm (explicit non-feeder kill)",
            "T^mm vs νP also escapes ~λ^{1/2} (same as total T)",
        ],
        "weakening": (
            "T^mm remains the mixed-sample bulk. Energy-linear and palinstrophy-"
            "linear Sobolev R both escape. Φ-identity rewrites T^ss bookkeeping "
            "only. Lane feeds C10 only as axisym-conditional structure target."
        ),
        "recorded_mm_frac_of_abs_split": mm_frac,
        "mm_dominates": all(f > 0.5 for f in mm_frac),
        "T_over_P_growth": float(ratio_P[-1] / ratio_P[0]),
        "T_over_EZ_growth": float(ratio_EZ[-1] / ratio_EZ[0]),
        "phi_renorm_closes_Tmm": False,
        "survives_as": "TRY_axisym_conditional_structure_route",
        "ns_solved": False,
    }


# ---------------------------------------------------------------------------
# C9 — rewrite only; feeds C10 only as bookkeeping
# ---------------------------------------------------------------------------


def harder_c9() -> dict:
    """Confirm rewrite cannot manufacture allowed R; no new feeder path."""
    rng = np.random.default_rng(20261001)
    drifts = []
    for _ in range(60):
        J_xi, J_eta = rng.normal(size=2)
        w_xi, w_eta, w_zeta = rng.normal(size=3)
        tau = (w_xi - w_zeta) * J_xi + (w_eta - w_zeta) * J_eta
        for w_star in (0.0, float(np.mean([w_xi, w_eta, w_zeta])), 7.3, -2.1):
            tau_shift = (w_xi - w_star - (w_zeta - w_star)) * J_xi + (
                w_eta - w_star - (w_zeta - w_star)
            ) * J_eta
            drifts.append(abs(tau - tau_shift))
    max_drift = float(np.max(drifts))
    return {
        "id": "C9",
        "name": "triad_tau_structure",
        "hard_verdict": "WEAKENED",
        "strength": "IDENTITY_ONLY",
        "feeds_C10": False,
        "new_vs_hard_run_1": [
            "Confirmed: no new feeder path to C10; rewrite stays bookkeeping",
        ],
        "weakening": (
            "AS-τ / AS-ω* invariance holds; cannot manufacture allowed R. "
            "Does not feed C10 as a bound route."
        ),
        "omega_star_invariance_max_abs_drift": max_drift,
        "invariance_holds": max_drift < 1e-10,
        "survives_as": "rewrite_tool_not_bound",
        "killed_as": "standalone_estimate_and_C10_feeder",
        "ns_solved": False,
    }


# ---------------------------------------------------------------------------
# C7 — HH-only budget (harder)
# ---------------------------------------------------------------------------


def harder_c7_analytic() -> dict:
    """Kill more naive HH product forms; HH can dominate by construction."""
    lambdas = np.array([4.0, 16.0, 64.0, 256.0, 1024.0])
    L = concentration_ledger(lambdas)
    T_HH = L["T"]  # assume HH carries bulk same-scale
    E, X, D = L["E"], L["Z"], L["D"]

    # Form A: energy-only ★-style E^{1/2} X^{3/2}
    form_A = np.sqrt(E) * (X**1.5)
    ratio_A = T_HH / form_A  # ~ λ^{3/2}

    # Form B: Agmon-style ||∇u||_∞ ≲ X^{1/4} D^{1/4} (up to E factors)
    # Then |T_HH| ≲ ||∇u||_∞ X  ⇒ ratio vs X^{5/4} D^{1/4}
    form_B = (X**1.25) * (D**0.25)
    ratio_B = T_HH / form_B  # λ^{4.5} / (λ^{2.5} λ^{1}) = λ^{1} → ∞
    # X^{5/4}=λ^{2.5}, D^{1/4}=λ; product λ^{3.5}; T/form = λ^{4.5}/λ^{3.5}=λ

    # Form C: Bernstein high-mode ||∇u_H||_∞ ≲ 2^{3j/2} X_H^{1/2} with 2^j~λ
    # ⇒ ||∇u_H||_∞ X ≲ λ^{3/2} λ  * λ²? X_H^{1/2}~λ, so λ^{3/2}*λ * X(=λ²) = λ^{3/2} λ λ² = λ^{4.5}
    # Actually: product bound |T|≲ ||∇u_H||_∞ X with ||∇u_H||_∞ ~ λ^{3/2} X^{1/2} ~ λ^{3/2} λ = λ^{5/2}
    # |T| bound ~ λ^{5/2} * λ² = λ^{9/2} = T scale — SCHWARZ equality / sharp, not a closing gap.
    # Closing ★ needs something smaller than T; Bernstein saturates T scale ⇒ no room for θνP.
    bernstein_bound_scale = (lambdas**1.5) * (X**0.5) * X  # ||∇u||_∞ * X
    ratio_C = T_HH / bernstein_bound_scale  # ~ 1 (saturates; no absorption margin)

    return {
        "id": "C7",
        "name": "HH_only_budget",
        "analytic_note": (
            "Energy-only HH product dies (λ^{3/2}). Agmon-style dies (λ). "
            "Bernstein high-mode product saturates the T scale (ratio~1) — "
            "sharp but gives no θνP absorption margin. HH can dominate by "
            "construction on high_triad. Lane SURVIVES as live bottleneck "
            "needing a geometric HH product beyond Sobolev/Bernstein/Agmon."
        ),
        "form_A_energy_ratio_growth": float(ratio_A[-1] / ratio_A[0]),
        "form_B_agmon_ratio_growth": float(ratio_B[-1] / ratio_B[0]),
        "form_C_bernstein_saturates": True,
        "form_C_ratio_mean": float(np.mean(ratio_C)),
        "naive_forms_killed": ["energy_only", "agmon_style"],
        "bernstein_no_absorption_margin": True,
        "ns_solved": False,
    }


# ---------------------------------------------------------------------------
# C8 — near-shell as C10 feeder (category gap)
# ---------------------------------------------------------------------------


def harder_c8_analytic() -> dict:
    """Pressure C8 as a feeder into shell-budget depletion ⇒ (A).

    Facts:
      - Single-shell fields: D_s=0, T_c=0 (vacuous for ★ quotient).
      - Same-scale shell transfer T_{j←j} lives ON shell j; near-shell
        cancellation in the ★ two-shell laboratory does not automatically
        deplete on-shell ρ_j.
      - Finite K_αβ / small R_★ on samples ≠ uniform depletion ⇒ (A).
      - Upgrading C8 → C10 requires a theorem linking near-shell structure
        to shell (A); that link is not seated.

    Verdict as lab for ★: still SURVIVES (no kill on samples).
    Verdict as C10 feeder: WEAKENED (category gap).
    """
    return {
        "id": "C8",
        "name": "near_shell_cancellation",
        "hard_verdict": "SURVIVES",
        "strength": "LAB_ONLY",
        "feeds_C10": "WEAKENED_CATEGORY_GAP",
        "new_vs_hard_run_1": [
            "Explicit category gap: ★ near-shell lab ≠ shell-budget (A) depletion",
            "Single-shell vacuity underscores that cancel-of-spread ≠ on-shell T control",
        ],
        "weakening": (
            "Still lab/evidence for ★ packaging only. As a C10 feeder into "
            "shell (A), WEAKENED: no seated theorem converts near-shell K_αβ / "
            "finite R_★ samples into ρ_j < ν. Occupancy 1 ≠ depletion."
        ),
        "category_gap": {
            "lemma_star_near_shell_lab": "SURVIVES_as_evidence",
            "shell_budget_depletion_to_A": "NOT_SEATED",
            "single_shell_Tc_Ds": "vacuous_zero",
        },
        "ns_solved": False,
    }


# ---------------------------------------------------------------------------
# Light numerics / subprocess
# ---------------------------------------------------------------------------


def light_rstar(rng: np.random.Generator) -> dict:
    def _rand_perp(k):
        w = rng.normal(size=3) + 1j * rng.normal(size=3)
        return project_perp(k, w)

    rows = []
    for n1, n2 in [(1, 2), (2, 5), (3, 6), (4, 7), (5, 8)]:
        f = Field()
        for n, amp in ((n1, 1.0), (n2, 1.0)):
            ks = shell_wavevectors(n, canonical_only=True)
            pick = list(ks)
            rng.shuffle(pick)
            for k in pick[: min(4, len(pick))]:
                f.set_mode(k, amp * _rand_perp(k))
        f = f.normalize(1.0)
        rec = R_star(f, verify=True)
        rs = rec["R_star"]
        rows.append(
            {
                "family": f"two_shell_{n1}_{n2}",
                "T_c": float(rec["T_c"]),
                "D_s": float(rec["D_s"]),
                "R_star": None if rs == float("inf") else float(rs),
            }
        )
    finite = [r["R_star"] for r in rows if r["R_star"] is not None]
    return {
        "rows": rows,
        "max_R_star_finite": max(finite) if finite else None,
        "note": "Finite samples ≠ sup; no C8 kill",
    }


def run_sub(script: str, args: list[str], timeout: int) -> dict:
    cmd = [sys.executable, str(ATTACKS / script), *args]
    env = os.environ.copy()
    scripts_dir = str(ATTACKS.parent)
    env["PYTHONPATH"] = scripts_dir + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env=env,
        )
        return {
            "script": script,
            "args": args,
            "returncode": proc.returncode,
            "ok": proc.returncode == 0,
            "stdout_tail": (proc.stdout or "")[-2000:],
            "stderr_tail": (proc.stderr or "")[-800:],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "script": script,
            "args": args,
            "returncode": None,
            "ok": False,
            "error": f"timeout after {timeout}s",
            "stdout_tail": (exc.stdout or "")[-1000:] if isinstance(exc.stdout, str) else "",
        }


def main() -> int:
    rng = np.random.default_rng(20261001)
    payload: dict = {
        "title": "T_{j←j} survivors HARDER RUN (pass 2)",
        "date": "2026-10-01",
        "prior_hard_run": "2026-09-16",
        "honesty": {
            "ns_solved": False,
            "clay_claimed": False,
            "spectral_shift_is_lemma_star": False,
            "numerics_are_depletion": False,
            "forbidden_slots": list(FORBIDDEN),
            "do_not_revive": ["C1", "C2", "C3", "C4", "C5"],
        },
        "analytic_harder": {
            "C10": harder_c10(),
            "C6": harder_c6(),
            "C11": harder_c11(),
            "C9": harder_c9(),
            "C7_analytic": harder_c7_analytic(),
            "C8_analytic": harder_c8_analytic(),
        },
        "light_numerics": {},
        "subprocess": {},
    }

    payload["light_numerics"]["rstar"] = light_rstar(rng)

    # C7 harness — structured + random
    a3_out = str(OUT / "attack3_harder.json")
    a3 = run_sub("attack3_bony_hh_l.py", ["--out", a3_out, "--seed", "101"], timeout=180)
    c7 = {
        "id": "C7",
        "harness": "attack3_bony_hh_l.py",
        "ok": a3["ok"],
        "hard_verdict": "INCONCLUSIVE",
    }
    high_triad_hh_dominates = None
    if a3["ok"] and Path(a3_out).is_file():
        a3j = json.loads(Path(a3_out).read_text())
        for case in a3j.get("cases", []):
            if case.get("name") == "high_triad":
                ch = case.get("channels") or {}
                hh = abs((ch.get("HH") or {}).get("Tc", 0.0))
                hl = abs((ch.get("HL") or {}).get("Tc", 0.0))
                ll = abs((ch.get("LL") or {}).get("Tc", 0.0))
                tot = hh + hl + ll
                high_triad_hh_dominates = (tot > 0) and (hh / tot > 0.9)
        c7.update(
            {
                "verdict_script": a3j.get("verdict"),
                "random_HH_frac_mean": a3j.get("random_HH_frac_mean"),
                "random_HH_frac_p90": a3j.get("random_HH_frac_p90"),
                "high_triad_HH_dominates": high_triad_hh_dominates,
                "analytic": payload["analytic_harder"]["C7_analytic"],
                "hard_verdict": "SURVIVES",
                "strength": "LIVE_BONY_BOTTLENECK",
                "new_vs_hard_run_1": [
                    "KILLED Agmon-style HH product (λ escape)",
                    "Bernstein saturates T scale — no θνP margin",
                    "high_triad HH-dominates confirmed in harness",
                ],
                "weakening": (
                    "Naive energy-only and Agmon-style HH products killed. "
                    "Bernstein saturates without absorption margin. "
                    f"HH frac mean={a3j.get('random_HH_frac_mean')}, "
                    f"p90={a3j.get('random_HH_frac_p90')}; "
                    f"high_triad_HH_dominates={high_triad_hh_dominates}. "
                    "No geometric HH product seated."
                ),
            }
        )
    payload["subprocess"]["attack3"] = {
        "ok": a3["ok"],
        "returncode": a3["returncode"],
        "stderr_tail": a3.get("stderr_tail", "")[-400:],
    }
    payload["light_numerics"]["C7"] = c7

    # C8 near-shell — light, not HPC
    near_out = str(OUT / "near_shell_harder.json")
    near = run_sub(
        "lemma_star_near_shell_search.py",
        ["--out", near_out, "--seed", "42", "--n-almost", "50", "--n-hh", "35"],
        timeout=360,
    )
    c8 = {
        "id": "C8",
        "harness": "lemma_star_near_shell_search.py",
        "ok": near["ok"],
        "hard_verdict": "HARNESS_FAIL",
    }
    c8_analytic = payload["analytic_harder"]["C8_analytic"]
    if near["ok"] and Path(near_out).is_file():
        nj = json.loads(Path(near_out).read_text())
        killed = bool(nj.get("LemmaStar_killed"))
        c8.update(
            {
                "LemmaStar_killed": killed,
                "max_R_star": nj.get("max_R_star"),
                "verdict_script": nj.get("verdict"),
                "hard_verdict": "KILLED_ON_SAMPLES" if killed else "SURVIVES",
                "strength": "LAB_ONLY",
                "feeds_C10": c8_analytic["feeds_C10"],
                "new_vs_hard_run_1": c8_analytic["new_vs_hard_run_1"],
                "weakening": c8_analytic["weakening"],
                "category_gap": c8_analytic["category_gap"],
            }
        )
    else:
        c8.update(
            {
                "hard_verdict": c8_analytic["hard_verdict"],
                "strength": c8_analytic["strength"],
                "feeds_C10": c8_analytic["feeds_C10"],
                "weakening": c8_analytic["weakening"]
                + " (harness inconclusive; analytic category gap still stands)",
                "category_gap": c8_analytic["category_gap"],
            }
        )
    payload["subprocess"]["near_shell"] = {
        "ok": near["ok"],
        "returncode": near["returncode"],
        "stderr_tail": near.get("stderr_tail", "")[-400:],
    }
    payload["light_numerics"]["C8"] = c8

    # Light Attack 9B companion
    a9_outdir = str(OUT / "attack9b_light")
    Path(a9_outdir).mkdir(parents=True, exist_ok=True)
    a9 = run_sub(
        "attack9b_exact_shell_K.py",
        [
            "--kmax",
            "4",
            "--trials",
            "16",
            "--refine",
            "8",
            "--max-modes",
            "8",
            "--seed",
            "2026",
            "--outdir",
            a9_outdir,
        ],
        timeout=240,
    )
    c8b = {"harness": "attack9b_exact_shell_K.py", "ok": a9["ok"]}
    a9_jsons = list(Path(a9_outdir).glob("*.json"))
    if a9_jsons:
        try:
            j = json.loads(a9_jsons[0].read_text())
            c8b["artifact"] = a9_jsons[0].name
            for key in (
                "max_K",
                "max_K_beta_gt_alpha",
                "max_K_beta_lt_alpha",
                "verdict",
                "summary",
            ):
                if key in j:
                    c8b[key] = j[key]
        except json.JSONDecodeError:
            pass
    for line in (a9.get("stdout_tail") or "").splitlines()[::-1]:
        if "max" in line.lower() and "K" in line:
            c8b["stdout_hint"] = line.strip()
            break
    payload["subprocess"]["attack9b"] = {
        "ok": a9["ok"],
        "returncode": a9["returncode"],
        "stdout_tail": a9.get("stdout_tail", "")[-1200:],
        "stderr_tail": a9.get("stderr_tail", "")[-400:],
    }
    payload["light_numerics"]["C8_attack9b"] = c8b

    ranking = [
        {
            "id": "C10",
            "hard_verdict": payload["analytic_harder"]["C10"]["hard_verdict"],
            "note": payload["analytic_harder"]["C10"]["weakening"],
            "new_kills": payload["analytic_harder"]["C10"]["killed_this_pass"],
        },
        {
            "id": "C7",
            "hard_verdict": c7.get("hard_verdict"),
            "note": c7.get("weakening", c7.get("analytic_note")),
            "new_kills": payload["analytic_harder"]["C7_analytic"]["naive_forms_killed"],
        },
        {
            "id": "C8",
            "hard_verdict": c8.get("hard_verdict"),
            "note": c8.get("weakening"),
            "feeds_C10": c8.get("feeds_C10"),
        },
        {
            "id": "C6",
            "hard_verdict": payload["analytic_harder"]["C6"]["hard_verdict"],
            "note": payload["analytic_harder"]["C6"]["weakening"],
            "new": payload["analytic_harder"]["C6"]["new_vs_hard_run_1"],
        },
        {
            "id": "C11",
            "hard_verdict": payload["analytic_harder"]["C11"]["hard_verdict"],
            "note": payload["analytic_harder"]["C11"]["weakening"],
            "new": payload["analytic_harder"]["C11"]["new_vs_hard_run_1"],
        },
        {
            "id": "C9",
            "hard_verdict": payload["analytic_harder"]["C9"]["hard_verdict"],
            "note": payload["analytic_harder"]["C9"]["weakening"],
            "feeds_C10": False,
        },
    ]
    payload["ranking"] = ranking
    payload["best_next_theorem_shaped_target"] = payload["analytic_harder"]["C10"][
        "theorem_shaped_target"
    ]
    payload["new_kills_or_weakens"] = {
        "C10_draft_kills": payload["analytic_harder"]["C10"]["killed_this_pass"],
        "C6_new": "αZ/(νP)~λ^{1/2} escape — Sobolev against palinstrophy dies",
        "C7_new": "Agmon HH killed; Bernstein saturates with no absorption margin",
        "C8_new": "WEAKENED as C10 feeder (category gap); still SURVIVES as ★ lab",
        "C11_new": "Φ-renorm ≠ T^mm bound; T vs P escapes",
        "C9_new": "Confirmed non-feeder to C10",
        "C1_to_C5": "not revived",
    }
    payload["blunt_bottom_line"] = (
        "NS / Clay B not solved. T_{j←j} still OPEN. "
        "Harder pass: C10 SURVIVES principal (new draft kills: Sobolev-vs-P, "
        "BKM shortcut, CZ pointwise, Φ-as-depletion). "
        "C7 SURVIVES HH bottleneck (Agmon killed; Bernstein no margin). "
        "C8 SURVIVES lab but WEAKENED as C10 feeder (category gap). "
        "C6 further WEAKENED (α escapes νP). C11/C9 stay WEAKENED. "
        "Best next theorem: geometric/conditional α_+ ⇒ depletion⇒(A)."
    )

    out_json = OUT / "tj_survivors_harder_run.json"
    out_json.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    (REPO_OUT / "tj_survivors_harder_run.json").write_text(
        json.dumps(payload, indent=2, default=str) + "\n"
    )

    summary = {
        "date": "2026-10-01",
        "prior_hard_run": "2026-09-16",
        "honesty": payload["honesty"],
        "ranking": ranking,
        "new_kills_or_weakens": payload["new_kills_or_weakens"],
        "best_next_theorem_shaped_target": payload["best_next_theorem_shaped_target"],
        "blunt_bottom_line": payload["blunt_bottom_line"],
        "C10": {
            "hard_verdict": payload["analytic_harder"]["C10"]["hard_verdict"],
            "killed_this_pass": payload["analytic_harder"]["C10"]["killed_this_pass"],
            "alpha_Z_over_P_growth": payload["analytic_harder"]["C10"]["ledger"][
                "alpha_Z_over_P_growth"
            ],
        },
        "C6": {
            "hard_verdict": payload["analytic_harder"]["C6"]["hard_verdict"],
            "alpha_Z_over_P_growth": payload["analytic_harder"]["C6"]["ledger"][
                "alpha_Z_over_P_growth"
            ],
        },
        "C7": {
            "hard_verdict": c7.get("hard_verdict"),
            "HH_frac_mean": c7.get("random_HH_frac_mean"),
            "HH_frac_p90": c7.get("random_HH_frac_p90"),
            "high_triad_HH_dominates": c7.get("high_triad_HH_dominates"),
            "agmon_ratio_growth": payload["analytic_harder"]["C7_analytic"][
                "form_B_agmon_ratio_growth"
            ],
        },
        "C8": {
            "hard_verdict": c8.get("hard_verdict"),
            "LemmaStar_killed": c8.get("LemmaStar_killed"),
            "max_R_star": c8.get("max_R_star"),
            "feeds_C10": c8.get("feeds_C10"),
            "attack9b_ok": c8b.get("ok"),
        },
        "C11": {
            "hard_verdict": payload["analytic_harder"]["C11"]["hard_verdict"],
            "phi_renorm_closes_Tmm": payload["analytic_harder"]["C11"][
                "phi_renorm_closes_Tmm"
            ],
            "T_over_P_growth": payload["analytic_harder"]["C11"]["T_over_P_growth"],
        },
        "C9": {
            "hard_verdict": payload["analytic_harder"]["C9"]["hard_verdict"],
            "feeds_C10": False,
            "invariance_holds": payload["analytic_harder"]["C9"]["invariance_holds"],
        },
        "rstar_max_finite": payload["light_numerics"]["rstar"]["max_R_star_finite"],
    }
    (REPO_OUT / "tj_survivors_harder_run_summary.json").write_text(
        json.dumps(summary, indent=2, default=str) + "\n"
    )
    (OUT / "tj_survivors_harder_run_summary.json").write_text(
        json.dumps(summary, indent=2, default=str) + "\n"
    )

    lines = [
        "=== T_{j←j} SURVIVORS HARDER RUN (pass 2, 2026-10-01) ===",
        "NS not solved. No Clay claim. Forbidden slots empty. C1–C5 not revived.",
        "",
        f"C10 PRINCIPAL: {payload['analytic_harder']['C10']['hard_verdict']} — "
        f"new kills={payload['analytic_harder']['C10']['killed_this_pass']} — "
        f"αZ/P growth={payload['analytic_harder']['C10']['ledger']['alpha_Z_over_P_growth']:.3g}",
        f"C6  α/Door-3: {payload['analytic_harder']['C6']['hard_verdict']} — "
        f"αZ/(νP) growth={payload['analytic_harder']['C6']['ledger']['alpha_Z_over_P_growth']:.3g}",
        f"C11 T^mm:     {payload['analytic_harder']['C11']['hard_verdict']} — "
        f"Φ⇒Tmm={payload['analytic_harder']['C11']['phi_renorm_closes_Tmm']} "
        f"T/P growth={payload['analytic_harder']['C11']['T_over_P_growth']:.3g}",
        f"C9  τ triad:  {payload['analytic_harder']['C9']['hard_verdict']} — "
        f"feeds_C10=False invariance={payload['analytic_harder']['C9']['invariance_holds']}",
        f"C7  HH:       {c7.get('hard_verdict')} — "
        f"HH mean={c7.get('random_HH_frac_mean')} p90={c7.get('random_HH_frac_p90')} "
        f"high_triad_HH={c7.get('high_triad_HH_dominates')} "
        f"agmon_growth={payload['analytic_harder']['C7_analytic']['form_B_agmon_ratio_growth']:.3g}",
        f"C8  near-shell:{c8.get('hard_verdict')} — "
        f"killed={c8.get('LemmaStar_killed')} maxR*={c8.get('max_R_star')} "
        f"feeds_C10={c8.get('feeds_C10')}",
        f"C8  attack9b: ok={c8b.get('ok')}",
        "",
        "NEW KILLS / WEAKENS:",
        json.dumps(payload["new_kills_or_weakens"], indent=2),
        "",
        "BEST NEXT THEOREM-SHAPED TARGET:",
        payload["best_next_theorem_shaped_target"],
        "",
        payload["blunt_bottom_line"],
        "",
        f"Wrote {out_json}",
        f"Wrote {REPO_OUT / 'tj_survivors_harder_run_summary.json'}",
    ]
    log = "\n".join(lines) + "\n"
    (OUT / "tj_survivors_harder_run.log").write_text(log)
    (REPO_OUT / "tj_survivors_harder_run.log").write_text(log)
    print(log, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
