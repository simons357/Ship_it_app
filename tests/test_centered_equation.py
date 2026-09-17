"""Centered equation (3): exact identity, not an estimate.

NS not solved.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "ns-recovery" / "CENTERED-EQUATION.md"
FORMULAS = ROOT / "docs" / "math" / "ns_attacks" / "LEMMA_STAR_EXACT_FORMULAS.md"


def test_centered_equation_is_the_identity():
    text = PAGE.read_text()
    assert r"\Lambda'" in text
    assert r"-\frac{2\nu}{X}D_s" in text
    assert r"+\frac{2}{X}T_c" in text
    assert "That is the centered equation." in text
    assert "This is not (4)." in text
    assert "This is not Young." in text
    assert "This is not Need★." in text
    assert "NS is solved" not in text
    formulas = FORMULAS.read_text()
    assert r"\Lambda'" in formulas
    assert r"-\frac{2\nu}{X}D_s" in formulas
    assert r"+\frac{2}{X}T_c" in formulas
