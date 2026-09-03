"""Live pipe: falsify verdicts, type current streams, refuse glue."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_pipe import FORMS, NOW, PIPES, VERDICTS, fetch_arxiv, run  # noqa: E402


class DaPipeTests(unittest.TestCase):
    def test_pipe_additive_glue_refused(self):
        tmp = Path(tempfile.mkdtemp()) / "da_pipe_test.json"
        payload = run(out=tmp, fetch=False)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["C1"]["verdict"], "pass")
        self.assertEqual(by["C2"]["verdict"], "fail")
        self.assertEqual(by["C3"]["verdict"], "fail")
        self.assertEqual(by["C4"]["verdict"], "fail")
        self.assertEqual(by["C5"]["verdict"], "fail")
        self.assertEqual(by["C6"]["verdict"], "fail")
        self.assertEqual(by["C7"]["verdict"], "fail")
        self.assertEqual(by["C8"]["verdict"], "fail")
        self.assertEqual(by["C9"]["verdict"], "pass")
        self.assertEqual(by["C10"]["verdict"], "fail")
        self.assertTrue(payload["meta"]["additive_to_team"])
        self.assertTrue(payload["meta"]["does_not_replace_past"])
        self.assertTrue(payload["meta"]["does_not_glue_primes_to_holes"])
        self.assertTrue(payload["meta"]["does_not_retune_nodes"])
        self.assertTrue(payload["meta"]["uses_wave_falsification"])
        self.assertEqual(payload["meta"]["snapshot"][:4], "2026")

    def test_forms_pipes_now_and_killers(self):
        forms = {r["name"] for r in FORMS}
        self.assertIn("graph", forms)
        self.assertIn("satellite", forms)
        self.assertIn("holographic_boundary", forms)
        names = {p["name"] for p in PIPES}
        self.assertIn("LVK_GWTC5", names)
        self.assertIn("EHT_M87", names)
        self.assertIn("DESI_DR2", names)
        self.assertIn("LMFDB_NT", names)
        slots = {p["name"]: p["slot"] for p in PIPES}
        self.assertEqual(slots["LMFDB_NT"], "Q")
        self.assertEqual(slots["arXiv_math_AP"], "B")
        self.assertEqual(slots["LVK_GWTC5"], "U")
        now = {m["name"] for m in NOW}
        self.assertIn("LVK collaboration", now)
        self.assertIn("EHT collaboration", now)
        self.assertIn("DESI collaboration", now)
        self.assertIn("LMFDB / analytic NT", now)
        for v in VERDICTS:
            self.assertTrue(v.get("killer"), v["id"])
        self.assertEqual(len(PIPES), len({p["id"] for p in PIPES}))
        self.assertEqual(len(VERDICTS), len({v["id"] for v in VERDICTS}))

    def test_fetch_arxiv_returns_structure(self):
        live = fetch_arxiv(timeout=2.0)
        self.assertIn("ok", live)
        self.assertIn("items", live)
        self.assertTrue(isinstance(live["items"], list))


if __name__ == "__main__":
    unittest.main()
