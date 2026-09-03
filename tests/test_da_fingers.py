"""Five-finger DA recursion smoke tests."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_fingers import GENERAL_FATE_KEYS, LINE, SIXTEEN, TOE_CATEGORIES, run  # noqa: E402


class DaFingersTests(unittest.TestCase):
    def test_line_has_five_fingers_and_each_has_five(self):
        tmp = Path(tempfile.mkdtemp()) / "da_fingers_test.json"
        payload = run(n=80, seed=1, out=tmp)
        self.assertEqual(payload["meta"]["line"], LINE)
        fingers = payload["tree"]["fingers"]
        self.assertEqual(len(fingers), 5)
        self.assertEqual([f["name"] for f in fingers], ["R", "kernel", "chi_ext", "chi_int", "F"])
        for f in fingers:
            self.assertEqual(len(f["fingers"]), 5, f["name"])

    def test_product_identity_and_implied_f_fail(self):
        tmp = Path(tempfile.mkdtemp()) / "da_fingers_test.json"
        payload = run(n=80, seed=1, out=tmp)
        self.assertLess(payload["checks"]["product_identity_err"], 1e-12)
        self.assertEqual(payload["tree"]["fingers"][4]["verdict"], "fail")
        self.assertEqual(payload["checks"]["affine_F"]["verdict"], "fail")

    def test_equal_width_flattens_external(self):
        tmp = Path(tempfile.mkdtemp()) / "da_fingers_test.json"
        payload = run(n=200, seed=1, out=tmp)
        self.assertTrue(payload["checks"]["equal_width_flattens_ext"])
        default = payload["checks"]["ext_contrib_default"]
        self.assertGreater(default["log_cc_ratio"], default["log_alpha_em"])

    def test_sixteen_have_categories_and_r_is_output(self):
        tmp = Path(tempfile.mkdtemp()) / "da_fingers_test.json"
        payload = run(n=40, seed=1, out=tmp)
        self.assertEqual(len(payload["candidates"]), 16)
        self.assertEqual({c["category"] for c in payload["candidates"]}, set(TOE_CATEGORIES))
        sixteenth = payload["candidates"][-1]
        self.assertEqual(sixteenth["name"], "R")
        self.assertEqual(sixteenth["fate"], "output")
        theta = next(c for c in payload["candidates"] if c["name"] == "theta_qcd")
        self.assertEqual(theta["category"], "topological")
        self.assertEqual(SIXTEEN[-1], "R")

    def test_each_candidate_has_the_same_five_general_questions(self):
        tmp = Path(tempfile.mkdtemp()) / "da_fingers_test.json"
        payload = run(n=40, seed=1, out=tmp)
        self.assertEqual(len(payload["candidates"]), 16)
        for rec in payload["candidates"]:
            keys = [f["name"] for f in rec["hand"]]
            self.assertEqual(keys, list(GENERAL_FATE_KEYS), rec["name"])
            nxt = rec["hand"][4]
            self.assertEqual(nxt["name"], "next_piece")
            self.assertTrue(nxt.get("fingers"), rec["name"])
        r_hand = payload["candidates"][-1]["hand"]
        self.assertEqual(r_hand[1]["verdict"], "fail")
        self.assertEqual(r_hand[3]["verdict"], "fail")


if __name__ == "__main__":
    unittest.main()
