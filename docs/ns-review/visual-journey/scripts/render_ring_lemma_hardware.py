#!/usr/bin/env python3
"""Render physically grounded Ring Lemma (Oct 2) hardware visuals.

Spatial geometry only. No NS / Clay claim.
Source of truth: RingLemma_Corrected_Geometric_Note_2026-10-02.tex
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

OUT_DIRS = [
    Path("/opt/cursor/artifacts/nse-status-now"),
    Path("docs/ns-review/visual-journey/figures"),
]

# Visual direction: ink / copper / slate (not purple / cream-default AI look)
INK = "#0f1c2e"
SLATE = "#2a3f55"
COPPER = "#b86b3c"
STEEL = "#4a6a82"
FOG = "#e8eef2"
MIST = "#f4f7f9"
GREEN = "#1f6b4a"
AMBER = "#c4892a"
MUTED = "#6b7c8a"


def ensure_dirs() -> None:
    for d in OUT_DIRS:
        d.mkdir(parents=True, exist_ok=True)


def save(fig: plt.Figure, name: str) -> None:
    for d in OUT_DIRS:
        path = d / name
        fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"wrote {path}")


def render_fourier_hardware() -> None:
    """3D Fourier lattice ball |k|≤L — the actual band-limit hardware."""
    L = 6.5
    ks = np.arange(-8, 9)
    pts = []
    for kx in ks:
        for ky in ks:
            for kz in ks:
                r = np.sqrt(kx * kx + ky * ky + kz * kz)
                if 0 < r <= L:
                    pts.append((kx, ky, kz, r))
    pts = np.array(pts)

    fig = plt.figure(figsize=(11.2, 7.2), facecolor=MIST)
    ax = fig.add_subplot(121, projection="3d", facecolor=MIST)
    ax2 = fig.add_subplot(122, facecolor=FOG)

    # Left: lattice ball
    rnorm = (pts[:, 3] - pts[:, 3].min()) / (pts[:, 3].max() - pts[:, 3].min() + 1e-9)
    colors = plt.cm.Blues_r(0.15 + 0.7 * rnorm)
    ax.scatter(
        pts[:, 0],
        pts[:, 1],
        pts[:, 2],
        c=colors,
        s=18 + 28 * (1 - rnorm),
        depthshade=True,
        alpha=0.95,
        edgecolors="none",
    )
    # Wire sphere at |k|=L
    u = np.linspace(0, 2 * np.pi, 60)
    v = np.linspace(0, np.pi, 30)
    xs = L * np.outer(np.cos(u), np.sin(v))
    ys = L * np.outer(np.sin(u), np.sin(v))
    zs = L * np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(xs, ys, zs, color=COPPER, linewidth=0.55, alpha=0.55)
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_zlim(-8, 8)
    ax.set_xlabel(r"$k_1$", color=SLATE)
    ax.set_ylabel(r"$k_2$", color=SLATE)
    ax.set_zlabel(r"$k_3$", color=SLATE)
    ax.set_title("Fourier hardware\nband-limited support $|k|\\leq L$", color=INK, pad=10)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.view_init(elev=22, azim=38)
    ax.set_box_aspect((1, 1, 1))

    # Right: what that buys you for ∇ω
    Lgrid = np.linspace(1, 12, 200)
    # From note: ||∇ω||_∞ ≤ C L^{5/2} ||ω||_2  (Fourier CS + Parseval)
    # and Bernstein: ||∇ω||_∞ ≤ C L ||ω||_∞
    ax2.fill_between(Lgrid, Lgrid**2.5, alpha=0.18, color=STEEL, label=r"$L^{5/2}$ ceiling from $L^2$ mass")
    ax2.plot(Lgrid, Lgrid**2.5, color=STEEL, lw=2.4, label=r"$\|\nabla\omega\|_\infty\lesssim L^{5/2}\|\omega\|_2$")
    ax2.plot(Lgrid, Lgrid, color=COPPER, lw=2.2, ls="--", label=r"Bernstein: $\lesssim L\|\omega\|_\infty$")
    ax2.set_xlabel("frequency cutoff $L$", color=SLATE)
    ax2.set_ylabel("spatial gradient scale (arb.)", color=SLATE)
    ax2.set_title("What the shell forces on $\\nabla\\omega$\n(Oct 2 Prop. 1 & 3)", color=INK, pad=10)
    ax2.legend(loc="upper left", frameon=False, fontsize=9)
    ax2.set_xlim(1, 12)
    ax2.set_ylim(0, 12**2.5 * 1.05)
    ax2.grid(True, alpha=0.25, color=STEEL)
    for spine in ax2.spines.values():
        spine.set_color("#c5d0d8")
    ax2.tick_params(colors=MUTED)

    fig.suptitle(
        "Ring Lemma hardware — the frequency ball is structure, not a PDE theorem",
        color=INK,
        fontsize=13,
        fontweight="bold",
        y=0.98,
    )
    fig.text(
        0.5,
        0.02,
        r"On $\mathbb{T}^3$: Fourier support in $|k|\leq L$ caps how fast vorticity can vary in space.",
        ha="center",
        color=MUTED,
        fontsize=9,
    )
    save(fig, "ring-hardware-fourier-ball.png")
    plt.close(fig)


def synthetic_bandlimited_omega(L: int = 8, ngrid: int = 96, seed: int = 7):
    """Build a real divergence-free-ish vorticity via band-limited Fourier modes.

    We synthesize ω directly with k·ω̂=0 so div ω = 0 (valid for ω=curl u).
    """
    rng = np.random.default_rng(seed)
    N = ngrid
    # Physical grid on [0, 2π)
    x = np.linspace(0, 2 * np.pi, N, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")

    omega = np.zeros((3, N, N, N), dtype=np.float64)
    # Sum random modes with |k|≤L, projected transverse to k
    modes = []
    for kx in range(-L, L + 1):
        for ky in range(-L, L + 1):
            for kz in range(-L, L + 1):
                kk = np.array([kx, ky, kz], dtype=float)
                r = np.linalg.norm(kk)
                if r == 0 or r > L:
                    continue
                # Prefer mid/high shell energy for visual structure
                if r < L * 0.35:
                    continue
                modes.append(kk)
    modes = modes[:180]  # keep render fast
    for kk in modes:
        amp = rng.normal(0, 1.0 / (1 + 0.15 * np.linalg.norm(kk)))
        phase = rng.uniform(0, 2 * np.pi)
        # Random vector, project off k
        v = rng.normal(size=3)
        v = v - kk * (v @ kk) / (kk @ kk)
        nv = np.linalg.norm(v)
        if nv < 1e-12:
            continue
        v = v / nv * amp
        wave = np.cos(kk[0] * X + kk[1] * Y + kk[2] * Z + phase)
        for a in range(3):
            omega[a] += v[a] * wave
    return omega, x


def render_strong_set_direction() -> None:
    """Spatial slice: |ω| heatmap + ξ arrows on E_c — what Ring controls."""
    omega, x = synthetic_bandlimited_omega(L=7, ngrid=80, seed=11)
    # Mid-plane z = π
    iz = omega.shape[3] // 2
    w = omega[:, :, :, iz]
    mag = np.linalg.norm(w, axis=0)
    # L2 norm over full 3D field
    w2 = float(np.sqrt(np.mean(np.sum(omega**2, axis=0))))
    c = 0.45
    thresh = c * w2
    Ec = mag >= thresh

    # Direction ξ
    eps = 1e-12
    xi = w / (mag[None, ...] + eps)

    # Approximate |∇ξ| on plane via finite differences of ξ
    dxi_dx = np.gradient(xi, x[1] - x[0], axis=1)
    dxi_dy = np.gradient(xi, x[1] - x[0], axis=2)
    # Frobenius of in-plane gradient of ξ
    grad_xi = np.sqrt(
        np.sum(dxi_dx**2, axis=0) + np.sum(dxi_dy**2, axis=0)
    )

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6), facecolor=MIST)
    extent = [0, 2 * np.pi, 0, 2 * np.pi]

    # Panel 1: |ω|
    ax = axes[0]
    im0 = ax.imshow(
        mag.T,
        origin="lower",
        extent=extent,
        cmap=LinearSegmentedColormap.from_list("mag", ["#0f1c2e", "#2a4a66", "#c4892a", "#f0e6d8"]),
        aspect="equal",
    )
    ax.contour(x, x, Ec.T.astype(float), levels=[0.5], colors=[COPPER], linewidths=1.6)
    ax.set_title(r"$|\omega|$ on a torus slice" + "\n" + r"copper contour = strong set $E_c$", color=INK)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    cb0 = fig.colorbar(im0, ax=ax, fraction=0.046, pad=0.04)
    cb0.ax.tick_params(labelsize=7)
    cb0.set_label(r"$|\omega|$", fontsize=8)

    # Panel 2: ξ arrows on E_c
    ax = axes[1]
    ax.imshow(
        mag.T,
        origin="lower",
        extent=extent,
        cmap="Greys",
        alpha=0.35,
        aspect="equal",
    )
    ax.contourf(x, x, Ec.T.astype(float), levels=[0.5, 1.5], colors=[("#1f6b4a33")], alpha=0.55)
    step = 4
    Xs, Ys = np.meshgrid(x[::step], x[::step], indexing="ij")
    U = xi[0, ::step, ::step]
    V = xi[1, ::step, ::step]
    mask = Ec[::step, ::step]
    ax.quiver(
        Xs[mask],
        Ys[mask],
        U[mask],
        V[mask],
        color=COPPER,
        scale=18,
        width=0.0045,
        headwidth=3.2,
        pivot="mid",
        alpha=0.95,
    )
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(0, 2 * np.pi)
    ax.set_aspect("equal")
    ax.set_title(r"direction $\xi=\omega/|\omega|$ on $E_c$" + "\nRing bounds how fast these arrows twist", color=INK)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    # Panel 3: |∇ξ| only on E_c
    ax = axes[2]
    show = np.where(Ec, grad_xi, np.nan)
    im2 = ax.imshow(
        show.T,
        origin="lower",
        extent=extent,
        cmap=LinearSegmentedColormap.from_list("gxi", ["#e8eef2", "#4a6a82", "#b86b3c", "#5a1f12"]),
        aspect="equal",
    )
    ax.contour(x, x, Ec.T.astype(float), levels=[0.5], colors=[INK], linewidths=1.0, alpha=0.7)
    ax.set_title(r"$|\nabla\xi|$ measured on $E_c$" + "\n" + r"Oct 2: $\lesssim L^{5/2}/c$ (sharp)", color=INK)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    cb2 = fig.colorbar(im2, ax=ax, fraction=0.046, pad=0.04)
    cb2.ax.tick_params(labelsize=7)
    cb2.set_label(r"$|\nabla\xi|$", fontsize=8)

    fig.suptitle(
        "What Ring does in space — control the twist of vorticity direction on the strong set",
        color=INK,
        fontsize=12.5,
        fontweight="bold",
        y=1.02,
    )
    fig.text(
        0.5,
        -0.02,
        r"Synthetic band-limited field ($|k|\leq 7$) on $\mathbb{T}^3$. Hardware fact about a snapshot — not NS evolution.",
        ha="center",
        color=MUTED,
        fontsize=9,
    )
    fig.tight_layout()
    save(fig, "ring-hardware-strong-set-xi.png")
    plt.close(fig)


def sharpness_family(n: int) -> float:
    """Lower bound constant piece from Prop. 2: e2·∂1 ξ(0) ≥ (15/64) n^{5/2}."""
    return (15.0 / 64.0) * (n**2.5)


def render_sharpness_obstruction() -> None:
    """Show why L^{5/2} is forced — the shear family lower bound."""
    ns = np.array([4, 8, 16, 32, 64], dtype=float)
    Ls = 4 * ns
    lower = sharpness_family(ns)
    # Naive hoped CL line (false at fixed L2 threshold)
    hoped = 0.08 * Ls
    # Upper envelope scale ~ L^{5/2}
    upper = 0.25 * (Ls**2.5)

    fig, ax = plt.subplots(figsize=(10.2, 5.8), facecolor=MIST)
    ax.set_facecolor(FOG)
    ax.loglog(Ls, lower, "o-", color=COPPER, lw=2.4, ms=8, label=r"shear family lower bound $\gtrsim L^{5/2}$")
    ax.loglog(Ls, upper, "--", color=STEEL, lw=2.0, label=r"matching $L^{5/2}$ scale (Prop. 1)")
    ax.loglog(Ls, hoped, ":", color=MUTED, lw=2.2, label=r"false hope: plain $CL$ at fixed $L^2$ threshold")
    ax.fill_between(Ls, lower, upper, color=STEEL, alpha=0.12)

    ax.annotate(
        "sharpness: you cannot\nreplace $L^{5/2}$ by $L$\nat fixed $c$ in $E_c$",
        xy=(Ls[3], lower[3]),
        xytext=(Ls[1] * 1.1, lower[3] * 8),
        color=INK,
        fontsize=10,
        arrowprops=dict(arrowstyle="->", color=COPPER, lw=1.4),
    )
    ax.set_xlabel(r"frequency cutoff $L$ (log)", color=SLATE)
    ax.set_ylabel(r"$\|\nabla\xi\|_{L^\infty(E_{1/2})}$ scale (log)", color=SLATE)
    ax.set_title(
        "Ring Lemma RL-G2 — sharpness is structural too\n"
        r"explicit divergence-free shear family forces the $L^{5/2}$ power",
        color=INK,
        fontweight="bold",
        pad=12,
    )
    ax.legend(loc="upper left", frameon=False)
    ax.grid(True, which="both", alpha=0.25, color=STEEL)
    for spine in ax.spines.values():
        spine.set_color("#c5d0d8")
    fig.text(
        0.5,
        0.02,
        "Oct 2 Prop. 2. Still spatial geometry. Does not say NS preserves the bad shear.",
        ha="center",
        color=MUTED,
        fontsize=9,
    )
    save(fig, "ring-hardware-sharpness-scaling.png")
    plt.close(fig)


def render_hardware_vs_live_gate() -> None:
    """One clear map: Ring = installed structure; live gate = dynamics still open."""
    fig, ax = plt.subplots(figsize=(11.5, 5.2), facecolor=MIST)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")

    def box(x, y, w, h, face, edge, title, body, lw=2.0, ls="-"):
        rect = mpatches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.15",
            facecolor=face,
            edgecolor=edge,
            linewidth=lw,
            linestyle=ls,
        )
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h - 0.45, title, ha="center", va="top", color=INK, fontsize=11, fontweight="bold")
        ax.text(x + w / 2, y + h / 2 - 0.15, body, ha="center", va="center", color=SLATE, fontsize=9.2)

    box(
        0.4,
        1.2,
        3.4,
        3.6,
        "#dceee4",
        GREEN,
        "INSTALLED HARDWARE",
        "Ring Lemma Oct 2\n"
        r"band-limit $|k|\leq L$" + "\n"
        r"+ direction $\xi=\omega/|\omega|$" + "\n"
        r"bound on $E_c$ / $F_a$" + "\n\n"
        "spatial · proved · sharp",
        lw=2.4,
    )
    box(
        4.3,
        1.2,
        3.4,
        3.6,
        "#ece7df",
        MUTED,
        "OPTIONAL TEXTURE",
        "SND (conditional)\n"
        "alignment language\n"
        "on top of geometry\n\n"
        "not required to\nname the live gate",
        lw=1.6,
        ls="--",
    )
    box(
        8.2,
        1.2,
        3.4,
        3.6,
        "#f7ecd8",
        AMBER,
        "LIVE GATE (OPEN)",
        "same-scale $T_{j\\leftarrow j}$\n"
        r"$(\alpha_{\mathrm{loc},j})_+$ depletion" + "\n"
        "product / uniform "
        r"$\mathcal{R}_\star$" + "\n\n"
        "dynamics — not Ring",
        lw=2.6,
        ls="--",
    )

    ax.annotate("", xy=(4.2, 3.0), xytext=(3.9, 3.0), arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.8))
    ax.annotate("", xy=(8.1, 3.0), xytext=(7.8, 3.0), arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.8, linestyle="--"))

    ax.text(
        6.0,
        5.5,
        "Yes — Ring is structural hardware on the side of the map",
        ha="center",
        color=INK,
        fontsize=13.5,
        fontweight="bold",
    )
    ax.text(
        6.0,
        0.45,
        "It bolts a geometric ceiling onto band-limited vorticity direction. It does not close the dynamical door.",
        ha="center",
        color=MUTED,
        fontsize=9.5,
    )
    save(fig, "ring-hardware-on-the-map.png")
    plt.close(fig)


def render_one_card() -> None:
    """Single hero card answering 'what is it / what does it do'."""
    fig = plt.figure(figsize=(11.2, 7.0), facecolor=MIST)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.15, 1], hspace=0.28, wspace=0.18)

    # Top spanning: plain English
    ax0 = fig.add_subplot(gs[0, :])
    ax0.set_xlim(0, 10)
    ax0.set_ylim(0, 4)
    ax0.axis("off")
    ax0.add_patch(
        mpatches.FancyBboxPatch(
            (0.2, 0.3),
            9.6,
            3.4,
            boxstyle="round,pad=0.05,rounding_size=0.12",
            facecolor=FOG,
            edgecolor=STEEL,
            lw=1.5,
        )
    )
    ax0.text(5, 3.3, "RING LEMMA — WHAT IT IS", ha="center", color=INK, fontsize=14, fontweight="bold")
    ax0.text(
        5,
        2.35,
        "A proved spatial fact about band-limited vorticity on the 3-torus.\n"
        "Where spin is strong enough relative to its L² mass, the direction of that spin\n"
        "cannot twist faster than about frequency to the power 5/2 — and that power is sharp.\n"
        "If amplitude is also peak-controlled, the ceiling drops to linear in frequency.",
        ha="center",
        va="center",
        color=SLATE,
        fontsize=10.5,
        linespacing=1.45,
    )
    ax0.text(
        5,
        0.75,
        "Hardware / structure  ·  not a Navier–Stokes theorem  ·  not Clay",
        ha="center",
        color=COPPER,
        fontsize=11,
        fontweight="bold",
    )

    # Bottom left: does
    ax1 = fig.add_subplot(gs[1, 0])
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis("off")
    ax1.add_patch(
        mpatches.FancyBboxPatch(
            (0.3, 0.4),
            9.4,
            9.2,
            boxstyle="round,pad=0.05,rounding_size=0.12",
            facecolor="#dceee4",
            edgecolor=GREEN,
            lw=2,
        )
    )
    ax1.text(5, 8.7, "WHAT IT DOES", ha="center", color=GREEN, fontsize=12, fontweight="bold")
    bullets_do = [
        r"Needs Fourier support $|k|\leq L$",
        r"Looks at $\xi=\omega/|\omega|$",
        r"On strong set $E_c$: $|\nabla\xi|\lesssim L^{5/2}/c$",
        r"Sharp: $L^{5/2}$ cannot drop to $L$",
        r"On peak set $F_a$ (amp control): $\lesssim L/a$",
    ]
    for i, t in enumerate(bullets_do):
        ax1.text(1.0, 7.2 - 1.2 * i, "▸  " + t, color=INK, fontsize=10.2)

    # Bottom right: does not
    ax2 = fig.add_subplot(gs[1, 1])
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis("off")
    ax2.add_patch(
        mpatches.FancyBboxPatch(
            (0.3, 0.4),
            9.4,
            9.2,
            boxstyle="round,pad=0.05,rounding_size=0.12",
            facecolor="#f7ecd8",
            edgecolor=AMBER,
            lw=2,
        )
    )
    ax2.text(5, 8.7, "WHAT IT DOES NOT", ha="center", color=AMBER, fontsize=12, fontweight="bold")
    bullets_dont = [
        "Does not evolve in time",
        "Does not preserve $E_c$ under NS",
        "Does not close same-scale $T$",
        r"Does not prove $\alpha_+$ depletion",
        "Does not solve Clay / regularity",
    ]
    for i, t in enumerate(bullets_dont):
        ax2.text(1.0, 7.2 - 1.2 * i, "▸  " + t, color=INK, fontsize=10.2)

    save(fig, "ring-hardware-what-it-is-card.png")
    plt.close(fig)


def main() -> None:
    ensure_dirs()
    render_fourier_hardware()
    render_strong_set_direction()
    render_sharpness_obstruction()
    render_hardware_vs_live_gate()
    render_one_card()
    # Keep the earlier names refreshed with best map/card too
    # Copy aliases for the status-now folder naming convention
    import shutil

    aliases = {
        "ring-hardware-what-it-is-card.png": "ring-lemma-what-it-is.png",
        "ring-hardware-on-the-map.png": "ring-lemma-on-the-map.png",
    }
    for src, dst in aliases.items():
        for d in OUT_DIRS:
            s, t = d / src, d / dst
            if s.exists():
                shutil.copy2(s, t)
                print(f"alias {t}")


if __name__ == "__main__":
    main()
