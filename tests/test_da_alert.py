"""Plain-language alerts on a watched flip, not on catalog churn."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_alert import WATCH, flips, notify, render_text  # noqa: E402


class DaAlertTests(unittest.TestCase):
    def test_baseline_not_significant_flip_is(self):
        tmp = Path(tempfile.mkdtemp())
        first = notify(
            source="test",
            state_path=tmp / "state.json",
            out_json=tmp / "a1.json",
            out_txt=tmp / "a1.txt",
        )
        self.assertTrue(first["meta"]["baseline"])
        self.assertFalse(first["meta"]["significant"])
        self.assertTrue(first["meta"]["no_phone_in_repo"])
        self.assertIn("baseline", first["plain"].lower())

        second = notify(
            source="test",
            state_path=tmp / "state.json",
            out_json=tmp / "a2.json",
            out_txt=tmp / "a2.txt",
        )
        self.assertFalse(second["meta"]["baseline"])
        self.assertFalse(second["meta"]["significant"])

        prev = {"B.B4b_hardy_not_I_tube": "open", "U.F_exists": "fail"}
        cur = {"B.B4b_hardy_not_I_tube": "fail", "U.F_exists": "fail"}
        ev = flips(prev, cur)
        self.assertEqual(len(ev), 1)
        self.assertEqual(ev[0]["slot"], "B")
        self.assertIn("wall", ev[0]["head"].lower() + ev[0]["next"].lower())
        text = render_text(ev, baseline=False)
        self.assertIn("WHAT IT MEANS", text)
        self.assertIn("WHAT TO DO", text)
        self.assertIn("DO NOT", text)
        self.assertIn("B.B4b_hardy_not_I_tube", WATCH)

    def test_catalog_keys_are_not_watched(self):
        self.assertNotIn("U.harmonic_vocab", WATCH)
        self.assertNotIn("U.desk", WATCH)


if __name__ == "__main__":
    unittest.main()
