#!/usr/bin/env python3
"""How Ring Lemma works — mechanism card (theoretical inequality, not a force)."""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUT_DIRS = [
    Path("/opt/cursor/artifacts/nse-status-now"),
    Path("docs/ns-review/visual-journey/figures"),
]

INK = "#0f1c2e"
SLATE = "#2a3f55"
COPPER = "#b86b3c"
STEEL = "#4a6a82"
FOG = "#e8eef2"
MIST = "#f4f7f9"
GREEN = "#1f6b4a"
AMBER = "#c4892a"
MUTED = "#6b7c8a"


def save(fig: plt.Figure, name: str) -> None:
    for d in OUT_DIRS:
        d.mkdir(parents=True, exist_ok=True)
        path = d / name
        fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"wrote {path}")


def render_chain() -> None:
    fig = plt.figure(figsize=(12.8, 7.6), facecolor=MIST)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis("off")

    def box(x, y, w, h, face, edge, lw=1.8):
        ax.add_patch(
            mpatches.FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.02,rounding_size=0.12",
                facecolor=face,
                edgecolor=edge,
                linewidth=lw,
            )
        )

    ax.text(
        7,
        9.55,
        'How Ring "does" anything — a proved inequality, not a force',
        ha="center",
        color=INK,
        fontsize=13.5,
        fontweight="bold",
    )

    steps = [
        (
            0.35,
            FOG,
            STEEL,
            "1. ASSUME HARDWARE",
            "Field is band-limited\n"
            r"$|k|\leq L$ in Fourier" + "\n\n"
            "Only so many modes.\nNo infinite fine wiggles.",
        ),
        (
            3.7,
            FOG,
            STEEL,
            "2. GRADIENT CEILING",
            "Fourier + Cauchy–Schwarz\n"
            r"$\|\nabla\omega\|_\infty$" + "\n"
            r"$\lesssim L^{5/2}\|\omega\|_2$" + "\n\n"
            "Intensity cannot change\narbitrarily fast in space.",
        ),
        (
            7.05,
            "#dceee4",
            GREEN,
            "3. DIRECTION BOUND",
            r"On strong set $E_c$" + "\n"
            r"$|\omega|\geq c\|\omega\|_2$" + "\n\n"
            r"$|\nabla\xi|\leq|\nabla\omega|/|\omega|$" + "\n"
            r"$\Rightarrow\lesssim L^{5/2}/c$",
        ),
        (
            10.4,
            "#dceee4",
            GREEN,
            "4. WHAT THAT MEANS",
            "Any such snapshot that\nexists must already obey\nthe twist ceiling.\n\n"
            "It rules out wild\ndirection geometry.",
        ),
    ]
    for x, face, edge, title, body in steps:
        box(x, 6.15, 3.15, 2.7, face, edge, lw=1.9)
        ax.text(x + 1.575, 8.5, title, ha="center", va="top", color=INK, fontsize=10, fontweight="bold")
        ax.text(x + 1.575, 7.2, body, ha="center", va="center", color=SLATE, fontsize=8.7, linespacing=1.3)

    for x0, x1 in [(3.5, 3.7), (6.85, 7.05), (10.2, 10.4)]:
        ax.annotate(
            "",
            xy=(x1, 7.5),
            xytext=(x0, 7.5),
            arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.8),
        )

    box(0.35, 0.85, 6.4, 4.7, "#e7f2ea", GREEN, lw=2.2)
    ax.text(3.55, 5.15, "WHAT IT AFFECTS (in a proof)", ha="center", color=GREEN, fontsize=11, fontweight="bold")
    ax.text(
        3.55,
        2.85,
        "• Which spatial configurations are allowed\n"
        "  for band-limited vorticity\n\n"
        "• You may invoke it when a field is\n"
        "  (approximately) shell-supported\n\n"
        "• Optional texture for SND / alignment\n"
        "  language on the side of the map\n\n"
        "• It is a lemma: a tool you can cite\n"
        "  if your hypotheses match",
        ha="center",
        va="center",
        color=SLATE,
        fontsize=9.3,
        linespacing=1.35,
    )

    box(7.15, 0.85, 6.45, 4.7, "#f7ecd8", AMBER, lw=2.2)
    ax.text(10.375, 5.15, "WHAT IT DOES NOT AFFECT", ha="center", color=AMBER, fontsize=11, fontweight="bold")
    ax.text(
        10.375,
        2.85,
        "• Does not push the fluid around\n"
        "  (no dynamical force / no time step)\n\n"
        "• Does not make Navier–Stokes\n"
        r"  preserve $E_c$ or the shell" + "\n\n"
        "• Does not by itself close\n"
        r"  $T_{j\leftarrow j}$, $\alpha_+$, or $\mathcal{R}_\star$" + "\n\n"
        "• Does not solve Clay / regularity\n\n"
        "Yes — it is theoretical mathematics:\n"
        "a proved bound, not a simulation knob.",
        ha="center",
        va="center",
        color=SLATE,
        fontsize=9.3,
        linespacing=1.35,
    )

    fig.text(
        0.5,
        0.015,
        "Analogy: a speed limit on how kinked a band-limited vector field can be — not an engine that drives the flow.",
        ha="center",
        color=MUTED,
        fontsize=9.5,
    )
    save(fig, "ring-how-it-works.png")
    plt.close(fig)


