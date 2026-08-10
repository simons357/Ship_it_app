#!/usr/bin/env python3
"""Unit tests for HB ringdown spectral selection statistics."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

import hb_ringdown_test as hb


ROOT = Path(__file__).resolve().parents[1]


class TestStatistics(unittest.TestCase):
    def test_log_distance_exact_node(self):
        nodes = np.array([1.0, 1.5, 2.0])
        self.assertAlmostEqual(hb.log_distance(1.5, nodes), 0.0)

    def test_score_higher_when_closer(self):
        nodes = np.array([1.5, 2.0])
        near = hb.score([1.51, 1.99], nodes, sigma=0.05)
        far = hb.score([3.0, 4.0], nodes, sigma=0.05)
        self.assertGreater(near, far)

    def test_bh_fdr_monotonic(self):
        p = [0.001, 0.02, 0.04, 0.5]
        q = hb.benjamini_hochberg(p)
        self.assertEqual(len(q), 4)
        self.assertLessEqual(q[0], q[1])
        self.assertLessEqual(q[1], q[2])
        self.assertTrue(all(0.0 <= x <= 1.0 for x in q))

    def test_frequency_ratios_positive(self):
        df = pd.DataFrame(
            [
                dict(event_id="E1", mode="220", f_Hz=100.0, split="train"),
                dict(event_id="E1", mode="330", f_Hz=150.0, split="train"),
            ]
        )
        pairs = hb.frequency_ratios(df)
        vals = [x for _, x in pairs]
        self.assertTrue(all(v > 0 for v in vals))
        self.assertIn(1.5, vals)
        self.assertIn(2.0 / 3.0, [round(v, 10) for v in vals] + vals)


class TestPipelineSmoke(unittest.TestCase):
    def test_repo_artifacts_exist(self):
        self.assertTrue((ROOT / "hb_ringdown_test.py").exists())
        self.assertTrue((ROOT / "nodes.json").exists())
        self.assertTrue((ROOT / "data" / "qnm_events.csv").exists())

    def test_end_to_end_small_mc(self):
        rng = np.random.default_rng(0)
        families, sigma, observable, _ = hb.load_nodes(ROOT / "nodes.json", rng)
        df = hb.filter_split(hb.load_events(ROOT / "data" / "qnm_events.csv"), "train")
        results, pairs = hb.analyze(df, families, observable, sigma, n_mc=200, rng=rng)
        self.assertGreater(len(pairs), 0)
        self.assertEqual(len(results), len(families))
        self.assertTrue(all(0.0 <= r.p_value <= 1.0 for r in results))
        self.assertTrue(all(0.0 <= r.q_value <= 1.0 for r in results))

    def test_cli_main_train(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out.json"
            rc = hb.main(
                [
                    "--csv",
                    str(ROOT / "data" / "qnm_events.csv"),
                    "--nodes",
                    str(ROOT / "nodes.json"),
                    "--mc",
                    "100",
                    "--split",
                    "train",
                    "--json-out",
                    str(out),
                ]
            )
            self.assertEqual(rc, 0)
            payload = json.loads(out.read_text())
            self.assertEqual(payload["split"], "train")
            self.assertGreater(len(payload["results"]), 0)


if __name__ == "__main__":
    unittest.main()
