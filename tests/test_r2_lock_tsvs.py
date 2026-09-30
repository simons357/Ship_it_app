#!/usr/bin/env python3
"""R2 folder lock pair: M.tsv and b_exact.tsv."""

from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from r2_lock_tsvs import (  # noqa: E402
    B_EXACT_TSV,
    J_ROWS,
    M_TSV,
    N_COLS,
    N_ROWS,
    PI12_ERRORS,
    R2_DIR,
    WEAK_IDENTITIES,
    build_M,
    build_b_exact,
    check_identities,
    check_weak_residues,
    load_tsv_matrix,
    write_all,
)


class TestR2FilesExist(unittest.TestCase):
    def test_folder_and_names(self):
        self.assertTrue(R2_DIR.is_dir())
        self.assertEqual(M_TSV.name, "M.tsv")
        self.assertEqual(B_EXACT_TSV.name, "b_exact.tsv")
        self.assertTrue(M_TSV.is_file(), "M.tsv missing from data/R2")
        self.assertTrue(B_EXACT_TSV.is_file(), "b_exact.tsv missing from data/R2")


class TestMatrixShapeAndIdentities(unittest.TestCase):
    def test_committed_M_is_20x12_integer(self):
        M = load_tsv_matrix(M_TSV)
        self.assertEqual(len(M), N_ROWS)
        for row in M:
            self.assertEqual(len(row), N_COLS)
            for x in row:
                self.assertEqual(x.denominator, 1)

    def test_committed_M_obeys_six_identities(self):
        rec = check_identities(load_tsv_matrix(M_TSV))
        self.assertTrue(rec["ok"], rec)

    def test_builder_matches_committed_file(self):
        built = [[Fraction(v) for v in row] for row in build_M()]
        loaded = load_tsv_matrix(M_TSV)
        self.assertEqual(built, loaded)

    def test_identity_table_is_the_B42_table(self):
        self.assertEqual(set(WEAK_IDENTITIES), set(J_ROWS))
        self.assertEqual(WEAK_IDENTITIES[14], {1: -1, 3: 1, 12: 1})
        self.assertEqual(WEAK_IDENTITIES[19], {2: -1, 4: 1, 5: -1, 7: 1, 10: 1})


class TestBExact(unittest.TestCase):
    def test_twenty_rational_phases(self):
        rows = load_tsv_matrix(B_EXACT_TSV)
        self.assertEqual(len(rows), N_ROWS)
        for row in rows:
            self.assertEqual(len(row), 1)
            self.assertIsInstance(row[0], Fraction)

    def test_strong_rows_vanish_at_yA(self):
        beta = [row[0] for row in load_tsv_matrix(B_EXACT_TSV)]
        for i in range(14):
            self.assertEqual(beta[i], 0)

    def test_weak_residues_match_pi12_errors(self):
        M = load_tsv_matrix(M_TSV)
        beta = [row[0] for row in load_tsv_matrix(B_EXACT_TSV)]
        rec = check_weak_residues(M, beta)
        self.assertTrue(rec["ok"], rec)
        self.assertEqual(list(PI12_ERRORS), [20, -4, 16, 8, 4, 4])

    def test_builder_matches_committed_file(self):
        beta = build_b_exact(build_M())
        loaded = [row[0] for row in load_tsv_matrix(B_EXACT_TSV)]
        self.assertEqual(beta, loaded)


class TestWriterRoundTrip(unittest.TestCase):
    def test_write_all_is_idempotent_on_committed_pair(self):
        before_M = M_TSV.read_text()
        before_b = B_EXACT_TSV.read_text()
        rec = write_all()
        self.assertTrue(rec["identities"]["ok"], rec)
        self.assertTrue(rec["weak_residues"]["ok"], rec)
        self.assertEqual(M_TSV.read_text(), before_M)
        self.assertEqual(B_EXACT_TSV.read_text(), before_b)


if __name__ == "__main__":
    unittest.main()
