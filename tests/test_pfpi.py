"""Tests for PFPI search spine and spell runner."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestPFPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmpdir = tempfile.TemporaryDirectory()
        cls.db_path = Path(cls._tmpdir.name) / "test_pfpi.db"
        from tools.pfpi.ingest import ingest_all

        cls.stats = ingest_all(cls.db_path, clear=True)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmpdir.cleanup()

    def test_ingest_count(self) -> None:
        self.assertGreater(self.stats["total"], 50)
        self.assertGreaterEqual(self.stats["zenodo"], 14)
        self.assertGreaterEqual(self.stats["ledger"], 20)

    def test_search_bridge_star(self) -> None:
        from tools.pfpi.search import search

        hits = search("Bridge multi-rep", db_path=self.db_path, limit=5)
        self.assertTrue(hits)
        titles = " ".join(h.title.lower() for h in hits)
        self.assertTrue(
            "bridge" in titles or any("bridge" in (h.snippet or "").lower() for h in hits)
        )

    def test_search_lead_filter(self) -> None:
        from tools.pfpi.search import search

        hits = search("spectral", db_path=self.db_path, da_status="LEAD", limit=10)
        self.assertTrue(hits)
        for hit in hits:
            self.assertEqual(hit.da_status, "LEAD")
            self.assertEqual(hit.warning, "LEAD — structural rhyme, not proved")

    def test_cut_warning_when_included(self) -> None:
        from tools.pfpi.search import search

        hits = search("Triple Lock", db_path=self.db_path, include_cut=True, limit=5)
        cut_hits = [h for h in hits if h.keep_cut == "CUT"]
        if cut_hits:
            self.assertEqual(cut_hits[0].warning, "CUT — do not cite as proof")

    def test_ledger_filter(self) -> None:
        from tools.pfpi.ledger import filter_ledger

        leads = filter_ledger(status="LEAD")
        self.assertEqual(len(leads), 4)
        ids = {e["id"] for e in leads}
        self.assertIn("lead-spectral-constant", ids)

    def test_ledger_json_valid(self) -> None:
        path = REPO_ROOT / "tools/pfpi/ledger.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertIn("entries", data)
        self.assertEqual(data["summary"]["LEAD"], 4)


class TestSpellRunner(unittest.TestCase):
    def test_list_spells(self) -> None:
        from packages.shared_core.spell_runner import list_spells

        spells = list_spells()
        self.assertIn("sfe_bh_overlay", spells)
        self.assertTrue(Path(REPO_ROOT / spells["sfe_bh_overlay"]["script"]).exists())

    def test_run_bridge_floor_small(self) -> None:
        from packages.shared_core.spell_runner import run_spell

        result = run_spell("bridge_floor_verify", {"Nmax": 30})
        self.assertEqual(result["returncode"], 0)
        self.assertIn("λ_min", result["stdout"] or result["stderr"] or "")

    def test_unknown_spell_raises(self) -> None:
        from packages.shared_core.spell_runner import run_spell

        with self.assertRaises(KeyError):
            run_spell("not_a_spell")


if __name__ == "__main__":
    unittest.main()
