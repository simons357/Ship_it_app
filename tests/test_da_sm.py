"""SM Lagrangian DA screen: consumes couplings, does not produce them."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_sm import run  # noqa: E402


class DaSmTests(unittest.TestCase):
    def test_started_over_consumes_not_produces(self):
        tmp = Path(tempfile.mkdtemp()) / "da_sm_test.json"
        payload = run(out=tmp)
        self.assertTrue(payload["meta"]["forget_cosmo_16"])
        self.assertTrue(payload["meta"]["L_consumes_couplings"])
        self.assertEqual(payload["produces"], [])
        self.assertIn("g_s", payload["consumes"])
        self.assertEqual(len(payload["blocks"]), 5)
        self.assertTrue(all(b["verdict"] == "pass" for b in payload["blocks"]))
        self.assertEqual(payload["gauge3"], "fail")
        self.assertEqual(payload["nature4"], "fail")
        self.assertFalse(payload["collapsed"])

    def test_real_isos_pass_fake_fail_and_realized_eq(self):
        tmp = Path(tempfile.mkdtemp()) / "da_sm_test.json"
        payload = run(out=tmp)
        by = {r["name"]: r for r in payload["isomorphisms"]}
        self.assertEqual(by["weinberg_rotation"]["verdict"], "pass")
        self.assertEqual(by["SU2_iso_Spin3"]["verdict"], "pass")
        self.assertEqual(by["U3xU2xU1_is_cosmo_16"]["verdict"], "fail")
        self.assertEqual(by["gluon_cubic_is_NS"]["verdict"], "fail")
        self.assertEqual(by["yukawa_is_koide"]["verdict"], "fail")
        self.assertEqual(by["harmonic_phenotype"]["verdict"], "fail")
        eq = payload["realized_equation"]
        self.assertTrue(eq["both_sides"])
        self.assertFalse(eq["produces_couplings"])
        self.assertEqual(eq["working_couple"], "pass")
        self.assertEqual(eq["nature4"], "fail")
        miss = {r["name"]: r for r in payload["missing"]}
        self.assertEqual(miss["gravity_G"]["verdict"], "fail")
        self.assertEqual(miss["cosmological_constant"]["verdict"], "fail")


if __name__ == "__main__":
    unittest.main()
