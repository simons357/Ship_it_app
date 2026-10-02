"""25 Sep working record: nu restored; sourcing flags stay down.

NS not solved.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "ns-recovery" / "WORKING-RECORD-2026-09-25.md"


def test_working_record_fixes_nu_and_flags_missing_sources():
    text = PAGE.read_text()
    assert text.startswith("# Working record — 25 September 2026")
    assert r"(\log\Lambda)'=\frac{2}{Y}(T_c-\nu D_s)" in text
    assert r"\int\frac{\alpha^2\chi^2\kappa X}{\nu}\,dt<\infty" in text
    assert "I3_WEIGHTED_TARGET_2026-09-20.md" in text
    assert "not proved internally" in text
    assert "NEUTRAL" in text
    assert "cube-field" in text
    assert "54/46" in text
    assert "A8-R construction" in text
    assert "Q4-0" in text
    assert "Do not run" in text or "not run" in text
    assert "NS is solved" not in text
    assert "Clay" not in text


def test_named_source_files_are_still_absent():
    names = (
        "I3_WEIGHTED_TARGET_2026-09-20.md",
        "I3_WEIGHTED_TARGET.md",
    )
    for name in names:
        hits = list(ROOT.rglob(name))
        assert hits == [], hits
