"""Pathwise first jet: Stokes keeps N=0 on v_n; T_c grows; not a close."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from pathwise import record  # noqa: E402

PAGE = ROOT / "docs" / "PATHWISE.md"
MNC = ROOT / "docs" / "MN-CANCEL.md"
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


class PathwiseArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_locks_and_amplitude(self):
        amp = self.row["amplitude"]
        self.assertTrue(amp["stokes_over_Tc_flat"])
        self.assertTrue(amp["euler_scaled_flat"])
        self.assertTrue(amp["B_match"])
        self.assertTrue(self.row["fd_lock"])
        self.assertTrue(self.row["B_match"])
        self.assertTrue(self.row["triangle_stokes_is_minus_eight_thirds"])

    def test_vn_jet_not_a_k(self):
        self.assertTrue(self.row["vn_N_zero"])
        self.assertTrue(self.row["vn_stokes_preserves_N"])
        self.assertTrue(self.row["vn_euler_generates_N"])
        self.assertTrue(self.row["vn_slice_not_invariant"])
        self.assertTrue(self.row["vn_Tc_grows"])
        self.assertFalse(self.row["sits_as_useful_K"])
        self.assertFalse(self.row["sits_as_g4_death"])
        self.assertTrue(self.row["g4_stays_open"])
        vn = {r["label"]: r for r in self.row["vn_table"]}
        self.assertLess(abs(vn["vn8"]["N_dot_stokes"]), 1e-8)
        self.assertLess(vn["vn8"]["N_dot_euler"], 0.0)
        self.assertGreater(vn["vn8"]["Tc_dot"], vn["vn1"]["Tc_dot"])


class PathwisePageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("Stokes keeps", raw)
        self.assertIn("v_n", raw)
        self.assertIn("G4 stays", raw)
        self.assertIn("OPEN", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("not a useful", text.lower())
        self.assertIn("MN-CANCEL.md", raw)
        self.assertIn("PATH-TO-CLOSE.md", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)
        self.assertNotIn("jet sits as K", text.lower())

    def test_not_the_abc_page(self):
        abc = ABC.read_text()
        self.assertIn("ABC", abc)
        self.assertNotIn("PATHWISE.md", abc)

    def test_pointers(self):
        self.assertIn("PATHWISE.md", MNC.read_text())
        self.assertIn("PATHWISE.md", LDOOR.read_text())
        self.assertIn("PATHWISE.md", ENERGY.read_text())
        self.assertIn("PATHWISE.md", GEOM.read_text())
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
            self.assertIn("PATHWISE.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
