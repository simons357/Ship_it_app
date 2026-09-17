"""Snapshot of the complete NS/SND Final Status Report (Markdown).

Ingest only. This book does not adopt that desk's leftover numbering.
NS not solved.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "docs" / "ns-snd-final-status"
STATUS = PACK / "NS-STATUS.md"

REQUIRED = (
    "NS-STATUS.md",
    "REPORT-AUDIT.md",
    "UNAUG-NS-UNIFIED.md",
    "MASTER-PLAN.md",
    "TINY.txt",
    "YES-NO-OPEN.md",
    "C10-CHAIN.md",
    "CENTERED-DRIFT.md",
    "SND-INSTRUMENT.md",
    "LEMMA-STAR.md",
    "ATTACK-9D-FULL-SUPPORT-BOUND.md",
    "SND-H-REVIEW.md",
    "SND-H-REPAIR.md",
    "SND-H-PLAIN.md",
    "SND-TO-REGULARITY.md",
    "OPENAI-NS-CLAIM.md",
    "ISSUES-SHEET.md",
    "LATEST.md",
    "README.md",
)


def test_complete_pack_present():
    for name in REQUIRED:
        path = PACK / name
        assert path.is_file(), name
        assert path.stat().st_size > 200, name


def test_status_title_and_lock():
    text = STATUS.read_text()
    assert text.startswith("# Final NS / SND status — 16 September 2026")
    assert "Ordinary Navier–Stokes is not solved." in text
    assert "Unrestricted" in text
    assert "killed" in text.lower()
    assert "CLAIMED" in text
    assert "Do not write “9D is claimed.”" in text or 'Do not write "9D is claimed."' in text
    assert "instrument" in text.lower()
    assert "NS not solved." in text
    assert "NS is solved" not in text
    assert "Clay is solved" not in text


def test_status_links_resolve_in_pack():
    text = STATUS.read_text()
    for name in (
        "REPORT-AUDIT.md",
        "MASTER-PLAN.md",
        "UNAUG-NS-UNIFIED.md",
        "TINY.txt",
        "YES-NO-OPEN.md",
        "C10-CHAIN.md",
        "CENTERED-DRIFT.md",
        "SND-INSTRUMENT.md",
        "LEMMA-STAR.md",
        "ATTACK-9D-FULL-SUPPORT-BOUND.md",
    ):
        assert f"]({name})" in text, name
        assert (PACK / name).is_file(), name


def test_unified_page_does_not_close():
    text = (PACK / "UNAUG-NS-UNIFIED.md").read_text()
    flat = " ".join(text.replace("*", "").split()).lower()
    assert "Yes to score" in text
    assert "No to close" in text
    assert "withdrawn" in text.lower()
    assert "KILLED" in text
    assert "CLAIMED" in text
    assert "NS is solved" not in text
    assert "almost proved" not in flat
    assert "Exact-shell 9D — claimed" not in text
