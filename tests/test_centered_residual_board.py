"""Residual board: one region; width arithmetic sits; B_prim not invented.

NS not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import centered_width_crossover as width  # noqa: E402


def test_width_conventions_and_v_n_crosses():
    payload = width.run()
    assert payload["ns_solved"] is False
    assert payload["crossover_stamped"] is False
    assert payload["B_prim_constructed"] is False
    assert payload["loop_families_on_this_tree"] is False
    assert payload["all_conventions_match"] is True
    assert payload["v_n_crosses_to_broad"] is True
    note = payload["note_triad"]
    assert note["region"] == "NARROW"
    assert abs(note["r"] - note["r_from_sigma_over_Lambda"]) < 1e-12
    vn = {row["n"]: row for row in payload["growing_layer"]}
    assert vn[1]["region"] == "NARROW"
    assert vn[8]["region"] == "BROAD"


def test_board_is_one_residual_and_does_not_claim_ns():
    page = (ROOT / "docs" / "ns-recovery" / "CENTERED-RESIDUAL-BOARD.md").read_text()
    assert page.startswith("# Centered residual board")
    assert "NARROW HETEROCHIRAL LAST MILE" in page
    assert "LOW-TAIL CAPACITY" in page
    assert "LOW-FREQUENCY TAIL" in page or "low-frequency tail" in page
    assert "not on this tree" in page
    assert "Not a stamped decision theorem" in page or "not a derived decision" in page
    assert "NS is solved" not in page
    assert "Clay is solved" not in page
    data = json.loads((ROOT / "results" / "centered_width_crossover.json").read_text())
    assert data["ns_solved"] is False
    assert data["B_prim_constructed"] is False
    assert data["crossover_stamped"] is False
