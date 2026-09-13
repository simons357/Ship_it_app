#!/usr/bin/env python3
"""SND leftover and the several '6's stay labeled and un-glued."""

from __future__ import annotations

import unittest
from pathlib import Path

from domain_architect.leftover_repair import leftover_repair
from domain_architect.open_board import open_board


ROOT = Path(__file__).resolve().parents[1]
CARD = ROOT / "docs" / "domain-architect" / "SND-AND-SIX.md"
OPEN_BOARD = ROOT / "docs" / "domain-architect" / "OPEN-BOARD.md"
LEFTOVER = ROOT / "docs" / "domain-architect" / "LEFTOVER-REPAIR.md"
CHAIN = ROOT / "docs" / "papers" / "ns-snd" / "NS_UNAUGMENTED_PROOF_CHAIN.md"
ESTIMATE = ROOT / "docs" / "papers" / "swirl" / "AXISYMMETRIC-SHELL-ESTIMATE.md"
NS_FACES = ROOT / "docs" / "papers" / "ns-snd" / "FACES.md"

FORBIDDEN_GLUE = (
    "snd leftover = t_{j",
    "t_{j\\leftarrow j} = write (6)",
    "write (6) = step 6 = q6",
    "identity controls transfer",
    "clay is solved",
)


class TestSndAndSixLabels(unittest.TestCase):
    def test_inventory_card_exists_and_unmixes(self):
        text = CARD.read_text(encoding="utf-8")
        self.assertIn("parked until Monday", text)
        self.assertIn("NOT CLAIMED", text)
        self.assertIn("CONDITIONAL", text)
        self.assertIn("steps **7–8**", text)
        self.assertIn("WRITE (6) / H1", text)
        self.assertIn("proposed closure **IF (A)**", text)
        self.assertIn("Does not exist", text)
        self.assertIn("DISCARD", text)
        self.assertIn("Do not glue", text)
        lowered = text.lower()
        for phrase in FORBIDDEN_GLUE:
            self.assertNotIn(phrase, lowered)

    def test_leftover_split_stays_three_and_open(self):
        payload = leftover_repair()
        self.assertEqual(len(payload["pieces"]), 3)
        self.assertFalse(payload["reconstruction"]["closed"])
        self.assertEqual(payload["reconstruction"]["honest_close"], "CONDITIONAL")
        self.assertTrue(all(p["status"] == "CONDITIONAL" for p in payload["pieces"]))
        refused = " ".join(payload["refused"]).lower()
        self.assertIn("no leftover-split item #6", refused)
        self.assertIn("write (6)", refused)

    def test_open_board_keeps_real_leftovers_open(self):
        payload = open_board()
        still = [row["id"] for row in payload["still_open"]]
        self.assertEqual(
            still, ["gap1-step-f", "route-j", "ns-open", "axisymmetric-shell"]
        )
        cond = [row["id"] for row in payload["conditional"]]
        self.assertEqual(cond, ["swirl-strain", "ring-snd", "paper2-simplex"])
        park = [row["id"] for row in payload["parked"]]
        self.assertEqual(park, ["estimate-step-6", "write-6-h1"])
        shell = next(
            row for row in payload["still_open"] if row["id"] == "axisymmetric-shell"
        )
        self.assertEqual(shell["bucket"], "STILL_OPEN")
        self.assertIn("Not SND leftover", shell["problem"])
        self.assertIn("Not WRITE (6)", shell["problem"])

    def test_docs_do_not_claim_t2_or_generic_3d(self):
        board = OPEN_BOARD.read_text(encoding="utf-8")
        leftover = LEFTOVER.read_text(encoding="utf-8")
        chain = CHAIN.read_text(encoding="utf-8")
        estimate = ESTIMATE.read_text(encoding="utf-8")
        faces = NS_FACES.read_text(encoding="utf-8")
        self.assertIn("no leftover-split item #6", board.lower())
        self.assertIn("SND-AND-SIX.md", leftover)
        self.assertIn("7–8", chain)
        self.assertIn("Not Clay", chain)
        self.assertIn("not claimed", estimate.lower())
        self.assertIn("WRITE (6) / H1", estimate)
        self.assertIn("13 Sept 2026 label", faces)
        self.assertIn("**not** generic 3-D", faces)
        self.assertIn("Not “SND implies generic 3-D.”", CARD.read_text(encoding="utf-8"))
        self.assertNotIn("identity controls transfer", estimate.lower())


if __name__ == "__main__":
    raise SystemExit(unittest.main())
