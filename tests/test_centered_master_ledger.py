"""Centered master ledger: DA-NS-2 open; W_K sits; reset jump not filled.

NS not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import centered_wk_identity as wk  # noqa: E402


def test_wk_identity_and_reset_not_filled():
    payload = wk.run()
    assert payload["ns_solved"] is False
    assert payload["reset_jump_completed"] is False
    assert payload["all_identities_ok"] is True
    note = payload["note_triad"]
    assert abs(note["Lambda"] - 1.4) < 1e-12
    assert note["identities_ok"] is True


def test_ledger_separates_exact_open_killed_and_truncation():
    page = (ROOT / "docs" / "ns-recovery" / "CENTERED-MASTER-LEDGER.md").read_text()
    assert page.startswith("# Centered master ledger — SAG / JGC consolidation")
    assert "DA-NS-2" in page
    assert "**OPEN**" in page
    assert "Charge-only coercivity" in page
    assert "TRUNCATED" in page
    assert "reset jump" in page.lower() or "Reset jump" in page
    assert "NS is solved" not in page
    assert "Clay is solved" not in page
    assert "Not a closure theorem" in page
    data = json.loads((ROOT / "results" / "centered_wk_identity.json").read_text())
    assert data["ns_solved"] is False
    assert data["reset_jump_completed"] is False
    assert data["all_identities_ok"] is True
