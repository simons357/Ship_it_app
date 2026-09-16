"""Guardrails for the boxed SND persistence statement (P)."""

from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.snd_persistence_test as snd  # noqa: E402


CLAR = ROOT / "docs" / "ns-review" / "SND-CLARIFICATION.md"
PERS = ROOT / "docs" / "ns-review" / "SND-PERSISTENCE.md"


class TestSndPersistence(unittest.TestCase):
    def test_sources_present(self) -> None:
        self.assertTrue(CLAR.is_file(), f"missing {CLAR}")
        self.assertTrue(PERS.is_file(), f"missing {PERS}")
        clar = CLAR.read_text(encoding="utf-8")
        pers = PERS.read_text(encoding="utf-8")
        self.assertIn("The original Theorem H is withdrawn", clar)
        self.assertIn("wrong-sided", clar)
        self.assertIn("Do **not** repair Theorem H", clar)
        self.assertIn("Statement (P): **false**", pers)
        self.assertIn("4^{j_*}", pers)
        self.assertIn("Family H", pers)
        self.assertNotIn("Clay Millennium solved", clar + pers)
        keep = ROOT / "docs" / "ns-review" / "SND-WHAT-IS-KEPT.md"
        if keep.is_file():
            text = keep.read_text(encoding="utf-8")
            self.assertIn("Do **not** repair it", text)
            self.assertIn("Persistence (P)", text)
            self.assertIn("**False**", text)

    def test_paraproduct_exhausts(self) -> None:
        snd.assert_paraproduct_exhausts()

    def test_a2_leftover(self) -> None:
        snd.assert_a2_leftover_unbounded()

    def test_family_h_kills_p(self) -> None:
        snd.assert_family_h_kills_p(
            candidate_times=(1.0, 1.0e-3, 1.0e-6),
        )

    def test_high_tail_does_not_kill_p(self) -> None:
        snd.assert_high_tail_does_not_kill_p()

    def test_rho_star_one_is_not_family_h(self) -> None:
        snd.assert_rho_star_one_survives_heat()

    def test_choose_L_plateau(self) -> None:
        for rho_star in (0.2, 0.5, 0.9, 0.99):
            l = snd.choose_L(rho_star)
            self.assertLess(1.0 / (l - 1), 0.5 * rho_star)
            self.assertGreater(rho_star, 1.0 / l)

    def test_dini_floor_matches_exact_dot_at_unique_peak(self) -> None:
        shells = snd.family_h(0.5, 1.0, k=12)
        floor, rdot = snd.dminus_rho_floor_f0(shells, nu=1.0)
        self.assertLessEqual(floor, rdot + 1.0e-12)
        self.assertLess(floor, 0.0)
        # Rest of mass at much lower frequency ⇒ floor ≈ ρ̇ ≈ −2ν 4^K ρ(1−ρ).
        self.assertAlmostEqual(floor, rdot, places=6)


if __name__ == "__main__":
    unittest.main()
