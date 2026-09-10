"""P1-loc cutoff sits. Dropping ∇u does not. Not H1."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from h1_p1_loc import run  # noqa: E402

PAGE = ROOT / "docs" / "H1-P1-LOC.md"


class H1P1LocTests(unittest.TestCase):
    def test_page_stays_open_and_not_h1(self):
        text = PAGE.read_text()
        self.assertIn("**This estimate sits. It is not H1.", text)
        self.assertIn("WRITE (6) is not proved. NS is not solved.**", text)
        self.assertIn("Lemma P1-loc", text)
        self.assertIn("nabla u", text.lower().replace("\\", ""))
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("H1 is proved", text)

    def test_probe_scores(self):
        payload = run(n=24, seed=3)
        rows = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(rows["H1p1loc_cutoff_sits"]["verdict"], "pass")
        self.assertEqual(rows["H1p1loc_drop_gradu"]["verdict"], "fail")
        self.assertEqual(rows["H1p1loc_is_h1"]["verdict"], "fail")
        self.assertEqual(rows["H1p1loc_nse_class"]["verdict"], "open")
        self.assertEqual(payload["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["h1_proved"])
        self.assertFalse(payload["meta"]["drop_gradu"])

    def test_inequality_holds_on_mixed_and_high(self):
        payload = run(n=24, seed=11)
        for row in payload["mixed"] + payload["highpass"]:
            self.assertTrue(row["held"], row)
        for row in payload["highpass"]:
            self.assertGreater(row["thinness_drop_gradu"], 4.0)


if __name__ == "__main__":
    unittest.main()