def render_plain() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.7), facecolor=MIST)
    L = np.array([2.0, 4.0, 8.0, 16.0])
    ceil = L**2.5
    xi_ceil = ceil / 0.5

    ax = axes[0]
    ax.set_facecolor(FOG)
    for i, (nmodes, title, col) in enumerate(
        [(8, "few modes\n(small L)", STEEL), (40, "many modes\n(large L)", COPPER)]
    ):
        rng = np.random.default_rng(i + 2)
        th = rng.uniform(0, 2 * np.pi, nmodes)
        ph = rng.uniform(0, np.pi, nmodes)
        r = 1.0 if i == 0 else 1.6
        xs = r * np.sin(ph) * np.cos(th)
        ys = r * np.sin(ph) * np.sin(th)
        ax.scatter(xs + i * 3.2, ys, s=18, c=col, alpha=0.85)
        ax.text(i * 3.2, -2.3, title, ha="center", color=INK, fontsize=9)
    ax.set_xlim(-2, 5.5)
    ax.set_ylim(-2.8, 2.2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("More frequencies\n⇒ finer spatial wiggles allowed", color=INK, fontsize=10.5)

    ax = axes[1]
    ax.set_facecolor(FOG)
    ax.plot(L, ceil, "o-", color=STEEL, lw=2.2, label=r"$\|\nabla\omega\|$ ceiling")
    ax.plot(L, xi_ceil, "s--", color=COPPER, lw=2.0, label=r"$|\nabla\xi|$ on $E_{1/2}$")
    ax.set_xlabel("cutoff L")
    ax.set_ylabel("bound scale")
    ax.set_title("The ceiling grows with L\n(but still a hard cap at each L)", color=INK, fontsize=10.5)
    ax.legend(frameon=False, fontsize=8)
    ax.grid(True, alpha=0.25)

    ax = axes[2]
    ax.set_facecolor(FOG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.add_patch(
        mpatches.FancyBboxPatch(
            (0.4, 0.5),
            9.2,
            9.0,
            boxstyle="round,pad=0.05,rounding_size=0.1",
            facecolor="#ffffff",
            edgecolor=STEEL,
            lw=1.4,
        )
    )
    ax.text(5, 8.7, "Plain English", ha="center", color=INK, fontsize=11, fontweight="bold")
    ax.text(
        5,
        5.0,
        'It does not "reach into" the PDE\nand push.\n\n'
        "It says:\n"
        "IF the field only uses frequencies\n"
        "up to L, THEN on the strong set\n"
        "the direction cannot twist faster\n"
        "than about L to the 5/2.\n\n"
        "That is all — and that is enough\n"
        "to be useful as a lemma when those\n"
        "hypotheses appear in a proof.",
        ha="center",
        va="center",
        color=SLATE,
        fontsize=9.2,
        linespacing=1.4,
    )

    fig.suptitle(
        "Ring is theoretical — a conditional speed limit on direction twist",
        color=INK,
        fontsize=12.5,
        fontweight="bold",
    )
    fig.tight_layout(rect=[0, 0.02, 1, 0.93])
    save(fig, "ring-how-theoretical.png")
    plt.close(fig)


if __name__ == "__main__":
    render_chain()
    render_plain()
