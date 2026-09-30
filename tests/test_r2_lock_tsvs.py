#!/usr/bin/env python3
"""R2 G3 computed-evidence pair + read-only verifier."""

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
    G3_JSON,
    J_ROWS,
    M_TSV,
    N_COLS,
    N_ROWS,
    PROVENANCE_JSON,
    R2_DIR,
    WEAK_IDENTITIES,
    check_identities,
    g3_turns,
    load_g3,
    load_tsv_matrix,
    match_g3,
    sha256_file,
    verify,
)
from r2_read_only_verifier import verify as readonly_verify  # noqa: E402


class TestR2FilesExist(unittest.TestCase):
    def test_folder_and_names(self):
        self.assertTrue(R2_DIR.is_dir())
        self.assertEqual(M_TSV.name, "M.tsv")
        self.assertEqual(B_EXACT_TSV.name, "b_exact.tsv")
        self.assertTrue(M_TSV.is_file())
        self.assertTrue(B_EXACT_TSV.is_file())
        self.assertTrue(G3_JSON.is_file())


class TestG3Matrix(unittest.TestCase):
    def test_committed_M_is_20x12_integer(self):
        M = load_tsv_matrix(M_TSV)
        self.assertEqual(len(M), N_ROWS)
        for row in M:
            self.assertEqual(len(row), N_COLS)
            for x in row:
                self.assertEqual(x.denominator, 1)

    def test_committed_M_matches_g3_json(self):
        M = [[int(x) for x in row] for row in load_tsv_matrix(M_TSV)]
        rows = [item["row"] for item in load_g3()["Gamma"]]
        self.assertEqual(M, rows)

    def test_committed_M_obeys_six_identities(self):
        rec = check_identities(load_tsv_matrix(M_TSV))
        self.assertTrue(rec["ok"], rec)

    def test_identity_table_is_the_B42_table(self):
        self.assertEqual(set(WEAK_IDENTITIES), set(J_ROWS))
        self.assertEqual(WEAK_IDENTITIES[14], {1: -1, 3: 1, 12: 1})
        self.assertEqual(WEAK_IDENTITIES[19], {2: -1, 4: 1, 5: -1, 7: 1, 10: 1})


class TestG3Targets(unittest.TestCase):
    def test_twenty_rational_phases(self):
        rows = load_tsv_matrix(B_EXACT_TSV)
        self.assertEqual(len(rows), N_ROWS)
        for row in rows:
            self.assertEqual(len(row), 1)
            self.assertIsInstance(row[0], Fraction)

    def test_b_matches_g3_turns(self):
        loaded = [row[0] for row in load_tsv_matrix(B_EXACT_TSV)]
        self.assertEqual(loaded, g3_turns())

    def test_g3_match_helper(self):
        rec = match_g3(load_tsv_matrix(M_TSV), [row[0] for row in load_tsv_matrix(B_EXACT_TSV)])
        self.assertTrue(rec["ok"], rec)
        self.assertEqual(rec["status"], "COMPUTED_EVIDENCE_ONLY")
        self.assertFalse(rec["kernel_or_holonomy_computed"])
        self.assertEqual(rec["conflicts"], 0)


class TestProvenance(unittest.TestCase):
    def test_g3_json_status(self):
        rec = load_g3()
        self.assertEqual(rec["gate"], "G3-corrected-channel-quotient")
        self.assertEqual(rec["status"], "COMPUTED_EVIDENCE_ONLY")
        self.assertEqual(rec["R"], 20)
        self.assertEqual(rec["n_columns"], 12)

    def test_provenance_is_computed_evidence(self):
        rec = json.loads(PROVENANCE_JSON.read_text())
        self.assertEqual(rec["provenance"], "g3_corrected_channel_quotient")
        self.assertEqual(rec.get("verifier"), "read-only")
        self.assertEqual(rec.get("status"), "COMPUTED_EVIDENCE_ONLY")
        self.assertTrue(rec["not_library_json"])
        self.assertFalse(rec.get("synthetic_fixture", True))

    def test_readme_identifies_computed_evidence(self):
        text = (R2_DIR / "README.md").read_text().lower()
        self.assertIn("computed_evidence_only", text)
        self.assertIn("read-only", text)
        self.assertIn("g3", text)

    def test_tsv_headers_say_g3_computed_evidence(self):
        self.assertIn("COMPUTED_EVIDENCE_ONLY", M_TSV.read_text())
        self.assertIn("COMPUTED_EVIDENCE_ONLY", B_EXACT_TSV.read_text())
        self.assertNotIn("SYNTHETIC FIXTURE", M_TSV.read_text())
        self.assertNotIn("SYNTHETIC FIXTURE", B_EXACT_TSV.read_text())

    def test_sha256_matches_provenance(self):
        rec = json.loads(PROVENANCE_JSON.read_text())
        self.assertEqual(rec["sha256"]["M.tsv"], sha256_file(M_TSV))
        self.assertEqual(rec["sha256"]["b_exact.tsv"], sha256_file(B_EXACT_TSV))
        self.assertEqual(rec["sha256"]["g3_json"], sha256_file(G3_JSON))


class TestReadOnlyVerifier(unittest.TestCase):
    def test_verify_report_is_read_only(self):
        rec = verify()
        self.assertTrue(rec["read_only"])
        self.assertFalse(rec["synthetic_fixture"])
        self.assertTrue(rec["computed_evidence_only"])
        self.assertTrue(rec["ok"], rec)
        self.assertEqual(rec["canonical_r2_identity"], "unverified")
        self.assertFalse(rec["kernel_or_holonomy_computed"])
        self.assertEqual(rec["classical_NS"], "open")

    def test_verifier_does_not_write(self):
        before = {
            "M": M_TSV.read_bytes(),
            "b": B_EXACT_TSV.read_bytes(),
            "p": PROVENANCE_JSON.read_bytes(),
            "g": G3_JSON.read_bytes(),
        }
        rec = readonly_verify()
        self.assertTrue(rec["read_only"])
        self.assertEqual(M_TSV.read_bytes(), before["M"])
        self.assertEqual(B_EXACT_TSV.read_bytes(), before["b"])
        self.assertEqual(PROVENANCE_JSON.read_bytes(), before["p"])
        self.assertEqual(G3_JSON.read_bytes(), before["g"])

    def test_canonical_r2_unverified(self):
        rec = verify()
        self.assertEqual(rec["canonical_r2_identity"], "unverified")
        self.assertFalse(rec.get("canonical_statement_ready", False))


if __name__ == "__main__":
    unittest.main()
