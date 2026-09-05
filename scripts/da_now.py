#!/usr/bin/env python3
"""
Living roster: seated papers + watch list.

The operator asked for modern living geniuses, especially
those involved in this desk. Genius is not a slot. The unit
is still the paper. A complete world list is omniscience;
that claim fails. A vote of names does not write X.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_living import SPEAKERS  # noqa: E402
from da_pipe import NOW  # noqa: E402


DEAD = {
    "Leray",
    "Kato",
    "Majda",
    "Ladyzhenskaya",
    "Nirenberg",
    "Scheffer",
    "Sohr",
    "Foias",
        "Heywood",
        "Bourgain",
        "Pruss",
    }

NOT_A_PERSON = {"Operator", "current math.AP", "operator"}

# Living chairs whose papers can sit. Not seated as walls.
# Do not auto-seat. Do not treat as a close.
WATCH = [
    {
        "name": "Prange",
        "slot": "B",
        "kingdom": "anomalous dissipation / ancient",
        "involved": "often with Barker; selection and blow-up limits",
        "do_not": "seat a second Type I / ancient chair next to Barker",
    },
    {
        "name": "Titi",
        "slot": "B",
        "kingdom": "a posteriori / data assimilation",
        "involved": "Chernyshenko–Constantin–Robinson–Titi cluster",
        "do_not": "seat as a twin of Robinson; Constantin already sits",
    },
    {
        "name": "Shvydkoy",
        "slot": "B",
        "kingdom": "Onsager lectures",
        "involved": "energy conservation / Onsager",
        "do_not": "seat as a twin of Isett or Cheskidov",
    },
    {
        "name": "Friedlander",
        "slot": "B",
        "kingdom": "hydrodynamic instability",
        "involved": "instability of Euler / MHD",
        "do_not": "seat as a twin of Elgindi or Isett",
    },
    {
        "name": "Coti Zelati",
        "slot": "B",
        "kingdom": "Kolmogorov 4/5 / mixing",
        "involved": "Bedrossian-Coti Zelati-Punshon-Smith-Weber 4/5; also mixing",
        "do_not": "seat as a second 4/5 chair next to Bedrossian",
    },
    {
        "name": "Staffilani",
        "slot": "B",
        "kingdom": "BMO-1 regularity of small Koch-Tataru solutions",
        "involved": "Germain-Pavlovic-Staffilani; already covered as Koch-Tataru plus Pavlovic",
        "do_not": "seat as a twin of Koch-Tataru or Pavlovic",
    },
    {
        "name": "Imbert",
        "slot": "B",
        "kingdom": "kinetic / Boltzmann / Fokker-Planck",
        "involved": "often with Silvestre on kinetic equations",
        "do_not": "seat as a second kinetic chair next to Silvestre",
    },
    {
        "name": "Kenig",
        "slot": "B",
        "kingdom": "unique continuation",
        "involved": "unique continuation for NS / parabolic systems",
        "do_not": "seat as a twin of Kukavica",
    },
    {
        "name": "Maynard",
        "slot": "Q",
        "kingdom": "bounded gaps",
        "involved": "prime gaps; live arithmetic",
        "do_not": "map a gap theorem onto omega·Sω",
    },
]


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


def seated_living() -> list[str]:
    names = []
    for who in SPEAKERS:
        if who in DEAD or who in NOT_A_PERSON:
            continue
        names.append(who)
    return sorted(set(names))


def collaborations() -> list[dict]:
    rows = []
    for row in NOW:
        rows.append(
            {
                "name": row["name"],
                "slot": row["slot"],
                "reads": row["reads"],
                "cannot": row["cannot"],
            }
        )
    extra = [
        {
            "name": "ATLAS / CMS / LHCb",
            "slot": "U",
            "reads": "LHC collision catalogs and public notes",
            "cannot": "why the poster numbers; write F; close X",
        },
    ]
    have = {r["name"] for r in rows}
    for row in extra:
        if row["name"] not in have:
            rows.append(row)
    return rows


CLAIMS = [
    rec(
        "N1",
        "roster_belongs",
        "A living roster of seated papers and collaborations belongs on the desk",
        "pass",
        "Especially involved means the living fluids bench plus the pipes. Papers, not a channel.",
    ),
    rec(
        "N2",
        "complete_genius_list",
        "This is a complete list of living geniuses in the world",
        "fail",
        "Omniscience already failed on the pipe. A desk list is a slice, not the world.",
    ),
    rec(
        "N3",
        "genius_vote_writes_X",
        "A vote of living geniuses writes a bound for classical X",
        "fail",
        "A team is not a vote. Genius is not a slot.",
    ),
    rec(
        "N4",
        "celebrity_iq_sits",
        "A celebrity IQ list sits as science on this desk",
        "fail",
        "The unit is the paper. Fame is not a kingdom.",
    ),
    rec(
        "N5",
        "ligo_people_write_X",
        "LIGO or LHC people write a bound on X",
        "fail",
        "Strain and collision catalogs stay on U. They are not 1/r^4.",
    ),
    rec(
        "N6",
        "watch_list_is_a_close",
        "The watch list sits as a close or as leftover B42",
        "fail",
        "Watch is not seated. Do not write leftover B42.",
    ),
    rec(
        "N7",
        "especially_involved",
        "Especially involved is the seated living fluids plus the experimental pipes",
        "pass",
        "That is the working set. The watch list is next papers, not a vote.",
    ),
    rec(
        "N8",
        "shahmurov_sits",
        "Shahmurov sits on the living roster",
        "fail",
        "Already refused. An announcement is not a chair.",
    ),
    rec(
        "N9",
        "dead_fluids_on_roster",
        "A dead fluid sits on this living roster",
        "fail",
        "Leray, Kato, Majda, Olga, Nirenberg, Scheffer, Sohr, Foias, Heywood, Bourgain, Pruss stay out.",
    ),
    rec(
        "N10",
        "more_chairs_later",
        "More living chairs may be added when a paper is scored",
        "open",
        "The collection is ongoing. A name is not a seat until a wall is scored.",
    ),
]


def run(out: Path | None = None) -> dict:
    seated = seated_living()
    watch_names = {row["name"] for row in WATCH}
    overlap = sorted(watch_names.intersection(seated))
    dead_on_roster = sorted(DEAD.intersection(seated))
    payload = {
        "meta": {
            "question": "list living chairs involved in this desk; not a world genius census",
            "writeup": "docs/DA-NOW.md",
            "genius_is_not_a_slot": True,
            "papers_not_persons": True,
            "not_a_vote": True,
            "not_omniscience": True,
            "does_not_write_X": True,
        },
        "seated_living": seated,
        "collaborations": collaborations(),
        "watch": WATCH,
        "dead_stay_out": sorted(DEAD),
        "claims": CLAIMS,
        "counts": {
            "seated_living": len(seated),
            "collaborations": len(collaborations()),
            "watch": len(WATCH),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
            "watch_already_seated": overlap,
            "dead_on_roster": dead_on_roster,
        },
        "how_far": [
            "seated living fluids derived from the living session",
            "collaborations include LVK, EHT, DESI, LHC detectors",
            "watch list is not a seat",
            "complete world-genius claim failed",
            "genius vote does not write X",
        ],
        "next_da_move": (
            "Re-run feed for new catalogs. Score one watch paper before seating it. "
            "Do not write leftover B42. Do not spawn n=64."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_now.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA now. Living roster. Genius is not a slot.")
    print("Full list: docs/DA-NOW.md")
    print("seated living:")
    for name in payload["seated_living"]:
        print(f"  {name}")
    print("collaborations:")
    for row in payload["collaborations"]:
        print(f"  {row['name']:<28} → {row['slot']}")
    print("watch (not seated):")
    for row in payload["watch"]:
        print(f"  {row['name']:<16} {row['slot']}  {row['kingdom']}")
    print("claims:")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("counts", payload["counts"])
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
