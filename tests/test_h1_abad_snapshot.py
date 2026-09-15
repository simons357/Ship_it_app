"""Snapshot A_bad: Lambda = Lambda0 fixed. Not leftover 1."""

from __future__ import annotations

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
    format_table,
    reference_lambda0,
    run_one,
    sweep,
)


PAGE = ROOT / "docs" / "H1-ABAD-SNAPSHOT.md"
WRITE = ROOT / "docs" / "H1-WRITE.md"


class H1AbadSnapshotTests(unittest.TestCase):
    def test_field_report_carries_c_needed_raw(self):
        names = {f.name for f in fields(FieldReport)}
        self.assertIn("c_needed_raw", names)
        self.assertIn("a_bad", names)
        self.assertIn("lambda_fixed", names)
        self.assertIn("amplitude", names)
        row = run_one("abc", 1.0, 0.5, n=8)
        self.assertIsInstance(row, FieldReport)
        self.assertEqual(row.label, SNAPSHOT_LABEL)
        self.assertFalse(row.leftover_1_closed)
        self.assertFalse(row.started_from_abc)
        self.assertAlmostEqual(row.c_needed_raw, c_needed_raw(row.a_bad, row.x_loc, row.r))

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
        self.assertEqual(rows[0].label, "snapshot test")

    def test_scaled_threshold_would_freeze_the_high_set(self):
        n = 10
        a = run_one("abc", 1.0, reference_lambda0("abc", n, amp0=1.0), n=n)
        b = run_one("abc", 2.0, reference_lambda0("abc", n, amp0=2.0), n=n)
        self.assertEqual(a.n_high, b.n_high)
        self.assertGreater(b.lambda_fixed, a.lambda_fixed)

    def test_c_needed_raw_is_abad_over_rinv2_x(self):
        self.assertAlmostEqual(c_needed_raw(8.0, 2.0, 2.0), 16.0)
        self.assertTrue(math_isnan(c_needed_raw(1.0, 0.0, 1.0)))

    def test_printed_results_include_requested_columns(self):
        lambda0 = reference_lambda0("taylor-green", 8)
        rows = [
            run_one("abc", 1.0, reference_lambda0("abc", 8), n=8),
            run_one("taylor-green", 1.0, lambda0, n=8),
        ]
        text = format_table(rows)
        self.assertIn("SNAPSHOT TESTS", text)
        self.assertIn("amplitude", text)
        self.assertIn("fixed threshold", text)
        self.assertIn("bad-pair integral", text)
        self.assertIn("C_needed_raw", text)
        self.assertIn("ABC", text)
        self.assertIn("Taylor–Green", text)
        payload = sweep(n=8, amps=(1.0,))
        self.assertIn("C_needed_raw", payload["printed"])
        self.assertFalse(payload["leftover_1_closed"])
        self.assertEqual(payload["label"], "snapshot test")

    def test_page_labels_snapshot_and_does_not_close_leftover_1(self):
        text = PAGE.read_text()
        self.assertIn("snapshot test", text.lower())
        self.assertIn("Lambda0", text)
        self.assertIn("C_needed_raw", text)
        self.assertIn("Taylor–Green", text)
        self.assertIn("not leftover 1", text.lower())
        self.assertIn("Do not start", text)
        self.assertNotIn("H1 is a theorem", text)
        self.assertNotIn("NS is solved", text)
        write = WRITE.read_text()
        self.assertIn("H1-ABAD-SNAPSHOT.md", write)
        self.assertIn("Do not start this write from ABC", write)


def math_isnan(value: float) -> bool:
    return value != value


if __name__ == "__main__":
    unittest.main()
