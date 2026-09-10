"""H1 estimate package stays OPEN. Not a GR close."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "DOOR-B-H1-ESTIMATE-PLAN.md"
SKETCH = ROOT / "docs" / "DOOR-B-H1-B5-LINFTY-SKETCH.md"


class H1EstimatePackageTests(unittest.TestCase):
    def test_plan_is_open_not_gr_close(self):
        text = PLAN.read_text()
        self.assertIn("**OPEN. Not a GR close.", text)
        self.assertIn("Outside-\\(\\mathcal{E}\\) identity: **blocked**.", text)
        self.assertIn("Lattice closure enumerator", text)
        self.assertIn("Two boxes sit (P1 on a stated class, PC on a", text)
        self.assertIn("Neither is H1", text)
        self.assertIn("NSE-class", text)
        self.assertIn("H1-P1.md", text)
        self.assertIn("H1-PC.md", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Zero boxes sit", text)

    def test_sketch_keeps_missing_marks(self):
        text = SKETCH.read_text()
        self.assertIn("**OPEN. Not a GR close.", text)
        for k in range(1, 10):
            self.assertIn(f"**MISSING-{k}.**", text)
        self.assertIn("No candidate", text)
        self.assertIn("Track B lemma B5", text)
        self.assertIn("BKM-from-\\(L^2\\)", text)


if __name__ == "__main__":
    unittest.main()
