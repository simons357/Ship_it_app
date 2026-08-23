#!/usr/bin/env python3
"""Integrity tests for archived SFE / UHF / DHFA / HB materials.

These tests keep the historical inventory honest. They are not part of
the live Domain Architect v1.0 mathematics.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np

from domain_architect.index_audit import audit_canonical_index
from domain_architect.registry import EquationRegistry
from domain_architect.historical import CANONICAL_SFE_STATUS
from domain_architect.schema import ConflictRelation
from domain_architect.selectors import run_selector_lab


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


if __name__ == "__main__":
    unittest.main()
