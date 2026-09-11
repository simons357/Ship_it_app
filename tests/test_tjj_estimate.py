"""Requested Young line is not seated. The chain stays a chain."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph, run  # noqa: E402

PAGE = ROOT / "docs" / "TJJ-ESTIMATE.md"
SHELL = ROOT / "docs" / "AXISYM-SHELL.md"
AUDIT = ROOT / "docs" / "ESTIMATE-AUDIT.md"


class TjjEstimateTests(unittest.TestCase):
    def test_page_refuses_the_line(self):
        text = PAGE.read_text()
        self.assertIn("The chain stays a chain.", text)
        self.assertIn("The estimate cannot be written.", text)
        self.assertIn("T_{j\\leftarrow j}", text)
        self.assertIn("\\varepsilon\\nu", text)
        self.assertIn("\\dot Z_j", text)
        self.assertIn("\\Lambda'", text)
        self.assertIn("energy", text)
        self.assertIn("direction factor", text)
        self.assertIn("TJJ_requested_line", text)
        self.assertIn("**fail**", text)
        self.assertIn("NS not solved.", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("unconditional 3-D regularity", text)
        self.assertNotIn("coherence viscosity", text)
        self.assertNotIn("gematria", text)
        # Do not cash the energy-linear shape as a theorem.
        self.assertIn("would close, not proved", text)
        self.assertIn("not seated", text)

    def test_page_passes_discard_filter(self):
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])

    def test_pointers_and_scores(self):
        self.assertIn("TJJ-ESTIMATE.md", SHELL.read_text())
        self.assertIn("TJJ-ESTIMATE.md", AUDIT.read_text())
        self.assertIn("AS_tjj_young", SHELL.read_text())
        self.assertIn("EAud_tjj_young", AUDIT.read_text())
        payload = run()
        rows = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(rows["EAud_tjj_young"]["verdict"], "fail")
        self.assertEqual(payload["domain_verdict"], "open")
        self.assertTrue(payload["meta"]["estimate_open"])


if __name__ == "__main__":
    unittest.main()
