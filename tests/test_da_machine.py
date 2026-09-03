"""Domain Architect process-machine smoke tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_machine import classify_claim  # noqa: E402


class DaMachineTests(unittest.TestCase):
    def test_forbidden_close_fails(self):
        r = classify_claim("I solved NS and RH last May")
        self.assertEqual(r["verdict"], "fail")

    def test_theorem_p_lands_in_q(self):
        r = classify_claim("Theorem P: the prime block of Q-tilde sits above -1/4")
        self.assertEqual(r["domain"], "Q")
        self.assertEqual(r["verdict"], "open")

    def test_unassigned_stays_open(self):
        r = classify_claim("hello there")
        self.assertIsNone(r["domain"])
        self.assertEqual(r["verdict"], "open")


if __name__ == "__main__":
    unittest.main()
