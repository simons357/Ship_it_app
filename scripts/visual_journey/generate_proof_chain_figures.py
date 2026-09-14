#!/usr/bin/env python3
"""Generate proof-chain Mermaid mirror figures (SVG/PNG) and chain-status card.

Public face: node colors = chain status. Open nodes labeled 'open estimate'.
No solved / not-solved stamps.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "docs" / "ns-review" / "visual-journey" / "figures"
ART_DIR = Path("/opt/cursor/artifacts/ns-proof-chain-visual")
JOURNEY_ART_DIR = Path("/opt/cursor/artifacts/ns-proof-journey")
CAMPAIGN_ASSETS = ROOT / "docs" / "ns-review" / "assets" / "lemma-campaign"
JOURNEY_ASSETS = ROOT / "docs" / "ns-review" / "visual-journey" / "assets"
CAMPAIGN_DIR = ROOT / "docs" / "campaign"

# Quiet craftsman palette — no purple glow cluster
C_CLASSICAL = "#dce6ef"
C_IDENTITY = "#d4e4d8"
C_PACKAGE = "#e8e0d0"
C_OPEN = "#f5e6c8"
C_OPTIONAL = "#eeeae2"
C_EDGE = "#3d5a73"
C_TEXT = "#1a2332"
C_BG = "#f7f4ef"


def _box(ax, xy, w, h, text, facecolor, *, dashed=False, fontsize=9):
    x, y = xy
    style = "dashed" if dashed else "solid"
    patch = FancyBboxPatch(
        (x - w / 2, y - h / 2),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=facecolor,
        edgecolor=C_EDGE,
        linewidth=1.4,
        linestyle=style,
    )
    ax.add_patch(patch)
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=C_TEXT,
        linespacing=1.25,
        family="DejaVu Sans",
    )
    return (x, y)


def _arrow(ax, a, b):
    ax.add_patch(
        FancyArrowPatch(
            a,
            b,
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=1.2,
            color="#5a6b7d",
            shrinkA=18,
            shrinkB=18,
        )
    )


def render_proof_chain(out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12.0, 9.0), dpi=160)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 10)
    ax.axis("off")

    ax.text(
        6.0,
        9.55,
        "Proof chain — Navier–Stokes packaging",
        ha="center",
        va="center",
        fontsize=15,
        color=C_TEXT,
        family="DejaVu Sans",
    )
    ax.text(
        6.0,
        9.15,
        "Node color = chain status · dashed = open estimate · optional texture muted",
        ha="center",
        va="center",
        fontsize=8.5,
        color="#5a6b7d",
        family="DejaVu Sans",
    )

    # Main trunk (left-center column)
    nse = _box(ax, (4.0, 8.2), 3.2, 0.75, "Classical NSE on $\\mathbb{T}^3$\n$\\nabla\\cdot u=0$, viscosity $\\nu$", C_CLASSICAL)
    mom = _box(ax, (4.0, 7.05), 3.2, 0.75, "Moments $E,X,Y,Z$\nspectral scale $\\Lambda=Y/X$", C_CLASSICAL)
    ident = _box(
        ax,
        (4.0, 5.8),
        3.4,
        0.85,
        "Identities\n$D_s=Z-\\Lambda Y$,\\; $T_c=M-\\Lambda N$\n$\\Lambda'=2(T_c-\\nu D_s)/X$",
        C_IDENTITY,
        fontsize=8.5,
    )
    star = _box(
        ax,
        (4.0, 4.5),
        3.4,
        0.85,
        "Lemma$\\star$ packaging\nshape form $\\mathcal{R}_\\star$ / energy budget",
        C_PACKAGE,
        fontsize=8.5,
    )
    five = _box(
        ax,
        (4.0, 3.3),
        3.4,
        0.8,
        "Five-lane diagnostics\nBony / shell / packet probes",
        C_PACKAGE,
        fontsize=8.5,
    )
    prod = _box(
        ax,
        (4.0, 2.05),
        3.4,
        0.85,
        "Product bound on $T_c$\nopen estimate",
        C_OPEN,
        dashed=True,
        fontsize=9,
    )
    reg = _box(
        ax,
        (4.0, 0.8),
        3.4,
        0.8,
        "Continuation / regularity\nfrom controlled $\\Lambda$",
        C_PACKAGE,
        fontsize=8.5,
    )

    for a, b in [(nse, mom), (mom, ident), (ident, star), (star, five), (five, prod), (prod, reg)]:
        _arrow(ax, a, b)

    # Phi branch (right)
    ax.text(9.4, 8.55, "Φ-renorm branch", ha="center", fontsize=9, color="#5a6b7d")
    phi = _box(
        ax,
        (9.4, 7.6),
        3.0,
        0.85,
        "$\\Gamma\\to\\Phi$ identity\n$r^{-4}\\partial_z(\\Gamma^2)=\\partial_z(\\Phi^2)$",
        C_IDENTITY,
        fontsize=8,
    )
    hdot = _box(
        ax,
        (9.4, 6.3),
        3.0,
        0.75,
        "Dissipation label\n$\\dot H^{1.3}$ (relabeled)",
        C_IDENTITY,
        fontsize=8.5,
    )
    bar = _box(
        ax,
        (9.4, 5.0),
        3.0,
        0.85,
        "$\\|u^r/r\\|_\\infty$ integrability\nopen estimate",
        C_OPEN,
        dashed=True,
        fontsize=8.5,
    )
    _arrow(ax, phi, hdot)
    _arrow(ax, hdot, bar)

    # Optional SND
    ax.text(9.4, 3.55, "Optional texture", ha="center", fontsize=9, color="#5a6b7d")
    snd = _box(
        ax,
        (9.4, 2.7),
        3.0,
        0.85,
        "SND / Ring Lemma\nconditional shell texture",
        C_OPTIONAL,
        dashed=True,
        fontsize=8.5,
    )
    # soft dashed links from identity to SND to product
    ax.annotate(
        "",
        xy=(snd[0] - 1.5, snd[1]),
        xytext=(ident[0] + 1.7, ident[1] - 0.2),
        arrowprops=dict(arrowstyle="-|>", color="#8a8580", lw=1.0, ls="--", shrinkA=6, shrinkB=6),
    )
    ax.annotate(
        "",
        xy=(prod[0] + 1.7, prod[1] + 0.1),
        xytext=(snd[0] - 1.5, snd[1] - 0.1),
        arrowprops=dict(arrowstyle="-|>", color="#8a8580", lw=1.0, ls="--", shrinkA=6, shrinkB=6),
    )

    # Legend
    legend_y = 0.35
    for i, (label, color, dashed) in enumerate(
        [
            ("classical / definition", C_CLASSICAL, False),
            ("identity / KEEP algebra", C_IDENTITY, False),
            ("packaging", C_PACKAGE, False),
            ("open estimate", C_OPEN, True),
            ("optional texture", C_OPTIONAL, True),
        ]
    ):
        x0 = 0.45 + i * 2.35
        patch = FancyBboxPatch(
            (x0, legend_y - 0.12),
            0.35,
            0.22,
            boxstyle="round,pad=0.01,rounding_size=0.04",
            facecolor=color,
            edgecolor=C_EDGE,
            linewidth=1.0,
            linestyle="dashed" if dashed else "solid",
        )
        ax.add_patch(patch)
        ax.text(x0 + 0.45, legend_y, label, va="center", fontsize=7.5, color=C_TEXT)

    png = out_dir / "proof-chain.png"
    svg = out_dir / "proof-chain.svg"
    fig.savefig(png, bbox_inches="tight", facecolor=C_BG)
    fig.savefig(svg, bbox_inches="tight", facecolor=C_BG)
    plt.close(fig)
    return {"png": png, "svg": svg}


def render_chain_status_card(out_dir: Path) -> Path:
    """Report-card as chain status (node colors), not political grades."""
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = [
        ("Classical NSE substrate", "in place", C_CLASSICAL),
        ("Moments $E,X,Y,Z$ and $\\Lambda$", "defined", C_CLASSICAL),
        ("$D_s$, $T_c$, $\\Lambda'$ identities", "in place", C_IDENTITY),
        ("Lemma$\\star$ shape / energy-budget packaging", "stated", C_PACKAGE),
        ("Five-lane diagnostics (Bony / shell / packet)", "probes", C_PACKAGE),
        ("Product bound on $T_c$", "open estimate", C_OPEN),
        ("Continuation arrow (needs product + packaging)", "conditional edge", C_PACKAGE),
        ("$\\Phi$-renorm $\\Gamma\\to\\Phi$ identity", "in place", C_IDENTITY),
        ("$\\dot H^{1.3}$ dissipation label", "corrected", C_IDENTITY),
        ("$\\|u^r/r\\|_\\infty$ integrability", "open estimate", C_OPEN),
        ("SND / Ring conditional texture", "optional", C_OPTIONAL),
    ]

    fig, ax = plt.subplots(figsize=(9.5, 7.8), dpi=160)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")
    ax.text(
        5,
        11.3,
        "Chain status",
        ha="center",
        fontsize=16,
        color=C_TEXT,
    )
    ax.text(
        5,
        10.8,
        "Colors mark nodes in the proof chain — not grades, not verdicts",
        ha="center",
        fontsize=9,
        color="#5a6b7d",
    )

    y = 10.0
    for name, status, color in rows:
        patch = FancyBboxPatch(
            (0.6, y - 0.32),
            8.8,
            0.68,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor=color,
            edgecolor=C_EDGE,
            linewidth=1.1,
            linestyle="dashed" if "open" in status or status == "optional" else "solid",
        )
        ax.add_patch(patch)
        ax.text(0.9, y, name, va="center", fontsize=10, color=C_TEXT)
        ax.text(9.1, y, status, va="center", ha="right", fontsize=9.5, color="#3d4a55")
        y -= 0.85

    path = out_dir / "chain-status-card.png"
    fig.savefig(path, bbox_inches="tight", facecolor=C_BG)
    plt.close(fig)
    return path


def stage_journey_assets() -> list[Path]:
    """Reuse existing math figures; do not invent fake data."""
    JOURNEY_ASSETS.mkdir(parents=True, exist_ok=True)
    wanted = [
        "lemma-star-barycenter.png",
        "00-barycenter-map.png",
        "fig_star_david_ring_lemma.png",
        "fig_three_spheres.png",
        "t3_torus_shape_render.png",
        "03-tug-of-war-stretch-vs-spread.png",
        "02-shape-ne-size.png",
        "amp_ratios_triad.png",
        "06-viscosity-melts-wrapper.png",
    ]
    copied: list[Path] = []
    for name in wanted:
        src = CAMPAIGN_ASSETS / name
        if src.is_file():
            dst = JOURNEY_ASSETS / name
            shutil.copy2(src, dst)
            copied.append(dst)
    return copied


def sync_artifacts(paths: list[Path], dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for p in paths:
        if p.is_file():
            shutil.copy2(p, dest / p.name)


def stage_campaign_docs() -> list[Path]:
    """Journey landing docs for artifact walkthrough."""
    wanted = [
        "PROOF-JOURNEY.md",
        "REPUTATION-LOCK.md",
        "NOTATION-GLOSSARY.md",
        "journey-chain.mmd",
    ]
    return [CAMPAIGN_DIR / name for name in wanted if (CAMPAIGN_DIR / name).is_file()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    parser.add_argument("--no-artifacts", action="store_true")
    args = parser.parse_args(argv)

    chain = render_proof_chain(args.out)
    status = render_chain_status_card(args.out)
    assets = stage_journey_assets()
    # also copy mermaid source into figures for pack completeness
    mmd_src = ROOT / "docs" / "ns-review" / "visual-journey" / "proof-chain.mmd"
    mmd_dst = args.out / "proof-chain.mmd"
    if mmd_src.is_file():
        shutil.copy2(mmd_src, mmd_dst)

    campaign_docs = stage_campaign_docs()
    all_paths = [chain["png"], chain["svg"], status, mmd_dst, *assets, *campaign_docs]
    if not args.no_artifacts:
        existing = [p for p in all_paths if p and Path(p).exists()]
        sync_artifacts(existing, ART_DIR)
        sync_artifacts(existing, JOURNEY_ART_DIR)

    print("Wrote:")
    for p in all_paths:
        if p and Path(p).exists():
            print(f"  {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
