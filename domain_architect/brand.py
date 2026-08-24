"""Domain Architect mark: parametric chrome A + rainbow triskelion.

The official mark is the open silver A with a three-arm swirl. Two
factory looks match the user renders: gold wordmark, and all-silver.
Sliders in the desktop Mark studio drive the same parameter object.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any


@dataclass
class MarkParams:
    size: int = 1024
    corner: float = 0.20
    frame: float = 0.055
    bg: str = "#161616"
    grain: float = 0.42
    light_angle: float = -38.0
    light: float = 0.88
    bevel: float = 0.55
    a_scale: float = 0.36
    a_thick: float = 0.11
    a_metal: str = "#d8d8d8"
    swirl_scale: float = 0.155
    swirl_rot: float = -18.0
    swirl_spread: float = 1.0
    arm_width: float = 0.048
    hue: float = 0.0
    sat: float = 1.0
    glow: float = 0.65
    sphere: float = 0.028
    sphere_metal: str = "#e6c35a"
    domain_metal: str = "#e6c35a"
    architect_metal: str = "#e8e8e8"
    tagline_metal: str = "#d4b45a"
    tracking: float = 0.34
    show_wordmark: bool = True
    show_tagline: bool = True
    show_frame: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "MarkParams":
        allowed = {f.name: f for f in fields(cls)}
        base = cls()
        for key, value in dict(data or {}).items():
            if key not in allowed:
                continue
            current = getattr(base, key)
            if isinstance(current, bool):
                if isinstance(value, str):
                    setattr(base, key, value.strip().lower() in {"1", "true", "yes", "on"})
                else:
                    setattr(base, key, bool(value))
            elif isinstance(current, int) and not isinstance(current, bool):
                setattr(base, key, int(value))
            elif isinstance(current, float):
                setattr(base, key, float(value))
            else:
                setattr(base, key, str(value))
        return base


PRESETS: dict[str, MarkParams] = {
    "gold": MarkParams(),
    "silver": MarkParams(
        sphere_metal="#e8e8e8",
        domain_metal="#e8e8e8",
        architect_metal="#f0f0f0",
        tagline_metal="#d0d0d0",
        hue=8.0,
        sat=0.92,
        light=0.90,
        a_metal="#dcdcdc",
    ),
    "icon": MarkParams(
        show_wordmark=False,
        show_tagline=False,
        a_scale=0.52,
        swirl_scale=0.22,
        arm_width=0.07,
        sphere=0.04,
        sphere_metal="#e6c35a",
    ),
}


def icon_params(params: MarkParams) -> MarkParams:
    """App-icon crop: same metals and rainbow, no type, larger A."""
    icon = deepcopy(params)
    icon.show_wordmark = False
    icon.show_tagline = False
    icon.a_scale = max(params.a_scale, 0.48)
    icon.swirl_scale = max(params.swirl_scale, 0.20)
    icon.arm_width = max(params.arm_width, 0.06)
    icon.sphere = max(params.sphere, 0.036)
    return icon


def _metal_stops(hex_color: str, light: float) -> tuple[str, str, str]:
    hi = _mix(hex_color, "#ffffff", 0.45 + 0.25 * light)
    lo = _mix(hex_color, "#000000", 0.35)
    return hi, hex_color, lo


def _mix(a: str, b: str, t: float) -> str:
    def rgb(h: str) -> tuple[int, int, int]:
        h = h.lstrip("#")
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    ar, ag, ab = rgb(a)
    br, bg, bb = rgb(b)
    t = max(0.0, min(1.0, t))
    return "#{:02x}{:02x}{:02x}".format(
        int(ar + (br - ar) * t),
        int(ag + (bg - ag) * t),
        int(ab + (bb - ab) * t),
    )


def _hsl(h: float, s: float, l: float) -> str:
    h = h % 360
    s = max(0.0, min(1.0, s))
    l = max(0.0, min(1.0, l))
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return "#{:02x}{:02x}{:02x}".format(
        int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)
    )


def render_mark_svg(params: MarkParams | dict[str, Any] | None = None) -> str:
    p = params if isinstance(params, MarkParams) else MarkParams.from_dict(params)
    s = p.size
    cx = s / 2
    hi, mid, lo = _metal_stops(p.a_metal, p.light)
    shi, smid, slo = _metal_stops("#cfd3d8", p.light)
    ghi, gmid, glo = _metal_stops(p.domain_metal, p.light)
    ahi, amid, alo = _metal_stops(p.architect_metal, p.light)
    sph_hi, sph, sph_lo = _metal_stops(p.sphere_metal, p.light)

    corner = p.corner * s
    frame = p.frame * s
    a_h = p.a_scale * s
    a_w = a_h * 0.92
    thick = p.a_thick * s
    ay = s * (0.30 if p.show_wordmark else 0.50)
    swirl_r = p.swirl_scale * s * p.swirl_spread
    arm_w = p.arm_width * s
    hues = [(p.hue + i * 120) % 360 for i in range(3)]

    arms = []
    for i, hue in enumerate(hues):
        rot = p.swirl_rot + i * 120
        c1 = _hsl(hue, p.sat, 0.58)
        c2 = _hsl(hue + 50, p.sat, 0.42)
        c3 = _hsl(hue + 90, p.sat, 0.48)
        arms.append((i, rot, c1, c2, c3))

    grain = max(0.0, min(1.0, p.grain))
    word_y = s * 0.72
    arch_y = s * 0.82
    tag_y = s * 0.90
    track = p.tracking
    frame_rx = corner
    inner_rx = max(0.0, frame_rx - frame * 0.6)
    bevel_w = max(1.5, thick * (0.22 + 0.28 * p.bevel))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s} {s}" width="{s}" height="{s}" role="img" aria-label="Domain Architect">
  <title>Domain Architect</title>
  <desc>Official mark: open chrome A, rainbow triskelion, optional gold or silver wordmark.</desc>
  <defs>
    <linearGradient id="frameGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{shi}"/>
      <stop offset="45%" stop-color="{smid}"/>
      <stop offset="100%" stop-color="{slo}"/>
    </linearGradient>
    <linearGradient id="aGrad" gradientTransform="rotate({p.light_angle} {cx} {ay})">
      <stop offset="0%" stop-color="{hi}"/>
      <stop offset="48%" stop-color="{mid}"/>
      <stop offset="100%" stop-color="{lo}"/>
    </linearGradient>
    <linearGradient id="aHi" gradientTransform="rotate({p.light_angle} {cx} {ay})">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="40%" stop-color="{hi}"/>
      <stop offset="100%" stop-color="{mid}"/>
    </linearGradient>
    <linearGradient id="domainGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{ghi}"/>
      <stop offset="55%" stop-color="{gmid}"/>
      <stop offset="100%" stop-color="{glo}"/>
    </linearGradient>
    <linearGradient id="archGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{ahi}"/>
      <stop offset="55%" stop-color="{amid}"/>
      <stop offset="100%" stop-color="{alo}"/>
    </linearGradient>
    <radialGradient id="sphereGrad" cx="35%" cy="30%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="35%" stop-color="{sph_hi}"/>
      <stop offset="100%" stop-color="{sph_lo}"/>
    </radialGradient>
    <filter id="grain">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7"/>
      <feColorMatrix type="luminanceToAlpha"/>
      <feComponentTransfer>
        <feFuncA type="table" tableValues="0 {grain * 0.55}"/>
      </feComponentTransfer>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="{max(1.2, p.glow * 6):.1f}" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="drop">
      <feDropShadow dx="{s * 0.006:.1f}" dy="{s * 0.01:.1f}" stdDeviation="{s * 0.006:.1f}" flood-color="#000" flood-opacity="0.55"/>
    </filter>
    <clipPath id="inner">
      <rect x="{frame}" y="{frame}" width="{s - 2 * frame}" height="{s - 2 * frame}" rx="{inner_rx}"/>
    </clipPath>
'''
    for i, _rot, c1, c2, c3 in arms:
        svg += (
            f'    <linearGradient id="arm{i}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0%" stop-color="{c1}"/>'
            f'<stop offset="55%" stop-color="{c2}"/>'
            f'<stop offset="100%" stop-color="{c3}"/>'
            f"</linearGradient>\n"
        )
    svg += "  </defs>\n"
    if p.show_frame:
        svg += f'  <rect width="{s}" height="{s}" rx="{frame_rx}" fill="url(#frameGrad)"/>\n'
        svg += f'  <rect x="{frame}" y="{frame}" width="{s - 2 * frame}" height="{s - 2 * frame}" rx="{inner_rx}" fill="{p.bg}"/>\n'
        svg += (
            f'  <rect x="{frame}" y="{frame}" width="{s - 2 * frame}" height="{s - 2 * frame}" '
            f'rx="{inner_rx}" fill="none" stroke="#ffffff" stroke-opacity="0.22" '
            f'stroke-width="{max(1.2, s * 0.004):.1f}"/>\n'
        )
    else:
        svg += f'  <rect width="{s}" height="{s}" rx="{frame_rx}" fill="{p.bg}"/>\n'
    svg += f'  <rect x="0" y="0" width="{s}" height="{s}" rx="{frame_rx}" filter="url(#grain)" opacity="0.9" clip-path="url(#inner)"/>\n'

    apex_x, apex_y = cx, ay - a_h * 0.52
    left_x, left_y = cx - a_w * 0.52, ay + a_h * 0.48
    right_x, right_y = cx + a_w * 0.52, ay + a_h * 0.48
    a_path = (
        f"M {left_x:.1f} {left_y:.1f} L {apex_x:.1f} {apex_y:.1f} L {right_x:.1f} {right_y:.1f}"
    )
    svg += (
        f'  <path d="{a_path}" fill="none" stroke="url(#aGrad)" stroke-width="{thick:.1f}" '
        f'stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="2.4" filter="url(#drop)"/>\n'
        f'  <path d="{a_path}" fill="none" stroke="url(#aHi)" stroke-width="{bevel_w:.1f}" '
        f'stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="2.4" opacity="0.55"/>\n'
    )

    for i, rot, _c1, _c2, _c3 in arms:
        arm_d = (
            f"M {cx:.1f} {ay - swirl_r * 0.16:.1f} "
            f"C {cx + swirl_r * 0.62:.1f} {ay - swirl_r * 0.02:.1f} "
            f"{cx + swirl_r * 1.02:.1f} {ay + swirl_r * 0.38:.1f} "
            f"{cx + swirl_r * 0.08:.1f} {ay + swirl_r * 0.98:.1f}"
        )
        svg += (
            f'  <g transform="rotate({rot:.1f} {cx:.1f} {ay:.1f})" filter="url(#softGlow)">\n'
            f'    <path d="{arm_d}" fill="none" stroke="#d8d8d8" '
            f'stroke-width="{arm_w * 1.28:.1f}" stroke-linecap="round"/>\n'
            f'    <path d="{arm_d}" fill="none" stroke="url(#arm{i})" '
            f'stroke-width="{arm_w:.1f}" stroke-linecap="round"/>\n'
            f"  </g>\n"
        )
    svg += f'  <circle cx="{cx:.1f}" cy="{ay:.1f}" r="{p.sphere * s:.1f}" fill="url(#sphereGrad)"/>\n'

    if p.show_wordmark:
        svg += (
            f'  <text x="{cx}" y="{word_y:.1f}" text-anchor="middle" '
            f'font-family="ui-sans-serif, system-ui, sans-serif" font-weight="700" '
            f'font-size="{s * 0.055:.1f}" letter-spacing="{track * s * 0.02:.1f}" '
            f'fill="url(#domainGrad)">DOMAIN</text>\n'
            f'  <text x="{cx}" y="{arch_y:.1f}" text-anchor="middle" '
            f'font-family="ui-sans-serif, system-ui, sans-serif" font-weight="700" '
            f'font-size="{s * 0.072:.1f}" letter-spacing="{track * s * 0.012:.1f}" '
            f'fill="url(#archGrad)">ARCHITECT</text>\n'
        )
    if p.show_tagline:
        svg += (
            f'  <text x="{cx}" y="{tag_y:.1f}" text-anchor="middle" '
            f'font-family="ui-sans-serif, system-ui, sans-serif" font-weight="600" '
            f'font-size="{s * 0.028:.1f}" letter-spacing="{s * 0.006:.1f}" '
            f'fill="{p.tagline_metal}">DECOMPOSE · TRANSLATE · SYNTHESIZE</text>\n'
        )
    svg += "</svg>\n"
    return svg


def preset_svg(name: str = "icon") -> str:
    if name not in PRESETS:
        raise KeyError(name)
    return render_mark_svg(deepcopy(PRESETS[name]))


def _icon_targets(root: Path) -> list[Path]:
    return [
        root / "assets" / "domain-architect.svg",
        root / "assets" / "brand" / "domain-architect.svg",
        root / "domain_architect" / "static" / "favicon.svg",
    ]


def apply_mark_files(svg: str, repo_root: str | Path) -> list[str]:
    """Write the live app icon + favicon from an SVG string."""
    root = Path(repo_root)
    payload = svg.encode("utf-8")
    if b"<svg" not in payload.lower():
        raise ValueError("not an SVG document")
    if len(payload) > 2_000_000:
        raise ValueError("SVG too large")
    written = []
    for path in _icon_targets(root):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        written.append(str(path))
    return written


def apply_mark_from_params(
    params: MarkParams | dict[str, Any] | None,
    repo_root: str | Path,
) -> dict[str, Any]:
    """Write live icon (no type) plus lockup SVG from slider params."""
    root = Path(repo_root)
    p = params if isinstance(params, MarkParams) else MarkParams.from_dict(params)
    lockup = render_mark_svg(p)
    icon = render_mark_svg(icon_params(p))
    written = apply_mark_files(icon, root)
    brand = root / "assets" / "brand"
    brand.mkdir(parents=True, exist_ok=True)
    lockup_path = brand / "domain-architect-official.svg"
    lockup_path.write_text(lockup, encoding="utf-8")
    written.append(str(lockup_path))
    if p.show_wordmark:
        word_path = brand / "domain-architect-wordmark.svg"
        word_path.write_text(lockup, encoding="utf-8")
        written.append(str(word_path))
    return {
        "written": written,
        "icon": icon,
        "lockup": lockup,
        "params": p.to_dict(),
    }


def preserve_legacy_spine(repo_root: str | Path) -> Path | None:
    """Keep the earlier spine/cyan glyph as an exploratory file once."""
    root = Path(repo_root)
    current = root / "assets" / "brand" / "domain-architect.svg"
    legacy = root / "assets" / "brand" / "exploratory-spine.svg"
    if not current.exists() or legacy.exists():
        return None
    raw = current.read_bytes()
    if b"#2EC4D6" not in raw:
        return None
    legacy.write_bytes(raw)
    return legacy


def write_factory_marks(repo_root: str | Path) -> dict[str, str]:
    """Install gold, silver, and icon factory files."""
    root = Path(repo_root)
    preserve_legacy_spine(root)
    brand = root / "assets" / "brand"
    brand.mkdir(parents=True, exist_ok=True)
    gold = preset_svg("gold")
    silver = preset_svg("silver")
    icon = preset_svg("icon")
    apply_mark_files(icon, root)
    (brand / "domain-architect-wordmark.svg").write_text(gold, encoding="utf-8")
    (brand / "domain-architect-silver.svg").write_text(silver, encoding="utf-8")
    (brand / "domain-architect-official.svg").write_text(gold, encoding="utf-8")
    (brand / "domain-architect-icon.svg").write_text(icon, encoding="utf-8")
    return {
        "gold": str(brand / "domain-architect-wordmark.svg"),
        "silver": str(brand / "domain-architect-silver.svg"),
        "icon": str(root / "assets" / "domain-architect.svg"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Domain Architect mark renderer")
    parser.add_argument("--preset", choices=sorted(PRESETS), default="icon")
    parser.add_argument("--apply", action="store_true", help="write factory marks into assets/")
    parser.add_argument("--stdout", action="store_true", help="print SVG to stdout")
    args = parser.parse_args(argv)
    if args.apply:
        paths = write_factory_marks(Path(__file__).resolve().parent.parent)
        for key, path in paths.items():
            print(f"{key}: {path}")
        return 0
    svg = preset_svg(args.preset)
    if args.stdout:
        print(svg, end="")
    else:
        print(svg[:120].split("\n", 1)[0])
        print(f"preset={args.preset} bytes={len(svg.encode())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
