"""Chart reset: jump is exact; remainder is chart-invariant; not a close."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from reset import record  # noqa: E402

PAGE = ROOT / "docs" / "RESET.md"
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


class ResetArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_locks(self):
        self.assertTrue(self.row["jump_formula_ok"])
        self.assertTrue(self.row["reset_to_lambda_drops_W"])
        self.assertTrue(self.row["reset_away_can_raise_W"])
        self.assertTrue(self.row["K_min_chart_invariant"])
        self.assertTrue(self.row["W_lambda_is_Ds"])
        self.assertTrue(self.row["K_min_positive_on_sample"])
        self.assertTrue(self.row["sum_abs_dW_is_X_sum_sq"])
        self.assertTrue(self.row["frequent_reset_weaker_than_TV"])
        self.assertTrue(self.row["da_ns2_is_not_a_theorem"])
        self.assertFalse(self.row["sits_as_useful_K"])
        self.assertFalse(self.row["sits_as_g4_death"])
        self.assertFalse(self.row["sits_as_jgc"])
        self.assertFalse(self.row["sits_as_da_ns2"])
        self.assertTrue(self.row["g4_stays_open"])
        self.assertTrue(self.row["paste_not_reconstructed"])
        self.assertTrue(self.row["do_not_glue_to_leftover_1"])

    def test_printed_jump(self):
        to_lam = self.row["rows"][0]
        self.assertLess(to_lam["dW"], 0.0)
        self.assertAlmostEqual(to_lam["K_min_old"], to_lam["K_min_new"])
        away = self.row["rows"][1]
        self.assertGreater(away["dW"], 0.0)


class ResetPageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("A reset is not a useful K", raw)
        self.assertIn("does not jump", text.lower())
        self.assertIn("G4 stays", raw)
        self.assertIn("OPEN", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("CENTERED-LEDGER.md", raw)
        self.assertIn("DA-NS-2.md", raw)
        self.assertIn("INTERVAL.md", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)
        self.assertNotIn("DA-NS-2 sits", raw)
        self.assertNotIn("JGC sits", raw)
        self.assertNotIn("reset sits as K", text.lower())

    def test_not_the_abc_page(self):
        abc = ABC.read_text()
        self.assertIn("ABC", abc)
        self.assertNotIn("RESET.md", abc)

    def test_pointers(self):
        self.assertIn("RESET.md", LEDGER.read_text())
        self.assertIn("RESET.md", DANS.read_text())
        self.assertIn("RESET.md", DRIFT.read_text())
        self.assertIn("RESET.md", INTERVAL.read_text())
        self.assertIn("RESET.md", GEOM.read_text())
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
            self.assertIn("RESET.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
