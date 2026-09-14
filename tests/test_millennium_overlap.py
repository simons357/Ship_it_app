#!/usr/bin/env python3
"""Millennium look: Pólya parts vs Clay prizes; rhymes are not solutions."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.millennium_overlap import overlap_looks, closest_rhymes
from domain_architect.polya_probe import run_polya_probe
from domain_architect.registry import EquationRegistry
from domain_architect.schema import RH_STATUS


ROOT = Path(__file__).resolve().parents[1]


class TestMillenniumLook(unittest.TestCase):
    def test_looks_do_not_unify_or_claim_rh(self):
        looks = {look.look_id: look for look in overlap_looks()}
        self.assertIn("LOOK-NS-GREEN", looks)
        self.assertEqual(looks["LOOK-NS-GREEN"].match_level, "shared-kernel-family")
        self.assertEqual(looks["LOOK-NS-PHI-LETTER"].match_level, "notation-collision")
        self.assertEqual(looks["LOOK-HODGE"].match_level, "none")
        rhymes = " ".join(closest_rhymes()).lower()
        self.assertIn("biot", rhymes)
        self.assertIn("unifies the clay prizes", rhymes)
        self.assertIn("still rh", rhymes)
        probe = run_polya_probe()
        self.assertEqual(probe.rh_status, RH_STATUS)
        ns = next(row for row in probe.millennium_routing if "Navier" in row["prize"])
        self.assertEqual(ns["relation"], "INSUFFICIENT_INFORMATION")
        narrative = probe.narrative().lower()
        self.assertIn("what rhymed when we looked", narrative)
        self.assertNotIn("proves the riemann hypothesis", narrative)
        self.assertTrue(any(c.component_id == "C-NSPhi" for c in probe.components))
        self.assertTrue(any(c.component_id == "C-Rearrange" for c in probe.components))
        registry = EquationRegistry.load_default()
        for eq_id in ("HP-H025", "HP-H027", "NS-H001", "NS-H002", "NS-H003"):
            self.assertIn(eq_id, registry.equations)
        pairs = {(c.left_id, c.right_id, c.relation) for c in registry.conflicts}
        self.assertIn(("HP-H012", "NS-H002", "INCOMPATIBLE"), pairs)
        self.assertIn(("HP-H027", "NS-H001", "COMPATIBLE_DISTINCT"), pairs)

    def test_cli_millennium_look(self):
        proc = subprocess.run(
            [sys.executable, "-m", "domain_architect", "--millennium-look"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("LOOK-NS-GREEN", proc.stdout)
        self.assertIn("Biot", proc.stdout)
        self.assertIn("notation-collision", proc.stdout)
        self.assertIn("not a unification", proc.stdout.lower())
        self.assertNotIn("proves the riemann hypothesis", proc.stdout.lower())


if __name__ == "__main__":
    unittest.main()
