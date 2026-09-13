"""Unit tests for SFE ↔ black-hole overlay spell scripts."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def _load(name: str, filename: str):
    path = SCRIPTS / filename
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


overlay = _load("sfe_bh_overlay_spells", "sfe_bh_overlay_spells.py")
phase_flow = _load("sfe_phase_flow_spell", "sfe_phase_flow_spell.py")
route_c = _load("route_c_gap_a_verify", "route_c_gap_a_verify.py")

TARGET = -1.0 / (2.0 * np.pi)


class TestOverlaySpells(unittest.TestCase):
    def test_isprime_basic(self):
        self.assertFalse(overlay.isprime(0))
        self.assertFalse(overlay.isprime(1))
        self.assertTrue(overlay.isprime(2))
        self.assertFalse(overlay.isprime(4))
        self.assertTrue(overlay.isprime(97))

    def test_pearson_perfect_correlation(self):
        x = np.arange(1.0, 11.0)
        self.assertAlmostEqual(overlay.pearson(x, x), 1.0, places=12)

    def test_harmonic_matches_inv_r_sqrt(self):
        N = 50
        bh = overlay.schwarzschild_templates(N)
        sfe = overlay.sfe_discrete_profiles(N)
        r = overlay.pearson(sfe["harmonic_free"], bh["inv_r_sqrt"])
        self.assertGreater(r, 0.999)

    def test_phase_readout_route_c_ratio(self):
        for N in (100, 500):
            ph = overlay.phase_readout(N)
            self.assertLess(ph["lambda_min"], -0.5)
            self.assertTrue(ph["phase_II_by_floor"])
            self.assertAlmostEqual(ph["ratio_to_target"], 1.0, delta=0.02)

    def test_run_spells_structure(self):
        report = overlay.run_spells([50, 100])
        self.assertIn("spells", report)
        self.assertIn("50", report["spells"])
        block = report["spells"]["50"]
        self.assertIn("phase", block)
        self.assertIn("overlay_best", block)
        self.assertGreaterEqual(len(block["overlay_best"]), 1)


class TestPhaseFlowSpell(unittest.TestCase):
    def test_herfindahl_uniform(self):
        v = np.ones(10)
        self.assertAlmostEqual(phase_flow.herfindahl(v), 0.1, places=12)

    def test_q_matrix_symmetric_positive(self):
        q = phase_flow.q_matrix(8)
        self.assertTrue(np.allclose(q, q.T))
        self.assertTrue(np.all(q > 0))


class TestRouteCGapA(unittest.TestCase):
    def test_lambda_min_over_logN_near_target(self):
        for N in (200, 500, 1000):
            q = route_c.mat_norm(N)
            lam_min = float(np.linalg.eigvalsh(q)[0])
            ratio = lam_min / np.log(N) / TARGET
            self.assertAlmostEqual(ratio, 1.0, delta=0.02)

    def test_v_alt_rayleigh_diverges_from_target(self):
        N = 500
        q = route_c.mat_norm(N)
        v = route_c.v_alt(N)
        r_alt = float(v @ q @ v) / float(v @ v)
        self.assertGreater(abs(r_alt / TARGET), 3.5)

    def test_mobius_lemma_a_entry_error(self):
        N = 100
        q = route_c.mat_norm(N)
        qm = route_c.mat_mobius_claim(N)
        err = float(np.max(np.abs(q - qm)))
        self.assertGreater(err, 0.1)


if __name__ == "__main__":
    unittest.main()
