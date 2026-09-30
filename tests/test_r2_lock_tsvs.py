#!/usr/bin/env python3
"""R2 synthetic fixture + read-only verifier: M.tsv and b_exact.tsv."""

from __future__ import annotations

import json
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
    PROVENANCE_JSON,
    R2_DIR,
    WEAK_IDENTITIES,
    build_M,
    build_b_exact,
    check_identities,
    check_weak_residues,
    load_tsv_matrix,
    sha256_file,
    verify,
)
from r2_read_only_verifier import verify as readonly_verify  # noqa: E402


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

    def test_builder_matches_committed_M(self):
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

    def test_builder_matches_committed_b_exact(self):
        beta = build_b_exact(build_M())
        loaded = [row[0] for row in load_tsv_matrix(B_EXACT_TSV)]
        self.assertEqual(beta, loaded)


class TestSyntheticFixture(unittest.TestCase):
    def test_provenance_is_synthetic_fixture(self):
        rec = json.loads(PROVENANCE_JSON.read_text())
        self.assertEqual(rec["provenance"], "synthetic_fixture")
        self.assertEqual(rec.get("verifier"), "read-only")
        self.assertTrue(rec["not_library_json"])

    def test_readme_identifies_synthetic_fixture(self):
        text = (R2_DIR / "README.md").read_text()
        self.assertIn("synthetic fixture", text.lower())
        self.assertIn("read-only", text.lower())

    def test_tsv_headers_say_synthetic_fixture(self):
        self.assertIn("SYNTHETIC FIXTURE", M_TSV.read_text())
        self.assertIn("SYNTHETIC FIXTURE", B_EXACT_TSV.read_text())

    def test_sha256_matches_provenance(self):
        rec = json.loads(PROVENANCE_JSON.read_text())
        self.assertEqual(rec["sha256"]["M.tsv"], sha256_file(M_TSV))
        self.assertEqual(rec["sha256"]["b_exact.tsv"], sha256_file(B_EXACT_TSV))


class TestReadOnlyVerifier(unittest.TestCase):
    def test_verify_report_is_read_only(self):
        rec = verify()
        self.assertTrue(rec["read_only"])
        self.assertTrue(rec["synthetic_fixture"])
        self.assertTrue(rec["ok"], rec)
        self.assertEqual(rec["canonical_r2_identity"], "unverified")
        self.assertEqual(rec["classical_NS"], "open")

    def test_verifier_does_not_write(self):
        before = {
            "M": M_TSV.read_bytes(),
            "b": B_EXACT_TSV.read_bytes(),
            "p": PROVENANCE_JSON.read_bytes(),
        }
        rec = readonly_verify()
        self.assertTrue(rec["read_only"])
        self.assertEqual(M_TSV.read_bytes(), before["M"])
        self.assertEqual(B_EXACT_TSV.read_bytes(), before["b"])
        self.assertEqual(PROVENANCE_JSON.read_bytes(), before["p"])

    def test_canonical_r2_unverified(self):
        rec = verify()
        self.assertEqual(rec["canonical_r2_identity"], "unverified")
        self.assertFalse(rec.get("canonical_statement_ready", False))


if __name__ == "__main__":
    unittest.main()
