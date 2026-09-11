"""Estimate audit stays a filter. Not a close."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph, run  # noqa: E402

PAGE = ROOT / "docs" / "ESTIMATE-AUDIT.md"


class EstimateAuditTests(unittest.TestCase):
    def test_page_is_a_filter(self):
        text = PAGE.read_text()
        self.assertIn("**Not a proof. NS not solved.", text)
        self.assertIn("axisymmetric with swirl", text)
        self.assertIn("T_{j\\leftarrow j}", text)
        self.assertIn("KEEP may enter", text)
        self.assertIn("DISCARD does not enter", text)
        self.assertIn("PARK lives in another stack", text)
        self.assertIn("Never bound that term by a", text)
        self.assertIn("copy of the time derivative", text)
        self.assertIn("Attack-6", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("falsifier-of-record", text)
        self.assertIn("The axisymmetric shell estimate is", text)
        self.assertIn("TJJ-ESTIMATE.md", text)
        self.assertIn("EAud_tjj_young", text)

    def test_probe_scores(self):
        payload = run()
        rows = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(rows["EAud_filter_seated"]["verdict"], "pass")
        self.assertEqual(rows["EAud_class_named"]["verdict"], "pass")
        self.assertEqual(rows["EAud_lambda_bookkeeping"]["verdict"], "pass")
        self.assertEqual(rows["EAud_remainder_named"]["verdict"], "pass")
        self.assertEqual(rows["EAud_tau_seated"]["verdict"], "pass")
        self.assertEqual(rows["EAud_omega_star_seated"]["verdict"], "pass")
        self.assertEqual(rows["EAud_tjj_young"]["verdict"], "fail")
        self.assertEqual(rows["EAud_door1_closed"]["verdict"], "fail")
        self.assertEqual(rows["EAud_door3_closed"]["verdict"], "fail")
        self.assertEqual(rows["EAud_discard_in_claim"]["verdict"], "fail")
        self.assertEqual(rows["EAud_ns_solved"]["verdict"], "fail")
        self.assertEqual(payload["domain_verdict"], "open")
        self.assertTrue(payload["meta"]["estimate_open"])
        self.assertTrue(payload["meta"]["lemma_star_open"])
        self.assertFalse(payload["meta"]["h1_started"])
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertTrue(payload["discard_self_check"]["allowed_in_estimate"])

    def test_discard_classifier(self):
        clean = classify_paragraph(
            "Axisymmetric-with-swirl NS; remainder T_{j<-j}; [no extra field]."
        )
        self.assertTrue(clean["allowed_in_estimate"])
        bad = classify_paragraph("Clay is solved by coherence viscosity and gematria.")
        self.assertFalse(bad["allowed_in_estimate"])
        self.assertIn("clay is solved", bad["discard_hits"])
        self.assertIn("coherence viscosity", bad["discard_hits"])
        self.assertIn("gematria", bad["discard_hits"])


if __name__ == "__main__":
    unittest.main()
