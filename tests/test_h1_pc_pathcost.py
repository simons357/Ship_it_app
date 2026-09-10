"""PC path-cost sits on a curve. It is not H1."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from h1_pc_pathcost import run  # noqa: E402

PAGE = ROOT / "docs" / "H1-PC.md"


class H1PCPathcostTests(unittest.TestCase):
    def test_page_stays_open_and_not_h1(self):
        text = PAGE.read_text()
        self.assertIn("**This estimate sits. It is not H1.", text)
        self.assertIn("WRITE (6) is not proved. NS is not solved.**", text)
        self.assertIn("Lemma PC", text)
        self.assertIn("not h1", text.lower())
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("H1 is proved", text)

    def test_probe_scores(self):
        payload = run(seed=3)
        rows = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(rows["H1pc_geodesic_sits"]["verdict"], "pass")
        self.assertEqual(rows["H1pc_path_sits"]["verdict"], "pass")
        self.assertEqual(rows["H1pc_bad_cut"]["verdict"], "pass")
        self.assertEqual(rows["H1pc_gap"]["verdict"], "pass")
        self.assertEqual(rows["H1pc_not_fold"]["verdict"], "pass")
        self.assertEqual(rows["H1pc_is_h1"]["verdict"], "fail")
        self.assertEqual(payload["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["h1_proved"])
        self.assertFalse(payload["meta"]["lemma_pc_is_h1"])

    def test_rotating_field_pays_the_angle(self):
        payload = run(seed=11)
        rot = payload["rotating"]
        self.assertGreaterEqual(rot["path_cost"] + 1e-12, rot["phi"])
        self.assertGreaterEqual(rot["phi"] + 1e-12, rot["sin_phi"])
        self.assertTrue(rot["bad_cut"])


if __name__ == "__main__":
    unittest.main()
