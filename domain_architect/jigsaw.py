"""Jigsaw: break into pieces, assemble, classify holes as damage vs identity.

A shelled building is still a building. Order-2 and order-3 holes do not
change the object. Order-1 holes stay in the walls (Parthenon) and still
do not turn it into a hill. Finest detail is not required: the general
shape plus how energy moves through the snapped pieces is enough to name
it. The assembler is a constraint matcher (same book, matching chart
tabs, transposable). It is not a neural net that silent-merges another
book into the picture.

Track B is the worked example. CosmoEvolution is not a piece.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Final

from .overlay import LAYERS, overlay_report
from .scan import leftover_holes
from .shell import shell_report
from .think_tank import consult


# Tabs: pieces snap only to the same chart, same book, and only if transposable.
ORDER_LABEL: Final[dict[int, str]] = {
    1: "in the walls — Parthenon damage; still a building; blocks the walk",
    2: "shell damage — not identity; park it",
    3: "rubble — refused; do not put back",
}

# Known rules among snapped Track B pieces. Reconstruction from the
# interior, not from a manufactured outside or a missing floor.
ENERGY_PATH_B: Final[tuple[str, ...]] = (
    "L12-ENERGY",
    "L3-BERNSTEIN",
    "L5-RING",
    "L6-STRAIN",
    "L7-HARDY",
    "L8-ANGULAR",
)

RELATIONS_B: Final[tuple[dict[str, str], ...]] = (
    {
        "from": "L12-ENERGY",
        "to": "L3-BERNSTEIN",
        "rule": "kinetic pile E fills shell enstrophy X_j = 2^{2j} E_j",
        "kind": "energy",
    },
    {
        "from": "L3-BERNSTEIN",
        "to": "L5-RING",
        "rule": "3-shell Bernstein lives on the concentrated ring E_c",
        "kind": "energy",
    },
    {
        "from": "L5-RING",
        "to": "L6-STRAIN",
        "rule": "traceless strain: two eigenvalues fill the third",
        "kind": "geometry",
    },
    {
        "from": "L7-HARDY",
        "to": "L8-ANGULAR",
        "rule": "inside the same tube, (Δu)_θ = Δu_θ − u_θ/r² is extra damping",
        "kind": "viscosity",
    },
    {
        "from": "L1-TORUS",
        "to": "L12-ENERGY",
        "rule": "the room everything sits in: T^3, div-free, Leray projector",
        "kind": "domain",
    },
    {
        "from": "L2-FLUX",
        "to": "L12-ENERGY",
        "rule": "low self-flux into one dyadic block vanishes",
        "kind": "energy",
    },
)


def _piece(layer: Any, book: str = "B") -> dict[str, Any]:
    snaps = bool(layer.done_in_piece and layer.transposable)
    return {
        "id": layer.id,
        "book": book,
        "glyph": layer.glyph,
        "chart": layer.chart,
        "tab": layer.chart,
        "what": layer.what,
        "status": layer.status,
        "clip_id": layer.clip_id,
        "snaps": snaps,
        "loose": layer.status == "play",
        "refused": layer.status == "refuse",
        "waiting": (not layer.done_in_piece) and layer.status != "refuse",
    }


def assemble_pieces(pieces: list[dict[str, Any]]) -> dict[str, Any]:
    """Constraint assembler. Tabs are charts. No cross-book snap."""
    by_tab: dict[tuple[str, str], list[str]] = defaultdict(list)
    snapped = []
    loose = []
    waiting = []
    refused = []
    for piece in pieces:
        if piece["snaps"]:
            snapped.append(piece["id"])
            by_tab[(piece.get("book", "?"), piece["tab"])].append(piece["id"])
        elif piece["loose"]:
            loose.append(piece["id"])
        elif piece["refused"]:
            refused.append(piece["id"])
        else:
            waiting.append(piece["id"])
    fits = [
        {
            "book": book,
            "tab": tab,
            "pieces": ids,
            "fit": "same chart, same book, transposable",
        }
        for (book, tab), ids in sorted(by_tab.items())
        if ids
    ]
    return {
        "kind": "constraint",
        "not": "a neural net that welds across books",
        "rule": "snap only same book + matching chart tab + transposable",
        "why_not_ml": (
            "A statistical joiner would silent-merge Q or Cosmo onto the "
            "building because the letters rhyme. Dijkstra / Parnas: no."
        ),
        "snapped": snapped,
        "loose": loose,
        "waiting": waiting,
        "refused": refused,
        "fits": fits,
        "cross_book_snap": False,
    }


def classify_holes(book: str = "B") -> list[dict[str, Any]]:
    rows = []
    for hole in leftover_holes(book=book):
        order = int(hole.get("order") or 2)
        if order == 1:
            role = "parthenon"
        elif order >= 3:
            role = "rubble"
        else:
            role = "damage"
        rows.append(
            {
                **hole,
                "order_label": ORDER_LABEL.get(order, ORDER_LABEL[2]),
                "identity_relevant": False,
                "walk_relevant": order == 1,
                "role": role,
            }
        )
    return rows


def _q_pieces() -> list[dict[str, Any]]:
    return [
        {
            "id": "Q6",
            "book": "Q",
            "glyph": "λmin",
            "chart": "arithmetic",
            "tab": "arithmetic",
            "what": "inverse-GCD operator",
            "status": "ready",
            "clip_id": "CLIP-Q-ZETA",
            "snaps": True,
            "loose": False,
            "refused": False,
            "waiting": False,
        },
        {
            "id": "LAMBDA-MIN",
            "book": "Q",
            "glyph": "λmax",
            "chart": "arithmetic",
            "tab": "arithmetic",
            "what": "matrix chart of the same object",
            "status": "ready",
            "clip_id": "CLIP-Q-FLOOR",
            "snaps": True,
            "loose": False,
            "refused": False,
            "waiting": False,
        },
    ]


def jigsaw_report(target: str = "B") -> dict[str, Any]:
    key = target.strip().upper()
    book = {
        "NS": "B",
        "TRACKB": "B",
        "JIGSAW": "B",
        "ASSEMBLE": "B",
        "PUZZLE": "B",
        "BUILDING": "B",
        "TRACKQ": "Q",
    }.get(key, key)
    if book not in {"B", "Q"}:
        return {
            "error": (
                "Jigsaw is wired for B (worked example) and Q. "
                "Same method: pieces, assemble, classify holes as damage."
            )
        }

    pieces = [_piece(layer) for layer in LAYERS] if book == "B" else _q_pieces()
    assembly = assemble_pieces(pieces)
    holes = classify_holes(book)
    shell = shell_report(book)
    catalog = list(shell.get("giveaway", {}).get("catalog") or [])
    other = "Q" if book == "B" else "B"
    building = {
        "verdict": "BUILDING",
        "not": "HILL",
        "object": shell.get("giveaway", {}).get("object") or book,
        "catalog": catalog,
        "certain": bool(shell.get("giveaway", {}).get("dead_giveaway")),
        "finest_detail": False,
        "floor_required": False,
        "outside_required": False,
        "why": (
            "Enough pieces snapped, and the identity shell is already in the "
            "catalog. Holes (even order-1) are damage. A hill would be a "
            "different silhouette (Q vs B, Cosmo vs either). Finest detail "
            "is not required. The general shape plus how energy moves "
            "through the snapped pieces is enough to name it."
        ),
    }
    if book == "B":
        relations = [dict(row) for row in RELATIONS_B]
        energy_path = list(ENERGY_PATH_B)
    else:
        relations = [
            {
                "from": "Q6",
                "to": "LAMBDA-MIN",
                "rule": "same inverse-GCD object, matrix chart",
                "kind": "arithmetic",
            }
        ]
        energy_path = []
    overlay = overlay_report() if book == "B" else {"composite": {"is_complete": False}}
    mixed = assemble_pieces(pieces + (_q_pieces() if book == "B" else [_piece(layer) for layer in LAYERS]))
    return {
        "title": "Jigsaw — pieces, assembly, damage that does not unmake the building",
        "not_a_proof": True,
        "book": book,
        "worked_example": book == "B",
        "pieces": pieces,
        "assembly": assembly,
        "holes": holes,
        "relations": relations,
        "energy_path": energy_path,
        "building": building,
        "smooth": False,
        "complete": bool(overlay.get("composite", {}).get("is_complete")),
        "foreign": {
            "other_book": other,
            "snap": "WRONG_OBJECT",
            "cosmo": "WRONG_OBJECT",
            "mixed_fits_share_a_tab": False,
            "why": (
                f"{other} and Cosmo are a different silhouette. "
                "They do not snap onto this building. A hill is not this building."
            ),
        },
        "probe_mixed_books": {
            "cross_book_snap": mixed["cross_book_snap"],
            "fit_books": sorted({row["book"] for row in mixed["fits"]}),
            "any_fit_has_two_books": False,
        },
        "rule": (
            "Break into literal pieces. Snap only matching tabs. "
            "Order-2/3 holes are not identity. Order-1 holes stay in the "
            "walls. Still a building, not a hill. Assembler is constraints, "
            "not a neural net. Finest detail is not required."
        ),
        "think_tank": consult("jigsaw"),
        "next": (
            "Keep the building. Park order-2/3. Reconstruct from known "
            "relations (energy path, viscosity). Do not fill order-1 with Q "
            "or Cosmo. Identification is not smoothness."
        ),
    }


def format_jigsaw(report: dict[str, Any] | None = None) -> str:
    data = report or jigsaw_report("B")
    if data.get("error"):
        return data["error"]
    bld = data["building"]
    asm = data["assembly"]
    lines = [
        data["title"],
        data["rule"],
        "",
        "Pieces",
    ]
    for piece in data["pieces"]:
        flag = (
            "SNAP"
            if piece["snaps"]
            else ("LOOSE" if piece["loose"] else ("REFUSE" if piece["refused"] else "WAIT"))
        )
        lines.append(
            f"  {piece['id']:14} [{flag:6}] tab={piece['tab']:12}  {piece['glyph']}"
        )
    lines.append("")
    lines.append(
        f"Assembler: {asm['kind']}  snapped={len(asm['snapped'])}  "
        f"loose={len(asm['loose'])}  waiting={len(asm['waiting'])}"
    )
    lines.append(f"  not: {asm['not']}")
    lines.append(f"  {asm['why_not_ml']}")
    if data.get("energy_path"):
        lines.append("")
        lines.append("Energy path (how it works, not finest detail)")
        lines.append("  " + " → ".join(data["energy_path"]))
    if data.get("relations"):
        lines.append("")
        lines.append("Known relations among snapped pieces")
        for rel in data["relations"]:
            lines.append(
                f"  {rel['from']:14} → {rel['to']:14}  [{rel['kind']}]  {rel['rule']}"
            )
    lines.append("")
    lines.append("Holes (damage, not a different object)")
    for hole in data["holes"]:
        lines.append(
            f"  order {hole['order']}  {hole['clip_id']:18}  "
            f"{hole['role']:10}  walk={str(hole['walk_relevant']).lower()}"
        )
        lines.append(f"      {hole['order_label']}")
    lines.append("")
    lines.append(
        f"Verdict: {bld['verdict']}  not {bld['not']}  "
        f"certain={str(bld['certain']).lower()}  smooth={str(data['smooth']).lower()}"
    )
    lines.append(f"  object: {bld['object']}")
    lines.append(f"  catalog: {', '.join(bld['catalog']) or 'none'}")
    lines.append("  " + bld["why"])
    foreign = data.get("foreign") or {}
    if foreign:
        lines.append(
            f"  {foreign.get('other_book', '?')} onto this book: {foreign.get('snap')}  "
            f"Cosmo: {foreign.get('cosmo')}"
        )
    tank = data.get("think_tank") or {}
    if tank.get("notes"):
        lines.append("")
        lines.append("Think tank")
        for note in tank["notes"][:6]:
            lines.append(f"  {note['name']}: {note['says']}")
    lines.append("Next: " + data["next"])
    return "\n".join(lines)
