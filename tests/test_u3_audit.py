"""||u||_3 derivation is not on the desk; three gates; not a useful K."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from u3_audit import record, serrin_index  # noqa: E402

PAGE = ROOT / "docs" / "U3-AUDIT.md"
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
        self.assertTrue(self.row["energy_L4_L3_owned_by_energy"])
        self.assertTrue(self.row["energy_L4_L3_is_not_Serrin"])
        self.assertTrue(self.row["ess_is_the_only_Serrin_L3"])
        self.assertTrue(self.row["finite_p_L3_is_supercritical"])
        self.assertTrue(self.row["H12_embeds_L3"])
        self.assertFalse(self.row["L3_embeds_H12"])

    def test_locks(self):
        self.assertTrue(self.row["derivation_not_on_desk"])
        self.assertTrue(self.row["press_L3_is_not_u3"])
        self.assertTrue(self.row["lemma_A_unaltered"])
        self.assertTrue(self.row["lemma_B_open"])
        self.assertFalse(self.row["sits_as_useful_K"])
        self.assertFalse(self.row["sits_as_g4_death"])
        self.assertFalse(self.row["sits_as_ess_a_priori"])
        self.assertFalse(self.row["sits_as_beyond_ess"])
        self.assertTrue(self.row["g4_stays_open"])
        self.assertTrue(self.row["do_not_invent_the_u3_inequality"])
        self.assertTrue(self.row["do_not_invent_a_bridge"])
        self.assertTrue(self.row["do_not_run_taylor_green"])
        self.assertTrue(self.row["do_not_glue_to_leftover_1"])


class U3AuditPageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("is not on this desk", raw)
        self.assertIn("G4 stays", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("Do not invent the inequality", raw)
        self.assertIn("PRESS.md", raw)
        self.assertIn("SBP.md", raw)
        self.assertIn("Escauriaza", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)
        self.assertNotIn("DA-NS-2 sits", raw)
        self.assertNotIn("the primitive is seated", text.lower())
        self.assertNotIn("the derivation sits", text.lower())
        self.assertNotIn("ESS sits as an a priori", raw)

    def test_not_the_abc_page(self):
        self.assertIn("ABC", ABC.read_text())
        self.assertNotIn("U3-AUDIT.md", ABC.read_text())

    def test_pointers(self):
        self.assertIn("U3-AUDIT.md", PRESS.read_text())
        self.assertIn("U3-AUDIT.md", SIGN.read_text())
        self.assertIn("U3-AUDIT.md", RUN.read_text())
        self.assertIn("U3-AUDIT.md", CHAIN.read_text())
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


if __name__ == "__main__":
    unittest.main()
