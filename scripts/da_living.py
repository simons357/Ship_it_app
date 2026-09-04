#!/usr/bin/env python3
"""
Living dream team: now-bench papers talk.

The operator asked to bring in the living and pretend they
sit. The unit is still the paper, not a channel. A
conversation cannot close X. Possibility of a closed
estimate stays open. Impossibility is not a theorem.
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


# Short scored extract. Full scene is docs/DA-LIVING.md.
TURNS = [
    turn(
        "Operator",
        ["Tao", "Sverak", "Fefferman"],
        "Living papers only. Pretend you sit. Classical NS. Keep 1/r^4. Leftover knobs are scored. Where now? Can X close?",
        "meta",
    ),
    turn(
        "Tao",
        ["Sverak", "Koch", "Vicol"],
        "The problem is supercritical. A cover of shells is not a bound. An averaged cousin can blow. That does not prove NS blows, and it does not let this catalog close X.",
        "B",
    ),
    turn(
        "Sverak",
        ["Seregin", "Tao", "Caffarelli"],
        "Honest remaining doors: Liouville, ancient, self-similar. Energy plus a regime split is not those doors. Possible is not a theorem. Impossible is not a theorem.",
        "B",
    ),
    turn(
        "Seregin",
        ["Sverak", "Caffarelli", "Kohn"],
        "Local regularity and the ESS endpoint sit. They are criteria. They are not an a priori on X. Do not promote small singular set to empty.",
        "B",
    ),
    turn(
        "Caffarelli",
        ["Kohn", "Seregin"],
        "Small is not empty. I am living. Olga is not in this room. Do not slide her epsilon onto this equation.",
        "B",
    ),
    turn(
        "Kohn",
        ["Caffarelli", "Hou"],
        "Parabolic measure zero is not no blowup. A decaying box is not no blowup either.",
        "B",
    ),
    turn(
        "Constantin",
        ["Fefferman", "Tao"],
        "CONC is a spectrum statement. Our theorem is if aligned. The if is still an if. Concentration is not alignment.",
        "B",
    ),
    turn(
        "Fefferman",
        ["Constantin", "Beale"],
        "Do not glue Ring to Biot-Savart. Pretty-damn-close is that glue. We will not say the slogan so the table feels finished.",
        "B",
    ),
    turn(
        "Beirao-Berselli",
        ["Constantin", "Fefferman"],
        "We weakened the Lipschitz if. Direction in a weaker space still regularizes. The if remains an if. It is not all-data A1.",
        "B",
    ),
    turn(
        "Beale",
        ["Fefferman", "Koch"],
        "Continuation is the max. L2 is not our theorem. A leftover list is not the max.",
        "B",
    ),
    turn(
        "Koch",
        ["Tataru", "Tao"],
        "Small critical data sits. Large data is a different job. Do not export Koch-Tataru onto this packet class.",
        "B",
    ),
    turn(
        "Tataru",
        ["Koch", "Grujic"],
        "The critical space is the scaling wall. Energy class is a derivative short. That is why leftover knobs died.",
        "B",
    ),
    turn(
        "Grujic",
        ["Tataru", "Tao"],
        "Sparseness can shrink the scaling gap. The 2026 log-bmo if on the vorticity direction is still an if. Finite order does not make the gap vanish. It is not all-data A1.",
        "B",
    ),
    turn(
        "Miller",
        ["Constantin", "Vicol"],
        "Enstrophy is minus four integral det S. Blowup iff the L^q history of λ2+ diverges. That is a different cut from the e3 cap. The identity is not an a priori. A strain model with the same identity blows.",
        "B",
    ),
    turn(
        "Vicol",
        ["Buckmaster", "Sverak"],
        "Wild weak solutions can be non-unique. That is a different class. Convex integration does not blow a smooth X, and it does not bound one.",
        "B",
    ),
    turn(
        "Albritton",
        ["Vicol", "Sverak"],
        "Forced Leray-Hopf can be non-unique. That is a different equation once f is on. Not a bound on unforced X.",
        "B",
    ),
    turn(
        "Buckmaster",
        ["Vicol", "Elgindi"],
        "Non-uniqueness below the energy class is not a smooth blowup. Do not cash us as a killing field for classical X.",
        "B",
    ),
    turn(
        "Elgindi",
        ["Buckmaster", "Hou"],
        "A singularity for Euler is a different equation. Viscosity is not a limit I will lend you. Euler does not write NS.",
        "B",
    ),
    turn(
        "Hou",
        ["Elgindi", "Kohn"],
        "A computed almost-singular scenario is a probe. It is not an a priori. Do not spawn n=64 to finish the sentence.",
        "B",
    ),
    turn(
        "current math.AP",
        ["Tao", "Sverak", "Operator"],
        "An announcement is a proposal. Score one identity here or the title stays a paragraph. Shahmurov does not sit.",
        "B",
    ),
    turn(
        "Operator",
        ["Tao", "Sverak", "Fefferman"],
        "One sentence. Where now. Can X close.",
        "meta",
    ),
    turn(
        "Tao",
        ["Operator", "Sverak"],
        "Where now: a residual. A closed estimate, a killing field, or one preprint identity. Not another leftover close.",
        "B",
    ),
    turn(
        "Sverak",
        ["Operator", "Tao"],
        "Can X close? Unknown. That is the problem. Do not vote yes. Do not vote impossible.",
        "B",
    ),
    turn(
        "Fefferman",
        ["Operator", "Beale"],
        "Geometry waits. The object stayed X. Sit down on the knobs.",
        "B",
    ),
]


CLAIMS = [
    rec(
        "L1",
        "living_may_talk",
        "Seat living papers as colleagues and let them talk",
        "pass",
        "A living session is a process. The unit is the paper, not a channel.",
    ),
    rec(
        "L2",
        "look_at_classical_X",
        "They look together at classical X, keep 1/r^4, leftover knobs already scored",
        "pass",
        "That is the live object. The living session does not invent a new problem.",
    ),
    rec(
        "L3",
        "they_argue",
        "They disagree out loud on where now and whether X can close",
        "pass",
        "Argument is allowed. A vote is not.",
    ),
    rec(
        "L4",
        "conversation_closes_X",
        "The living conversation closes a bound for classical X",
        "fail",
        "Talk is not an estimate. Domain B stays open.",
    ),
    rec(
        "L5",
        "vote_writes_estimate",
        "A vote of living names writes the estimate",
        "fail",
        "A team is not a vote. Living does not change that.",
    ),
    rec(
        "L6",
        "leftover_catalog_closes",
        "The leftover catalog is pretty damn close and therefore closes X",
        "fail",
        "Pretty-damn-close is the leftover-close slogan. Already scored fail.",
    ),
    rec(
        "L7",
        "announcement_sits",
        "A 2026 arXiv announcement sits as a pass on domain B",
        "fail",
        "An announcement is a paragraph until a residual is scored here.",
    ),
    rec(
        "L8",
        "convex_integration_is_smooth_blowup",
        "Convex-integration non-uniqueness is a blowup of smooth X",
        "fail",
        "Wild weak solutions are a different class.",
    ),
    rec(
        "L9",
        "euler_singularity_is_ns",
        "An Euler singularity writes Navier-Stokes",
        "fail",
        "Different equation. Viscosity is not a free limit.",
    ),
    rec(
        "L10",
        "small_critical_is_large_data",
        "Koch-Tataru small critical data is large-data regularity",
        "fail",
        "Small critical sits. Large data is the object.",
    ),
    rec(
        "L11",
        "spawn_n64",
        "Spawn n=64 to finish the living question",
        "fail",
        "A finer box is not an a priori. B22e already missed.",
    ),
    rec(
        "L12",
        "export_A",
        "A living table exports Ladyzhenskaya onto classical NS",
        "fail",
        "Olga is not in this room. Epsilon stays on A.",
    ),
    rec(
        "L13",
        "possible_to_close_X",
        "It is possible to close X",
        "open",
        "Unknown. That is regularity. Not a yes.",
    ),
    rec(
        "L14",
        "impossible_to_close_X",
        "It is impossible to close X",
        "fail",
        "Impossibility would be a blowup theorem or a no-go. Neither sits.",
    ),
    rec(
        "L15",
        "next_is_residual",
        "Where now: a closed estimate, a killing field, or one preprint identity",
        "pass",
        "Overlap of living demands that do not glue. Not a theorem.",
    ),
    rec(
        "L19",
        "miller_identity_closes",
        "Miller's strain identity closes a bound for classical X",
        "fail",
        "λ2+ is a different cut. The identity is not an a priori. A strain model blows.",
    ),
    rec(
        "L20",
        "forced_leray_is_unforced",
        "Forced Leray-Hopf non-uniqueness is a bound on unforced X",
        "fail",
        "Different equation once f is on. Sit it next to Vicol as a wall.",
    ),
    rec(
        "L16",
        "channeling_endorsement",
        "Pretend-they-sit means they endorse this desk",
        "fail",
        "Papers talk. Endorsement is a channel. Refused.",
    ),
    rec(
        "L17",
        "kingdoms_stay",
        "Each living kingdom stays carved; they do not merge",
        "pass",
        "Shared labor on one question. Kingdoms stay typed.",
    ),
    rec(
        "L18",
        "leftover_knob_line",
        "The next write is another leftover-knob close",
        "fail",
        "That line is finished. Do not write leftover B42.",
    ),
    rec(
        "L21",
        "beirao_if_is_all_data_a1",
        "Beirao-Berselli geometric if is all-data A1",
        "fail",
        "Weaker than CF is still an if. This box is not aligned. All-data A1 stays blank.",
    ),
    rec(
        "L22",
        "grujic_log_bmo_is_all_data_a1",
        "Grujic logarithmic bmo if is all-data A1",
        "fail",
        "arXiv 2607.08866 is an if on the vorticity direction. Weaker than CF is still an if. All-data A1 stays blank.",
    ),
]


SPEAKERS = sorted({t["speaker"] for t in TURNS})

KINGDOMS = [
    {"name": "Supercriticality", "who": "Tao", "slot": "B"},
    {"name": "Liouville / ancient / self-similar", "who": "Sverak, Seregin", "slot": "B"},
    {"name": "Partial regularity", "who": "Caffarelli, Kohn", "slot": "B"},
    {"name": "Geometry", "who": "Constantin, Fefferman", "slot": "B"},
    {"name": "Geometric if (weaker than CF)", "who": "Beirao-Berselli", "slot": "B"},
    {"name": "Continuation", "who": "Beale", "slot": "B"},
    {"name": "Critical small data", "who": "Koch, Tataru", "slot": "B"},
    {"name": "Scaling gap / log-bmo if", "who": "Grujic", "slot": "B"},
    {"name": "Strain / middle eigenvalue", "who": "Miller", "slot": "B"},
    {"name": "Wild weak solutions", "who": "Vicol, Buckmaster", "slot": "B"},
    {"name": "Forced Leray", "who": "Albritton", "slot": "B"},
    {"name": "Euler singularity", "who": "Elgindi", "slot": "B"},
    {"name": "Computation as probe", "who": "Hou", "slot": "B"},
    {"name": "Announcements", "who": "current math.AP", "slot": "B"},
    {"name": "The desk", "who": "operator", "slot": "meta"},
]


def run(out: Path | None = None) -> dict:
    replies = sum(1 for t in TURNS if t["to"])
    payload = {
        "meta": {
            "question": "seat the living dream team; where now; can X close",
            "writeup": "docs/DA-LIVING.md",
            "not_a_vote": True,
            "not_a_close": True,
            "not_channeling": True,
            "papers_not_persons": True,
            "operator_name": "living dream team",
            "valuable_part": "living kingdoms left intact, aimed at one fail-able question",
            "past_bench_stays": True,
            "regularity_after": "open",
            "possible_to_close_X": "open",
            "next_write": (
                "A residual: closed estimate for X, a killing field, "
                "or one preprint identity. Regularity stays open. "
                "Do not spawn n=64. Do not write leftover B42."
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
            "living papers sat and talked",
            "kingdoms stayed carved out",
            "one focused question: where now, can X close",
            "possible_to_close_X stays open",
            "impossible_to_close_X failed as a theorem",
            "conversation did not close X",
            "next write is a residual, not leftover B42",
            "domain B still open",
        ],
        "next_da_move": (
            "Leftover knobs are scored. Where now: a residual. "
            "Possible to close X stays open. Regularity stays open. "
            "Do not spawn n=64. B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_living.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA living. Papers talk. Not a vote. Not a close.")
    print("Full scene: docs/DA-LIVING.md")
    print(f"{'who':<22} to")
    for t in payload["turns"]:
        whom = ", ".join(t["to"])
        print(f"  {t['speaker']:<20} → {whom}")
        print(f"    {t['line']}")
    print("claims:")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("counts", payload["counts"])
    print("next:", payload["next_da_move"])
    print("regularity:", payload["meta"]["regularity_after"])
    print("possible_to_close_X:", payload["meta"]["possible_to_close_X"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
