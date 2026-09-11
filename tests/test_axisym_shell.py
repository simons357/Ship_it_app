"""Axisymmetric shell estimate: identities sit; remainder stays open."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from axisym_shell import run, tau, tau_shift_identity  # noqa: E402
from estimate_audit import classify_paragraph  # noqa: E402

PAGE = ROOT / "docs" / "AXISYM-SHELL.md"
AUDIT = ROOT / "docs" / "ESTIMATE-AUDIT.md"


class AxisymShellTests(unittest.TestCase):
    def test_page_first_sentence(self):
        text = PAGE.read_text()
        self.assertIn("Axisymmetric-with-swirl Navier–Stokes", text)
        self.assertIn("Z_j=", text)
        self.assertIn("T_{j\\leftarrow j}", text)
        self.assertIn("[no extra", text)
        self.assertIn("C_{\\mathrm{IR}}[\\varphi]", text)
        self.assertIn("C_{\\mathrm{UV}}[\\varphi]", text)
        self.assertIn("**Not a close. NS not solved.", text)
        self.assertIn("Proposition AS-Id", text)
        self.assertIn("Theorem AS-Gal", text)
        self.assertIn("[ρ]", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("unconditional 3-D regularity", text)
        self.assertNotIn("coherence viscosity", text)
        self.assertNotIn("gematria", text)
        self.assertIn("not bounded by", text)
        self.assertIn("\\dot Z_j", text)
        self.assertIn("Attack-6 Door 1", text)
        self.assertIn("2-D stays 2-D", text)

    def test_page_passes_discard_filter(self):
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])

    def test_tau_shift_is_exact(self):
        row = tau_shift_identity(omega_star=11.0)
        self.assertTrue(row["closed"])
        self.assertEqual(tau(1.0, 2.0, 3.0, 4.0, 5.0), (1.0 - 3.0) * 4.0 + (2.0 - 3.0) * 5.0)

    def test_probe_scores(self):
        payload = run(n=16, seed=1390)
        rows = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(rows["AS_identity"]["verdict"], "pass")
        self.assertEqual(rows["AS_split"]["verdict"], "pass")
        self.assertEqual(rows["AS_young_IR"]["verdict"], "pass")
        self.assertEqual(rows["AS_young_UV"]["verdict"], "pass")
        self.assertEqual(rows["AS_tau"]["verdict"], "pass")
        self.assertEqual(rows["AS_omega_star"]["verdict"], "pass")
        self.assertEqual(rows["AS_pairing_check"]["verdict"], "pass")
        self.assertEqual(rows["AS_remainder"]["verdict"], "fail")
        self.assertEqual(rows["AS_rho"]["verdict"], "fail")
        self.assertEqual(rows["AS_door3"]["verdict"], "fail")
        self.assertEqual(rows["AS_page_clean"]["verdict"], "pass")
        self.assertEqual(rows["AS_ns_solved"]["verdict"], "fail")
        self.assertEqual(payload["domain_verdict"], "open")
        self.assertTrue(payload["meta"]["estimate_open"])
        self.assertFalse(payload["meta"]["lambda_prime_sign_quoted"])
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertFalse(payload["meta"]["h1_started"])
        for field in payload["fields"]:
            self.assertTrue(field["pairing_closed"], field["name"])
            self.assertLess(field["max_split_err"], 1e-12)
        self.assertIn("remainder T_{j<-j}", payload["claim"])

    def test_audit_still_a_filter(self):
        text = AUDIT.read_text()
        self.assertIn("AXISYM-SHELL.md", text)


if __name__ == "__main__":
    unittest.main()
