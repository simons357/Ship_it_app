#!/usr/bin/env python3
"""
DA hunt: proof-chain hunter.

The operator asked for a mode that understands how
the scored pieces connect. That is a graph. Nodes are
lemmas and blanks. Edges are pass, fail, open, or blocked.

The hunter does not write the leftover. An LLM may
phrase a sentence. It does not fill an open edge.
The object stays in a window you can look at.
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


OBJECT = {
    "name": "X",
    "slot": "B",
    "english": "enstrophy on classical 3D Navier-Stokes; keep 1/r^4; no Q1",
    "math": WALL["target_B"],
    "leftover": WALL["looks_like"],
    "window": [
        "X = ||omega||_2^2",
        "need int_0^T R(t) dt < infinity",
        WALL["looks_like"],
        "A1 (alignment in time, all data) is off / blank",
        "A2 (int ||lambda_2^+||, all data) is live on the box / blank as an a priori",
        "F is not this object",
    ],
    "look_is_not_a_bound": True,
}


# Live residual chain only. Not the full lemma catalog.
# kind: scored | blank | target
NODES = [
    {"id": "identity", "name": "enstrophy identity", "kind": "scored", "verdict": "pass",
     "math": "dX/dt + nu ||grad omega||_2^2 = -int omega·S omega (up to lower terms)"},
    {"id": "form", "name": "leftover form", "kind": "scored", "verdict": "pass",
     "math": WALL["looks_like"]},
    {"id": "B15", "name": "stretching budget on n=32", "kind": "scored", "verdict": "pass",
     "math": "B15 readable; B15e fail as an a priori"},
    {"id": "B37", "name": "three holes of R", "kind": "scored", "verdict": "pass",
     "math": "aligned P+ / unaligned P+ / off E_c; readable, not integrable"},
    {"id": "B38", "name": "Miller lambda_2^+ cut", "kind": "scored", "verdict": "pass",
     "math": "different cut from hole 2; not an a priori"},
    {"id": "B40", "name": "A1 off, A2 live on the box", "kind": "scored", "verdict": "pass",
     "math": "blanks named; naming is not the integral"},
    {"id": "B41", "name": "A2 along the B15 path", "kind": "scored", "verdict": "pass",
     "math": "flat ratio; not all-data int ||lambda_2^+||"},
    {"id": "A1", "name": "all-data alignment in time", "kind": "blank", "verdict": "open",
     "math": "would make hole 1 integrable if it held for all data"},
    {"id": "A2", "name": "all-data int ||lambda_2^+||", "kind": "blank", "verdict": "open",
     "math": "would make the live cubic integrable if it held for all data"},
    {"id": "R", "name": "integrable residual", "kind": "blank", "verdict": "open",
     "math": "int_0^T R(t) dt < infinity"},
    {"id": "B_regularity", "name": "classical regularity", "kind": "target", "verdict": "open",
     "math": "closed a priori for X; keep 1/r^4; no Q1"},
]


# How the desk actually connected them.
EDGES = [
    {"src": "identity", "dst": "form", "kind": "writes", "verdict": "pass",
     "why": "The identity produces the leftover inequality."},
    {"src": "form", "dst": "R", "kind": "needs", "verdict": "open",
     "why": "Gronwall needs integrable R. The form is not the integral."},
    {"src": "B15", "dst": "B37", "kind": "reads", "verdict": "pass",
     "why": "Same n=32 cache. Holes are a split of the stretching leftover."},
    {"src": "B37", "dst": "B38", "kind": "reads", "verdict": "pass",
     "why": "Miller cut is a different reading of the unaligned cubic."},
    {"src": "B37", "dst": "B40", "kind": "names", "verdict": "pass",
     "why": "Holes name the A1 / A2 blanks."},
    {"src": "B40", "dst": "B41", "kind": "reads", "verdict": "pass",
     "why": "A2 along the B15 path; ratio stays flat."},
    {"src": "B41", "dst": "A2", "kind": "does_not_give", "verdict": "fail",
     "why": "A flat box path is not all-data int ||lambda_2^+||."},
    {"src": "B40", "dst": "A1", "kind": "does_not_give", "verdict": "fail",
     "why": "A1 off on this box is not alignment for all data."},
    {"src": "A1", "dst": "R", "kind": "would_give", "verdict": "open",
     "why": "All-data alignment in time would make hole 1 integrable."},
    {"src": "A2", "dst": "R", "kind": "would_give", "verdict": "open",
     "why": "All-data int ||lambda_2^+|| would make the live cubic integrable."},
    {"src": "R", "dst": "B_regularity", "kind": "would_give", "verdict": "open",
     "why": "Integrable R plus Gronwall is the continuation. Not written."},
]


# Edges the process already killed. Connecting them again is not a hunt.
BLOCKED = [
    {"src": "A", "dst": "B", "why": "Q1-augmented NS does not imply classical B."},
    {"src": "L2", "dst": "BKM", "why": "Beale owns int ||omega||_infty. Nobody votes L2 into the max."},
    {"src": "B41", "dst": "R", "why": "A flat path is not integrable R."},
    {"src": "B37", "dst": "R", "why": "Readable holes are not integrable R."},
    {"src": "council", "dst": "R", "why": "A vote does not write the integral."},
    {"src": "LLM", "dst": "R", "why": "A generator may phrase. It does not fill an open edge."},
    {"src": "B42", "dst": "B_regularity", "why": "Leftover-close is not a lemma."},
    {"src": "n64", "dst": "B_regularity", "why": "A finer box is a knob on the check."},
    {"src": "F", "dst": "X", "why": "F is the U producing-map and fails."},
    {"src": "wall", "dst": "X", "why": "A seated wall is a veto, not a bound."},
    {"src": "SFE", "dst": "B", "why": "Shelved. Different PDE."},
    {"src": "TrackA", "dst": "B", "why": "Ladyzhenskaya stays on A. Do not slide epsilon."},
]


LEGAL = [
    {"id": "H_A1", "claim": "all-data alignment in time on a vorticity packet",
     "edge": "A1 → R", "do": "classify that sentence; do not cash CF-if"},
    {"id": "H_A2", "claim": "all-data int ||lambda_2^+|| on a vorticity packet",
     "edge": "A2 → R", "do": "classify that sentence; do not cash the n=32 path"},
    {"id": "H_R", "claim": "a different integrable residual on a vorticity packet",
     "edge": "form → R", "do": "classify the formula; do not invent leftover B42"},
    {"id": "H_kill", "claim": "a killing field for the stretching leftover",
     "edge": "identity → R", "do": "classify the field; do not retune the PDE"},
]


MEANING = {
    "uses_llm": True,
    "llm_does": "Phrase English into one killable claim. That is the generator.",
    "llm_does_not": "Fill an open edge. Write R. Vote. Unshelve SFE. Retune the PDE.",
    "context_that_sits": "The graph: which node, which edge, which veto, which object.",
    "meaning_that_sits": "classify → slot + pre-verdict + a checker that can kill it.",
    "english": (
        "Yes, we use an LLM. It phrases. "
        "Context that sits is the chain. "
        "Meaning that sits is classify. "
        "Understanding does not write R."
    ),
}


ILLEGAL = [
    {"claim": "leftover-close B42", "blocks": "B42 → B_regularity"},
    {"claim": "spawn n=64 as the proof", "blocks": "n64 → B_regularity"},
    {"claim": "graft Q1 onto classical NS", "blocks": "A → B"},
    {"claim": "BKM from L2", "blocks": "L2 → BKM"},
    {"claim": "the council / LLM writes R", "blocks": "council → R; LLM → R"},
    {"claim": "a seated wall is the bound", "blocks": "wall → X"},
]


CLAIMS = [
    rec(
        "H1",
        "hunter_walks_graph",
        "The hunter walks scored connections: what links, what is blocked, what is still open",
        "pass",
        "A graph of the residual chain. Not the full catalog replay.",
    ),
    rec(
        "H2",
        "object_window",
        "The object stays in a window you can look at",
        "pass",
        "X, the leftover form, A1/A2 blanks. Looking is allowed. Looking is not a bound.",
    ),
    rec(
        "H3",
        "hunter_is_the_graph",
        "The hunter is the graph of how this desk connected the pieces",
        "pass",
        "Propose / classify / kill / log on an edge. That is the process.",
    ),
    rec(
        "H4",
        "llm_fills_middle",
        "An LLM that understands context fills the open edge",
        "fail",
        "Both ends are already named. The wall is writing R. A generator may phrase a claim.",
    ),
    rec(
        "H5",
        "hunter_writes_R",
        "Hunting the chain writes the leftover",
        "fail",
        "A legal next is a claim to classify. The blanks stay blank until an estimate sits.",
    ),
    rec(
        "H6",
        "a_implies_b",
        "Connecting Track A to Track B is a legal hunt",
        "fail",
        "Q1 does not imply classical B. That edge is blocked.",
    ),
    rec(
        "H7",
        "bkm_from_l2",
        "Connecting L2 to BKM is a legal hunt",
        "fail",
        "Beale owns the max. That edge is blocked.",
    ),
    rec(
        "H8",
        "vote_or_b42",
        "A vote, leftover B42, or n=64 is a legal hunt",
        "fail",
        "Those edges are already killed.",
    ),
    rec(
        "H9",
        "look_writes_X",
        "Looking at the object window writes X",
        "fail",
        "The window is the object. It is not the estimate.",
    ),
    rec(
        "H10",
        "more_edges_later",
        "A new scored lemma may add an edge",
        "open",
        "An edge sits when a checker scores it. Do not invent leftover B42.",
    ),
    rec(
        "H11",
        "llm_phrases",
        "We use an LLM as the generator that phrases a claim",
        "pass",
        "Ordinary AI proposes. The operator does not need the chops. Phrasing is allowed.",
    ),
    rec(
        "H12",
        "meaning_is_classify",
        "Context that sits is the graph; meaning that sits is classify",
        "pass",
        "Which edge, which veto, which slot. Not a vibe. Not a séance.",
    ),
    rec(
        "H13",
        "understanding_writes_R",
        "An LLM that understands context and meaning writes the leftover",
        "fail",
        "Understanding is not the integral. H4 already killed the fill.",
    ),
]


def run(out: Path | None = None) -> dict:
    open_edges = [e for e in EDGES if e["verdict"] == "open"]
    payload = {
        "meta": {
            "question": "proof chain hunter: how the pieces connect",
            "writeup": "docs/DA-HUNT.md",
            "is_graph": True,
            "not_a_closer": True,
            "llm_does_not_fill": True,
            "uses_llm_to_phrase": True,
            "meaning_is_classify": True,
            "object_window": True,
            "does_not_write_X": True,
            "does_not_rerun_trackb": True,
        },
        "object": OBJECT,
        "nodes": NODES,
        "edges": EDGES,
        "blocked": BLOCKED,
        "meaning": MEANING,
        "legal": LEGAL,
        "illegal": ILLEGAL,
        "claims": CLAIMS,
        "counts": {
            "nodes": len(NODES),
            "edges": len(EDGES),
            "open_edges": len(open_edges),
            "blocked": len(BLOCKED),
            "legal": len(LEGAL),
            "illegal": len(ILLEGAL),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "open_edges": open_edges,
        "next_da_move": (
            "Look at the object. Pick one legal edge. Classify it. "
            "Do not fill R with a generator. Do not graft Q1 onto B."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_hunt.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_object_window(obj: dict | None = None) -> None:
    row = obj if obj is not None else OBJECT
    print("OBJECT WINDOW")
    print(f"  {row['name']}  slot {row['slot']}")
    print(f"  {row['english']}")
    for line in row["window"]:
        print(f"  {line}")
    print("  looking is allowed; looking is not a bound")


def print_hunt(out: Path | None = None, look: bool = False) -> dict:
    payload = run(out=out)
    print_object_window(payload["object"])
    if look:
        print()
        print("look only. Run hunt without --look for the chain.")
        print(f"wrote {payload['_wrote']}")
        return payload
    print()
    print("CHAIN  (how this desk connected the pieces)")
    for e in payload["edges"]:
        print(f"  [{e['verdict']}] {e['src']} --{e['kind']}--> {e['dst']}")
        print(f"           {e['why']}")
    print()
    print("BLOCKED  (do not connect these again)")
    for b in payload["blocked"]:
        print(f"  {b['src']} -x-> {b['dst']}: {b['why']}")
    print()
    print("MEANING")
    print(" ", payload["meaning"]["english"])
    print("  llm does:    ", payload["meaning"]["llm_does"])
    print("  llm does not:", payload["meaning"]["llm_does_not"])
    print("  context:     ", payload["meaning"]["context_that_sits"])
    print("  meaning:     ", payload["meaning"]["meaning_that_sits"])
    print()
    print("HUNT  legal next")
    for row in payload["legal"]:
        print(f"  {row['id']}  {row['edge']}")
        print(f"    claim: {row['claim']}")
        print(f"    do:    {row['do']}")
    print()
    print("HUNT  illegal")
    for row in payload["illegal"]:
        print(f"  {row['claim']}  ({row['blocks']})")
    print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return payload


def main() -> int:
    look = "--look" in sys.argv
    print_hunt(look=look)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
