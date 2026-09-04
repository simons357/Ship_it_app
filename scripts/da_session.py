#!/usr/bin/env python3
"""
Working session: the dream team talks as colleagues.

A conversation is a process. The operator's name for it is
a virtual séance: kingdoms left intact, one focused
problem. It does not close regularity, export A to B, or
write F. Next write stays Hardy → I_tube.
"""

from __future__ import annotations

import json
from pathlib import Path


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


def turn(speaker: str, to: list[str], line: str, slot: str) -> dict:
    return {"speaker": speaker, "to": to, "line": line, "slot": slot}


# Short scored extract. Full scene is docs/DA-SESSION.md.
TURNS = [
    turn(
        "Operator",
        ["Leray", "Kato", "Ladyzhenskaya"],
        "Sit as colleagues. Look at classical NS. Keep 1/r^4. Work together. One honest write.",
        "meta",
    ),
    turn(
        "Leray",
        ["Kato", "Beale", "Majda"],
        "Energy and integrable X are mine. They do not put X in L^∞. Do not close the cubic ODE from my integral.",
        "B",
    ),
    turn(
        "Kato",
        ["Leray", "Beale", "Majda"],
        "Continuation needs ∫‖ω‖_∞. L² is not our theorem. We will sit for the a priori job; we will not rename it.",
        "B",
    ),
    turn(
        "Caffarelli",
        ["Kohn", "Nirenberg", "Leray"],
        "Partial regularity: small is not empty. Keep us as a wall, not a global pass.",
        "B",
    ),
    turn(
        "Constantin",
        ["Fefferman", "Leray"],
        "Stretching dies if aligned. The if is load-bearing. Geometry after the tube, not instead of it.",
        "B",
    ),
    turn(
        "Fefferman",
        ["Constantin", "Kato"],
        "Ring on E_c is not all-data cos α_3 → 0. We will not say the slogan to make the table feel finished.",
        "B",
    ),
    turn(
        "Ladyzhenskaya",
        ["Leray", "Kato", "Caffarelli"],
        "I finish a modified stress. I will show you the weights in the tube. I will not slide ε into your equation.",
        "A",
    ),
    turn(
        "Kohn",
        ["Caffarelli", "Feynman", "Tesla"],
        "B4b means leftover I_tube versus viscous budget at δ ~ 2^{-j*}. A bad tube kills it. That is a clean check.",
        "B",
    ),
    turn(
        "Feynman",
        ["Kohn", "Tesla"],
        "Good. A number you can miss. No close without that residual.",
        "U",
    ),
    turn(
        "Tesla",
        ["Ladyzhenskaya", "Feynman"],
        "δ and j* are knobs. If you detune δ and the script does not move, you have a paragraph, not an apparatus.",
        "U",
    ),
    turn(
        "Einstein",
        ["Operator", "Weinberg"],
        "Keep the classical object named. Do not change the PDE to look finished. Couplings are the other chair.",
        "U",
    ),
    turn(
        "Weinberg",
        ["Einstein", "PDG"],
        "The W³–B rotation is real. It does not absorb I_tube. If you hunt θ_W in a vortex, I leave.",
        "U",
    ),
    turn(
        "von Neumann",
        ["Weyl", "Wigner"],
        "The unknown is X = ‖ω‖_2². Write an estimate or store a residual. Do not open a slot on the word modes.",
        "U",
    ),
    turn(
        "Majda",
        ["Leray", "Ladyzhenskaya", "Fefferman"],
        "Joint plan: energy, unused L^∞ criterion, partial regularity as a wall, geometry later, Olga on weights not on the PDE. Then Hardy → I_tube.",
        "B",
    ),
    turn(
        "Kato",
        ["Operator", "Leray", "Beale"],
        "Slot B. Sentence: Hardy plus wall absorbs I_tube at δ ~ 2^{-j*}, or it does not. Check: a killing tube field, or a closed estimate.",
        "B",
    ),
    turn(
        "Beale",
        ["Kato", "Operator"],
        "Nobody votes this into global regularity. A lemma pass leaves domain B open. A lemma fail is still science.",
        "B",
    ),
]


