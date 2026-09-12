"""Analytic-review score stays a score. Not a kill."""

from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lemma_star_cube_review import (  # noqa: E402
    C_BOX_FLOAT_REVIEW,
    C_BOX_FROM_M0,
    D0,
    E0,
    M0_CLAIMED,
    X0,
    Y0,
    Z0,
    run,
)

PAGE = ROOT / "docs" / "LEMMA-STAR-CUBE-REVIEW.md"


class LemmaStarCubeReviewTests(unittest.TestCase):
    def test_page_stays_open(self):
        text = PAGE.read_text()
        self.assertIn("**★ OPEN. NS not solved.", text)
        self.assertIn("Do not start H1.", text)
        self.assertIn("Do not stamp a kill.", text)
        self.assertIn("89567/134534400", text)
        self.assertIn("are **not**", text)
        self.assertIn("on this branch", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("falsifier-of-record", text)
        self.assertIn("this review did not kill ★", text)

    def test_quadratic_moments(self):
        self.assertEqual(E0, Fraction(736, 315))
        self.assertEqual(X0, Fraction(21536, 5775))
        self.assertEqual(Y0, Fraction(91342432, 14189175))
        self.assertEqual(Z0, Fraction(280364512, 23648625))
        self.assertEqual(D0, Z0 - Y0 * Y0 / X0)
        self.assertEqual(M0_CLAIMED, Fraction(89567, 134534400))
        self.assertAlmostEqual(float(C_BOX_FROM_M0), C_BOX_FLOAT_REVIEW, places=20)
        self.assertGreater(float(C_BOX_FROM_M0), 3e-8)
        self.assertLess(float(C_BOX_FROM_M0), 5e-8)

    def test_probe_scores(self):
        payload = run()
        rows = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(rows["LSrev_files_on_branch"]["verdict"], "fail")
        self.assertEqual(rows["LSrev_quad_moments"]["verdict"], "pass")
        self.assertEqual(rows["LSrev_reported_constants_clean"]["verdict"], "fail")
        self.assertEqual(rows["LSrev_N0_discrete"]["verdict"], "pass")
        self.assertEqual(rows["LSrev_M0_from_lock"]["verdict"], "fail")
        self.assertEqual(rows["LSrev_no_defect_35"]["verdict"], "fail")
        self.assertEqual(rows["LSrev_samples_unnecessary"]["verdict"], "fail")
        self.assertEqual(rows["LSrev_unrestricted_killed"]["verdict"], "fail")
        self.assertEqual(rows["LSrev_ns_h1"]["verdict"], "fail")
        self.assertEqual(payload["domain_verdict"], "open")
        self.assertTrue(payload["meta"]["lemma_star_open"])
        self.assertFalse(payload["meta"]["kill"])
        self.assertFalse(payload["meta"]["files_on_branch"])
        self.assertTrue(payload["continuum"]["L0_is_10_E0"])
        self.assertTrue(payload["continuum"]["review_float_matches_corrected"])


if __name__ == "__main__":
    unittest.main()
