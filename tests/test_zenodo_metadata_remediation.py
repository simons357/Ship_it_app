"""Tests for Zenodo metadata remediation helper."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "zenodo_metadata_remediation.py"
METADATA = ROOT / "data" / "zenodo" / "deposit_metadata.json"
UPLOAD_PACK = ROOT / "data" / "zenodo" / "upload_packs" / "21071991"
SWIRL_TEX = ROOT / "docs" / "papers" / "swirl" / "Simons_PhiRenorm_Swirl_2026-06-30.tex"
PHI_TEX = ROOT / "docs" / "papers" / "phi-renorm" / "Simons_PhiRenorm_Swirl_2026-06-30.tex"


def _load_script_module():
    import importlib.util

    spec = importlib.util.spec_from_file_location("zenodo_metadata_remediation", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


class ZenodoMetadataRemediationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_script_module()

    def test_metadata_json_loads(self):
        with METADATA.open(encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertGreaterEqual(len(data["deposits"]), 20)
        self.assertIn("presentation_rule", data)
        self.assertIn("live_audit_summary", data)

    def test_keep_set_present(self):
        with METADATA.open(encoding="utf-8") as fh:
            data = json.load(fh)
        keep_ids = {
            d["record_id"]
            for d in data["deposits"]
            if d.get("disposition") == "KEEP" and d.get("record_id")
        }
        self.assertEqual(
            keep_ids,
            {22050962, 22050974, 22050975, 22050976, 22050965, 22050963, 22050978, 21071991},
        )

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

    def test_strip_errata_banner_and_trailing_quote(self):
        clean = self.mod.strip_errata_banner(
            "[Claim withdrawn - see errata] Triple Lock title"
        )
        self.assertEqual(clean, "Triple Lock title")
        self.assertEqual(
            self.mod.strip_errata_banner('Route C: Spectral Closure"'),
            "Route C: Spectral Closure",
        )

    def test_build_errata_block_park(self):
        with METADATA.open(encoding="utf-8") as fh:
            inventory = json.load(fh)
        deposit = next(d for d in inventory["deposits"] if d["slug"] == "triple-lock")
        block = self.mod.build_errata_description_block(deposit, inventory)
        self.assertIn("Correction notice (August 2026)", block)
        self.assertIn("22050978", block)
        self.assertIn("https://doi.org/10.5281/zenodo.", block)
        self.assertIn("dated archive", block)

    def test_build_errata_block_phirenorm_file_fix(self):
        with METADATA.open(encoding="utf-8") as fh:
            inventory = json.load(fh)
        deposit = next(d for d in inventory["deposits"] if d["record_id"] == 21071991)
        block = self.mod.build_errata_description_block(deposit, inventory)
        self.assertIn("File correction notice", block)
        self.assertIn("1.3", block)
        self.assertIn("conditional", block.lower())
        self.assertNotIn("Clay Statement (B).</p>\n<p>This deposit is kept as", block)

    def test_no_stale_errata_title_flags_as_live_truth(self):
        """Live titles were cleaned; metadata must not pretend banners are still present."""
        with METADATA.open(encoding="utf-8") as fh:
            inventory = json.load(fh)
        live_banners = [d for d in inventory["deposits"] if d.get("errata_in_title")]
        self.assertEqual(live_banners, [])
        self.assertGreaterEqual(inventory["live_audit_summary"]["needs_description_errata"], 1)
        self.assertEqual(inventory["live_audit_summary"]["needs_file_fix"], 1)

    def test_upload_pack_has_corrected_tex_pdf(self):
        tex = (UPLOAD_PACK / "Simons_PhiRenorm_Swirl_2026-06-30.tex").read_text(encoding="utf-8")
        self.assertNotIn(r"\dot H^{2.6}", tex)
        self.assertIn(r"\dot H^{1.3}", tex)
        self.assertTrue((UPLOAD_PACK / "Simons_PhiRenorm_Swirl_2026-06-30.pdf").exists())
        self.assertTrue((UPLOAD_PACK / "README.md").exists())

    def test_phi_renorm_mirror_matches_swirl(self):
        self.assertEqual(
            SWIRL_TEX.read_text(encoding="utf-8"),
            PHI_TEX.read_text(encoding="utf-8"),
        )

    def test_package_files_idempotent(self):
        info = self.mod.package_files()
        self.assertFalse(info["hdot_26_in_tex"])
        self.assertTrue(info["hdot_13_in_tex"])

    def test_write_docs_creates_deposit_files(self):
        with METADATA.open(encoding="utf-8") as fh:
            inventory = json.load(fh)
        self.mod.write_deposit_docs(inventory)
        out = ROOT / "docs" / "zenodo" / "deposits" / "triple-lock.md"
        self.assertTrue(out.exists())
        text = out.read_text(encoding="utf-8")
        self.assertIn("Clean title", text)
        self.assertIn("Correction notice", text)
        phirenorm = ROOT / "docs" / "zenodo" / "deposits" / "phirenorm-june30-conditional.md"
        self.assertTrue(phirenorm.exists())
        self.assertIn("File correction", phirenorm.read_text(encoding="utf-8"))

    def test_token_help_mentions_export(self):
        help_text = self.mod.token_help()
        self.assertIn("ZENODO_ACCESS_TOKEN", help_text)
        self.assertIn("apply --record-id 21071991", help_text)


if __name__ == "__main__":
    unittest.main()
