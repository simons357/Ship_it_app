#!/usr/bin/env python3
"""
DA picture: advice from the published big-picture account
in each area. A survey can name the next write. Seeing
the whole field is not the estimate. Omniscience is not
a slot.
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


def area(
    aid: str,
    field: str,
    survey: str,
    who: str,
    picture: str,
    next_write: str,
    cannot: str,
    **extra,
) -> dict:
    row = {
        "id": aid,
        "field": field,
        "survey": survey,
        "who": who,
        "picture": picture,
        "next": next_write,
        "cannot": cannot,
    }
    row.update(extra)
    return row


# One comprehensive published account per area. Papers, not minds.
# "Most knowledge on earth" is not a census. A treatise is a picture.
AREAS = [
    area(
        "B",
        "classical 3D Navier-Stokes",
        "Lemarie-Rieusset, The Navier-Stokes Problem in the 21st Century (2016)",
        "Lemarie-Rieusset",
        (
            "The whole problem as it sits: energy, weak solutions, "
            "partial regularity, criteria, geometric ifs, local Leray. "
            "That is the map. The leftover on this desk is still X."
        ),
        (
            "Write one all-data integrable R, or all-data A1, or all-data A2. "
            "The monograph already listed the doors. A door is not the bound."
        ),
        "The book as the integral. Comprehensive is a map, not X in L^infty.",
        slot="B",
    ),
    area(
        "A",
        "Q1-augmented / modified-stress NS",
        "Ladyzhenskaya, The Mathematical Theory of Viscous Incompressible Flow",
        "Ladyzhenskaya",
        (
            "The modified stress at p>=5/2 in 3D is a different equation "
            "and it is closed. That is the comprehensive account of THIS PDE."
        ),
        (
            "Keep Theorem A on A. If you want classical, open Temam / "
            "Lemarie-Rieusset and write a uniform H1 as eps->0, or do not."
        ),
        "Export the modified-system book onto classical NS.",
        slot="A",
    ),
    area(
        "RH",
        "Riemann zeta / the line",
        "Titchmarsh, The Theory of the Riemann Zeta-Function (Heath-Brown)",
        "Titchmarsh",
        (
            "Zeta, xi, the strip, PNT, infinitely many on the line, "
            "explicit formula. That is the classical picture through (5)."
        ),
        (
            "WRITE: every non-trivial zero has Re s = 1/2. "
            "The treatise does not contain that line as a theorem."
        ),
        "A comprehensive zeta book as RH. Inverse-GCD as a chapter of Titchmarsh.",
        slot="RH",
    ),
    area(
        "Q",
        "inverse-GCD floors",
        "docs/SPECTRAL-FLOOR-EXPLORATION.md (this desk's retraction)",
        "this desk",
        (
            "Full Q>-1/2 false. H_N>=-1 proved. Theorem P proved. "
            "There is no comprehensive earth-expert who made this RH. "
            "The picture is the retraction."
        ),
        "Keep H_N>=-1 and Theorem P. To sharpen, H_N>=-1/4. Do not glue to zeros.",
        "A missing number-theory treatise as permission to glue Q to RH.",
        slot="Q",
    ),
    area(
        "SND",
        "occupation CONC / SPREAD",
        "Bony 1981 paraproduct + Constantin-Fefferman 1993 geometric if",
        "Bony / Constantin-Fefferman",
        (
            "Two pictures, not one brand. Paraproducts on SPREAD. "
            "Geometry if aligned on CONC. Occupation is not already aligned."
        ),
        "SPREAD: uniform SND-C as rho->0. CONC: A1 if. Neither is a bound on X.",
        "One comprehensive SND book that closes X.",
        slot="B",
    ),
    area(
        "H",
        "fluids H and arithmetic H_N",
        "Bony T+T*+R (fluids) and the pairing proof of H_N>=-1 (Q)",
        "Bony / this desk",
        (
            "Two comprehensive accounts. Fluids: paraproduct calculus. "
            "Arithmetic: a two-line pairing. They do not share a treatise."
        ),
        "Fluids: uniform low T in SPREAD. Arithmetic: keep -1; sharp is -1/4.",
        "One expert who sees both H's as one close.",
        slot="B / Q",
    ),
    area(
        "U",
        "program review (principle vs catalog)",
        "Einstein two-sided couple; Tesla a resonator you can detune",
        "Einstein / Tesla",
        (
            "The big picture on process: name the object, name the knob. "
            "A catalog of every paper is not a theory."
        ),
        (
            "Einstein: one object per job. Tesla: one detunable write "
            "(R, uniform H1, SND-C, or H_N>=-1/4). Then the script."
        ),
        "Sit as the most qualified and emit the leftover.",
        slot="U",
    ),
]


CLAIMS = [
    rec(
        "P1",
        "survey_names_next",
        "A published survey can name the next write from the picture of the field",
        "pass",
        "Lemarie-Rieusset, Ladyzhenskaya, Titchmarsh, Bony. The next line is already on this desk.",
    ),
    rec(
        "P2",
        "papers_not_omniscience",
        "The picture is a treatise, not the most knowledgeable mind on earth",
        "pass",
        "Genius is not a slot. Comprehensive means a book that covers the area.",
    ),
    rec(
        "P3",
        "picture_writes",
        "Someone who sees the whole field writes the leftover by seeing it",
        "fail",
        "The big picture is a map. The missing write is still the missing write.",
    ),
    rec(
        "P4",
        "qualified_vote",
        "The most qualified person is entitled to determine the close",
        "fail",
        "Qualification is a paper. Determination is an estimate that can fail.",
    ),
    rec(
        "P5",
        "q_has_a_sage",
        "Inverse-GCD has a comprehensive earth-expert who made it RH",
        "fail",
        "The picture on Q is the retraction. No sage authorizes the glue.",
    ),
    rec(
        "P6",
        "einstein_tesla_picture",
        "Einstein and Tesla review whether the picture is a principle or a catalog",
        "pass",
        "Object first. Knob second. They cannot output R.",
    ),
    rec(
        "P7",
        "more_surveys",
        "Another survey may join if it is a treatise of the same object",
        "open",
        "A new book sits when it covers the area. Not a genius census.",
    ),
    rec(
        "P8",
        "next_from_picture",
        "The next write named by the picture may sit later",
        "open",
        "Same writes: integrable R, uniform H1, SND-C, RH (6), H_N>=-1/4.",
    ),
]


def is_picture_ask(ask: str) -> bool:
    text = (ask or "").lower().strip()
    if not text:
        return False
    return bool(
        re.search(
            r"\bbig picture\b|\bcomprehensive\b|\bmost knowledge\b|"
            r"\bqualified to determine\b|\bda picture\b|"
            r"\bwhat would they do next\b|\badvice from\b|"
            r"\bwhole field\b|\bthe (big )?expert\b|\bsurvey chair\b",
            text,
        )
    )


def run(out: Path | None = None) -> dict:
    payload = {
        "meta": {
            "question": "advice from the published big-picture account; what they would do next",
            "writeup": "docs/DA-PICTURE.md",
            "papers_not_minds": True,
            "not_a_genius_census": True,
            "picture_is_not_the_estimate": True,
        },
        "areas": AREAS,
        "claims": CLAIMS,
        "counts": {
            "areas": len(AREAS),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "next_da_move": (
            "Read the picture. Take the named next write. Classify it. "
            "Do not ask the treatise to sit as the integral."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_picture.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_picture(out: Path | None = None) -> dict:
    payload = run(out=out)
    print("PICTURE  (survey of the field; next write; not omniscience)")
    print("A treatise can name what to do next. Seeing the whole is not the estimate.")
    print()
    for a in payload["areas"]:
        print(f"AREA {a['id']}  {a['field']}")
        print(f"  SURVEY  {a['who']} — {a['survey']}")
        print(f"  PICTURE {a['picture']}")
        print(f"  NEXT    {a['next']}")
        print(f"  CANNOT  {a['cannot']}")
        print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return payload


def main() -> int:
    print_picture()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
