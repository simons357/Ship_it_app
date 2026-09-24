"""Lemma A sits on the unit torus; Lemma B stays OPEN; not a useful K."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from press import record  # noqa: E402

PAGE = ROOT / "docs" / "PRESS.md"
SBP = ROOT / "docs" / "SBP.md"
WIDTH = ROOT / "docs" / "WIDTH.md"
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


class PressArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_locks(self):
        self.assertTrue(self.row["lemma_A_sits"])
        self.assertTrue(self.row["P_at_one_ok"])
        self.assertTrue(self.row["P_nonneg"])
        self.assertTrue(self.row["P_prime_lower_ok"])
        self.assertTrue(self.row["P_prime_fd_ok"])
        self.assertTrue(self.row["ratio_le_one"])
        self.assertTrue(self.row["C_to_one"])
        self.assertTrue(self.row["C_finite_lt_one"])
        self.assertTrue(self.row["shell_formula_ok"])
        self.assertTrue(self.row["at_shell_check"])
        self.assertTrue(self.row["off_torus_fails"])
        self.assertTrue(self.row["zero_mode_is_kappa4"])
        self.assertTrue(self.row["samples_Phi_le_W"])
        self.assertTrue(self.row["W_identity_ok"])
        self.assertTrue(self.row["young_ok"])
        self.assertTrue(self.row["young_weaker_than_W"])
        self.assertTrue(self.row["L4_ok"])
        self.assertTrue(self.row["reset_is_not_broad_scale"])
        self.assertTrue(self.row["reset_is_not_a_payment"])
        self.assertTrue(self.row["lemma_B_open"])
        self.assertTrue(self.row["lemma_B_not_seated"])
        self.assertTrue(self.row["charge_different_bill"])
        self.assertTrue(self.row["unit_torus_only"])
        self.assertTrue(self.row["not_R3"])
        self.assertTrue(self.row["da_ns2_is_not_a_theorem"])
        self.assertFalse(self.row["sits_as_useful_K"])
        self.assertFalse(self.row["sits_as_g4_death"])
        self.assertFalse(self.row["sits_as_da_ns2"])
        self.assertFalse(self.row["sits_as_jgc"])
        self.assertFalse(self.row["sits_as_bprim"])
        self.assertTrue(self.row["g4_stays_open"])
        self.assertTrue(self.row["do_not_invent_a_bridge"])
        self.assertTrue(self.row["do_not_run_taylor_green"])
        self.assertTrue(self.row["do_not_mix_heavy"])
        self.assertTrue(self.row["do_not_glue_to_leftover_1"])

    def test_printed(self):
        self.assertLess(self.row["off_torus_P"], 0.0)
        self.assertGreater(self.row["C_rows"][-1]["C"], self.row["C_rows"][0]["C"])
        self.assertLess(self.row["C_rows"][-1]["C"], 1.0)
        self.assertGreater(self.row["samples"]["low"]["W"], self.row["samples"]["low"]["Phi"])


class PressPageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("Lemma A sits", raw)
        self.assertIn("Lemma B stays OPEN", raw)
        self.assertIn("The SBP identity is not a useful K", raw)
        self.assertIn("G4 stays", raw)
        self.assertIn("OPEN", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("Do not invent a bridge", raw)
        self.assertIn("Do not run Taylor", raw)
        self.assertIn("SBP.md", raw)
        self.assertIn("RESET.md", raw)
        self.assertIn("WIDTH.md", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)
        self.assertNotIn("DA-NS-2 sits", raw)
        self.assertNotIn("JGC sits", raw)
        self.assertNotIn("lemma b sits", text.lower())
        self.assertNotIn("the primitive is seated", text.lower())

    def test_not_the_abc_page(self):
        abc = ABC.read_text()
        self.assertIn("ABC", abc)
        self.assertNotIn("PRESS.md", abc)

    def test_pointers(self):
        self.assertIn("PRESS.md", SBP.read_text())
        self.assertIn("PRESS.md", WIDTH.read_text())
        self.assertIn("PRESS.md", RESET.read_text())
        self.assertIn("PRESS.md", LEDGER.read_text())
        self.assertIn("PRESS.md", DANS.read_text())
        self.assertIn("PRESS.md", DRIFT.read_text())
        self.assertIn("PRESS.md", INTERVAL.read_text())
        self.assertIn("PRESS.md", GEOM.read_text())
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
            self.assertIn("PRESS.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
