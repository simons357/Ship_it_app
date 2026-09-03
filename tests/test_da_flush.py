"""Hilbert combination-flush smoke tests."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_flush import run  # noqa: E402


class DaFlushTests(unittest.TestCase):
    def test_born_normalized_and_flushes_core(self):
        tmp = Path(tempfile.mkdtemp()) / "da_flush_test.json"
        payload = run(n=80, seed=1, out=tmp)
        born = payload["state"]["born"]
        self.assertAlmostEqual(sum(born.values()), 1.0, places=6)
        flushed = set(payload["flushed"])
        self.assertIn("log_cc_ratio", flushed)
        self.assertIn("log_hierarchy", flushed)
        self.assertTrue(payload["meta"]["not_quantum_lens"])
        self.assertEqual(payload["best_combination_by_born_mass"][0]["set"], ["log_cc_ratio"])


if __name__ == "__main__":
    unittest.main()
