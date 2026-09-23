"""Triangle lift: two-shell sits; third eigenvalue dies; K~sqrt(E) dead."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from triangle_lift import record  # noqa: E402

PAGE = ROOT / "docs" / "TRIANGLE-LIFT.md"
GEOM = ROOT / "docs" / "FOURIER-TRIANGLE.md"
STATUS = ROOT / "docs" / "NS-STATUS.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
TINY = ROOT / "docs" / "TINY.txt"
LATEST = ROOT / "docs" / "LATEST.md"
ISSUES = ROOT / "docs" / "ISSUES-SHEET.md"
PLAN = ROOT / "docs" / "MASTER-PLAN.md"
PATH = ROOT / "docs" / "PATH-TO-CLOSE.md"
DRIFT = ROOT / "docs" / "CENTERED-DRIFT.md"
BSTAR = ROOT / "docs" / "BSTAR.md"
CLOSE = ROOT / "docs" / "NS-CLOSE-REPORT.md"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "").replace("*", "")


class TriangleLiftArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_same_two_shells_keep_gap(self):
        sit = self.row["lifts_that_sit"]
        self.assertTrue(sit["two_shell_a"])
        self.assertTrue(sit["two_shell_b"])
        self.assertTrue(sit["same_two_shells_still_gap"])
        self.assertEqual(sit["same_two_shells_n"], 2)

    def test_third_eigenvalue_kills_gap(self):
        fail = self.row["first_failed_sum"]
        self.assertEqual(fail["four_shell_n"], 4)
        self.assertFalse(fail["four_shell_gap_formula"])
        self.assertTrue(fail["nonadditive"])
        self.assertTrue(fail["unbal_still_two_shell"])

    def test_isolated_triangle_leaks(self):
        ev = self.row["first_failed_evolve"]
        self.assertFalse(ev["isolated_closed_under_B"])
        self.assertGreater(ev["leak_a"]["leak_frac"], 0.2)
        self.assertGreater(ev["leak_a"]["n_off_live"], 0)

    def test_energy_k_killed_by_vn(self):
        k = self.row["attempted_energy_K"]
        self.assertTrue(k["vn_R_E_grows"])
        self.assertTrue(k["imag_R_E_grows"])
        self.assertFalse(k["sits_as_universal_C"])
        vn = {r["label"]: r["R_E"] for r in k["families"] if r["label"].startswith("vn")}
        self.assertGreater(vn["vn8"], 10.0 * vn["vn1"])


class TriangleLiftPageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("same two shells", text.lower())
        self.assertIn("third eigenvalue", text.lower())
        self.assertIn("leaks", text.lower())
        self.assertIn("sqrt", text.lower())
        self.assertIn("v_n", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("FOURIER-TRIANGLE.md", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)

    def test_pointers(self):
        self.assertIn("TRIANGLE-LIFT.md", GEOM.read_text())
        for path in (
            STATUS,
            TAPE,
            TINY,
            LATEST,
            ISSUES,
            PLAN,
            PATH,
            DRIFT,
            BSTAR,
            CLOSE,
        ):
            self.assertIn("TRIANGLE-LIFT.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
