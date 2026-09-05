#!/usr/bin/env python3
"""
DA from: take the operator's scored steps to the break.

A regularity proof is a chain. DA can print the skeleton
and walk this desk's work until it stops being a proof.
It does not write the missing estimate. Proceed is a
claim to classify, not smoothness.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

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


# The operator's work, in proof order. a_priori False means
# it does not yet give a bound on X for all data.
MINE = [
    {
        "id": "S1",
        "name": "Leray energy",
        "verdict": "pass",
        "a_priori": False,
        "note": "int X < infinity on these packets. Not X in L^infty.",
    },
    {
        "id": "S2",
        "name": "enstrophy identity",
        "verdict": "pass",
        "a_priori": False,
        "note": "The identity is scored. It writes the leftover. It is not the bound.",
    },
    {
        "id": "S3",
        "name": "leftover form",
        "verdict": "pass",
        "a_priori": False,
        "note": WALL["looks_like"],
    },
    {
        "id": "S4",
        "name": "B15 stretching budget on n=32",
        "verdict": "pass",
        "a_priori": False,
        "note": "Readable. B15e: not an a priori.",
    },
    {
        "id": "S5",
        "name": "B16 enstrophy balance",
        "verdict": "pass",
        "a_priori": False,
        "note": "Visc owns the net on this box. B16e: not an a priori.",
    },
    {
        "id": "S6",
        "name": "B37 three holes of R",
        "verdict": "pass",
        "a_priori": False,
        "note": "Holes named. Readable is not integrable.",
    },
    {
        "id": "S7",
        "name": "B38 Miller lambda_2^+ cut",
        "verdict": "pass",
        "a_priori": False,
        "note": "A different cut from hole 2. Not an a priori.",
    },
    {
        "id": "S8",
        "name": "B40 A1 off, A2 live",
        "verdict": "pass",
        "a_priori": False,
        "note": "Blanks named. Naming is not the integral.",
    },
    {
        "id": "S9",
        "name": "B41 A2 along the B15 path",
        "verdict": "pass",
        "a_priori": False,
        "note": "Flat ratio. Not all-data int ||lambda_2^+||.",
    },
    {
        "id": "S10",
        "name": "all-data A1 / all-data A2 / integrable R",
        "verdict": "open",
        "a_priori": False,
        "break_here": True,
        "note": "The form needs int R < infinity. Neither integral is known for all data.",
    },
    {
        "id": "S11",
        "name": "Gronwall on X",
        "verdict": "open",
        "a_priori": False,
        "reached": False,
        "note": "Would follow from integrable R. Not reached.",
    },
    {
        "id": "S12",
        "name": "X in L^infty / Beale continuation",
        "verdict": "open",
        "a_priori": False,
        "reached": False,
        "note": "Beale owns int ||omega||_infty. L2 is not the max. Not reached.",
    },
    {
        "id": "S13",
        "name": "smoothness / global regularity",
        "verdict": "open",
        "a_priori": False,
        "reached": False,
        "note": "B_regularity. Keep 1/r^4. No Q1. Not written.",
    },
]


NEEDED = [
    {
        "step": "integrable R, or all-data A1, or all-data A2, or a killing field",
        "gives": "the leftover becomes a bound",
    },
    {
        "step": "Gronwall on that bound",
        "gives": "X stays finite on [0, T]",
    },
    {
        "step": "Beale or an equivalent continuation",
        "gives": "no blowup of ||omega||_infty",
    },
    {
        "step": "standard bootstrap",
        "gives": "smoothness on that interval; global if T is arbitrary",
    },
]


BREAK = {
    "id": "S10",
    "english": (
        "Your work writes the leftover form and reads the holes. "
        "It breaks where an all-data integrable R would sit. "
        "Box readings (B15-B41) do not cross that line."
    ),
    "math": (
        "Have: leftover inequality. "
        "Need: int_0^T R < infinity for all data, "
        "or all-data A1, or all-data A2, or a killing field."
    ),
    "not": (
        "Track A smoothness is a different PDE. "
        "A seated wall is a veto. "
        "A generator does not fill this edge."
    ),
}


CLAIMS = [
    rec(
        "P1",
        "skeleton_chain",
        "DA can print the regularity skeleton this desk is aiming at",
        "pass",
        "Needed steps after the leftover form. Not a filled proof.",
    ),
    rec(
        "P2",
        "walk_mine_to_break",
        "DA can walk the operator's scored steps to the first break",
        "pass",
        "S1-S9 are scored and not a priori. S10 is the break.",
    ),
    rec(
        "P3",
        "skeleton_is_regularity",
        "Printing the skeleton is global regularity",
        "fail",
        "A list of needed estimates is not smoothness.",
    ),
    rec(
        "P4",
        "analyze_writes_R",
        "Analyzing the break writes the leftover",
        "fail",
        "Diagnosis is not the integral.",
    ),
    rec(
        "P5",
        "track_a_proceeds",
        "Proceed from this work by sliding Track A onto B",
        "fail",
        "Ladyzhenskaya stays on A. Q1 does not imply classical B.",
    ),
    rec(
        "P6",
        "catalog_is_proceed",
        "The leftover catalog or a box path is the proceed to smoothness",
        "fail",
        "B15-B41 read the blank. They do not fill it.",
    ),
    rec(
        "P7",
        "llm_proceeds_to_smooth",
        "An LLM proceeds from the break to global regularity",
        "fail",
        "It may phrase one claim. It does not write R.",
    ),
    rec(
        "P8",
        "proceed_is_classify",
        "Proceed from this work is classify one legal estimate at the break",
        "pass",
        "A1, A2, a different R, or a killing field. Then the checker.",
    ),
    rec(
        "P9",
        "break_may_move",
        "A new scored all-data estimate may move the break",
        "open",
        "An edge sits when a checker scores it. Regularity stays open until then.",
    ),
]


def is_from_ask(ask: str) -> bool:
    """Analyze my steps / proceed toward regularity."""
    text = (ask or "").lower().strip()
    if not text:
        return False
    return bool(
        re.search(
            r"\bfrom my work\b|\bwhere it breaks\b|\bmy steps\b|"
            r"\bproceed\b|\bglobal regularity\b|\bsmoothness\b|"
            r"\bproof chain for ns\b|\banalyze (all )?(of )?my\b|"
            r"\bda from\b|\bbreaks here\b",
            text,
        )
    )


def run(out: Path | None = None) -> dict:
    brk = next(s for s in MINE if s.get("break_here"))
    payload = {
        "meta": {
            "question": "from my work: walk the steps to the break; proceed toward regularity",
            "writeup": "docs/DA-FROM.md",
            "takes_mine": True,
            "not_a_closer": True,
            "does_not_write_X": True,
            "track_a_does_not_imply_b": True,
        },
        "object": OBJECT,
        "mine": MINE,
        "break": BREAK,
        "needed": NEEDED,
        "proceed": LEGAL,
        "claims": CLAIMS,
        "counts": {
            "mine": len(MINE),
            "scored_not_a_priori": sum(
                1 for s in MINE if s["verdict"] == "pass" and not s["a_priori"]
            ),
            "needed": len(NEEDED),
            "proceed": len(LEGAL),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "break_id": brk["id"],
        "in_math": WALL["looks_like"],
        "target": WALL["target_B"],
        "next_da_move": (
            "You are at S10. Classify one legal estimate. "
            "Do not slide A onto B. Do not fill R with a generator."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_from.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_break_brief() -> None:
    print("BREAKS HERE")
    print(" ", BREAK["english"])
    print(" ", BREAK["math"])
    print("  full walk: python3 scripts/da_machine.py from")


def print_from(out: Path | None = None) -> dict:
    payload = run(out=out)
    print_object_window(payload["object"])
    print()
    print("YOUR STEPS  (this desk; scored; not a proof yet)")
    for s in payload["mine"]:
        mark = " BREAK" if s.get("break_here") else ""
        reached = "" if s.get("reached", True) else "  [not reached]"
        ap = "a priori" if s["a_priori"] else "not an a priori"
        print(f"  [{s['verdict']}] {s['id']} {s['name']}  ({ap}){mark}{reached}")
        print(f"           {s['note']}")
    print()
    print("BREAKS HERE")
    print(" ", payload["break"]["english"])
    print(" ", payload["break"]["math"])
    print(" ", payload["break"]["not"])
    print()
    print("A REGULARITY PROOF STILL NEEDS")
    for i, row in enumerate(payload["needed"], 1):
        print(f"  {i}. {row['step']}")
        print(f"      → {row['gives']}")
    print()
    print("FROM YOUR WORK  (legal next; not smoothness)")
    for row in payload["proceed"]:
        print(f"  {row['id']}  {row['edge']}")
        print(f"    claim: {row['claim']}")
        print(f"    do:    {row['do']}")
    print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return payload


def main() -> int:
    print_from()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
