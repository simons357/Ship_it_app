"""Signed cancellation test locks: keep T_abc, one DF field."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ns_attacks.qx_kernel import (
    C_abc,
    df_mode,
    df_residual,
    equal_energy_amplitudes,
    similar_seed_triad,
    subnet_triads,
    triad_T_signed,
)
from ns_attacks.signed_cancellation_test import (
    majorant_ok,
    random_baseline,
    report,
    signed_Q_and_T,
    single_triad_signed,
    subnet_signed,
)


class TestSignedCancellation(unittest.TestCase):
    def test_df_mode_is_divergence_free(self) -> None:
        k = (3, -1, 2)
        u = df_mode(k, 1.3, 0.4, 0.7)
        self.assertLess(df_residual(k, u), 1e-12)

    def test_signed_T_bounded_by_C_on_one_triad(self) -> None:
        rng = random.Random(0)
        row = single_triad_signed(4, rng)
        self.assertTrue(row["signed_le_majorant"])
        self.assertLess(row["df_residual_max"], 1e-10)
        self.assertGreater(row["Qplus2_over_Omega"], 0.0)
        self.assertGreater(row["Qsgn2_over_Omega"], 0.0)
        self.assertLessEqual(row["ratio_Qsgn_to_Qplus"], 1.0 + 1e-9)

    def test_reassembly_identity_on_subnet(self) -> None:
        rng = random.Random(1)
        row = subnet_signed(4, rng)
        self.assertTrue(row["reassembly_identity"])
        self.assertTrue(row["majorant_holds"])
        self.assertGreater(row["n_triads"], 1)
        self.assertGreater(row["n_modes"], 3)
        # Shared w: one common high mode for every triad.
        w = subnet_triads(4)[0][2]
        self.assertTrue(all(t[2] == w for t in subnet_triads(4)))

    def test_random_baseline_not_a_bound(self) -> None:
        triads = subnet_triads(4)
        from ns_attacks.qx_kernel import occupied_shells

        f = equal_energy_amplitudes(occupied_shells(triads))
        base = random_baseline(triads, f, random.Random(2), n_samples=12)
        self.assertGreater(base["Q2_max"], 0.0)
        self.assertGreaterEqual(base["Q2_max"], base["Q2_mean"] - 1e-15)
        self.assertLessEqual(base["coherence_max"], 1.0 + 1e-12)

    def test_zero_field_vanishes(self) -> None:
        triads = [similar_seed_triad(4)]
        _u, _v, _w, a, b, c = triads[0]
        f = {a: 0.0, b: 0.0, c: 0.0}
        Q, T, abs_sum = signed_Q_and_T(triads, f, {}, {})
        self.assertEqual(T, 0.0)
        self.assertEqual(abs_sum, 0.0)
        self.assertEqual(l2_safe(Q), 0.0)

    def test_majorant_envelope_formula(self) -> None:
        triads = [similar_seed_triad(4)]
        _u, _v, _w, a, b, c = triads[0]
        f = equal_energy_amplitudes([a, b, c])
        envelope = C_abc(a, b, c) * f[a] * f[b] * f[c]
        self.assertTrue(majorant_ok(triads, f, envelope))
        self.assertFalse(majorant_ok(triads, f, envelope * 1.01, atol=0.0))

    def test_report_does_not_claim_power_gain(self) -> None:
        payload = report(seed=0)
        sub = payload["subnet_shared_w"]
        self.assertTrue(sub["constant_factor_only_on_sample"])
        self.assertFalse(sub["coherent_adversary_beats_half_on_sample"])
        self.assertFalse(payload["locks"]["theta_signed_proved"])
        self.assertFalse(payload["locks"]["theorem_17_proved"])
        self.assertAlmostEqual(sub["mean_Qsgn_over_Qplus"], 0.20, delta=0.03)
        self.assertEqual(payload["single_triad"]["theta_hat_nonneg"], 0.5)

    def test_docs_forbid_killing_signs(self) -> None:
        note = (ROOT / "docs" / "GATE-B-SIGNED-CANCELLATION-TEST.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("T_{abc}", note)
        self.assertIn("divergence-free", note)
        self.assertIn("Not (17)", note)


def l2_safe(Q: dict) -> float:
    from math import sqrt

    return sqrt(sum(v * v for v in Q.values()))


if __name__ == "__main__":
    unittest.main()
