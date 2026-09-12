"""Family-check score stays a score. Not a kill."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lemma_star_family_check import run  # noqa: E402

PAGE = ROOT / "docs" / "LEMMA-STAR-FAMILY-CHECK.md"


class LemmaStarFamilyCheckTests(unittest.TestCase):
    def test_page_stays_open(self):
        text = PAGE.read_text()
        self.assertIn("**★ OPEN. NS not solved.", text)
        self.assertIn("Do not start H1.", text)
        self.assertIn("Do not stamp a kill.", text)
        self.assertIn("well-posed on paper", text)
        self.assertIn("Fourier dilation", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("falsifier-of-record", text)
        self.assertIn("this paste did not kill ★", text)

    def test_probe_scores(self):
        payload = run(seed=3)
        rows = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(rows["LSfam_lock_first"]["verdict"], "pass")
        self.assertEqual(rows["LSfam_div_real"]["verdict"], "pass")
        self.assertEqual(rows["LSfam_dilation_flat"]["verdict"], "pass")
        self.assertEqual(rows["LSfam_wellposed_kills"]["verdict"], "fail")
        self.assertEqual(rows["LSfam_small_lattice_kills"]["verdict"], "fail")
        self.assertEqual(rows["LSfam_unrestricted_killed"]["verdict"], "fail")
        self.assertEqual(payload["domain_verdict"], "open")
        self.assertTrue(payload["meta"]["lemma_star_open"])
        self.assertFalse(payload["meta"]["kill"])
        self.assertFalse(payload["meta"]["new_family_arrived"])
        self.assertFalse(payload["meta"]["h1_started"])

    def test_locked_families_finite_and_flat(self):
        payload = run(seed=7)
        for row in payload["families"]:
            self.assertTrue(row["setup"]["ok"], row)
            self.assertTrue(row["Ds_match"])
            self.assertTrue(row["dilate_flat"])
            self.assertTrue(row["amp_flat"])
            self.assertTrue(row["Tc_odd"])
            self.assertGreater(row["R_star_unsigned"], 0.0)
            self.assertLess(row["R_star_unsigned"], 2.0)
            if row["T_c"] < 0:
                self.assertEqual(row["R_star"], 0.0)
                self.assertGreater(row["R_star_reverse"], 0.0)


if __name__ == "__main__":
    unittest.main()
