#!/usr/bin/env python3
"""Jigsaw: pieces, constraint assembler, building not hill."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.jigsaw import (
    assemble_pieces,
    format_jigsaw,
    jigsaw_report,
)
from domain_architect.think_tank import consult
from domain_architect.visual import DEFAULT_STATE, svg_jigsaw


ROOT = Path(__file__).resolve().parents[1]


class TestJigsaw(unittest.TestCase):
    def test_building_not_hill(self):
        data = jigsaw_report("B")
        self.assertEqual(data["building"]["verdict"], "BUILDING")
        self.assertEqual(data["building"]["not"], "HILL")
        self.assertTrue(data["building"]["certain"])
        self.assertFalse(data["building"]["finest_detail"])
        self.assertFalse(data["smooth"])
        self.assertFalse(data["complete"])
        text = format_jigsaw(data).lower()
        self.assertNotIn("clay", text)
        self.assertIn("building", text)
        self.assertIn("not hill", text)

    def test_order_two_is_not_identity(self):
        data = jigsaw_report("B")
        by_id = {h["clip_id"]: h for h in data["holes"]}
        occ = by_id["CLIP-B2-OCCUPATION"]
        self.assertEqual(occ["order"], 2)
        self.assertFalse(occ["identity_relevant"])
        self.assertFalse(occ["walk_relevant"])
        self.assertEqual(occ["role"], "damage")

    def test_weld_is_parthenon_walk(self):
        data = jigsaw_report("B")
        weld = next(h for h in data["holes"] if h["clip_id"] == "CLIP-T3-WELD")
        self.assertEqual(weld["order"], 1)
        self.assertFalse(weld["identity_relevant"])
        self.assertTrue(weld["walk_relevant"])
        self.assertEqual(weld["role"], "parthenon")
        phi = next(h for h in data["holes"] if h["clip_id"] == "CLIP-PHI-LINFTY")
        self.assertEqual(phi["role"], "rubble")
        self.assertFalse(phi["identity_relevant"])

    def test_assembler_is_constraints_not_a_net(self):
        data = jigsaw_report("B")
        asm = data["assembly"]
        self.assertEqual(asm["kind"], "constraint")
        self.assertFalse(asm["cross_book_snap"])
        self.assertIn("neural net", asm["not"])
        self.assertGreaterEqual(len(asm["snapped"]), 8)
        self.assertIn("L12-ENERGY", data["energy_path"])
        self.assertIn("L8-ANGULAR", data["energy_path"])

    def test_q_is_wrong_object_on_b(self):
        b = jigsaw_report("B")
        q = jigsaw_report("Q")
        self.assertEqual(q["book"], "Q")
        self.assertEqual(q["foreign"]["snap"], "WRONG_OBJECT")
        self.assertEqual(b["foreign"]["snap"], "WRONG_OBJECT")
        self.assertNotEqual(b["building"]["catalog"], q["building"]["catalog"])
        mixed = assemble_pieces(b["pieces"] + q["pieces"])
        self.assertFalse(mixed["cross_book_snap"])
        for fit in mixed["fits"]:
            ids = set(fit["pieces"])
            self.assertFalse({"Q6", "L1-TORUS"} <= ids)

    def test_think_tank_does_not_weld(self):
        tank = consult("jigsaw")
        self.assertEqual(tank["topic"], "jigsaw")
        self.assertEqual(tank["fills_found"], 0)
        names = {row["name"] for row in tank["notes"]}
        self.assertIn("Edsger Dijkstra", names)
        self.assertIn("Caffarelli–Kohn–Nirenberg", names)
        self.assertTrue(all(n["fills_gap"] == "no" for n in tank["notes"]))

    def test_svg_is_literal_pieces(self):
        svg = svg_jigsaw()
        self.assertIn("<path", svg)
        self.assertIn("BUILDING", svg)
        self.assertIn("not a hill", svg)
        self.assertIn("GAP-T3", svg)
        self.assertNotIn("clay", svg.lower())

    def test_cli_follows_see(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--jigsaw", "B", "--json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["building"]["verdict"], "BUILDING")
        self.assertEqual(payload["assembly"]["kind"], "constraint")
        state = json.loads((ROOT / DEFAULT_STATE).read_text(encoding="utf-8"))
        self.assertEqual(state["action"], "jigsaw")


if __name__ == "__main__":
    unittest.main()
