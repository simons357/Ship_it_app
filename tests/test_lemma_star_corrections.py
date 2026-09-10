"""Four Lemma★ corrections: a^4 death, oddness of Tc, aligned 9B limit.

Not a proof. NS is not solved.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.attack9b_exact_shell_K import (  # noqa: E402
    K_of_w,
    build_exact_shell_field,
    choose_closing_sign,
    closing_packet_from_PiB,
    combine_eps,
    field_l2,
    normalize_field,
    project_B_to_shell,
)
from ns_attacks.stokes_moments import (  # noqa: E402
    high_triad_field,
    nonlinear_B,
    probe,
    scale_field,
)


def _false_a4_ratio(r) -> float:
    """|Tc| / (||u||_2 X^{3/2}). Scales as 1/a. Not ★."""
    return abs(r.Tc) / (math.sqrt(r.E) * (r.X ** 1.5))


def _field_inner(a, b) -> complex:
    acc = 0j
    for k, va in a.items():
        vb = b.get(k)
        if vb is None:
            continue
        acc += np.vdot(va, vb)
    return acc


class LemmaStarCorrectionsTests(unittest.TestCase):
    def test_missing_inequality_blows_as_amplitude_vanishes(self):
        v = high_triad_field(amp=1.0)
        r1 = probe(v)
        self.assertGreater(abs(r1.Tc), 1e-12)
        q1 = _false_a4_ratio(r1)
        q_small = _false_a4_ratio(probe(scale_field(v, 1e-3)))
        self.assertGreater(q_small / q1, 100.0)
        # Attack-2 C_* is a different object: amplitude-invariant.
        r_small = probe(scale_field(v, 1e-3))
        self.assertAlmostEqual(r1.ratio_cstar, r_small.ratio_cstar, places=8)
        self.assertAlmostEqual(r1.ratio_box, r_small.ratio_box, places=8)

    def test_Tc_is_odd_Ds_E_Y_even(self):
        v = high_triad_field(amp=1.0, phases=(0.2, -0.4, 0.7))
        r = probe(v)
        rn = probe(scale_field(v, -1.0))
        self.assertGreater(abs(r.Tc), 1e-12)
        self.assertAlmostEqual(rn.Tc, -r.Tc, places=10)
        self.assertAlmostEqual(rn.Ds, r.Ds, places=10)
        self.assertAlmostEqual(rn.E, r.E, places=10)
        self.assertAlmostEqual(rn.Y, r.Y, places=10)
        unsigned = (r.Tc ** 2) / (r.Ds * r.E * r.Y)
        unsigned_n = (rn.Tc ** 2) / (rn.Ds * rn.E * rn.Y)
        self.assertAlmostEqual(unsigned, unsigned_n, places=10)
        if r.Tc > 0:
            self.assertAlmostEqual(r.ratio_box, unsigned, places=10)
            self.assertEqual(rn.ratio_box, 0.0)
        elif r.Tc < 0:
            self.assertEqual(r.ratio_box, 0.0)
            self.assertAlmostEqual(rn.ratio_box, unsigned, places=10)

    def test_aligned_closer_recovers_K_misaligned_does_not(self):
        modes = [(2, 0, 0), (0, 2, 0), (0, 0, 2)]
        amps = np.ones(3)
        thetas = np.array([0.2, 0.7, 1.1])
        phis = np.array([0.1, 0.4, 0.9])
        w = normalize_field(build_exact_shell_field(modes, amps, thetas, phis))
        alpha, beta, eps = 4.0, 8.0, 1e-4
        PiB = project_B_to_shell(nonlinear_B(w), beta)
        self.assertGreater(field_l2(PiB), 1e-12)
        sign = choose_closing_sign(w, PiB)
        z_al = closing_packet_from_PiB(PiB, sign=sign)
        K = K_of_w(w, alpha, beta)["K"]
        r_al = probe(combine_eps(w, z_al, eps))
        self.assertAlmostEqual(r_al.ratio_box / K, 1.0, delta=0.05)

        z_other = normalize_field(
            build_exact_shell_field(
                [(2, 2, 0), (2, 0, 2), (0, 2, 2)],
                np.ones(3),
                np.array([1.3, 0.4, 2.1]),
                np.array([0.8, 1.2, 0.3]),
            )
        )
        inner = _field_inner(PiB, z_other)
        n_pib = field_l2(PiB)
        cos2 = (abs(inner) ** 2) / (n_pib * n_pib)
        self.assertLess(cos2, 0.85)
        r_mis = probe(combine_eps(w, z_other, eps))
        self.assertLess(r_mis.ratio_box, 0.9 * K)

    def test_working_docs_name_the_four_corrections(self):
        canonical = (ROOT / "docs/math/ns_attacks/LEMMA_STAR_CANONICAL.md").read_text()
        formulas = (ROOT / "docs/math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md").read_text()
        status = (ROOT / "docs/five-lane-export/PROOF_LemmaStar_STATUS.md").read_text()
        phone = (ROOT / "docs/LEMMA-STAR-CORRECTIONS.md").read_text()
        self.assertIn("left side scales as", canonical)
        self.assertIn("a^3", canonical)
        self.assertIn("a^4", canonical)
        self.assertIn("no converse", canonical)
        self.assertIn("T_c(-v)", canonical)
        self.assertIn("Section 4", canonical)
        self.assertIn("sign-selected", formulas)
        self.assertIn("DEAD BY SCALING", status)
        self.assertIn("One direction only", status)
        self.assertIn("no converse", phone.lower())
        self.assertIn("not equivalent to it", canonical)
        self.assertIn("NS not solved", canonical)


if __name__ == "__main__":
    unittest.main()
