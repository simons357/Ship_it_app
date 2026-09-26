"""2026-09-10 Lemma-star shape-form lock: formulas sit; page does not prove star.

NS not solved. Unrestricted star is already dead on v_n on this book.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "math" / "ns_attacks" / "LEMMA_STAR_SHAPE_FORM.md"
CANON = ROOT / "docs" / "math" / "ns_attacks" / "LEMMA_STAR_CANONICAL.md"


def test_shape_form_locks_formulas_and_does_not_prove_star():
    text = PAGE.read_text()
    assert text.startswith("# Lemma★ — canonical shape form (exact lock)")
    assert "cursor/ns-five-lane-lemma-star-1390" in text
    assert "locks formulas" in text
    assert r"\mathcal{R}_\star(v)" in text
    assert r"(T_c(v)_+)^2" in text
    assert r"C_{\mathrm{geom}}" in text
    assert r"C_0(\theta)=C_{\mathrm{geom}}/(4\theta)" in text
    assert r"\Lambda'=\frac{2}{X}\bigl(T_c-\nu\mathcal{D}_s\bigr)" in text
    assert "Do **not** replace" in text or "Do not replace" in text
    assert "one Fourier shell" in text and r"T_c>0" in text
    assert "vacuous — not a kill" in text
    assert "The kill lane is closed" in text
    assert "NS is solved" not in text
    assert "does not prove" in text
    # this-book status is separated from the 10 Sep lock
    assert "growing-layer" in text or "v_n" in text
    canon = CANON.read_text()
    assert "FALSE" in canon
    assert "growing-layer" in canon or "v_n" in canon
    assert "NS is not solved" in canon
