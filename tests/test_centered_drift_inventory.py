"""Centered-drift inventory: identities sit, estimate open, K not integrable.

NS not solved.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "ns-recovery" / "CENTERED-DRIFT-INVENTORY.md"


def test_inventory_is_current_files_only():
    text = PAGE.read_text()
    flat = " ".join(text.split())
    assert text.startswith("# Centered spectral drift — current-files inventory")
    assert r"T_c=M-\Lambda N" in text
    assert "Open" in text
    assert "Never derived" in text
    assert "Ordinary NS is not solved" in text
    assert "NS is solved" not in text
    assert "Clay is solved" not in text
    assert "NoCancellation reconstruction: **never written.**" in text
    assert r"Do not put \(K(t)\)" in text
    assert "in the PDE." in flat
    assert "CENTERED-SPECTRAL-DRIFT-MASTER-REPORT.md" in text
