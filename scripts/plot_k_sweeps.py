#!/usr/bin/env python3
"""Regenerate K-by-pair plots from committed JSON. Does not rerun searches."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
NINE_B = ROOT / "results/ns_five_lane_2026-09-10/attack9b_exact_shell"
NINE_D = ROOT / "results/attack9d_growing_io"


def plot_9b() -> Path:
    data = json.loads((NINE_B / "attack9b.json").read_text())
    rows = data["per_pair"]
    order = np.argsort([r["K"] for r in rows])[::-1]
    labels = [f"{rows[i]['alpha']},{rows[i]['beta']}" for i in order]
    Ks = [rows[i]["K"] for i in order]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(range(len(Ks)), Ks, color="#2c5f6e")
    ax.set_xticks(range(len(Ks)))
    ax.set_xticklabels(labels, rotation=75, ha="right", fontsize=8)
    ax.set_ylabel(r"$K_{\alpha,\beta}$")
    ax.set_title("Aligned 9B exact-shell K (24 pairs, kmax=6). Finite sample, not a bound.")
    ax.axhline(16 / 9, color="#a33", linestyle="--", linewidth=1, label=r"$16/9$ (claimed 9D)")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    out = NINE_B / "K_by_ab_pair.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    return out


def plot_9d_top() -> Path:
    data = json.loads((NINE_D / "attack9d_growing_io.json").read_text())
    rows = [r for r in data["per_pair"] if r["K"] > 0]
    rows.sort(key=lambda r: r["K"], reverse=True)
    top = rows[:20]
    labels = [f"{r['alpha']},{r['beta']}" for r in top]
    Ks = [r["K"] for r in top]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(range(len(Ks)), Ks, color="#4a7c59")
    ax.set_xticks(range(len(Ks)))
    ax.set_xticklabels(labels, rotation=75, ha="right", fontsize=8)
    ax.set_ylabel(r"$K_{\alpha,\beta}$")
    ax.set_title("Natural 9D growing I/O: top 20 of 1632 pairs (kmax=5). Finite sample.")
    ax.axhline(16 / 9, color="#a33", linestyle="--", linewidth=1, label=r"$16/9$ (claimed 9D)")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    out = NINE_D / "K_top20.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    return out


def main() -> None:
    print(plot_9b())
    print(plot_9d_top())


if __name__ == "__main__":
    main()
