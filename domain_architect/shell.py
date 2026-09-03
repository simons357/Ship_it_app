"""Inside plus an outer shell: the silhouette can identify a known object.

You look at the interior (stacked pieces). You put a shell around it so
the object has a readable shape. That outline may be a dead giveaway for
something already in the catalog. Identification is not smoothness.
An invented shell (even-reflect, extra E) is play, not the original object.

Track B is the worked example. The method is general.
"""

from __future__ import annotations

from typing import Any, Final

from .desk import LIBRARY_OBJECTS, compare_shape
from .overlay import overlay_report
from .think_tank import consult


def match_silhouette(shape: str) -> dict[str, Any]:
    """Catalog objects whose shape is this silhouette. Not a weld."""
    hits = [
        {"id": name, "book": meta["book"], "texture": meta["texture"]}
        for name, meta in LIBRARY_OBJECTS.items()
        if meta["shape"] == shape
    ]
    return {
        "shape": shape,
        "hits": hits,
        "hit_count": len(hits),
        "already_identified": len(hits) > 0,
        "giveaway": (
            f"Silhouette matches {', '.join(h['id'] for h in hits)}."
            if hits
            else "Silhouette is not in the catalog."
        ),
    }


SHELLS: Final[dict[str, dict[str, Any]]] = {
    "B": {
        "inside": {
            "what": "stacked Track B pieces: torus, energy tank, Bernstein, strain, Hardy wall, angular 1/r²",
            "kind": "interior",
            "source": "overlay stacked layers",
        },
        "identity_shell": {
            "id": "T3-DOMAIN",
            "what": "the actual outer shape: periodic box T^3 / R^3",
            "status": "identity",
            "clip_id": "—",
            "shape": "classical NS role skeleton on T^3 / R^3",
        },
        "play_shell": {
            "id": "EVEN-REFLECT",
            "what": "manufactured outside across r=δ so h(R)=0",
            "status": "play",
            "clip_id": "CLIP-T3-OUTER",
            "shape": "cylinder with manufactured outer vanishing",
        },
    },
    "Q": {
        "inside": {
            "what": "inverse-GCD operator pieces",
            "kind": "interior",
            "source": "Track Q catalog",
        },
        "identity_shell": {
            "id": "ARITHMETIC-FORM",
            "what": "the actual outer shape: inverse-GCD arithmetic operator",
            "status": "identity",
            "clip_id": "—",
            "shape": "inverse-GCD arithmetic operator",
        },
        "play_shell": {
            "id": "COSMO-MANIFOLD",
            "what": "a fly-through wrapped around the arithmetic",
            "status": "play",
            "clip_id": "VIZ→Q",
            "shape": "display / proposed-model animation",
        },
    },
}


def _inside_layers(book: str) -> list[dict[str, str]]:
    if book != "B":
        return []
    overlay = overlay_report()
    return [
        {"id": layer["id"], "glyph": layer["glyph"], "what": layer["what"]}
        for layer in overlay["stacked"]
    ]


def shell_report(target: str = "B") -> dict[str, Any]:
    key = target.strip().upper()
    aliases = {
        "NS": "B",
        "TRACKB": "B",
        "NAVIERSTOKES": "B",
        "NAVIER-STOKES": "B",
        "TRACKQ": "Q",
        "SHELL": "B",
        "OUTSIDE": "B",
        "SILHOUETTE": "B",
    }
    book = aliases.get(key, key)
    spec = SHELLS.get(book)
    if spec is None:
        return {
            "error": (
                "Shell is wired for B (worked example) and Q. "
                "Same method: inside, then outer shape, then catalog match."
            )
        }

    ident = dict(spec["identity_shell"])
    play = dict(spec["play_shell"])
    ident_match = match_silhouette(ident["shape"])
    play_match = match_silhouette(play["shape"])
    # Play shell matching VIZ is a trap, not a giveaway of the interior object.
    play_is_trap = play_match["already_identified"] and any(
        h["book"] != book for h in play_match["hits"]
    )
    ident["match"] = ident_match
    play["match"] = play_match
    play["trap"] = play_is_trap

    wrong = []
    if book == "B":
        compared = compare_shape("NS-B", "Q6")
        wrong.append(
            {
                "left": "NS-B",
                "right": "Q6",
                "verdict": compared.verdict,
                "why": "A Q silhouette is not this interior. Letters can rhyme.",
            }
        )

    return {
        "title": "Shell — inside, then outer shape, then the giveaway",
        "not_a_proof": True,
        "book": book,
        "worked_example": book == "B",
        "inside": {
            **spec["inside"],
            "layers": _inside_layers(book),
        },
        "identity_shell": ident,
        "play_shell": play,
        "giveaway": {
            "dead_giveaway": ident_match["already_identified"],
            "object": ident["shape"],
            "catalog": [h["id"] for h in ident_match["hits"]],
            "smooth": False,
            "why": (
                "The outer identity-shape matches objects already in the catalog. "
                "That names the object. It does not fill leftover holes and it "
                "does not weld books."
            ),
        },
        "wrong_silhouettes": wrong,
        "rule": (
            "Look at the inside. Put the real shell on. If the silhouette is "
            "already in the catalog, that is a dead giveaway. An invented "
            "shell is play (extra E). Play is not identification."
        ),
        "think_tank": consult("shell"),
        "next": (
            "Keep the identity shell. Do not promote even-reflect to the "
            "object. Identification is not smoothness."
        ),
    }


def format_shell(report: dict[str, Any] | None = None) -> str:
    data = report or shell_report("B")
    if data.get("error"):
        return data["error"]
    ident = data["identity_shell"]
    play = data["play_shell"]
    give = data["giveaway"]
    lines = [
        data["title"],
        data["rule"],
        "",
        "Inside",
        f"  {data['inside']['what']}",
    ]
    for layer in data["inside"]["layers"][:8]:
        lines.append(f"      {layer['glyph']}  {layer['id']}")
    if len(data["inside"]["layers"]) > 8:
        lines.append(f"      … {len(data['inside']['layers'])} stacked pieces")
    lines.append("")
    lines.append("Identity shell (the real outside)")
    lines.append(f"  {ident['id']}  [{ident['status']}]  {ident['what']}")
    lines.append(f"  silhouette: {ident['shape']}")
    lines.append(f"  giveaway: {ident['match']['giveaway']}")
    lines.append("")
    lines.append("Play shell (invented outside — extra E)")
    lines.append(
        f"  {play['id']}  [{play['status']}]  clip {play['clip_id']}  {play['what']}"
    )
    lines.append(f"  silhouette: {play['shape']}")
    lines.append(f"  giveaway: {play['match']['giveaway']}")
    if play.get("trap"):
        lines.append("  trap: this silhouette is a different book. Not the interior.")
    lines.append("")
    lines.append(
        f"Dead giveaway: {str(give['dead_giveaway']).lower()}  "
        f"catalog={', '.join(give['catalog']) or 'none'}  "
        f"smooth={str(give['smooth']).lower()}"
    )
    lines.append("  " + give["why"])
    for row in data.get("wrong_silhouettes") or []:
        lines.append(f"  not {row['right']}: {row['verdict']} — {row['why']}")
    tank = data.get("think_tank") or {}
    if tank.get("notes"):
        lines.append("")
        lines.append("Think tank")
        for note in tank["notes"][:6]:
            lines.append(f"  {note['name']}: {note['says']}")
    lines.append("Next: " + data["next"])
    return "\n".join(lines)
