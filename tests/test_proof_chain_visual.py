"""Tests for proof-chain visual generators and campaign copy rules."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "scripts" / "visual_journey" / "generate_proof_chain_figures.py"
JOURNEY = ROOT / "docs" / "ns-review" / "visual-journey"
CLEAN = ROOT / "docs" / "ns-review" / "PROOF-CHAIN-CLEAN.md"
MMD = JOURNEY / "proof-chain.mmd"
CAMPAIGN = ROOT / "docs" / "campaign"
PROOF_JOURNEY = CAMPAIGN / "PROOF-JOURNEY.md"
REPUTATION = CAMPAIGN / "REPUTATION-LOCK.md"
GLOSSARY = CAMPAIGN / "NOTATION-GLOSSARY.md"
JOURNEY_MMD = CAMPAIGN / "journey-chain.mmd"

FORBIDDEN_VERDICT = re.compile(
    r"\b(NS\s+(NOT\s+)?solved|Clay\s+(NOT\s+)?(closed|solved)|Millennium\s+closed|"
    r"prize\s+won|we\s+solved|not\s+solved)\b",
    re.IGNORECASE,
)
# Allow discussing open estimates / packaging without verdict stamps
FORBIDDEN_THEATER = re.compile(
    r"dream[-\s]?team|s[eé]ance|investigator\s+theater|LinkedIn\s+shade|"
    r"CRNA\s+in\s+Savannah|wife-test",
    re.IGNORECASE,
)


def _campaign_text_files() -> list[Path]:
    files = [
        CLEAN,
        JOURNEY / "README.md",
        JOURNEY / "CAPTIONS.md",
        ROOT / "docs" / "campaign" / "visual-journey" / "README.md",
        MMD,
        PROOF_JOURNEY,
        REPUTATION,
        GLOSSARY,
        JOURNEY_MMD,
    ]
    return [p for p in files if p.is_file()]


def test_generator_writes_figures(tmp_path: Path) -> None:
    out = tmp_path / "figures"
    proc = subprocess.run(
        [sys.executable, str(GEN), "--out", str(out), "--no-artifacts"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert (out / "proof-chain.png").is_file()
    assert (out / "proof-chain.svg").is_file()
    assert (out / "chain-status-card.png").is_file()
    # SVG should contain open-estimate language, not FAILED
    svg = (out / "proof-chain.svg").read_text(encoding="utf-8", errors="ignore")
    assert "open estimate" in svg.lower() or "open" in svg.lower()
    assert "FAILED" not in svg
    assert "not solved" not in svg.lower()


def test_mermaid_marks_open_neutrally() -> None:
    text = MMD.read_text(encoding="utf-8")
    assert "open estimate" in text
    assert "FAILED" not in text
    assert "Product bound" in text or "T_c" in text
    assert "Five-lane" in text or "five-lane" in text.lower()
    assert "Phi" in text or "Φ" in text or "renorm" in text.lower()


def test_clean_note_has_definitions() -> None:
    text = CLEAN.read_text(encoding="utf-8")
    for sym in ["T_c", "\\Lambda", "D_s", "E", "X", "Y", "Z", "mathcal{R}"]:
        assert sym in text or sym.replace("\\", "") in text
    assert "open estimate" in text.lower() or "Open estimate" in text
    # superior exposition: identity for Lambda'
    assert "Lambda'" in text or "\\Lambda'" in text


def test_campaign_pack_avoids_verdict_and_theater() -> None:
    for path in _campaign_text_files():
        text = path.read_text(encoding="utf-8")
        bad = FORBIDDEN_VERDICT.search(text)
        assert bad is None, f"{path}: verdict language {bad.group(0)!r}"
        theater = FORBIDDEN_THEATER.search(text)
        assert theater is None, f"{path}: theater language {theater.group(0)!r}"


def test_phi_relabel_visible_in_chain_docs() -> None:
    blob = "\n".join(p.read_text(encoding="utf-8") for p in _campaign_text_files())
    assert "1.3" in blob
    assert "u^r/r" in blob or "u^r" in blob or "ur/r" in blob or "u^{r}" in blob


def test_proof_journey_links_major_chapters() -> None:
    text = PROOF_JOURNEY.read_text(encoding="utf-8")
    for needle in [
        "Lemma",
        "five-lane",
        "Φ-renorm",
        "SND",
        "Q6",
        "Domain Architect",
        "22050974",
        "Archive",
        "barycenter",
        "PROOF-CHAIN-CLEAN",
    ]:
        assert needle in text, f"missing chapter cue {needle!r}"


def test_reputation_lock_barycenter_not_clay() -> None:
    text = REPUTATION.read_text(encoding="utf-8")
    assert "barycenter" in text.lower()
    assert "full evidence" in text.lower() or "clean chain" in text.lower()
    assert "locus" in text.lower()
    assert "billboard" in text.lower()


def test_glossary_has_core_symbols() -> None:
    text = GLOSSARY.read_text(encoding="utf-8")
    for sym in ["T_c", "D_s", "Lambda", "Phi", "SND"]:
        assert sym in text or sym.replace("Lambda", "\\Lambda") in text or "Λ" in text
