"""DA pack: reprint what sits; open WRITE stays open."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_pack import CLAIMS, is_pack_ask, run  # noqa: E402
from da_proof import is_all_ask, is_proof_ask  # noqa: E402
from da_study import is_study_ask  # noqa: E402


class DaPackTests(unittest.TestCase):
    def test_pack_is_status_not_qed(self):
        tmp = Path(tempfile.mkdtemp()) / "da_pack_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["P1"]["verdict"], "pass")
        self.assertEqual(by["P2"]["verdict"], "fail")
        self.assertEqual(by["P3"]["verdict"], "fail")
        self.assertEqual(by["P4"]["verdict"], "fail")
        self.assertTrue(payload["meta"]["emit_is_not_qed"])
        self.assertTrue(payload["meta"]["not_prize_packaging"])
        self.assertTrue(payload["meta"]["da_did_not_close_bsd"])
        self.assertTrue(payload["meta"]["sfe_is_not_hodge"])
        by_p = {row["problem"]: row for row in payload["status"]}
        self.assertTrue(by_p["POINCARE"]["leftover_sits"])
        self.assertFalse(by_p["BSD"]["leftover_sits"])
        self.assertFalse(by_p["HODGE"]["leftover_sits"])
        self.assertFalse(by_p["NS"]["leftover_sits"])
        pdf = ROOT / "docs" / "DA-STATUS-PACK.pdf"
        self.assertTrue(pdf.is_file())
        raw = pdf.read_bytes()
        self.assertTrue(raw.startswith(b"%PDF"))
        self.assertIn(b"DA leftover status pack", raw)
        self.assertIn(b"This is status. It is not QED.", raw)
        self.assertNotIn(b"prize packaging of a close", raw)
        pdf_ask = (
            "close out what you can on the millennials and then "
            "give them to me in like a PDF form"
        )
        self.assertTrue(is_pack_ask(pdf_ask))
        self.assertFalse(is_study_ask(pdf_ask))
        self.assertTrue(is_all_ask(ask=pdf_ask))
        self.assertTrue(is_proof_ask("Give me a master status report"))
        self.assertFalse(is_pack_ask("Give me a master status report"))
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-PACK.md").is_file())


if __name__ == "__main__":
    unittest.main()
