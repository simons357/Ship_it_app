#!/usr/bin/env python3
"""Labeled teaching plots for the Navier–Stokes learning pack.

Run from the repo root:

    python3 docs/learn/navier-stokes/scripts/make_figures.py

Writes PNGs next to the hand-drawn figures under
``docs/learn/navier-stokes/figures/``. Copies the same files to
``/opt/cursor/artifacts`` when that directory exists.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

NAVY = "#1B365D"
TEAL = "#1A7A8C"
CORAL = "#C94C3C"
CREAM = "#FBF8F3"
INK = "#1A1A1A"

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
ARTIFACTS = Path("/opt/cursor/artifacts")


def _save(fig: plt.Figure, name: str) -> Path:
    FIG.mkdir(parents=True, exist_ok=True)
    dest = FIG / name
    fig.savefig(dest, dpi=160, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    if ARTIFACTS.is_dir():
        shutil.copy2(dest, ARTIFACTS / f"ns_{name}")
    return dest


def plot_laminar_vs_turbulent() -> Path:
    rng = np.random.default_rng(7)
    y = np.linspace(-1.0, 1.0, 400)
    u_lam = 1.0 - y**2
    u_turb_mean = (1.0 - np.abs(y)) ** (1.0 / 7.0)
    u_turb_mean = u_turb_mean / u_turb_mean.max()
    noise = 0.08 * rng.normal(size=y.size) * (1.0 - y**2)
    u_turb = np.clip(u_turb_mean + noise, 0.0, None)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), facecolor=CREAM)
    for ax in axes:
        ax.set_facecolor(CREAM)
        ax.set_xlim(0, 1.25)
        ax.set_ylim(-1.08, 1.08)
        ax.set_xlabel("speed across the pipe")
        ax.set_yticks([-1, 0, 1])
        ax.set_yticklabels(["wall", "center", "wall"])
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        ax.spines["left"].set_color(NAVY)
        ax.spines["bottom"].set_color(NAVY)
        ax.axhspan(-1.0, 1.0, color="#d9e7ea", alpha=0.35, zorder=0)
        ax.axhline(-1.0, color=NAVY, lw=3)
        ax.axhline(1.0, color=NAVY, lw=3)

    axes[0].plot(u_lam, y, color=TEAL, lw=2.6)
    axes[0].fill_betweenx(y, 0, u_lam, color=TEAL, alpha=0.18)
    axes[0].set_title("Laminar  (Poiseuille parabola)", color=TEAL, loc="left")
    axes[0].text(
        0.08,
        0.0,
        "smooth layers\nslide past each other",
        color=NAVY,
        va="center",
        fontsize=9,
    )

    axes[1].plot(u_turb_mean, y, color=CORAL, lw=2.2, label="mean")
    axes[1].plot(u_turb, y, color=NAVY, lw=0.9, alpha=0.7, label="one snapshot")
    axes[1].set_title("Turbulent  (mean + fluctuations)", color=CORAL, loc="left")
    axes[1].legend(frameon=False, loc="lower right", fontsize=8)

    fig.suptitle("Speed across a pipe: one profile vs many scales", color=INK, fontsize=13)
    fig.tight_layout()
    return _save(fig, "laminar_vs_turbulent_plot.png")


def plot_control_volume() -> Path:
    fig, ax = plt.subplots(figsize=(10.5, 5.2), facecolor=CREAM)
    ax.set_facecolor(CREAM)
    ax.set_xlim(-0.15, 1.15)
    ax.set_ylim(-0.2, 1.05)
    ax.set_aspect("equal")
    ax.axis("off")

    box = FancyBboxPatch(
        (0.22, 0.22),
        0.56,
        0.56,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        linewidth=2.0,
        edgecolor=NAVY,
        facecolor="#eef4f6",
        linestyle="--",
    )
    ax.add_patch(box)
    foil = FancyBboxPatch(
        (0.40, 0.44),
        0.22,
        0.08,
        boxstyle="round,pad=0.01,rounding_size=0.04",
        linewidth=1.6,
        edgecolor=NAVY,
        facecolor="#c5dbe0",
    )
    ax.add_patch(foil)

    for y in (0.38, 0.50, 0.62):
        ax.annotate(
            "",
            xy=(0.22, y),
            xytext=(0.02, y),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.0),
        )
        ax.annotate(
            "",
            xy=(0.98, y),
            xytext=(0.78, y),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.0),
        )

    ax.annotate(
        "",
        xy=(0.50, 0.08),
        xytext=(0.50, 0.22),
        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.8),
    )
    ax.text(0.50, 0.02, "gravity", ha="center", color=NAVY, fontsize=10)
    ax.text(0.50, 0.84, "control volume  V", ha="center", color=NAVY, fontsize=12, weight="bold")
    ax.text(0.50, 0.76, "surface  S  (dashed)", ha="center", color=TEAL, fontsize=10)
    ax.text(0.02, 0.72, "inlet", color=NAVY, fontsize=10)
    ax.text(0.86, 0.72, "outlet", color=NAVY, fontsize=10)
    ax.text(0.51, 0.48, "object", ha="center", va="center", fontsize=8, color=NAVY)
    ax.set_title(
        "A control volume: account for mass and momentum crossing S",
        color=INK,
        loc="left",
        fontsize=13,
        pad=12,
    )
    fig.tight_layout()
    return _save(fig, "control_volume_plot.png")


def plot_vortex() -> Path:
    n = 28
    x = np.linspace(-2.2, 2.2, n)
    y = np.linspace(-2.2, 2.2, n)
    X, Y = np.meshgrid(x, y)
    r = np.hypot(X, Y)
    r_core = 0.45
    circ = 1.8
    speed = np.where(r < r_core, (circ * r) / (2 * np.pi * r_core**2), circ / (2 * np.pi * np.maximum(r, 1e-6)))
    u = np.where(r < 1e-6, 0.0, -speed * Y / np.maximum(r, 1e-6))
    v = np.where(r < 1e-6, 0.0, speed * X / np.maximum(r, 1e-6))

    fig, ax = plt.subplots(figsize=(6.8, 6.4), facecolor=CREAM)
    ax.set_facecolor(CREAM)
    mag = np.hypot(u, v)
    ax.streamplot(
        X,
        Y,
        u,
        v,
        color=mag,
        cmap="viridis",
        density=1.35,
        linewidth=1.1,
        arrowsize=1.1,
    )
    q = ax.quiver(X, Y, u, v, mag, cmap="magma", scale=18, width=0.004, alpha=0.55)
    fig.colorbar(q, ax=ax, fraction=0.046, pad=0.04, label="speed")
    core = Circle((0, 0), r_core, fill=False, color=CORAL, lw=1.6, linestyle="--")
    ax.add_patch(core)
    ax.set_aspect("equal")
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("A vortex (Rankine): spinning core, 1/r swirl outside", color=INK)
    ax.annotate("core", xy=(r_core * 0.2, r_core * 0.7), color=CORAL, fontsize=10)
    for spine in ax.spines.values():
        spine.set_color(NAVY)
    fig.tight_layout()
    return _save(fig, "vortex_plot.png")


def plot_energy_spectrum() -> Path:
    k = np.logspace(-1, 1.85, 500)
    k_i, k_d = 0.9, 9.0
    # Piecewise Kolmogorov sketch: production bump, -5/3, then viscous cutoff.
    E = np.where(
        k < k_i,
        (k / k_i) ** (-1.0),
        (k / k_i) ** (-5.0 / 3.0),
    )
    E = E * np.exp(-((k / k_d) ** 2))
    E = E / E.max()

    fig, ax = plt.subplots(figsize=(9.6, 5.0), facecolor=CREAM)
    ax.set_facecolor(CREAM)
    ax.loglog(k, E, color=NAVY, lw=2.4)
    k_line = np.array([1.1, 10.0])
    ref = E[np.argmin(np.abs(k - 1.1))] * (k_line / 1.1) ** (-5.0 / 3.0)
    ax.loglog(k_line, ref, color=TEAL, lw=1.8, linestyle="--")
    ax.axvspan(0.1, 0.9, color=TEAL, alpha=0.12)
    ax.axvspan(0.9, 7.5, color="#e8d5b5", alpha=0.25)
    ax.axvspan(7.5, 80, color=CORAL, alpha=0.10)
    ax.text(0.16, 0.55, "large eddies", color=NAVY, fontsize=9)
    ax.text(1.5, 0.28, "in-between scales", color=NAVY, fontsize=9)
    ax.text(1.5, 0.12, r"$k^{-5/3}$ sketch", color=TEAL, fontsize=9)
    ax.text(11, 0.008, "viscosity\nkills them", color=CORAL, fontsize=9)
    ax.set_ylim(2e-4, 2.0)
    ax.set_xlim(0.1, 50)
    ax.set_xlabel("wavenumber  k  (1 / eddy size)")
    ax.set_ylabel("energy density  E(k)")
    ax.set_title("Energy cascade as a spectrum — a sketch, not a measurement", color=INK, loc="left")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()
    return _save(fig, "energy_spectrum_plot.png")


def main() -> None:
    written = [
        plot_laminar_vs_turbulent(),
        plot_control_volume(),
        plot_vortex(),
        plot_energy_spectrum(),
    ]
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
