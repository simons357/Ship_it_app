#!/usr/bin/env python3
"""Clip-splice: ID and measure remainders instead of silent-merge."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from domain_architect.clip_splice import clip_splice


ROOT = Path(__file__).resolve().parents[1]

NS = "partial_t u + (u * nabla) * u = - nabla p + nu * laplacian u"
NS_Q1 = "partial_t u + (u * nabla) * u = - nabla p + nu * laplacian u + epsilon * div(f)"
POISSON = "laplacian Phi = 4 * pi * G * rho"
POISSON_L = "laplacian Phi = 4 * pi * G * rho + Lambda * Phi"


class TestClipSplice(unittest.TestCase):
    def test_identical_has_no_clip(self):
        result = clip_splice(POISSON, POISSON)
        self.assertEqual(result.alignment, "IDENTICAL")
        self.assertEqual(result.left_clips, [])
        self.assertEqual(result.right_clips, [])
        self.assertFalse(result.silent_merge)
        self.assertTrue(result.cores_made_same)

    def test_poisson_lambda_clip_is_id_and_kept(self):
        result = clip_splice(POISSON, POISSON_L)
        self.assertEqual(result.alignment, "CLIPPED")
        self.assertTrue(result.cores_made_same)
        self.assertFalse(result.silent_merge)
        self.assertEqual(result.left_clips, [])
        self.assertEqual(len(result.right_clips), 1)
        clip = result.right_clips[0]
        self.assertTrue(clip.clip_id.startswith("CLIP-"))
        self.assertFalse(clip.discarded)
        self.assertEqual(clip.kind, "EXTENSION_ROLE")
        self.assertTrue(clip.independently_specifiable)
        self.assertIn("Lambda", clip.symbols)
        self.assertIn("=", result.shared_core)

    def test_q1_term_is_a_named_dynamics_clip(self):
        result = clip_splice(NS, NS_Q1)
        self.assertEqual(result.alignment, "CLIPPED")
        self.assertFalse(result.silent_merge)
        self.assertEqual(len(result.right_clips), 1)
        clip = result.right_clips[0]
        self.assertEqual(clip.kind, "DYNAMICS_TERM")
        self.assertTrue(clip.independently_specifiable)
        self.assertFalse(clip.discarded)
        self.assertIn("epsilon", clip.symbols)
        self.assertTrue(result.weld_lemma_required)
        self.assertNotIn("A⇒B", result.message)  # message talks about not making originals the same

    def test_no_shared_terms_refuses_fake_identity(self):
        result = clip_splice("x = 1", "laplacian Phi = 4 * pi * G * rho")
        self.assertIn(result.alignment, {"INCOMPATIBLE", "PARTIAL"})
        self.assertFalse(result.cores_made_same)

    def test_cli_clip(self):
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "domain_architect",
                "--clip",
                POISSON,
                POISSON_L,
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("CLIP-", proc.stdout)
        self.assertIn("discarded=False", proc.stdout)
        self.assertIn("Silent merge: no", proc.stdout)


if __name__ == "__main__":
    unittest.main()
