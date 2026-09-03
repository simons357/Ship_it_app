#!/usr/bin/env python3
"""
Screen published unification claims against the DA criteria.

Two levels, not glued:
  gauge3  — do the three SM couplings meet at one scale?
  nature4 — one map F hits (g_s, g_w, g_em, g_N) and Λ stays in the sum.

A slogan is not a pass. This is a claim-structure + public-status screen,
not a recode of anyone's Lagrangian.
"""

from __future__ import annotations

import json
from pathlib import Path


# DA unifier-at-ε (same as the score book). Gravity and vacuum stay in.
CRITERIA = {
    "one_F": "one map (or one group + RG) from a finite knob set",
    "gauge3": "α_em, α_s, sin²θ_W (or g, g', g_s) meet at one scale",
    "gravity": "G_N / Planck is an output of the same F, not an input leftover",
    "vacuum": "ρ_Λ / Λ is an output of the same F, not dropped",
    "falsifiable": "a finite experiment could kill it",
    "not_killed": "that experiment has not already killed it",
}


def row(
    name: str,
    kind: str,
    one_F: str,
    gauge3: str,
    gravity: str,
    vacuum: str,
    falsifiable: str,
    not_killed: str,
    gauge3_verdict: str,
    nature4_verdict: str,
    note: str,
) -> dict:
    return {
        "name": name,
        "kind": kind,
        "checks": {
            "one_F": one_F,
            "gauge3": gauge3,
            "gravity": gravity,
            "vacuum": vacuum,
            "falsifiable": falsifiable,
            "not_killed": not_killed,
        },
        "gauge3_verdict": gauge3_verdict,
        "nature4_verdict": nature4_verdict,
        "note": note,
    }


CLAIMS = [
    row(
        "SM running (no extra stuff)",
        "gauge",
        "RG of the SM",
        "the three couplings miss",
        "no",
        "no",
        "yes — they either meet or they do not",
        "already missed",
        "fail",
        "fail",
        "Baseline. The Standard Model does not unify the couplings.",
    ),
    row(
        "Georgi–Glashow SU(5)",
        "gauge",
        "SU(5) → SM, one α_GUT",
        "misses without extra thresholds",
        "no",
        "no",
        "yes — proton decay, coupling meet",
        "minimal form killed (proton lifetime + miss)",
        "fail",
        "fail",
        "The original GUT. Publicly dead in its minimal form.",
    ),
    row(
        "MSSM / SUSY SU(5) or SO(10)",
        "gauge",
        "MSSM RG + a GUT group",
        "approximate meet near 2e16 GeV (α_GUT ~ 1/24)",
        "no",
        "no",
        "yes — proton decay, superpartners, Higgs mass",
        "not fully killed; squeezed (mini-split / multi-TeV)",
        "open",
        "fail",
        "Best-known 3-gauge program still standing. Does not output G_N or Λ.",
    ),
    row(
        "Pati–Salam SU(4)×SU(2)×SU(2)",
        "gauge",
        "partial unification, then a further step",
        "not a single meeting of all three at one shot",
        "no",
        "no",
        "yes — extra gauge bosons, proton decay in embeddings",
        "not a complete 3-meet by itself",
        "fail",
        "fail",
        "Lepton-as-fourth-color. A piece, not nature4.",
    ),
    row(
        "Heterotic / type-II string landscape",
        "gravity_gauge",
        "no unique F (10^500-class vacua)",
        "some vacua can be arranged to meet",
        "G_N exists in the framework, not a unique output",
        "Λ is a vacuum-selection problem, not a prediction",
        "yes in principle; unique numbers are not",
        "no unique prediction to kill",
        "open",
        "fail",
        "Has gravity in the story. Does not hand you one F to the observed leftovers.",
    ),
    row(
        "Asymptotic safety (gravity)",
        "gravity_gauge",
        "UV fixed point for gravity",
        "not a 3-gauge unifier",
        "gravity is the object; G_N runs, not derived as a meet",
        "no",
        "yes — fixed-point existence, collider / cosmology bounds",
        "open as a gravity program",
        "fail",
        "fail",
        "A gravity UV story. Not four-force unification.",
    ),
    row(
        "Lisi E8",
        "gauge",
        "claimed E8 embedding of SM + gravity",
        "not a demonstrated 3-meet from a working rep",
        "claimed, not accepted as a working output",
        "no",
        "yes — representations, three generations, chirality",
        "standard objections stand (chirality / generations)",
        "fail",
        "fail",
        "A published claim. Screened. Does not pass.",
    ),
    row(
        "Loop quantum gravity / causal sets",
        "topological",
        "no F to the three couplings",
        "no",
        "quantum geometry; not G_N as a derived coupling meet",
        "no",
        "yes — area spectrum, cosmology, Lorentz tests",
        "open as quantum-gravity programs",
        "fail",
        "fail",
        "Quantum geometry, not a four-force unifier.",
    ),
    row(
        "This repo's reconstructed R / SFE knobs",
        "teleological",
        "no producing-map (affine holdout failed)",
        "couplings were pasted, not produced",
        "hierarchy is a leftover coordinate",
        "vacuum is a leftover coordinate",
        "yes — lock-R, holdout F, width control",
        "F already killed on this vector",
        "fail",
        "fail",
        "Screened the same way. Score is not F. Official Cosmo 16 is a different catalog.",
    ),
    row(
        "CosmoEvolution 3D / Domain Architect (public app)",
        "topological",
        "core equation is private / trade secret",
        "app predicts couplings should NOT meet; a miss is not a 3-meet",
        "claimed via Planck spectral gap (order of magnitude)",
        "claimed via domain web tension (order of magnitude)",
        "yes — manifold λ1/λ2, neutrino sum, Koide deviation",
        "manifold sweep already failed for every known exact-spectrum topology",
        "fail",
        "fail",
        "Official 16 is in docs/COSMO-SIXTEEN.md. UI 16/16 is not a DA pass. F is not public.",
    ),
]


