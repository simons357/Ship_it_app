#!/usr/bin/env python3
"""B42 tests: first-order T2-ray coefficient, not a close."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.t2_starvation_coefficient import (  # noqa: E402
    D_A,
    F_15_16,
    LIBRARY_JSON_SHA256,
    PI12_ERRORS,
    WEAK_IDENTITIES,
    check_identities,
    cos_of_pi12,
    cosine_and_DA_check,
    d_phase,
    first_order_numeric,
    four_cycle_relative_phase,
    identity_implication_check,
    lock_status,
    parallelogram_helicity_20x12,
    parallelogram_reconstruction_check,
    pi12_to_fraction,
    run_report,
    synthetic_matrix,
    two_row_min_numeric,
    weak_cosines,
    weak_deficits,
)


class TestCosineArithmetic(unittest.TestCase):
    def test_pi12_errors_to_half_integers(self):
        self.assertEqual(
            [float(cos_of_pi12(n)) for n in PI12_ERRORS],
            [0.5, 0.5, -0.5, -0.5, 0.5, 0.5],
        )
        self.assertEqual(
            [float(d) for d in weak_deficits()],
            [0.5, 0.5, 1.5, 1.5, 0.5, 0.5],
        )

    def test_minus_four_is_same_cosine_as_twenty(self):
        self.assertEqual(cos_of_pi12(-4), cos_of_pi12(20))

    def test_turn_fraction(self):
        self.assertEqual(pi12_to_fraction(20), pi12_to_fraction(20) % 1)
        self.assertEqual(float(pi12_to_fraction(4)), 4 / 24)

    def test_D_A_matches_deficits(self):
        rec = cosine_and_DA_check()
        self.assertTrue(rec["ok"], rec)
        C = list(range(1, 21))
        self.assertAlmostEqual(
            D_A(C),
            (C[14] + C[15] + C[18] + C[19] + 3 * (C[16] + C[17])) / 2.0,
        )


class TestTwoRowBound(unittest.TestCase):
    def test_closed_form_matches_grid(self):
        rec = four_cycle_relative_phase()
        self.assertTrue(rec["ok"], rec)

    def test_positive_for_positive_coefficients(self):
        self.assertGreater(F_15_16(1.0, 1.0), 0.0)
        self.assertAlmostEqual(F_15_16(1.0, 1.0), 2.0 - math.sqrt(3.0), places=12)

    def test_strictly_below_D_A_on_ones(self):
        C = [1.0] * 20
        self.assertGreater(D_A(C), F_15_16(C[15], C[16]))
        self.assertAlmostEqual(D_A(C), 5.0)

    def test_numeric_min_near_ones(self):
        exact = F_15_16(1.0, 1.0)
        numeric = two_row_min_numeric(1.0, 1.0, n=50000)
        self.assertLess(abs(exact - numeric), 1e-8)


class TestFirstOrderLimit(unittest.TestCase):
    def test_synthetic_one_dimensional_ray(self):
        rec = first_order_numeric()
        self.assertTrue(rec["ok"], rec)
        self.assertAlmostEqual(rec["m_J"], 0.5, places=12)
        self.assertAlmostEqual(rec["target"], 0.5 / 3.0, places=12)
        self.assertLess(rec["max_abs_err_smallest_t"], 5e-4)

    def test_deficit_positive(self):
        rec = first_order_numeric()
        for s in rec["samples"]:
            self.assertGreater(s["deficit"], 0.0)


class TestIntegerIdentities(unittest.TestCase):
    def test_synthetic_matrix_satisfies_claimed_identities(self):
        M = synthetic_matrix()
        rec = check_identities(M)
        self.assertTrue(rec["ok"], rec)
        self.assertEqual(M.shape, (20, 12))

    def test_identity_count_and_support(self):
        self.assertEqual(set(WEAK_IDENTITIES), set(range(14, 20)))
        self.assertEqual(WEAK_IDENTITIES[14], {1: -1, 3: 1, 12: 1})
        self.assertEqual(WEAK_IDENTITIES[17], {0: -1, 3: 1, 12: 1})

    def test_implication_F_J_equals_D_A_on_Z_K(self):
        rec = identity_implication_check()
        self.assertTrue(rec["ok"], rec)
        self.assertTrue(rec["F_J_equals_D_A"])
        self.assertTrue(rec["Z_K_nonempty_by_construction"])

    def test_broken_row_is_detected(self):
        M = synthetic_matrix()
        M[14, 0] += 1
        rec = check_identities(M)
        self.assertFalse(rec["ok"])
        self.assertEqual(rec["mismatches"][0]["row"], 14)


class TestParallelogramIsNotTheJSON(unittest.TestCase):
    def test_live_parallelogram_does_not_match_claimed_identities(self):
        rec = parallelogram_reconstruction_check()
        self.assertEqual(rec["shape"], [20, 12])
        self.assertFalse(rec["identities_hold"])
        self.assertEqual(parallelogram_helicity_20x12().shape, (20, 12))


class TestLockAndPacket(unittest.TestCase):
    def test_library_hash_is_the_stated_one(self):
        self.assertEqual(
            LIBRARY_JSON_SHA256,
            "87745b3cb585e138b6768ab5b9e330f3f045ff4d4ad82ba6f71f0b6fe86be898",
        )

    def test_locked_files_absent_in_this_checkout(self):
        rec = lock_status()
        self.assertFalse(rec["library_json"]["found"])
        self.assertFalse(rec["locked_tsvs"]["both_present"])
        self.assertFalse(rec["matrix_row_check"]["ok"])
        self.assertEqual(rec["classical_NS"], "open")
        self.assertEqual(rec["canonical_r2_identity"], "unverified")

    def test_run_report_refuses_canonical_close(self):
        report = run_report()
        self.assertTrue(report["all_independent_checks_ok"], report)
        self.assertFalse(report["canonical_statement_ready"])
        self.assertTrue(report["not_a_close"])
        self.assertFalse(report["scope"]["classical_NS_closed"])
        self.assertFalse(report["scope"]["drag_reduction"])
        self.assertFalse(
            report["json_row_identities"]["verified_on_hashed_json_or_locked_tsv"]
        )

    def test_deficit_d_phase_zeros_on_integers(self):
        self.assertAlmostEqual(d_phase(0.0), 0.0, places=12)
        self.assertAlmostEqual(d_phase(1.0), 0.0, places=12)
        self.assertAlmostEqual(d_phase(0.5), 2.0, places=12)


if __name__ == "__main__":
    unittest.main()
