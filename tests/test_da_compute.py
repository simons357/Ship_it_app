"""Computing techniques: wired / borrow / refuse, no fake close."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_compute import TECH, run  # noqa: E402


class DaComputeTests(unittest.TestCase):
    def test_wired_legal_refuse_closes(self):
        tmp = Path(tempfile.mkdtemp()) / "da_compute_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["C1"]["verdict"], "pass")
        self.assertEqual(by["C2"]["verdict"], "pass")
        self.assertEqual(by["C3"]["verdict"], "fail")
        self.assertEqual(by["C4"]["verdict"], "fail")
        names = {t["name"]: t for t in TECH}
        self.assertEqual(names["numpy_fft_galerkin"]["status"], "wired")
        self.assertEqual(names["numpy_eigh_gcd"]["slot"], "Q")
        self.assertEqual(names["lp_bony_fft"]["status"], "borrow")
        self.assertEqual(names["dns_never_blew_up"]["verdict"], "fail")
        self.assertEqual(names["llm_proves_the_theorem"]["verdict"], "fail")
        self.assertIn("numpy_fft_galerkin", payload["already"])
        self.assertIn("sympy_identities", payload["borrow"])
        self.assertIn("dns_never_blew_up", payload["refuse"])
        self.assertTrue(payload["meta"]["does_not_close_B"])
        self.assertEqual(len(TECH), len({t["id"] for t in TECH}))


if __name__ == "__main__":
    unittest.main()
