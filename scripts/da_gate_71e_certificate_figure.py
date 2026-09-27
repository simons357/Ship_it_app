#!/usr/bin/env python3
"""Render the Gate 71E certificate figure (patch + exact residuals)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

import da_gate_71e_branch_eliminate as g

ROOT = Path(__file__).resolve().parents[1]


def main(out_path: Path | None = None) -> Path:
    modes = g.patch_modes()
    groups = g.repeated_outputs(modes)
    cert = g.exact_star_certificate()
    act = g.activity_from_z(g.Z_STAR_FLOAT, modes, groups)
    labels = [
        r"$p_{00}$",
        r"$p_{01}$",
        r"$p_{02}$",
        r"$p_{03}$",
        r"$p_{10}$",
        r"$p_{11}$",
        r"$p_{12}$",
        r"$p_{13}$",
    ]

    fig = plt.figure(figsize=(11.2, 5.6), facecolor="white")
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    row0 = modes[:4]
    row1 = modes[4:]
    ax.scatter(row0[:, 0], row0[:, 1], row0[:, 2], c="#1d4ed8", s=70, depthshade=False, label="row i=0")
    ax.scatter(row1[:, 0], row1[:, 1], row1[:, 2], c="#b45309", s=70, depthshade=False, label="row i=1")
    for i, p in enumerate(modes):
        ax.text(p[0] + 0.05, p[1] + 0.05, p[2] + 0.05, labels[i], fontsize=8)
    # affine edges
    for i in range(3):
        ax.plot(modes[[i, i + 1], 0], modes[[i, i + 1], 1], modes[[i, i + 1], 2], color="#1d4ed8", lw=1.2)
        ax.plot(modes[[i + 4, i + 5], 0], modes[[i + 4, i + 5], 1], modes[[i + 4, i + 5], 2], color="#b45309", lw=1.2)
    for i in range(4):
        ax.plot(modes[[i, i + 4], 0], modes[[i, i + 4], 1], modes[[i, i + 4], 2], color="#64748b", lw=0.8, ls="--")
    ax.set_xlabel(r"$k_1$")
    ax.set_ylabel(r"$k_2$")
    ax.set_zlabel(r"$k_3$")
    ax.set_title("2×4 additive patch")
    ax.legend(loc="upper left", fontsize=8)
    ax.view_init(elev=18, azim=-55)

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.axis("off")
    ztxt = r"$z^\star=(3,\ 3/2,\ 1,\ 3/4,\ 9/11,\ 15/19,\ 21/31,\ 27/47)$"
    lines = [
        "Gate 71E  —  Outcome B",
        "isolated / tuned active coherence",
        "",
        ztxt,
        "",
        f"equations: 11    variables: 8    repeated outputs: 7",
        f"triples exactly 0: {cert['all_triples_exactly_zero']}",
        f"dead pairs: {cert['dead_pairs']} / {cert['n_live_pairs']}",
        f"min |W|^2 = {cert['min_W_norm2']}",
        f"A(z*) = {cert['A']}   B(z*) = {cert['B']}   cubic = {cert['cubic']}",
        f"float max |collinearity| = {act['max_abs_collinearity']:.2e}",
        f"unit-U min |W| = {act['min_unit_pair_norm']:.4f}",
        "",
        "first-row harmonic satisfies the cubic for every t;",
        "only t = 3 completes. Not a continuum.",
        "",
        "NS not solved.  DA-NS-2 open.",
    ]
    ax2.text(
        0.02,
        0.98,
        "\n".join(lines),
        va="top",
        ha="left",
        family="monospace",
        fontsize=10,
        transform=ax2.transAxes,
    )
    ax2.set_title("exact rational certificate")
    fig.tight_layout()

    if out_path is None:
        out_path = ROOT / "results" / "da_gate_71e_certificate.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    path = main()
    print(path)
