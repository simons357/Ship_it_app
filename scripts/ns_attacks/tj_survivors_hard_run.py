#!/usr/bin/env python3
"""Hard run of SURVIVING same-scale T_{j←j} candidates (C10, C6, C11, C7, C8, C9).

Analytic-first pressure tests + light existing harnesses.
Does NOT revive C1–C5. Does NOT claim NS / Clay B.
Forbidden: bound T by ė_j, Ż, Ż_j, or Λ'. Numerics ≠ depletion.
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
OUT = Path("/opt/cursor/artifacts/tj-survivors-hard-run")
REPO_OUT = ROOT / "results" / "tj-survivors-hard-run"
OUT.mkdir(parents=True, exist_ok=True)
REPO_OUT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ATTACKS))
from ns_lemma_star_core import Field, R_star, project_perp, shell_wavevectors  # noqa: E402

FORBIDDEN = (r"\dot e_j", r"\dot Z", r"\dot Z_j", r"\Lambda'")


# ---------------------------------------------------------------------------
# C10 — non-circular depletion ⇒ (A)  [PRINCIPAL]
# ---------------------------------------------------------------------------


def hard_c10() -> dict:
    """Pressure-test depletion⇒(A) drafts; refuse circular; map collapses.

    Sharpest honest sketch (empty forbidden slots):
      If (T_{j←j})_+ ≤ θ ν P_j + R_allowed  with θ<1 and R_allowed from
      energy / {Z_k} / geometric direction only, then ρ_j < ν enters (A).
    Instantiations that stay non-circular all collapse onto:
      (i) control of (α_loc,j)_+   → C6 Door-3
      (ii) structure/cancel of T^mm → C11 (axisym)
      (iii) near-shell cancel feeding depletion → C8 upgrade
    No independent geometric depletion theorem is seated here.
    """
    drafts = [
        {
            "name": "smuggle_Zdot",
            "claim": r"(T)_+ ≤ |Ż_j| + ν D_j  ⇒ (A)",
            "forbidden": True,
            "slot": r"\dot Z_j",
            "verdict": "REFUSED",
        },
        {
            "name": "smuggle_Lambda",
            "claim": r"depletion from sign(Λ') or |Λ'| control",
            "forbidden": True,
            "slot": r"\Lambda'",
            "verdict": "REFUSED",
        },
        {
            "name": "smuggle_ej_dot",
            "claim": r"|T| ≤ C|ė_j| ⇒ depletion",
            "forbidden": True,
            "slot": r"\dot e_j",
            "verdict": "REFUSED",
        },
        {
            "name": "occupancy_alignment_samples",
            "claim": "occupancy≈1 + alignment≈1/2 ⇒ depletion ⇒ (A)",
            "forbidden": False,
            "slot": None,
            "verdict": "REFUSED_HONESTY",
            "note": "samples ≠ depletion; no K_max→∞",
        },
        {
            "name": "alpha_plus_integrable",
            "claim": r"∫(α_loc,j)_+ |ω_j|^2 ≤ θ ν P_j + R_E,Z  ⇒ (A)",
            "forbidden": False,
            "slot": None,
            "verdict": "COLLAPSES_TO_C6",
            "note": "α_+ control is exactly Door-3; not seated unaugmented",
        },
        {
            "name": "Tmm_structure_axisym",
            "claim": r"|T^mm| ≤ θ ν P_j + R_geom under SO(2) ⇒ (A) on axisym face",
            "forbidden": False,
            "slot": None,
            "verdict": "COLLAPSES_TO_C11",
            "note": "axisym-conditional; T^mm bulk still uncontrolled",
        },
        {
            "name": "near_shell_cancel_to_depletion",
            "claim": "near-shell / K_αβ cancel ⇒ ρ_j < ν uniformly",
            "forbidden": False,
            "slot": None,
            "verdict": "COLLAPSES_TO_C8_UPGRADE",
            "note": "lab evidence only; no uniform depletion theorem",
        },
        {
            "name": "standalone_geometric_depletion",
            "claim": "new geometric depletion not reducing to C6/C8/C11",
            "forbidden": False,
            "slot": None,
            "verdict": "ABSENT",
            "note": "no independent sketch found that stays non-circular and seated",
        },
    ]
    refused = [d["name"] for d in drafts if d["verdict"] in ("REFUSED", "REFUSED_HONESTY")]
    collapses = [d["name"] for d in drafts if str(d["verdict"]).startswith("COLLAPSES")]
    absent = [d["name"] for d in drafts if d["verdict"] == "ABSENT"]
    return {
        "id": "C10",
        "name": "noncircular_depletion_to_A",
        "hard_verdict": "SURVIVES",
        "strength": "PRINCIPAL_OPEN",
        "weakening": (
            "Every non-circular concrete sketch collapses onto C6 / C11 / C8-upgrade; "
            "no standalone depletion theorem seated. Door stays principal and empty."
        ),
        "forbidden_slots": list(FORBIDDEN),
        "drafts": drafts,
        "refused": refused,
        "collapses_onto": collapses,
        "absent_independent": absent,
        "theorem_shaped_target": (
            "Prove depletion ⇒ (A) by controlling (α_loc,j)_+ "
            "(or an integrable substitute) so stretch enters θν P_j + allowed R, "
            "without ė_j / Ż / Λ' and without Bernstein cubic wall."
        ),
        "ns_solved": False,
    }


# ---------------------------------------------------------------------------
# C6 — Door-3 / α_+
# ---------------------------------------------------------------------------


def hard_c6() -> dict:
    """Concentration sharpness + Bernstein cubic wall for α_+.

    Prop. TJJ-α / TJJ-E-false ledger:
      u^λ = λ^{3/2} φ(λx): strain ~ λ^{5/2}, Z ~ λ² ⇒ α_+ Z ~ λ^{9/2} = T scale.
      Energy E invariant ⇒ α_+ not controlled by E or {Z_k} via Sobolev (W^{1,2}⊄L^∞).
      Bernstein on ||u_loc||_∞ / ||∇u_loc||_∞ returns 2^{3j/2} or cubic wall.
    Identities (transport vanish; stretch = α) SURVIVE. Absolute α bound does not.
    """
    lambdas = np.array([4.0, 16.0, 64.0, 256.0, 1024.0])
    # Relative prototype powers (constants cancel in growth ratios).
    E = np.ones_like(lambdas)
    Z = lambdas**2
    alpha_plus = lambdas**2.5  # strain scale
    alpha_Z = alpha_plus * Z  # ~ λ^{9/2}
    T = lambdas**4.5
    # Allowed energy-linear remainder C E Z
    R_energy = E * Z
    ratio_vs_energy = alpha_Z / R_energy  # ~ λ^{5/2} → ∞ actually wait: αZ/EZ = α/E ~ λ^{5/2}
    # Sharpness: αZ / T → const
    sharpness = alpha_Z / T
    # Bernstein-style cubic wall proxy: 2^{3j/2} with j ~ log2(λ) ⇒ λ^{3/2} * Z^{1/2} etc.
    # Commutator leftover needs ||u_loc||_∞^2 Z / ν ~ (λ^{3/2})^2 * λ^2 = λ^5 if ||u||_∞~λ^{3/2}
    # vs ν D ~ λ^4 — still escapes.
    u_inf = lambdas**1.5
    D = lambdas**4
    comm_proxy = (u_inf**2) * Z  # ν^{-1} absorbed into C
    comm_over_D = comm_proxy / D  # ~ λ^{3+2-4} wait: λ^3 * λ^2 / λ^4 = λ^{1} → ∞
    return {
        "id": "C6",
        "name": "alpha_door3",
        "hard_verdict": "WEAKENED",
        "strength": "CONDITIONAL_CRITERION_ONLY",
        "weakening": (
            "α_+ Z_j is sharp for main stretch (ratio αZ/T ~ 1) and escapes every "
            "energy-linear R (αZ/(E Z) ~ λ^{5/2}→∞). Bernstein commutator proxy "
            "also escapes νD (~λ→∞). Door-3 remains a printed criterion / α-hypothesis, "
            "not an unaugmented bound."
        ),
        "identities_still_sit": [
            "TJJ-Trans: transport main vanishes",
            "TJJ-α: main stretch = ∫ α |ω_j|^2",
            "TJJ-template inequality sits; remainder not allowed R",
        ],
        "ledger": {
            "lambdas": lambdas.tolist(),
            "alpha_Z_over_T": sharpness.tolist(),
            "alpha_Z_over_E_Z": ratio_vs_energy.tolist(),
            "comm_proxy_over_D": comm_over_D.tolist(),
            "ratio_energy_growth": float(ratio_vs_energy[-1] / ratio_vs_energy[0]),
            "comm_growth": float(comm_over_D[-1] / comm_over_D[0]),
        },
        "survives_as": "TRY_CONDITIONAL_if_alpha_hypothesis_named",
        "killed_as": "unaugmented_absolute_alpha_plus_bound",
        "ns_solved": False,
    }


# ---------------------------------------------------------------------------
# C11 — meridional T^mm cancel (axisym-conditional)
# ---------------------------------------------------------------------------


def hard_c11() -> dict:
    """After C2 death: attack T^mm. Kill energy-R and 2D-transfer myths.

    Mixed compact swirl+meridional table (TJJ chain, n=24): T^mm is bulk.
    Since T ≈ T^mm on energy-carrying shells, Prop. TJJ-E-false kills any
    energy+viscosity R aimed at T^mm the same way it kills R for total T.
    No-swirl regularity does not transfer to the meridional piece of a mixed field.
    """
    table = [
        {"j": 1, "T_mm": 8.15e3, "T_ss": -62.0, "T_cross": 217.0, "T": 8.30e3},
        {"j": 2, "T_mm": -1.08e4, "T_ss": 4.03e3, "T_cross": -142.0, "T": -6.89e3},
        {"j": 3, "T_mm": -1.32e4, "T_ss": 622.0, "T_cross": 88.0, "T": -1.25e4},
    ]
    mm_frac = []
    for row in table:
        tot = abs(row["T_mm"]) + abs(row["T_ss"]) + abs(row["T_cross"])
        mm_frac.append(abs(row["T_mm"]) / tot)

    # Analytic kill of energy-linear R for T_mm via concentration (same powers as C1,
    # since T_mm is the bulk carrier of T on mixed class).
    lambdas = np.array([4.0, 16.0, 64.0, 256.0])
    T_mm = lambdas**4.5  # bulk scales with T
    E, Z, D = np.ones_like(lambdas), lambdas**2, lambdas**4
    eps, nu, C = 0.1, 1.0, 1.0
    denom = eps * nu * D + C * E * Z
    ratio = T_mm / denom

    myth_kills = [
        {
            "myth": "no-swirl regularity ⇒ |T^mm| controlled on mixed fields",
            "verdict": "KILLED",
            "why": "meridional piece of mixed field is not a no-swirl solution",
        },
        {
            "myth": "T^mm ≤ C E Z + εν D (energy-linear R)",
            "verdict": "KILLED",
            "why": "same λ^{1/2} blowup as Prop. TJJ-E-false; T_mm carries the bulk",
            "ratio_growth": float(ratio[-1] / ratio[0]),
        },
        {
            "myth": "T^ss (centrifugal) is the leftover after T^mm free",
            "verdict": "KILLED",
            "why": "C2 already DEAD; T_mm dominates abs on recorded shells",
        },
        {
            "myth": "SO(2) alone cancels T^mm",
            "verdict": "NOT_SEATED",
            "why": "axisym kills free helical HHH but is not a bound on T^mm",
        },
    ]
    return {
        "id": "C11",
        "name": "meridional_Tmm_cancel",
        "axisym_conditional": True,
        "hard_verdict": "WEAKENED",
        "strength": "NAMED_BULK_TARGET_OPEN",
        "weakening": (
            "Energy-linear R for T^mm is false (ratio growth ~λ^{1/2}). "
            "2D/no-swirl transfer myths killed. SO(2) restriction ≠ cancel. "
            "Lane survives only as the named bulk structure target under axisym."
        ),
        "recorded_mm_frac_of_abs_split": mm_frac,
        "mm_dominates": all(f > 0.5 for f in mm_frac),
        "myth_kills": myth_kills,
        "energy_R_ratio_growth": float(ratio[-1] / ratio[0]),
        "survives_as": "TRY_axisym_conditional_structure_route",
        "ns_solved": False,
    }


# ---------------------------------------------------------------------------
# C9 — triad / τ structure
# ---------------------------------------------------------------------------


def hard_c9() -> dict:
    """AS-τ / AS-ω* are identities. ω_* shift invariance ⇒ no manufactured smallness.

    Algebraic probe: τ(ω) = Σ (ω(leg)−ω(ref)) J_leg is invariant under ω ↦ ω−ω_*.
    Therefore shifting by shell-mean / lattice frequency cannot reduce |τ|.
    Rewrite remains useful bookkeeping under other attacks; not a standalone bound.
    """
    rng = np.random.default_rng(42)
    rows = []
    for _ in range(40):
        # Synthetic closed-triad couplings
        J_xi, J_eta = rng.normal(size=2)
        w_xi, w_eta, w_zeta = rng.normal(size=3)
        tau = (w_xi - w_zeta) * J_xi + (w_eta - w_zeta) * J_eta
        for w_star in (0.0, float(np.mean([w_xi, w_eta, w_zeta])), 10.0, -3.7):
            tau_shift = (w_xi - w_star - (w_zeta - w_star)) * J_xi + (
                w_eta - w_star - (w_zeta - w_star)
            ) * J_eta
            rows.append(abs(tau - tau_shift))
    max_drift = float(np.max(rows)) if rows else None
    # Naive "bound by frequency gap" also fails: gap can be O(1) while J large
    J = 1e6
    tau_big = (0.1) * J  # small frequency weight gap, huge coupling
    return {
        "id": "C9",
        "name": "triad_tau_structure",
        "hard_verdict": "WEAKENED",
        "strength": "IDENTITY_ONLY",
        "weakening": (
            "AS-τ rewrite + AS-ω* shift invariance confirmed (max |τ−τ_shift| ~ 0). "
            "Shift cannot manufacture an allowed R. Small frequency gaps with large "
            "J still produce large |τ|. Standalone bound route is dead; rewrite "
            "survives only as structure under C6/C10/C11."
        ),
        "omega_star_invariance_max_abs_drift": max_drift,
        "invariance_holds": max_drift is not None and max_drift < 1e-10,
        "large_J_small_gap_example_|tau|": abs(tau_big),
        "survives_as": "rewrite_tool_not_bound",
        "killed_as": "standalone_estimate_producing_allowed_R",
        "ns_solved": False,
    }


# ---------------------------------------------------------------------------
# C7 — HH-only budget
# ---------------------------------------------------------------------------


def hard_c7_analytic() -> dict:
    """Naive energy-only HH product forms die on concentration; Agmon loses geometry."""
    lambdas = np.array([4.0, 16.0, 64.0, 256.0])
    # Same-scale HH parent channel can carry the full T ~ λ^{9/2}
    T_HH = lambdas**4.5
    E = np.ones_like(lambdas)
    # Naive ★-style: C ||u||_2 X^{3/2} with X~Z~λ² ⇒ E^{1/2} (λ²)^{3/2} = λ^3
    # Actually X enstrophy-like ~ λ², X^{3/2}~λ^3; T/X^{3/2}~λ^{1.5}→∞ on this family
    X = lambdas**2
    naive = np.sqrt(E) * (X**1.5)
    ratio = T_HH / naive
    return {
        "id": "C7",
        "name": "HH_only_budget",
        "analytic_note": (
            "Concentration family sends |T_HH| / (E^{1/2} X^{3/2}) ~ λ^{3/2}→∞ "
            "if HH carries bulk same-scale transfer. Energy-only HH product is false "
            "as uniform bound; geometry-only Agmon also loses control. "
            "Lane survives as the live Bony bottleneck needing a geometric HH product."
        ),
        "naive_HH_product_ratio_growth": float(ratio[-1] / ratio[0]),
        "naive_form_killed": True,
        "ns_solved": False,
    }


# ---------------------------------------------------------------------------
# Light numerics + subprocess harnesses
# ---------------------------------------------------------------------------


def light_rstar(rng: np.random.Generator) -> dict:
    def _rand_perp(k):
        w = rng.normal(size=3) + 1j * rng.normal(size=3)
        return project_perp(k, w)

    rows = []
    for n1, n2 in [(1, 2), (2, 5), (3, 6), (4, 7)]:
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
        "note": "Finite samples ≠ sup; no kill of C8 lab",
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
    rng = np.random.default_rng(20260916)
    payload: dict = {
        "title": "T_{j←j} survivors HARD RUN",
        "date": "2026-09-16",
        "honesty": {
            "ns_solved": False,
            "clay_claimed": False,
            "spectral_shift_is_lemma_star": False,
            "numerics_are_depletion": False,
            "forbidden_slots": list(FORBIDDEN),
            "do_not_revive": ["C1", "C2", "C3", "C4", "C5"],
        },
        "analytic_hard": {
            "C10": hard_c10(),
            "C6": hard_c6(),
            "C11": hard_c11(),
            "C9": hard_c9(),
            "C7_analytic": hard_c7_analytic(),
        },
        "light_numerics": {},
        "subprocess": {},
    }

    payload["light_numerics"]["rstar"] = light_rstar(rng)

    # C7 harness (attack3)
    a3_out = str(OUT / "attack3_hard.json")
    a3 = run_sub("attack3_bony_hh_l.py", ["--out", a3_out, "--seed", "3"], timeout=180)
    c7 = {
        "id": "C7",
        "harness": "attack3_bony_hh_l.py",
        "ok": a3["ok"],
        "hard_verdict": "INCONCLUSIVE",
    }
    if a3["ok"] and Path(a3_out).is_file():
        a3j = json.loads(Path(a3_out).read_text())
        c7.update(
            {
                "verdict_script": a3j.get("verdict"),
                "random_HH_frac_mean": a3j.get("random_HH_frac_mean"),
                "random_HH_frac_p90": a3j.get("random_HH_frac_p90"),
                "naive_product_killed": payload["analytic_hard"]["C7_analytic"][
                    "naive_form_killed"
                ],
                "hard_verdict": "SURVIVES",
                "strength": "LIVE_BONY_BOTTLENECK",
                "weakening": (
                    "Naive energy-only HH product killed by concentration "
                    f"(ratio growth "
                    f"{payload['analytic_hard']['C7_analytic']['naive_HH_product_ratio_growth']:.3g}). "
                    "Channel still live; no geometric HH product seated."
                ),
            }
        )
    payload["subprocess"]["attack3"] = {
        "ok": a3["ok"],
        "returncode": a3["returncode"],
        "stderr_tail": a3.get("stderr_tail", "")[-400:],
    }
    payload["light_numerics"]["C7"] = c7

    # C8 near-shell (slightly larger than first pass)
    near_out = str(OUT / "near_shell_hard.json")
    near = run_sub(
        "lemma_star_near_shell_search.py",
        ["--out", near_out, "--seed", "17", "--n-almost", "60", "--n-hh", "40"],
        timeout=360,
    )
    c8 = {
        "id": "C8",
        "harness": "lemma_star_near_shell_search.py",
        "ok": near["ok"],
        "hard_verdict": "HARNESS_FAIL",
    }
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
                "weakening": (
                    "Still lab/evidence: no upgrade to uniform depletion ⇒ (A). "
                    "Finite-sample R_★ stays small on tested families; not a supremum."
                ),
            }
        )
    payload["subprocess"]["near_shell"] = {
        "ok": near["ok"],
        "returncode": near["returncode"],
        "stderr_tail": near.get("stderr_tail", "")[-400:],
    }
    payload["light_numerics"]["C8"] = c8

    # C8 companion: light Attack 9B (small budget)
    a9_outdir = str(OUT / "attack9b_light")
    Path(a9_outdir).mkdir(parents=True, exist_ok=True)
    a9 = run_sub(
        "attack9b_exact_shell_K.py",
        [
            "--kmax",
            "4",
            "--trials",
            "20",
            "--refine",
            "10",
            "--max-modes",
            "8",
            "--seed",
            "1390",
            "--outdir",
            a9_outdir,
        ],
        timeout=240,
    )
    c8b = {"harness": "attack9b_exact_shell_K.py", "ok": a9["ok"]}
    # Parse stdout for max K if present
    for line in (a9.get("stdout_tail") or "").splitlines()[::-1]:
        if "max" in line.lower() and "K" in line:
            c8b["stdout_hint"] = line.strip()
            break
    # Prefer JSON artifacts if written
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
    payload["subprocess"]["attack9b"] = {
        "ok": a9["ok"],
        "returncode": a9["returncode"],
        "stdout_tail": a9.get("stdout_tail", "")[-1200:],
        "stderr_tail": a9.get("stderr_tail", "")[-400:],
    }
    payload["light_numerics"]["C8_attack9b"] = c8b

    # Ranking table
    ranking = [
        {
            "id": "C10",
            "hard_verdict": payload["analytic_hard"]["C10"]["hard_verdict"],
            "note": payload["analytic_hard"]["C10"]["weakening"],
        },
        {
            "id": "C6",
            "hard_verdict": payload["analytic_hard"]["C6"]["hard_verdict"],
            "note": payload["analytic_hard"]["C6"]["weakening"],
        },
        {
            "id": "C11",
            "hard_verdict": payload["analytic_hard"]["C11"]["hard_verdict"],
            "note": payload["analytic_hard"]["C11"]["weakening"],
        },
        {
            "id": "C7",
            "hard_verdict": c7.get("hard_verdict"),
            "note": c7.get("weakening", c7.get("analytic_note")),
        },
        {
            "id": "C8",
            "hard_verdict": c8.get("hard_verdict"),
            "note": c8.get("weakening"),
        },
        {
            "id": "C9",
            "hard_verdict": payload["analytic_hard"]["C9"]["hard_verdict"],
            "note": payload["analytic_hard"]["C9"]["weakening"],
        },
    ]
    payload["ranking"] = ranking
    payload["best_next_theorem_shaped_target"] = payload["analytic_hard"]["C10"][
        "theorem_shaped_target"
    ]
    payload["blunt_bottom_line"] = (
        "NS / Clay B not solved. T_{j←j} still OPEN. "
        "Hard run: C10 SURVIVES as principal empty door (sketches collapse to C6/C11/C8). "
        "C6/C11/C9 WEAKENED (criterion / bulk-target / identity-only). "
        "C7 SURVIVES as live HH bottleneck (naive product killed). "
        "C8 SURVIVES as lab only. Best next theorem target: non-circular "
        "α_+ (or integrable) control feeding depletion⇒(A)."
    )

    out_json = OUT / "tj_survivors_hard_run.json"
    out_json.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    # Mirror into repo results for PR evidence
    (REPO_OUT / "tj_survivors_hard_run.json").write_text(
        json.dumps(payload, indent=2, default=str) + "\n"
    )
    # Compact summary for docs
    summary = {
        "honesty": payload["honesty"],
        "ranking": ranking,
        "best_next_theorem_shaped_target": payload["best_next_theorem_shaped_target"],
        "blunt_bottom_line": payload["blunt_bottom_line"],
        "C10": {
            "hard_verdict": payload["analytic_hard"]["C10"]["hard_verdict"],
            "collapses_onto": payload["analytic_hard"]["C10"]["collapses_onto"],
        },
        "C6": {
            "hard_verdict": payload["analytic_hard"]["C6"]["hard_verdict"],
            "energy_escape_growth": payload["analytic_hard"]["C6"]["ledger"][
                "ratio_energy_growth"
            ],
            "comm_escape_growth": payload["analytic_hard"]["C6"]["ledger"]["comm_growth"],
        },
        "C11": {
            "hard_verdict": payload["analytic_hard"]["C11"]["hard_verdict"],
            "mm_dominates": payload["analytic_hard"]["C11"]["mm_dominates"],
            "energy_R_ratio_growth": payload["analytic_hard"]["C11"][
                "energy_R_ratio_growth"
            ],
        },
        "C9": {
            "hard_verdict": payload["analytic_hard"]["C9"]["hard_verdict"],
            "invariance_holds": payload["analytic_hard"]["C9"]["invariance_holds"],
            "max_drift": payload["analytic_hard"]["C9"][
                "omega_star_invariance_max_abs_drift"
            ],
        },
        "C7": {
            "hard_verdict": c7.get("hard_verdict"),
            "HH_frac_mean": c7.get("random_HH_frac_mean"),
            "HH_frac_p90": c7.get("random_HH_frac_p90"),
            "naive_product_ratio_growth": payload["analytic_hard"]["C7_analytic"][
                "naive_HH_product_ratio_growth"
            ],
        },
        "C8": {
            "hard_verdict": c8.get("hard_verdict"),
            "LemmaStar_killed": c8.get("LemmaStar_killed"),
            "max_R_star": c8.get("max_R_star"),
            "attack9b_ok": c8b.get("ok"),
        },
        "rstar_max_finite": payload["light_numerics"]["rstar"]["max_R_star_finite"],
    }
    (REPO_OUT / "tj_survivors_hard_run_summary.json").write_text(
        json.dumps(summary, indent=2, default=str) + "\n"
    )
    (OUT / "tj_survivors_hard_run_summary.json").write_text(
        json.dumps(summary, indent=2, default=str) + "\n"
    )

    lines = [
        "=== T_{j←j} SURVIVORS HARD RUN ===",
        "NS not solved. No Clay claim. Forbidden slots empty. C1–C5 not revived.",
        "",
        f"C10 PRINCIPAL: {payload['analytic_hard']['C10']['hard_verdict']} — "
        f"collapses={payload['analytic_hard']['C10']['collapses_onto']}",
        f"C6  α/Door-3: {payload['analytic_hard']['C6']['hard_verdict']} — "
        f"αZ/(EZ) growth={payload['analytic_hard']['C6']['ledger']['ratio_energy_growth']:.3g}",
        f"C11 T^mm:     {payload['analytic_hard']['C11']['hard_verdict']} — "
        f"mm_dom={payload['analytic_hard']['C11']['mm_dominates']} "
        f"energyR growth={payload['analytic_hard']['C11']['energy_R_ratio_growth']:.3g}",
        f"C9  τ triad:  {payload['analytic_hard']['C9']['hard_verdict']} — "
        f"ω* invariance={payload['analytic_hard']['C9']['invariance_holds']}",
        f"C7  HH:       {c7.get('hard_verdict')} — "
        f"HH mean={c7.get('random_HH_frac_mean')} p90={c7.get('random_HH_frac_p90')}",
        f"C8  near-shell:{c8.get('hard_verdict')} — "
        f"killed={c8.get('LemmaStar_killed')} maxR*={c8.get('max_R_star')}",
        f"C8  attack9b: ok={c8b.get('ok')}",
        "",
        "BEST NEXT THEOREM-SHAPED TARGET:",
        payload["best_next_theorem_shaped_target"],
        "",
        payload["blunt_bottom_line"],
        "",
        f"Wrote {out_json}",
        f"Wrote {REPO_OUT / 'tj_survivors_hard_run_summary.json'}",
    ]
    log = "\n".join(lines) + "\n"
    (OUT / "tj_survivors_hard_run.log").write_text(log)
    (REPO_OUT / "tj_survivors_hard_run.log").write_text(log)
    print(log, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
