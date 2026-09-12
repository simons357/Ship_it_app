"""H1 shape 3 predictive. Not a close. Not ABC. ★ not glued."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from h1_predictive import (  # noqa: E402
    C_STAR,
    holder,
    pictures,
    run,
)

DOC = ROOT / "docs" / "H1-PREDICTIVE.md"
OBJECT = ROOT / "docs" / "H1-OBJECT.md"
LIVE = ROOT / "docs" / "LEMMA-STAR-LIVE.md"
SCRIPT = ROOT / "scripts" / "h1_predictive.py"


class H1PredictiveTests(unittest.TestCase):
    def test_doc_locks_the_door(self):
        text = DOC.read_text()
        self.assertIn("Not a theorem", text)
        self.assertIn("H1 is not proved", text)
        self.assertIn("NS is not solved", text)
        self.assertIn("Not from ABC", text)
        self.assertIn("shape 3", text.lower())
        self.assertNotIn("NS is solved", text)
        self.assertTrue(SCRIPT.is_file())
        obj = OBJECT.read_text()
        self.assertIn("H1-PREDICTIVE.md", obj)
        live = LIVE.read_text()
        self.assertIn("H1-PREDICTIVE.md", live)

    def test_holder_and_xi_unit(self):
        z = np.array([0.0, 0.0, 1.0])
        y = np.array([0.0, 1.0, 0.0])
        self.assertAlmostEqual(holder(z, y, 0.25, 0.25), 1.0, places=12)
        pics = pictures(rho0=0.25, G0=1.0, nu=0.02)
        for name, rec in pics.items():
            self.assertLess(rec["xi_unit_err"], 1e-8, msg=name)
            self.assertTrue(rec["started_bad"], msg=name)
            self.assertGreater(rec["holder0"], C_STAR, msg=name)

    def test_alignment_frozen_and_shape3_fails(self):
        summary = run(rho0=0.25, G0=1.0, nu=0.02)
        self.assertIs(summary["h1_proved"], False)
        self.assertIs(summary["shape3_sits"], False)
        self.assertIs(summary["ns_solved"], False)
        self.assertIs(summary["started_from_abc"], False)
        self.assertIs(summary["glued_to_star"], False)
        by = {r["name"]: r for r in summary["lemmas"]}
        self.assertEqual(by["H1p_xi_unit"]["verdict"], "pass")
        self.assertEqual(by["H1p_not_abc"]["verdict"], "pass")
        self.assertEqual(by["H1p_gap_forbidden"]["verdict"], "fail")
        self.assertEqual(by["H1p_sheet_forbidden"]["verdict"], "fail")
        self.assertEqual(by["H1p_shape3"]["verdict"], "fail")
        self.assertEqual(by["H1p_not_a_close"]["verdict"], "fail")
        self.assertEqual(by["H1p_not_star"]["verdict"], "fail")
        gap = summary["pictures"]["gap"]
        fold = summary["pictures"]["fold"]
        self.assertLess(abs(gap["holder_rel_change"]), 0.05)
        self.assertLess(abs(fold["holder_rel_change"]), 0.08)
        self.assertTrue(gap["persisted_through_4waiting"])
        self.assertTrue(summary["verdict"].startswith("SHAPE3_NOT_SEATED"))


if __name__ == "__main__":
    unittest.main()
