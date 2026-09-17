"""Plots regenerate from committed JSON. Finite samples, not a bound."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import plot_k_sweeps as plots  # noqa: E402


def test_plots_write_from_committed_json():
    p1 = plots.plot_9b()
    p2 = plots.plot_9d_top()
    assert p1.is_file() and p1.stat().st_size > 1000
    assert p2.is_file() and p2.stat().st_size > 1000
    root = Path(__file__).resolve().parents[1]
    assert (root / "results/ns_five_lane_2026-09-10/attack9b_exact_shell/attack9b.json").is_file()
