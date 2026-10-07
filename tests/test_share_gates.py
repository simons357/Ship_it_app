"""Share-Gate A/B: lattice identities sit; kill not stamped; not Track A/B."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from share_gates import record, triad  # noqa: E402

PAGE = ROOT / "docs" / "SHARE-GATES.md"
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
U3 = ROOT / "docs" / "U3-AUDIT.md"
ABC = ROOT / "docs" / "CS-REMAINDER.md"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "").replace("*", "")


class ShareGatesArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_triad_345(self):
        t = triad(5, 4, 3)
        self.assertEqual(t["sum"], (0, 0, 0))
        self.assertEqual(t["x"], 10)
        self.assertEqual(t["y"], 25)
        self.assertEqual(t["z"], 25)
        self.assertEqual(t["p_norm2"], t["x"])
        self.assertEqual(t["q_norm2"], t["y"])
        self.assertEqual(t["r_norm2"], t["z"])
        self.assertEqual(t["pxq_abs"], 15)
        self.assertEqual(t["Delta"], 225)
        self.assertTrue(t["x_le_y_le_z"])

    def test_locks(self):
        self.assertTrue(self.row["lattice_triad_identities_sit"])
        self.assertTrue(self.row["not_a_close"])
        self.assertTrue(self.row["star_stays_killed"])
        self.assertTrue(self.row["not_track_A"])
        self.assertTrue(self.row["not_track_B"])
        self.assertTrue(self.row["do_not_merge_letters"])
        self.assertFalse(self.row["share_gate_A_kill_stamped"])
        self.assertFalse(self.row["frozen_rule_from_original_shell_estimate"])
        self.assertFalse(self.row["restricted_pythagorean_count_seated"])
        self.assertFalse(self.row["W_N_log_divergence_seated"])
        self.assertTrue(self.row["share_gate_B_open"])
        self.assertFalse(self.row["share_gate_B_waits_for_A"])
        self.assertTrue(self.row["share_gate_B_is_not_prove_regularity"])
        self.assertFalse(self.row["share_gate_B_schematic_derived"])
        self.assertTrue(self.row["kill_would_not_prove_regularity"])
        self.assertTrue(self.row["do_not_revive_K_sqrt_E"])
        self.assertTrue(self.row["do_not_start_leftover_1"])
        self.assertTrue(self.row["sign_gate_unaltered"])
        self.assertFalse(self.row["sits_as_useful_K"])
        self.assertFalse(self.row["sits_as_g4_death"])
        self.assertTrue(self.row["g4_stays_open"])
        self.assertTrue(self.row["not_a_thirteenth_leftover"])
        self.assertTrue(self.row["do_not_invent_a_bridge"])
        self.assertTrue(all(s["ok"] for s in self.row["samples"]))


class ShareGatesPageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("Share-Gate B is OPEN", raw)
        self.assertIn("Do not merge letters", raw)
        self.assertIn("Not Track A", raw)
        self.assertIn("construct", raw)
        self.assertIn("L_{z_j}", raw)
        self.assertIn("not seated", raw)
        self.assertIn("Not “prove", raw)
        self.assertIn("ENERGY-K.md", raw)
        self.assertIn("C10-CHAIN.md", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("G4 stays", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("DA-NS-2 sits", raw)
        self.assertNotIn("the kill sits", text.lower())
        self.assertNotIn("W_N sits", raw)
        self.assertNotIn("regularity sits", text.lower())

    def test_not_the_abc_page(self):
        self.assertIn("ABC", ABC.read_text())
        self.assertNotIn("SHARE-GATES.md", ABC.read_text())

    def test_pointers(self):
        self.assertIn("SHARE-GATES.md", U3.read_text())
        self.assertIn("SHARE-GATES.md", SIGN.read_text())
        self.assertIn("SHARE-GATES.md", CHAIN.read_text())
        self.assertIn("SHARE-GATES.md", TAPE.read_text())
        self.assertIn("SHARE-GATES.md", DRIFT.read_text())
        for path in (
            PRESS,
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
            RUN,
        ):
            self.assertIn("SHARE-GATES.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
