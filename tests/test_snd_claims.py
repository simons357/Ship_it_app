#!/usr/bin/env python3
"""Tests for SND-U / SND-C / Clay B inventory anatomizer."""

from __future__ import annotations

import unittest

from domain_architect.audit import audit_expression
from domain_architect.snd_claims import (
    anatomize_claim,
    assert_not_unconditional_regularity,
    inventory_status_map,
    load_inventory,
    refuse_unconditional_regularity_routing,
)


class TestSNDInventory(unittest.TestCase):
    def test_status_map_frozen(self):
        status = inventory_status_map()
        self.assertEqual(status["SND-U"], "open")
        self.assertEqual(status["SND-C"], "conditional")
        self.assertEqual(status["CLAY-B"], "not_resolved")

    def test_inventory_file_loads(self):
        inv = load_inventory()
        ids = {c["claim_id"] for c in inv["claims"]}
        self.assertEqual(
            ids,
            {
                "SND-U",
                "SND-C",
                "CLAY-B",
                "THEOREM-H-MISLABEL",
                "CSTAR-ARITHMETIC",
            },
        )


class TestRefusal(unittest.TestCase):
    def test_refuses_unconditional_regularity(self):
        audit = anatomize_claim(
            "We prove unconditional global regularity for 3D Navier-Stokes"
        )
        self.assertTrue(audit.refused)
        self.assertIsNone(audit.allowed_routing)
        self.assertTrue(any("unconditional regularity" in r.lower() for r in audit.refusal_reasons))

    def test_refuses_clay_b_resolved(self):
        result = refuse_unconditional_regularity_routing(
            "Clay Statement B resolved via Theorem H"
        )
        self.assertTrue(result["refused"])
        self.assertFalse(result["ok"])

    def test_assert_raises(self):
        with self.assertRaises(ValueError):
            assert_not_unconditional_regularity(
                "millennium prize solved by SND for all data proved"
            )

    def test_allows_snd_c_conditional_language(self):
        audit = anatomize_claim(
            "Theorem H proves SND-C under X<=M in the spread regime"
        )
        self.assertFalse(audit.refused)
        self.assertEqual(audit.allowed_routing, "SND-C_conditional_under_X_le_M")
        self.assertTrue(any(h.claim_id == "SND-C" for h in audit.hits))

    def test_snd_u_marked_open(self):
        audit = anatomize_claim("SND-U remains the open spectral non-dispersal law")
        self.assertFalse(audit.refused)
        self.assertEqual(audit.allowed_routing, "SND-U_hypothesis_open")
        hit = next(h for h in audit.hits if h.claim_id == "SND-U")
        self.assertEqual(hit.status, "open")


class TestAuditIntegration(unittest.TestCase):
    def test_audit_warns_on_unconditional_regularity_phrase(self):
        report = audit_expression(
            "unconditional global regularity claimed for classical NS"
        )
        blob = " ".join(report.warnings).lower()
        self.assertIn("refuse", blob)


if __name__ == "__main__":
    unittest.main()
