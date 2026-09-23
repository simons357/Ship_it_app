"""L-door: tight CS is star; LE dead; LX not a universal C; not a close."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from l_door import record  # noqa: E402

PAGE = ROOT / "docs" / "L-DOOR.md"
ENERGY = ROOT / "docs" / "ENERGY-K.md"
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
PROOF = ROOT / "docs" / "BSTAR-PROOF.md"
CLOSE = ROOT / "docs" / "NS-CLOSE-REPORT.md"
ABC = ROOT / "docs" / "CS-REMAINDER.md"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "").replace("*", "")


class LDoorArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_amplitude_and_tight_is_star(self):
        amp = self.row["amplitude"]
        self.assertTrue(amp["R_LE_flat"])
        self.assertTrue(amp["R_LX_flat"])
        self.assertTrue(amp["R_L_flat"])
        self.assertTrue(self.row["tight_is_star"])

    def test_le_dead_lx_not_seated(self):
        self.assertTrue(self.row["vn_R_LE_grows"])
        self.assertTrue(self.row["vn_R_LX_grows"])
        self.assertTrue(self.row["imag_R_LE_grows"])
        self.assertTrue(self.row["imag_R_LX_grows"])
        self.assertTrue(self.row["sep_R_LE_grows"])
        self.assertTrue(self.row["LE_door_dead"])
        self.assertTrue(self.row["LX_door_not_seated"])
        self.assertFalse(self.row["sits_as_universal_C"])
        self.assertTrue(self.row["g4_stays_open"])
        vn = {r["label"]: r for r in self.row["vn_table"]}
        self.assertGreater(vn["vn8"]["R_LE"], 10.0 * vn["vn1"]["R_LE"])
        self.assertGreater(vn["vn8"]["R_LX"], vn["vn1"]["R_LX"])
        # v_n does not kill the B-star CS door.
        self.assertLess(vn["vn8"]["R_L"], vn["vn1"]["R_L"])


class LDoorPageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("tight", text.lower())
        self.assertIn("v_n", raw)
        self.assertIn("LE is dead", raw)
        self.assertIn("not a universal", text.lower())
        self.assertIn("G4 stays OPEN", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("CS-REMAINDER.md", raw)
        self.assertIn("not", text.lower())
        self.assertIn("ENERGY-K.md", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)
        self.assertNotIn("LX sits", raw)

    def test_not_the_abc_page(self):
        abc = ABC.read_text()
        self.assertIn("ABC", abc)
        self.assertNotIn("L-DOOR.md", abc)

    def test_pointers(self):
        self.assertIn("L-DOOR.md", ENERGY.read_text())
        self.assertIn("L-DOOR.md", GEOM.read_text())
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
            PROOF,
            CLOSE,
            LIFT,
        ):
            self.assertIn("L-DOOR.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
