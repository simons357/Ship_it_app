"""SBP rewrite is elementary if the flux holds; it is not a useful K."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from sbp import record  # noqa: E402

PAGE = ROOT / "docs" / "SBP.md"
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


class SbpArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_locks(self):
        self.assertTrue(self.row["phi_expand_ok"])
        self.assertTrue(self.row["phi_nonneg"])
        self.assertTrue(self.row["phi_zero_at_shell"])
        self.assertTrue(self.row["phi_at_zero_is_kappa4"])
        self.assertTrue(self.row["quadratic_factor_positive"])
        self.assertTrue(self.row["grad_R_ok"])
        self.assertTrue(self.row["CS_ok"])
        self.assertTrue(self.row["single_shell_equality"])
        self.assertTrue(self.row["tail_can_hold_Ds"])
        self.assertTrue(self.row["phi_capacity_identity_ok"])
        self.assertTrue(self.row["single_shell_Phi_zero"])
        self.assertTrue(self.row["core_Phi_over_Y_small"])
        self.assertTrue(self.row["low_Phi_over_Y_beats_r2"])
        self.assertTrue(self.row["high_Phi_over_Y_order_one"])
        self.assertTrue(self.row["rewrite_ok"])
        self.assertTrue(self.row["live_moving_term_vanishes"])
        self.assertTrue(self.row["flux_normalization_not_reproduced"])
        self.assertTrue(self.row["Phi_is_not_Psi"])
        self.assertTrue(self.row["N_is_not_S_Gamma"])
        self.assertTrue(self.row["gate_file_not_in_repo"])
        self.assertTrue(self.row["chebyshev_not_reproduced"])
        self.assertTrue(self.row["do_not_mix_live_and_frozen"])
        self.assertTrue(self.row["Phi_over_Y_not_controlled_by_r2"])
        self.assertTrue(self.row["identity_is_not_a_payment"])
        self.assertTrue(self.row["da_ns2_is_not_a_theorem"])
        self.assertFalse(self.row["sits_as_useful_K"])
        self.assertFalse(self.row["sits_as_g4_death"])
        self.assertFalse(self.row["sits_as_da_ns2"])
        self.assertFalse(self.row["sits_as_jgc"])
        self.assertFalse(self.row["sits_as_bprim"])
        self.assertTrue(self.row["g4_stays_open"])
        self.assertTrue(self.row["do_not_invent_a_bridge"])
        self.assertTrue(self.row["do_not_run_taylor_green"])
        self.assertTrue(self.row["do_not_glue_to_leftover_1"])

    def test_printed(self):
        self.assertAlmostEqual(self.row["R_core"], self.row["two_k3"])
        self.assertGreater(self.row["tail_sample"]["Ds_over_Y"], 1.0)
        low = next(r for r in self.row["phi_rows"] if r["label"] == "low")
        self.assertGreater(low["Phi_over_Y"] / low["r2"], 100.0)


class SbpPageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("The SBP identity is not a useful K", raw)
        self.assertIn("G4 stays", raw)
        self.assertIn("OPEN", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("Do not invent a bridge", raw)
        self.assertIn("Do not run Taylor", raw)
        self.assertIn("WIDTH.md", raw)
        self.assertIn("RESET.md", raw)
        self.assertIn("CENTERED-LEDGER.md", raw)
        self.assertIn("DA-NS-2.md", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)
        self.assertNotIn("DA-NS-2 sits", raw)
        self.assertNotIn("JGC sits", raw)
        self.assertNotIn("sbp sits as k", text.lower())
        self.assertNotIn("the primitive is seated", text.lower())

    def test_not_the_abc_page(self):
        abc = ABC.read_text()
        self.assertIn("ABC", abc)
        self.assertNotIn("SBP.md", abc)

    def test_pointers(self):
        self.assertIn("SBP.md", WIDTH.read_text())
        self.assertIn("SBP.md", RESET.read_text())
        self.assertIn("SBP.md", LEDGER.read_text())
        self.assertIn("SBP.md", DANS.read_text())
        self.assertIn("SBP.md", DRIFT.read_text())
        self.assertIn("SBP.md", INTERVAL.read_text())
        self.assertIn("SBP.md", GEOM.read_text())
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
            self.assertIn("SBP.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
