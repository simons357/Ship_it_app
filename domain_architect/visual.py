"""Human see: pictures first, math under a fold.

Visual cognition is cheap. Inequalities are expensive. This module draws
the cylinder, energy, overlay, and gap as SVG from the same objects the
CLI already knows. The picture is a package appendage: it follows the
math you just ran. It is not CosmoEvolution and not a proof.
"""

from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any, Final
import json

from .energy_play import energy_play
from .gap import gap_report
from .overlay import overlay_report
from .scan import scan_report
from .shell import shell_report
from .jigsaw import jigsaw_report
from .shape_play import play_cylinder


DEFAULT_HTML: Final[str] = "docs/domain-architect/see.html"
DEFAULT_STATE: Final[str] = "docs/domain-architect/see-state.json"
READY = "#1b7f6e"
PLAY = "#c9a227"
OPEN = "#c44536"
HOLE = "#c44536"
REFUSE = "#6b6570"
INK = "#1c1917"
PAPER = "#f6f1e7"
FOCUS_LINE: Final[dict[str, str]] = {
    "tube": "Live math: tube estimate — Hardy, wall, I_tube",
    "gap": "Live math: stop at the wall — missing piece in view",
    "overlay": "Live math: overlay of done pieces",
    "energy": "Live math: energy as a pile you can see",
    "energy-play": "Live math: energy as a pile you can see",
    "shape": "Live math: fill the other side of a shape",
    "shape-play": "Live math: fill the other side of a shape",
    "chain": "Live math: lemma chain as shapes",
    "geometry": "Live math: four charts on one object",
    "clip": "Live math: clip the excess, keep the remainder",
    "compare": "Live math: shape first, then texture",
    "shape-compare": "Live math: shape first, then texture",
    "audit": "Live math: role audit of an expression",
    "scan": "Live math: scan leftover holes against every rudimentary piece",
    "shell": "Live math: inside plus outer shell — silhouette may already be known",
    "jigsaw": "Live math: over the goal — name it, show how energy goes through it",
    "see": "Visual appendage — slave of the math, not Cosmo",
}
TITLES: Final[dict[str, str]] = {
    "tube": "Tube estimate — Hardy, wall, I_tube",
    "gap": "Stop at the wall — missing piece in view",
    "overlay": "Overlay of done pieces, holes through the stack",
    "energy": "Energy as a pile you can see",
    "energy-play": "Energy as a pile you can see",
    "shape": "Cylinder fill + even-reflect play",
    "shape-play": "Cylinder fill + even-reflect play",
    "chain": "Track B chain as shapes",
    "geometry": "Geometric analysis of Track B",
    "clip": "Clip the excess, keep the remainder",
    "compare": "Shape first, then texture",
    "shape-compare": "Shape first, then texture",
    "audit": "Role audit of an expression",
    "scan": "Scan — match the hole, do not weld",
    "shell": "Shell — inside, outer shape, dead giveaway",
    "jigsaw": "Jigsaw — over the goal: this is the object, how energy goes through it",
    "see": "See desk — pictures first, math under the fold",
}


def _default_focus() -> dict[str, Any]:
    return {
        "appendage": "SEE",
        "slave_of": "math",
        "action": "see",
        "book": "B",
        "title": TITLES["see"],
        "live": FOCUS_LINE["see"],
        "not_a_proof": True,
        "not_cosmo": True,
    }


def load_focus() -> dict[str, Any]:
    path = Path(DEFAULT_STATE)
    if not path.exists():
        return _default_focus()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _default_focus()
    if not isinstance(data, dict):
        return _default_focus()
    merged = _default_focus()
    merged.update(data)
    return merged


def write_state(action: str, book: str = "B") -> dict[str, Any]:
    """Persist what the math just did so the picture can follow."""
    key = action.strip().lower()
    state = {
        "appendage": "SEE",
        "slave_of": "math",
        "action": key,
        "book": book,
        "title": TITLES.get(key, key),
        "live": FOCUS_LINE.get(key, FOCUS_LINE["see"]),
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "not_a_proof": True,
        "not_cosmo": True,
    }
    path = Path(DEFAULT_STATE)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return state


def follow(action: str, book: str = "B") -> dict[str, Any]:
    """Always adjust the visual to the math that just ran."""
    state = write_state(action, book)
    path = write_see()
    state["picture"] = str(path)
    return state


def format_follow(state: dict[str, Any] | None = None) -> str:
    data = state or load_focus()
    picture = data.get("picture") or DEFAULT_HTML
    return (
        "Visual appendage followed the math.\n"
        f"  now looking at: {data.get('title')}\n"
        f"  {data.get('live')}\n"
        f"  picture: {picture}\n"
        "  CosmoEvolution 3D is not this appendage.\n"
    )


