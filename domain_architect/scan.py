"""Scan leftover holes against every rudimentary piece Domain Architect knows.

The method is general. Track B is a worked example, not the product.
If an object is unknown, or one slot is empty: break the catalog into
pieces, group the views of the same object, and computer-match each hole
to an equation that might fit. A match is a candidate. It does not weld.

Endpoint: name the object from its views and stacked anatomy, then see
whether any piece actually smooths an order-1 hole. Smooth is not the
same as identified.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Final

from .desk import LIBRARY_OBJECTS, SHAPE_ROLES
from .overlay import LAYERS, overlay_report
from .registry import EquationRegistry
from .think_tank import consult


FAMILY_BOOK: Final[dict[str, str]] = {
    "FRA": "DA",
    "UHF": "DA",
    "SFE": "SFE",
    "DHFA": "DA",
    "GRV": "U",
    "EXP01": "EXP01",
    "VIZ": "VIZ",
    "SYS": "SEARCH",
}

# Order-1 holes change the walk. Order-2 is extra texture. Order-3 is refused.
HOLE_SPEC: Final[dict[str, dict[str, Any]]] = {
    "CLIP-T3-WELD": {
        "order": 1,
        "gap_id": "GAP-T3",
        "wants": "an identity that maps Hardy/Young wall traces onto I_off",
        "fields": ("Gamma", "omega^r", "I_off"),
        "book": "B",
        "chart": "swirl",
    },
    "CLIP-T3-OUTER": {
        "order": 1,
        "gap_id": "GAP-T3",
        "wants": "swirl vanishing at an outer radius on the actual domain",
        "fields": ("Gamma(R)=0",),
        "book": "B",
        "chart": "cylinder",
    },
    "CLIP-B4b-ITUBE": {
        "order": 1,
        "gap_id": "GAP-ITUBE",
        "wants": "I_tube versus viscosity at the wall scale",
        "fields": ("I_tube", "nu"),
        "book": "B",
        "chart": "swirl",
    },
    "CLIP-B3b-ALIGN": {
        "order": 2,
        "gap_id": "GAP-ALIGN",
        "wants": "strain–vorticity alignment / depletion",
        "fields": ("cos alpha",),
        "book": "B",
        "chart": "vorticity",
    },
    "CLIP-B2-OCCUPATION": {
        "order": 2,
        "gap_id": "GAP-OCCUPATION",
        "wants": "how long CONC versus SPREAD occupies (0,1]",
        "fields": ("sigma",),
        "book": "B",
        "chart": "frequency",
    },
    "CLIP-B5b-VS-VISC": {
        "order": 2,
        "gap_id": "GAP-VISC",
        "wants": "angular 1/r^2 damping dominating I_tube",
        "fields": ("u_theta/r^2",),
        "book": "B",
        "chart": "swirl",
    },
    "CLIP-B6-SPIKE": {
        "order": 2,
        "gap_id": "GAP-SPIKE",
        "wants": "energy bounding X; seeing E does not",
        "fields": ("E", "X"),
        "book": "B",
        "chart": "energy",
    },
    "CLIP-B4-WALL": {
        "order": 2,
        "gap_id": "GAP-WALL",
        "wants": "absorb the wall term 2h(δ)^2",
        "fields": ("h(δ)",),
        "book": "B",
        "chart": "swirl",
    },
    "CLIP-PHI-LINFTY": {
        "order": 3,
        "gap_id": "GAP-PHI",
        "wants": "nothing — Φ_θ as unknown is refused",
        "fields": ("Phi_theta",),
        "book": "B",
        "chart": "swirl",
    },
    "CLIP-Q-ZETA": {
        "order": 1,
        "gap_id": "GAP-Q-ZETA",
        "wants": "an operator→ζ lemma, stated and checked",
        "fields": ("Q_N", "zeta"),
        "book": "Q",
        "chart": "arithmetic",
    },
    "CLIP-Q-FLOOR": {
        "order": 2,
        "gap_id": "GAP-Q-FLOOR",
        "wants": "λ_min(H_N) ≥ -1/4 proved, not only numeric",
        "fields": ("lambda_min",),
        "book": "Q",
        "chart": "arithmetic",
    },
    "CLIP-A-EPS": {
        "order": 2,
        "gap_id": "GAP-A-EPS",
        "wants": "energy law on the augmented PDE while ε>0 stays",
        "fields": ("epsilon",),
        "book": "A",
        "chart": "augmented",
    },
    "CLIP-U-PDG": {
        "order": 2,
        "gap_id": "GAP-U-PDG",
        "wants": "PDG numbers as inputs; Cosmo 16/16 stays out",
        "fields": ("PDG",),
        "book": "U",
        "chart": "bookkeeping",
    },
    "CLIP-SFE-CANON": {
        "order": 1,
        "gap_id": "GAP-SFE",
        "wants": "a canonical SFE — currently unresolved",
        "fields": ("SFE",),
        "book": "SFE",
        "chart": "grammar",
    },
}

# Honest pre-scored fits for the live order-1 hole. Nothing here welds.
WELD_SCAN: Final[tuple[dict[str, str], ...]] = (
    {
        "piece": "L9-YOUNG",
        "equation": "Young from outside when h(R)=0",
        "verdict": "LOOKS_LIKE_FIT",
        "why": "Same 1/r^3 weight as Hardy. Different fields, extra E, cylinder chart.",
        "fills": "no",
    },
    {
        "piece": "L11-ITUBE",
        "equation": "T5 |I_tube| vs viscosity",
        "verdict": "AFTER_NOT_FILL",
        "why": "Sits after the hole. Needs the weld first.",
        "fills": "no",
    },
    {
        "piece": "L6-STRAIN",
        "equation": "λ1+λ2+λ3=0",
        "verdict": "ALREADY_IN",
        "why": "Traceless strain is stacked. It does not map traces onto I_off.",
        "fills": "no",
    },
    {
        "piece": "L3-BERNSTEIN",
        "equation": "X_j = 2^{2j} E_j",
        "verdict": "ALREADY_IN",
        "why": "Fills enstrophy from shell energy. Not I_off.",
        "fills": "no",
    },
    {
        "piece": "L8-ANGULAR",
        "equation": "(Δu)_θ = Δu_θ − u_θ/r²",
        "verdict": "WRONG_SLOT",
        "why": "Same tube, different identity. Contests I_tube later, does not weld traces.",
        "fills": "no",
    },
    {
        "piece": "Q6",
        "equation": "λ_min of inverse-GCD",
        "verdict": "WRONG_OBJECT",
        "why": "Arithmetic operator. Symbols can rhyme with λ and still be another book.",
        "fills": "no",
    },
    {
        "piece": "VIZ",
        "equation": "CosmoEvolution display",
        "verdict": "WRONG_OBJECT",
        "why": "A picture is not an identity.",
        "fills": "no",
    },
    {
        "piece": "GRV-H001",
        "equation": "Poisson / Newtonian gravity",
        "verdict": "WRONG_OBJECT",
        "why": "Gravity bookkeeping is Track U. Not swirl.",
        "fills": "no",
    },
    {
        "piece": "SFE-H001",
        "equation": "historical SFE candidate",
        "verdict": "WRONG_OBJECT",
        "why": "Unresolved / retired grammar. Do not drop it into the hole.",
        "fills": "no",
    },
)

Q_SCAN: Final[tuple[dict[str, str], ...]] = (
    {
        "piece": "Q6",
        "equation": "λ_min of inverse-GCD",
        "verdict": "SAME_OBJECT_VIEW",
        "why": "Another chart of Track Q. Not the operator→ζ lemma.",
        "fills": "no",
    },
    {
        "piece": "LAMBDA-MIN",
        "equation": "λ_min / λ_max matrix chart",
        "verdict": "SAME_OBJECT_VIEW",
        "why": "Same object, different texture.",
        "fills": "no",
    },
    {
        "piece": "NS-B",
        "equation": "classical NS role skeleton",
        "verdict": "WRONG_OBJECT",
        "why": "Fluids anatomy was the worked example. It is not Track Q.",
        "fills": "no",
    },
    {
        "piece": "VIZ",
        "equation": "CosmoEvolution display",
        "verdict": "WRONG_OBJECT",
        "why": "A picture is not zeros of ζ.",
        "fills": "no",
    },
    {
        "piece": "SFE-H001",
        "equation": "historical SFE candidate",
        "verdict": "WRONG_OBJECT",
        "why": "Unresolved grammar. Do not drop it into Q.",
        "fills": "no",
    },
)

NAMED_BY_HOLE: Final[dict[str, tuple[dict[str, str], ...]]] = {
    "CLIP-T3-WELD": WELD_SCAN,
    "CLIP-Q-ZETA": Q_SCAN,
}

METHOD_STEPS: Final[tuple[str, ...]] = (
    "Name the views of one object (many charts, still one shape).",
    "Break DA into rudimentary pieces (roles, layers, inventory).",
    "List leftover holes. Order-1 changes the walk. Order-2 is extra texture.",
    "Computer-match each hole. LOOKS_LIKE_FIT is not a weld. WRONG_OBJECT stays out.",
    "Endpoint: identified from anatomy, or smooth if an order-1 hole actually fills.",
)

BOOK_FOCUS: Final[dict[str, str]] = {
    "B": "CLIP-T3-WELD",
    "Q": "CLIP-Q-ZETA",
    "A": "CLIP-A-EPS",
    "U": "CLIP-U-PDG",
    "SFE": "CLIP-SFE-CANON",
    "DA": "CLIP-SFE-CANON",
}


def views_of_same_object() -> list[dict[str, Any]]:
    """Many textures, one shape — the 3-into-1 (or N-into-1) anatomy."""
    groups: dict[tuple[str, str], list[str]] = defaultdict(list)
    for name, meta in LIBRARY_OBJECTS.items():
        groups[(meta["book"], meta["shape"])].append(name)
    out = []
    for (book, shape), names in groups.items():
        out.append(
            {
                "book": book,
                "shape": shape,
                "views": names,
                "view_count": len(names),
                "same_object": len(names) > 1,
            }
        )
    out.sort(key=lambda g: (-g["view_count"], g["book"]))
    return out


def rudimentary_pieces(registry: EquationRegistry | None = None) -> list[dict[str, Any]]:
    """Break DA all the way down: FRA slots, overlay layers, inventory equations."""
    pieces: list[dict[str, Any]] = []
    for role in SHAPE_ROLES:
        pieces.append(
            {
                "id": f"ROLE-{role}",
                "kind": "role",
                "book": "DA",
                "what": f"FRA slot {role}",
                "chart": "grammar",
            }
        )
    for layer in LAYERS:
        pieces.append(
            {
                "id": layer.id,
                "kind": "layer",
                "book": "B",
                "what": layer.what,
                "chart": layer.chart,
                "glyph": layer.glyph,
                "done_in_piece": layer.done_in_piece,
                "transposable": layer.transposable,
                "status": layer.status,
                "clip_id": layer.clip_id,
                "hole": layer.hole,
            }
        )
    reg = registry or EquationRegistry.load_default()
    for rec in reg.equations.values():
        pieces.append(
            {
                "id": rec.equation_id,
                "kind": "inventory",
                "book": FAMILY_BOOK.get(rec.family, rec.family),
                "what": rec.original_expression,
                "chart": rec.family,
                "disposition": rec.audit_disposition,
            }
        )
    return pieces


def leftover_holes(
    overlay: dict[str, Any] | None = None, book: str | None = None
) -> list[dict[str, Any]]:
    want = (book or "").upper() or None
    holes: list[dict[str, Any]] = []
    if want in {None, "B"}:
        data = overlay or overlay_report()
        for hole in data["holes"]:
            cid = hole["clip_id"]
            spec = HOLE_SPEC.get(cid, {})
            holes.append(
                {
                    "clip_id": cid,
                    "from": hole["from"],
                    "what": hole["what"],
                    "order": spec.get("order", 2),
                    "gap_id": spec.get("gap_id", cid),
                    "wants": spec.get("wants", hole["what"]),
                    "book": spec.get("book", "B"),
                    "chart": spec.get("chart", ""),
                }
            )
    if want != "B":
        for cid, spec in HOLE_SPEC.items():
            if spec["book"] == "B":
                continue
            if want and spec["book"] != want:
                continue
            holes.append(
                {
                    "clip_id": cid,
                    "from": spec["book"],
                    "what": spec["wants"],
                    "order": spec["order"],
                    "gap_id": spec["gap_id"],
                    "wants": spec["wants"],
                    "book": spec["book"],
                    "chart": spec["chart"],
                }
            )
    holes.sort(key=lambda h: (h["book"], h["order"], h["clip_id"]))
    return holes


def _match_inventory_against_hole(
    piece: dict[str, Any], hole: dict[str, Any]
) -> dict[str, str]:
    if piece["book"] == hole["book"] and piece["kind"] == "layer":
        if piece.get("clip_id") == hole["clip_id"]:
            return {
                "verdict": "THIS_IS_THE_HOLE",
                "why": "This layer is the empty slot, not a filler.",
                "fills": "no",
            }
        if piece.get("done_in_piece") and piece.get("transposable"):
            return {
                "verdict": "ALREADY_IN",
                "why": "Already stacked on the composite. Not the missing piece.",
                "fills": "no",
            }
        if piece.get("status") == "play":
            return {
                "verdict": "LOOKS_LIKE_FIT",
                "why": "Done on another chart. Looks like it could slot in. Extra E.",
                "fills": "no",
            }
        if piece.get("status") == "refuse":
            return {
                "verdict": "REFUSED",
                "why": "This piece is banned from the stack.",
                "fills": "no",
            }
        return {
            "verdict": "WAITING",
            "why": "Open in the same book. Not a fill until it is an identity.",
            "fills": "no",
        }
    if piece["book"] != hole["book"]:
        return {
            "verdict": "WRONG_OBJECT",
            "why": f"{piece['book']} is not {hole['book']}. Do not drop it in the hole.",
            "fills": "no",
        }
    return {
        "verdict": "NO_FIT",
        "why": "Same book label is not a shape match.",
        "fills": "no",
    }


def scan_hole(clip_id: str, pieces: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    spec = HOLE_SPEC.get(clip_id)
    if spec is None:
        return {"error": f"Unknown hole {clip_id}. No invented weld."}
    overlay = overlay_report() if spec["book"] == "B" else None
    hole = next(
        (h for h in leftover_holes(overlay, spec["book"]) if h["clip_id"] == clip_id),
        None,
    )
    if hole is None:
        hole = {
            "clip_id": clip_id,
            "from": "",
            "what": spec["wants"],
            "order": spec["order"],
            "gap_id": spec["gap_id"],
            "wants": spec["wants"],
            "book": spec["book"],
            "chart": spec["chart"],
        }
    catalog = pieces or rudimentary_pieces()
    scored = []
    for piece in catalog:
        hit = _match_inventory_against_hole(piece, hole)
        scored.append(
            {
                "piece": piece["id"],
                "kind": piece["kind"],
                "book": piece["book"],
                "what": piece["what"],
                **hit,
            }
        )
    named = [dict(row) for row in NAMED_BY_HOLE.get(clip_id, ())]
    fills = [row for row in named if row["fills"] == "yes"]
    return {
        "hole": hole,
        "named_matches": named,
        "inventory_matches": scored,
        "any_fill": bool(fills),
        "smooths": False,
        "rule": (
            "Computer match is a candidate. LOOKS_LIKE_FIT is not a weld. "
            "WRONG_OBJECT stays out. Empty after a full scan means the "
            "equation is not in this catalog."
        ),
    }


def _book_anatomy(book: str, pieces: list[dict[str, Any]], views: list[dict[str, Any]]) -> dict[str, Any]:
    object_views = next(
        (g for g in views if g["book"] == book),
        {"views": [], "view_count": 0, "shape": f"book {book}"},
    )
    holes = leftover_holes(book=book)
    order1 = [h for h in holes if h["order"] == 1]
    stacked = 0
    if book == "B":
        stacked = len(overlay_report()["stacked"])
    identified = bool(object_views.get("views")) or book in {"A", "U", "SFE", "DA"}
    return {
        "object": object_views.get("shape") or f"book {book}",
        "identified": identified,
        "why_identified": (
            "Views of one shape plus leftover holes. Holes do not make it a "
            "different object. Track B is the worked example of this method."
            if book == "B"
            else "Named from the catalog. Holes do not make it a different object."
        ),
        "views": object_views.get("views") or [],
        "view_count": object_views.get("view_count") or 0,
        "stacked_count": stacked,
        "piece_count": len(pieces),
        "smooth": False,
        "smooth_needs": [h["clip_id"] for h in order1],
        "example_of_method": book == "B",
    }


def method_report() -> dict[str, Any]:
    pieces = rudimentary_pieces()
    views = views_of_same_object()
    by_book = {
        book: {
            "anatomy": _book_anatomy(book, pieces, views),
            "leftover": leftover_holes(book=book),
            "focus_hole": BOOK_FOCUS[book],
        }
        for book in ("B", "Q", "A", "U", "SFE")
    }
    return {
        "title": "Scan — general anatomy. Track B is a worked example.",
        "mode": "method",
        "not_a_proof": True,
        "book": "DA",
        "worked_example": "B",
        "steps": list(METHOD_STEPS),
        "objects": views,
        "books": by_book,
        "pieces": pieces,
        "think_tank": consult("method"),
        "counts": {
            "pieces": len(pieces),
            "views": len(views),
            "books": len(by_book),
            "fills_found": 0,
        },
        "endpoint": (
            "The method is: views → pieces → leftover holes → match. "
            "B is one object you already started. Q, A, U, SFE use the same machine."
        ),
        "next": (
            "python -m domain_architect --scan B   # worked example\n"
            "  python -m domain_architect --scan Q   # same method, other book"
        ),
    }


def scan_report(target: str = "B") -> dict[str, Any]:
    key = target.strip().upper()
    if key in {"ANY", "METHOD", "GENERAL", "ALL", "SCAN", "ANATOMY", "EXAMPLE"}:
        return method_report()
    if key in {"GAP-T3", "T3", "WELD", "CLIP-T3-WELD"}:
        hole_id = "CLIP-T3-WELD"
        book = "B"
    elif key in HOLE_SPEC:
        hole_id = key
        book = str(HOLE_SPEC[key]["book"])
    elif key in {"B", "NS", "TRACKB", "NAVIERSTOKES", "NAVIER-STOKES"}:
        hole_id = "CLIP-T3-WELD"
        book = "B"
    elif key in BOOK_FOCUS:
        hole_id = BOOK_FOCUS[key]
        book = "SFE" if key == "DA" else key
    else:
        return {
            "error": (
                "Scan is the general anatomy machine. "
                "Try --scan, --scan B (worked example), --scan Q, --scan A, --scan U."
            )
        }

    pieces = rudimentary_pieces()
    views = views_of_same_object()
    holes = leftover_holes(book=book)
    first = scan_hole(hole_id, pieces)
    ana = _book_anatomy(book, pieces, views)
    tank_topic = "scan" if book == "B" else "method"
    example_line = (
        "Worked example of the general method. Not the only object."
        if book == "B"
        else "Same method as --scan. Track B was only the example."
    )
    return {
        "title": f"Scan — {book}  ({example_line})",
        "mode": "book",
        "not_a_proof": True,
        "book": book,
        "worked_example": book == "B",
        "anatomy": ana,
        "views_catalog": views,
        "pieces": pieces,
        "leftover": holes,
        "focus": first,
        "think_tank": consult(tank_topic),
        "counts": {
            "pieces": len(pieces),
            "views": len(views),
            "holes": len(holes),
            "order1": len(ana["smooth_needs"]),
            "fills_found": 0,
        },
        "endpoint": (
            "Identified from anatomy. Not smooth: no catalog equation fills "
            "the order-1 hole."
            + (" LOOKS_LIKE_FIT (T3a Young) is extra E." if book == "B" else "")
        ),
        "next": (
            "Keep the empty slot in view. Do not drop another book into it "
            "because the symbols rhyme. --scan with no book shows the method."
        ),
    }


def format_scan(report: dict[str, Any] | None = None) -> str:
    data = report or scan_report("B")
    if data.get("error"):
        return data["error"]
    if data.get("mode") == "method":
        lines = [
            data["title"],
            "Not a proof. Track B was the example used to show the method.",
            "",
            "Method",
        ]
        for i, step in enumerate(data["steps"], 1):
            lines.append(f"  {i}. {step}")
        lines.append("")
        lines.append("Objects in the catalog (views of each shape)")
        for group in data["objects"]:
            flag = "same object, many views" if group["same_object"] else "one view"
            lines.append(
                f"  [{group['book']}] {group['shape']}  "
                f"({group['view_count']} views, {flag})"
            )
            lines.append(f"      {', '.join(group['views'])}")
        lines.append("")
        lines.append("Leftover holes by book")
        for book, block in data["books"].items():
            needs = ", ".join(block["anatomy"]["smooth_needs"]) or "none"
            lines.append(f"  {book}: order-1 open: {needs}")
        tank = data.get("think_tank") or {}
        if tank.get("notes"):
            lines.append("")
            lines.append("Think tank on the method (insight is not a weld)")
            for note in tank["notes"]:
                lines.append(f"  {note['name']}: {note['says']}")
        lines.append("")
        lines.append("Endpoint: " + data["endpoint"])
        lines.append("Next: " + data["next"])
        return "\n".join(lines)
    ana = data["anatomy"]
    focus = data["focus"]
    hole = focus["hole"]
    lines = [
        data["title"],
        "Not a proof. A match is a candidate. Empty is an honest scan.",
        "",
        "Anatomy of the object",
        f"  object: {ana['object']}",
        f"  identified: {str(ana['identified']).lower()}  "
        f"views={ana['view_count']}  stacked={ana['stacked_count']}  "
        f"pieces={ana['piece_count']}",
        f"  views: {', '.join(ana['views'])}",
        f"  {ana['why_identified']}",
        f"  smooth: {str(ana['smooth']).lower()}  "
        f"order-1 still open: {', '.join(ana['smooth_needs'])}",
        "",
        "Leftover pieces (holes)",
    ]
    for hole_row in data["leftover"]:
        lines.append(
            f"  order {hole_row['order']}  {hole_row['clip_id']:18}  "
            f"{hole_row['wants']}"
        )
    lines.append("")
    lines.append(f"Scan focus: {hole['clip_id']}  wants: {hole['wants']}")
    lines.append("  " + focus["rule"])
    lines.append("")
    lines.append("Computer match (named)")
    for row in focus["named_matches"]:
        lines.append(
            f"  {row['verdict']:16}  {row['piece']:14}  fills={row['fills']}"
        )
        lines.append(f"      {row['equation']}")
        lines.append(f"      {row['why']}")
    wrong = [
        row
        for row in focus["inventory_matches"]
        if row["kind"] == "inventory" and row["verdict"] == "WRONG_OBJECT"
    ]
    lines.append("")
    lines.append(f"Inventory scan: {len(focus['inventory_matches'])} pieces")
    lines.append(
        f"  wrong-object (other books / retired grammar): {len(wrong)}  "
        "none of these fill the hole"
    )
    tank = data.get("think_tank") or {}
    if tank.get("notes"):
        lines.append("")
        lines.append("Think tank (insight is not a weld)")
        for note in tank["notes"]:
            lines.append(f"  {note['name']}: {note['says']}")
    lines.append("")
    lines.append("Endpoint: " + data["endpoint"])
    lines.append("Next: " + data["next"])
    return "\n".join(lines)