CLAIMS = [
    rec(
        "S1",
        "colleagues_may_talk",
        "Seat the benches as colleagues and let them talk to each other",
        "pass",
        "A working session is a process. People being gone does not matter. The papers still talk.",
    ),
    rec(
        "S2",
        "look_at_live_B",
        "They look together at classical NS, keep 1/r^4, next write Hardy → I_tube",
        "pass",
        "That is the live object. The session does not invent a new problem.",
    ),
    rec(
        "S3",
        "help_without_glue",
        "They help each other without changing the PDE or exporting A",
        "pass",
        "Ladyzhenskaya on weights; BKM unused as L^∞; CKN as a wall; CF later. Shared labor, same equation.",
    ),
    rec(
        "S4",
        "lock_next_write",
        "They lock Hardy → I_tube at δ ~ 2^{-j*}, then energy-class low Bony T",
        "pass",
        "Overlap of suggestions that do not glue. Not a theorem. The next write already on the desk.",
    ),
    rec(
        "S5",
        "conversation_closes_regularity",
        "The conversation closes classical regularity",
        "fail",
        "Talk is not an estimate for X. Domain B stays open.",
    ),
    rec(
        "S6",
        "vote_writes_theorem",
        "A vote at the table writes a theorem",
        "fail",
        "A team is not a vote. A vote cannot close.",
    ),
    rec(
        "S7",
        "ladyzhenskaya_exports_A",
        "Ladyzhenskaya exports A ⇒ B by sitting here",
        "fail",
        "She said so. ε stays on A.",
    ),
    rec(
        "S8",
        "bkm_from_l2",
        "Beale–Kato–Majda accept an L² continuation criterion",
        "fail",
        "They refused the rename. L^∞ is the point.",
    ),
    rec(
        "S9",
        "all_data_depletion",
        "Constantin–Fefferman grant all-data cos α_3 → 0",
        "fail",
        "The if is load-bearing. Ring is not alignment.",
    ),
    rec(
        "S10",
        "session_writes_F",
        "Einstein, Weinberg, or PDG write F from the session",
        "fail",
        "Wrong chair. Couplings stay a bag.",
    ),
    rec(
        "S11",
        "virtual_seance_as_name",
        "Call this a virtual séance: published kingdoms at one table on one focused problem",
        "pass",
        "The operator's name for the process. Papers talk. People being gone does not matter.",
    ),
    rec(
        "S12",
        "kingdoms_stay_carved",
        "Each mind keeps the kingdom they carved; they do not merge into one mind",
        "pass",
        "That is the valuable part. Shared labor on one problem. Kingdoms stay typed.",
    ),
    rec(
        "S13",
        "sarcastic_channel",
        "A sarcastic séance: spirits, a vote, a finished theorem",
        "fail",
        "That use is still refused. Virtual is the table. It is not a channel.",
    ),
    rec(
        "S14",
        "unify_the_kingdoms",
        "Put every kingdom on every problem at once and call that a unifier",
        "fail",
        "That is a bag again. One focused problem, or it is not this method.",
    ),
]


SPEAKERS = sorted({t["speaker"] for t in TURNS})

KINGDOMS = [
    {"name": "Energy", "who": "Leray", "slot": "B"},
    {"name": "Continuation", "who": "Beale, Kato, Majda", "slot": "B"},
    {"name": "Partial regularity", "who": "Caffarelli, Kohn, Nirenberg", "slot": "B"},
    {"name": "Geometry", "who": "Constantin, Fefferman", "slot": "B"},
    {"name": "Extra dissipation", "who": "Ladyzhenskaya", "slot": "A"},
    {"name": "Principle", "who": "Einstein", "slot": "U"},
    {"name": "Mixing", "who": "Weinberg", "slot": "U"},
    {"name": "Apparatus", "who": "Tesla", "slot": "U"},
    {"name": "A missable number", "who": "Feynman", "slot": "U"},
    {"name": "Group / type / space", "who": "Weyl, Wigner, von Neumann", "slot": "U"},
    {"name": "The numbers", "who": "PDG, neutrino / cosmology", "slot": "U"},
    {"name": "The desk", "who": "operator", "slot": "meta"},
]


def run(out: Path | None = None) -> dict:
    replies = sum(1 for t in TURNS if t["to"])
    payload = {
        "meta": {
            "question": "have the dream team converse as colleagues on the live problem",
            "writeup": "docs/DA-SESSION.md",
            "not_a_vote": True,
            "not_a_close": True,
            "not_channeling": True,
            "virtual_seance": True,
            "operator_name": "virtual séance",
            "valuable_part": "kingdoms left intact, aimed at one fail-able problem",
            "program_review_sits": True,
            "now_bench_sends_a_note": True,
            "regularity_after": "open",
            "next_write": (
                "Hardy → I_tube at δ ~ 2^{-j*}, then energy-class low Bony T. "
                "Regularity stays open."
            ),
        },
        "turns": TURNS,
        "claims": CLAIMS,
        "speakers": SPEAKERS,
        "kingdoms": KINGDOMS,
        "counts": {
            "turns": len(TURNS),
            "speakers": len(SPEAKERS),
            "addressed_replies": replies,
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "how_far": [
            "they sat and talked",
            "kingdoms stayed carved out",
            "one focused problem: Hardy → I_tube",
            "virtual séance as a name for the process",
            "they refused glue and refused a vote",
            "next write unchanged",
            "domain B still open",
        ],
        "next_da_move": (
            "Tube write is in. Use B4c inside 3-CONC. Then low Bony T on SPREAD."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_session.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA session. Colleagues at one table. Not a vote. Not a close.")
    print("Full scene: docs/DA-SESSION.md")
    print(f"{'who':<16} to")
    for t in payload["turns"]:
        whom = ", ".join(t["to"])
        print(f"  {t['speaker']:<14} → {whom}")
        print(f"    {t['line']}")
    print("claims:")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print("regularity:", payload["meta"]["regularity_after"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
