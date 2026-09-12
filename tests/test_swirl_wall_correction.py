"""Wall correction: identities sit; occupation from the detector is out."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from swirl_wall_correction import (  # noqa: E402
    classify_detector_paragraph,
    compression_on_zdot,
    if_mu_prime,
    run,
    wall_rhs,
)
from estimate_audit import classify_paragraph  # noqa: E402

PAGE = ROOT / "docs" / "SWIRL-WALL-CORRECTION.md"
SHELL = ROOT / "docs" / "AXISYM-SHELL.md"


class SwirlWallCorrectionTests(unittest.TestCase):
    def test_page_first_sentence(self):
        text = PAGE.read_text()
        self.assertIn("Axisymmetric-with-swirl Navier–Stokes", text)
        self.assertIn("F=u^\\theta/r", text)
        self.assertIn("G=\\omega^\\theta/r", text)
        self.assertIn("T_{j\\leftarrow j}", text)
        self.assertIn("Occupation decay from the detector is", text)
        self.assertIn("withdrawn", text)
        self.assertIn("p(1-d)", text)
        self.assertIn("(u^r)_-", text)
        self.assertIn("\\sqrt{\\nu h", text)
        self.assertIn("good-set estimate remains fixed", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("coherence viscosity", text)

    def test_page_passes_discard_filter(self):
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])

    def test_if_cancels_compression(self):
        for p, d in ((2.0, 0.0), (2.0, 0.5), (3.0, 0.25)):
            self.assertAlmostEqual(compression_on_zdot(p, d) + if_mu_prime(p, d), 0.0)
        # Wrong-sign IF would add, not cancel.
        self.assertGreater(compression_on_zdot(2.0, 0.0) * if_mu_prime(2.0, 0.0) * -1.0, 0.0)

    def test_wall_has_square_root(self):
        rhs = wall_rhs(1.0, 0.01, 1.0)
        raw = 1.0 * 0.01 * math.log(math.log(math.e**math.e * 1.0 / 0.01))
        self.assertAlmostEqual(rhs, 2.0 * math.sqrt(raw))
        self.assertNotAlmostEqual(rhs, 2.0 * raw)

    def test_detector_classifier(self):
        clean = classify_detector_paragraph(
            "F=u^theta/r; G=omega^theta/r; wall is a time-window if; occupation withdrawn."
        )
        self.assertTrue(clean["allowed_in_estimate"])
        bad = classify_detector_paragraph(
            "The detector establishes occupation decay via a five-dimensional spatial occupation bound."
        )
        self.assertFalse(bad["allowed_in_estimate"])

    def test_probe_scores(self):
        payload = run()
        rows = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(rows["SWC_F_G"]["verdict"], "pass")
        self.assertEqual(rows["SWC_IF"]["verdict"], "pass")
        self.assertEqual(rows["SWC_identity"]["verdict"], "pass")
        self.assertEqual(rows["SWC_wall_time"]["verdict"], "pass")
        self.assertEqual(rows["SWC_good_set"]["verdict"], "pass")
        self.assertEqual(rows["SWC_occ_from_detector"]["verdict"], "fail")
        self.assertEqual(rows["SWC_five_d_occupation"]["verdict"], "fail")
        self.assertEqual(rows["SWC_remainder"]["verdict"], "fail")
        self.assertEqual(rows["SWC_page_clean"]["verdict"], "pass")
        self.assertEqual(rows["SWC_ns_solved"]["verdict"], "fail")
        self.assertEqual(payload["domain_verdict"], "open")
        self.assertEqual(payload["meta"]["F"], "u^theta/r")
        self.assertEqual(payload["meta"]["G"], "omega^theta/r")
        self.assertEqual(payload["meta"]["occupation_from_detector"], "withdrawn")
        self.assertEqual(payload["meta"]["good_set"], "fixed")
        self.assertFalse(payload["meta"]["source_note_on_branch"])
        self.assertFalse(payload["wall"]["spatial_occupation"])
        self.assertIn("SWIRL-WALL-CORRECTION.md", SHELL.read_text())


if __name__ == "__main__":
    unittest.main()
