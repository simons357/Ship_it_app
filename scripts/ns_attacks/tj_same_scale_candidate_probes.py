#!/usr/bin/env python3
"""Same-scale T_{j←j} candidate probes — analytic-first, light numerics.

Narrow-first filter for Jonathan's remainder door:
  - confirm known DEAD routes (energy-linear R; circular Gronwall; numerics≠depletion)
  - keep TRY survivors (α/Door-3, HH budget, near-shell lab, triad structure, depletion⇒(A))
  - run cheap product / HH / near-shell harnesses already in scripts/ns_attacks/

Does NOT prove T_{j←j} control. Does NOT claim NS / Clay B.
Spectral-shift ≠ Lemma★. Forbidden: bound T by ė_j, Ż, Ż_j, or Λ'.
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
OUT = Path("/opt/cursor/artifacts/tj-same-scale-candidates")
OUT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ATTACKS))
from ns_lemma_star_core import Field, R_star, project_perp, shell_wavevectors  # noqa: E402


FORBIDDEN_SLOTS = (r"\dot e_j", r"\dot Z", r"\dot Z_j", r"\Lambda'")


def analytic_concentration_kill() -> dict:
    """Prop. TJJ-E-false scaling ledger (analytic).

    u^λ = λ^{3/2} φ(λ x): energy invariant; occupied shell j ~ log₂ λ;
    Z ~ λ², D ~ λ⁴, T ~ λ^{9/2}. Ratio vs energy+viscosity R ~ λ^{1/2} → ∞.
    """
    lambdas = np.array([4.0, 16.0, 64.0, 256.0])
    # Prototype powers (relative); overall constants cancel in the ratio growth.
    Z = lambdas**2
    D = lambdas**4
    T = lambdas**4.5
    E = np.ones_like(lambdas)  # energy invariant under this scaling
    eps, nu, C = 0.1, 1.0, 1.0
    denom = eps * nu * D + C * E * Z
    ratio = T / denom
    growth = float(ratio[-1] / ratio[0])
    return {
        "candidate": "C1_energy_visc_R",
        "verdict": "DEAD",
        "lambdas": lambdas.tolist(),
        "ratio": ratio.tolist(),
        "ratio_growth_last_over_first": growth,
        "note": "ratio ~ λ^{1/2} → ∞; energy-linear R is false as a uniform bound",
    }


def refuse_circular_slots() -> dict:
    """C3: any bound that uses forbidden time/spectral-shift slots dies."""
    drafts = [
        {
            "name": "bound_by_Zdot",
            "text": r"|T_{j←j}| ≤ |Ż_j| + ν D_j",
            "uses_forbidden": True,
            "slot": r"\dot Z_j",
        },
        {
            "name": "bound_by_Lambda_prime",
            "text": r"|T_{j←j}| ≤ C X |Λ'| + ν D_j",
            "uses_forbidden": True,
            "slot": r"\Lambda'",
        },
        {
            "name": "bound_by_ej_dot",
            "text": r"|T_{j←j}| ≤ C |ė_j|",
            "uses_forbidden": True,
            "slot": r"\dot e_j",
        },
        {
            "name": "honest_alpha_template",
            "text": r"T ≤ εν D_j + ||(α)_+||_∞ Z_j + commutator R (not seated)",
            "uses_forbidden": False,
            "slot": None,
        },
    ]
    refused = [d["name"] for d in drafts if d["uses_forbidden"]]
    survivors = [d["name"] for d in drafts if not d["uses_forbidden"]]
    return {
        "candidate": "C3_circular_gronwall",
        "verdict": "DEAD",
        "forbidden_slots": list(FORBIDDEN_SLOTS),
        "drafts": drafts,
        "refused": refused,
        "non_circular_templates_seen": survivors,
        "note": "Forbidden slots stay out; honest α-template is TRY not a close",
    }


def occupancy_not_depletion() -> dict:
    return {
        "candidate": "C4_occupancy_alignment",
        "verdict": "DEAD",
        "observed_sample_claim": "occupancy ≈ 1 with alignment ≈ 1/2",
        "implies_depletion_for_A": False,
        "note": "Honesty card: samples ≠ depletion ≠ (A)",
    }


def pure_swirl_blocked() -> dict:
    return {
        "candidate": "C5_pure_swirl_class_bound",
        "verdict": "BLOCKED",
        "sits": "Prop. TJJ-pure: pure swirl pairing vanishes",
        "does_not_upgrade": "mixed swirl+meridional (T_mm bulk)",
        "note": "Subclass check only",
    }


def centrifugal_only_dead() -> dict:
    # Recorded mixed-sample table from docs/TJJ-ESTIMATE.md (n=24 compact blob).
    table = [
        {"j": 1, "T_mm": 8.15e3, "T_ss": -62.0, "T_cross": 217.0, "T": 8.30e3},
        {"j": 2, "T_mm": -1.08e4, "T_ss": 4.03e3, "T_cross": -142.0, "T": -6.89e3},
        {"j": 3, "T_mm": -1.32e4, "T_ss": 622.0, "T_cross": 88.0, "T": -1.25e4},
    ]
    mm_bulk = []
    for row in table:
        abs_mm = abs(row["T_mm"])
        abs_ss = abs(row["T_ss"])
        mm_bulk.append(abs_mm > abs_ss)
    return {
        "candidate": "C2_centrifugal_only_leftover",
        "verdict": "DEAD",
        "axisym_conditional": True,
        "recorded_table": table,
        "T_mm_dominates_abs": all(mm_bulk),
        "note": "Centrifugal-only leftover false; T_mm is the bulk on mixed samples",
    }


def survivors_status() -> list[dict]:
    return [
        {
            "candidate": "C6_alpha_door3",
            "verdict": "TRY",
            "why": "Main stretch is α; transport main vanishes; α_+ control open",
            "kill": "α_+ escapes every allowed R while identities hold, or α-hypothesis closes conditionally",
        },
        {
            "candidate": "C7_HH_only_budget",
            "verdict": "TRY",
            "why": "HH channel is the live Bony bottleneck in attack3",
            "kill": "No geometric HH product; or proposed HH form killed by a family",
        },
        {
            "candidate": "C8_near_shell_cancellation",
            "verdict": "TRY",
            "why": "Attack 9B / near-shell lab; finite K_αβ on tested families",
            "kill": "Uniform shell statement fails; or K→∞ along a named family",
        },
        {
            "candidate": "C9_triad_structure",
            "verdict": "TRY",
            "why": "Closed-triad τ / ω_* rewrite seated as identity in AXISYM-SHELL",
            "kill": "Rewrite never produces an allowed R",
        },
        {
            "candidate": "C10_noncircular_depletion_to_A",
            "verdict": "TRY",
            "why": "Principal honest Step-6 route on UNAUG lock card",
            "kill": "Any draft that reintroduces ė_j / Ż / Λ' as the controlling quantity",
        },
        {
            "candidate": "C11_meridional_Tmm_cancel",
            "verdict": "TRY",
            "axisym_conditional": True,
            "why": "After C2 death, T_mm is the named bulk target under SO(2)",
            "kill": "T_mm saturates every proposed geometric R on mixed blobs",
        },
        {
            "candidate": "C12_SND_conditional",
            "verdict": "TRY_CONDITIONAL_ONLY",
            "why": "Optional shell-concentration texture; must stay labeled conditional",
            "kill": "Sold as unaugmented Clay, or SND fails on a named family",
        },
    ]


def light_rstar_ceilings(rng: np.random.Generator) -> dict:
    """Tiny product / R_★ ceiling sample (not a supremum)."""

    def _rand_perp(k):
        w = rng.normal(size=3) + 1j * rng.normal(size=3)
        return project_perp(k, w)

    rows = []
    for n1, n2 in [(1, 2), (2, 5), (3, 6)]:
        f = Field()
        for n, amp in ((n1, 1.0), (n2, 1.0)):
            ks = shell_wavevectors(n, canonical_only=True)
            pick = list(ks)
            rng.shuffle(pick)
            for k in pick[: min(3, len(pick))]:
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
                "vacuous": bool(rec.get("vacuous_single_shell")),
            }
        )
    finite = [r["R_star"] for r in rows if r["R_star"] is not None]
    return {
        "harness": "light_rstar_ceilings",
        "candidate_link": ["C7", "C8"],
        "rows": rows,
        "max_R_star_finite": max(finite) if finite else None,
        "note": "Finite samples ≠ sup R_★; no kill claimed",
        "verdict_for_C8": "SURVIVES_AS_LAB",
    }


def run_subprocess_probe(script: str, args: list[str], timeout: int) -> dict:
    cmd = [sys.executable, str(ATTACKS / script), *args]
    env = os.environ.copy()
    # attack3 / near-shell import `ns_attacks.*` — need scripts/ on PYTHONPATH
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
            "stdout_tail": proc.stdout[-2000:],
            "stderr_tail": proc.stderr[-1000:],
            "ok": proc.returncode == 0,
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


def parse_attack3(stdout: str) -> dict:
    # Prefer JSON blob if present; else mark diagnostic-only.
    verdict = "HH_CHANNEL_LIVE_BOTTLENECK_no_closure"
    if "HH_CHANNEL_LIVE_BOTTLENECK" in stdout or "HH channel" in stdout:
        status = "SURVIVES"
    else:
        status = "INCONCLUSIVE"
    return {
        "candidate": "C7_HH_only_budget",
        "expected_verdict_substring": verdict,
        "probe_status": status,
        "note": "HH remains live bottleneck unless script fails",
    }


def main() -> int:
    rng = np.random.default_rng(20260916)
    payload: dict = {
        "title": "T_{j←j} same-scale candidate probes",
        "honesty": {
            "ns_solved": False,
            "clay_claimed": False,
            "spectral_shift_is_lemma_star": False,
            "numerics_are_depletion": False,
            "forbidden_slots": list(FORBIDDEN_SLOTS),
        },
        "analytic": {
            "C1": analytic_concentration_kill(),
            "C2": centrifugal_only_dead(),
            "C3": refuse_circular_slots(),
            "C4": occupancy_not_depletion(),
            "C5": pure_swirl_blocked(),
            "survivors": survivors_status(),
        },
        "light_numerics": {},
        "subprocess": {},
    }

    payload["light_numerics"]["rstar"] = light_rstar_ceilings(rng)

    # Cheap existing harnesses (budgeted). Write JSON under artifacts.
    a3_out = str(OUT / "attack3_summary.json")
    a3 = run_subprocess_probe(
        "attack3_bony_hh_l.py",
        ["--out", a3_out, "--seed", "3"],
        timeout=180,
    )
    payload["subprocess"]["attack3"] = {
        "script": a3["script"],
        "returncode": a3["returncode"],
        "ok": a3["ok"],
        "stdout_tail": a3.get("stdout_tail", "")[-1500:],
        "stderr_tail": a3.get("stderr_tail", "")[-500:],
        "out": a3_out if a3["ok"] else None,
    }
    a3_status = parse_attack3(a3.get("stdout_tail", ""))
    if a3["ok"] and Path(a3_out).is_file():
        try:
            a3_json = json.loads(Path(a3_out).read_text())
            a3_status["verdict"] = a3_json.get("verdict")
            a3_status["random_HH_frac_mean"] = a3_json.get("random_HH_frac_mean")
            a3_status["random_HH_frac_p90"] = a3_json.get("random_HH_frac_p90")
            if a3_json.get("verdict") == "HH_CHANNEL_LIVE_BOTTLENECK_no_closure":
                a3_status["probe_status"] = "SURVIVES"
        except json.JSONDecodeError:
            pass
    payload["light_numerics"]["C7_from_attack3"] = a3_status

    near_out = str(OUT / "near_shell_summary.json")
    near = run_subprocess_probe(
        "lemma_star_near_shell_search.py",
        [
            "--out",
            near_out,
            "--seed",
            "17",
            "--n-almost",
            "40",
            "--n-hh",
            "30",
        ],
        timeout=300,
    )
    payload["subprocess"]["near_shell"] = {
        "script": near["script"],
        "returncode": near["returncode"],
        "ok": near["ok"],
        "stdout_tail": near.get("stdout_tail", "")[-1500:],
        "stderr_tail": near.get("stderr_tail", "")[-500:],
        "out": near_out if near["ok"] else None,
    }
    c8 = {
        "candidate": "C8_near_shell_cancellation",
        "probe_ok": near["ok"],
        "probe_status": "SURVIVES_AS_LAB" if near["ok"] else "HARNESS_FAIL_OR_TIMEOUT",
        "note": "Kill decision uses complete signed Tc; no theorem",
    }
    if near["ok"] and Path(near_out).is_file():
        try:
            njson = json.loads(Path(near_out).read_text())
            c8["LemmaStar_killed"] = njson.get("LemmaStar_killed")
            c8["max_R_star"] = njson.get("max_R_star")
            c8["verdict"] = njson.get("verdict")
            if njson.get("LemmaStar_killed"):
                c8["probe_status"] = "KILL_ON_SAMPLES"
            elif njson.get("verdict") == "SURVIVE_numeric_gap_remains":
                c8["probe_status"] = "SURVIVES_AS_LAB"
        except json.JSONDecodeError:
            pass
    payload["light_numerics"]["C8_near_shell"] = c8

    # Summary table
    summary = []
    for key in ("C1", "C2", "C3", "C4", "C5"):
        summary.append(
            {
                "id": key,
                "verdict": payload["analytic"][key]["verdict"],
            }
        )
    for row in payload["analytic"]["survivors"]:
        summary.append({"id": row["candidate"], "verdict": row["verdict"]})
    summary.append(
        {
            "id": "C7_numeric",
            "verdict": payload["light_numerics"]["C7_from_attack3"]["probe_status"],
        }
    )
    summary.append(
        {
            "id": "C8_numeric",
            "verdict": payload["light_numerics"]["C8_near_shell"]["probe_status"],
        }
    )
    payload["summary"] = summary

    survivors = [
        s
        for s in summary
        if str(s["verdict"]).startswith("TRY")
        or s["verdict"] in ("SURVIVES", "SURVIVES_AS_LAB")
    ]
    payload["who_survived"] = survivors

    out_json = OUT / "tj_candidate_probe_results.json"
    out_json.write_text(json.dumps(payload, indent=2, default=str) + "\n")

    # Human-readable log
    lines = [
        "=== T_{j←j} SAME-SCALE CANDIDATE PROBES ===",
        "NS not solved. Spectral-shift ≠ Lemma★. Numerics ≠ depletion.",
        "",
        "Analytic DEAD/BLOCKED:",
        f"  C1 energy+visc R: {payload['analytic']['C1']['verdict']} "
        f"(ratio growth {payload['analytic']['C1']['ratio_growth_last_over_first']:.3g})",
        f"  C2 centrifugal-only: {payload['analytic']['C2']['verdict']} "
        f"(T_mm dominates={payload['analytic']['C2']['T_mm_dominates_abs']})",
        f"  C3 circular Gronwall: {payload['analytic']['C3']['verdict']} "
        f"refused={payload['analytic']['C3']['refused']}",
        f"  C4 occupancy⇒depletion: {payload['analytic']['C4']['verdict']}",
        f"  C5 pure-swirl class bound: {payload['analytic']['C5']['verdict']}",
        "",
        "TRY survivors:",
    ]
    for row in payload["analytic"]["survivors"]:
        ax = " [axisym-conditional]" if row.get("axisym_conditional") else ""
        lines.append(f"  {row['candidate']}: {row['verdict']}{ax}")
    rs = payload["light_numerics"]["rstar"]
    lines += [
        "",
        f"Light R_★ max (finite samples): {rs['max_R_star_finite']}",
        f"attack3 ok={a3['ok']} → C7 {payload['light_numerics']['C7_from_attack3']['probe_status']}",
        f"near-shell ok={near['ok']} → C8 {payload['light_numerics']['C8_near_shell']['probe_status']}",
        "",
        f"Wrote {out_json}",
    ]
    log = "\n".join(lines) + "\n"
    (OUT / "tj_candidate_probe_results.log").write_text(log)
    print(log, flush=True)
    # Analytic filter always succeeds; harness failures are recorded, not fatal.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
