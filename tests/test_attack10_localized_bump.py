"""Attack 10: localized bump kills static uniform R★."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.attack10_localized_bump import (  # noqa: E402
    evaluate_family,
    r_star,
    run,
    sign_flip_check,
    single_shell_vacuous,
)

SOT = ROOT / "docs" / "math" / "ns_attacks" / "ATTACK_10_LOCALIZED_BUMP.md"
PACKET = ROOT / "packets" / "ATTACK-10-LOCALIZED-BUMP-2026-09-24.md"
SCRIPT = ROOT / "scripts" / "ns_attacks" / "attack10_localized_bump.py"


class Attack10RecordTests(unittest.TestCase):
    def test_sources_present(self) -> None:
        self.assertTrue(SOT.is_file(), f"missing {SOT}")
        self.assertTrue(PACKET.is_file(), f"missing {PACKET}")
        self.assertTrue(SCRIPT.is_file(), f"missing {SCRIPT}")

    def test_doc_kills_static_star_and_does_not_solve_ns(self) -> None:
        text = SOT.read_text(encoding="utf-8")
        self.assertIn("★ dead as a static bound", text)
        self.assertIn(r"\ell^{-3}", text)
        self.assertIn("NS not solved", text)
        self.assertIn("D_s=0", text)
        self.assertIn("16/9", text)
        self.assertIn("concentrating bump", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay Statement B is closed", text)
        packet = PACKET.read_text(encoding="utf-8")
        self.assertIn("KILLED", packet)
        self.assertIn("Not a close", packet)


class Attack10VacuousAndSignTests(unittest.TestCase):
    def test_single_shell_forces_tc_zero(self) -> None:
        vac = single_shell_vacuous(n=16)
        self.assertAlmostEqual(vac["Tc"], 0.0, places=12)
        self.assertLess(abs(vac["Ds"]), 1e-10)
        self.assertAlmostEqual(vac["Lambda"], 1.0, places=10)

    def test_sign_flip_reverses_tc_only(self) -> None:
        flip = sign_flip_check(n=32, ell=0.55, seed=20260924)
        self.assertLess(flip["rel_Tc_sum"], 1e-12)
        self.assertLess(flip["rel_Ds"], 1e-12)
        self.assertGreater(abs(flip["Tc_plus"]), 1e-8)


class Attack10ScalingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = evaluate_family(n=32, widths=(0.70, 0.55), seed=20260924)

    def test_positive_stretch_and_growing_rstar(self) -> None:
        self.assertEqual(len(self.rows), 2)
        wide, narrow = self.rows
        self.assertGreater(wide.Tc, 0.0)
        self.assertGreater(narrow.Tc, 0.0)
        self.assertGreater(narrow.R_star, wide.R_star)
        self.assertGreater(narrow.Tc, wide.Tc)

    def test_rstar_ell3_is_stable(self) -> None:
        wide, narrow = self.rows
        self.assertGreater(wide.R_star_ell3, 0.0)
        rel = abs(wide.R_star_ell3 - narrow.R_star_ell3) / wide.R_star_ell3
        self.assertLess(rel, 2e-2)

    def test_tc_scales_like_ell_to_minus_five(self) -> None:
        wide, narrow = self.rows
        predicted = wide.Tc * (wide.ell / narrow.ell) ** 5
        rel = abs(narrow.Tc - predicted) / abs(predicted)
        self.assertLess(rel, 3e-2)

    def test_rstar_helper_uses_positive_part(self) -> None:
        self.assertEqual(r_star(-1.0, 1.0, 1.0, 1.0), 0.0)
        self.assertEqual(r_star(2.0, 1.0, 1.0, 1.0), 4.0)

    def test_run_payload_does_not_claim_ns(self) -> None:
        payload = run(n=32, widths=(0.70, 0.55), seed=20260924)
        self.assertIs(payload["ns_solved"], False)
        self.assertEqual(payload["verdict"], "STATIC_UNIFORM_RSTAR_DEAD")
        self.assertEqual(payload["lemma_star"], "KILLED_AS_STATIC_BOUND")
        self.assertIn("NS is not solved", payload["note"])


if __name__ == "__main__":
    unittest.main()
