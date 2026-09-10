"""Tests for bridge tuning handoff demo (UI wiring sketch, no optimizer)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "bridge_tuning_handoff_demo.py"


class BridgeTuningHandoffTests(unittest.TestCase):
    def test_ns_handoff_prints_nu_dial(self) -> None:
        payload = {
            "auto_assigned": True,
            "domain_book": "NS-B",
            "controls": [
                {
                    "name": "nu",
                    "role": "scale_response",
                    "subtype": "viscosity",
                    "status": "free",
                    "why": "Dissipative scale",
                    "default_intervention": "Vary nu",
                    "bridge_app_hint": "Primary continuous dial",
                }
            ],
            "fixed_structure": [
                "Do not bake λ_min(Q_N)>-1/2 or prime floors into unaugmented NS"
            ],
            "protocol_reminder": "Freeze protocol first.",
            "statement": "Handoff only.",
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(payload, fh)
            path = fh.name
        try:
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), path],
                check=True,
                capture_output=True,
                text=True,
            )
        finally:
            Path(path).unlink(missing_ok=True)
        out = proc.stdout
        self.assertIn("nu [free]", out)
        self.assertIn("slider or numeric field", out)
        self.assertIn("not an optimizer", out)
        self.assertIn("λ_min", out)

    def test_gravity_handoff_prints_p_selector(self) -> None:
        payload = {
            "auto_assigned": True,
            "domain_book": "gravity-poisson",
            "controls": [
                {
                    "name": "P",
                    "role": "admissibility",
                    "subtype": "mode_permission",
                    "status": "protocol_selector",
                    "why": "Mode permission",
                    "default_intervention": "Compare P=I vs masks",
                    "bridge_app_hint": "Selector",
                }
            ],
            "fixed_structure": [],
            "protocol_reminder": "",
            "statement": "",
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(payload, fh)
            path = fh.name
        try:
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), path],
                check=True,
                capture_output=True,
                text=True,
            )
        finally:
            Path(path).unlink(missing_ok=True)
        out = proc.stdout
        self.assertIn("P [protocol_selector]", out)
        self.assertIn("dropdown / mask picker", out)
        self.assertIn("not 'prime'", out)


if __name__ == "__main__":
    unittest.main()
