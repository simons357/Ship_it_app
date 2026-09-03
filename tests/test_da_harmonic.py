"""Typed harmonic vocabulary: catalog yes, unifier no."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_harmonic import VOCAB, claims, run  # noqa: E402


class DaHarmonicTests(unittest.TestCase):
    def test_typed_catalog_not_one_object_or_unifier(self):
        tmp = Path(tempfile.mkdtemp()) / "da_harmonic_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["C1"]["verdict"], "pass")
        self.assertEqual(by["C2"]["verdict"], "pass")
        self.assertEqual(by["C3"]["verdict"], "fail")
        self.assertEqual(by["C4"]["verdict"], "fail")
        self.assertEqual(by["C5"]["verdict"], "fail")
        self.assertEqual(by["C6"]["verdict"], "fail")
        self.assertEqual(by["C7"]["verdict"], "fail")
        self.assertEqual(by["C8"]["verdict"], "fail")
        self.assertEqual(by["C9"]["verdict"], "fail")
        self.assertEqual(by["C10"]["verdict"], "fail")
        self.assertEqual(by["C11"]["verdict"], "fail")
        self.assertGreaterEqual(payload["counts"]["families"], 5)
        self.assertGreaterEqual(payload["counts"]["real_math"], 20)
        self.assertGreaterEqual(payload["counts"]["false_friends"], 3)
        self.assertTrue(payload["meta"]["not_a_unifier"])
        self.assertTrue(payload["meta"]["does_not_retune_nodes"])

    def test_desk_uses_are_typed_and_names_unique(self):
        names = [r["name"] for r in VOCAB]
        ids = [r["id"] for r in VOCAB]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(ids), len(set(ids)))
        by = {r["name"]: r for r in VOCAB}
        self.assertEqual(by["littlewood_paley"]["slot"], "B")
        self.assertEqual(by["bony_paraproduct"]["slot"], "B")
        self.assertEqual(by["tube_hardy"]["slot"], "B")
        self.assertEqual(by["spherical_harmonic"]["slot"], "B")
        self.assertEqual(by["fourier_character"]["slot"], "A")
        self.assertEqual(by["helmholtz_leray"]["slot"], "A")
        self.assertEqual(by["dirichlet_character"]["slot"], "Q")
        self.assertEqual(by["cosmo_oscillator_knobs"]["slot"], "U")
        self.assertFalse(by["cosmo_oscillator_knobs"]["real_math"])
        self.assertFalse(by["hb_nodes"]["real_math"])
        self.assertFalse(by["sfe_F"]["real_math"])
        self.assertNotEqual(by["hardy_space"]["slot"], by["tube_hardy"]["slot"])
        self.assertEqual(len(claims()), 11)
        self.assertTrue(by["littlewood_paley"]["on_desk"])
        self.assertFalse(by["hb_nodes"]["on_desk"])


if __name__ == "__main__":
    unittest.main()
