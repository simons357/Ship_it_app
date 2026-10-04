#!/usr/bin/env python3
"""Richer 2D / 3D geometry pictures of Ring Lemma (Oct 2).

Spatial structure only. Synthetic band-limited vorticity on T^3.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap, Normalize
from mpl_toolkits.mplot3d.art3d import Line3DCollection
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
MUTED = "#6b7c8a"
MAG_CMAP = LinearSegmentedColormap.from_list(
    "mag", ["#0f1c2e", "#1e3a55", "#3d6b7a", "#c4892a", "#f2e6d4"]
)
TWIST_CMAP = LinearSegmentedColormap.from_list(
    "twist", ["#e8eef2", "#6a8a9e", "#b86b3c", "#5a1f12"]
)


def ensure_dirs() -> None:
    for d in OUT_DIRS:
        d.mkdir(parents=True, exist_ok=True)


def save(fig: plt.Figure, name: str) -> None:
    for d in OUT_DIRS:
        path = d / name
        fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"wrote {path}")


def synthetic_omega(L: int = 6, ngrid: int = 56, seed: int = 19):
    rng = np.random.default_rng(seed)
    N = ngrid
    x = np.linspace(0, 2 * np.pi, N, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    omega = np.zeros((3, N, N, N), dtype=np.float64)

    # Structured carrier + band-limited noise → readable geometry
    # Carrier: helical-ish shear (div-free as a vorticity field)
    omega[0] += 0.55 * np.sin(2 * Y) * np.cos(Z)
    omega[1] += 0.55 * np.cos(2 * X) * np.sin(Z)
    omega[2] += 0.85 * np.cos(X) * np.cos(Y)

    modes = []
    for kx in range(-L, L + 1):
        for ky in range(-L, L + 1):
            for kz in range(-L, L + 1):
                kk = np.array([kx, ky, kz], dtype=float)
                r = np.linalg.norm(kk)
                if r == 0 or r > L or r < 0.4 * L:
                    continue
                modes.append(kk)
    rng.shuffle(modes)
    for kk in modes[:140]:
        amp = rng.normal(0, 0.55 / (1 + 0.12 * np.linalg.norm(kk)))
        phase = rng.uniform(0, 2 * np.pi)
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


def strong_mask(omega, c=0.42):
    mag = np.linalg.norm(omega, axis=0)
    w2 = float(np.sqrt(np.mean(mag**2)))
    return mag, mag >= c * w2, w2


def render_2d_slice_gallery() -> None:
    omega, x = synthetic_omega(L=6, ngrid=64, seed=21)
    mag, Ec, _ = strong_mask(omega, c=0.4)
    eps = 1e-12
    xi = omega / (mag[None, ...] + eps)
    N = mag.shape[0]
    z_fracs = [0.15, 0.35, 0.55, 0.75]
    fig, axes = plt.subplots(2, 4, figsize=(14.5, 7.0), facecolor=MIST)
    extent = [0, 2 * np.pi, 0, 2 * np.pi]

    for col, zf in enumerate(z_fracs):
        iz = int(zf * N) % N
        m = mag[:, :, iz]
        e = Ec[:, :, iz]
        # |ω|
        ax = axes[0, col]
        ax.imshow(m.T, origin="lower", extent=extent, cmap=MAG_CMAP, aspect="equal")
        ax.contour(x, x, e.T.astype(float), levels=[0.5], colors=[COPPER], linewidths=1.4)
        ax.set_title(rf"$z={zf:.2f}\cdot 2\pi$" + "\n" + r"$|\omega|$ + $E_c$", color=INK, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
        # ξ arrows
        ax = axes[1, col]
        ax.imshow(m.T, origin="lower", extent=extent, cmap="Greys", alpha=0.3, aspect="equal")
        ax.contourf(x, x, e.T.astype(float), levels=[0.5, 1.5], colors=["#1f6b4a22"])
        step = 3
        Xs, Ys = np.meshgrid(x[::step], x[::step], indexing="ij")
        U = xi[0, ::step, ::step, iz]
        V = xi[1, ::step, ::step, iz]
        mask = e[::step, ::step]
        ax.quiver(
            Xs[mask], Ys[mask], U[mask], V[mask],
            color=COPPER, scale=16, width=0.005, headwidth=3.0, pivot="mid",
        )
        ax.set_xlim(0, 2 * np.pi)
        ax.set_ylim(0, 2 * np.pi)
        ax.set_aspect("equal")
        ax.set_title(r"$\xi$ arrows on $E_c$", color=INK, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle(
        "Ring geometry in 2D — successive torus slices (band-limited vorticity)",
        color=INK, fontsize=13, fontweight="bold", y=0.98,
    )
    fig.text(
        0.5, 0.01,
        r"Copper contour / arrows live only where $|\omega|$ is strong enough ($E_c$). Ring bounds how fast those arrows twist.",
        ha="center", color=MUTED, fontsize=9,
    )
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    save(fig, "ring-geom-2d-slice-gallery.png")
    plt.close(fig)


def render_2d_twist_closeup() -> None:
    omega, x = synthetic_omega(L=7, ngrid=80, seed=11)
    mag, Ec, _ = strong_mask(omega, c=0.45)
    iz = omega.shape[3] // 2
    m = mag[:, :, iz]
    e = Ec[:, :, iz]
    eps = 1e-12
    xi = omega[:, :, :, iz] / (m[None, ...] + eps)
    dxi_dx = np.gradient(xi, x[1] - x[0], axis=1)
    dxi_dy = np.gradient(xi, x[1] - x[0], axis=2)
    grad_xi = np.sqrt(np.sum(dxi_dx**2, axis=0) + np.sum(dxi_dy**2, axis=0))

    fig, axes = plt.subplots(1, 2, figsize=(12.2, 5.6), facecolor=MIST)
    extent = [0, 2 * np.pi, 0, 2 * np.pi]

    ax = axes[0]
    ax.imshow(m.T, origin="lower", extent=extent, cmap=MAG_CMAP, aspect="equal")
    # streamplot-like dense arrows on E_c
    step = 2
    Xs, Ys = np.meshgrid(x[::step], x[::step], indexing="ij")
    U = xi[0, ::step, ::step]
    V = xi[1, ::step, ::step]
    mask = e[::step, ::step]
    ax.quiver(
        Xs[mask], Ys[mask], U[mask], V[mask],
        color="white", scale=22, width=0.0032, headwidth=2.6, pivot="mid", alpha=0.9,
    )
    ax.contour(x, x, e.T.astype(float), levels=[0.5], colors=[COPPER], linewidths=2.0)
    ax.set_title("2D close-up — direction field on the strong set", color=INK, fontweight="bold")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    ax = axes[1]
    show = np.where(e, grad_xi, np.nan)
    im = ax.imshow(show.T, origin="lower", extent=extent, cmap=TWIST_CMAP, aspect="equal")
    ax.contour(x, x, e.T.astype(float), levels=[0.5], colors=[INK], linewidths=1.2)
    # Overlay a few arrows colored by local twist
    step = 3
    Xs, Ys = np.meshgrid(x[::step], x[::step], indexing="ij")
    U = xi[0, ::step, ::step]
    V = xi[1, ::step, ::step]
    g = grad_xi[::step, ::step]
    mask = e[::step, ::step]
    ax.quiver(
        Xs[mask], Ys[mask], U[mask], V[mask], g[mask],
        cmap=TWIST_CMAP, scale=18, width=0.004, headwidth=3.0, pivot="mid",
        norm=Normalize(vmin=np.nanpercentile(grad_xi[e], 5), vmax=np.nanpercentile(grad_xi[e], 95)),
    )
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r"$|\nabla\xi|$  (twist rate)", fontsize=9)
    ax.set_title(r"Same slice — twist rate $|\nabla\xi|$ on $E_c$", color=INK, fontweight="bold")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    fig.suptitle(
        "What Ring controls in the plane: how fast the spin direction turns",
        color=INK, fontsize=12.5, fontweight="bold",
    )
    fig.text(
        0.5, 0.01,
        r"Oct 2: on $E_c$, $\|\nabla\xi\|_\infty\lesssim L^{5/2}/c$. Geometry of a snapshot.",
        ha="center", color=MUTED, fontsize=9,
    )
    fig.tight_layout(rect=[0, 0.04, 1, 0.95])
    save(fig, "ring-geom-2d-twist-closeup.png")
    plt.close(fig)


def render_3d_strong_set_cloud() -> None:
    omega, x = synthetic_omega(L=5, ngrid=48, seed=7)
    mag, Ec, _ = strong_mask(omega, c=0.55)
    # Subsample strong points for cloud
    idx = np.argwhere(Ec)
    rng = np.random.default_rng(0)
    if len(idx) > 3500:
        pick = rng.choice(len(idx), size=3500, replace=False)
        idx = idx[pick]
    pts = x[idx]
    vals = mag[idx[:, 0], idx[:, 1], idx[:, 2]]
    xi = omega[:, idx[:, 0], idx[:, 1], idx[:, 2]]
    xi = xi / (np.linalg.norm(xi, axis=0) + 1e-12)

    fig = plt.figure(figsize=(12.5, 6.0), facecolor=MIST)
    ax1 = fig.add_subplot(121, projection="3d", facecolor=MIST)
    ax2 = fig.add_subplot(122, projection="3d", facecolor=MIST)

    sc = ax1.scatter(
        pts[:, 0], pts[:, 1], pts[:, 2],
        c=vals, cmap=MAG_CMAP, s=8, alpha=0.85, edgecolors="none",
    )
    ax1.set_title(r"3D strong set $E_c$" + "\n" + r"points where $|\omega|$ is large enough", color=INK)
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$y$")
    ax1.set_zlabel(r"$z$")
    ax1.set_xlim(0, 2 * np.pi)
    ax1.set_ylim(0, 2 * np.pi)
    ax1.set_zlim(0, 2 * np.pi)
    fig.colorbar(sc, ax=ax1, shrink=0.55, pad=0.08, label=r"$|\omega|$")
    ax1.view_init(elev=24, azim=35)

    # Direction sticks on a thinner sample
    if len(idx) > 700:
        pick2 = rng.choice(len(idx), size=700, replace=False)
    else:
        pick2 = np.arange(len(idx))
    p2 = pts[pick2]
    v2 = xi[:, pick2]
    # Scale arrow length
    scale = 0.55
    segs = np.stack([p2, p2 + scale * v2.T], axis=1)
    # Color by |ω|
    lc = Line3DCollection(segs, colors=plt.cm.copper(Normalize()(vals[pick2])), linewidths=1.1, alpha=0.9)
    ax2.add_collection3d(lc)
    ax2.scatter(p2[:, 0], p2[:, 1], p2[:, 2], c=vals[pick2], cmap=MAG_CMAP, s=6, alpha=0.5)
    ax2.set_title(r"3D direction sticks $\xi=\omega/|\omega|$" + "\nRing bounds how fast these turn in space", color=INK)
    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$y$")
    ax2.set_zlabel(r"$z$")
    ax2.set_xlim(0, 2 * np.pi)
    ax2.set_ylim(0, 2 * np.pi)
    ax2.set_zlim(0, 2 * np.pi)
    ax2.view_init(elev=24, azim=35)

    fig.suptitle(
        "Ring geometry in 3D — the strong set and its direction field",
        color=INK, fontsize=13, fontweight="bold",
    )
    fig.text(
        0.5, 0.02,
        r"Synthetic band-limited field on $\mathbb{T}^3$. Hardware/structure of a frozen frame — not NS time evolution.",
        ha="center", color=MUTED, fontsize=9,
    )
    save(fig, "ring-geom-3d-strong-set.png")
    plt.close(fig)


def render_3d_fourier_shell() -> None:
    """Shell (annulus) view — modes live near a frequency ring/ball surface."""
    L_lo, L_hi = 4.0, 7.0
    ks = np.arange(-9, 10)
    pts = []
    for kx in ks:
        for ky in ks:
            for kz in ks:
                r = np.sqrt(kx * kx + ky * ky + kz * kz)
                if L_lo <= r <= L_hi:
                    pts.append((kx, ky, kz, r))
    pts = np.array(pts)

    fig = plt.figure(figsize=(12.2, 5.8), facecolor=MIST)
    ax1 = fig.add_subplot(121, projection="3d", facecolor=MIST)
    ax2 = fig.add_subplot(122, projection="3d", facecolor=MIST)

    rnorm = (pts[:, 3] - L_lo) / (L_hi - L_lo + 1e-9)
    ax1.scatter(
        pts[:, 0], pts[:, 1], pts[:, 2],
        c=plt.cm.Blues_r(0.15 + 0.75 * rnorm),
        s=22, alpha=0.95, edgecolors="none", depthshade=True,
    )
    # Wire spheres
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 25)
    for R, col, lw in [(L_lo, MUTED, 0.5), (L_hi, COPPER, 0.9)]:
        xs = R * np.outer(np.cos(u), np.sin(v))
        ys = R * np.outer(np.sin(u), np.sin(v))
        zs = R * np.outer(np.ones_like(u), np.cos(v))
        ax1.plot_wireframe(xs, ys, zs, color=col, linewidth=lw, alpha=0.45)
    ax1.set_title("3D Fourier shell (dyadic annulus)\nmodes that make the spatial field", color=INK)
    ax1.set_xlabel(r"$k_1$")
    ax1.set_ylabel(r"$k_2$")
    ax1.set_zlabel(r"$k_3$")
    ax1.set_box_aspect((1, 1, 1))
    ax1.view_init(elev=20, azim=40)

    # Cutaway: only k3>=0 hemisphere for readability
    half = pts[pts[:, 2] >= 0]
    ax2.scatter(
        half[:, 0], half[:, 1], half[:, 2],
        c=plt.cm.copper(0.2 + 0.7 * ((half[:, 3] - L_lo) / (L_hi - L_lo))),
        s=28, alpha=0.95, edgecolors="none",
    )
    # Equatorial ring
    th = np.linspace(0, 2 * np.pi, 200)
    for R in (L_lo, L_hi):
        ax2.plot(R * np.cos(th), R * np.sin(th), 0 * th, color=STEEL, lw=1.2, alpha=0.7)
    ax2.set_title("Cutaway — same shell from above\nthis is the \"ring\" in frequency space", color=INK)
    ax2.set_xlabel(r"$k_1$")
    ax2.set_ylabel(r"$k_2$")
    ax2.set_zlabel(r"$k_3$")
    ax2.set_box_aspect((1, 1, 1))
    ax2.view_init(elev=55, azim=-60)

    fig.suptitle(
        "Frequency-space geometry — the hardware ball / shell that Ring assumes",
        color=INK, fontsize=13, fontweight="bold",
    )
    fig.text(
        0.5, 0.02,
        r"Band-limit / shell support $|k|\sim L$ is the structural hypothesis. Spatial twist bounds follow from it.",
        ha="center", color=MUTED, fontsize=9,
    )
    save(fig, "ring-geom-3d-fourier-shell.png")
    plt.close(fig)


def render_3d_direction_ribbons() -> None:
    """Trace short integral curves of ξ inside E_c — geometric ribbons of direction."""
    omega, x = synthetic_omega(L=5, ngrid=48, seed=3)
    mag, Ec, _ = strong_mask(omega, c=0.5)
    N = mag.shape[0]
    dx = x[1] - x[0]
    # Interpolate ω on continuous coords via nearest for simplicity
    def omega_at(p):
        ijk = np.clip(np.rint(p / dx).astype(int) % N, 0, N - 1)
        return omega[:, ijk[0], ijk[1], ijk[2]]

    def in_Ec(p):
        ijk = np.clip(np.rint(p / dx).astype(int) % N, 0, N - 1)
        return Ec[ijk[0], ijk[1], ijk[2]]

    rng = np.random.default_rng(5)
    seeds_idx = np.argwhere(Ec)
    if len(seeds_idx) > 60:
        seeds_idx = seeds_idx[rng.choice(len(seeds_idx), size=60, replace=False)]
    seeds = x[seeds_idx]

    fig = plt.figure(figsize=(11.5, 6.2), facecolor=MIST)
    ax = fig.add_subplot(111, projection="3d", facecolor=MIST)

    # Background faint strong-set dust
    dust = seeds_idx
    if len(np.argwhere(Ec)) > 1200:
        dust = np.argwhere(Ec)[rng.choice(len(np.argwhere(Ec)), 1200, replace=False)]
    else:
        dust = np.argwhere(Ec)
    pd = x[dust]
    ax.scatter(pd[:, 0], pd[:, 1], pd[:, 2], c="#9aa8b4", s=3, alpha=0.25, depthshade=False)

    for s in seeds:
        path = [s.copy()]
        p = s.astype(float).copy()
        for _ in range(28):
            w = omega_at(p)
            n = np.linalg.norm(w)
            if n < 1e-10 or not in_Ec(p):
                break
            p = (p + 0.22 * w / n) % (2 * np.pi)
            path.append(p.copy())
        path = np.array(path)
        if len(path) < 4:
            continue
        ax.plot(path[:, 0], path[:, 1], path[:, 2], color=COPPER, lw=1.35, alpha=0.9)

    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(0, 2 * np.pi)
    ax.set_zlim(0, 2 * np.pi)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_zlabel(r"$z$")
    ax.view_init(elev=22, azim=48)
    ax.set_title(
        r"3D direction ribbons — integral curves of $\xi$ inside $E_c$"
        + "\n"
        + "How aligned the spin direction is through the strong region",
        color=INK, fontweight="bold", pad=12,
    )
    fig.text(
        0.5, 0.02,
        "Ring says these curves cannot kink too sharply when the field is band-limited — twist rate has a ceiling.",
        ha="center", color=MUTED, fontsize=9,
    )
    save(fig, "ring-geom-3d-direction-ribbons.png")
    plt.close(fig)


def render_2d3d_combo_poster() -> None:
    """One poster: 2D slice + 3D cloud side by side for quick reading."""
    omega, x = synthetic_omega(L=5, ngrid=52, seed=12)
    mag, Ec, _ = strong_mask(omega, c=0.48)
    iz = mag.shape[2] // 2
    m2 = mag[:, :, iz]
    e2 = Ec[:, :, iz]
    eps = 1e-12
    xi2 = omega[:, :, :, iz] / (m2[None] + eps)

    fig = plt.figure(figsize=(13.0, 6.0), facecolor=MIST)
    ax2 = fig.add_subplot(121, facecolor=FOG)
    ax3 = fig.add_subplot(122, projection="3d", facecolor=MIST)

    extent = [0, 2 * np.pi, 0, 2 * np.pi]
    ax2.imshow(m2.T, origin="lower", extent=extent, cmap=MAG_CMAP, aspect="equal")
    ax2.contour(x, x, e2.T.astype(float), levels=[0.5], colors=["white"], linewidths=1.8)
    step = 3
    Xs, Ys = np.meshgrid(x[::step], x[::step], indexing="ij")
    U = xi2[0, ::step, ::step]
    V = xi2[1, ::step, ::step]
    mask = e2[::step, ::step]
    ax2.quiver(Xs[mask], Ys[mask], U[mask], V[mask], color=COPPER, scale=17, width=0.0045, pivot="mid")
    ax2.set_title("2D — one torus cut\n" + r"$|\omega|$ + $\xi$ on $E_c$", color=INK, fontweight="bold")
    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$y$")

    idx = np.argwhere(Ec)
    rng = np.random.default_rng(1)
    if len(idx) > 2800:
        idx = idx[rng.choice(len(idx), 2800, replace=False)]
    pts = x[idx]
    vals = mag[idx[:, 0], idx[:, 1], idx[:, 2]]
    ax3.scatter(pts[:, 0], pts[:, 1], pts[:, 2], c=vals, cmap=MAG_CMAP, s=7, alpha=0.8, edgecolors="none")
    # Draw the slice plane as a translucent square at z=π
    xx = np.linspace(0, 2 * np.pi, 2)
    yy = np.linspace(0, 2 * np.pi, 2)
    XX, YY = np.meshgrid(xx, yy)
    ZZ = np.full_like(XX, x[iz])
    ax3.plot_surface(XX, YY, ZZ, color=COPPER, alpha=0.18, shade=False)
    ax3.set_title("3D — full strong set\ncopper plane = the 2D cut", color=INK, fontweight="bold")
    ax3.set_xlabel(r"$x$")
    ax3.set_ylabel(r"$y$")
    ax3.set_zlabel(r"$z$")
    ax3.set_xlim(0, 2 * np.pi)
    ax3.set_ylim(0, 2 * np.pi)
    ax3.set_zlim(0, 2 * np.pi)
    ax3.view_init(elev=18, azim=32)

    fig.suptitle(
        "Same geometry, two views — Ring lives in physical space as a strong-set + direction field",
        color=INK, fontsize=12.5, fontweight="bold",
    )
    fig.text(
        0.5, 0.01,
        "Left is a cut through the right. The lemma is about this spatial picture under a frequency cutoff.",
        ha="center", color=MUTED, fontsize=9,
    )
    save(fig, "ring-geom-2d3d-combo.png")
    plt.close(fig)


def main() -> None:
    ensure_dirs()
    render_2d_slice_gallery()
    render_2d_twist_closeup()
    render_3d_strong_set_cloud()
    render_3d_fourier_shell()
    render_3d_direction_ribbons()
    render_2d3d_combo_poster()


if __name__ == "__main__":
    main()
