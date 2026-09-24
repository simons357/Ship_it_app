"""Finite-N BOTH SIGNS is printed; persistence OPEN; not a useful K."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from sign_run import record  # noqa: E402

PAGE = ROOT / "docs" / "SIGN-RUN.md"
GATE = ROOT / "docs" / "SIGN-GATE.md"
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
SEEDS = ROOT / "results" / "A_N_plus_seeds.json"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "").replace("*", "")


class SignRunArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = record()

    def test_locks(self):
        self.assertTrue(self.row["helical_basis_ok"])
        self.assertTrue(self.row["expansion_ok"])
        self.assertTrue(self.row["gate_unaltered"])
        self.assertTrue(self.row["lemma_A_unaltered"])
        self.assertTrue(self.row["lemma_B_open"])
        self.assertTrue(self.row["BOTH_SIGNS_on_printed_range"])
        self.assertTrue(self.row["BOTH_SIGNS_at_every_printed_N_with_neighbors"])
        self.assertTrue(self.row["ZERO_ONLY_homochiral_on_printed_range"])
        self.assertFalse(self.row["NO_NEIGHBOR_appeared"])
        self.assertTrue(self.row["persistence_open"])
        self.assertTrue(self.row["finite_N_is_not_persistence"])
        self.assertTrue(self.row["universal_depletion_not_killed"])
        self.assertTrue(self.row["static_closure_not_stopped"])
        self.assertTrue(self.row["A_N_plus_saved_finite_N_only"])
        self.assertGreaterEqual(self.row["n_seeds"], 2)
        self.assertTrue(self.row["i3_bridge_not_seated"])
        self.assertFalse(self.row["sits_as_useful_K"])
        self.assertFalse(self.row["sits_as_g4_death"])
        self.assertTrue(self.row["g4_stays_open"])
        self.assertTrue(self.row["do_not_invent_a_bridge"])
        self.assertTrue(self.row["do_not_run_taylor_green"])
        self.assertTrue(self.row["do_not_mix_heavy"])
        self.assertTrue(self.row["do_not_glue_to_leftover_1"])

    def test_remainder_shrinks(self):
        rows = self.row["by_N"]
        first = rows[0]["mean_abs_R2_over_L1"]
        last = rows[-1]["mean_abs_R2_over_L1"]
        self.assertIsNotNone(first)
        self.assertIsNotNone(last)
        self.assertLess(last, first)
        self.assertLess(last, 0.02)

    def test_seeds_are_complete(self):
        self.assertTrue(SEEDS.is_file())
        for seed in self.row["seeds"]:
            self.assertIn("p", seed)
            self.assertIn("q", seed)
            self.assertIn("k", seed)
            self.assertIn("helicity", seed)
            self.assertIn("polarizations", seed)
            self.assertIn("amplitudes", seed)
            self.assertGreaterEqual(abs(seed["rho"]), 0.05)


class SignRunPageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        raw = PAGE.read_text()
        text = _plain(PAGE)
        self.assertIn("Not a close", raw)
        self.assertIn("Persistence stays OPEN", raw)
        self.assertIn("is not killed", raw)
        self.assertIn("G4 stays", raw)
        self.assertIn("Do not start leftover 1", raw)
        self.assertIn("Do not invent a bridge", raw)
        self.assertIn("SIGN-GATE.md", raw)
        self.assertIn("A_N_plus_seeds.json", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("B★ sits", raw)
        self.assertNotIn("9D is claimed", raw)
        self.assertNotIn("DA-NS-2 sits", raw)
        self.assertNotIn("the primitive is seated", text.lower())
        self.assertNotIn("the bridge is seated", text.lower())
        self.assertNotIn("persistence sits", text.lower())

    def test_not_the_abc_page(self):
        self.assertIn("ABC", ABC.read_text())
        self.assertNotIn("SIGN-RUN.md", ABC.read_text())

    def test_pointers(self):
        self.assertIn("SIGN-RUN.md", GATE.read_text())
        self.assertIn("SIGN-RUN.md", PRESS.read_text())
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
            self.assertIn("SIGN-RUN.md", path.read_text(), msg=str(path))


if __name__ == "__main__":
    unittest.main()
