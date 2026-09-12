"""Swirl probe prints ρ_j on the class. It does not close the estimate."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from axisym_swirl_probe import (  # noqa: E402
    compact_swirl,
    rotate_z90_about_axis,
    run,
)
from estimate_audit import classify_paragraph  # noqa: E402

PAGE = ROOT / "docs" / "AXISYM-SWIRL-PROBE.md"
ESTIMATE = ROOT / "docs" / "AXISYM-SHELL.md"


class AxisymSwirlProbeTests(unittest.TestCase):
    def test_page_first_sentence(self):
        text = PAGE.read_text()
        self.assertIn("Axisymmetric-with-swirl Navier–Stokes", text)
        self.assertIn("T_{j\\leftarrow j}", text)
        self.assertIn("[no extra field]", text)
        self.assertIn("**Not a close. NS not solved.", text)
        self.assertIn("[ρ] not assumed", text)
        self.assertIn("local-remainder occupancy", text)
        self.assertIn("Occupation from the detector", text)
        self.assertIn("withdrawn", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("coherence viscosity", text)
        self.assertNotIn("gematria", text)
        self.assertIn("2-D", text)

    def test_page_passes_discard_filter(self):
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])

    def test_continuum_rotation(self):
        u = compact_swirl(24)
        rot = rotate_z90_about_axis(u)
        num = float(((u - rot) ** 2).mean())
        den = float((u**2).mean()) + 1e-30
        self.assertLess(num / den, 1e-28)

    def test_probe_scores(self):
        payload = run(n=24)
        rows = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(rows["ASW_class_field"]["verdict"], "pass")
        self.assertEqual(rows["ASW_pairing"]["verdict"], "pass")
        self.assertEqual(rows["ASW_split"]["verdict"], "pass")
        self.assertEqual(rows["ASW_rho_printed"]["verdict"], "pass")
        self.assertEqual(rows["ASW_alpha_separate"]["verdict"], "pass")
        self.assertEqual(rows["ASW_occ_printed"]["verdict"], "pass")
        self.assertEqual(rows["ASW_occ_class"]["verdict"], "fail")
        self.assertEqual(rows["ASW_remainder"]["verdict"], "fail")
        self.assertEqual(rows["ASW_rho_class"]["verdict"], "fail")
        self.assertEqual(rows["ASW_page_clean"]["verdict"], "pass")
        self.assertEqual(rows["ASW_ns_solved"]["verdict"], "fail")
        self.assertEqual(payload["domain_verdict"], "open")
        self.assertTrue(payload["meta"]["estimate_open"])
        self.assertFalse(payload["meta"]["lambda_prime_sign_quoted"])
        self.assertTrue(payload["meta"]["occupancy_scored"])
        self.assertFalse(payload["meta"]["h1_started"])
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        by_name = {f["name"]: f for f in payload["fields"]}
        self.assertIn("pure_swirl", by_name)
        self.assertIn("swirl_meridional_m1", by_name)
        self.assertIn("swirl_meridional_m3", by_name)
        for field in payload["fields"]:
            self.assertTrue(field["pairing_closed"], field["name"])
            self.assertLess(field["rotation_residual"], 1e-12)
            self.assertFalse(field["lambda_prime_sign_quoted"])
        pure = by_name["pure_swirl"]
        mer = by_name["swirl_meridional_m3"]
        self.assertLess(pure["max_abs_rho_E"], 1e-12)
        self.assertGreater(mer["max_abs_rho_E"], pure["max_abs_rho_E"])
        self.assertTrue(pure["remainder"]["peak_vacuous"])
        self.assertFalse(mer["remainder"]["peak_vacuous"])
        self.assertGreater(mer["remainder"]["C_peak"], 0.0)
        self.assertLessEqual(mer["remainder"]["C_peak"], 1.0)
        self.assertGreater(mer["remainder"]["occ_support_peak"], 0.0)
        self.assertLessEqual(mer["remainder"]["occ_support_peak"], 1.0)
        self.assertIn("AXISYM-SWIRL-PROBE.md", ESTIMATE.read_text())


if __name__ == "__main__":
    unittest.main()
