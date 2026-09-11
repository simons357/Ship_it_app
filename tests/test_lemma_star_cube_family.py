"""Cube-family score stays a score. Not a kill."""

from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lemma_star_cube_family import C_BOX, C_BOX_NUM, C_BOX_DEN, run  # noqa: E402

PAGE = ROOT / "docs" / "LEMMA-STAR-CUBE.md"


class LemmaStarCubeFamilyTests(unittest.TestCase):
    def test_page_stays_open(self):
        text = PAGE.read_text()
        self.assertIn("**★ OPEN. NS not solved.", text)
        self.assertIn("Do not start H1.", text)
        self.assertIn("Do not stamp a kill.", text)
        self.assertIn("Do not rewrite the boxed claim.", text)
        self.assertIn("4959/32768", text)
        self.assertIn("not** Fourier dilation", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("falsifier-of-record", text)
        self.assertIn("unrestricted ★ is OPEN", text)

    def test_claimed_c_box_fraction_is_not_the_float(self):
        self.assertAlmostEqual(C_BOX, C_BOX_NUM / C_BOX_DEN, places=20)
        self.assertLess(C_BOX, 1e-9)
        self.assertGreater(C_BOX, 1e-10)
        # Dump also writes ~3.97e-8. Those two SuperGrok numbers disagree.
        self.assertLess(C_BOX * 50, 3.9677e-8)

    def test_probe_scores(self):
        payload = run(nmax=2)
        rows = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(rows["LScube_named"]["verdict"], "pass")
        self.assertEqual(rows["LScube_lock_first"]["verdict"], "pass")
        self.assertEqual(rows["LScube_div_real"]["verdict"], "pass")
        self.assertEqual(rows["LScube_amp_odd"]["verdict"], "pass")
        self.assertEqual(rows["LScube_screenshot_stamp"]["verdict"], "fail")
        self.assertEqual(rows["LScube_bernstein_every_n"]["verdict"], "fail")
        self.assertEqual(rows["LScube_ns_solved"]["verdict"], "fail")
        self.assertEqual(rows["LScube_unrestricted_killed"]["verdict"], "fail")
        self.assertEqual(payload["domain_verdict"], "open")
        self.assertTrue(payload["meta"]["lemma_star_open"])
        self.assertFalse(payload["meta"]["kill"])
        self.assertTrue(payload["meta"]["new_family_arrived"])
        self.assertFalse(payload["meta"]["screenshots_are_a_stamp"])
        self.assertFalse(payload["meta"]["h1_started"])

    def test_n2_matches_dump_ratio_and_locked_tc(self):
        payload = run(nmax=2)
        n2 = payload["rows"][1]
        self.assertEqual(n2["n"], 2)
        self.assertTrue(n2["setup"]["ok"])
        self.assertTrue(n2["Ds_match"])
        self.assertTrue(n2["amp_flat"])
        self.assertTrue(n2["Tc_odd"])
        self.assertEqual(n2["N"], 0.0)
        self.assertAlmostEqual(n2["T_c"], float(Fraction(4959, 32768)), places=12)
        self.assertAlmostEqual(n2["R_star"], 8.062432073094823e-07, places=20)
        self.assertLess(n2["R_star"], 1e-5)
        n1 = payload["rows"][0]
        self.assertEqual(n1["T_c"], 0.0)
        self.assertEqual(n1["R_star"], 0.0)


if __name__ == "__main__":
    unittest.main()
