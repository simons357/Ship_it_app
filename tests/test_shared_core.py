"""Tests for platform spine v0."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from packages.shared_core.config import get_product, load_registry, load_spell_registry
from packages.shared_core.link_resolver import link_status, resolve_url

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestSharedCore(unittest.TestCase):
    def test_registry_loads(self) -> None:
        reg = load_registry()
        self.assertIn("products", reg)
        self.assertIn("field-lock", reg["products"])

    def test_field_lock_prefers_replit(self) -> None:
        url = resolve_url("field-lock")
        self.assertEqual(url, "https://field-lock.replit.app/")

    def test_arbiter_prefers_base44_not_hollow_hub(self) -> None:
        url = resolve_url("arbiter")
        self.assertEqual(url, "https://arbiter.base44.app/")
        status = link_status("arbiter")
        self.assertEqual(status["status"], "live")
        self.assertTrue(status["safe_for_outreach"])

    def test_chatvault_is_not_outreach_safe(self) -> None:
        status = link_status("chatvault")
        self.assertFalse(status["safe_for_outreach"])
        self.assertEqual(status["status"], "hollow")

    def test_exo_ratio_is_cut(self) -> None:
        status = link_status("exo-ratio")
        self.assertFalse(status["safe_for_outreach"])
        self.assertEqual(status["keep_cut"], "CUT")

    def test_env_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = REPO_ROOT / "packages/shared_core/product_registry.json"
            dst = Path(tmp) / "product_registry.json"
            data = json.loads(src.read_text(encoding="utf-8"))
            data["products"]["chatvault"]["urls"]["canonical"] = "https://chatvault.example.com/"
            data["products"]["chatvault"]["status"] = "live"
            dst.write_text(json.dumps(data), encoding="utf-8")

            import os

            old = os.environ.pop("PF_CHATVAULT_URL", None)
            try:
                os.environ["PF_CHATVAULT_URL"] = "https://env-override.example.com/"
                reg = load_registry(dst)
                url = resolve_url("chatvault", reg)
                self.assertEqual(url, "https://env-override.example.com/")
            finally:
                if old is not None:
                    os.environ["PF_CHATVAULT_URL"] = old
                else:
                    os.environ.pop("PF_CHATVAULT_URL", None)

    def test_spell_registry_has_overlay(self) -> None:
        spells = load_spell_registry()
        self.assertIn("sfe_bh_overlay", spells["spells"])
        entry = spells["spells"]["sfe_bh_overlay"]
        self.assertTrue(Path(REPO_ROOT / entry["script"]).exists())

    def test_get_product_unknown_raises(self) -> None:
        reg = load_registry()
        with self.assertRaises(KeyError):
            get_product(reg, "not-a-product")


if __name__ == "__main__":
    unittest.main()
