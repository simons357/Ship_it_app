"""H1 write: locked G; machine refuses a fake close; not a theorem."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph  # noqa: E402
from h1_machine import classify_h1_claim, kernel_exponent, run  # noqa: E402

PAGE = ROOT / "docs" / "H1-WRITE.md"
TINY = ROOT / "docs" / "TINY.txt"
SHEET = ROOT / "docs" / "ISSUES-SHEET.md"


class H1WriteTests(unittest.TestCase):
    def test_page_is_the_write_not_the_theorem(self):
        text = PAGE.read_text()
        flat = " ".join(text.split())
        self.assertIn("Unaugmented Navier–Stokes, one cylinder", text)
        self.assertIn("A_{\\mathrm{bad}}", text)
        self.assertIn("\\mathcal G(Q_r)", text)
        self.assertIn("OPEN", text)
        self.assertIn("This is the write. It is not proved", flat)
        self.assertIn("Hölder cut, spent once", text)
        self.assertIn("Do not start this write from ABC", text)
        self.assertNotIn("H1 is a theorem", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)

    def test_machine_scores(self):
        payload = run()
        rows = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(rows["H1w_first_sentence"]["verdict"], "pass")
        self.assertEqual(rows["H1w_G_locked"]["verdict"], "pass")
        self.assertEqual(rows["H1w_holder_once"]["verdict"], "pass")
        self.assertEqual(rows["H1w_p1_is_h1"]["verdict"], "fail")
        self.assertEqual(rows["H1w_p1loc_is_h1"]["verdict"], "fail")
        self.assertEqual(rows["H1w_pc_is_h1"]["verdict"], "fail")
        self.assertEqual(rows["H1w_cs_is_shape1"]["verdict"], "fail")
        self.assertEqual(rows["H1w_write_proved"]["verdict"], "fail")
        self.assertEqual(rows["H1w_abc_start"]["verdict"], "fail")
        self.assertEqual(rows["H1w_sup_G"]["verdict"], "open")
        self.assertEqual(payload["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["h1_proved"])
        self.assertEqual(kernel_exponent("good"), -2.5)
        self.assertEqual(kernel_exponent("bad"), -3.0)

    def test_machine_refuses_fake_closes(self):
        fake = classify_h1_claim("H1 is proved. P1 is H1. NS is solved.")
        self.assertFalse(fake["allowed_as_write"])
        self.assertFalse(fake["accepted_as_close"])
        self.assertIn("h1 is proved", fake["refuse_hits"])
        honest = classify_h1_claim(PAGE.read_text())
        self.assertTrue(honest["allowed_as_write"])
        self.assertFalse(honest["accepted_as_close"])

    def test_pointers_and_filter(self):
        self.assertIn("H1-WRITE.md", TINY.read_text())
        self.assertIn("H1-WRITE.md", SHEET.read_text())
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
