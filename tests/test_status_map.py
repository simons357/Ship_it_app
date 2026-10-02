"""Desk status map: open work, instruments, no scoreboard.

NS not solved.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "docs" / "STATUS-MAP.md"


def test_status_map_is_on_the_record():
    text = MAP.read_text()
    assert text.startswith("# Status map — 16 Sep 2026")
    assert "Open work. Instruments. No scoreboard." in text
    assert "## Live" in text
    assert "## Holding" in text
    assert "## Cold" in text
    assert "## Street" in text
    assert "## Standing rule" in text
    assert "NS lemmas:" in text
    assert "negative results kept on the record" in text
    assert "as instruments, not claims" in text
    assert "No Clay / prize / QED / “solved” language in public output." in text
    assert "NS is solved" not in text
    assert "Clay is solved" not in text
    assert "almost proved" not in text.lower()
