"""MN-cancel: N=0 on v_n so R_mn=R_ab=1; not a useful K; not a close."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from mn_cancel import record  # noqa: E402

PAGE = ROOT / "docs" / "MN-CANCEL.md"
LDOOR = ROOT / "docs" / "L-DOOR.md"
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


class MNCancelArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_identities_and_amplitude(self):
        amp = self.row["amplitude"]
        self.assertTrue(amp["R_mn_flat"])
        self.assertTrue(amp["R_sign_flat"])
        self.assertTrue(amp["R_ab_flat"])
        self.assertTrue(amp["identities"])
        self.assertTrue(self.row["identities_sit"])
        self.assertTrue(self.row["vn_closed_match"])

    def test_instantaneous_mn_dead(self):
        self.assertTrue(self.row["vn_N_zero"])
        self.assertTrue(self.row["vn_R_mn_one"])
        self.assertTrue(self.row["instantaneous_MN_dead"])
        self.assertFalse(self.row["sits_as_universal_theta"])
        self.assertTrue(self.row["g4_stays_open"])
        vn = {r["label"]: r for r in self.row["vn_table"]}
        self.assertAlmostEqual(vn["vn1"]["R_mn"], 1.0)
        self.assertAlmostEqual(vn["vn8"]["R_mn"], 1.0)
        self.assertAlmostEqual(vn["vn1"]["R_ab"], 1.0, places=8)
        self.assertAlmostEqual(vn["vn8"]["R_ab"], 1.0, places=8)
        # Signed vertices cancel some, then stall. Not a useful K.
        self.assertGreater(vn["vn1"]["R_sign"], 0.2)
        self.assertLess(vn["vn10"]["R_sign"], 0.4)
        self.assertGreater(vn["vn10"]["R_sign"], vn["vn1"]["R_sign"])


class MNCancelPageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("N=0", raw)
        self.assertIn("R_{mn}=1", text)
        self.assertIn("v_n", raw)
        self.assertIn("G4 stays OPEN", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("not a useful", text.lower())
        self.assertIn("L-DOOR.md", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)
        self.assertNotIn("MN sits", raw)

    def test_not_the_abc_page(self):
        abc = ABC.read_text()
        self.assertIn("ABC", abc)
        self.assertNotIn("MN-CANCEL.md", abc)

    def test_pointers(self):
        self.assertIn("MN-CANCEL.md", LDOOR.read_text())
        self.assertIn("MN-CANCEL.md", ENERGY.read_text())
        self.assertIn("MN-CANCEL.md", GEOM.read_text())
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
            self.assertIn("MN-CANCEL.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
