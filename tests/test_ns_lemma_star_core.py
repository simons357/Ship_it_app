"""Independent Lemma★ core vs boxed identities and live probe().

Not a proof. NS is not solved. Live stokes_moments.py is not replaced.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.ns_lemma_star_core import (  # noqa: E402
    D_s_direct_form,
    D_s_double_sum,
    D_s_moment_form,
    Field,
    K_of_w,
    R_star,
    build_closing_direction,
    dilate,
    from_mode_dict,
    moments,
    random_shell_field,
    shell_wavevectors,
    sum_Tk,
    to_mode_dict,
)
from ns_attacks.stokes_moments import (  # noqa: E402
    Ds_two_shell,
    high_triad_field,
    probe,
    random_field,
    three_shell_field,
)


CORE = ROOT / "scripts" / "ns_attacks" / "ns_lemma_star_core.py"
LIVE = ROOT / "scripts" / "ns_attacks" / "stokes_moments.py"
PHONE = ROOT / "docs" / "LEMMA-STAR-CORE.md"


def _assert_divfree_reality(field: Field, places: int = 10) -> None:
    for k, vk in field.modes.items():
        kdot = np.dot(np.array(k, dtype=float), vk)
        if abs(kdot) > 10 ** (-places):
            raise AssertionError(f"not div-free at {k}: k·v={kdot}")
        nk = tuple(-x for x in k)
        if nk not in field.modes:
            raise AssertionError(f"missing conjugate partner of {k}")
        err = np.linalg.norm(field.modes[nk] - np.conj(vk))
        if err > 10 ** (-places):
            raise AssertionError(f"reality broken at {k}: {err}")


class LemmaStarCoreTests(unittest.TestCase):
    def test_phone_and_live_stokes_not_replaced(self):
        self.assertTrue(CORE.is_file())
        self.assertTrue(PHONE.is_file())
        phone = PHONE.read_text()
        self.assertIn("ns_lemma_star_core.py", phone)
        self.assertIn("not overwritten", phone)
        self.assertIn("NS not solved", phone)
        live = LIVE.read_text()
        self.assertIn("def hh_l_sphere_pairs", live)
        self.assertNotIn("class Field:", live)

    def test_shell_wavevectors_match_exhaustive(self):
        for n in range(1, 50):
            got = set(shell_wavevectors(n, canonical_only=False))
            brute = {
                (a, b, c)
                for a in range(-8, 9)
                for b in range(-8, 9)
                for c in range(-8, 9)
                if a * a + b * b + c * c == n
            }
            self.assertEqual(got, brute, msg=n)

    def test_Ds_three_forms_and_two_shell_closed(self):
        rng = np.random.default_rng(7)
        w = random_shell_field(4, rng)
        z, raw = build_closing_direction(w, 8)
        self.assertIsNotNone(z)
        v = w.add(z.scale(0.15))
        E, X, Y, Z, Lambda = moments(v)
        dm = D_s_moment_form(X, Y, Z)
        dd = D_s_direct_form(v, Lambda)
        ds = D_s_double_sum(v, X)
        self.assertAlmostEqual(dm, dd, places=10)
        self.assertAlmostEqual(dm, ds, places=8)
        shells = {}
        for k, vk in v.modes.items():
            lamk = k[0] * k[0] + k[1] * k[1] + k[2] * k[2]
            shells[lamk] = shells.get(lamk, 0.0) + float(np.vdot(vk, vk).real)
        self.assertEqual(len(shells), 2)
        (a, ea), (b, eb) = list(shells.items())
        closed = Ds_two_shell(a, b, ea, eb)
        self.assertAlmostEqual(dm, closed, places=10)

    def test_Ds_mismatch_raises(self):
        v = from_mode_dict(high_triad_field(amp=1.0))
        E, X, Y, Z, Lambda = moments(v)
        self.assertGreater(D_s_moment_form(X, Y, Z), 1e-8)

        def boom(*_a, **_k):
            return 123.456

        import ns_attacks.ns_lemma_star_core as core

        old = core.D_s_direct_form
        core.D_s_direct_form = boom
        try:
            with self.assertRaises(RuntimeError) as ctx:
                core.R_star(v, verify=True, tol=1e-8)
            self.assertIn("D_s cross-check FAILED", str(ctx.exception))
        finally:
            core.D_s_direct_form = old

    def test_matches_live_probe_on_triad_and_random(self):
        fields = [
            high_triad_field(amp=1.2, phases=(0.2, -0.4, 0.7)),
            three_shell_field((1, 0, 0), (0, 1, 0)),
            random_field(np.random.default_rng(13), kmax=4, n_modes=10, amp=1.0),
        ]
        for d in fields:
            live = probe(d)
            core = R_star(from_mode_dict(d))
            self.assertAlmostEqual(core["E"], live.E, places=10)
            self.assertAlmostEqual(core["X"], live.X, places=10)
            self.assertAlmostEqual(core["Y"], live.Y, places=10)
            self.assertAlmostEqual(core["D_s"], live.Ds, places=9)
            self.assertAlmostEqual(core["T_c"], live.Tc, places=9)
            if live.Ds > 1e-12 and live.Tc >= 0:
                self.assertAlmostEqual(core["R_star"], live.ratio_box, places=9)
            elif live.Tc < 0:
                self.assertEqual(core["R_star"], 0.0)
                self.assertEqual(live.ratio_box, 0.0)

    def test_R_star_amplitude_and_dilation_invariance(self):
        v = from_mode_dict(high_triad_field(amp=1.0))
        r1 = R_star(v)
        self.assertFalse(r1["vacuous_single_shell"])
        self.assertGreater(r1["R_star"] + abs(r1["T_c"]), 0.0)
        for a in (0.2, 3.0, 11.0, 1e-2):
            r2 = R_star(v.scale(a))
            self.assertAlmostEqual(r1["R_star"], r2["R_star"], places=9)
            self.assertAlmostEqual(r1["Lambda"], r2["Lambda"], places=10)
        for n in (2, 3):
            r3 = R_star(dilate(v, n))
            self.assertAlmostEqual(r1["R_star"], r3["R_star"], places=8)

    def test_Tc_odd_Ds_E_Y_even_and_reverse_orientation(self):
        v = from_mode_dict(high_triad_field(amp=1.0, phases=(0.2, -0.4, 0.7)))
        r = R_star(v)
        rn = R_star(v.scale(-1.0))
        self.assertGreater(abs(r["T_c"]), 1e-12)
        self.assertAlmostEqual(rn["T_c"], -r["T_c"], places=10)
        self.assertAlmostEqual(rn["D_s"], r["D_s"], places=10)
        self.assertAlmostEqual(rn["E"], r["E"], places=10)
        self.assertAlmostEqual(rn["Y"], r["Y"], places=10)
        unsigned = (r["T_c"] ** 2) / (r["D_s"] * r["E"] * r["Y"])
        if r["T_c"] > 0:
            self.assertAlmostEqual(r["R_star"], unsigned, places=10)
            self.assertEqual(rn["R_star"], 0.0)
        else:
            self.assertEqual(r["R_star"], 0.0)
            self.assertAlmostEqual(rn["R_star"], unsigned, places=10)

    def test_complex_scale_rejected(self):
        v = from_mode_dict(high_triad_field(amp=1.0))
        with self.assertRaises(ValueError):
            v.scale(1j)

    def test_divfree_reality_energy_identity(self):
        v = from_mode_dict(high_triad_field(amp=1.3, phases=(0.1, -0.4, 0.8)))
        _assert_divfree_reality(v)
        self.assertLess(abs(sum_Tk(v)), 1e-10)
        roundtrip = from_mode_dict(to_mode_dict(v))
        r1 = R_star(v)
        r2 = R_star(roundtrip)
        self.assertAlmostEqual(r1["R_star"], r2["R_star"], places=12)

    def test_single_shell_vacuous(self):
        w = random_shell_field(5, np.random.default_rng(3))
        r = R_star(w)
        self.assertTrue(r["vacuous_single_shell"])
        self.assertLess(abs(r["D_s"]), 1e-12)
        self.assertLess(abs(r["T_c"]), 1e-10)
        self.assertEqual(r["R_star"], 0.0)

    def test_aligned_closer_recovers_K_misaligned_does_not(self):
        rng = np.random.default_rng(21)
        w = random_shell_field(4, rng)
        z, raw = build_closing_direction(w, 8)
        self.assertIsNotNone(z)
        self.assertGreater(raw, 1e-12)
        info = K_of_w(w, 4.0, 8.0)
        K = info["K"]
        self.assertTrue(math.isfinite(K))
        self.assertGreater(K, 0.0)
        eps = 1e-4
        rp = R_star(w.add(z.scale(eps)))
        rm = R_star(w.add(z.scale(-eps)))
        aligned = max(rp["R_star"], rm["R_star"])
        self.assertLess(abs(aligned - K) / max(K, 1e-12), 5e-3)
        # Misaligned: unit z on shell 8 orthogonal to Π_8 B. Limit is the
        # squared projection, not K.
        z_rand = random_shell_field(8, rng)
        ip = 0j
        for k, vk in z.modes.items():
            ip += np.vdot(vk, z_rand.get(k))
        z_mis = Field()
        for k in set(z.support()) | set(z_rand.support()):
            z_mis.modes[k] = z_rand.get(k) - ip * z.get(k)
        self.assertGreater(z_mis.energy(), 1e-16)
        z_mis = z_mis.normalize(1.0)
        r_mis = R_star(w.add(z_mis.scale(eps)))
        r_mis_n = R_star(w.add(z_mis.scale(-eps)))
        mis = max(r_mis["R_star"], r_mis_n["R_star"])
        self.assertLess(mis, 0.05 * K + 1e-12)


if __name__ == "__main__":
    unittest.main()
