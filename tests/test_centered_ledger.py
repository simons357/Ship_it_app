"""Incoming centered ledger: identities sit; DA-NS-2 is not a theorem."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from centered_ledger import record  # noqa: E402

PAGE = ROOT / "docs" / "CENTERED-LEDGER.md"
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


class LedgerArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_locks(self):
        self.assertTrue(self.row["product_matches_gap"])
        self.assertTrue(self.row["two_shell_centered_zero_empty"])
        self.assertTrue(self.row["flat_kills_perp"])
        self.assertTrue(self.row["k_perp2_ok"])
        self.assertTrue(self.row["W_K_ok"])
        self.assertTrue(self.row["unequal_defect_ok"])
        self.assertTrue(self.row["charge_only_dead"])
        self.assertTrue(self.row["da_ns2_is_not_a_theorem"])
        self.assertFalse(self.row["sits_as_useful_K"])
        self.assertFalse(self.row["sits_as_g4_death"])
        self.assertFalse(self.row["sits_as_da_ns2"])
        self.assertFalse(self.row["sits_as_sag_gamma"])
        self.assertFalse(self.row["sits_as_jgc"])
        self.assertTrue(self.row["g4_stays_open"])
        self.assertTrue(self.row["paste_truncated_at_17"])


class LedgerPageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("DA-NS-2", raw)
        self.assertIn("not a theorem", text.lower())
        self.assertIn("empty on two shells", text.lower())
        self.assertIn("G4 stays", raw)
        self.assertIn("OPEN", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("INTERVAL.md", raw)
        self.assertIn("DA-NS-2.md", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)
        self.assertNotIn("DA-NS-2 sits", raw)
        self.assertNotIn("ledger sits as K", text.lower())

    def test_not_the_abc_page(self):
        abc = ABC.read_text()
        self.assertIn("ABC", abc)
        self.assertNotIn("CENTERED-LEDGER.md", abc)

    def test_pointers(self):
        self.assertIn("CENTERED-LEDGER.md", DANS.read_text())
        self.assertIn("CENTERED-LEDGER.md", DRIFT.read_text())
        self.assertIn("CENTERED-LEDGER.md", INTERVAL.read_text())
        self.assertIn("CENTERED-LEDGER.md", GEOM.read_text())
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
            self.assertIn("CENTERED-LEDGER.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
