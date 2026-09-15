"""Periodic snapshot diagnostics: angle factor kept; C_needed_raw subtracts dissipation."""

from __future__ import annotations

import math
import sys
import unittest
from dataclasses import fields
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from h1_abad_snapshot import (  # noqa: E402
    FieldReport,
    SNAPSHOT_LABEL,
    c_needed_raw,
    c_no_angle_diag,
    format_table,
    reference_lambda0,
    run_one,
    sweep,
)


PAGE = ROOT / "docs" / "H1-ABAD-SNAPSHOT.md"
WRITE = ROOT / "docs" / "H1-WRITE.md"


class H1AbadSnapshotTests(unittest.TestCase):
    def test_field_report_carries_both_integrals_and_c_needed_raw(self):
        names = {f.name for f in fields(FieldReport)}
        self.assertIn("c_needed_raw", names)
        self.assertIn("a_angle", names)
        self.assertIn("a_no_angle", names)
        self.assertIn("d_phi", names)
        self.assertIn("e", names)
        self.assertIn("lambda_fixed", names)
        self.assertNotIn("a_bad", names)
        row = run_one("abc", 1.0, 0.5, n=8)
        self.assertIsInstance(row, FieldReport)
        self.assertEqual(row.label, SNAPSHOT_LABEL)
        self.assertFalse(row.leftover_1_closed)
        self.assertFalse(row.started_from_abc)
        self.assertFalse(row.unrestricted_local_6_rescued)
        self.assertAlmostEqual(
            row.c_needed_raw,
            c_needed_raw(row.a_angle, row.e, row.d_phi, row.r, nu=row.nu),
        )
        self.assertAlmostEqual(
            row.c_no_angle_diag,
            c_no_angle_diag(row.a_no_angle, row.e, row.r),
        )

    def test_angle_factor_makes_a_smaller_integral_on_the_same_bad_pairs(self):
        row = run_one("abc", 1.0, reference_lambda0("abc", 10), n=10)
        self.assertGreater(row.a_no_angle, 0.0)
        self.assertGreater(row.a_angle, 0.0)
        self.assertLessEqual(row.a_angle, row.a_no_angle)
        self.assertLess(row.a_angle / row.a_no_angle, 0.999)
        self.assertGreater(row.n_bad_pairs, 0)

    def test_c_needed_raw_subtracts_dissipation_and_floors_at_zero(self):
        self.assertAlmostEqual(c_needed_raw(8.0, 2.0, 16.0, 2.0, nu=1.0), 12.0)
        self.assertEqual(c_needed_raw(1.0, 2.0, 100.0, 2.0, nu=1.0), 0.0)
        self.assertTrue(math.isnan(c_needed_raw(1.0, 0.0, 1.0, 1.0)))

    def test_lambda_stays_fixed_across_amplitude_sweep(self):
        n = 10
        lambda0 = reference_lambda0("abc", n)
        self.assertGreater(lambda0, 0.0)
        amps = (0.5, 1.0, 2.0)
        rows = [run_one("abc", amp, lambda0, n=n) for amp in amps]
        for row in rows:
            self.assertAlmostEqual(row.lambda_fixed, lambda0, places=12)
        highs = [row.n_high for row in rows]
        self.assertLess(highs[0], highs[-1])
        self.assertEqual(rows[0].label, "periodic snapshot diagnostic")

    def test_scaled_threshold_would_freeze_the_high_set(self):
        n = 10
        a = run_one("abc", 1.0, reference_lambda0("abc", n, amp0=1.0), n=n)
        b = run_one("abc", 2.0, reference_lambda0("abc", n, amp0=2.0), n=n)
        self.assertEqual(a.n_high, b.n_high)
        self.assertGreater(b.lambda_fixed, a.lambda_fixed)

    def test_printed_results_include_both_integrals(self):
        lambda0 = reference_lambda0("taylor-green", 8)
        rows = [
            run_one("abc", 1.0, reference_lambda0("abc", 8), n=8),
            run_one("taylor-green", 1.0, lambda0, n=8),
        ]
        text = format_table(rows)
        self.assertIn("PERIODIC SNAPSHOT DIAGNOSTICS", text)
        self.assertIn("amplitude", text)
        self.assertIn("fixed threshold", text)
        self.assertIn("A_angle", text)
        self.assertIn("A_no_angle", text)
        self.assertIn("C_needed_raw", text)
        self.assertIn("ABC", text)
        self.assertIn("Taylor–Green", text)
        self.assertIn("Does not rescue unrestricted local (6)", text)
        payload = sweep(n=8, amps=(1.0,))
        self.assertIn("C_needed_raw", payload["printed"])
        self.assertIn("A_angle", payload["printed"])
        self.assertFalse(payload["leftover_1_closed"])
        self.assertFalse(payload["unrestricted_local_6_rescued"])
        self.assertEqual(payload["label"], "periodic snapshot diagnostic")

    def test_page_labels_periodic_snapshot_and_does_not_rescue_local_6(self):
        text = PAGE.read_text()
        self.assertIn("periodic snapshot diagnostic", text.lower())
        self.assertIn("Lambda0", text)
        self.assertIn("C_needed_raw", text)
        self.assertIn("A_angle", text)
        self.assertIn("A_no_angle", text)
        self.assertIn("Taylor–Green", text)
        self.assertIn("not leftover 1", text.lower())
        self.assertIn("unrestricted local", text.lower())
        self.assertIn("Does not rescue", text)
        self.assertIn("Do not call it the original", text)
        self.assertNotIn("| original bad-pair integral |", text)
        self.assertNotIn("H1 is a theorem", text)
        write = WRITE.read_text()
        self.assertIn("H1-ABAD-SNAPSHOT.md", write)
        self.assertIn("Do not start this write from ABC", write)
