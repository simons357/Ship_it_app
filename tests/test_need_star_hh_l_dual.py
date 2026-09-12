"""Need★: gap-cancel sits; signed dual MISSING; not a theorem."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph  # noqa: E402
from need_star_hh_l_dual import classify_need_star_claim, run  # noqa: E402

PAGE = ROOT / "docs" / "NEED-STAR-HH-L-DUAL.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
SHEET = ROOT / "docs" / "ISSUES-SHEET.md"


class NeedStarHHLDualTests(unittest.TestCase):
    def test_page_names_the_missing_signed_dual(self):
        text = PAGE.read_text()
        self.assertIn("quantity is the signed dual", text)
        self.assertIn("MISSING", text)
        self.assertIn("gap-cancel", text)
        self.assertIn("HH→L", text)
        self.assertIn("\\mathrm{Im}", text)
        self.assertIn("16s", text)
        self.assertIn("secondary", text)
        self.assertIn("Soft X silent", text)
        self.assertIn("Lemma★", text)
        self.assertIn("OPEN", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("almost proved", text.lower())

    def test_identity_sits_and_machine_refuses_close(self):
        summary = run(seed=1390)
        self.assertTrue(summary["gap_cancel_identity"])
        self.assertGreaterEqual(summary["n_fields"], 1)
        self.assertEqual(summary["need_star"], "SIGNED_DUAL_MISSING")
        self.assertIs(summary["accepted_as_close"], False)
        self.assertIs(summary["ns_solved"], False)
        self.assertEqual(summary["lemma_star"], "OPEN")
        self.assertEqual(summary["soft_x"], "silent")
        stretching = [r for r in summary["rows"] if abs(r["T_beta"]) > 1e-12]
        self.assertGreaterEqual(len(stretching), 1)
        for row in summary["rows"]:
            self.assertLess(row["gap_cancel_abs"], 1e-9)
            self.assertLess(abs(row["T_alpha_plus_T_beta"]), 1e-9)
            if row["signed_over_CS"] is not None:
                self.assertLessEqual(row["signed_over_CS"], 1.0 + 1e-9)
            if row["Tc"] > 0 and row["R_star"] is not None:
                self.assertAlmostEqual(
                    row["R_star"], row["R_star_after_gap_cancel"], places=8
                )

    def test_fake_close_is_refused(self):
        claim = classify_need_star_claim("Need★ is proved. NS is solved.")
        self.assertFalse(claim["accepted_as_close"])
        self.assertGreaterEqual(len(claim["refuse_hits"]), 1)
        self.assertEqual(claim["signed_dual"], "MISSING")

    def test_pointers_and_filter(self):
        self.assertIn("NEED-STAR-HH-L-DUAL.md", TAPE.read_text())
        self.assertIn("NEED-STAR-HH-L-DUAL.md", SHEET.read_text())
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