def _bar_row(values: list[float], x: float, y: float, w: float, h: float, fill: str) -> str:
    if not values:
        return ""
    peak = max(values) or 1.0
    n = len(values)
    bw = w / n
    parts: list[str] = []
    for i, v in enumerate(values):
        bh = h * (v / peak)
        parts.append(
            f'<rect x="{x + i * bw + 1:.1f}" y="{y + h - bh:.1f}" '
            f'width="{bw - 2:.1f}" height="{bh:.1f}" fill="{fill}" rx="2"/>'
        )
    return "\n".join(parts)


def svg_cylinder() -> str:
    """Inside disk, gold wall, dashed outside — the cut you can see."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 220" role="img" aria-label="Cylinder wall as a cut">
  <rect width="460" height="220" fill="{PAPER}"/>
  <text x="16" y="28" font-family="Georgia, serif" font-size="16" fill="{INK}">Cylinder — you see the cut</text>
  <circle cx="150" cy="125" r="78" fill="none" stroke="{PLAY}" stroke-width="2" stroke-dasharray="7 6"/>
  <circle cx="150" cy="125" r="40" fill="#d7efe9" stroke="{READY}" stroke-width="3"/>
  <circle cx="150" cy="125" r="42" fill="none" stroke="{PLAY}" stroke-width="6"/>
  <text x="150" y="120" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="{INK}">tube</text>
  <text x="150" y="138" text-anchor="middle" font-family="Georgia, serif" font-size="11" fill="{READY}">Hardy done</text>
  <text x="252" y="80" font-family="Georgia, serif" font-size="12" fill="{PLAY}">wall r=δ</text>
  <text x="248" y="168" font-family="Georgia, serif" font-size="12" fill="{OPEN}">outside unknown</text>
  <text x="300" y="70" font-family="Georgia, serif" font-size="14" fill="{INK}">Even reflect = play</text>
  <text x="300" y="92" font-family="Georgia, serif" font-size="12" fill="{INK}">fills a fake outside</text>
  <text x="300" y="114" font-family="Georgia, serif" font-size="12" fill="{OPEN}">does not fill I_off</text>
  <text x="16" y="208" font-family="Georgia, serif" font-size="11" fill="{INK}">Math stays under the picture. CLIP-T3-OUTER / CLIP-T3-WELD.</text>
</svg>'''


def svg_energy() -> str:
    """Energy pile you can see; enstrophy pile warped; tube guess fails."""
    e = [0.18, 0.22, 0.16, 0.10, 0.06, 0.04, 0.03]
    x = [v * (4**i) for i, v in enumerate(e)]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 250" role="img" aria-label="Energy versus enstrophy piles">
  <rect width="500" height="250" fill="{PAPER}"/>
  <text x="16" y="28" font-family="Georgia, serif" font-size="16" fill="{INK}">Energy — the pile you can see</text>
  <text x="16" y="52" font-family="Georgia, serif" font-size="12" fill="{READY}">E_j kinetic (seen)</text>
  {_bar_row(e, 16, 60, 220, 70, READY)}
  <text x="260" y="52" font-family="Georgia, serif" font-size="12" fill="{INK}">X_j = 2^{{2j}} E_j (filled, warped)</text>
  {_bar_row(x, 260, 60, 220, 70, INK)}
  <text x="16" y="160" font-family="Georgia, serif" font-size="13" fill="{INK}">Guess the tube from the outside?</text>
  <rect x="16" y="172" width="200" height="48" rx="8" fill="#d7efe9" stroke="{READY}"/>
  <text x="116" y="201" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="{READY}">even blob — yes, play</text>
  <rect x="236" y="172" width="248" height="48" rx="8" fill="#f8d7d3" stroke="{OPEN}"/>
  <text x="360" y="201" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="{OPEN}">energy in the tube — no</text>
  <text x="16" y="240" font-family="Georgia, serif" font-size="11" fill="{INK}">Bernstein is the honest fill. Seeing E does not bound X. CLIP-B6-SPIKE.</text>
</svg>'''


def svg_overlay(report: dict[str, Any] | None = None) -> str:
    """Stack of transparencies; holes punched; unfinished layers off to the side."""
    data = report or overlay_report()
    stacked = data["stacked"]
    cards: list[str] = []
    n = len(stacked)
    for i, layer in enumerate(stacked):
        y = 48 + i * 28
        cards.append(
            f'<rect x="24" y="{y}" width="280" height="34" rx="6" '
            f'fill="{READY}" fill-opacity="0.18" stroke="{READY}" stroke-width="2"/>'
            f'<text x="36" y="{y + 22}" font-family="Georgia, serif" font-size="13" fill="{INK}">'
            f'{escape(layer["glyph"])}  {escape(layer["id"])}</text>'
        )
    # Holes as red circles through the stack
    holes = [h["clip_id"] for h in data["holes"][:6]]
    hole_marks: list[str] = []
    for i, cid in enumerate(holes):
        cx = 340
        cy = 70 + i * 28
        hole_marks.append(
            f'<circle cx="{cx}" cy="{cy}" r="9" fill="none" stroke="{HOLE}" stroke-width="3"/>'
            f'<text x="{cx + 16}" y="{cy + 4}" font-family="Georgia, serif" font-size="10" fill="{HOLE}">{escape(cid)}</text>'
        )
    waiting = data["waiting"] + data["done_not_stacked"] + data["refused"]
    side: list[str] = []
    for i, layer in enumerate(waiting):
        color = {"open": OPEN, "play": PLAY, "refuse": REFUSE}.get(layer["status"], PLAY)
        y = 48 + i * 36
        side.append(
            f'<rect x="520" y="{y}" width="210" height="30" rx="6" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-dasharray="5 4"/>'
            f'<text x="532" y="{y + 20}" font-family="Georgia, serif" font-size="12" fill="{color}">'
            f'{escape(layer["glyph"])}  {escape(layer["id"])}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 {max(48 + n * 28 + 50, 280)}" role="img" aria-label="Overlay of done pieces with holes">
  <rect width="750" height="{max(48 + n * 28 + 50, 280)}" fill="{PAPER}"/>
  <text x="24" y="28" font-family="Georgia, serif" font-size="16" fill="{INK}">Overlay — done pieces, holes through the stack</text>
  {"".join(cards)}
  {"".join(hole_marks)}
  <text x="520" y="28" font-family="Georgia, serif" font-size="13" fill="{INK}">Not stacked</text>
  {"".join(side)}
</svg>'''


def svg_gap(report: dict[str, Any] | None = None) -> str:
    """Walk, wall, missing piece, candidates after — as a picture."""
    data = report or gap_report("B")
    walked = data.get("walked") or []
    wall = data.get("wall") or {}
    n = len(walked)
    nodes: list[str] = []
    for i, step in enumerate(walked):
        x = 28 + i * 88
        nodes.append(
            f'<rect x="{x}" y="70" width="76" height="40" rx="8" fill="{READY}"/>'
            f'<text x="{x + 38}" y="95" text-anchor="middle" font-family="Georgia, serif" '
            f'font-size="12" fill="{PAPER}">{escape(str(step["step"]))}</text>'
        )
        if i + 1 < n:
            nodes.append(f'<line x1="{x + 76}" y1="90" x2="{x + 88}" y2="90" stroke="{READY}" stroke-width="3"/>')
    wx = 28 + n * 88
    nodes.append(f'<line x1="{wx - 12}" y1="90" x2="{wx}" y2="90" stroke="{OPEN}" stroke-width="3"/>')
    nodes.append(
        f'<rect x="{wx}" y="62" width="90" height="56" rx="8" fill="{OPEN}"/>'
        f'<text x="{wx + 45}" y="86" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{PAPER}">'
        f'{escape(str(wall.get("step", "WALL")))}</text>'
        f'<text x="{wx + 45}" y="104" text-anchor="middle" font-family="Georgia, serif" font-size="11" fill="{PAPER}">STOP</text>'
    )
    gx = wx + 110
    nodes.append(
        f'<rect x="{gx}" y="58" width="130" height="64" rx="8" fill="none" stroke="{PLAY}" stroke-width="3" stroke-dasharray="6 4"/>'
        f'<text x="{gx + 65}" y="84" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{INK}">GAP-T3</text>'
        f'<text x="{gx + 65}" y="104" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="{INK}">missing piece</text>'
    )
    cx = gx + 150
    nodes.append(
        f'<rect x="{cx}" y="70" width="76" height="40" rx="8" fill="none" stroke="{INK}" stroke-dasharray="5 4" stroke-width="2"/>'
        f'<text x="{cx + 38}" y="95" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{INK}">T5</text>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 180" role="img" aria-label="Stop at the wall, missing piece, T5 after">
  <rect width="720" height="180" fill="{PAPER}"/>
  <text x="16" y="28" font-family="Georgia, serif" font-size="16" fill="{INK}">Walk until the wall — then you see the hole</text>
  {"".join(nodes)}
  <text x="16" y="160" font-family="Georgia, serif" font-size="12" fill="{INK}">Solid = walked. Red = stop. Gold dashed = missing. Hollow T5 = candidate, not a step.</text>
</svg>'''


def svg_scan(report: dict[str, Any] | None = None) -> str:
    """Jigsaw of stacked pieces, empty slot, rejected matches."""
    data = report or scan_report("B")
    ana = data.get("anatomy") or {}
    named = (data.get("focus") or {}).get("named_matches") or []
    tiles: list[str] = []
    stacked_n = min(int(ana.get("stacked_count") or 0), 9)
    for i in range(stacked_n):
        col, row = i % 3, i // 3
        x, y = 24 + col * 70, 56 + row * 48
        tiles.append(
            f'<rect x="{x}" y="{y}" width="62" height="40" rx="6" fill="#d7efe9" stroke="{READY}" stroke-width="2"/>'
        )
    # Missing slot
    tiles.append(
        f'<rect x="234" y="104" width="90" height="48" rx="8" fill="none" '
        f'stroke="{OPEN}" stroke-width="3" stroke-dasharray="6 4"/>'
        f'<text x="279" y="124" text-anchor="middle" font-family="Georgia, serif" font-size="11" fill="{OPEN}">GAP-T3</text>'
        f'<text x="279" y="140" text-anchor="middle" font-family="Georgia, serif" font-size="10" fill="{OPEN}">empty</text>'
    )
    rejects: list[str] = []
    for i, row in enumerate(named[:6]):
        color = PLAY if row["verdict"] == "LOOKS_LIKE_FIT" else REFUSE
        y = 56 + i * 28
        rejects.append(
            f'<rect x="360" y="{y}" width="250" height="24" rx="5" fill="none" '
            f'stroke="{color}" stroke-width="1.5"/>'
            f'<text x="372" y="{y + 16}" font-family="Georgia, serif" font-size="11" fill="{color}">'
            f'{escape(row["verdict"])}  {escape(row["piece"])}</text>'
        )
    views = ", ".join(ana.get("views") or [])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 250" role="img" aria-label="Scan leftover hole against pieces">
  <rect width="640" height="250" fill="{PAPER}"/>
  <text x="16" y="28" font-family="Georgia, serif" font-size="16" fill="{INK}">Scan — same object, empty slot, no weld</text>
  <text x="16" y="48" font-family="Georgia, serif" font-size="11" fill="{INK}">views: {escape(views)}</text>
  {"".join(tiles)}
  {"".join(rejects)}
  <text x="16" y="230" font-family="Georgia, serif" font-size="11" fill="{INK}">Identified from anatomy. Not smooth. LOOKS_LIKE_FIT is extra E. Wrong-object pieces stay out.</text>
</svg>'''


def svg_shell(report: dict[str, Any] | None = None) -> str:
    """Interior organs, outer identity shell, dashed play shell."""
    data = report or shell_report("B")
    give = data.get("giveaway") or {}
    names = ", ".join(give.get("catalog") or [])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 260" role="img" aria-label="Inside plus outer shell">
  <rect width="520" height="260" fill="{PAPER}"/>
  <text x="16" y="28" font-family="Georgia, serif" font-size="16" fill="{INK}">Inside, then a shell — the outline can already be known</text>
  <ellipse cx="160" cy="140" rx="120" ry="88" fill="none" stroke="{PLAY}" stroke-width="2" stroke-dasharray="7 6"/>
  <ellipse cx="160" cy="140" rx="78" ry="58" fill="none" stroke="{READY}" stroke-width="5"/>
  <circle cx="160" cy="140" r="36" fill="#d7efe9" stroke="{READY}" stroke-width="2"/>
  <text x="160" y="136" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="{INK}">inside</text>
  <text x="160" y="154" text-anchor="middle" font-family="Georgia, serif" font-size="11" fill="{READY}">stacked</text>
  <text x="300" y="88" font-family="Georgia, serif" font-size="13" fill="{READY}">identity shell = T³</text>
  <text x="300" y="110" font-family="Georgia, serif" font-size="12" fill="{READY}">giveaway: {escape(names)}</text>
  <text x="300" y="148" font-family="Georgia, serif" font-size="13" fill="{PLAY}">dashed = even-reflect play</text>
  <text x="300" y="168" font-family="Georgia, serif" font-size="12" fill="{OPEN}">not the original object</text>
  <text x="16" y="242" font-family="Georgia, serif" font-size="11" fill="{INK}">Dead giveaway names the object. It does not fill holes. CLIP-T3-OUTER is extra E.</text>
</svg>'''


def _jigsaw_edge(x0: float, y0: float, x1: float, y1: float, tab: int) -> str:
    """Clockwise edge. tab +1 = knob out, -1 = socket in, 0 = flat."""
    if tab == 0:
        return f"L {x1:.1f} {y1:.1f}"
    dx, dy = x1 - x0, y1 - y0
    length = (dx * dx + dy * dy) ** 0.5 or 1.0
    ux, uy = dx / length, dy / length
    px, py = uy, -ux  # outward for a clockwise path
    mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    sign = 1.0 if tab > 0 else -1.0
    r = min(length * 0.20, 14.0)
    n0x, n0y = mx - ux * r, my - uy * r
    n1x, n1y = mx + ux * r, my + uy * r
    cx, cy = mx + sign * px * r * 1.45, my + sign * py * r * 1.45
    q0x, q0y = n0x + sign * px * r * 0.35, n0y + sign * py * r * 0.35
    q1x, q1y = n1x + sign * px * r * 0.35, n1y + sign * py * r * 0.35
    return (
        f"L {n0x:.1f} {n0y:.1f} "
        f"Q {q0x:.1f} {q0y:.1f} {cx:.1f} {cy:.1f} "
        f"Q {q1x:.1f} {q1y:.1f} {n1x:.1f} {n1y:.1f} "
        f"L {x1:.1f} {y1:.1f}"
    )


def _jigsaw_piece_path(
    x: float, y: float, w: float, h: float, n: int, e: int, s: int, west: int
) -> str:
    top = _jigsaw_edge(x, y, x + w, y, n)
    right = _jigsaw_edge(x + w, y, x + w, y + h, e)
    bot = _jigsaw_edge(x + w, y + h, x, y + h, s)
    left = _jigsaw_edge(x, y + h, x, y, west)
    return f"M {x:.1f} {y:.1f} {top} {right} {bot} {left} Z"


def svg_jigsaw(report: dict[str, Any] | None = None) -> str:
    """Literal interlocking pieces forming a building; holes are damage, not a hill."""
    data = report or jigsaw_report("B")
    pieces = {p["id"]: p for p in data.get("pieces") or []}
    grid: list[tuple[str, int, int]] = [
        ("L1-TORUS", 1, 0),
        ("L12-ENERGY", 0, 1),
        ("L3-BERNSTEIN", 1, 1),
        ("L4-COVER", 2, 1),
        ("L2-FLUX", 0, 2),
        ("L5-RING", 1, 2),
        ("L6-STRAIN", 2, 2),
        ("L7-HARDY", 0, 3),
        ("L8-ANGULAR", 1, 3),
    ]
    ox, oy, w, h = 36.0, 58.0, 78.0, 62.0
    # Neighbor tabs so adjacent pieces interlock.
    tabs: dict[str, tuple[int, int, int, int]] = {
        "L1-TORUS": (0, 0, 1, 0),
        "L12-ENERGY": (0, 1, 1, 0),
        "L3-BERNSTEIN": (-1, 1, 1, -1),
        "L4-COVER": (0, 0, 1, -1),
        "L2-FLUX": (-1, 1, 1, 0),
        "L5-RING": (-1, 1, 1, -1),
        "L6-STRAIN": (-1, 0, 1, -1),
        "L7-HARDY": (-1, 1, 0, 0),
        "L8-ANGULAR": (-1, 1, 0, -1),
    }
    drawn: list[str] = []
    for pid, col, row in grid:
        piece = pieces.get(pid)
        if not piece:
            continue
        x, y = ox + col * w, oy + row * h
        n, e, s, west = tabs[pid]
        d = _jigsaw_piece_path(x, y, w, h, n, e, s, west)
        drawn.append(
            f'<path d="{d}" fill="#d7efe9" stroke="{READY}" stroke-width="2.2"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + h / 2 - 4:.1f}" text-anchor="middle" '
            f'font-family="Georgia, serif" font-size="10" fill="{INK}">{escape(piece["glyph"])}</text>'
            f'<text x="{x + w / 2:.1f}" y="{y + h / 2 + 10:.1f}" text-anchor="middle" '
            f'font-family="Georgia, serif" font-size="9" fill="{READY}">{escape(pid.split("-", 1)[-1])}</text>'
        )
    # Empty socket where a waiting piece would go (Parthenon hole in the wall).
    wx, wy = ox + 2 * w, oy + 3 * h
    missing = _jigsaw_piece_path(wx, wy, w, h, -1, 0, 0, -1)
    drawn.append(
        f'<path d="{missing}" fill="none" stroke="{OPEN}" stroke-width="2.4" stroke-dasharray="6 4"/>'
        f'<text x="{wx + w / 2:.1f}" y="{wy + h / 2:.1f}" text-anchor="middle" '
        f'font-family="Georgia, serif" font-size="10" fill="{OPEN}">GAP-T3</text>'
    )
    # Cannon holes through the assembled building (order-1).
    holes_1 = [(ox + 1.5 * w, oy + 2.2 * h, "WELD"), (ox + 0.55 * w, oy + 3.15 * h, "TUBE")]
    hole_marks: list[str] = []
    for cx, cy, label in holes_1:
        hole_marks.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="11" fill="{PAPER}" stroke="{OPEN}" stroke-width="3"/>'
            f'<text x="{cx:.1f}" y="{cy + 4:.1f}" text-anchor="middle" font-family="Georgia, serif" '
            f'font-size="8" fill="{OPEN}">{label}</text>'
        )
    # Order-2 pockmarks
    pocks = [(ox + 2.35 * w, oy + 1.35 * h), (ox + 0.4 * w, oy + 1.45 * h)]
    for cx, cy in pocks:
        hole_marks.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="none" stroke="{PLAY}" stroke-width="2"/>'
        )
    # Energy path through the snapped pieces — this is how it works.
    arrows = (
        f'<path d="M {ox + 0.5 * w:.1f} {oy + 1.55 * h:.1f} '
        f'L {ox + 1.5 * w:.1f} {oy + 1.55 * h:.1f} '
        f'L {ox + 1.5 * w:.1f} {oy + 2.55 * h:.1f} '
        f'L {ox + 0.5 * w:.1f} {oy + 3.55 * h:.1f}" '
        f'fill="none" stroke="{INK}" stroke-width="2.2"/>'
        f'<text x="{ox + 1.62 * w:.1f}" y="{oy + 1.42 * h:.1f}" '
        f'font-family="Georgia, serif" font-size="10" fill="{INK}">energy</text>'
        f'<text x="{ox + 0.08 * w:.1f}" y="{oy + 3.72 * h:.1f}" '
        f'font-family="Georgia, serif" font-size="10" fill="{INK}">visc 1/r²</text>'
    )
    # Goal line the energy path crosses. Identification, not smoothness.
    goal_y = oy + 2.05 * h
    goal_mark = (
        f'<line x1="{ox - 8:.1f}" y1="{goal_y:.1f}" x2="{ox + 3.05 * w:.1f}" y2="{goal_y:.1f}" '
        f'stroke="{PLAY}" stroke-width="3"/>'
        f'<text x="{ox - 6:.1f}" y="{goal_y - 6:.1f}" font-family="Georgia, serif" '
        f'font-size="11" fill="{PLAY}">GOAL</text>'
    )
    over = bool((data.get("goal") or {}).get("over"))
    over_line = (
        "OVER THE GOAL — this is the object. This is how energy goes through it."
        if over
        else "Short of the goal — not yet named, or no energy path."
    )
    # Play piece (even-reflect) off to the side — extra E, not a wall.
    play_d = _jigsaw_piece_path(ox + 3.4 * w, oy + 0.2 * h, w, h, 0, 0, 0, 1)
    play = (
        f'<path d="{play_d}" fill="none" stroke="{PLAY}" stroke-width="2" stroke-dasharray="5 4"/>'
        f'<text x="{ox + 3.9 * w:.1f}" y="{oy + 0.2 * h + h / 2:.1f}" text-anchor="middle" '
        f'font-family="Georgia, serif" font-size="10" fill="{PLAY}">play )δ(</text>'
    )
    # Rubble (order-3) on the ground.
    rubble = (
        f'<rect x="{ox + 3.4 * w:.1f}" y="{oy + 3.35 * h:.1f}" width="{w:.1f}" height="22" '
        f'rx="4" fill="none" stroke="{REFUSE}" stroke-width="1.5"/>'
        f'<text x="{ox + 3.9 * w:.1f}" y="{oy + 3.35 * h + 15:.1f}" text-anchor="middle" '
        f'font-family="Georgia, serif" font-size="10" fill="{REFUSE}">rubble Φ!</text>'
    )
    # Hill silhouette — the thing this is not.
    hill = (
        f'<path d="M {ox + 3.35 * w:.1f} {oy + 2.55 * h:.1f} '
        f'Q {ox + 3.85 * w:.1f} {oy + 1.35 * h:.1f} {ox + 4.45 * w:.1f} {oy + 2.55 * h:.1f} Z" '
        f'fill="none" stroke="{REFUSE}" stroke-width="2" stroke-dasharray="7 5"/>'
        f'<text x="{ox + 3.9 * w:.1f}" y="{oy + 2.85 * h:.1f}" text-anchor="middle" '
        f'font-family="Georgia, serif" font-size="12" fill="{REFUSE}">not a hill</text>'
    )
    verdict = data.get("building", {}).get("verdict", "BUILDING")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 370" role="img" aria-label="Jigsaw building assembled from pieces, energy path over the goal">
  <rect width="520" height="370" fill="{PAPER}"/>
  <text x="16" y="24" font-family="Georgia, serif" font-size="15" fill="{INK}">{escape(over_line)}</text>
  <text x="16" y="44" font-family="Georgia, serif" font-size="12" fill="{READY}">{verdict}  not a hill. Finest detail not required.</text>
  {"".join(drawn)}
  {goal_mark}
  {arrows}
  {"".join(hole_marks)}
  {play}
  {hill}
  {rubble}
  <text x="16" y="358" font-family="Georgia, serif" font-size="11" fill="{INK}">Gold GOAL is identification: named + how energy moves. Red holes still block the walk. Not smoothness.</text>
</svg>'''


def render_html(state: dict[str, Any] | None = None) -> str:
    overlay = overlay_report()
    gap = gap_report("B")
    energy = energy_play()
    cyl = play_cylinder()
    even = next(c for c in cyl["completions"] if c["id"] == "even_reflect")
    scan = scan_report("B")
    shell = shell_report("B")
    jigsaw = jigsaw_report("B")
    st = state or load_focus()
    live = st.get("live") or FOCUS_LINE.get(st.get("action", "see"), FOCUS_LINE["see"])
    title = st.get("title") or TITLES.get(st.get("action", "see"), TITLES["see"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Domain Architect — see</title>
  <style>
    :root {{ color-scheme: light; }}
    body {{
      margin: 0; font-family: Georgia, "Times New Roman", serif;
      background: {PAPER}; color: {INK}; line-height: 1.45;
    }}
    header, main {{ max-width: 760px; margin: 0 auto; padding: 1.2rem 1.2rem 0; }}
    h1 {{ font-size: 1.6rem; font-weight: 600; margin: 0 0 .3rem; }}
    .banner {{
      background: {INK}; color: {PAPER}; padding: .5rem .8rem; border-radius: 8px;
      font-size: .95rem;
    }}
    .live {{
      margin: .8rem 0 0; padding: .6rem .8rem; border: 1px solid {PLAY};
      border-radius: 8px; background: #fffaf0;
    }}
    .live strong {{ color: {INK}; font-weight: 600; }}
    .note {{ font-size: .95rem; margin: .8rem 0 1.2rem; }}
    figure {{ margin: 0 0 1.6rem; }}
    figcaption {{ font-size: .9rem; margin-top: .4rem; color: #444; }}
    details {{ margin: .4rem 0 0; font-family: ui-monospace, monospace; font-size: .8rem; }}
    svg {{ width: 100%; height: auto; display: block; border-radius: 10px; }}
    footer {{ max-width: 760px; margin: 0 auto; padding: 0 1.2rem 2rem; font-size: .85rem; color: #555; }}
  </style>
</head>
<body>
  <header>
    <p class="banner">Human see. Math is git. Not a proof. Not CosmoEvolution.</p>
    <h1>See the pieces, then the stack, then the hole</h1>
    <p class="live"><strong>Now looking at:</strong> {escape(str(title))}<br/>{escape(str(live))}</p>
    <p class="note">
      Visual appendage of the think tank. The picture follows the math you just ran.
      Pictures first. Inequalities are under each figure.
      Overlay stacks {overlay["composite"]["counts"]["stacked"]} done layers.
      Complete? {str(overlay["composite"]["is_complete"]).lower()}.
      Regularity? {str(overlay["composite"]["is_regularity"]).lower()}.
    </p>
  </header>
  <main>
    <figure>
      {svg_jigsaw(jigsaw)}
      <figcaption>Literal jigsaw. Gold GOAL line is identification: named, and how energy goes through the pieces. Finest detail is not required. Red holes still block the walk. Dashed hill is the wrong object.</figcaption>
      <details><summary>Math</summary>
        Goal over? {str((jigsaw.get("goal") or {}).get("over")).lower()}.
        Fills walk? {str((jigsaw.get("goal") or {}).get("fills_walk")).lower()}.
        Verdict {escape(str(jigsaw["building"]["verdict"]))} not {escape(str(jigsaw["building"]["not"]))}.
        Smooth? {str(jigsaw["smooth"]).lower()}.
        Energy path: {escape(" → ".join(jigsaw.get("energy_path") or []))}.
      </details>
    </figure>
    <figure>
      {svg_cylinder()}
      <figcaption>The wall is a cut. Green disk is Hardy (done). Gold ring is the wall. Dashed outside is not NS.</figcaption>
      <details><summary>Math</summary>
        Even reflect buys T3a on a toy field (Young holds={even["young_holds"]}).
        Does not buy CLIP-T3-WELD. Cylinder spark inside: {escape(cyl["inside"]["spark"])}.
      </details>
    </figure>
    <figure>
      {svg_energy()}
      <figcaption>You can see kinetic energy. Bernstein fills enstrophy and warps the pile. The tube is not filled from the outside.</figcaption>
      <details><summary>Math</summary>
        {escape(energy["identity"]["fill"])}.
        Outside fills tube? {energy["gap"]["outside_fills_tube"]}.
        Energy bounds X? {energy["gap"]["energy_fills_X_infty"]}.
      </details>
    </figure>
    <figure>
      {svg_overlay(overlay)}
      <figcaption>Done layers stacked like transparencies. Red rings are holes. Dashed cards are not in the general shape.</figcaption>
      <details><summary>Math</summary>
        Composite is: {escape(overlay["composite"]["what_it_is"])}
        Is not: {escape(overlay["composite"]["what_it_is_not"])}
      </details>
    </figure>
    <figure>
      {svg_gap(gap)}
      <figcaption>Walk the green steps. Stop at red. The gold dashed box is the missing piece. Hollow T5 is after, not walked.</figcaption>
      <details><summary>Math</summary>
        Wall {escape(str((gap.get("wall") or {}).get("step")))} clip {escape(str((gap.get("wall") or {}).get("clip_id")))}.
        Missing {escape(str((gap.get("missing") or {}).get("gap_id")))} between {escape(str((gap.get("missing") or {}).get("between")))}.
      </details>
    </figure>
    <figure>
      {svg_scan(scan)}
      <figcaption>Same object, many views. Empty slot is the leftover. Gold LOOKS_LIKE_FIT is not a fill. Wrong-object pieces stay out.</figcaption>
      <details><summary>Math</summary>
        Identified? {str(scan["anatomy"]["identified"]).lower()}.
        Smooth? {str(scan["anatomy"]["smooth"]).lower()}.
        Views: {escape(", ".join(scan["anatomy"]["views"]))}.
        Any fill? {str(scan["focus"]["any_fill"]).lower()}.
      </details>
    </figure>
    <figure>
      {svg_shell(shell)}
      <figcaption>Green interior is stacked pieces. Solid ring is the real outer shape. Dashed ring is an invented shell (play). If the solid outline is already in the catalog, that is a dead giveaway.</figcaption>
      <details><summary>Math</summary>
        Dead giveaway? {str(shell["giveaway"]["dead_giveaway"]).lower()}.
        Catalog: {escape(", ".join(shell["giveaway"]["catalog"]))}.
        Smooth? {str(shell["giveaway"]["smooth"]).lower()}.
        Play clip: {escape(str(shell["play_shell"]["clip_id"]))}.
      </details>
    </figure>
  </main>
  <footer>
    Domain Architect package · think tank + visual appendage.
    Store of record is git, not this page.
    CosmoEvolution 3D is visualization only and is not this appendage.
  </footer>
</body>
</html>
"""


def write_see(path: str | Path | None = None) -> Path:
    dest = Path(path) if path is not None else Path(DEFAULT_HTML)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(render_html(load_focus()), encoding="utf-8")
    # Sibling SVGs so markdown can show the pictures on GitHub.
    dest.with_name("see-cylinder.svg").write_text(svg_cylinder(), encoding="utf-8")
    dest.with_name("see-energy.svg").write_text(svg_energy(), encoding="utf-8")
    dest.with_name("see-overlay.svg").write_text(svg_overlay(), encoding="utf-8")
    dest.with_name("see-gap.svg").write_text(svg_gap(), encoding="utf-8")
    dest.with_name("see-scan.svg").write_text(svg_scan(), encoding="utf-8")
    dest.with_name("see-shell.svg").write_text(svg_shell(), encoding="utf-8")
    dest.with_name("see-jigsaw.svg").write_text(svg_jigsaw(), encoding="utf-8")
    return dest
