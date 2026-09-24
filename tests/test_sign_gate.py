"""First-variation gate is L_1,N; no sign verdict; not a useful K."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from sign_gate import record  # noqa: E402

PAGE = ROOT / "docs" / "SIGN-GATE.md"
PRESS = ROOT / "docs" / "PRESS.md"
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


class SignGateArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_locks(self):
        self.assertTrue(self.row["expansion_ok"])
        self.assertTrue(self.row["frozen_R2_is_quadratic"])
        self.assertTrue(self.row["shrink_higher_order"])
        self.assertTrue(self.row["hard_deformation_not_higher_order"])
        self.assertTrue(self.row["soft_deformation_higher_order"])
        self.assertTrue(self.row["do_not_sub_T0_into_finite_gap"])
        self.assertTrue(self.row["retain_neighbor_T_as_remainder"])
        self.assertTrue(self.row["no_sign_verdict"])
        self.assertTrue(self.row["both_signs_not_printed"])
        self.assertTrue(self.row["one_sign_not_printed"])
        self.assertTrue(self.row["A_N_plus_not_invented"])
        self.assertTrue(self.row["lemma_A_unaltered"])
        self.assertTrue(self.row["lemma_B_open"])
        self.assertTrue(self.row["i3_bridge_not_seated"])
        self.assertTrue(self.row["no_more_potentials"])
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
        self.assertTrue(self.row["do_not_run_heavy_search"])
        self.assertTrue(self.row["do_not_glue_to_leftover_1"])

    def test_printed(self):
        self.assertNotEqual(self.row["base_sample"]["T_c"], 0.0)
        self.assertGreater(abs(self.row["hard"][-1]["R2_over_gap2"]), abs(self.row["hard"][0]["R2_over_gap2"]))
        self.assertLess(abs(self.row["shrink"][-1]["R2"]), abs(self.row["shrink"][0]["R2"]))


class SignGatePageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("The gate is", raw)
        self.assertIn("No sign verdict sits", raw)
        self.assertIn("G4 stays", raw)
        self.assertIn("OPEN", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("Do not invent a bridge", raw)
        self.assertIn("Do not run Taylor", raw)
        self.assertIn("PRESS.md", raw)
        self.assertIn("FOURIER-TRIANGLE.md", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)
        self.assertNotIn("DA-NS-2 sits", raw)
        self.assertNotIn("JGC sits", raw)
        self.assertNotIn("both signs sits", text.lower())
        self.assertNotIn("the primitive is seated", text.lower())
        self.assertNotIn("the bridge is seated", text.lower())

    def test_not_the_abc_page(self):
        abc = ABC.read_text()
        self.assertIn("ABC", abc)
        self.assertNotIn("SIGN-GATE.md", abc)

    def test_pointers(self):
        self.assertIn("SIGN-GATE.md", PRESS.read_text())
        self.assertIn("SIGN-GATE.md", SBP.read_text())
        self.assertIn("SIGN-GATE.md", WIDTH.read_text())
        self.assertIn("SIGN-GATE.md", RESET.read_text())
        self.assertIn("SIGN-GATE.md", LEDGER.read_text())
        self.assertIn("SIGN-GATE.md", DANS.read_text())
        self.assertIn("SIGN-GATE.md", DRIFT.read_text())
        self.assertIn("SIGN-GATE.md", INTERVAL.read_text())
        self.assertIn("SIGN-GATE.md", GEOM.read_text())
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
            self.assertIn("SIGN-GATE.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
