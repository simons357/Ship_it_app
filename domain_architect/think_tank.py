"""Inner think tank: who actually knows this move, and what they refuse.

Insight is not a weld. Reputation does not fill GAP-T3. CosmoEvolution
is not on this bench.
"""

from __future__ import annotations

from typing import Any, Final


# Seats. Fluids names own Track B geometry. Computing names own the
# compiler discipline. Inverse/geometry names own "views of one object".
MEMBERS: Final[tuple[dict[str, str], ...]] = (
    {
        "name": "Jean Leray",
        "seat": "fluids",
        "knows": "energy class, Leray projector, the piece you can already see",
    },
    {
        "name": "Beale–Kato–Majda",
        "seat": "fluids",
        "knows": "vorticity stretching control; energy is not that integral",
    },
    {
        "name": "Caffarelli–Kohn–Nirenberg",
        "seat": "fluids",
        "knows": "partial regularity; a thin singular set is still the same equation",
    },
    {
        "name": "Constantin–Fefferman",
        "seat": "fluids",
        "knows": "alignment / depletion is a different piece than the tube weld",
    },
    {
        "name": "Constantin–Fefferman–Majda",
        "seat": "fluids",
        "knows": "swirl; a geometric identity in the tube is not a bound on X",
    },
    {
        "name": "Jacques Hadamard",
        "seat": "well-posedness",
        "knows": "a nearby problem is a different problem; extra E is not the original",
    },
    {
        "name": "Hassler Whitney",
        "seat": "geometry",
        "knows": "extension off a set is extra structure, not the object you had",
    },
    {
        "name": "Hermann Weyl",
        "seat": "geometry",
        "knows": "the form of the object; letters are a chart",
    },
    {
        "name": "Claude Shannon",
        "seat": "computing",
        "knows": "many encodings of one source are still one source",
    },
    {
        "name": "Richard Hamming",
        "seat": "computing",
        "knows": "you cannot inspect a missing identity into existence",
    },
    {
        "name": "Edsger Dijkstra",
        "seat": "computing",
        "knows": "unglued books; do not leak Q into B",
    },
    {
        "name": "David Parnas",
        "seat": "computing",
        "knows": "information hiding; Cosmo must not compile",
    },
)

