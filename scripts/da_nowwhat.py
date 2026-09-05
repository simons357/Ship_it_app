#!/usr/bin/env python3
"""
DA nowwhat: lost-operator council.

The operator is a normal person. They say "now what."
DA asks the seated papers — not ChatGPT freestyle —
"what would you try for the missing piece?"
Papers answer from published work. They do not endorse
this desk. A council is not a vote and not a close.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

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


# Papers that actually touch this leftover. Not the full roster.
# "would_try" is the next entry they would write. "cannot" is the veto.
COUNCIL = [
    {
        "who": "Tao",
        "bench": "living",
        "would_try": "A residual: a closed estimate for X, a killing field, or one preprint identity.",
        "cannot": "An averaged cousin that blows. That is a different equation.",
    },
    {
        "who": "Fefferman",
        "bench": "living",
        "would_try": "Depletion if the vorticity stays aligned in time. That if is A1.",
        "cannot": "Alignment for all data. Geometry waits on that if.",
    },
    {
        "who": "Constantin",
        "bench": "living",
        "would_try": "The same geometric if. CONC is not already aligned.",
        "cannot": "Cash a cover of shells as a bound.",
    },
    {
        "who": "Miller",
        "bench": "living",
        "would_try": "The middle-strain cut. lambda_2^+ is the live cubic on this box. That integral is A2.",
        "cannot": "A reading on n=32 as an a priori.",
    },
    {
        "who": "Beale",
        "bench": "living",
        "would_try": "Continuation from int ||omega||_infty. That is the criterion I own.",
        "cannot": "BKM from L2. Nobody votes a leftover list into the max.",
    },
    {
        "who": "Sverak",
        "bench": "living",
        "would_try": "Honest doors: Liouville, ancient, self-similar. Ask whether a door is a bound.",
        "cannot": "Possible as a theorem. Impossible as a theorem.",
    },
    {
        "who": "Escauriaza",
        "bench": "living",
        "would_try": "The L3 endpoint as a criterion. Bounded in L3 is a class.",
        "cannot": "A criterion as an a priori on enstrophy.",
    },
    {
        "who": "Seregin",
        "bench": "living",
        "would_try": "Local regularity / ESS. Sit the endpoint. Do not promote it.",
        "cannot": "Small singular set as no blowup.",
    },
    {
        "who": "Caffarelli",
        "bench": "living",
        "would_try": "Partial regularity. Measure zero is a theorem.",
        "cannot": "Small as empty. Olga is not in this room.",
    },
    {
        "who": "Koch",
        "bench": "living",
        "would_try": "Stay in the critical space for small data. That wall is why leftover knobs died.",
        "cannot": "Small critical as large-data regularity.",
    },
    {
        "who": "Tataru",
        "bench": "living",
        "would_try": "The same critical wall. Large data is still the object.",
        "cannot": "The critical space as the estimate.",
    },
    {
        "who": "Grujic",
        "bench": "living",
        "would_try": "Sparseness / log-bmo. The gap can shrink.",
        "cannot": "A weaker if as all-data A1.",
    },
    {
        "who": "Elgindi",
        "bench": "living",
        "would_try": "If you want a singularity, change the equation to Euler and say so.",
        "cannot": "An Euler blowup as an NS bound.",
    },
    {
        "who": "Hou",
        "bench": "living",
        "would_try": "A computed almost-singular run as a probe. Read it. Do not cash it.",
        "cannot": "Numerics as an a priori or as blowup.",
    },
    {
        "who": "Isett",
        "bench": "living",
        "would_try": "Onsager for Euler Holder 1/3. A different class.",
        "cannot": "Euler Holder as a bound on NS X.",
    },
    {
        "who": "Vicol",
        "bench": "living",
        "would_try": "Wild weak solutions. Say you changed class.",
        "cannot": "Convex integration as smooth blowup.",
    },
    {
        "who": "Albritton",
        "bench": "living",
        "would_try": "Forced Leray non-uniqueness. A different question.",
        "cannot": "Non-uniqueness as a bound on X.",
    },
    {
        "who": "Robinson",
        "bench": "living",
        "would_try": "An a posteriori certificate if you already have a numerical solution.",
        "cannot": "A certificate as an a priori.",
    },
    {
        "who": "Gibbon",
        "bench": "living",
        "would_try": "Stretching identities and strain-vorticity diagnostics. Name them.",
        "cannot": "An identity as a bound on X.",
    },
    {
        "who": "Ponce",
        "bench": "living",
        "would_try": "A commutator if you need a tool on the leftover term.",
        "cannot": "A tool as the estimate.",
    },
    {
        "who": "Leray",
        "bench": "past",
        "would_try": "Energy and dissipation. I own int X < infinity on these packets.",
        "cannot": "X in L^infty from that. I am not in the living room.",
    },
    {
        "who": "Ladyzhenskaya",
        "bench": "past",
        "would_try": "Put epsilon on a modified equation. That is Track A.",
        "cannot": "Slide epsilon onto classical NS. I stay on A.",
    },
]


CLAIMS = [
    rec(
        "N1",
        "lost_operator_council",
        "A lost operator can ask nowwhat and get the papers' next try",
        "pass",
        "Plain English. Seated work only. Not ChatGPT freestyle.",
    ),
    rec(
        "N2",
        "papers_not_minds",
        "The council is papers, not minds in the room",
        "pass",
        "They do not endorse this desk. Pretend-they-sit is a process name.",
    ),
    rec(
        "N3",
        "council_is_not_a_vote",
        "The council votes the missing piece into existence",
        "fail",
        "Twelve or twenty-five answers are a library. A vote cannot write R.",
    ),
    rec(
        "N4",
        "council_writes_leftover",
        "Asking the experts writes the leftover",
        "fail",
        "would_try is a claim to classify. cannot is a veto.",
    ),
    rec(
        "N5",
        "chatgpt_instead",
        "Ordinary AI freestyle replaces the council",
        "fail",
        "The generator may phrase. The next try must come from a seated paper.",
    ),
    rec(
        "N6",
        "more_chairs_later",
        "More leftover-relevant chairs may join the council",
        "open",
        "A chair sits when a paper touches this wall. Not a genius census.",
    ),
]


HERE = (
    "You are at the leftover on X. The proof steps before this "
    "are scored. The box can read the holes. It cannot write "
    "the integrals. You do not need the chops. Ask the papers."
)

MISSING = (
    "An integrable R, or all-data A1 (alignment in time), "
    "or all-data A2 (int ||lambda_2^+||), or a killing field. "
    "Not F. Not a new LIGO event. Not leftover B42."
)


def run(out: Path | None = None) -> dict:
    payload = {
        "meta": {
            "question": "now what; what would the papers try",
            "writeup": "docs/DA-NOWWHAT.md",
            "for_lost_operator": True,
            "papers_not_minds": True,
            "not_a_vote": True,
            "does_not_write_X": True,
        },
        "here": HERE,
        "missing": MISSING,
        "wall": WALL,
        "council": COUNCIL,
        "claims": CLAIMS,
        "counts": {
            "asked": len(COUNCIL),
            "living": sum(1 for c in COUNCIL if c["bench"] == "living"),
            "past": sum(1 for c in COUNCIL if c["bench"] == "past"),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "in_math": WALL["looks_like"],
        "target": WALL["target_B"],
        "next_da_move": (
            "Pick one would_try. Classify it. Do not vote. "
            "Do not graft Q1 onto B. Re-run feed if the rim is stale."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_nowwhat.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_nowwhat(out: Path | None = None) -> dict:
    payload = run(out=out)
    print("NOW WHAT")
    print(payload["here"])
    print()
    print("THE MISSING PIECE")
    print(payload["missing"])
    print()
    print("WHAT THE PAPERS WOULD TRY")
    print("(papers, not minds; they do not endorse this desk; not a vote)")
    for row in payload["council"]:
        print(f"  {row['who']} ({row['bench']})")
        print(f"    would try: {row['would_try']}")
        print(f"    cannot:    {row['cannot']}")
    print()
    print("IN MATH")
    print(" ", payload["in_math"])
    print(" ", payload["target"])
    print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return payload


def main() -> int:
    print_nowwhat()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
