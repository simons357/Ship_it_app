"""Short interval: Stokes keeps N=0 on v_n; NSE keeps R_mn=1; not a close."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from interval import record  # noqa: E402

PAGE = ROOT / "docs" / "INTERVAL.md"
PATHWISE = ROOT / "docs" / "PATHWISE.md"
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


class IntervalArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_locks(self):
        self.assertTrue(self.row["jet_lock_ok"])
        self.assertTrue(self.row["R_E0_amp_flat"])
        self.assertTrue(self.row["stokes_vn_N0_zero"])
        self.assertTrue(self.row["stokes_vn_N_stays_small"])
        self.assertTrue(self.row["stokes_vn_R_mn_stays_one"])
        self.assertTrue(self.row["nse_energy_lock"])
        self.assertTrue(self.row["nse_vn_N_leaves_zero"])
        self.assertTrue(self.row["nse_vn_N_negative"])
        self.assertTrue(self.row["nse_vn_Tc_grows"])
        self.assertTrue(self.row["nse_vn_R_E_stays_large"])
        self.assertTrue(self.row["nse_vn_R_mn_stays_one"])
        self.assertTrue(self.row["nse_euler_N_negative"])
        self.assertTrue(self.row["nse_euler_Tc_grows"])
        self.assertTrue(self.row["amp_large_K_not_killed_by_viscosity"])
        self.assertFalse(self.row["sits_as_useful_K"])
        self.assertFalse(self.row["sits_as_g4_death"])
        self.assertTrue(self.row["g4_stays_open"])

    def test_printed_growth(self):
        nse = {r["label"]: r for r in self.row["nse"]}
        self.assertGreater(nse["vn1"]["Tc_end"], nse["vn1"]["Tc0"])
        self.assertLess(nse["vn1"]["N_end"], 0.0)
        self.assertGreater(nse["vn1a4"]["K_half_end"], nse["vn1a4"]["K_half0"])
        self.assertGreater(nse["vn1a4"]["K_half_end"], 1.0)
        stokes = {r["label"]: r for r in self.row["stokes"]}
        self.assertLess(abs(stokes["vn1"]["N_end"]), 1e-12)
        self.assertGreater(stokes["vn8"]["R_E_end"], stokes["vn1"]["R_E_end"])


class IntervalPageTests(unittest.TestCase):
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
        self.assertIn("PATHWISE.md", raw)
        self.assertIn("PATH-TO-CLOSE.md", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)
        self.assertNotIn("interval sits as K", text.lower())

    def test_not_the_abc_page(self):
        abc = ABC.read_text()
        self.assertIn("ABC", abc)
        self.assertNotIn("INTERVAL.md", abc)

    def test_pointers(self):
        self.assertIn("INTERVAL.md", PATHWISE.read_text())
        self.assertIn("INTERVAL.md", MNC.read_text())
        self.assertIn("INTERVAL.md", LDOOR.read_text())
        self.assertIn("INTERVAL.md", ENERGY.read_text())
        self.assertIn("INTERVAL.md", GEOM.read_text())
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
            self.assertIn("INTERVAL.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
