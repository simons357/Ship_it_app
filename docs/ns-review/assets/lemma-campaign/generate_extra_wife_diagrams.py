#!/usr/bin/env python3
"""Extra wife-test diagrams: five-lane map, door card, products, postcard.

Re-run:
  python3 docs/ns-review/assets/lemma-campaign/generate_extra_wife_diagrams.py
"""
from __future__ import annotations

from pathlib import Path
import shutil

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import numpy as np

OUT = Path(__file__).resolve().parent
ART = Path("/opt/cursor/artifacts/lemma-star-paper")
ART.mkdir(parents=True, exist_ok=True)

CREAM = "#F4EBD8"
INK = "#1A1208"
BROWN = "#6B4E2E"
BROWN_SOFT = "#A08060"
RED = "#8B1E1E"
WHITE = "#FFFDF8"
FOOTER_BG = "#D9C9A8"
TEAL = "#2F5D62"
GOLD = "#B08A3E"
BLUE = "#3A5A7A"
GREEN = "#4A6B4A"
ORANGE = "#A85A2A"
BODY = "DejaVu Sans"
STAR = "★"
OUTCOME = f"Outcome: {STAR} NOT proved · NS NOT solved · kill lane LIVE · uniform R{STAR} / HH→L still open"

plt.rcParams.update(
    {
        "font.family": BODY,
        "figure.facecolor": CREAM,
        "axes.facecolor": CREAM,
        "savefig.facecolor": CREAM,
        "savefig.dpi": 160,
    }
)


def save(fig, name: str) -> None:
    fig.savefig(OUT / name, dpi=160, facecolor=CREAM, edgecolor="none", bbox_inches="tight")
    fig.savefig(ART / name, dpi=160, facecolor=CREAM, edgecolor="none", bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def footer_bar(ax, x, y, w, h, text=OUTCOME):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            facecolor=FOOTER_BG,
            edgecolor=BROWN,
            lw=1.2,
            zorder=5,
        )
    )
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9.5, color=INK, zorder=6)


