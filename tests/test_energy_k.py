"""Energy-class K ladder: only sqrt(E) matches amplitude; all three doors die."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from energy_k import (  # noqa: E402
    E_n,
    R_Y_closed,
    R_mid_closed,
    T_c_n,
    X_n,
    Y_n,
    record,
)

PAGE = ROOT / "docs" / "ENERGY-K.md"
GEOM = ROOT / "docs" / "FOURIER-TRIANGLE.md"
LIFT = ROOT / "docs" / "TRIANGLE-LIFT.md"
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


class EnergyKArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_closed_forms_match_vn(self):
        self.assertEqual(E_n(1), 12.0)
        self.assertEqual(T_c_n(1), 21.0)
        self.assertAlmostEqual(X_n(1), 53.0)
        self.assertAlmostEqual(Y_n(1), 269.0)
        self.assertAlmostEqual(X_n(8), 17952.0)
        self.assertAlmostEqual(Y_n(8), 5518880.0)
        closed = self.row["closed_forms"]
        self.assertTrue(closed["all_match"])
        self.assertGreater(R_Y_closed(8), 10.0 * R_Y_closed(1))
        self.assertGreater(R_mid_closed(8), 10.0 * R_mid_closed(1))

    def test_amplitude_unique_half(self):
        amp = self.row["amplitude"]
        self.assertTrue(amp["R_E_flat"])
        self.assertTrue(amp["R_Y_flat"])
        self.assertTrue(amp["R_mid_flat"])
        self.assertTrue(amp["R_p1_grows_as_A_shrinks"])
        self.assertTrue(amp["R_p0_grows_as_A_grows"])
        self.assertEqual(amp["unique_amp_legal_p"], 0.5)

    def test_all_three_doors_die(self):
        self.assertTrue(self.row["vn_R_E_grows"])
        self.assertTrue(self.row["vn_R_Y_grows"])
        self.assertTrue(self.row["vn_R_mid_grows"])
        self.assertTrue(self.row["imag_R_Y_grows"])
        self.assertTrue(self.row["imag_R_mid_grows"])
        self.assertTrue(self.row["sep_not_the_kill"])
        self.assertFalse(self.row["sits_as_universal_C"])
        self.assertTrue(self.row["energy_class_ladder_dead"])
        self.assertTrue(self.row["g4_stays_open"])
        vn = {r["label"]: r for r in self.row["vn_table"]}
        self.assertGreater(vn["vn8"]["R_Y"], 10.0 * vn["vn1"]["R_Y"])


class EnergyKPageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("amplitude", text.lower())
        self.assertIn("v_n", raw)
        self.assertIn("sqrt", text.lower())
        self.assertIn("n^{3/2}", raw)
        self.assertIn("G4 stays OPEN", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("Attack-2", raw)
        self.assertIn("TRIANGLE-LIFT.md", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)

    def test_pointers(self):
        self.assertIn("ENERGY-K.md", GEOM.read_text())
        self.assertIn("ENERGY-K.md", LIFT.read_text())
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
            self.assertIn("ENERGY-K.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
