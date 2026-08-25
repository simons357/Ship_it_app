#!/usr/bin/env python3
"""Integrity tests for archived SFE / UHF / DHFA / HB materials.

These tests keep the historical inventory honest. They are not part of
the live Domain Architect v1.0 mathematics.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import numpy as np

from domain_architect.index_audit import audit_canonical_index
from domain_architect.registry import EquationRegistry
from domain_architect.historical import CANONICAL_SFE_STATUS
from domain_architect.schema import ConflictRelation
from domain_architect.selectors import run_selector_lab

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_PRIME_FIELD = ROOT / "docs" / "archive" / "prime-field-2026-08-25"
LIVE_ROOT = ROOT / "domain_architect"

PRIME_FIELD_FILES = {
    "PRIME_FIELD_MASTER_WHITEPAPER.md": (
        "2e2c7a446c2b6c1024ee8649e1aa0675f282e7de23123a4c9d79b12e102978e2",
        21572,
    ),
    "Arithmetic_Tests_of_the_Simons_Field_Equation.pdf": (
        "d486bdb286b234a798d46c07b0e9415b9ffa45f1d6b3c8a2a502a431c6f02191",
        199772,
    ),
    "SFE_RH_Probes_Preprint.docx": (
        "6d414dee5ee26f8dd011496a6d1e216e633643be1697ac212fd49e380c151ef6",
        22060,
    ),
    "Simons_Prime_Resonance_Law.pdf": (
        "7aa187c62f20190e012e4c7f7209c69abb7b8aa112755e5d8aeaa45a6cc06264",
        403089,
    ),
    "Simons_Prime_Resonance_Law.docx": (
        "8da0163a58eee92157c0f5896fb8d47e4b9ffd63873d749eb40f663a20043b38",
        271661,
    ),
    "Prime_order_Kepler.pdf": (
        "f2da5ae51db4a539bd55c3706ce65b3479c887e485dcb08bb8bf8832245ef02c",
        403012,
    ),
    "Cosmic_Scale_Paper_Clean.pdf": (
        "6453503a07f13f19775a2e7755e85b8f4bf10d3cfb4253d34ce7bac3634dac3d",
        210182,
    ),
    "Simons_Prime_Harmony_Law.pdf": (
        "96f836c859dd8e6d2b850243177deb3bf66e33c18459b3a5e1e265e1bf764280",
        83155,
    ),
    "SFE_formal_reference.pdf": (
        "c44488294e00de06099e8fc729d7662400a45c3beece7dea3b587e3c42c97d77",
        204066,
    ),
    "prime_indexed_order_accross_domains.docx": (
        "e178b0ea1f1c456cd0527182e18a27e8c51b24ba0137fa385c00a579fad6ce49",
        23219,
    ),
    "planet_periods_full.csv": (
        "fb497e3fb0164dea9cd3c6666de71b47751eebec4f81ceadcd93812fb0d24c6c",
        179026,
    ),
    "missing_planets_analysis_3619_candidates.csv": (
        "8cac6ccfdb05c4aa34e6ffe18f0c42a866cbf27b6b7cf43ee826ee1f6b8fbde9",
        122426,
    ),
    "exoplanets_base44.csv": (
        "09868306da16747cb1a65830b90055586910ade1077f278f19afc0795155a490",
        116313,
    ),
    "prime_resonance_pro_exoplanet_analyzer_full_rebuild.jsx": (
        "1732dd0a4859428267e4bfe64f887208ee1f6fb7c675f8a05c0caac70cd47534",
        26928,
    ),
    "prime_field_coherence.py": (
        "62728c7436fa7bd3093ed8a18da155eee22fd6bbe4121378aaf5df4273a9decf",
        23513,
    ),
}


class TestHistoricalInventory(unittest.TestCase):
    def test_incompatible_sfe_candidates_are_preserved(self):
        registry = EquationRegistry.load_default()
        self.assertIn("SFE-H001", registry.equations)
        self.assertIn("SFE-H002", registry.equations)
        status = registry.refuse_hybrid("SFE-H001", "SFE-H002")
        self.assertEqual(status, "preserved_both_flagged_conflict")
        pairs = {frozenset({c.left_id, c.right_id}): c for c in registry.conflicts}
        self.assertIn(frozenset({"SFE-H001", "SFE-H002"}), pairs)
        self.assertEqual(
            pairs[frozenset({"SFE-H001", "SFE-H002"})].relation,
            ConflictRelation.INCOMPATIBLE.value,
        )
        e1 = registry.equations["SFE-H001"].original_expression
        e2 = registry.equations["SFE-H002"].original_expression
        self.assertNotEqual(e1, e2)
        self.assertEqual(registry.canonical_sfe_status(), CANONICAL_SFE_STATUS)
        self.assertIn("archived", CANONICAL_SFE_STATUS.lower())

    def test_json_loads(self):
        root = Path(__file__).resolve().parents[1] / "data" / "domain_architect"
        eqs = json.loads((root / "historical_equations.json").read_text())
        cfs = json.loads((root / "conflicts.json").read_text())
        self.assertGreaterEqual(len(eqs), 16)
        self.assertTrue(any(e["equation_id"] == "SFE-H001" for e in eqs))
        self.assertTrue(any(c["relation"] == "INCOMPATIBLE" for c in cfs))


class TestHistoricalPrimeLab(unittest.TestCase):
    def test_degenerate_spectrum_warns_basis_dependence(self):
        eigenvalues = np.array([1.0, 1.0, 4.0, 9.0])
        audit = audit_canonical_index(
            eigenvalues,
            selector_acts_on="individual_basis_vectors",
        )
        self.assertTrue(audit.degenerate)
        self.assertTrue(audit.basis_dependent)
        self.assertFalse(audit.valid_for_physical_prime_test)

    def test_negative_prime_result_is_stored(self):
        n = 32
        field = np.zeros(n)
        field[[0, 1, 4, 6, 8, 9, 10, 12]] = 1.0
        lab = run_selector_lab(field, budget=4, random_seeds=(1, 2, 3), include_optimized=True)
        self.assertTrue(lab.negative)
        registry = EquationRegistry()
        rec = registry.record_null(
            kind="prime selector failed",
            statement=lab.conclusion,
            evidence=str(lab.metrics),
            source="historical archive Test H",
        )
        self.assertEqual(registry.prominent_nulls()[0].null_id, rec.null_id)


class TestPrimeFieldArchiveIntake(unittest.TestCase):
    """SFE / prime / cosmic / exoplanet drop stays historical, not live DA."""

    def test_hash_locks_and_no_duplicate_copies(self):
        self.assertTrue(ARCHIVE_PRIME_FIELD.is_dir(), ARCHIVE_PRIME_FIELD)
        for name, (digest, size) in PRIME_FIELD_FILES.items():
            path = ARCHIVE_PRIME_FIELD / name
            self.assertTrue(path.is_file(), path)
            raw = path.read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), digest, name)
            self.assertEqual(len(raw), size, name)
        resonance = (ARCHIVE_PRIME_FIELD / "Simons_Prime_Resonance_Law.pdf").read_bytes()
        kepler = (ARCHIVE_PRIME_FIELD / "Prime_order_Kepler.pdf").read_bytes()
        self.assertNotEqual(resonance, kepler)
        self.assertFalse((ARCHIVE_PRIME_FIELD / "Cosmic_Scale_Paper_Clean_ed05.pdf").is_file())
        self.assertFalse(
            (ARCHIVE_PRIME_FIELD / "Simons_Prime_Resonance_Law_2.pdf").is_file()
        )
        self.assertFalse((LIVE_ROOT / "prime_field_coherence.py").is_file())

    def test_readme_is_historical_not_canonical_sfe(self):
        note = (ARCHIVE_PRIME_FIELD / "README.md").read_text(encoding="utf-8")
        index = (ROOT / "docs" / "archive" / "README.md").read_text(encoding="utf-8")
        self.assertIn("archive only", note.lower())
        self.assertIn("Not live Domain Architect", note)
        self.assertIn("Do not make SFE canonical", note)
        self.assertIn("NOT CLAIMED", note)
        self.assertIn("Do not stamp DA-VC-01", note)
        self.assertNotIn("DA-VC-01 PASS", note)
        self.assertIn("prime_field_coherence.py", note)
        self.assertIn("Not live DA", note)
        self.assertIn("duplicate", note.lower())
        self.assertIn("PhiRenorm_TrackB_May16", note)
        self.assertIn("prime-field-2026-08-25/", index)
        self.assertIn("not live DA", index)
        self.assertIn("not FIXED.tex", index)
        self.assertIn("sfe-hb/", index)
        self.assertFalse(
            (ROOT / "docs" / "papers" / "ns-snd" / "Paper2_NS_Regularity_SND_FIXED.tex").is_file()
        )
        self.assertTrue(
            (ROOT / "docs" / "archive" / "sfe-hb" / "SPECTRAL_UNIFICATION_PAPER.tex").is_file()
        )
        note = (
            ROOT / "docs" / "archive" / "sfe-hb" / "SPECTRAL_UNIFICATION_PAPER.md"
        )
        self.assertTrue(note.is_file(), note)
        self.assertIn("NOT CLAIMED", note.read_text(encoding="utf-8"))
        self.assertFalse(
            (ROOT / "docs" / "archive" / "sfe-hb" / "SPECTRAL_UNIFICATION_PAPER.MISSING.md").is_file()
        )
        overleaf = (
            ROOT / "docs" / "archive" / "overleaf-2026-04" / "OVERLEAF-EXPORTS.MISSING.md"
        )
        self.assertTrue(overleaf.is_file(), overleaf)
        self.assertIn("not received", overleaf.read_text(encoding="utf-8").lower())
        self.assertIn("overleaf-2026-04/", index)
        self.assertIn("CLAY_FINAL", index)
        self.assertFalse((LIVE_ROOT / "clay_final.py").is_file())
        self.assertFalse((LIVE_ROOT / "serpent_final.py").is_file())


class TestUhsaSessionDumpIsHistorical(unittest.TestCase):
    def test_uhsa_synthesis_stays_under_archive_sfe_hb(self):
        path = (
            ROOT
            / "docs"
            / "archive"
            / "sfe-hb"
            / "Unified_Harmonic_Spectral_Architecture_Session_Master_Synthesis_2026-08-19.md"
        )
        self.assertTrue(path.is_file(), path)
        text = path.read_text(encoding="utf-8")
        self.assertIn("Historical session synthesis only", text)
        self.assertIn("Not live Domain Architect", text)
        self.assertIn("NOT CLAIMED", text)
        self.assertFalse((LIVE_ROOT / "d_master.py").is_file())
        self.assertFalse((LIVE_ROOT / "c_master.py").is_file())


class TestEquationExplorerIsHistorical(unittest.TestCase):
    def test_explorer_stays_under_archive_sfe_hb(self):
        path = (
            ROOT
            / "docs"
            / "archive"
            / "sfe-hb"
            / "equation_explorer_simons_field.py"
        )
        self.assertTrue(path.is_file(), path)
        text = path.read_text(encoding="utf-8")
        self.assertIn("Historical toy only", text)
        self.assertIn("Not live Domain Architect", text)
        self.assertIn("NOT CLAIMED", text)
        self.assertIn("does not depend on x", text)
        self.assertIn("def simons_field", text)
        self.assertFalse((LIVE_ROOT / "simons_field.py").is_file())
        self.assertFalse((LIVE_ROOT / "equation_explorer_simons_field.py").is_file())
        index = (ROOT / "docs" / "archive" / "README.md").read_text(encoding="utf-8")
        self.assertIn("equation_explorer_simons_field.py", index)


if __name__ == "__main__":
    unittest.main()
