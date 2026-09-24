"""Locks for the 24 Sep Heavy Fourier-triangle audit board."""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import hilbert_gram  # noqa: E402
from fourier_triangle_eq1_S_pq import EQUATION_1, prove_all as prove_eq1  # noqa: E402
from fourier_triangles_audit import prove_odd_Xprime  # noqa: E402

PACKET = ROOT / "packets" / "FOURIER-TRIANGLES-HEAVY-BOARD-2026-09-24.md"
LOCK = ROOT / "data" / "fourier_triangles_heavy_board_2026-09-24.json"
SPEC = ROOT / "data" / "l1_both_signs_fixture_spec.json"
EQ1 = ROOT / "scripts" / "fourier_triangle_eq1_S_pq.py"
HILBERT = ROOT / "scripts" / "hilbert_gram.py"


class TestFourierTrianglesHeavyBoard(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = PACKET.read_text(encoding="utf-8")
        cls.lock = json.loads(LOCK.read_text(encoding="utf-8"))
        cls.spec = json.loads(SPEC.read_text(encoding="utf-8"))

    def test_open_items_stay_open(self) -> None:
        self.assertFalse(self.lock["ns_solved"])
        self.assertEqual(self.lock["missing_theorem_17"], "OPEN")
        self.assertEqual(self.lock["L1_both_signs"], "OPEN")
        self.assertEqual(self.spec["status"], "OPEN")
        self.assertIn("NS not solved", self.page)

    def test_equation_1_is_seated(self) -> None:
        self.assertTrue(EQ1.is_file())
        self.assertIn("S_pq", EQUATION_1)
        proof = prove_eq1()
        self.assertTrue(proof["symbolic"]["S_identity"])
        self.assertTrue(proof["numeric"]["held"])
        self.assertFalse(proof["ns_solved"])

    def test_alpha98_not_invented(self) -> None:
        self.assertFalse(self.lock["alpha98"]["in_source"])
        self.assertFalse(self.lock["alpha98"]["computed_here"])
        self.assertEqual(
            self.lock["groups_expected_after_three_files"]["G3"],
            "PASS_only_if_alpha98_stamped",
        )

    def test_hilbert_gram_is_the_source(self) -> None:
        self.assertTrue(HILBERT.is_file())
        src = HILBERT.read_text(encoding="utf-8")
        self.assertIn("def relevant_primes", src)
        self.assertEqual(self.lock["hilbert_gram_source"], "scripts/hilbert_gram.py")
        primes = hilbert_gram.relevant_primes(2, 5)
        self.assertEqual(primes, [2, 5])
        self.assertNotIn(20, primes)
        self.assertTrue(all(hilbert_gram.is_prime(p) for p in primes))
        with self.assertRaises(ValueError):
            hilbert_gram.hilbert_symbol(2, 5, 20)

    def test_relevant_primes_callers_are_listed(self) -> None:
        callers = []
        for path in (ROOT / "scripts").glob("*.py"):
            if path.name == "hilbert_gram.py":
                continue
            text = path.read_text(encoding="utf-8")
            if "relevant_primes" in text:
                callers.append(f"scripts/{path.name}")
        for path in (ROOT / "tests").glob("test_fourier_triangles*.py"):
            text = path.read_text(encoding="utf-8")
            if "relevant_primes" in text:
                callers.append(f"tests/{path.name}")
        self.assertEqual(sorted(callers), sorted(self.lock["relevant_primes_callers"]))

    def test_sixteen_positive_part_untested(self) -> None:
        self.assertTrue(self.lock["sixteen_trajectory_S_was_zero"])
        self.assertTrue(self.lock["sixteen_positive_part_untested"])
        self.assertIn("N^2=12", self.lock["sixteen_rerun_on"])
        self.assertIn("never exercises", self.page)

    def test_both_signs_pre_run_conditions(self) -> None:
        ids = [item["id"] for item in self.spec["pre_run_required"]]
        self.assertEqual(
            ids, ["R2_scaling", "quotient_trivial_symmetries", "uniform_exact_signs"]
        )
        self.assertIn("u\\to-u", self.page.replace(" ", ""))
        self.assertIn("1.8", self.page)

    def test_odd_Xprime_factors(self) -> None:
        odd = prove_odd_Xprime()
        self.assertTrue(odd["factors"])
        self.assertTrue(odd["matches_50688"])
        self.assertTrue(self.lock["conventions_agree_with_13"])
        self.assertIn("8A^2(6A-133)", self.page.replace(" ", ""))

    def test_g4_stays_open_on_expected_board(self) -> None:
        self.assertEqual(self.lock["groups_expected_after_three_files"]["G4"], "OPEN")
        self.assertEqual(self.lock["groups_expected_after_three_files"]["G1"], "PASS")
        self.assertEqual(self.lock["groups_expected_after_three_files"]["G2"], "PASS")


if __name__ == "__main__":
    unittest.main()
