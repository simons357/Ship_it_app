"""Fourier-triangle reconstruction: identities, loss point, first missing implication.

NS not solved.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "ns-recovery" / "FOURIER-TRIANGLE-GEOMETRY.md"


def test_triangle_page_separates_buckets_and_names_the_gap():
    text = PAGE.read_text()
    assert text.startswith("# Fourier-triangle geometry — reconstruction")
    assert "## I. Exact identities" in text
    assert "## II. Numerical observations (not identities)" in text
    assert "## III. Illustrative motion (not the PDE)" in text
    assert r"I_3(p,q;k)" in text
    assert "Equal-length cancellation" in text
    assert "Unequal-length defect" in text
    assert "Where the geometry is lost" in text
    assert "First missing implication" in text
    assert r"K\in L^1_{\mathrm{loc}}" in text
    assert "Do not glue." in text
    assert "No new estimate is written here." in text
    assert "NS is solved" not in text
    assert "Clay is solved" not in text