# Frozen notes on the live scan. Not a vote. Not a proof.
INSIGHTS: Final[dict[str, tuple[dict[str, str], ...]]] = {
    "method": (
        {
            "name": "Hermann Weyl",
            "on": "the method",
            "says": (
                "The object is a form. Charts are textures. Many views of one "
                "form are still one object. Track B was an example of this, "
                "not the only object."
            ),
            "fills_gap": "no",
        },
        {
            "name": "Claude Shannon",
            "on": "views",
            "says": (
                "Many encodings of one source are still one source. An encoding "
                "from another book is a different source."
            ),
            "fills_gap": "no",
        },
        {
            "name": "Jacques Hadamard",
            "on": "LOOKS_LIKE_FIT",
            "says": (
                "A neighboring problem is a different problem. Extra structure "
                "is not the original object, whatever the object was."
            ),
            "fills_gap": "no",
        },
        {
            "name": "Hassler Whitney",
            "on": "filling the other side",
            "says": (
                "Extension off a set is extra structure. That rule does not "
                "care which book the set came from."
            ),
            "fills_gap": "no",
        },
        {
            "name": "Richard Hamming",
            "on": "empty scan",
            "says": (
                "You cannot test-in a missing identity. An empty catalog after "
                "a full scan is the honest result on any object."
            ),
            "fills_gap": "no",
        },
        {
            "name": "Edsger Dijkstra",
            "on": "unglued books",
            "says": (
                "The method is the same. The books stay unglued. Do not leak "
                "one object into another's hole because a letter matches."
            ),
            "fills_gap": "no",
        },
        {
            "name": "David Parnas",
            "on": "Cosmo",
            "says": (
                "Information hiding: visualization must not compile, for any "
                "book."
            ),
            "fills_gap": "no",
        },
    ),
    "scan": (
        {
            "name": "Jean Leray",
            "on": "anatomy",
            "says": (
                "The energy inequality is already stacked. That is the piece "
                "you can see. It does not determine the swirl weld."
            ),
            "fills_gap": "no",
        },
        {
            "name": "Beale–Kato–Majda",
            "on": "missing control",
            "says": (
                "The dangerous integral is vorticity stretching, not kinetic "
                "energy. Matching the energy tank onto CLIP-T3-WELD is the "
                "wrong piece."
            ),
            "fills_gap": "no",
        },
        {
            "name": "Caffarelli–Kohn–Nirenberg",
            "on": "holes vs object",
            "says": (
                "A thin set of holes can remain and the equation is still "
                "the same object. That is not a license to skip an open "
                "identity in the walk."
            ),
            "fills_gap": "no",
        },
        {
            "name": "Constantin–Fefferman",
            "on": "wrong slot",
            "says": (
                "Alignment / depletion is a different layer. Do not scan it "
                "into GAP-T3 because both live in vorticity language."
            ),
            "fills_gap": "no",
        },
        {
            "name": "Jacques Hadamard",
            "on": "LOOKS_LIKE_FIT",
            "says": (
                "Cylinder Young with h(R)=0 is a neighboring problem. Extra E. "
                "Well-posedness does not transfer from the toy outside."
            ),
            "fills_gap": "no",
        },
        {
            "name": "Hassler Whitney",
            "on": "CLIP-T3-OUTER",
            "says": (
                "Filling the other side of the cylinder is an extension. "
                "Extension is extra structure. It is not T^3."
            ),
            "fills_gap": "no",
        },
        {
            "name": "Hermann Weyl",
            "on": "views",
            "says": (
                "PDE, J/X, and SND-C are charts of one form. More charts do "
                "not invent a filler for the empty slot."
            ),
            "fills_gap": "no",
        },
        {
            "name": "Claude Shannon",
            "on": "three into one",
            "says": (
                "Three encodings of one source are still one source. A fourth "
                "encoding from Track Q is a different source."
            ),
            "fills_gap": "no",
        },
        {
            "name": "Richard Hamming",
            "on": "empty scan",
            "says": (
                "You cannot test-in a missing identity. An empty catalog after "
                "a full scan is the honest result."
            ),
            "fills_gap": "no",
        },
        {
            "name": "Edsger Dijkstra",
            "on": "wrong object",
            "says": (
                "Separation of concerns: inverse-GCD, gravity, and Cosmo do "
                "not belong in this hole even if a letter matches."
            ),
            "fills_gap": "no",
        },
    )
}


def _norm_topic(token: str) -> str:
    key = token.strip().upper().replace(" ", "")
    aliases = {
        "SCAN": "scan",
        "ANATOMY": "method",
        "METHOD": "method",
        "ANY": "method",
        "GENERAL": "method",
        "HOLE": "scan",
        "GAPT3": "scan",
        "B": "scan",
        "NS": "scan",
        "TRACKB": "scan",
        "Q": "method",
        "THINK": "method",
        "TANK": "method",
        "CONSULT": "method",
    }
    return aliases.get(key, "method")


def consult(topic: str = "scan") -> dict[str, Any]:
    """Ask the inner tank. They comment. They do not weld."""
    key = _norm_topic(topic)
    notes = [dict(row) for row in INSIGHTS.get(key, INSIGHTS["scan"])]
    return {
        "appendage": "THINK",
        "topic": key,
        "title": "Think tank consult — insight is not a weld",
        "not_a_proof": True,
        "members_on_this_move": list(MEMBERS),
        "notes": notes,
        "fills_found": 0,
        "rule": (
            "These people know this field. Their notes constrain the scan. "
            "None of them fill the empty slot by sitting on the bench."
        ),
        "next": "python -m domain_architect --scan",
    }


def format_consult(report: dict[str, Any] | None = None) -> str:
    data = report or consult("scan")
    lines = [
        data["title"],
        data["rule"],
        "",
        "Who knows this move",
    ]
    for member in data["members_on_this_move"]:
        lines.append(
            f"  {member['name']:28}  [{member['seat']}]  {member['knows']}"
        )
    lines.append("")
    lines.append("Notes on the live scan")
    for note in data["notes"]:
        lines.append(f"  {note['name']}  on {note['on']}  fills={note['fills_gap']}")
        lines.append(f"      {note['says']}")
    lines.append("")
    lines.append(f"Fills found: {data['fills_found']}. Insight is not a weld.")
    lines.append("Next: " + data["next"])
    return "\n".join(lines)
