#!/usr/bin/env python3
"""Odlyzko–Pólya origin dump: 1914 remark is not a Hamiltonian."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.hilbert_polya import audit_candidate, hamiltonian_is_independent
from domain_architect.odlyzko_origin import POLYA_1914_REMARK, run_odlyzko_origin
from domain_architect.schema import CANONICAL_SFE_STATUS, RH_STATUS


ROOT = Path(__file__).resolve().parents[1]


class TestOdlyzkoOrigin(unittest.TestCase):
    def test_remark_is_not_a_hamiltonian(self):
        report = run_odlyzko_origin()
        text = report.narrative().lower()
        ids = {p.piece_id for p in report.pieces}
        self.assertIn("OD-A", ids)
        self.assertIn("OD-HILBERT", ids)
        self.assertIn("OD-GUE", ids)
        self.assertEqual(report.rh_status, RH_STATUS)
        self.assertEqual(report.canonical_sfe_status, CANONICAL_SFE_STATUS)
        self.assertIn("not a hamiltonian", text)
        self.assertIn("empty", text)
        self.assertIn("very weak", text)
        self.assertNotIn("proves the riemann hypothesis", text)
        audit = audit_candidate("polya-1914")
        self.assertFalse(audit.complete)
        self.assertFalse(audit.circular)
        self.assertIn("HP-S0", audit.missing_piece_ids)
        s0 = next(p for p in audit.pieces if p["piece_id"] == "HP-S0")
        self.assertNotEqual(s0["status"], "supplied_by_candidate")
        self.assertIn("eigenvalues", POLYA_1914_REMARK.lower())
        self.assertFalse(
            hamiltonian_is_independent(
                "RH iff all eigenvalues of a physical problem are real, "
                "given a connection of Ξ zeros to that problem (Pólya 1914/1982)"
            )
        )

    def test_cli_odlyzko(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--odlyzko"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Odlyzko–Pólya origin dump", proc.stdout)
        self.assertIn("HP-H026", proc.stdout)
        self.assertIn("1914", proc.stdout)
        self.assertIn("Riemann hypothesis status: not claimed", proc.stdout)
        self.assertIn("it is empty", proc.stdout.lower())
        self.assertIn("very weak", proc.stdout.lower())
        self.assertNotIn("proves the riemann hypothesis", proc.stdout.lower())


if __name__ == "__main__":
    unittest.main()
