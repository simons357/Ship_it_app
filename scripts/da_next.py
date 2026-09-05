#!/usr/bin/env python3
"""
DA next: now-what spoke. Hub, rim, wall, target, translate.

The operator asked for a comprehensive support system:
latest public data, the dream-team library, and an
interface that turns "what do we do from here" into math.
That is a spoke. It does not write the leftover.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_feed import SOURCES, format_freshness, freshness, run as feed_run  # noqa: E402
from da_now import WATCH, seated_living  # noqa: E402


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


WALL = {
    "where": "Track B residual, scored through B41 on the n=32 box",
    "english": (
        "The proof chain is correct up to the leftover. "
        "Viscosity still owns the net on this box. "
        "A1 (alignment in time for all data) is off. "
        "A2 (the middle-strain cubic) is live and did not blow "
        "on the B15 path. The wall is that neither integral "
        "is known for all data, so R is not known to be integrable."
    ),
    "looks_like": (
        "dX/dt + nu ||grad omega||_2^2 <= eps nu ||grad omega||_2^2 "
        "+ C_eps X R(t), with R unknown."
    ),
    "around": (
        "Write one all-data integral (A1 or A2), a different "
        "integrable R, or a killing field. Do not invent leftover "
        "B42. Do not spawn n=64. Do not graft Q1 onto B."
    ),
    "target_B": "X = ||omega||_2^2; need int_0^T R(t) dt < infinity",
    "target_U": "F is the producing-map on the SM poster. It fails. It is not the NS leftover.",
    "not_F": True,
}

SUGGESTIONS = [
    {
        "from": "Tao",
        "english": "Next entry is a residual: closed estimate, killing field, or one preprint identity.",
        "math": "Need a closed a priori for X, or a field that kills the stretching leftover.",
        "classify_as": "residual closed estimate on a vorticity packet",
        "not": "another leftover-close B42",
    },
    {
        "from": "Fefferman",
        "english": "The named if behind the wall is alignment in time.",
        "math": "A1: cos alpha_3 depletion in time for all data would make R integrable.",
        "classify_as": "alignment a priori on a vorticity packet",
        "not": "CF-if cashed as all-data A1",
    },
    {
        "from": "Miller",
        "english": "The live cubic on this box is the middle-strain cut.",
        "math": "A2: int ||lambda_2^+||_{L^q} for all data would make R integrable.",
        "classify_as": "lambda_2 plus integral on a vorticity packet",
        "not": "a box reading of A2 cashed as an a priori",
    },
]

SPOKES = [
    {"name": "feed", "command": "feed", "slot": "U/B", "does": "LIGO, LHC, PDG, arXiv math.AP"},
    {"name": "now", "command": "now", "slot": "U", "does": "living roster + watch"},
    {"name": "team", "command": "team", "slot": "U", "does": "past papers + experiment"},
    {"name": "living", "command": "living", "slot": "U", "does": "living papers talk; veto library"},
    {"name": "trackb", "command": "trackb", "slot": "B", "does": "lemma catalog; residual through B41"},
    {"name": "classify", "command": "classify", "slot": "meta", "does": "words to slot + pre-verdict"},
    {"name": "check B", "command": "check --domain B", "slot": "B", "does": "run the residual checker"},
    {"name": "nowwhat", "command": "nowwhat", "slot": "U / B", "does": "lost-operator council: 22 leftover papers"},
    {"name": "hunt", "command": "hunt", "slot": "U / B", "does": "proof-chain hunter: edges, blocks, object window"},
    {"name": "look", "command": "look", "slot": "B", "does": "object window anytime"},
    {"name": "from", "command": "from", "slot": "U / B", "does": "your steps to the break; proceed toward regularity"},
    {"name": "proof", "command": "proof", "slot": "B / A / RH", "does": "write the NS / A / RH proof chain"},
    {"name": "repair", "command": "repair", "slot": "U / A / B / Q", "does": "take A, SND, or H; name the fault and the write"},
    {"name": "attempt", "command": "attempt", "slot": "U / A / RH / Q", "does": "best A and RH; dream team looks; legal write"},
    {"name": "brute", "command": "brute", "slot": "U", "does": "finite list vs all-data write; quantum is not the estimate"},
    {"name": "picture", "command": "picture", "slot": "U", "does": "published survey names the next write; not a genius"},
]


def is_lost_ask(ask: str) -> bool:
    """Empty, 'now what', or 'what would you try' goes to the council."""
    text = (ask or "").lower().strip()
    if not text:
        return True
    return bool(
        re.search(
            r"\bnow\s*what\b|\bnowwhat\b|\bwhat would you\b|"
            r"\bmissing piece\b|\blost\b|\bdream team answer\b|"
            r"\bwhat would (they|the papers)\b|"
            r"\bsmartest\b|\bin history\b|\bwhat would you do now\b",
            text,
        )
    )


def translate(ask: str) -> dict:
    """Turn an operator sentence into a slot, English, and math."""
    text = ask.lower().strip()
    if not text:
        return {
            "ask": ask,
            "slot": "B",
            "chair": "Tao",
            "english": WALL["english"],
            "math": WALL["target_B"],
            "do_not": "Do not map F onto X. Do not cash LIGO as a bound.",
        }
    if re.search(r"\bf\b|realiz", text) and re.search(r"target|need|wall|next|what", text):
        return {
            "ask": ask,
            "slot": "U",
            "chair": "Einstein",
            "english": "The NS target is not F. F is the U producing-map and it fails.",
            "math": WALL["target_B"],
            "do_not": "Do not load realization into omega·Sω.",
        }
    if re.search(r"ligo|lhc|largo|gwtc|arxiv|pdg", text):
        return {
            "ask": ask,
            "slot": "U",
            "chair": "feed",
            "english": "Re-run feed. Latest public catalogs belong on the rim. They do not write the leftover.",
            "math": "A new math.AP item is a claim to classify, not a close of X.",
            "do_not": "GWTC and LHC stay off 1/r^4.",
        }
    if re.search(r"align|\bfefferman\b|\ba1\b|cos.?alpha", text):
        return {
            "ask": ask,
            "slot": "B",
            "chair": "Fefferman",
            "english": SUGGESTIONS[1]["english"],
            "math": SUGGESTIONS[1]["math"],
            "do_not": SUGGESTIONS[1]["not"],
        }
    if re.search(r"miller|lambda|strain|a2", text):
        return {
            "ask": ask,
            "slot": "B",
            "chair": "Miller",
            "english": SUGGESTIONS[2]["english"],
            "math": SUGGESTIONS[2]["math"],
            "do_not": SUGGESTIONS[2]["not"],
        }
    if re.search(r"around|wall|next|what|proof|fill|gap|middle", text):
        return {
            "ask": ask,
            "slot": "B",
            "chair": "Tao",
            "english": WALL["around"],
            "math": WALL["looks_like"],
            "do_not": "A conversation cannot fill the wall.",
        }
    return {
        "ask": ask,
        "slot": None,
        "chair": "classify",
        "english": "No spoke matched. Rephrase into A, B, Q, or U and run classify.",
        "math": "classify --claim '...'",
        "do_not": "Do not treat silence as a close.",
    }


CLAIMS = [
    rec(
        "W1",
        "hub_and_spoke",
        "DA sits in the middle; feed, dream team, and residual are spokes",
        "pass",
        "A support system is a rim. The hub still classifies and scores.",
    ),
    rec(
        "W2",
        "translate_words_to_math",
        "next can translate 'what now' into a math sentence",
        "pass",
        "Deterministic map: English ask → slot, chair, math. Not a genius.",
    ),
    rec(
        "W3",
        "target_is_X_not_F",
        "On Track B the target is X / integrable R, not F",
        "pass",
        "F is slot U and fails. Realization is not the NS leftover.",
    ),
    rec(
        "W4",
        "next_writes_leftover",
        "The next spoke writes the leftover",
        "fail",
        "A suggestion is a claim to classify. The wall is still R.",
    ),
    rec(
        "W5",
        "ligo_arxiv_closes_X",
        "Latest LIGO or arXiv announcement closes X",
        "fail",
        "Up to date is a U duty. A headline is not an a priori.",
    ),
    rec(
        "W6",
        "vote_fills_wall",
        "The dream team votes the middle of the proof chain into existence",
        "fail",
        "Papers veto and point. They do not write the integral.",
    ),
    rec(
        "W7",
        "realization_is_F_on_B",
        "The realization variable on B is F",
        "fail",
        "F stays on U. B target stays X.",
    ),
    rec(
        "W8",
        "next_is_leftover_b42",
        "next is leftover-close B42 or n=64",
        "fail",
        "Tao already blocked both. Knob on the check, not the PDE.",
    ),
    rec(
        "W9",
        "more_spokes_later",
        "More spokes may be added",
        "open",
        "A new spoke is a command plus a kill check. Not a unifier.",
    ),
    rec(
        "W10",
        "stale_feed_weaker",
        "A stale feed makes next weaker",
        "pass",
        "You need data to ask. Missing or >24h is stale. Re-run feed.",
    ),
]


def run(out: Path | None = None, ask: str = "", fetch: bool = False) -> dict:
    seated = seated_living()
    feed = feed_run(fetch=fetch)
    fresh = freshness()
    payload = {
        "meta": {
            "question": "now what: wall, target, suggestion, latest data",
            "writeup": "docs/DA-NEXT.md",
            "hub": "DA",
            "not_a_closer": True,
            "target_is_not_F": True,
            "does_not_write_X": True,
        },
        "wall": WALL,
        "spokes": SPOKES,
        "suggestions": SUGGESTIONS,
        "translate": translate(ask),
        "rim": {
            "seated_living": len(seated),
            "watch": [row["name"] for row in WATCH],
            "feed_sources": [s["name"] for s in SOURCES],
            "feed_ok": feed["counts"].get("ok", 0),
            "feed_items": feed["counts"].get("items", 0),
            "fetched": fetch,
            "freshness": fresh,
        },
        "claims": CLAIMS,
        "counts": {
            "spokes": len(SPOKES),
            "suggestions": len(SUGGESTIONS),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "next_da_move": (
            "Lost? Run nowwhat. Re-run feed. Classify one suggestion. "
            "Do not write leftover B42. Do not spawn n=64. "
            "F is not the NS target."
        ),
        "nowwhat": "python3 scripts/da_machine.py nowwhat",
        "lost_ask": is_lost_ask(ask),
    }
    dest = Path(out) if out is not None else Path("results/da_next.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    ask = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    payload = run(ask=ask, fetch=False)
    print("DA next. Hub, rim, wall.")
    print("Full note: docs/DA-NEXT.md")
    print("WHERE", payload["wall"]["where"])
    print("ENGLISH", payload["wall"]["english"])
    print("MATH", payload["wall"]["looks_like"])
    print("TARGET B", payload["wall"]["target_B"])
    print("TARGET U", payload["wall"]["target_U"])
    print("AROUND", payload["wall"]["around"])
    print(format_freshness(payload["rim"].get("freshness")))
    tr = payload["translate"]
    if tr.get("ask"):
        print("ASK", tr["ask"])
        print("→", tr["slot"], tr["chair"])
        print("  ", tr["english"])
        print("  ", tr["math"])
    for s in payload["suggestions"]:
        print(f"  try [{s['from']}] {s['math']}")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("counts", payload["counts"])
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