def fig_five_lane():
    fig, ax = plt.subplots(figsize=(12.8, 9.0))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.text(6.5, 9.55, "Five lanes · Attacks 9A–9D · one locked door", ha="center", fontsize=18, fontweight="bold", color=INK)
    ax.text(
        6.5,
        9.05,
        "Many routes around the center. The door still needs the key — R★ for every shape.",
        ha="center",
        fontsize=11,
        style="italic",
        color=BROWN,
    )

    ax.add_patch(Circle((5.2, 5.0), 0.95, facecolor=INK, edgecolor=INK, zorder=6))
    ax.text(5.2, 5.15, STAR, ha="center", va="center", color=WHITE, fontsize=26, zorder=7)
    ax.text(5.2, 4.5, "barycenter", ha="center", color=WHITE, fontsize=9, zorder=7)
    ax.text(5.2, 3.7, "door locked", ha="center", color=RED, fontsize=12, fontweight="bold")

    lanes = [
        (5.2, 7.85, TEAL, "Lane 1 · kill search", "Can we break ★\nwith a bad shape?"),
        (8.55, 6.55, GOLD, "Lane 2 · K=0", "Stretch ≤ spread alone?\nDEAD"),
        (8.7, 3.35, ORANGE, "Lane 3 · HH→L", "Product gap\nstill OPEN"),
        (5.2, 2.0, BLUE, "Lane 4 · packaging", "Shape form of ★\nmapped"),
        (1.85, 3.35, GREEN, "Lane 5 · DA locks", "Refuse greening\nstatus honest"),
    ]
    for x, y, color, title, sub in lanes:
        ax.plot([x, 5.2], [y, 5.0], color=color, lw=5.5, solid_capstyle="round", zorder=2, alpha=0.88)
        ax.add_patch(Circle((x, y), 0.18, facecolor=color, edgecolor=INK, lw=1.0, zorder=5))
        if y > 6.5:
            box_y = y + 0.15
        elif y < 3.0:
            box_y = y - 1.05
        else:
            box_y = y - 0.35
        ax.add_patch(
            FancyBboxPatch(
                (x - 1.4, box_y),
                2.8,
                0.95,
                boxstyle="round,pad=0.01,rounding_size=0.02",
                facecolor=WHITE,
                edgecolor=color,
                lw=1.6,
                zorder=5,
            )
        )
        ax.text(x, box_y + 0.62, title, ha="center", va="center", fontsize=10, fontweight="bold", color=color, zorder=6)
        ax.text(x, box_y + 0.28, sub, ha="center", va="center", fontsize=9, color=INK, zorder=6)

    theta = np.linspace(0, 2 * np.pi, 300)
    ax.plot(5.2 + 2.15 * np.cos(theta), 5.0 + 1.85 * np.sin(theta), color=BROWN_SOFT, lw=1.5, ls="--", zorder=3)
    for ang, code in [(0.35, "9A"), (1.55, "9B"), (3.2, "9C"), (4.85, "9D")]:
        x = 5.2 + 2.15 * np.cos(ang)
        y = 5.0 + 1.85 * np.sin(ang)
        ax.add_patch(Circle((x, y), 0.26, facecolor=RED, edgecolor=INK, lw=1.0, zorder=6))
        ax.text(x, y, code, ha="center", va="center", color=WHITE, fontsize=8.5, fontweight="bold", zorder=7)

    ax.add_patch(
        FancyBboxPatch(
            (10.0, 2.0),
            2.7,
            5.5,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            facecolor=WHITE,
            edgecolor=BROWN,
            lw=1.6,
            zorder=4,
        )
    )
    ax.text(11.35, 7.1, "Neighborhood\nprobes", ha="center", fontsize=11, fontweight="bold", color=INK, zorder=5)
    rows = [
        ("9A", "packet fan — did not kill ★"),
        ("9B", "near-shell — ≠ full ★"),
        ("9C", "fixed-gap — R★ fell"),
        ("9D", "falsifier — LIVE"),
    ]
    for i, (code, note) in enumerate(rows):
        y = 6.3 - 0.95 * i
        ax.add_patch(Circle((10.45, y), 0.22, facecolor=RED, edgecolor=INK, lw=1.0, zorder=5))
        ax.text(10.45, y, code, ha="center", va="center", color=WHITE, fontsize=8, fontweight="bold", zorder=6)
        ax.text(10.85, y, note, ha="left", va="center", fontsize=9, color=BROWN, zorder=5)

    ax.text(
        5.2,
        0.85,
        "Probes circle the door. Five lanes keep the work honest. Key still missing.",
        ha="center",
        fontsize=11,
        color=INK,
    )
    footer_bar(ax, 0.7, 0.18, 11.6, 0.45)
    save(fig, "09-five-lane-subway-map.png")


