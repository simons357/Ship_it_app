#!/usr/bin/env python3
"""Pólya probe: N-component briefing, no Millennium glue, no RH claim."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.polya_probe import run_polya_probe
from domain_architect.registry import EquationRegistry
from domain_architect.schema import CANONICAL_SFE_STATUS, RH_STATUS


ROOT = Path(__file__).resolve().parents[1]


class TestPolyaProbe(unittest.TestCase):
    def test_expands_past_five_roles_and_asks_for_h(self):
        probe = run_polya_probe()
        self.assertGreater(probe.component_count, 8)
        self.assertEqual(probe.core_role_count, 5)
        self.assertGreater(probe.extension_count, 2)
        narrative = probe.narrative()
        self.assertIn("DA decided the component count", narrative)
        self.assertIn("not a cap", narrative)
        self.assertIn("How quantum fitted", narrative)
        self.assertTrue(any("ℋ" in line or "Hilbert space" in line for line in probe.how_quantum_fitted))
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
        occupants = " ".join(c.occupant.lower() for c in probe.components)
        self.assertIn("1926", occupants)
        self.assertIn("cos", occupants)

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
        self.assertIn("relocates the gap", " ".join(probe.findings).lower())
        self.assertTrue(any(c.component_id == "C-Polya1926" for c in probe.components))
        self.assertIn("de bruijn", " ".join(probe.filter_pops).lower())
        self.assertTrue(any(c.component_id == "C-BN" for c in probe.components))
        self.assertIn("HP-H014", EquationRegistry.load_default().equations)
        dumped = {c.component_id for c in probe.components}
        for cid in (
            "C-PF",
            "C-Turan",
            "C-Isoperimetric",
            "C-Membrane",
            "C-Enumeration",
            "C-RandomWalk",
            "C-XiIntegral",
            "C-EntireZeros",
            "C-IntegerEntire",
        ):
            self.assertIn(cid, dumped)
        self.assertGreaterEqual(probe.component_count, 30)
        pops = " ".join(probe.filter_pops).lower()
        self.assertIn("frequency", pops)
        self.assertIn("membrane", pops)
        self.assertIn("HP-H017", EquationRegistry.load_default().equations)
        self.assertIn("HP-H024", EquationRegistry.load_default().equations)
        board = probe.filter_scoreboard
        self.assertEqual(board[0]["result"], "survived")
        self.assertIn("Pólya", board[0]["source"])
        self.assertTrue(any(r["result"] == "false" and "Liouville" in r["source"] for r in board))
        self.assertTrue(any(r["result"] == "incomplete" and "Hilbert" in r["source"] for r in board))
        self.assertIn("the only one whose theorems survive", " ".join(probe.filter_pops))

    def test_cli_probe(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--polya-probe"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Independently specifiable components recorded:", proc.stdout)
        self.assertIn("DA decided the component count", proc.stdout)
        self.assertIn("How quantum fitted", proc.stdout)
        self.assertIn("not a cap", proc.stdout)
        self.assertIn("Riemann hypothesis status: not claimed", proc.stdout)
        self.assertIn("Laguerre", proc.stdout)
        self.assertIn("INSUFFICIENT_INFORMATION", proc.stdout)
        self.assertIn("What popped through the DA filter", proc.stdout)
        self.assertIn("de Bruijn", proc.stdout)
        self.assertIn("Pólya frequency", proc.stdout)
        self.assertIn("vibrating membrane", proc.stdout)
        self.assertIn("Who survived the filter", proc.stdout)
        self.assertIn("[survived] George Pólya", proc.stdout)
        self.assertIn("the only one whose theorems survive", proc.stdout)
        self.assertIn("What rhymed when we looked", proc.stdout)
        self.assertIn("Biot", proc.stdout)
        self.assertNotIn("proves the riemann hypothesis", proc.stdout.lower())


if __name__ == "__main__":
    unittest.main()
