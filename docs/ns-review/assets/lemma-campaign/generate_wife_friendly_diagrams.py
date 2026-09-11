#!/usr/bin/env python3
"""Generate cream/tan Lemma★ campaign diagrams matching the barycenter orbit map style.

Honest footer on every figure. ★ NOT proved · NS NOT solved · kill lane LIVE.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Arc, Rectangle, Polygon
from matplotlib.lines import Line2D
import numpy as np
from matplotlib import font_manager

OUT = Path(__file__).resolve().parent
ART = Path("/opt/cursor/artifacts/lemma-star-paper")
ART.mkdir(parents=True, exist_ok=True)

# Visual tokens matching Jonathan's barycenter maps
CREAM = "#F4EBD8"
CREAM_DARK = "#E8DCC4"
INK = "#1A1208"
BROWN = "#6B4E2E"
BROWN_SOFT = "#A08060"
RED = "#8B1E1E"
RED_SOFT = "#B84A3A"
WHITE = "#FFFDF8"
FOOTER_BG = "#D9C9A8"
NEAR = "#D8D0C0"

for fp in (
    "/tmp/LibreBaskerville-Regular.ttf",
    "/tmp/LibreBaskerville-Bold.ttf",
    "/tmp/SourceSans3-Regular.ttf",
    "/tmp/SourceSans3-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
):
    p = Path(fp)
    if p.exists():
        font_manager.fontManager.addfont(str(p))

DISPLAY = "DejaVu Sans"
BODY = "DejaVu Sans"  # reliable ★ ≠ glyphs; cream diagrams stay readable
avail = {f.name for f in font_manager.fontManager.ttflist}
if DISPLAY not in avail:
    DISPLAY = "DejaVu Sans"

plt.rcParams.update(
    {
        "font.family": BODY,
        "text.color": INK,
        "axes.edgecolor": BROWN,
        "figure.facecolor": CREAM,
        "axes.facecolor": CREAM,
        "savefig.facecolor": CREAM,
        "savefig.bbox": "tight",
        "savefig.dpi": 160,
    }
)

# Use ASCII-friendly star in matplotlib text where Libre Baskerville lacks ★
STAR = "★"
OUTCOME = f"Outcome: {STAR} NOT proved · NS NOT solved · kill lane LIVE · uniform R{STAR} / HH→L still open"


def set_mixed_font(ax_text_kwargs=None):
    """Prefer DejaVu for glyphs missing from display fonts."""
    return {"fontfamily": "DejaVu Sans"}


def save(fig, name: str) -> Path:
    path = OUT / name
    fig.savefig(path, dpi=160, facecolor=CREAM, edgecolor="none")
    fig.savefig(ART / name, dpi=160, facecolor=CREAM, edgecolor="none")
    plt.close(fig)
    print("wrote", path)
    return path


def footer(ax, y=0.045, text=OUTCOME):
    ax.add_patch(
        FancyBboxPatch(
            (0.06, y - 0.018),
            0.88,
            0.055,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            transform=ax.transAxes,
            facecolor=FOOTER_BG,
            edgecolor=BROWN,
            linewidth=1.2,
            clip_on=False,
            zorder=20,
        )
    )
    ax.text(
        0.5,
        y + 0.01,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=9.5,
        color=INK,
        fontfamily=BODY,
        fontweight="regular",
        zorder=21,
    )


def title_block(ax, title: str, subtitle: str):
    ax.text(
        0.5,
        0.955,
        title,
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=18,
        fontfamily=DISPLAY,
        fontweight="bold",
        color=INK,
    )
    ax.text(
        0.5,
        0.905,
        subtitle,
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=11,
        fontfamily=DISPLAY,
        style="italic",
        color=BROWN,
    )


def rounded_label(ax, xy, w, h, text, *, ec=RED, fc=WHITE, fontsize=9.5, tw=1.6):
    x, y = xy
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.008,rounding_size=0.012",
            facecolor=fc,
            edgecolor=ec,
            linewidth=tw,
            zorder=5,
        )
    )
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=ec if ec == RED else INK,
        fontfamily=BODY,
        zorder=6,
        linespacing=1.25,
    )


# ---------------------------------------------------------------------------
# 1. Tea cup — viscosity melts the hard edges
# ---------------------------------------------------------------------------
def fig_tea_cup():
    fig, ax = plt.subplots(figsize=(11.2, 9.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    title_block(
        ax,
        "Lemma★ — the tea-cup picture",
        "Hot tea cools. Sharp swirls soften. Viscosity melts the hard edges — but shape remains.",
    )

    # Saucer
    ax.add_patch(
        mpatches.Ellipse((5, 2.55), 4.6, 0.55, facecolor=CREAM_DARK, edgecolor=BROWN, lw=1.8, zorder=1)
    )
    # Cup body
    cup = Polygon(
        [(3.15, 2.7), (3.45, 5.35), (6.55, 5.35), (6.85, 2.7)],
        closed=True,
        facecolor=WHITE,
        edgecolor=BROWN,
        lw=2.2,
        zorder=2,
    )
    ax.add_patch(cup)
    # Tea surface
    ax.add_patch(
        mpatches.Ellipse((5, 5.2), 2.95, 0.42, facecolor="#C4A882", edgecolor=BROWN, lw=1.4, zorder=3)
    )
    # Handle
    ax.add_patch(
        Arc((6.85, 4.0), 1.35, 1.9, angle=0, theta1=-70, theta2=70, lw=2.4, color=BROWN, zorder=3)
    )
    ax.add_patch(
        Arc((6.85, 4.0), 0.95, 1.4, angle=0, theta1=-65, theta2=65, lw=1.4, color=BROWN_SOFT, zorder=3)
    )

    # Swirl lines in tea (softening)
    for i, (amp, phase, alpha) in enumerate([(0.55, 0, 0.9), (0.4, 1.2, 0.55), (0.28, 2.4, 0.35)]):
        t = np.linspace(0, 2 * np.pi, 200)
        x = 5 + amp * np.cos(t + phase) * (1 - 0.15 * i)
        y = 5.2 + 0.12 * np.sin(2 * t + phase) - 0.02 * i
        ax.plot(x, y, color=RED if i == 0 else BROWN, lw=1.8 - 0.4 * i, alpha=alpha, zorder=4)

    # Melt arrows / labels
    ax.annotate(
        "sharp swirl\n(dangerous stretch)",
        xy=(4.55, 5.25),
        xytext=(1.15, 7.35),
        fontsize=10,
        color=RED,
        fontfamily=BODY,
        arrowprops=dict(arrowstyle="->", color=RED, lw=1.5),
        ha="center",
    )
    ax.annotate(
        "viscosity melts\n(outer packaging)",
        xy=(5.9, 4.55),
        xytext=(8.55, 7.2),
        fontsize=10,
        color=BROWN,
        fontfamily=BODY,
        arrowprops=dict(arrowstyle="->", color=BROWN, lw=1.5),
        ha="center",
    )

    rounded_label(
        ax,
        (1.0, 1.15),
        8.0,
        0.85,
        "Wife-friendly: the tea cools — edges soften — but the shape of the swirl is still the question.\nLemma★ asks whether that shape-danger stays bounded for every smooth cup.",
        ec=BROWN,
        fc=WHITE,
        fontsize=10,
        tw=1.4,
    )
    footer(ax)
    # Reposition footer in data? footer uses axes — ok
    save(fig, "01-tea-cup-viscosity-melts.png")


# ---------------------------------------------------------------------------
# 2. Shape ≠ size
# ---------------------------------------------------------------------------
def fig_shape_ne_size():
    fig, ax = plt.subplots(figsize=(11.2, 9.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    title_block(
        ax,
        "Shape ≠ size",
        "Turn the volume up. Turn viscosity. The Lemma★ score should not care — only the shape.",
    )

    # Two blobs: same shape, different size
    def blob(cx, cy, s, color, label, sub):
        t = np.linspace(0, 2 * np.pi, 300)
        r = s * (1.0 + 0.22 * np.cos(3 * t) + 0.08 * np.sin(5 * t))
        x = cx + r * np.cos(t)
        y = cy + r * np.sin(t)
        ax.fill(x, y, facecolor=color, edgecolor=BROWN, lw=2.0, alpha=0.85, zorder=2)
        ax.text(cx, cy - s - 0.55, label, ha="center", fontsize=12, fontfamily=DISPLAY, color=INK)
        ax.text(cx, cy - s - 0.95, sub, ha="center", fontsize=9.5, fontfamily=BODY, color=BROWN)

    blob(2.7, 5.6, 1.05, "#E8D4B8", "small amplitude", "same shape")
    blob(7.2, 5.6, 1.85, "#DDBFA0", "large amplitude", "same shape")

    ax.annotate(
        "",
        xy=(5.1, 5.6),
        xytext=(4.1, 5.6),
        arrowprops=dict(arrowstyle="<->", color=RED, lw=2.0),
    )
    ax.text(4.6, 6.15, "size changes", ha="center", color=RED, fontsize=11, fontfamily=BODY)

    rounded_label(
        ax,
        (1.2, 2.35),
        7.6,
        1.35,
        "R★ is amplitude-invariant and dilation-invariant.\nScale the field. Optimize size. Viscosity cancels.\nWhat’s left is pure geometry on the shape.",
        ec=BROWN,
        fc=WHITE,
        fontsize=11,
        tw=1.5,
    )
    ax.text(
        5.0,
        1.55,
        "Packaging right ≠ prize won.",
        ha="center",
        fontsize=12,
        fontfamily=DISPLAY,
        style="italic",
        color=BROWN,
    )
    footer(ax)
    save(fig, "02-shape-ne-size.png")


# ---------------------------------------------------------------------------
# 3. Tug-of-war — stretch vs spread
# ---------------------------------------------------------------------------
def fig_tug_of_war():
    fig, ax = plt.subplots(figsize=(11.2, 9.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    title_block(
        ax,
        "Tug-of-war: stretch vs spread",
        "Stretching pulls toward blowup. Spectral spread pulls toward safety. R★ is the score.",
    )

    # Rope
    ax.plot([1.4, 8.6], [5.5, 5.5], color=BROWN, lw=6, solid_capstyle="round", zorder=2)
    ax.plot([1.4, 8.6], [5.5, 5.5], color=CREAM_DARK, lw=2.2, solid_capstyle="round", zorder=3)

    # Left team — stretch (red)
    ax.add_patch(Circle((1.55, 5.5), 0.55, facecolor=RED, edgecolor=INK, lw=1.5, zorder=4))
    ax.text(1.55, 5.5, "Tc", ha="center", va="center", color=WHITE, fontsize=12, fontfamily=DISPLAY, fontweight="bold", zorder=5)
    ax.text(1.55, 6.45, "STRETCH", ha="center", color=RED, fontsize=13, fontfamily=DISPLAY, fontweight="bold")
    ax.text(1.55, 4.45, "wants blowup", ha="center", color=RED, fontsize=10, fontfamily=BODY)

    # Right team — spread (brown)
    ax.add_patch(Circle((8.45, 5.5), 0.55, facecolor=BROWN, edgecolor=INK, lw=1.5, zorder=4))
    ax.text(8.45, 5.5, "Ds", ha="center", va="center", color=WHITE, fontsize=12, fontfamily=DISPLAY, fontweight="bold", zorder=5)
    ax.text(8.45, 6.45, "SPREAD", ha="center", color=BROWN, fontsize=13, fontfamily=DISPLAY, fontweight="bold")
    ax.text(8.45, 4.45, "spectral variance", ha="center", color=BROWN, fontsize=10, fontfamily=BODY)

    # Center knot / R★
    ax.add_patch(Circle((5.0, 5.5), 0.72, facecolor=INK, edgecolor=INK, lw=1.5, zorder=5))
    ax.text(5.0, 5.58, "R★", ha="center", va="center", color=WHITE, fontsize=16, fontfamily=DISPLAY, fontweight="bold", zorder=6)
    ax.text(5.0, 6.55, "score", ha="center", color=INK, fontsize=11, fontfamily=BODY)

    # Pull arrows
    ax.annotate("", xy=(2.4, 5.5), xytext=(3.7, 5.5), arrowprops=dict(arrowstyle="->", color=RED, lw=2.2))
    ax.annotate("", xy=(7.6, 5.5), xytext=(6.3, 5.5), arrowprops=dict(arrowstyle="->", color=BROWN, lw=2.2))

    rounded_label(
        ax,
        (1.1, 2.15),
        7.8,
        1.45,
        "Lemma★: for every smooth shape, stretch cannot beat spread\nby more than one finite geometric constant C_geom.\nIf that constant exists for ALL shapes — this packaging closes Clay B.\nIt is not proved. Kill lane is still LIVE.",
        ec=BROWN,
        fc=WHITE,
        fontsize=10.5,
        tw=1.5,
    )
    footer(ax)
    save(fig, "03-tug-of-war-stretch-vs-spread.png")


# ---------------------------------------------------------------------------
# 4. R★ scoreboard
# ---------------------------------------------------------------------------
def fig_rstar_scoreboard():
    fig, ax = plt.subplots(figsize=(11.2, 9.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    title_block(
        ax,
        "R★ scoreboard — neighborhood probes",
        "Orbits around the barycenter. Not the barycenter itself.",
    )

    rows = [
        ("9A", "AP packet fan", "did not kill ★", "Ds grew faster than stretch"),
        ("9B", "near-shell K", "K ≈ 0.641 at (4,8)", "restricted family ≠ full ★"),
        ("9C", "fixed-gap spheres", "R★ 0.11 → 0.031", "falling — not a kill"),
        ("9D", "Θ(m²) falsifier", "stub / LIVE", "kill lane still open"),
    ]

    # Header strip
    ax.add_patch(
        FancyBboxPatch(
            (0.7, 7.55),
            8.6,
            0.55,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            facecolor=CREAM_DARK,
            edgecolor=BROWN,
            lw=1.3,
        )
    )
    ax.text(1.35, 7.82, "ATK", fontsize=10, fontfamily=BODY, fontweight="bold", color=BROWN)
    ax.text(2.6, 7.82, "PROBE", fontsize=10, fontfamily=BODY, fontweight="bold", color=BROWN)
    ax.text(5.3, 7.82, "RESULT", fontsize=10, fontfamily=BODY, fontweight="bold", color=BROWN)
    ax.text(7.55, 7.82, "READ", fontsize=10, fontfamily=BODY, fontweight="bold", color=BROWN)

    y = 6.7
    for code, probe, result, read in rows:
        ax.add_patch(
            FancyBboxPatch(
                (0.7, y - 0.35),
                8.6,
                0.85,
                boxstyle="round,pad=0.01,rounding_size=0.02",
                facecolor=WHITE,
                edgecolor=RED if code == "9D" else BROWN,
                lw=1.5 if code == "9D" else 1.2,
            )
        )
        ax.add_patch(Circle((1.35, y + 0.08), 0.28, facecolor=RED, edgecolor=INK, lw=1.0, zorder=3))
        ax.text(1.35, y + 0.08, code, ha="center", va="center", color=WHITE, fontsize=9, fontfamily=BODY, fontweight="bold", zorder=4)
        ax.text(2.6, y + 0.08, probe, fontsize=11, fontfamily=BODY, color=INK, va="center")
        ax.text(5.3, y + 0.08, result, fontsize=10.5, fontfamily=BODY, color=RED, va="center")
        ax.text(7.55, y + 0.08, read, fontsize=9.5, fontfamily=BODY, color=BROWN, va="center")
        y -= 1.05

    rounded_label(
        ax,
        (0.9, 1.35),
        8.2,
        0.95,
        "A finite list of small R★ fields is not a supremum.\nFailure to find a counterexample is not a proof.",
        ec=BROWN,
        fc=WHITE,
        fontsize=11,
        tw=1.4,
    )
    footer(ax)
    save(fig, "04-rstar-scoreboard.png")


# ---------------------------------------------------------------------------
# 5. Claim vs not
# ---------------------------------------------------------------------------
def fig_claim_vs_not():
    fig, ax = plt.subplots(figsize=(11.2, 9.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    title_block(
        ax,
        "What we claim · what we do not",
        "Warm and honest. Recognition for the map — not for a prize that was not won.",
    )

    # Left: claim
    ax.add_patch(
        FancyBboxPatch(
            (0.55, 2.35),
            4.25,
            5.35,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            facecolor=WHITE,
            edgecolor=BROWN,
            lw=2.0,
        )
    )
    ax.text(2.67, 7.3, "WE CLAIM", ha="center", fontsize=14, fontfamily=DISPLAY, fontweight="bold", color=BROWN)
    claims = [
        "Found the right center (shape / R★)",
        "K=0 absorption fantasy is dead",
        "R★ is amp- & dilation-invariant",
        "Five-lane + DA refuse greening",
        "Neighborhood probes 9A–9D mapped",
        "Kill criteria written in advance",
    ]
    for i, c in enumerate(claims):
        ax.text(0.85, 6.55 - 0.65 * i, f"•  {c}", fontsize=10.5, fontfamily=BODY, color=INK, va="center")

    # Right: do not
    ax.add_patch(
        FancyBboxPatch(
            (5.2, 2.35),
            4.25,
            5.35,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            facecolor="#F8E8E4",
            edgecolor=RED,
            lw=2.0,
        )
    )
    ax.text(7.32, 7.3, "WE DO NOT CLAIM", ha="center", fontsize=14, fontfamily=DISPLAY, fontweight="bold", color=RED)
    nonclaims = [
        "Lemma★ proved",
        "Navier–Stokes / Clay B solved",
        "Millennium prize",
        "Kill lane closed",
        "Uniform R★ / HH→L closed",
        "Numeric survival = proof",
    ]
    for i, c in enumerate(nonclaims):
        ax.text(5.5, 6.55 - 0.65 * i, f"•  {c}", fontsize=10.5, fontfamily=BODY, color=RED, va="center")

    ax.text(
        5.0,
        1.55,
        "We mapped to the center; door still locked.",
        ha="center",
        fontsize=13,
        fontfamily=DISPLAY,
        style="italic",
        color=INK,
    )
    footer(ax)
    save(fig, "05-claim-vs-not.png")


# ---------------------------------------------------------------------------
# 6. Viscosity melts (orbit wrapper)
# ---------------------------------------------------------------------------
def fig_viscosity_melts():
    fig, ax = plt.subplots(figsize=(11.2, 9.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    title_block(
        ax,
        "Viscosity melts — outer wrapper only",
        "The energy-budget form is derived. The real claim is pure shape at the center.",
    )

    cx, cy = 5.0, 5.15
    # Outer viscosity ring
    ax.add_patch(Circle((cx, cy), 3.15, facecolor="#EFE3CF", edgecolor=BROWN_SOFT, lw=2.0, zorder=1))
    ax.add_patch(Circle((cx, cy), 2.35, facecolor=CREAM, edgecolor=BROWN, lw=1.6, zorder=2))
    ax.add_patch(Circle((cx, cy), 1.45, facecolor=NEAR, edgecolor=BROWN, lw=1.4, zorder=3))
    ax.add_patch(Circle((cx, cy), 0.72, facecolor=INK, edgecolor=INK, lw=1.0, zorder=4))
    ax.text(cx, cy + 0.05, "★", ha="center", va="center", color=WHITE, fontsize=22, zorder=5)
    ax.text(cx, cy - 0.95, "shape / R★", ha="center", color=INK, fontsize=11, fontfamily=DISPLAY, zorder=5)

    ax.text(cx, 8.05, "outer: viscosity form", ha="center", color=BROWN, fontsize=11, fontfamily=BODY)
    ax.text(cx + 2.85, 6.4, "shell\nattacks", ha="left", color=BROWN, fontsize=10, fontfamily=BODY)
    ax.text(cx, 3.95, "near R★", ha="center", color=INK, fontsize=10, fontfamily=BODY)

    # Melt annotation
    ax.annotate(
        "viscosity melts here\n(Young in ν — derived)",
        xy=(cx + 2.6, cy + 1.2),
        xytext=(7.85, 7.35),
        fontsize=10,
        color=BROWN,
        fontfamily=BODY,
        ha="center",
        arrowprops=dict(arrowstyle="->", color=BROWN, lw=1.4),
    )
    ax.annotate(
        "barycenter =\nfinite C_geom\nfor ALL shapes",
        xy=(cx, cy - 0.2),
        xytext=(1.35, 3.0),
        fontsize=10,
        color=RED,
        fontfamily=BODY,
        ha="center",
        arrowprops=dict(arrowstyle="->", color=RED, lw=1.5),
    )

    rounded_label(
        ax,
        (1.0, 1.25),
        8.0,
        0.85,
        "Do not confuse the outer tea (viscosity packaging) with the star at the center.\nMelting edges is not the same as proving the bound.",
        ec=BROWN,
        fc=WHITE,
        fontsize=10.5,
        tw=1.4,
    )
    footer(ax)
    save(fig, "06-viscosity-melts-wrapper.png")


# ---------------------------------------------------------------------------
# 7. 18-month report card card (NS + RH)
# ---------------------------------------------------------------------------
def fig_report_card():
    fig, ax = plt.subplots(figsize=(11.2, 9.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    title_block(
        ax,
        "18-month report card — NS & RH",
        "From a CRNA in Savannah with a phone. Proud of the map. Honest about the door.",
    )

    # NS card
    ax.add_patch(
        FancyBboxPatch(
            (0.5, 2.5),
            4.35,
            5.15,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            facecolor=WHITE,
            edgecolor=BROWN,
            lw=2.0,
        )
    )
    ax.text(2.67, 7.25, "NS / Clay B", ha="center", fontsize=15, fontfamily=DISPLAY, fontweight="bold", color=INK)
    ax.text(2.67, 6.8, "Navier–Stokes regularity", ha="center", fontsize=10, fontfamily=BODY, color=BROWN)
    ns_lines = [
        ("Packaging", "R★ shape — mapped"),
        ("K=0 lane", "DEAD"),
        ("9A–9D probes", "mapped"),
        ("HH→L gap", "OPEN"),
        ("Lemma★", "NOT proved"),
        ("Clay B", "NOT solved"),
        ("Kill lane", "LIVE"),
    ]
    for i, (k, v) in enumerate(ns_lines):
        y = 6.25 - 0.48 * i
        ax.text(0.85, y, k, fontsize=10, fontfamily=BODY, color=BROWN)
        color = RED if v in ("NOT proved", "NOT solved", "LIVE", "OPEN", "DEAD") else INK
        ax.text(4.5, y, v, fontsize=10, fontfamily=BODY, color=color, ha="right", fontweight="bold")

    # RH card
    ax.add_patch(
        FancyBboxPatch(
            (5.15, 2.5),
            4.35,
            5.15,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            facecolor=WHITE,
            edgecolor=BROWN,
            lw=2.0,
        )
    )
    ax.text(7.32, 7.25, "RH", ha="center", fontsize=15, fontfamily=DISPLAY, fontweight="bold", color=INK)
    ax.text(7.32, 6.8, "Riemann Hypothesis", ha="center", fontsize=10, fontfamily=BODY, color=BROWN)
    rh_lines = [
        ("Navigation", "shape/texture map built"),
        ("Q6 / Route C", "exploratory — open weld"),
        ("Cross-glue to NS", "REFUSED (incompatible)"),
        ("Operator program", "parked / not closed"),
        ("RH", "NOT proved"),
        ("Clay prize", "NOT claimed"),
        ("Honesty rule", "no fake splices"),
    ]
    for i, (k, v) in enumerate(rh_lines):
        y = 6.25 - 0.48 * i
        ax.text(5.5, y, k, fontsize=10, fontfamily=BODY, color=BROWN)
        color = RED if ("NOT" in v or v.startswith("REFUSED") or "open" in v.lower()) else INK
        ax.text(9.2, y, v, fontsize=9.5, fontfamily=BODY, color=color, ha="right", fontweight="bold")

    ax.text(
        5.0,
        1.7,
        "Grade for effort & packaging: A · Grade for Millennium closure: incomplete — doors still locked.",
        ha="center",
        fontsize=10.5,
        fontfamily=BODY,
        color=INK,
    )
    footer(ax, text="Outcome: ★ NOT proved · NS NOT solved · RH NOT proved · kill lane LIVE")
    save(fig, "07-eighteen-month-report-card.png")


# ---------------------------------------------------------------------------
# 8. Phone / CRNA opener card
# ---------------------------------------------------------------------------
def fig_crna_opener():
    fig, ax = plt.subplots(figsize=(11.2, 9.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    title_block(
        ax,
        "From a CRNA in Savannah",
        "Could a normal person with a phone take on something really hard?",
    )

    # Phone silhouette
    ax.add_patch(
        FancyBboxPatch(
            (3.55, 2.9),
            2.9,
            4.6,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor=INK,
            edgecolor=INK,
            lw=2,
            zorder=2,
        )
    )
    ax.add_patch(
        FancyBboxPatch(
            (3.75, 3.35),
            2.5,
            3.7,
            boxstyle="round,pad=0.01,rounding_size=0.04",
            facecolor=CREAM,
            edgecolor=CREAM_DARK,
            lw=1,
            zorder=3,
        )
    )
    ax.add_patch(Circle((5.0, 3.15), 0.14, facecolor=CREAM_DARK, zorder=4))
    ax.text(5.0, 6.55, "Lemma★", ha="center", fontsize=14, fontfamily=DISPLAY, fontweight="bold", color=INK, zorder=4)
    ax.text(5.0, 5.95, "map the center", ha="center", fontsize=10, fontfamily=BODY, color=BROWN, zorder=4)
    ax.text(5.0, 5.35, "door still", ha="center", fontsize=10, fontfamily=BODY, color=RED, zorder=4)
    ax.text(5.0, 4.95, "locked", ha="center", fontsize=10, fontfamily=BODY, color=RED, zorder=4)
    ax.add_patch(Circle((5.0, 4.25), 0.35, facecolor=INK, zorder=4))
    ax.text(5.0, 4.25, "★", ha="center", va="center", color=WHITE, fontsize=14, zorder=5)

    rounded_label(
        ax,
        (0.7, 1.25),
        8.6,
        1.15,
        "Jonathan R. Simons, CRNA · Savannah, GA\nMotivation: see whether discipline + honesty + a phone-sized workflow\ncould map a Millennium door. Recognition wanted for the map — not a fake win.\nNot a jerk about labs or models. Not a bad teacher — wife-friendly pictures first.",
        ec=BROWN,
        fc=WHITE,
        fontsize=10,
        tw=1.4,
    )
    footer(ax)
    save(fig, "08-crna-savannah-phone.png")


def main():
    fig_tea_cup()
    fig_shape_ne_size()
    fig_tug_of_war()
    fig_rstar_scoreboard()
    fig_claim_vs_not()
    fig_viscosity_melts()
    fig_report_card()
    fig_crna_opener()
    print("done")


if __name__ == "__main__":
    main()
