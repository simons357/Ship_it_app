"""DA brute: finite list is legal; try-every is not the leftover."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_brute import CLAIMS, FINITE, NOT_FINITE, VISUAL, is_brute_ask, run  # noqa: E402


class DaBruteTests(unittest.TestCase):
    def test_try_every_is_not_the_write(self):
        tmp = Path(tempfile.mkdtemp()) / "da_brute_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["K1"]["verdict"], "pass")
        self.assertEqual(by["K2"]["verdict"], "fail")
        self.assertEqual(by["K3"]["verdict"], "fail")
        self.assertEqual(by["K4"]["verdict"], "fail")
        self.assertEqual(by["K5"]["verdict"], "fail")
        self.assertEqual(by["K6"]["verdict"], "fail")
        self.assertEqual(by["K7"]["verdict"], "pass")
        self.assertEqual(by["K8"]["verdict"], "open")
        self.assertTrue(payload["meta"]["finite_list_is_legal"])
        self.assertTrue(payload["meta"]["try_every_is_not_a_write"])
        self.assertTrue(payload["meta"]["quantum_is_not_the_estimate"])
        self.assertIn("finite list", VISUAL)
        self.assertIn("QUANTUM", VISUAL)
        self.assertEqual(len(FINITE), 5)
        self.assertEqual(len(NOT_FINITE), 5)
        self.assertTrue(is_brute_ask("try every combination on a quantum computer"))
        self.assertTrue(is_brute_ask("supercomputer try them all instantly"))
        self.assertFalse(is_brute_ask(""))
        self.assertFalse(is_brute_ask("now what"))
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-BRUTE.md").is_file())
        self.assertTrue((ROOT / "docs" / "assets" / "da-brute-visual.png").is_file())


if __name__ == "__main__":
    unittest.main()
