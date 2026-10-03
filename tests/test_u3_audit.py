"""||u||_3 correction: L^4_t L^3 is not Serrin; int X^2 supplies L^4_t L^6."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from u3_audit import (  # noqa: E402
    h12_cs,
    interpolation_L4_bound,
    optimized_split,
    record,
    serrin_index,
    split_pieces,
)

PAGE = ROOT / "docs" / "U3-AUDIT.md"
DERIV = ROOT / "docs" / "U3-DERIV.md"
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
SIGN = ROOT / "docs" / "SIGN-GATE.md"
RUN = ROOT / "docs" / "SIGN-RUN.md"
CHAIN = ROOT / "docs" / "UNAUGMENTED-NS-CHAIN.md"
ABC = ROOT / "docs" / "CS-REMAINDER.md"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "").replace("*", "")


class U3AuditArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_scaling(self):
        self.assertAlmostEqual(serrin_index(4.0, 3.0), 1.5)
        self.assertAlmostEqual(serrin_index(None, 3.0), 1.0)
        self.assertAlmostEqual(serrin_index(4.0, 6.0), 1.0)
        self.assertAlmostEqual(serrin_index(2.0, 3.0), 2.0)
        self.assertTrue(self.row["energy_L4_L3_owned_by_energy"])
        self.assertTrue(self.row["energy_L4_L3_is_not_Serrin"])
        self.assertTrue(self.row["L4_L3_stays_outside_Serrin"])
        self.assertTrue(self.row["int_X2_supplies_L4_L6_not_L4_L3"])
        self.assertTrue(self.row["int_X2_gives_Serrin_via_L4_L6"])
        self.assertTrue(self.row["L4_L6_is_Serrin"])
        self.assertTrue(self.row["ess_is_the_only_Serrin_L3"])
        self.assertTrue(self.row["finite_p_L3_is_supercritical"])
        self.assertTrue(self.row["high_piece_L2_L3_is_supercritical"])
        self.assertTrue(self.row["H12_embeds_L3"])
        self.assertFalse(self.row["L3_embeds_H12"])

    def test_derivation_algebra(self):
        self.assertAlmostEqual(interpolation_L4_bound(2.0, 0.5, 1.0), 4.0)
        self.assertAlmostEqual(h12_cs(2.0, 8.0), 4.0)
        opt = optimized_split(4.0, 16.0, 1.0, 1.0)
        self.assertAlmostEqual(opt["kappa"], 2.0)
        self.assertAlmostEqual(opt["low_over_scale"], 1.0)
        self.assertAlmostEqual(opt["high_over_scale"], 1.0)
        pieces = split_pieces(4.0, 16.0, 4.0, 1.0, 1.0)
        self.assertAlmostEqual(pieces["low"], 4.0)
        self.assertAlmostEqual(pieces["high"], 2.0)
        self.assertTrue(self.row["optimized_split_recovers_interpolation"])
        self.assertTrue(self.row["cs_sharp_on_single_shell"])
        self.assertTrue(self.row["L4_bound_formula_ok"])
        self.assertAlmostEqual(math.sqrt(4.0 * 16.0), 8.0)

    def test_locks(self):
        self.assertTrue(self.row["derivation_on_desk"])
        self.assertTrue(self.row["owned_interpolation_sits"])
        self.assertTrue(self.row["d1_d2_d3_retained_at_stated_scope"])
        self.assertTrue(self.row["subject_to_source_constant_domain_check"])
        self.assertTrue(self.row["correction_from_screenshots_not_fresh_verification"])
        self.assertTrue(self.row["d4_is_unresolved_pressure"])
        self.assertTrue(self.row["d5_remainder_must_be_cutoff_uniform"])
        self.assertTrue(self.row["d5_does_not_prove_every_estimate_needs_higher_norm"])
        self.assertTrue(self.row["L3_direction_not_proved_impossible"])
        self.assertTrue(self.row["no_budget_derived_in_this_audit"])
        self.assertTrue(self.row["no_new_mechanism_is_a_search_result"])
        self.assertFalse(self.row["nse_L3_closed_cutoff_uniform"])
        self.assertFalse(self.row["pressure_remainder_paid"])
        self.assertFalse(self.row["interesting_outcome_sits"])
        self.assertTrue(self.row["press_L3_is_not_u3"])
        self.assertTrue(self.row["lemma_A_unaltered"])
        self.assertTrue(self.row["lemma_B_open"])
        self.assertFalse(self.row["sits_as_useful_K"])
        self.assertFalse(self.row["sits_as_g4_death"])
        self.assertFalse(self.row["sits_as_ess_a_priori"])
        self.assertFalse(self.row["sits_as_beyond_ess"])
        self.assertFalse(self.row["sits_as_new_mechanism"])
        self.assertTrue(self.row["g4_stays_open"])
        self.assertTrue(self.row["do_not_invent_a_new_mechanism"])
        self.assertTrue(self.row["do_not_invent_a_bridge"])
        self.assertTrue(self.row["do_not_run_taylor_green"])
        self.assertTrue(self.row["do_not_glue_to_leftover_1"])


class U3AuditPageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("U3-DERIV.md", raw)
        self.assertIn("D1–D3 retained", raw)
        self.assertIn("not Serrin", raw)
        self.assertIn("L^4_t L^6", raw)
        self.assertIn("impossibility", raw)
        self.assertIn("G4 stays", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("Do not invent a new mechanism", raw)
        self.assertIn("PRESS.md", raw)
        self.assertIn("SBP.md", raw)
        self.assertIn("Escauriaza", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)
        self.assertNotIn("DA-NS-2 sits", raw)
        self.assertNotIn("the primitive is seated", text.lower())
        self.assertNotIn("ESS sits as an a priori", raw)
        self.assertNotIn("new regularity mechanism sits", text.lower())

    def test_deriv_page(self):
        raw = DERIV.read_text()
        text = _plain(DERIV)
        self.assertIn("Not a close", raw)
        self.assertIn("Implication chain", raw)
        self.assertIn("D1", raw)
        self.assertIn("D3hi", raw)
        self.assertIn("Galerkin commutator", raw)
        self.assertIn("growth-capable", raw)
        self.assertIn("Escauriaza", raw)
        self.assertIn("I6", raw)
        self.assertIn("is withdrawn", raw)
        self.assertIn("2/4+3/3=3/2", raw)
        self.assertIn("2/4+3/6=1", raw)
        self.assertIn("L^4_t L^6", raw)
        self.assertIn("not prove that every", raw)
        self.assertIn("do not establish", raw)
        self.assertIn("the missing", raw)
        self.assertIn("Not an impossibility", raw)
        self.assertNotIn("and is Serrin in", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("ESS sits as an a priori", raw)
        self.assertIn("U3-AUDIT.md", raw)

    def test_not_the_abc_page(self):
        self.assertIn("ABC", ABC.read_text())
        self.assertNotIn("U3-AUDIT.md", ABC.read_text())

    def test_pointers(self):
        self.assertIn("U3-AUDIT.md", PRESS.read_text())
        self.assertIn("U3-AUDIT.md", SIGN.read_text())
        self.assertIn("U3-AUDIT.md", RUN.read_text())
        self.assertIn("U3-AUDIT.md", CHAIN.read_text())
        self.assertIn("U3-DERIV.md", CHAIN.read_text())
        self.assertIn("U3-DERIV.md", TAPE.read_text())
        self.assertIn("U3-DERIV.md", DRIFT.read_text())
        for path in (
            SBP,
            WIDTH,
            RESET,
            LEDGER,
            DANS,
            DRIFT,
            INTERVAL,
            GEOM,
            LIFT,
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
            ENERGY,
            LDOOR,
            MNC,
            PATHWISE,
        ):
            self.assertIn("U3-AUDIT.md", path.read_text(), msg=str(path))
            self.assertIn("U3-DERIV.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
