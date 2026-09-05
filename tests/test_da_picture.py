"""DA picture: a treatise names the next write; omniscience is not a slot."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_next import is_lost_ask  # noqa: E402
from da_picture import AREAS, CLAIMS, is_picture_ask, run  # noqa: E402


class DaPictureTests(unittest.TestCase):
    def test_survey_names_next_and_refuses_omniscience(self):
        tmp = Path(tempfile.mkdtemp()) / "da_picture_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["P1"]["verdict"], "pass")
        self.assertEqual(by["P2"]["verdict"], "pass")
        self.assertEqual(by["P3"]["verdict"], "fail")
        self.assertEqual(by["P4"]["verdict"], "fail")
        self.assertEqual(by["P5"]["verdict"], "fail")
        self.assertEqual(by["P6"]["verdict"], "pass")
        self.assertEqual(by["P7"]["verdict"], "open")
        self.assertEqual(by["P8"]["verdict"], "open")
        self.assertTrue(payload["meta"]["papers_not_minds"])
        self.assertTrue(payload["meta"]["not_a_genius_census"])
        self.assertTrue(payload["meta"]["picture_is_not_the_estimate"])
        ids = [a["id"] for a in AREAS]
        self.assertEqual(ids, ["B", "A", "RH", "Q", "SND", "H", "U"])
        self.assertIn("Lemarie-Rieusset", AREAS[0]["who"])
        self.assertIn("Ladyzhenskaya", AREAS[1]["who"])
        self.assertIn("Titchmarsh", AREAS[2]["who"])
        self.assertTrue(is_picture_ask("big picture advice"))
        self.assertTrue(is_picture_ask("what would they do next"))
        self.assertTrue(is_picture_ask("the most comprehensive knowledge"))
        self.assertFalse(is_picture_ask(""))
        self.assertFalse(is_picture_ask("now what"))
        self.assertTrue(is_lost_ask("now what"))
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-PICTURE.md").is_file())


if __name__ == "__main__":
    unittest.main()
