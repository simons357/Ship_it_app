#!/usr/bin/env python3
"""
DA repair: take the operator's A / SND / H work.

They already put the work in. They have heard "closed"
on the augmented system. DA names the fault and the
repair write. Exporting A onto B is not a repair.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def rec(
    hid: str,
    name: str,
    statement: str,
    verdict: str,
    why: str,
    **extra,
) -> dict:
    row = {
        "id": hid,
        "name": name,
        "statement": statement,
        "verdict": verdict,
        "why": why,
    }
    row.update(extra)
    return row


JOBS = {
    "A": {
        "id": "A",
        "aliases": ("augmented", "q1", "olga", "ladyzhenskaya", "track a"),
        "have": (
            "Theorem A pass for the Q1-augmented PDE at eps>0, beta>=1/2. "
            "Energy, Galerkin, weak limit, unique H1, C^infty. That is closed "
            "for this equation. That is the close you heard a half-dozen times."
        ),
        "fault": (
            "The extra dissipation that closed Theorem A leaves as eps->0 "
            "(A6 pass, A7 fail). Lemma 4's H1 constant blows up. "
            "A_uniform_H1 is open. A_implies_B fails. "
            "A declaration that A is classical NS is the fake close."
        ),
        "repair": (
            "Write a bound on ||u||_H1 that stays finite as eps->0, "
            "or a named obstruction that it cannot. That write stays on A. "
            "Do not export Olga onto classical NS. Do not cancel to Phi."
        ),
        "to_close": (
            "This PDE: already closed (Theorem A). "
            "Classical NS: A_uniform_H1, then a separate argument that the "
            "limit is classical. That second step is Track B, not a slide."
        ),
        "do_not": "A=>B. Slide eps onto B. Revive Phi as the estimate. Retune nodes.json.",
        "docs": ("docs/TRACK-A-LEMMAS.md", "docs/TRACK-A-GAP.md", "docs/AUGMENTED-NS-PROOF-CHAIN.md"),
        "object": {
            "name": "Q1-augmented NS",
            "slot": "A",
            "english": "eps>0, beta>=1/2; Theorem A pass; uniform H1 as eps->0 open",
            "window": [
                "this PDE is closed at eps>0",
                "the extra term leaves as eps->0",
                "A_uniform_H1 is the repair write",
                "A is not B",
            ],
        },
    },
    "SND": {
        "id": "SND",
        "aliases": ("snd", "conc", "spread", "3-conc"),
        "have": (
            "Two opposite statements were both called SND. "
            "August: CONC, inf J/X >= c_*. June T2: SPREAD, rho=J/X <= rho0 < 1. "
            "The desk already froze 3-CONC / EQ3 / SPREAD."
        ),
        "fault": (
            "One word for opposites. Bridge* glued to SND (withdrawn). "
            "Phi put in front of H so the package looked like it died "
            "when the cancel dropped. SIMPLEX used GCD arithmetic."
        ),
        "repair": (
            "Keep two names. CONC (sigma>=1/2) and SPREAD (sigma<1/2). "
            "Cut Phi and Q from this track. "
            "Write SND-C only in SPREAD: a uniform bound on the low "
            "paraproduct as rho->0. That is the real remaining write. "
            "Do not reattach Bridge*."
        ),
        "to_close": (
            "A two-regime a priori: CONC uses Ring / geometry; "
            "SPREAD uses T2 Lemma 1 plus uniform SND-C. "
            "Neither is written as an all-data bound on X."
        ),
        "do_not": "One symbol SND. Bridge*=>SND. SIMPLEX. Phi in front of H.",
        "docs": ("docs/UNAUGMENTED-R4-VORTICITY-PLAN.md",),
        "object": {
            "name": "occupation rho = J/X",
            "slot": "B",
            "english": "CONC vs SPREAD; do not call both SND",
            "window": [
                "CONC: inf J/X >= c_*",
                "SPREAD: rho <= rho0 < 1",
                "SND-C is a commutator in SPREAD only",
                "Bridge* does not imply SND",
            ],
        },
    },
    "H": {
        "id": "H",
        "aliases": ("h", "theorem h", "h-floor", "h_n", "snd-c"),
        "have": (
            "Two H objects. Fluids: Theorem H = SND-C in SPREAD via Bony "
            "T+T*+R (May T3). Arithmetic: Theorem H-floor, lambda_min(H_N)>=-1, "
            "proved by pairing. Both sit. They are not the same H."
        ),
        "fault": (
            "Fluids H: Theorem F is too strong (super-exponential dissipation "
            "as rho->0 is not a theorem). The low Bony T sum of many shells "
            "need not be small. G needs C_* uniform down to rho->0. "
            "Phi-glue made H look broken after the cancel. "
            "Arithmetic H: -3/14 is false (H4~-0.225). Q>-1/2 is false. "
            "Those were the fake closes."
        ),
        "repair": (
            "Fluids: delete B/C/I/Phi from the H track. State H only for "
            "classical velocity on T^3, SPREAD, no eps. Write a uniform "
            "energy-class bound on the low paraproduct as rho->0. "
            "Arithmetic: keep H_N>=-1. To sharpen, prove H_N>=-1/4 "
            "(numeric through N=200; pairing does not give it). "
            "Do not revive -3/14 or the full Q floor."
        ),
        "to_close": (
            "Fluids H: uniform SND-C in SPREAD. "
            "Arithmetic H: H_N>=-1 is already closed; H_N>=-1/4 is the "
            "remaining floor if you want every coordinate, not only primes."
        ),
        "do_not": "Phi in front of H. F as super-exponential. -3/14. Q>-1/2. Glue H-fluids to H_N.",
        "docs": (
            "docs/UNAUGMENTED-R4-VORTICITY-PLAN.md",
            "docs/SPECTRAL-FLOOR-EXPLORATION.md",
        ),
        "object": {
            "name": "H (two objects)",
            "slot": "B / Q",
            "english": "fluids SND-C vs degree-normalized H_N",
            "window": [
                "fluids H: |Pi_j*| bound in SPREAD",
                "arithmetic H: lambda_min(H_N) >= -1 (proved)",
                "H_N >= -1/4 is open",
                "not the same H",
            ],
        },
    },
}


CLAIMS = [
    rec(
        "R1",
        "take_mine",
        "DA can take the operator's A / SND / H work and name the fault",
        "pass",
        "They already put the work in. Diagnosis uses the scored catalog.",
    ),
    rec(
        "R2",
        "name_the_repair",
        "DA can name the repair write for each job",
        "pass",
        "A: uniform H1. SND: two names + uniform SND-C. H: cut Phi; H_N>=-1/4.",
    ),
    rec(
        "R3",
        "repair_exports_a",
        "Repairing A is exporting Olga onto classical NS",
        "fail",
        "The repair write stays on A. A=>B is not a repair.",
    ),
    rec(
        "R4",
        "one_snd_word",
        "Calling both statements SND is the repair",
        "fail",
        "August CONC and June SPREAD are opposites. Two names is the hygiene.",
    ),
    rec(
        "R5",
        "revive_false_floors",
        "Repair H by reviving Q>-1/2 or H>=-3/14",
        "fail",
        "Those are false. The live floor is H_N>=-1. Sharp is H_N>=-1/4, open.",
    ),
    rec(
        "R6",
        "a_closed_is_b",
        "Hearing Theorem A closed means classical NS is done",
        "fail",
        "That close is this PDE at eps>0. That is why it felt done a half-dozen times.",
    ),
    rec(
        "R7",
        "uniform_h1_may_sit",
        "A_uniform_H1 may sit later",
        "open",
        "A bound or a named no-go. Neither sits. The write stays on A.",
    ),
    rec(
        "R8",
        "snd_c_may_sit",
        "Uniform SND-C in SPREAD may sit later",
        "open",
        "Low paraproduct, energy class, rho->0. That is the fluids H write.",
    ),
    rec(
        "R9",
        "h_quarter_may_sit",
        "H_N >= -1/4 may sit later",
        "open",
        "Numeric through N=200. Pairing does not prove it.",
    ),
]


def parse_jobs(ask: str = "", job: str = "") -> list[str]:
    text = f"{job} {ask}".lower()
    found: list[str] = []
    for jid, spec in JOBS.items():
        for alias in spec["aliases"]:
            if re.search(rf"\b{re.escape(alias)}\b", text):
                found.append(jid)
                break
    token = (job or "").strip().upper()
    if token in JOBS and token not in found:
        found.insert(0, token)
    if "A" not in found and re.search(r"\b(?:job|repair|fix|close)\s+a\b", text):
        found.insert(0, "A")
    return found


def parse_job(ask: str = "", job: str = "") -> str | None:
    found = parse_jobs(ask=ask, job=job)
    return found[0] if found else None


def is_repair_ask(ask: str) -> bool:
    text = (ask or "").lower().strip()
    if not text:
        return False
    return bool(
        re.search(
            r"\brepair\b|\bwhat.?s wrong\b|\bhow to fix\b|"
            r"\baugmented one\b|\bfix (snd|h|a)\b|"
            r"\bda repair\b",
            text,
        )
    )


def run(out: Path | None = None, job: str | None = None, ask: str = "") -> dict:
    picked = parse_jobs(ask=ask, job=job or "")
    jobs = [JOBS[j] for j in picked] if picked else list(JOBS.values())
    payload = {
        "meta": {
            "question": "repair the operator's A / SND / H work",
            "writeup": "docs/DA-REPAIR.md",
            "takes_mine": True,
            "a_is_closed_for_this_pde": True,
            "a_is_not_b": True,
            "q_is_not_snd": True,
        },
        "jobs": jobs,
        "all_jobs": list(JOBS),
        "picked": picked,
        "claims": CLAIMS,
        "counts": {
            "jobs": len(jobs),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "next_da_move": (
            "Pick one repair write. Classify it. "
            "Theorem A is already closed for this PDE. "
            "Do not export it onto B."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_repair.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_job_window(obj: dict) -> None:
    print("OBJECT WINDOW")
    print(f"  {obj['name']}  slot {obj['slot']}")
    print(f"  {obj['english']}")
    for line in obj["window"]:
        print(f"  {line}")


def print_repair(out: Path | None = None, job: str | None = None, ask: str = "") -> dict:
    payload = run(out=out, job=job, ask=ask)
    print("REPAIR  (your work; fault; write)")
    print("Jobs:", ", ".join(payload["all_jobs"]))
    print()
    for spec in payload["jobs"]:
        print_job_window(spec["object"])
        print()
        print(f"JOB {spec['id']}")
        print("  HAVE   ", spec["have"])
        print("  FAULT  ", spec["fault"])
        print("  REPAIR ", spec["repair"])
        print("  CLOSE  ", spec["to_close"])
        print("  DO NOT ", spec["do_not"])
        print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return payload


def main() -> int:
    ask = " ".join(a for a in sys.argv[1:] if not a.startswith("-"))
    print_repair(ask=ask, job=ask)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
