#!/usr/bin/env python3
"""
DA attempt: take the operator's best A (Q1 + renormalization)
and best RH work. Dream-team papers look. They say what they
would do, how, and DA does the legal write.

A vote does not complete a missing line. Theorem A is already
complete for this PDE. RH WRITE does not sit. Q is not RH.
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


def chair(
    who: str,
    paper: str,
    would: str,
    how: str,
    cannot: str,
    does: str,
    sits: bool,
) -> dict:
    return {
        "who": who,
        "paper": paper,
        "would": would,
        "how": how,
        "cannot": cannot,
        "does": does,
        "sits": sits,
    }


JOBS = {
    "A": {
        "id": "A",
        "aliases": (
            "augmented",
            "q1",
            "renormal",
            "olga",
            "ladyzhenskaya",
            "track a",
        ),
        "name": "Q1-augmented NS (this PDE) plus the eps->0 renormalization",
        "slot": "A",
        "furthest": (
            "Theorem A pass: energy, Galerkin, weak limit, unique H1, "
            "C^infty at eps>0, beta>=1/2. That is the close you already have. "
            "The latest extra write is the renormalization: send the extra "
            "dissipation to zero (A6: Q1 integral falls as eps falls) and "
            "hope H1 stays. It does not, on the scored box."
        ),
        "progress": [
            {"id": "A1", "what": "energy identity", "verdict": "pass"},
            {"id": "A2", "what": "Galerkin global", "verdict": "pass"},
            {"id": "A3", "what": "weak limit is a weak solution", "verdict": "pass"},
            {"id": "A4", "what": "unique H1 at eps>0, beta>=1/2", "verdict": "pass"},
            {"id": "A5", "what": "C^infty bootstrap at eps>0", "verdict": "pass"},
            {"id": "A_theorem", "what": "Theorem A for this PDE", "verdict": "pass"},
            {"id": "A6", "what": "Q1 integral falls as eps falls (the renormalization)", "verdict": "pass"},
            {"id": "A7", "what": "enstrophy on the box is independent of eps", "verdict": "fail"},
            {"id": "A8", "what": "box non-uniformity is a no-go for all data", "verdict": "fail"},
            {"id": "A9", "what": "Q1 vanishing writes a uniform H1 bound", "verdict": "fail"},
            {"id": "A_uniform_H1", "what": "Lemma 4 stays finite as eps->0", "verdict": "open"},
            {"id": "A_implies_B", "what": "Theorem A is classical NS", "verdict": "fail"},
        ],
        "errors_corrected": [
            "Hearing Theorem A closed is not classical NS.",
            "Vanishing Q1 (the renormalization) is the gap, not a bound (A9).",
            "Phi is not the estimate variable.",
            "Exporting Ladyzhenskaya onto B is refused.",
            "A=>B is refused.",
        ],
        "needs": (
            "A bound on ||u||_H1 that stays finite as eps->0, or a named "
            "obstruction that it cannot. That write stays on A. Classical "
            "NS then still needs a separate Track B argument."
        ),
        "completed": (
            "This PDE: the chain is already complete (Theorem A). "
            "The renormalization to eps=0 is not complete. "
            "Classical NS is not complete."
        ),
        "docs": (
            "docs/TRACK-A-LEMMAS.md",
            "docs/TRACK-A-GAP.md",
            "docs/AUGMENTED-NS-PROOF-CHAIN.md",
            "docs/DA-REPAIR.md",
        ),
        "team": [
            chair(
                "Ladyzhenskaya",
                "1968 modified-stress / p-Laplacian NS",
                "Keep Theorem A on this PDE. I already closed it at eps>0, beta>=1/2.",
                "Extra integrability of grad u from the monotone extra stress. p>=5/2 in 3D.",
                "Pass eps->0. A different equation is not classical NS.",
                "Restate Theorem A as complete for this PDE. Leave Olga on A.",
                True,
            ),
            chair(
                "Malek-Necas-Ruzicka",
                "Weak and Measure-valued Solutions, Ch. 5",
                "Keep the weak limit and Minty-Browder passage for the extra stress.",
                "Galerkin + monotonicity. The extra dissipation only helps compactness.",
                "A uniform H1 constant as eps->0.",
                "Keep Lemmas 2-4 as scored. A4's constant still blows up.",
                True,
            ),
            chair(
                "Temam",
                "smoothness / attractor after an H1 bound",
                "Bootstrap to C^infty once H1 is already uniform.",
                "Standard NS bootstrap. Gevrey and attractors wait on smoothness.",
                "Write the missing uniform constant.",
                "A5 stays pass only at eps>0. Do not treat the attractor as the gap.",
                True,
            ),
            chair(
                "Tao",
                "averaged / regularized cousins as different equations",
                "Treat Q1 as a different PDE. Do not export the close.",
                "Name the extra term. If it leaves, you have changed the problem back.",
                "A slide of eps onto B.",
                "Score A_implies_B fail. The renormalization is a different claim.",
                True,
            ),
            chair(
                "Fefferman",
                "Clay official NS problem; geometric ifs on the classical field",
                "If you want classical regularity, write an a priori on classical leftover.",
                "Alignment in time (A1) is an if on B, not a Q1 identity.",
                "Cash Olga as Fefferman A1.",
                "Send the classical close to the B chain. Do not mix chairs.",
                True,
            ),
            chair(
                "Constantin",
                "geometric depletion if aligned (with Fefferman)",
                "Geometry after you are on the classical vorticity field.",
                "CF-if on omega. CONC is not already aligned.",
                "Q1 dissipation as alignment. Phi as the estimate.",
                "Refuse Phi. Geometry stays off this A write.",
                True,
            ),
        ],
        "da_does": (
            "Correct the five errors. Print the A progress table. "
            "Complete the this-PDE chain (already sat). "
            "Attempt uniform H1 from the renormalization (A6/A7/A9): "
            "does not sit. Do not invent leftover B42. Do not retune nodes.json."
        ),
    },
    "RH": {
        "id": "RH",
        "aliases": ("rh", "riemann", "zeta", "theorem p", "furthest"),
        "name": "Riemann hypothesis — furthest desk attempt was inverse-GCD",
        "slot": "RH / Q",
        "furthest": (
            "Classical RH chain through (5) sits (zeta, xi, strip, PNT, "
            "Hardy + proportion). The furthest original write on this desk "
            "was the inverse-GCD package: Bridge*, Theorem P "
            "(prime-supported Q-tilde >= -1/4), and the renormalized "
            "H_N = D^{-1/2} Q-tilde D^{-1/2} with H_N >= -1. "
            "Those are completed Q theorems. They were glued to zeros. "
            "That glue is the error. Full Q > -1/2 and H >= -3/14 are false."
        ),
        "progress": [
            {"id": "RH1", "what": "zeta meromorphic, Euler product", "verdict": "pass"},
            {"id": "RH2", "what": "xi entire, xi(s)=xi(1-s)", "verdict": "pass"},
            {"id": "RH3", "what": "non-trivial zeros in the strip", "verdict": "pass"},
            {"id": "RH4", "what": "no zeros on Re s = 1 (PNT)", "verdict": "pass"},
            {"id": "RH5", "what": "infinitely many / a proportion on Re s = 1/2", "verdict": "pass"},
            {"id": "RH6", "what": "every non-trivial zero has Re s = 1/2", "verdict": "open"},
            {"id": "Q_H_floor", "what": "lambda_min(H_N) >= -1 (renormalized Q)", "verdict": "pass"},
            {"id": "Q_theorem_P", "what": "prime-supported Q-tilde >= -1/4", "verdict": "pass"},
            {"id": "Q_bridge", "what": "Bridge* on e_p - e_q", "verdict": "pass"},
            {"id": "Q_full_floor", "what": "lambda_min(Q_N) > -1/2 for all N", "verdict": "fail"},
            {"id": "Q_h_314", "what": "lambda_min(H_N) >= -3/14", "verdict": "fail"},
            {"id": "Q_is_RH", "what": "Theorem P / H_N is the Riemann hypothesis", "verdict": "fail"},
        ],
        "errors_corrected": [
            "Track Q is inverse-GCD. It is not RH.",
            "Theorem P is not every zero on the line.",
            "H_N >= -1 is a matrix floor, not a zero.",
            "Bridge* is a two-prime identity, not RH.",
            "Q > -1/2 is false (Q_10 ~ -1.90).",
            "H >= -3/14 is false (H_4 ~ -0.225).",
        ],
        "needs": (
            "One write that puts every non-trivial zero on Re s = 1/2: "
            "a zero-free region that reaches the line, a positivity "
            "certificate in the explicit formula, or one new estimate "
            "that forces the line. Do not use Theorem P, Bridge*, or H_N."
        ),
        "completed": (
            "RH through (5): complete (literature + classical). "
            "RH WRITE (6): not complete. "
            "Q floors H_N>=-1 and Theorem P: complete as Q, not as RH."
        ),
        "docs": (
            "docs/RH-PROOF-CHAIN.md",
            "docs/SPECTRAL-FLOOR-EXPLORATION.md",
            "docs/DA-PROOF.md",
        ),
        "team": [
            chair(
                "Riemann",
                "1859 xi and the functional equation",
                "Start from zeta and xi. That is the ground floor.",
                "Completed zeta, xi(s)=xi(1-s), entire of order 1.",
                "The line from xi alone. The functional equation is a symmetry, not RH.",
                "Keep RH lines (1)-(2) as have. Do not load Q into xi.",
                True,
            ),
            chair(
                "Hadamard",
                "1896 prime number theorem / zero-free on Re s = 1",
                "Keep the prime number theorem. No zeros on Re s = 1.",
                "Zero-free region next to the line Re s = 1.",
                "Push that region all the way to Re s = 1/2.",
                "Keep RH line (4). A classical zero-free region is not RH.",
                True,
            ),
            chair(
                "de la Vallee Poussin",
                "1896 prime number theorem, independently",
                "The same PNT. Stay on the edge Re s = 1.",
                "Classical zero-free width. Error term from that width.",
                "RH, or a Q-matrix as a zero-free region.",
                "Keep RH line (4). Unglue inverse-GCD from PNT.",
                True,
            ),
            chair(
                "Hardy",
                "infinitely many zeros on Re s = 1/2",
                "Keep infinitely many zeros on the line.",
                "Moments / mollified xi on the critical line.",
                "Every zero. Infinitely many is not all.",
                "Keep RH line (5) as have. Do not cash it as (6).",
                True,
            ),
            chair(
                "Conrey",
                "positive proportion of zeros on the line",
                "Keep a positive proportion on the line.",
                "Mollifiers. Later work raises the proportion. It is not 1.",
                "Proportion 1. A proportion is not RH.",
                "Keep RH line (5). The WRITE is still every zero.",
                True,
            ),
            chair(
                "Weil",
                "explicit formula",
                "If every zero is on the line, write the explicit formula with all oscillations on Re s = 1/2.",
                "von Mangoldt explicit formula. Consequences after (6).",
                "Force (6) from a GCD matrix. H_N is not a zero.",
                "Keep RH (7)-(8) as follows. They wait on (6).",
                True,
            ),
        ],
        "da_does": (
            "Correct the six errors. Unglue Q from RH. "
            "Keep H_N>=-1 and Theorem P as completed Q. "
            "Emit the RH chain. WRITE (6) does not sit. "
            "Do not revive -3/14 or the full Q floor."
        ),
    },
}


CLAIMS = [
    rec(
        "D1",
        "take_best",
        "DA can take the best A (Q1 + renormalization) and the furthest RH attempt",
        "pass",
        "A catalog and the Q floors plus the RH chain are already scored.",
    ),
    rec(
        "D2",
        "dream_team_looks",
        "Field papers say what they would do, how, and what they cannot",
        "pass",
        "Ladyzhenskaya / Malek / Temam / Tao / Fefferman / Constantin on A. "
        "Riemann / Hadamard / de la Vallee Poussin / Hardy / Conrey / Weil on RH.",
    ),
    rec(
        "D3",
        "da_does_legal",
        "DA does the legal corrections and restates the chains that already sit",
        "pass",
        "This-PDE Theorem A. Q floors as Q. Errors fail. Missing WRITE stays open.",
    ),
    rec(
        "D4",
        "team_writes_rh",
        "The dream team completes RH WRITE (every zero on the line)",
        "fail",
        "A council cannot write (6). Hardy and Conrey already sat and are not RH.",
    ),
    rec(
        "D5",
        "team_writes_uniform",
        "The dream team completes A_uniform_H1 or A=>B",
        "fail",
        "Olga already closed this PDE. She cannot pass eps->0. A vote cannot.",
    ),
    rec(
        "D6",
        "a_this_pde_done",
        "The Q1-augmented chain at eps>0 is already complete",
        "pass",
        "That is the close heard a half-dozen times. It stays on A.",
    ),
    rec(
        "D7",
        "q_is_rh",
        "Theorem P or H_N >= -1 is the Riemann hypothesis",
        "fail",
        "Different object. Inverse-GCD is not a zero of zeta.",
    ),
    rec(
        "D8",
        "vote_fills_write",
        "Experts looking at it write the missing line by agreeing",
        "fail",
        "would / how / cannot is a library. A vote is not an estimate.",
    ),
    rec(
        "D9",
        "uniform_later",
        "A_uniform_H1 may sit later",
        "open",
        "A bound or a named no-go. Neither sits. The write stays on A.",
    ),
    rec(
        "D10",
        "rh_write_later",
        "RH WRITE may sit later",
        "open",
        "A zero-free region to 1/2, a positivity certificate, or one new estimate. Not Q.",
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
    if "A" not in found and re.search(
        r"\b(?:job|repair|fix|close|attempt|my|track|analyze)\s+a\b",
        text,
    ):
        found.insert(0, "A")
    return found


def parse_job(ask: str = "", job: str = "") -> str | None:
    found = parse_jobs(ask=ask, job=job)
    return found[0] if found else None


def is_attempt_ask(ask: str) -> bool:
    text = (ask or "").lower().strip()
    if not text:
        return False
    return bool(
        re.search(
            r"\bdream team\b|\banalyze my\b|\bcomplete the chain\b|"
            r"\brenormali[sz]|\bfurthest\b|\bmy rh\b|"
            r"\bmy (best )?(rh|augmented)\b|"
            r"\bexperts (look|do|say)\b|\bda attempt\b|"
            r"\blook at (my )?(a|rh|augmented)\b",
            text,
        )
    )


def run(out: Path | None = None, job: str | None = None, ask: str = "") -> dict:
    picked = parse_jobs(ask=ask, job=job or "")
    jobs = [JOBS[j] for j in picked] if picked else list(JOBS.values())
    payload = {
        "meta": {
            "question": "analyze best A (Q1 + renormalization) and furthest RH; dream team looks; do the legal write",
            "writeup": "docs/DA-ATTEMPT.md",
            "takes_mine": True,
            "uses_dream_team": True,
            "vote_is_not_a_close": True,
            "a_this_pde_complete": True,
            "a_uniform_not_complete": True,
            "rh_write_not_complete": True,
            "q_is_not_rh": True,
        },
        "jobs": jobs,
        "all_jobs": list(JOBS),
        "picked": picked,
        "claims": CLAIMS,
        "counts": {
            "jobs": len(jobs),
            "chairs": sum(len(j["team"]) for j in jobs),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "next_da_move": (
            "This PDE is already closed. RH WRITE and A_uniform_H1 do not sit. "
            "Pick one remaining write. Classify it. Do not glue Q to RH. "
            "Do not export Olga."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_attempt.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_attempt(out: Path | None = None, job: str | None = None, ask: str = "") -> dict:
    payload = run(out=out, job=job, ask=ask)
    print("ATTEMPT  (your best work; dream team looks; legal write)")
    print("Jobs:", ", ".join(payload["all_jobs"]))
    print("A vote does not complete a missing line.")
    print()
    for spec in payload["jobs"]:
        print(f"JOB {spec['id']}  {spec['name']}")
        print(f"  SLOT    {spec['slot']}")
        print(f"  FURTHEST {spec['furthest']}")
        print("  PROGRESS")
        for row in spec["progress"]:
            print(f"    [{row['verdict']}] {row['id']}: {row['what']}")
        print("  ERRORS CORRECTED")
        for err in spec["errors_corrected"]:
            print(f"    - {err}")
        print(f"  NEEDS   {spec['needs']}")
        print(f"  DONE    {spec['completed']}")
        print("  DREAM TEAM")
        for c in spec["team"]:
            print(f"    {c['who']}  ({c['paper']})")
            print(f"      WOULD  {c['would']}")
            print(f"      HOW    {c['how']}")
            print(f"      CANNOT {c['cannot']}")
            print(f"      DOES   {c['does']}")
        print(f"  DA DOES {spec['da_does']}")
        print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return payload


def main() -> int:
    ask = " ".join(a for a in sys.argv[1:] if not a.startswith("-"))
    print_attempt(ask=ask, job=ask)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
