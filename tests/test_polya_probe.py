#!/usr/bin/env python3
"""Pólya probe: N-component briefing, no Millennium glue, no RH claim."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.polya_probe import run_polya_probe
from domain_architect.schema import CANONICAL_SFE_STATUS, RH_STATUS


ROOT = Path(__file__).resolve().parents[1]


class TestPolyaProbe(unittest.TestCase):
    def test_expands_past_five_roles_and_asks_for_h(self):
        probe = run_polya_probe()
        self.assertGreater(probe.component_count, 5)
        self.assertEqual(probe.core_role_count, 5)
        self.assertGreater(probe.extension_count, 0)
        self.assertFalse(probe.complete)
        self.assertEqual(probe.rh_status, RH_STATUS)
        self.assertEqual(probe.canonical_sfe_status, CANONICAL_SFE_STATUS)
        roles = {c.role for c in probe.components}
        self.assertIn("ℋ", roles)
        self.assertIn("ℬ", roles)
        self.assertIn("E-entire", roles)
        self.assertIn("other-book", roles)
        text = " ".join(probe.da_requests).lower()
        self.assertIn("independent operator", text)
        self.assertTrue(any("laguerre" in c.occupant.lower() for c in probe.components))

    def test_does_not_glue_navier_stokes_or_claim_rh(self):
        probe = run_polya_probe()
        ns = next(row for row in probe.millennium_routing if "Navier" in row["prize"])
        self.assertEqual(ns["relation"], "INSUFFICIENT_INFORMATION")
        rh = next(row for row in probe.millennium_routing if "Riemann" in row["prize"])
        self.assertIn("open", rh["status"].lower())
        narrative = probe.narrative().lower()
        self.assertNotIn("proves the riemann hypothesis", narrative)
        self.assertIn("not claimed", narrative)
        self.assertIn("not be merged", " ".join(probe.findings).lower())
        self.assertFalse(probe.gue_laboratory["is_riemann_spectrum"])
        self.assertTrue(probe.weyl_laboratory["oscillator_rejected"])
        self.assertTrue(probe.weyl_laboratory["xp_classical_leading_term_compatible"])
        self.assertIn("1/log", probe.weyl_laboratory["conclusion"])
        self.assertTrue(any(s["candidate_id"] == "berry-keating" and not s["complete"] for s in probe.candidate_scores))
        self.assertTrue(any(s["candidate_id"] == "diagonal-zeros" and s["circular"] for s in probe.candidate_scores))

    def test_cli_probe(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--polya-probe"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Independently specifiable components recorded:", proc.stdout)
        self.assertIn("Riemann hypothesis status: not claimed", proc.stdout)
        self.assertIn("Laguerre", proc.stdout)
        self.assertIn("INSUFFICIENT_INFORMATION", proc.stdout)
        self.assertIn("oscillator rejected: true", proc.stdout.lower())
        self.assertNotIn("proves the riemann hypothesis", proc.stdout.lower())


if __name__ == "__main__":
    unittest.main()
