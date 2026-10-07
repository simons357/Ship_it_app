"""Rerun guards for B41 phase-convention audit."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestB41PhaseConventionAudit(unittest.TestCase):
    def test_audit_script(self) -> None:
        script = ROOT / "scripts" / "b41_phase_convention_audit.py"
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        payload = json.loads(
            (ROOT / "results" / "b41" / "phase_convention_audit.json").read_text()
        )
        self.assertEqual(payload["four_pi_offset_targets"][0]["row"], 0)
        rows = [t["row"] for t in payload["four_pi_offset_targets"]]
        self.assertEqual(rows, [0, 5, 10, 11])
        self.assertFalse(
            payload["mode_phase_absorption"]["A_strong_only_delta"]["solvable_mod1"]
        )
        self.assertTrue(
            payload["mode_phase_absorption"]["B_identity_consistent_delta"][
                "solvable_mod1"
            ]
        )
        self.assertFalse(payload["g6a_transfer"]["via_raw_r2_identity"])


if __name__ == "__main__":
    unittest.main()
