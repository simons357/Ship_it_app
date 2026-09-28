"""Phase rotation dynamics: 2D3C lock, zeros, transverse kick.

Finite Galerkin only. Not a cutoff-uniform theorem. NS is not solved.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.fourier import cube_modes, dist_to_real_ray, nrm  # noqa: E402
from ns_attacks.galerkin import Field, random_cube, rk4_step, six_mode_cutoff  # noqa: E402
from ns_attacks.phase_network import (  # noqa: E402
    SEED_K,
    SEED_P,
    SEED_Q,
    SEED_SIGMA,
    C_multiplier,
    angular_current,
    monomial,
    signed_radii,
)
from ns_attacks.symmetry_2d3c import (  # noqa: E402
    N_VEC,
    locked_seed,
    off_plane_energy,
    s_residual,
    signed_subspace_energy,
    tracked_W,
)


def _integrate(field: Field, cutoff, nu: float, T: float, dt: float, record_every: int = 1):
    f = field.copy()
    n = int(round(T / dt))
    hist = []
    for i in range(n + 1):
        if i % record_every == 0:
            W = tracked_W(f)
            a, b, c = signed_radii(SEED_K, SEED_P, SEED_Q, SEED_SIGMA)
            # Lambda from current field
            from ns_attacks.galerkin import moments

            Lam = moments(f)["Lambda"]
            C = C_multiplier(a, b, c, Lam)
            ak = f.amplitude(SEED_K, SEED_SIGMA[0], N_VEC)
            ap = f.amplitude(SEED_P, SEED_SIGMA[1], N_VEC)
            aq = f.amplitude(SEED_Q, SEED_SIGMA[2], N_VEC)
            inside, total = signed_subspace_energy(f)
            six = six_mode_cutoff(SEED_K, SEED_P, SEED_Q)
            hist.append(
                {
                    "t": i * dt,
                    "W": W,
                    "abs_W": abs(W),
                    "psi": math.atan2(W.imag, W.real) if abs(W) > 0 else 0.0,
                    "ray_dist": dist_to_real_ray(math.atan2(W.imag, W.real)) if abs(W) > 1e-14 else 0.0,
                    "C": C,
                    "prod": abs(ak * ap * aq),
                    "outside_six": f.energy_outside(six),
                    "leak": 1.0 - (inside / total if total else 1.0),
                    "off_plane": off_plane_energy(f),
                    "S_res": s_residual(f),
                    "J": angular_current(f, SEED_K, SEED_P, SEED_Q, SEED_SIGMA, cutoff, nu, N_VEC)["J_W"],
                }
            )
        if i < n:
            f = rk4_step(f, cutoff, nu, dt)
    return f, hist


class PhaseRotationDynamicsTests(unittest.TestCase):
    def test_six_mode_stays_on_real_rays(self):
        f0 = locked_seed()
        cutoff = six_mode_cutoff(SEED_K, SEED_P, SEED_Q)
        _, hist = _integrate(f0, cutoff, nu=0.05, T=1.0, dt=0.01, record_every=1)
        max_dist = max(h["ray_dist"] for h in hist if h["abs_W"] > 1e-10)
        max_off = max(h["off_plane"] for h in hist)
        max_S = max(h["S_res"] for h in hist)
        self.assertLess(max_dist, 1e-10)
        self.assertLess(max_off, 1e-12)
        self.assertLess(max_S, 1e-10)
        # Tracked signed channel is not an invariant subspace: other helicities grow.
        self.assertGreater(max(h["leak"] for h in hist), 0.1)

    def test_cube_one_preserves_plane_and_real_W(self):
        f0 = locked_seed()
        cutoff = cube_modes(1)
        # Embed seed into the cube (already only six modes).
        _, hist = _integrate(f0, cutoff, nu=0.05, T=0.5, dt=0.01, record_every=1)
        max_dist = max(h["ray_dist"] for h in hist if h["abs_W"] > 1e-10)
        max_off = max(h["off_plane"] for h in hist)
        self.assertLess(max_dist, 1e-9)
        self.assertLess(max_off, 1e-12)
        self.assertGreater(max(h["outside_six"] for h in hist), 0.0)

    def test_modal_or_radial_zero_occurs(self):
        """At least one of: product zero, or C(Λ) zero, on a locked trajectory."""
        f0 = locked_seed(ak=1.0j, ap=1.5j, aq=-0.4j)
        cutoff = six_mode_cutoff(SEED_K, SEED_P, SEED_Q)
        _, hist = _integrate(f0, cutoff, nu=0.02, T=2.0, dt=0.005, record_every=1)
        min_prod = min(h["prod"] for h in hist)
        min_absC = min(abs(h["C"]) for h in hist)
        self.assertTrue(min_prod < 5e-3 or min_absC < 5e-3, msg=f"prod={min_prod} |C|={min_absC}")

    def test_random_cube_rotates(self):
        rng = np.random.default_rng(2)
        f = random_cube(1, rng)
        cutoff = cube_modes(1)
        fT, hist = _integrate(f, cutoff, nu=0.1, T=0.3, dt=0.01, record_every=1)
        max_dist = max(h["ray_dist"] for h in hist)
        max_off = max(h["off_plane"] for h in hist)
        self.assertGreater(max_dist, 0.05)
        self.assertGreater(max_off, 0.05)
        self.assertGreater(max(abs(h["J"]) for h in hist), 0.0)

    def test_transverse_rank_three_generates_rotation(self):
        # Seed planar lock plus a second triad in a different plane, sharing k.
        r = (0, 1, 0)
        s = (-1, -1, 0)
        f = locked_seed(ak=1.0j, ap=0.7j, aq=-1.0j)
        # Add a transverse (++−)-style pair on (k, r, s) with small ε.
        eps = 0.3
        extra = Field().from_amplitudes(
            {
                ((1, 0, 0), 1): 0.0,  # keep existing k
                (r, 1): eps * 1.0j,
                (s, -1): eps * 1.0j,
            },
            reality=True,
        )
        for k, v in extra.u.items():
            f.set(k, f.get(k) + v)
        f.enforce_reality()
        cutoff = list(set(six_mode_cutoff(SEED_K, SEED_P, SEED_Q) + six_mode_cutoff(SEED_K, r, s)))
        _, hist = _integrate(f, cutoff, nu=0.05, T=0.4, dt=0.01, record_every=1)
        max_dist = max(h["ray_dist"] for h in hist)
        max_off = max(h["off_plane"] for h in hist)
        self.assertGreater(max_off, 0.0)
        self.assertGreater(max(abs(h["J"]) for h in hist), 1e-8)
        # Finite rotation: not a uniform escape theorem.
        self.assertGreater(max_dist, 0.0)

    def test_viscous_angular_current_vanishes_without_overlap(self):
        """Single isolated tracked channel: J^W from viscosity is zero (W stays real)."""
        f = locked_seed()
        cutoff = six_mode_cutoff(SEED_K, SEED_P, SEED_Q)
        cur = angular_current(f, SEED_K, SEED_P, SEED_Q, SEED_SIGMA, cutoff, nu=1.0, planar_n=N_VEC)
        self.assertLess(abs(cur["J_W"]), 1e-12)
        self.assertLess(abs(cur["W_im"]), 1e-12)


if __name__ == "__main__":
    unittest.main()
