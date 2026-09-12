"""Attack 9D setup: same B as 9B; do not start 9D."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph  # noqa: E402

PAGE = ROOT / "docs" / "ATTACK-9D-SETUP.md"


class Attack9DSetupTests(unittest.TestCase):
    def test_call_is_do_not_start(self):
        text = PAGE.read_text()
        self.assertIn("Do **not** implement Attack 9D", text)
        self.assertIn("Pi_\\beta B(w,w)", text.replace("\\Pi", "Pi"))
        self.assertIn("\\Pi_\\beta B(w,w)", text)
        self.assertIn("9B family", text)
        self.assertIn("HH→L", text)
        self.assertIn("16s", text)
        self.assertIn("wrong packaging", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)

    def test_page_passes_discard_filter(self):
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
