"""Requested Young line is not seated. The chain stays a chain."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph, run as audit_run  # noqa: E402
from tjj_estimate import local_block_identities, run, vortex_blob  # noqa: E402

PAGE = ROOT / "docs" / "TJJ-ESTIMATE.md"
SHELL = ROOT / "docs" / "AXISYM-SHELL.md"
AUDIT = ROOT / "docs" / "ESTIMATE-AUDIT.md"


class TjjEstimateTests(unittest.TestCase):
    def test_page_refuses_the_line(self):
        text = PAGE.read_text()
        self.assertIn("The chain stays a chain.", text)
        self.assertIn("The estimate cannot be written.", text)
        self.assertIn("T_{j\\leftarrow j}", text)
        self.assertIn("\\varepsilon\\nu", text)
        self.assertIn("\\dot Z_j", text)
        self.assertIn("\\Lambda'", text)
        self.assertIn("energy", text)
        self.assertIn("direction factor", text)
        self.assertIn("TJJ_requested_line", text)
        self.assertIn("**fail**", text)
        self.assertIn("NS not solved.", text)
        self.assertIn("**false** as a", text.lower())
        self.assertIn("Proposition TJJ-E-false", text)
        self.assertIn("Proposition TJJ-Trans", text)
        self.assertIn("Proposition TJJ-α", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("unconditional 3-D regularity", text)
        self.assertNotIn("coherence viscosity", text)
        self.assertNotIn("gematria", text)
        self.assertNotIn("would close, not proved", text)
        self.assertIn("not seated", text)

    def test_page_passes_discard_filter(self):
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])

    def test_pointers_and_scores(self):
        self.assertIn("TJJ-ESTIMATE.md", SHELL.read_text())
        self.assertIn("TJJ-ESTIMATE.md", AUDIT.read_text())
        self.assertIn("AS_tjj_young", SHELL.read_text())
        self.assertIn("EAud_tjj_young", AUDIT.read_text())
        payload = audit_run()
        rows = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(rows["EAud_tjj_young"]["verdict"], "fail")
        self.assertEqual(payload["domain_verdict"], "open")
        self.assertTrue(payload["meta"]["estimate_open"])

    def test_transport_and_alpha_identities(self):
        uh = vortex_blob(24, width=0.8)
        row = local_block_identities(uh, 1)
        if row["Z_j"] <= 1e-14:
            row = local_block_identities(uh, 0)
        self.assertLess(row["trans_rel"], 1e-10)
        self.assertLess(row["stretch_alpha_rel"], 1e-10)

    def test_probe_scores(self):
        payload = run(n=24)
        rows = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(rows["TJJ_transport_vanishes"]["verdict"], "pass")
        self.assertEqual(rows["TJJ_stretch_is_alpha"]["verdict"], "pass")
        self.assertEqual(rows["TJJ_energy_visc_false"]["verdict"], "pass")
        self.assertEqual(rows["TJJ_requested_line"]["verdict"], "fail")
        self.assertEqual(rows["TJJ_ns_solved"]["verdict"], "fail")
        self.assertEqual(payload["domain_verdict"], "open")
        self.assertTrue(payload["meta"]["estimate_open"])
        self.assertFalse(payload["meta"]["ns_solved"])
        self.assertLess(payload["identities"]["trans_rel"], 1e-10)
        self.assertLess(payload["identities"]["stretch_alpha_rel"], 1e-10)


if __name__ == "__main__":
    unittest.main()
