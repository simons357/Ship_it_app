"""SuperGrok PR-24 review: score the table, do not stamp 4/3 a theorem."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "PR24-SUPERGROK-REVIEW.md"
KILL = ROOT / "docs" / "LEMMA-STAR-GROWING-LAYER.md"
MATH_KILL = ROOT / "docs" / "math" / "ns_attacks" / "LEMMA_STAR_GROWING_LAYER_COUNTEREXAMPLE.md"
MATH_BOUND = ROOT / "docs" / "math" / "ns_attacks" / "ATTACK_9D_FULL_SUPPORT_BOUND.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"


def dn3_count(n: int) -> int:
    return sum(
        1
        for a in range(-n, n + 1)
        for b in range(-n, n + 1)
        if abs(a + b) <= n
    )


class Pr24SuperGrokReviewTests(unittest.TestCase):
    def test_page_keeps_four_thirds_claimed(self):
        text = PAGE.read_text()
        self.assertIn("CLAIMED", text)
        self.assertIn("2/3", text)
        self.assertIn("write-up example", text)
        self.assertIn("KILLED", text)
        self.assertIn("two-plane", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("hygiene", text.lower())
        self.assertIn("Theorem stamp **NO**", text)
        self.assertIn("8/3", text)

    def test_killed_inequality_and_side_conditions_sit(self):
        kill = KILL.read_text()
        self.assertIn("no finite", kill)
        self.assertIn("C_{\\mathrm{geom}}", kill)
        self.assertIn("Side-conditions from the reason page", kill)
        self.assertIn("mathrm{Im}", kill)
        self.assertIn("D_n^3", kill)

    def test_three_line_sum_matches_count(self):
        math = MATH_KILL.read_text()
        self.assertIn("3n^2+3n+1", math)
        self.assertIn("sum_{a=0}", math.replace("\\", ""))
        for n in range(1, 21):
            self.assertEqual(dn3_count(n), 3 * n * n + 3 * n + 1)

    def test_two_plane_is_isolated_and_claimed(self):
        text = MATH_BOUND.read_text()
        self.assertIn("two-plane incidence", text)
        self.assertIn("CLAIMED", text)
        self.assertIn("r=-p", text.replace("\\", ""))
        self.assertIn("Geometry on one input shell", text)
        self.assertIn("8/3", text)
        self.assertIn("lambda", text.replace("\\", ""))
        tape = TAPE.read_text()
        self.assertIn("PR24-SUPERGROK-REVIEW.md", tape)
        self.assertIn("keep exact-shell", tape)


if __name__ == "__main__":
    unittest.main()
