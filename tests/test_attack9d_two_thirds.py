"""Three-shear floor K=2/3. Not the 16/9 bound. NS not solved."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.attack9d_two_thirds import run  # noqa: E402

PAGE = ROOT / "docs" / "ATTACK-9D-TWO-THIRDS.md"
BOUND = ROOT / "docs" / "ATTACK-9D-FULL-SUPPORT-BOUND.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"


class Attack9DTwoThirdsTests(unittest.TestCase):
    def test_page_is_a_floor_not_the_ceiling(self):
        text = PAGE.read_text()
        self.assertIn("sin y", text)
        self.assertIn("2/3", text)
        self.assertIn("floor", text.lower())
        self.assertIn("16/9", text)
        self.assertIn("CLAIMED", text)
        self.assertIn("write-up example", text)
        self.assertIn("by hand", text)
        self.assertIn("random", text.lower())
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("hygiene", text.lower())

    def test_evaluator_hits_two_thirds(self):
        payload = run()
        self.assertTrue(payload["ok"])
        self.assertAlmostEqual(payload["K"], 2.0 / 3.0, places=12)
        self.assertGreater(payload["K"], 0.641)
        self.assertLess(payload["K"], 16.0 / 9.0)
        self.assertFalse(payload["is_C0"])
        self.assertFalse(payload["proves_16_over_9"])
        self.assertFalse(payload["ns_solved"])
        self.assertEqual(payload["exact_shell_9d"], "CLAIMED")

    def test_bound_page_and_tape_keep_16_over_9_claimed(self):
        bound = BOUND.read_text()
        tape = TAPE.read_text()
        self.assertIn("2/3", bound)
        self.assertIn("CLAIMED", bound)
        self.assertIn("write-up example", bound)
        self.assertIn("written bound on exact-shell", bound)
        self.assertIn("regularity close", bound)
        self.assertIn("global regularity", bound)
        self.assertIn("Geometry on one input shell", bound)
        self.assertIn("8/3", bound)
        self.assertIn("lambda", bound.replace("\\", ""))
        self.assertIn("Hermitian", bound)
        self.assertIn("Constraint set", bound)
        self.assertIn("internal check", bound)
        self.assertIn("no extra", bound)
        self.assertIn("ATTACK-9D-TWO-THIRDS.md", tape)
        self.assertIn("2/3", tape)
        self.assertIn("write-up example", tape)
        self.assertIn("regularity close", tape)
        self.assertIn("internal", tape.lower())
        self.assertIn("envelope", tape.lower())

    def test_claimed_cubic_max_is_16_over_9_at_eight_thirds(self):
        def f(x: float) -> float:
            return 0.75 * x * x * (1.0 - x / 4.0)

        self.assertAlmostEqual(f(8.0 / 3.0), 16.0 / 9.0, places=12)
        self.assertAlmostEqual(f(4.0), 0.0, places=12)
        grid = [i / 300.0 for i in range(1, 1201)]
        self.assertLessEqual(max(f(x) for x in grid), 16.0 / 9.0 + 1e-9)


if __name__ == "__main__":
    unittest.main()
