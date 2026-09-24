"""Locks for the 24 Sep Heavy Fourier-triangle audit board."""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fourier_triangle_eq1_S_pq import EQUATION_1, prove_all as prove_eq1  # noqa: E402
from fourier_triangles_audit import is_prime, relevant_primes  # noqa: E402

PACKET = ROOT / "packets" / "FOURIER-TRIANGLES-HEAVY-BOARD-2026-09-24.md"
LOCK = ROOT / "data" / "fourier_triangles_heavy_board_2026-09-24.json"
EQ1 = ROOT / "scripts" / "fourier_triangle_eq1_S_pq.py"


class TestFourierTrianglesHeavyBoard(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = PACKET.read_text(encoding="utf-8")
        cls.lock = json.loads(LOCK.read_text(encoding="utf-8"))

    def test_open_items_stay_open(self) -> None:
        self.assertFalse(self.lock["ns_solved"])
        self.assertEqual(self.lock["missing_theorem_17"], "OPEN")
        self.assertEqual(self.lock["L1_both_signs"], "OPEN")
        self.assertEqual(self.lock["lemma_star"], "OPEN")
        self.assertIn("OPEN", self.page)
        self.assertIn("NS not solved", self.page)

    def test_equation_1_is_seated(self) -> None:
        self.assertTrue(EQ1.is_file())
        self.assertIn("S_pq", EQUATION_1)
        self.assertIn("e1", EQUATION_1)
        self.assertIn("e2", EQUATION_1)
        proof = prove_eq1()
        self.assertTrue(proof["symbolic"]["S_identity"])
        self.assertTrue(proof["numeric"]["held"])
        self.assertFalse(proof["ns_solved"])
        self.assertIn("fourier_triangle_eq1_S_pq.py", self.lock["equation_1"]["now_seated"])

    def test_alpha98_not_invented(self) -> None:
        self.assertFalse(self.lock["alpha98"]["in_source"])
        self.assertFalse(self.lock["alpha98"]["computed_here"])
        self.assertIn("Not computed", self.page)

    def test_relevant_primes_never_returns_composites(self) -> None:
        # Gram (2,3,1): Δ=5, 2aΔ=20. Primes are {2,5}, not {20}.
        primes = relevant_primes(2, 5)
        self.assertEqual(primes, [2, 5])
        self.assertNotIn(20, primes)
        self.assertTrue(all(is_prime(p) for p in primes))
        self.assertTrue(self.lock["relevant_primes_must_not_return_composites"])

    def test_schulze_pillot_blocked(self) -> None:
        self.assertEqual(self.lock["schulze_pillot"], "BLOCKED-ON-SOURCE")
        self.assertIn("BLOCKED-ON-SOURCE", self.page)

    def test_sixteen_slack_recorded(self) -> None:
        self.assertTrue(self.lock["sixteen_checks_used_random_not_adversarial"])
        self.assertIn("random fields", self.page)


if __name__ == "__main__":
    unittest.main()
