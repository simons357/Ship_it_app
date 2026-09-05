"""DA product: capabilities spec; not a leftover closer."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_product import CLAIMS, is_product_ask, run  # noqa: E402
from da_proof import is_proof_ask  # noqa: E402
from da_study import is_study_ask  # noqa: E402


class DaProductTests(unittest.TestCase):
    def test_spec_is_not_qed(self):
        tmp = Path(tempfile.mkdtemp()) / "da_product_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["L1"]["verdict"], "pass")
        self.assertEqual(by["L2"]["verdict"], "pass")
        self.assertEqual(by["L3"]["verdict"], "fail")
        self.assertEqual(by["L4"]["verdict"], "fail")
        self.assertEqual(by["L5"]["verdict"], "fail")
        self.assertTrue(payload["meta"]["not_a_contract"])
        self.assertFalse(payload["meta"]["sell_as_qed"])
        ask = (
            "I gotta know what's under the hood and what I can do with it "
            "if I choose to sell it or license it out"
        )
        self.assertTrue(is_product_ask(ask))
        self.assertFalse(is_study_ask(ask))
        self.assertFalse(is_proof_ask(ask))
        self.assertTrue(is_product_ask("capabilities"))
        self.assertFalse(is_product_ask(""))
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-PRODUCT.md").is_file())
        text = (ROOT / "docs" / "DA-PRODUCT.md").read_text()
        self.assertIn("not a leftover solver", text)
        self.assertIn("not a contract", text)
        conf = ROOT / "docs" / "DA-CONFIDENTIAL.md"
        self.assertTrue(conf.is_file())
        body = conf.read_text()
        self.assertIn("Operator-confidential", body)
        self.assertIn("Radial structure", body)
        self.assertIn("One-WRITE intake", body)
        self.assertTrue((ROOT / "docs" / "figures" / "da-radial-hub.png").is_file())
        self.assertTrue((ROOT / "docs" / "figures" / "da-four-slots.png").is_file())


if __name__ == "__main__":
    unittest.main()
