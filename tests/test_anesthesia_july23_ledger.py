#!/usr/bin/env python3
"""July 23 anesthesia claim ledger was not received. Do not invent it."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "archive" / "anesthesia-claim-governance"
LIVE_ROOT = ROOT / "domain_architect"
NS_SND = ROOT / "docs" / "papers" / "ns-snd"
LEDGER_NAME = "CURRENT_CLAIM_LEDGER_JULY23_FULL.md"
FRANKIE_LEDGER = "ns_routej_bridge_recovery/CURRENT_CLAIM_LEDGER.md"
FACE_NAME = "PAPER1_REBUILT_Coherence_Index.md"


class TestJuly23AnesthesiaLedgerWasNotReceived(unittest.TestCase):
    def test_no_invented_ledger_bytes(self):
        invented = [
            ARCHIVE / LEDGER_NAME,
            ROOT / "docs" / "anesthesia" / "claim_governance" / LEDGER_NAME,
            ROOT / "docs" / "papers" / "anesthesia" / LEDGER_NAME,
            NS_SND / LEDGER_NAME,
            LIVE_ROOT / LEDGER_NAME,
        ]
        for path in invented:
            self.assertFalse(path.is_file(), f"do not invent {path}")
        named = list((ROOT / "docs").rglob(LEDGER_NAME))
        self.assertEqual(named, [])
        self.assertFalse((LIVE_ROOT / FACE_NAME).is_file())

    def test_missing_receipt_locks_the_hunt(self):
        receipt = ARCHIVE / "CURRENT_CLAIM_LEDGER_JULY23_FULL.MISSING.md"
        self.assertTrue(receipt.is_file(), receipt)
        text = receipt.read_text(encoding="utf-8")
        self.assertIn("July 23 claim ledger", text)
        self.assertIn("not received", text.lower())
        self.assertIn("Do **not** invent the ledger", text)
        self.assertIn("NOT CLAIMED", text)
        self.assertIn("**Not** NS Clay", text)
        self.assertIn("7de9444d", text)
        self.assertIn("**Not** Ring SND unless arriving text actually", text)
        self.assertIn("PAPER1_REBUILT_Coherence_Index.md", text)
        self.assertIn(FRANKIE_LEDGER, text)
        self.assertIn("Do **not** glue", text)
        self.assertIn("08_publish_queue_2026-08-15/ANESTHESIA/claim_governance", text)
        self.assertIn("HTTP **302**", text)
        self.assertIn("**403**", text)
        self.assertIn("0 bytes", text)
        self.assertIn("69b28657b0df374441f0302e", text)
        self.assertIn("69b2865953e46e195fc302f0", text)
        self.assertIn("unknown", text.lower())
        self.assertIn("Has J in it?", text)
        self.assertIn(r"Ring \(J\)", text)
        self.assertIn("Route J", text)
        self.assertIn("enstrophy", text)
        self.assertIn("import into `domain_architect/`", text)
        self.assertEqual(text.count("Do **not** import into `domain_architect/`"), 1)
        self.assertNotIn("DA-VC-01 PASS", text)
        # Do not invent a SHA of the unread ledger.
        self.assertNotRegex(text, r"(?i)ledger SHA-256:\s*[0-9a-f]{64}")

    def test_readme_and_index_keep_governance_off_the_face(self):
        note = (ARCHIVE / "README.md").read_text(encoding="utf-8")
        index = (ROOT / "docs" / "archive" / "README.md").read_text(encoding="utf-8")
        lookup = (ROOT / "docs" / "packets" / "OLD-PAPERS-LOOK-UP.md").read_text(
            encoding="utf-8"
        )
        policy = (
            ROOT / "docs" / "packets" / "OVERLEAF-VS-PACK-AUDIT-2026-08-15.md"
        ).read_text(encoding="utf-8")
        for text in (note, index, lookup, policy):
            self.assertIn("CURRENT_CLAIM_LEDGER_JULY23_FULL", text)
            self.assertIn("not received", text.lower())
        self.assertIn("anesthesia-claim-governance/", index)
        self.assertIn("governance, not that face", note.lower())
        self.assertIn("PAPER1_REBUILT_Coherence_Index.md", policy)
        self.assertIn("governance, not the ci face", policy.lower())
        self.assertIn(FRANKIE_LEDGER, lookup)
        self.assertIn("CURRENT_CLAIM_LEDGER_JULY23_FULL.MISSING.md", lookup)
        self.assertIn("import into `domain_architect/`", note)

    def test_live_da_does_not_import_the_ledger(self):
        for path in LIVE_ROOT.glob("*.py"):
            hay = path.read_text(encoding="utf-8")
            self.assertNotIn(
                "CURRENT_CLAIM_LEDGER_JULY23",
                hay,
                path.name,
            )
            self.assertNotIn("PAPER1_REBUILT_Coherence_Index", hay, path.name)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
