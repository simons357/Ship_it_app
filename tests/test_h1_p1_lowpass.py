"""P1 low-pass Biot-Savart sits. It is not H1."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from h1_p1_lowpass import run  # noqa: E402


class H1P1LowpassTests(unittest.TestCase):
    def test_lowpass_bound_sits(self):
        payload = run(n=24, seed=3)
        rows = {r["name"]: r for r in payload["lemmas"]}
        self.assertEqual(rows["H1p1_lowpass_sits"]["verdict"], "pass")
        self.assertEqual(rows["H1p1_highpass_needed"]["verdict"], "pass")
        self.assertEqual(rows["H1p1_is_h1"]["verdict"], "fail")
        self.assertEqual(rows["H1p1_nse_class"]["verdict"], "open")
        self.assertEqual(payload["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["h1_proved"])

    def test_ratio_respects_kmax(self):
        payload = run(n=24, seed=11)
        for row in payload["lowpass"]:
            self.assertLessEqual(row["ratio_w_over_u"], row["bound_kmax2"] * (1.0 + 1e-9))
            self.assertGreater(row["modes"], 0)

    def test_highpass_exceeds_lowpass_rho(self):
        payload = run(n=24, seed=11)
        rho = 1.0 / 3.0
        for row in payload["highpass"]:
            self.assertGreater((rho * rho) * row["ratio_w_over_u"], 4.0)


if __name__ == "__main__":
    unittest.main()
