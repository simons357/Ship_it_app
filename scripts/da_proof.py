#!/usr/bin/env python3
"""
DA proof: write the Navier-Stokes proof chain.

The operator says: write me the proof chain for
Navier-Stokes. Nothing is wrong with that. DA writes
the aimed theorem and the chain from this desk.

Line (k) is the next write. Emitting the chain is
not QED. Filling (k) is the attempt.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_from import MINE, NEEDED  # noqa: E402
from da_hunt import LEGAL, OBJECT, print_object_window  # noqa: E402
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


THEOREM = {
    "aimed": (
        "Let u be a smooth solution of 3D incompressible Navier-Stokes "
        "(periodic or whole space), viscosity nu > 0, no Q1, keep 1/r^4. "
        "Let X = ||omega||_2^2. Then X stays finite on [0, T] for arbitrary T, "
        "and u remains smooth."
    ),
    "object": WALL["target_B"],
    "form": WALL["looks_like"],
}


# The chain as a proof, not as a wall catalog.
LINES = [
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
        "text": (
            "Gronwall. From (3) and (6), X(t) stays finite on [0, T]."
        ),
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


CLAIMS = [
    rec(
        "C1",
        "ask_for_the_chain",
        "You can tell DA to write the proof chain for Navier-Stokes",
        "pass",
        "proof / write the proof / Xavier Stokes / Navi Stokes. That is the point.",
    ),
    rec(
        "C2",
        "chain_is_the_argument",
        "The written chain is the aimed theorem plus have / write / follows",
        "pass",
        "Lines 1-5 are this desk. Line 6 is the write. 7-9 follow if 6 sits.",
    ),
    rec(
        "C3",
        "emit_is_qed",
        "Emitting the proof chain is QED",
        "fail",
        "The chain is the argument. Line 6 is still a write.",
    ),
    rec(
        "C4",
        "llm_writes_line_6",
        "An LLM writes line 6 into a theorem",
        "fail",
        "It may phrase a candidate for (6). The checker scores it.",
    ),
    rec(
        "C5",
        "nothing_wrong_with_asking",
        "Asking DA to write the NS proof chain is a category error",
        "fail",
        "Asking is the product. A fake last line is the refuse.",
    ),
    rec(
        "C6",
        "line_6_may_sit",
        "Line 6 may sit later",
        "open",
        "That is the attempt. Regularity follows if it sits.",
    ),
]


def is_proof_ask(ask: str) -> bool:
    """Write me the proof chain for Navier-Stokes / Xavier Stokes."""
    text = (ask or "").lower().strip()
    if not text:
        return False
    return bool(
        re.search(
            r"\bwrite (me )?(the )?proof\b|\bproof chain\b|"
            r"\bxavier stokes\b|\bnavi(er)?.?stokes\b|"
            r"\bda proof\b|\bthe proof for (ns|navier)\b",
            text,
        )
    )


def run(out: Path | None = None) -> dict:
    payload = {
        "meta": {
            "question": "write the proof chain for Navier-Stokes",
            "writeup": "docs/DA-PROOF.md",
            "chain": "docs/NS-PROOF-CHAIN.md",
            "nothing_wrong_with_asking": True,
            "emit_is_not_qed": True,
        },
        "theorem": THEOREM,
        "object": OBJECT,
        "lines": LINES,
        "mine": MINE,
        "needed": NEEDED,
        "proceed": LEGAL,
        "claims": CLAIMS,
        "counts": {
            "lines": len(LINES),
            "have": sum(1 for L in LINES if L["status"] == "have"),
            "write": sum(1 for L in LINES if L["status"] == "write"),
            "follows": sum(1 for L in LINES if L["status"] == "follows"),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "next_da_move": (
            "Line 6 is the write. Classify one candidate. "
            "If it sits, 7-9 follow. That is the close."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_proof.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_proof(out: Path | None = None) -> dict:
    payload = run(out=out)
    print_object_window(payload["object"])
    print()
    print("THEOREM (aimed)")
    print(" ", payload["theorem"]["aimed"])
    print()
    print("PROOF CHAIN")
    for L in payload["lines"]:
        tag = {"have": "HAVE", "write": "WRITE", "follows": "THEN"}[L["status"]]
        print(f"  ({L['n']}) [{tag}] {L['text']}")
    print()
    print("If (6) sits, (7)-(9) give global regularity. That is the close.")
    print("A candidate for (6):")
    for row in payload["proceed"]:
        print(f"  {row['id']}: {row['claim']}")
    print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    print("chain: docs/NS-PROOF-CHAIN.md")
    return payload


def main() -> int:
    print_proof()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
