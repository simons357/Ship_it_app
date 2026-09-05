#!/usr/bin/env python3
"""
DA proof: write a proof chain from the ground floor.

The operator is not a math person. They name a problem
(NS, RH). DA writes the aimed theorem and the chain.
Asking is the product. Emitting the chain is not QED.
Line WRITE is the attempt.

Track Q is inverse-GCD. It is not RH. Do not glue.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_from import MINE, NEEDED  # noqa: E402
from da_hunt import LEGAL, OBJECT  # noqa: E402
from da_next import WALL  # noqa: E402


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


NS_LINES = [
    {
        "n": 1,
        "status": "have",
        "text": (
            "Energy. Leray: int_0^T X(t) dt < infinity on these packets, "
            "and the energy inequality holds."
        ),
    },
    {
        "n": 2,
        "status": "have",
        "text": (
            "Enstrophy identity. Differentiating X along the NSE gives "
            "dX/dt + nu ||grad omega||_2^2 = -int omega · S omega "
            "(up to lower-order terms already controlled)."
        ),
    },
    {
        "n": 3,
        "status": "have",
        "text": (
            "Leftover form. Absorb a slice of dissipation to obtain "
            + WALL["looks_like"]
            + " The only term that can beat viscosity is the stretching leftover."
        ),
    },
    {
        "n": 4,
        "status": "have",
        "text": (
            "Split. int omega · S omega = hole 1 (aligned P+ on E_c) "
            "+ hole 2 (unaligned P+ on E_c) + hole 3 (off E_c). "
            "Scored on the n=32 box as B37."
        ),
    },
    {
        "n": 5,
        "status": "have",
        "text": (
            "Named blanks. A1 = alignment in time for all data (hole 1). "
            "A2 = int ||lambda_2^+|| for all data (live cubic; Miller cut B38). "
            "On this box A1 is off and A2 is live and did not blow on the B15 path (B40, B41)."
        ),
    },
    {
        "n": 6,
        "status": "write",
        "text": (
            "WRITE. One all-data integrable residual: int_0^T R(t) dt < infinity, "
            "or all-data A1, or all-data A2, or a field that kills the stretching leftover."
        ),
    },
    {
        "n": 7,
        "status": "follows",
        "text": "Gronwall. From (3) and (6), X(t) stays finite on [0, T].",
    },
    {
        "n": 8,
        "status": "follows",
        "text": (
            "Continuation. Beale-Kato-Majda: if int_0^T ||omega||_infty dt < infinity "
            "then the solution continues. A bound that yields that integral, "
            "or an equivalent criterion, gives no blowup. L2 is not the max."
        ),
    },
    {
        "n": 9,
        "status": "follows",
        "text": (
            "Bootstrap. Standard parabolic regularity: a bound on X and no blowup "
            "of ||omega||_infty upgrades to smoothness on [0, T]. "
            "If T is arbitrary, the solution is globally regular."
        ),
    },
]


RH_LINES = [
    {
        "n": 1,
        "status": "have",
        "text": (
            "Zeta. Riemann zeta is meromorphic, simple pole at s=1, "
            "Euler product for Re s > 1."
        ),
    },
    {
        "n": 2,
        "status": "have",
        "text": (
            "xi. The completed xi-function is entire of order 1 "
            "and satisfies a functional equation xi(s) = xi(1-s)."
        ),
    },
    {
        "n": 3,
        "status": "have",
        "text": (
            "Strip. Every non-trivial zero lies in 0 < Re s < 1."
        ),
    },
    {
        "n": 4,
        "status": "have",
        "text": (
            "Prime number theorem. No zeros on Re s = 1 "
            "(Hadamard / de la Vallee Poussin)."
        ),
    },
    {
        "n": 5,
        "status": "have",
        "text": (
            "The line. Infinitely many zeros on Re s = 1/2 (Hardy). "
            "A positive proportion sit on the line (Conrey and later). "
            "Literature, not a theorem of this desk."
        ),
    },
    {
        "n": 6,
        "status": "write",
        "text": (
            "WRITE. Every non-trivial zero has Re s = 1/2."
        ),
    },
    {
        "n": 7,
        "status": "follows",
        "text": (
            "Explicit formula. If (6) sits, the von Mangoldt explicit formula "
            "has all oscillatory terms on the critical line."
        ),
    },
    {
        "n": 8,
        "status": "follows",
        "text": (
            "Error term. The prime-counting error is then of the classical "
            "Riemann order (up to logs)."
        ),
    },
]


PROBLEMS = {
    "NS": {
        "id": "NS",
        "aliases": ("ns", "navier", "stokes", "xavier", "navi"),
        "slot": "B",
        "name": "3D Navier-Stokes global regularity",
        "object": {
            "name": "X",
            "slot": "B",
            "english": OBJECT["english"],
            "window": OBJECT["window"],
        },
        "theorem": (
            "Let u be a smooth solution of 3D incompressible Navier-Stokes "
            "(periodic or whole space), viscosity nu > 0, no Q1, keep 1/r^4. "
            "Let X = ||omega||_2^2. Then X stays finite on [0, T] for arbitrary T, "
            "and u remains smooth."
        ),
        "lines": NS_LINES,
        "chain_doc": "docs/NS-PROOF-CHAIN.md",
        "proceed": [row["claim"] for row in LEGAL],
        "if_write_sits": "If (6) sits, (7)-(9) give global regularity.",
        "do_not": "Do not graft Q1 onto B. Track A is a different equation.",
        "mine": MINE,
        "needed": NEEDED,
    },
    "RH": {
        "id": "RH",
        "aliases": ("rh", "riemann"),
        "slot": "RH",
        "name": "Riemann hypothesis",
        "object": {
            "name": "non-trivial zeros of zeta",
            "slot": "RH",
            "english": "every non-trivial zero of zeta has real part 1/2",
            "window": [
                "xi(s) = xi(1-s), entire of order 1",
                "need: Re rho = 1/2 for every non-trivial zero rho",
                "Track Q on this desk is inverse-GCD, not RH",
                "Theorem P is not the Riemann hypothesis",
            ],
        },
        "theorem": (
            "Every non-trivial zero of the Riemann zeta function "
            "has real part equal to 1/2."
        ),
        "lines": RH_LINES,
        "chain_doc": "docs/RH-PROOF-CHAIN.md",
        "proceed": [
            "a zero-free region that reaches Re s = 1/2",
            "a positivity certificate in the explicit formula that forces the line",
            "one new estimate that puts every zero on Re s = 1/2",
        ],
        "if_write_sits": "If (6) sits, (7)-(8) are the classical consequences.",
        "do_not": (
            "Do not glue inverse-GCD / Theorem P / Bridge* onto RH. "
            "Track Q is a different object."
        ),
        "mine": [],
        "needed": [],
    },
}

# Back-compat names for existing NS tests.
THEOREM = {"aimed": PROBLEMS["NS"]["theorem"], "object": WALL["target_B"], "form": WALL["looks_like"]}
LINES = NS_LINES


CLAIMS = [
    rec(
        "C1",
        "ask_for_the_chain",
        "You can tell DA to write a proof chain by naming the problem",
        "pass",
        "NS / Xavier Stokes / RH / Riemann. The operator does not need the chops.",
    ),
    rec(
        "C2",
        "chain_is_the_argument",
        "The written chain is the aimed theorem plus have / write / follows",
        "pass",
        "Ground floor up. Line WRITE is the attempt.",
    ),
    rec(
        "C3",
        "emit_is_qed",
        "Emitting the proof chain is QED",
        "fail",
        "The chain is the argument. WRITE is still a write.",
    ),
    rec(
        "C4",
        "llm_writes_line_6",
        "An LLM writes the WRITE line into a theorem",
        "fail",
        "It may phrase a candidate. The checker scores it.",
    ),
    rec(
        "C5",
        "nothing_wrong_with_asking",
        "Asking DA to write a proof chain is a category error",
        "fail",
        "Asking is the product. A fake last line is the refuse.",
    ),
    rec(
        "C6",
        "line_write_may_sit",
        "The WRITE line may sit later",
        "open",
        "That is the attempt. The aimed theorem follows if it sits.",
    ),
    rec(
        "C7",
        "q_is_rh",
        "Track Q / Theorem P is the Riemann hypothesis",
        "fail",
        "Inverse-GCD floors are not zeta zeros. No glue.",
    ),
    rec(
        "C8",
        "more_problems",
        "More named problems may get a ground-floor chain",
        "open",
        "A problem sits when the aimed theorem and the have/write/follows lines are typed.",
    ),
]


def parse_problem(ask: str = "", problem: str = "") -> str:
    text = f"{problem} {ask}".lower()
    if re.search(r"\brh\b|riemann", text):
        return "RH"
    if re.search(r"xavier|navi|\bstokes\b|\bns\b|navier", text):
        return "NS"
    if problem.upper() in PROBLEMS:
        return problem.upper()
    return "NS"


def is_proof_ask(ask: str) -> bool:
    """Write me the proof chain / NS / RH."""
    text = (ask or "").lower().strip()
    if not text:
        return False
    return bool(
        re.search(
            r"\bwrite (me )?(the )?proof\b|\bproof chain\b|"
            r"\bxavier stokes\b|\bnavi(er)?.?stokes\b|"
            r"\bda proof\b|\bthe proof for (ns|navier|rh|riemann)\b|"
            r"\brh\b|\briemann\b",
            text,
        )
    )


def print_problem_window(obj: dict) -> None:
    print("OBJECT WINDOW")
    print(f"  {obj['name']}  slot {obj['slot']}")
    print(f"  {obj['english']}")
    for line in obj["window"]:
        print(f"  {line}")


def run(out: Path | None = None, problem: str = "NS", ask: str = "") -> dict:
    pid = parse_problem(ask=ask, problem=problem)
    spec = PROBLEMS[pid]
    write_n = next(L["n"] for L in spec["lines"] if L["status"] == "write")
    payload = {
        "meta": {
            "question": f"write the proof chain for {pid}",
            "writeup": "docs/DA-PROOF.md",
            "chain": spec["chain_doc"],
            "problem": pid,
            "nothing_wrong_with_asking": True,
            "emit_is_not_qed": True,
            "q_is_not_rh": True,
            "operator_needs_no_chops": True,
        },
        "problem": pid,
        "problems": list(PROBLEMS),
        "theorem": {"aimed": spec["theorem"], "name": spec["name"]},
        "object": spec["object"],
        "lines": spec["lines"],
        "mine": spec["mine"],
        "needed": spec["needed"],
        "proceed": spec["proceed"],
        "if_write_sits": spec["if_write_sits"],
        "do_not": spec["do_not"],
        "write_n": write_n,
        "claims": CLAIMS,
        "counts": {
            "problems": len(PROBLEMS),
            "lines": len(spec["lines"]),
            "have": sum(1 for L in spec["lines"] if L["status"] == "have"),
            "write": sum(1 for L in spec["lines"] if L["status"] == "write"),
            "follows": sum(1 for L in spec["lines"] if L["status"] == "follows"),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "next_da_move": (
            f"Line ({write_n}) is the write. Classify one candidate. "
            "If it sits, the THEN lines follow. That is the close."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_proof.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_proof(out: Path | None = None, problem: str = "NS", ask: str = "") -> dict:
    payload = run(out=out, problem=problem, ask=ask)
    print_problem_window(payload["object"])
    print()
    print(f"PROBLEM {payload['problem']}")
    print("Problems on this desk:", ", ".join(payload["problems"]))
    print()
    print("THEOREM (aimed)")
    print(" ", payload["theorem"]["aimed"])
    print()
    print("PROOF CHAIN  (ground floor up)")
    for L in payload["lines"]:
        tag = {"have": "HAVE", "write": "WRITE", "follows": "THEN"}[L["status"]]
        print(f"  ({L['n']}) [{tag}] {L['text']}")
    print()
    print(payload["if_write_sits"])
    print(payload["do_not"])
    print("A candidate for the WRITE line:")
    for row in payload["proceed"]:
        print(f"  - {row}")
    print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    print("chain:", payload["meta"]["chain"])
    return payload


def main() -> int:
    problem = "NS"
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if args:
        problem = parse_problem(ask=" ".join(args))
    print_proof(problem=problem, ask=" ".join(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
