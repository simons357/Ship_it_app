"""Tests for Zenodo metadata remediation helper."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "zenodo_metadata_remediation.py"
METADATA = ROOT / "data" / "zenodo" / "deposit_metadata.json"


def _load_script_module():
    import importlib.util

    spec = importlib.util.spec_from_file_location("zenodo_metadata_remediation", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ZenodoMetadataRemediationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_script_module()

    def test_metadata_json_loads(self):
        with METADATA.open(encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertGreaterEqual(len(data["deposits"]), 10)
        self.assertIn("presentation_rule", data)

    def test_errata_banner_detection(self):
        self.assertTrue(
            self.mod.has_errata_banner(
                "[Claim withdrawn - see errata] Global Regularity of the Navier-Stokes"
            )
        )
        self.assertTrue(
            self.mod.has_errata_banner(
                "[Superseded - see errata] Borromean Triads, the Ring Lemma"
            )
        )
        self.assertFalse(
            self.mod.has_errata_banner(
                "Phi-Renormalization for Axisymmetric Navier-Stokes with Swirl"
            )
        )

    def test_strip_errata_banner(self):
        clean = self.mod.strip_errata_banner(
            "[Claim withdrawn - see errata] Triple Lock title"
        )
        self.assertEqual(clean, "Triple Lock title")

    def test_build_errata_block_contains_status_index(self):
        with METADATA.open(encoding="utf-8") as fh:
            inventory = json.load(fh)
        deposit = next(d for d in inventory["deposits"] if d["slug"] == "triple-lock")
        block = self.mod.build_errata_description_block(deposit, inventory)
        self.assertIn("Correction notice (August 2026)", block)
        self.assertIn("22050978", block)
        self.assertIn("Triple Lock", "".join(deposit["claims_withdrawn"]))

    def test_inventory_flags_eight_errata_title_records(self):
        with METADATA.open(encoding="utf-8") as fh:
            inventory = json.load(fh)
        flagged = [d for d in inventory["deposits"] if d.get("errata_in_title")]
        self.assertEqual(len(flagged), 8)

    def test_write_docs_creates_deposit_files(self):
        with METADATA.open(encoding="utf-8") as fh:
            inventory = json.load(fh)
        self.mod.write_deposit_docs(inventory)
        out = ROOT / "docs" / "zenodo" / "deposits" / "triple-lock.md"
        self.assertTrue(out.exists())
        text = out.read_text(encoding="utf-8")
        self.assertIn("Clean title", text)
        self.assertIn("Correction notice", text)


if __name__ == "__main__":
    unittest.main()