def tally(claims: list[dict]) -> dict:
    g3 = {"pass": 0, "fail": 0, "open": 0}
    n4 = {"pass": 0, "fail": 0, "open": 0}
    for c in claims:
        g3[c["gauge3_verdict"]] += 1
        n4[c["nature4_verdict"]] += 1
    return {"gauge3": g3, "nature4": n4}


def run(out: Path | None = None) -> dict:
    counts = tally(CLAIMS)
    still = [c["name"] for c in CLAIMS if c["gauge3_verdict"] == "open"]
    nature_pass = [c["name"] for c in CLAIMS if c["nature4_verdict"] == "pass"]
    payload = {
        "meta": {
            "question": "can we discern unification by screening published claims?",
            "not_a_unifier": True,
            "two_levels": ["gauge3", "nature4"],
            "do_not_glue": True,
        },
        "criteria": CRITERIA,
        "claims": CLAIMS,
        "counts": counts,
        "still_open_as_gauge3": still,
        "passed_nature4": nature_pass,
        "discernment": (
            "Yes. Gauge-coupling meeting (gauge3) is a real, fail-able claim. "
            "Four-force unification with gravity and vacuum in the same F (nature4) "
            "is a stricter claim. Nothing on this list passes nature4. "
            "MSSM-class GUTs stay open as gauge3. Minimal SU(5) and the SM miss. "
            "That is discernment. It is not a unifier in this repo."
        ),
        "how_far": [
            f"screened {len(CLAIMS)} published-or-local claims",
            f"gauge3 open: {still}",
            "nature4 pass: none",
            "3-meet ≠ 4-force unifier; do not glue the levels",
            "next: paste a specific Lagrangian / RG and re-score gauge3 χ²; nature4 still needs G_N and Λ out of the same F",
        ],
        "next_da_move": (
            "If you name one program, DA will score that one at gauge3 with numbers. "
            "Nature4 stays fail until G_N and Λ are outputs of the same F."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_screen.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA unification screen. Two levels. Do not glue them.")
    print(f"{'claim':<42} {'kind':<16} {'gauge3':<6} {'nature4'}")
    for c in payload["claims"]:
        print(f"{c['name']:<42} {c['kind']:<16} {c['gauge3_verdict']:<6} {c['nature4_verdict']}")
    print("still open as gauge3:", payload["still_open_as_gauge3"])
    print("passed nature4:", payload["passed_nature4"])
    print(payload["discernment"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
