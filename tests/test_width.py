"""Relative width sits; crossover is not a theorem; no S_Γ primitive."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from width import record  # noqa: E402

PAGE = ROOT / "docs" / "WIDTH.md"
RESET = ROOT / "docs" / "RESET.md"
LEDGER = ROOT / "docs" / "CENTERED-LEDGER.md"
DANS = ROOT / "docs" / "DA-NS-2.md"
DRIFT = ROOT / "docs" / "CENTERED-DRIFT.md"
INTERVAL = ROOT / "docs" / "INTERVAL.md"
GEOM = ROOT / "docs" / "FOURIER-TRIANGLE.md"
LIFT = ROOT / "docs" / "TRIANGLE-LIFT.md"
STATUS = ROOT / "docs" / "NS-STATUS.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
TINY = ROOT / "docs" / "TINY.txt"
LATEST = ROOT / "docs" / "LATEST.md"
ISSUES = ROOT / "docs" / "ISSUES-SHEET.md"
PLAN = ROOT / "docs" / "MASTER-PLAN.md"
PATH = ROOT / "docs" / "PATH-TO-CLOSE.md"
BSTAR = ROOT / "docs" / "BSTAR.md"
PROOF = ROOT / "docs" / "BSTAR-PROOF.md"
CLOSE = ROOT / "docs" / "NS-CLOSE-REPORT.md"
ENERGY = ROOT / "docs" / "ENERGY-K.md"
LDOOR = ROOT / "docs" / "L-DOOR.md"
MNC = ROOT / "docs" / "MN-CANCEL.md"
PATHWISE = ROOT / "docs" / "PATHWISE.md"
ABC = ROOT / "docs" / "CS-REMAINDER.md"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "").replace("*", "")


class WidthArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_locks(self):
        self.assertTrue(self.row["identities_ok"])
        self.assertTrue(self.row["r_scale_invariant"])
        self.assertTrue(self.row["threshold_not_scale_invariant"])
        self.assertTrue(self.row["conversion_ok"])
        self.assertTrue(self.row["ladder_r_stays_order_one"])
        self.assertTrue(self.row["ladder_becomes_broad"])
        self.assertTrue(self.row["charge_only_dead"])
        self.assertTrue(self.row["no_primitive_for_S"])
        self.assertTrue(self.row["crossover_is_not_a_theorem"])
        self.assertTrue(self.row["broad_is_not_a_payment"])
        self.assertTrue(self.row["da_ns2_is_not_a_theorem"])
        self.assertFalse(self.row["sits_as_useful_K"])
        self.assertFalse(self.row["sits_as_g4_death"])
        self.assertFalse(self.row["sits_as_da_ns2"])
        self.assertFalse(self.row["sits_as_jgc"])
        self.assertFalse(self.row["sits_as_bprim"])
        self.assertTrue(self.row["g4_stays_open"])
        self.assertTrue(self.row["do_not_invent_a_bridge"])

    def test_printed(self):
        self.assertGreater(self.row["scale"]["ell"], 1.0)
        self.assertAlmostEqual(self.row["conversion"]["ratio"], 0.5)
        self.assertGreater(self.row["ladders"][-1]["kappa"], self.row["ladders"][0]["kappa"])


class WidthPageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("The crossover is not a useful K", raw)
        self.assertIn("No primitive for", raw)
        self.assertIn("on this desk", text.lower())
        self.assertIn("G4 stays", raw)
        self.assertIn("OPEN", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("Do not invent a bridge", raw)
        self.assertIn("RESET.md", raw)
        self.assertIn("CENTERED-LEDGER.md", raw)
        self.assertIn("DA-NS-2.md", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)
        self.assertNotIn("DA-NS-2 sits", raw)
        self.assertNotIn("JGC sits", raw)
        self.assertNotIn("crossover sits as K", text.lower())
        self.assertNotIn("the primitive is seated", text.lower())

    def test_not_the_abc_page(self):
        abc = ABC.read_text()
        self.assertIn("ABC", abc)
        self.assertNotIn("WIDTH.md", abc)

    def test_pointers(self):
        self.assertIn("WIDTH.md", RESET.read_text())
        self.assertIn("WIDTH.md", LEDGER.read_text())
        self.assertIn("WIDTH.md", DANS.read_text())
        self.assertIn("WIDTH.md", DRIFT.read_text())
        self.assertIn("WIDTH.md", INTERVAL.read_text())
        self.assertIn("WIDTH.md", GEOM.read_text())
        for path in (
            STATUS,
            TAPE,
            TINY,
            LATEST,
            ISSUES,
            PLAN,
            PATH,
            BSTAR,
            PROOF,
            CLOSE,
            LIFT,
            ENERGY,
            LDOOR,
            MNC,
            PATHWISE,
        ):
            self.assertIn("WIDTH.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