def fig_door_card():
    fig, ax = plt.subplots(figsize=(11.2, 9.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.text(5.0, 9.45, "Door locked · the key is R★", ha="center", fontsize=18, fontweight="bold", color=INK)
    ax.text(
        5.0,
        8.95,
        "We found the door. We named the key. We do not pretend we turned it.",
        ha="center",
        fontsize=11,
        style="italic",
        color=BROWN,
    )
    ax.add_patch(
        FancyBboxPatch((3.2, 2.6), 3.6, 5.2, boxstyle="round,pad=0.01,rounding_size=0.02", facecolor="#5A3A22", edgecolor=INK, lw=2.2, zorder=2)
    )
    for yy in (3.4, 4.6, 5.8, 7.0):
        ax.plot([3.35, 6.65], [yy, yy], color="#3A2414", lw=1.2, alpha=0.5, zorder=3)
    ax.add_patch(
        FancyBboxPatch((4.55, 4.55), 0.9, 1.15, boxstyle="round,pad=0.01,rounding_size=0.04", facecolor="#2A2A2A", edgecolor=INK, lw=1.5, zorder=4)
    )
    ax.add_patch(Circle((5.0, 5.35), 0.18, facecolor=CREAM, edgecolor=INK, lw=1.2, zorder=5))
    ax.add_patch(Rectangle((4.92, 4.7), 0.16, 0.35, facecolor=CREAM, edgecolor=INK, lw=1.0, zorder=5))
    ax.text(5.0, 7.55, "LOCKED", ha="center", color=CREAM, fontsize=14, fontweight="bold", zorder=5)
    ax.add_patch(
        FancyBboxPatch((1.1, 1.55), 2.6, 0.85, boxstyle="round,pad=0.01,rounding_size=0.05", facecolor=GOLD, edgecolor=INK, lw=1.4, zorder=4)
    )
    ax.add_patch(Circle((1.45, 1.97), 0.28, facecolor=CREAM, edgecolor=INK, lw=1.2, zorder=5))
    ax.text(2.5, 1.97, f"key = R{STAR}", ha="center", va="center", fontsize=12, fontweight="bold", color=INK, zorder=5)
    ax.add_patch(
        FancyBboxPatch((6.3, 1.55), 2.6, 0.85, boxstyle="round,pad=0.01,rounding_size=0.05", facecolor=WHITE, edgecolor=RED, lw=1.6, zorder=4)
    )
    ax.text(7.6, 1.97, "not turned yet", ha="center", va="center", fontsize=12, color=RED, fontweight="bold", zorder=5)
    ax.text(
        5.0,
        8.35,
        "If R★ stays bounded for every smooth shape,\nthis packaging would open Clay B.",
        ha="center",
        fontsize=11,
        color=BROWN,
    )
    ax.text(5.0, 1.05, "Recognition for finding the door. Honesty about the lock.", ha="center", fontsize=12, style="italic", color=INK)
    footer_bar(ax, 0.7, 0.25, 8.6, 0.5)
    save(fig, "10-door-locked-key-rstar.png")


def fig_products():
    fig, ax = plt.subplots(figsize=(12.2, 8.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.text(6.0, 9.45, "Discoveries → products he is developing", ha="center", fontsize=18, fontweight="bold", color=INK)
    ax.text(
        6.0,
        8.95,
        "Light touch. The math feeds the products. The products do not green the math.",
        ha="center",
        fontsize=11,
        style="italic",
        color=BROWN,
    )
    ax.add_patch(FancyBboxPatch((3.7, 7.0), 4.6, 1.35, boxstyle="round,pad=0.02,rounding_size=0.04", facecolor=INK, edgecolor=INK, lw=1.5, zorder=3))
    ax.text(6.0, 7.85, "Discoveries & maps", ha="center", color=WHITE, fontsize=14, fontweight="bold", zorder=4)
    ax.text(6.0, 7.35, f"Lemma{STAR} · shape scores · five-lane discipline · DA locks", ha="center", color=CREAM, fontsize=10, zorder=4)
    products = [
        (1.6, 3.6, "Ship_it", "Shipping discipline\nfrom kill-or-prove\nclarity", TEAL),
        (6.0, 3.6, "Domain\nArchitect", "Books, welds,\nstatus locks —\nrefuse greening", GOLD),
        (10.4, 3.6, "Harmonic\nBlueprint", "Shape / texture\nnavigation ideas\n(light)", BLUE),
    ]
    for x, y, name, blurb, color in products:
        ax.annotate("", xy=(x, y + 1.55), xytext=(6.0, 7.0), arrowprops=dict(arrowstyle="->", color=BROWN_SOFT, lw=2.0))
        ax.add_patch(
            FancyBboxPatch((x - 1.55, y - 1.1), 3.1, 2.6, boxstyle="round,pad=0.02,rounding_size=0.04", facecolor=WHITE, edgecolor=color, lw=2.0, zorder=3)
        )
        ax.text(x, y + 1.05, name, ha="center", va="center", fontsize=14, fontweight="bold", color=color, zorder=4)
        ax.text(x, y - 0.15, blurb, ha="center", va="center", fontsize=10.5, color=INK, zorder=4)
    ax.add_patch(FancyBboxPatch((1.2, 1.15), 9.6, 0.85, boxstyle="round,pad=0.01,rounding_size=0.02", facecolor=WHITE, edgecolor=BROWN, lw=1.4, zorder=3))
    ax.text(6.0, 1.55, "Dignity first — not a pitch deck. ★ not proved · NS not solved · kill lane LIVE.", ha="center", va="center", fontsize=11, color=INK, zorder=4)
    footer_bar(ax, 0.9, 0.25, 10.2, 0.5)
    save(fig, "11-discoveries-to-products.png")


def fig_postcard():
    fig, ax = plt.subplots(figsize=(11.5, 8.0))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.35, 0.55), 10.3, 7.0, boxstyle="round,pad=0.01,rounding_size=0.02", facecolor=WHITE, edgecolor=BROWN, lw=2.4, zorder=1))
    ax.add_patch(FancyBboxPatch((0.55, 0.75), 10.0, 6.6, boxstyle="round,pad=0.01,rounding_size=0.015", facecolor=CREAM, edgecolor=BROWN_SOFT, lw=1.2, zorder=2))
    ax.text(5.55, 6.85, "POSTCARD FROM SAVANNAH", ha="center", fontsize=16, fontweight="bold", color=INK, zorder=3)
    ax.text(5.55, 6.4, "18-month report card · NS & RH · from a CRNA with a phone", ha="center", fontsize=11, style="italic", color=BROWN, zorder=3)
    ax.add_patch(FancyBboxPatch((9.15, 5.55), 1.15, 1.35, boxstyle="round,pad=0.01,rounding_size=0.02", facecolor="#E8DCC4", edgecolor=RED, lw=1.6, zorder=3))
    ax.text(9.72, 6.35, STAR, ha="center", fontsize=18, color=RED, zorder=4)
    ax.text(9.72, 5.85, "LIVE", ha="center", fontsize=9, color=RED, fontweight="bold", zorder=4)
    ax.add_patch(FancyBboxPatch((0.9, 1.6), 4.4, 4.3, boxstyle="round,pad=0.02,rounding_size=0.03", facecolor=WHITE, edgecolor=BROWN, lw=1.6, zorder=3))
    ax.text(3.1, 5.55, "NS / Clay B", ha="center", fontsize=14, fontweight="bold", color=INK, zorder=4)
    ns = [
        ("Effort & packaging", "A"),
        ("Door mapped?", "YES"),
        ("Door opened?", "NO"),
        ("Lemma★ proved?", "NO"),
        ("Kill lane", "LIVE"),
        ("Millennium closure", "incomplete"),
    ]
    for i, (k, v) in enumerate(ns):
        y = 4.95 - 0.48 * i
        ax.text(1.15, y, k, fontsize=11, color=BROWN, zorder=4)
        ax.text(5.05, y, v, fontsize=11, color=RED if v in ("NO", "LIVE", "incomplete") else INK, ha="right", fontweight="bold", zorder=4)
    ax.add_patch(FancyBboxPatch((5.6, 1.6), 4.4, 4.3, boxstyle="round,pad=0.02,rounding_size=0.03", facecolor=WHITE, edgecolor=BROWN, lw=1.6, zorder=3))
    ax.text(7.8, 5.55, "RH", ha="center", fontsize=14, fontweight="bold", color=INK, zorder=4)
    rh = [
        ("Effort & packaging", "A"),
        ("Navigation built?", "YES"),
        ("RH proved?", "NO"),
        ("Fake glue to NS?", "REFUSED"),
        ("Clay prize", "not claimed"),
        ("Millennium closure", "incomplete"),
    ]
    for i, (k, v) in enumerate(rh):
        y = 4.95 - 0.48 * i
        ax.text(5.85, y, k, fontsize=11, color=BROWN, zorder=4)
        ax.text(9.75, y, v, fontsize=11, color=RED if v in ("NO", "REFUSED", "incomplete", "not claimed") else INK, ha="right", fontweight="bold", zorder=4)
    ax.text(5.55, 1.15, "Proud of the map. Honest about the locked doors. Love, Jonathan", ha="center", fontsize=12, style="italic", color=INK, zorder=4)
    footer_bar(ax, 0.7, 0.15, 9.6, 0.4, text="Outcome: ★ NOT proved · NS NOT solved · RH NOT proved · kill lane LIVE")
    save(fig, "07b-postcard-report-card.png")


def ensure_photo_door():
    src = Path("/opt/cursor/artifacts/assets/09-door-locked-key-rstar.png")
    if src.exists():
        shutil.copy(src, OUT / "10b-door-locked-photo.png")
        shutil.copy(src, ART / "10b-door-locked-photo.png")
        print("copied 10b-door-locked-photo.png")


def main():
    fig_five_lane()
    fig_door_card()
    fig_products()
    fig_postcard()
    ensure_photo_door()
    print("done")


if __name__ == "__main__":
    main()
