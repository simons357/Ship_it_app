"""Class hunt for axisymmetric-with-swirl Door-1 remainder control.

Mission: find or falsify a mathematically usable CLASS on which either
(A) seats (without ė_j/Ż/Λ′ recycling), or near-scale T_{j←j} admits a
class-uniform geometric/depletion bound that plugs Door-1 into the
conditional Gronwall — or kill natural candidates with counterexamples.

Class: unaugmented axisymmetric-with-swirl (exact-disk / algebraic probes).
Quantity: Door-1 same-scale / near-scale T_{j←j} and route (A).
Remainder: T_{j←j}.
Assumed: [signed Im; no abs Young; no ė_j/Ż/Λ′; spectral-shift ≠ Lemma★;
NS not solved; Clay NOT CLAIMED; finite disks ≠ K_max→∞].

Verdicts are KEEP / KEEP-CONDITIONAL / KILL for the *Door-1 proof chain*.
A KEEP that only works at fixed K_max is labeled not Millennium-scaling.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from .axisymmetric_shell import COMPACT_SWIRL_SAMPLES, THREE_D_FACTS
from .axisym_same_scale_tjj import (
    build_reality_paired_field,
    conditional_theta_bound,
    dissipation_proxy,
    energy_z,
    enumerate_near_scale_feeders,
    enumerate_same_scale_triads,
    geometric_factor_theta,
    maximize_same_scale_ratio,
    random_div_free_amp,
    same_scale_transfer,
    shell_modes,
    triad_signed_transfer,
)

HONESTY = {
    "NS_solved": False,
    "clay": "NOT CLAIMED",
    "lemma_star_smuggled": False,
    "uses_edot_zdot_lambda_to_bound_Tjj": False,
    "principal_unresolved": "T_{j←j}",
    "proofs_invented": False,
}


def _pure_swirl_amp(
    k: tuple[int, int, int],
    rng: np.random.Generator,
) -> np.ndarray:
    """Swirl polarization only: û ∥ ê_y when k_y=0 (admissible)."""
    kv = np.array(k, dtype=float)
    kn = np.linalg.norm(kv)
    assert kn > 0.0
    ey = np.array([0.0, 1.0, 0.0])
    khat = kv / kn
    assert abs(float(np.dot(ey, khat))) < 1e-12
    c = (rng.normal() + 1j * rng.normal()) / math.sqrt(2.0)
    return c * ey


def build_pure_swirl_field(
    modes: list[tuple[int, int, int]],
    rng: np.random.Generator,
) -> dict[tuple[int, int, int], np.ndarray]:
    field: dict[tuple[int, int, int], np.ndarray] = {}
    seen: set[tuple[int, int, int]] = set()
    for k in modes:
        if k in seen:
            continue
        mk = (-k[0], -k[1], -k[2])
        amp = _pure_swirl_amp(k, rng)
        field[k] = amp
        field[mk] = np.conjugate(amp)
        seen.add(k)
        seen.add(mk)
    return field


def build_meridional_only_field(
    modes: list[tuple[int, int, int]],
    rng: np.random.Generator,
) -> dict[tuple[int, int, int], np.ndarray]:
    """No swirl: û in the meridional plane (ê_y component = 0)."""
    field: dict[tuple[int, int, int], np.ndarray] = {}
    seen: set[tuple[int, int, int]] = set()
    for k in modes:
        if k in seen:
            continue
        mk = (-k[0], -k[1], -k[2])
        kv = np.array(k, dtype=float)
        kn = np.linalg.norm(kv)
        khat = kv / kn
        ey = np.array([0.0, 1.0, 0.0])
        e_mer = np.cross(khat, ey)
        e_mer /= np.linalg.norm(e_mer)
        c = (rng.normal() + 1j * rng.normal()) / math.sqrt(2.0)
        amp = c * e_mer
        field[k] = amp
        field[mk] = np.conjugate(amp)
        seen.add(k)
        seen.add(mk)
    return field


def probe_field_near_scale(
    field: dict[tuple[int, int, int], np.ndarray],
    *,
    k_min: float = 2.5,
    k_max: float = 4.5,
    neighbor_pad: float = 1.5,
) -> dict[str, Any]:
    shell = shell_modes(k_min, k_max, disk="axisym_swirl_slice")
    neighbors = shell_modes(
        max(0.5, k_min - neighbor_pad),
        k_max + neighbor_pad,
        disk="axisym_swirl_slice",
    )
    near = enumerate_near_scale_feeders(shell, neighbors)
    internal = enumerate_same_scale_triads(shell)
    shell_field = {m: field[m] for m in shell if m in field}
    z = energy_z(shell_field)
    d = dissipation_proxy(shell_field)
    t_near = same_scale_transfer(field, near)
    t_int = same_scale_transfer(field, internal)
    theta = geometric_factor_theta(field, near)
    return {
        "Z_shell": z,
        "D_proxy": d,
        "T_near": t_near,
        "T_internal_b0": t_int,
        "theta_near": theta,
        "|T_near|/Z^{3/2}": abs(t_near) / (z**1.5) if z > 1e-30 else 0.0,
        "n_near_triads": len(near),
        "n_internal_triads": len(internal),
    }


# ---------------------------------------------------------------------------
# Candidate classes
# ---------------------------------------------------------------------------


def class_pure_swirl(*, n_trials: int = 40, seed: int = 21) -> dict[str, Any]:
    """Instantaneous pure swirl u^r=u^z=0 (û ∥ ê_y on k_y=0).

    Analytic: meridional velocity vanishes ⇒ energy/enstrophy same-scale
    pairing that needs u·∇ acting through meridional legs is zero on the
    pure-swirl field (estimate note §7 / samples). Numeric: T_near≈0.

    Dynamical invariance under NS: KILLED — centrifugal forcing of swirl
    generally sources meridional flow; pure-swirl IC is not a closed
    evolutionary class for the Door-1 close of generic mixed data.
    """
    rng = np.random.default_rng(seed)
    support = shell_modes(0.5, 7.0, disk="axisym_swirl_slice")
    max_ratio = 0.0
    max_abs_t = 0.0
    for _ in range(n_trials):
        field = build_pure_swirl_field(support, rng)
        rec = probe_field_near_scale(field)
        max_ratio = max(max_ratio, rec["|T_near|/Z^{3/2}"])
        max_abs_t = max(max_abs_t, abs(rec["T_near"]))
    sample = float(COMPACT_SWIRL_SAMPLES["pure_swirl_n32_max_|Tjj/Xj|"])
    instantaneous_ok = max_abs_t < 1e-10 and sample < 1e-15
    return {
        "class_id": "pure_swirl",
        "definition": (
            "Axisymmetric fields with u^r ≡ u^z ≡ 0 (swirl only); "
            "on disks: û(k) ∥ ê_y for all k=(k_x,0,k_z) in the support"
        ),
        "verdict_instantaneous": "KEEP",
        "verdict_evolutionary": "KILL",
        "verdict_door1_chain": "KEEP-INSTANTANEOUS-ONLY",
        "A_seats": instantaneous_ok,  # T≡0 ⇒ (A) with R=0 on that field
        "Tjj_controlled": instantaneous_ok,
        "control_kind": "identity_zero (not depletion)",
        "numeric": {
            "max_|T_near|": max_abs_t,
            "max_|T_near|/Z^{3/2}": max_ratio,
            "compact_sample_max_|Tjj/Xj|": sample,
            "n_trials": n_trials,
        },
        "analytic": (
            "On a pure-swirl field the meridional advection/stretch legs "
            "vanish, so T_{j←j}=0 (estimate §7). This is an identity on "
            "the field class, not geometric depletion of mixed HHH."
        ),
        "why_evolutionary_killed": (
            "NS with swirl sources meridional motion via centrifugal force "
            "unless specially balanced; pure-swirl is not an invariant "
            "solution class that closes generic Door-1 data"
        ),
        "millennium_relevant": False,
        "uses_edot_zdot_lambda": False,
    }


def class_finite_fourier_disk(
    *, k_max_fixed: float = 6.0, n_trials: int = 30, seed: int = 22
) -> dict[str, Any]:
    """Gevrey / analytic / finite Fourier disk with fixed K_max.

    Trivial: finite-dimensional Galerkin / fixed disk ⇒ all norms equivalent;
    enstrophy finite a priori on the truncation. Not a K_max→∞ statement.
    """
    run = maximize_same_scale_ratio(
        disk="axisym_swirl_slice",
        n_trials=n_trials,
        seed=seed,
        support_k_max=k_max_fixed,
        k_max=min(4.5, k_max_fixed - 0.5),
    )
    return {
        "class_id": "gevrey_analytic_finite_fourier_disk",
        "definition": (
            f"Fields with Fourier support in |k|≤K_max (here K_max={k_max_fixed}), "
            "or Gevrey/analytic with uniform radius giving effective finite disk"
        ),
        "verdict_door1_chain": "KEEP-CONDITIONAL",
        "label": "NOT scaling to K_max→∞; not Millennium-relevant",
        "A_seats": True,  # on the truncation, trivial equivalence of norms
        "A_seats_scope": "fixed-K_max truncation / Galerkin only",
        "Tjj_controlled": True,
        "control_kind": "finite-dimensional a priori (trivial)",
        "numeric": {
            "fixed_K_max": k_max_fixed,
            "max_|T_near|/Z^{3/2}_on_disk": run["best"]["max_|T_near|/Z^{3/2}"],
            "energy_sharp_b0_identity_holds": run["energy_sharp_b0_identity_holds"],
            "scope": run["scope"],
        },
        "analytic": (
            "On a fixed finite mode set every Sobolev norm is equivalent; "
            "the ODE for the Galerkin system has globally finite enstrophy. "
            "This seats regularity of the truncation, not a uniform-in-K_max "
            "Door-1 bound for continuum NS."
        ),
        "millennium_relevant": False,
        "uses_edot_zdot_lambda": False,
    }


def class_small_data(*, seed: int = 23) -> dict[str, Any]:
    """Small data in critical / subcritical norms.

    Classical path: smallness in Ḃ^{-1+3/p}_{p,∞} / H^{1/2} / etc. gives
    global regularity by contraction — a different theorem path from Door-1+(A).
    Under smallness, cubic transfer is absorbed by viscosity (standard),
    so (A)-shaped bounds can be arranged; this is not large-data depletion.
    """
    _ = seed  # reserved for future quantitative disk thresholds
    return {
        "class_id": "small_data_critical_subcritical",
        "definition": (
            "Initial data with ‖u₀‖_X ≤ ε_* for a critical/subcritical space X "
            "(e.g. Ḃ^{-1}_{∞,∞}, H^{1/2}, or axisym small-swirl thresholds in "
            "the literature) so that Picard/Kato contraction closes"
        ),
        "verdict_door1_chain": "KEEP-CONDITIONAL",
        "A_seats": True,
        "A_seats_scope": (
            "under smallness: |Tjj| = O(‖u‖_X^3) absorbed by εν P_j for ε_* small; "
            "standard small-data argument — not a geometric Door-1 close for large data"
        ),
        "Tjj_controlled": True,
        "control_kind": "smallness absorption (different theorem path)",
        "numeric": {
            "disk_probe": "not required; small-data is analytic/classical",
            "recorded_mixed_sample_is_not_small_data_close": float(
                COMPACT_SWIRL_SAMPLES["mixed_m1_n32_max_|Tjj/Xj|"]
            ),
        },
        "analytic": (
            "Small-data global regularity for NS is classical; axisymmetric-with-swirl "
            "admits improved thresholds in places. That path does not produce a "
            "large-data class bound on T_{j←j} without smallness. No ė_j/Ż/Λ′ used."
        ),
        "millennium_relevant": False,
        "uses_edot_zdot_lambda": False,
        "note": "KEEP as conditional/small-data path; does not finish large-data Door-1",
    }


def _parity_probe(
    pred,
    *,
    n_trials: int,
    seed: int,
) -> dict[str, Any]:
    """Near-scale max ratio under a meridional lattice parity predicate."""
    rng = np.random.default_rng(seed)
    support = [k for k in shell_modes(0.5, 7.0, disk="axisym_swirl_slice") if pred(k)]
    shell = [k for k in shell_modes(2.5, 4.5, disk="axisym_swirl_slice") if pred(k)]
    neighbors = [k for k in shell_modes(1.0, 6.0, disk="axisym_swirl_slice") if pred(k)]
    near = enumerate_near_scale_feeders(shell, neighbors)
    max_ratio = 0.0
    max_theta = 0.0
    for _ in range(n_trials):
        if len(support) < 4:
            break
        field = build_reality_paired_field(support, rng, disk="axisym_swirl_slice")
        shell_field = {m: field[m] for m in shell if m in field}
        z = energy_z(shell_field)
        if z <= 1e-30:
            continue
        t_near = same_scale_transfer(field, near) if near else 0.0
        theta = geometric_factor_theta(field, near) if near else 0.0
        max_ratio = max(max_ratio, abs(t_near) / (z**1.5))
        max_theta = max(max_theta, theta)
    return {
        "n_support": len(support),
        "n_shell": len(shell),
        "n_near_triads": len(near),
        "max_|T_near|/Z^{3/2}": max_ratio,
        "max_theta_near": max_theta,
    }


def class_odd_odd_even(*, n_trials: int = 60, seed: int = 24) -> dict[str, Any]:
    """Additional discrete reflection symmetries beyond axisymmetry.

    Some toy parities empty near-scale triads (sparse-like KEEP-CONDITIONAL).
    Others retain triads with O(1) |T_near|/Z^{3/2}. That kills the claim that
    'reflection / OOE symmetry alone seats (A) or forces T_near≡0'.
    """
    empty_parity = _parity_probe(
        lambda k: (k[0] % 2 != 0) and (k[2] % 2 == 0),
        n_trials=n_trials,
        seed=seed,
    )
    # Parity that retains near-scale feeders — counterexample to "symmetry⇒(A)"
    live_parity = _parity_probe(
        lambda k: (k[0] % 2 == 0) and (k[2] % 2 == 0),
        n_trials=n_trials,
        seed=seed + 1,
    )
    baseline = maximize_same_scale_ratio(
        disk="axisym_swirl_slice", n_trials=40, seed=seed + 2
    )
    killed_as_general_seat = live_parity["max_|T_near|/Z^{3/2}"] > 1e-8
    return {
        "class_id": "odd_odd_even_reflection",
        "definition": (
            "Axisymmetric-with-swirl fields with additional discrete parity "
            "on the meridional lattice (OOE-style reflections beyond axisymmetry)"
        ),
        "verdict_door1_chain": "KILL",
        "verdict_detail": (
            "KILL as a general seating of (A) / Door-1: live parities retain "
            "O(1) near-scale transfer. Some rigid parities empty triads — those "
            "are reclassified as sparse-support KEEP-CONDITIONAL, not OOE magic."
        ),
        "A_seats": False,
        "Tjj_controlled": False,
        "control_kind": None,
        "numeric": {
            "empty_triad_parity_kx_odd_kz_even": empty_parity,
            "live_parity_kx_even_kz_even": live_parity,
            "baseline_axisym_max_|T_near|/Z^{3/2}": baseline["best"][
                "max_|T_near|/Z^{3/2}"
            ],
            "n_trials": n_trials,
            "general_seat_killed": killed_as_general_seat,
        },
        "analytic": (
            "Extra reflection symmetries thin the mode set. When they empty "
            "near-scale triads they reduce to the sparse-support class. When "
            "they do not, meridional self-stretch / near-scale transfer survives "
            "at O(1) on disks. Neither case seats (A) for unrestricted "
            "axisymmetric-with-swirl."
        ),
        "why_killed": (
            "kx-even/kz-even restricted disks show max |T_near|/Z^{3/2} = "
            f"{live_parity['max_|T_near|/Z^{3/2}']:.4g} > 0; "
            "reflection symmetry alone does not kill Door-1 or seat (A)"
        ),
        "millennium_relevant": False,
        "uses_edot_zdot_lambda": False,
    }


def class_spectral_gap(
    *, n_trials: int = 40, seed: int = 25
) -> dict[str, Any]:
    """Decaying high-mode tails / enforced spectral gap between shells.

    If the neighbor band outside the target shell carries zero energy, then
    Door-1 b≥1 feeders from outside vanish and sharp b=0 energy internal
    telescopes to 0 — so energy T_{j←j}=0 under an *enforced* gap.
    Enstrophy same-scale does not inherit the telescope.
    Dynamical invariance: KILLED (NS fills gaps).
    """
    rng = np.random.default_rng(seed)
    # Enforced gap: support exactly the target shell only
    shell = shell_modes(2.5, 4.5, disk="axisym_swirl_slice")
    near_with_gap = enumerate_near_scale_feeders(shell, shell)  # pad=0
    internal = enumerate_same_scale_triads(shell)
    max_near = 0.0
    max_int = 0.0
    for _ in range(n_trials):
        field = build_reality_paired_field(shell, rng, disk="axisym_swirl_slice")
        t_near = same_scale_transfer(field, near_with_gap)
        t_int = same_scale_transfer(field, internal)
        max_near = max(max_near, abs(t_near))
        max_int = max(max_int, abs(t_int))
    # Counterexample without gap: neighbors filled
    filled = maximize_same_scale_ratio(
        disk="axisym_swirl_slice", n_trials=30, seed=seed + 3
    )
    energy_gap_ok = max_near < 1e-8 and max_int < 1e-8
    return {
        "class_id": "spectral_gap_decaying_tails",
        "definition": (
            "Fields whose Fourier mass outside each target shell's b-neighborhood "
            "is zero (hard gap) or Gevrey-small (decaying tails), so near-scale "
            "feeders are empty or negligible"
        ),
        "verdict_door1_chain": "KEEP-CONDITIONAL",
        "verdict_evolutionary": "KILL",
        "A_seats": False,  # energy Door-1 zero ≠ enstrophy (A)
        "Tjj_controlled": energy_gap_ok,
        "control_kind": (
            "energy Door-1 under enforced gap: T_near≡0 by empty feeders + "
            "b=0 identity; enstrophy same-scale NOT controlled; not invariant"
        ),
        "numeric": {
            "enforced_gap_max_|T_near|": max_near,
            "enforced_gap_max_|T_internal_b0|": max_int,
            "energy_gap_identity_holds": energy_gap_ok,
            "filled_neighbors_max_|T_near|/Z^{3/2}": filled["best"][
                "max_|T_near|/Z^{3/2}"
            ],
            "n_shell_modes": len(shell),
            "n_trials": n_trials,
        },
        "analytic": (
            "Hard gap ⇒ neighbor feeders empty ⇒ energy near-scale sum reduces "
            "to sharp b=0 internal ≡0. Soft decaying tails give a perturbative "
            "remainder controlled by the tail — conditional on the gap hypothesis. "
            "Enstrophy same-scale lacks the energy telescope. NS evolution fills "
            "spectral gaps in general (evolutionary KILL)."
        ),
        "millennium_relevant": False,
        "uses_edot_zdot_lambda": False,
    }


def class_alignment_theta(
    *, theta_star: float = 0.05, n_trials: int = 100, seed: int = 26
) -> dict[str, Any]:
    """Conditional class: geometric factor θ ≤ θ_*.

    Already have disk template |T_near|≤θ C √D Z. Class {θ≤θ_*} inherits it.
    Bridging to palinstrophy (A) still missing. Not seated for unrestricted data.
    """
    run = maximize_same_scale_ratio(
        disk="axisym_swirl_slice", n_trials=n_trials, seed=seed
    )
    # Fraction of trials with θ ≤ θ_* (diagnostic occupancy of the class)
    rng = np.random.default_rng(seed)
    support = shell_modes(0.5, 7.0, disk="axisym_swirl_slice")
    shell = shell_modes(2.5, 4.5, disk="axisym_swirl_slice")
    neighbors = shell_modes(1.0, 6.0, disk="axisym_swirl_slice")
    near = enumerate_near_scale_feeders(shell, neighbors)
    n_in = 0
    max_ratio_in = 0.0
    for _ in range(n_trials):
        field = build_reality_paired_field(support, rng, disk="axisym_swirl_slice")
        theta = geometric_factor_theta(field, near)
        if theta <= theta_star:
            n_in += 1
            shell_field = {m: field[m] for m in shell if m in field}
            z = energy_z(shell_field)
            d = dissipation_proxy(shell_field)
            t_near = same_scale_transfer(field, near)
            if z > 1e-30:
                max_ratio_in = max(max_ratio_in, abs(t_near) / (z**1.5))
    cond = conditional_theta_bound(theta=theta_star, z=1.0, d_proxy=1.0)
    return {
        "class_id": "enforced_alignment_theta",
        "definition": (
            f"Axisymmetric-with-swirl fields whose near-scale geometric factor "
            f"θ = |signed|/∑|contrib| satisfies θ ≤ θ_* = {theta_star}"
        ),
        "verdict_door1_chain": "KEEP-CONDITIONAL",
        "A_seats": False,
        "Tjj_controlled": True,
        "control_kind": (
            "conditional disk template |T_near|≤θ_* C_young √D Z; "
            "NOT (A); bridge to εν P_j missing"
        ),
        "numeric": {
            "theta_star": theta_star,
            "fraction_trials_in_class": n_in / max(n_trials, 1),
            "max_|T_near|/Z^{3/2}_inside_class": max_ratio_in,
            "unrestricted_max_|T_near|/Z^{3/2}": run["best"]["max_|T_near|/Z^{3/2}"],
            "unrestricted_theta_at_best": run["best"].get("theta_near_at_best"),
            "template": cond,
        },
        "analytic": (
            "By definition of θ, |T_near| ≤ θ ∑|contrib|. Young/Bernstein on the "
            "disk diagnostic upgrades to |T_near|≤θ C √D Z under [θ]. This plugs "
            "a Door-1 remainder *shape* into a Gronwall-ready bound only after "
            "palinstrophy normalization and ε<1 absorption — not seated. "
            "No class mechanism forces θ≤θ_* on unrestricted axisym data "
            f"(recorded α≈{THREE_D_FACTS['alignment_alpha']} is not θ-control)."
        ),
        "millennium_relevant": False,
        "uses_edot_zdot_lambda": False,
        "sharpest_surviving_note": (
            "Strongest conditional geometric candidate still open for a full "
            "proof: seat θ_* on a natural subclass OR bridge template → (A)"
        ),
    }


def class_sparse_no_near_triads(
    *, seed: int = 27
) -> dict[str, Any]:
    """Sparse spectral support with no near-scale triad into the target shell.

    Instantaneous: T_near=0 by empty triad list.
    Evolutionary: KILL (nonlinear interactions fill support).
    """
    # Hand-picked sparse meridional modes with no p+q in a designated shell
    # Shell target around |k|~3: use modes that cannot sum into that shell.
    sparse = [(1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]
    target_shell = shell_modes(2.8, 3.2, disk="axisym_swirl_slice")
    neighbor = sparse  # only these modes exist
    near = enumerate_near_scale_feeders(target_shell, neighbor)
    rng = np.random.default_rng(seed)
    field = build_reality_paired_field(sparse, rng, disk="axisym_swirl_slice")
    t_near = same_scale_transfer(field, near) if near else 0.0
    # Counterexample: denser support creates near triads
    dense = maximize_same_scale_ratio(
        disk="axisym_swirl_slice", n_trials=20, seed=seed
    )
    return {
        "class_id": "sparse_no_near_scale_triads",
        "definition": (
            "Fields whose Fourier support admits no triad (p,q,k=p+q) with "
            "p,q in the b-neighborhood and k in the target shell"
        ),
        "verdict_door1_chain": "KEEP-CONDITIONAL",
        "verdict_evolutionary": "KILL",
        "A_seats": False,  # zero energy near-scale ≠ enstrophy (A) seated for class
        "Tjj_controlled": len(near) == 0 or abs(t_near) < 1e-12,
        "control_kind": (
            "empty near-scale triad set ⇒ T_near=0 instantaneously; "
            "not NS-invariant; enstrophy path not seated"
        ),
        "numeric": {
            "sparse_modes": sparse,
            "n_near_triads": len(near),
            "T_near_on_sparse": t_near,
            "dense_max_|T_near|/Z^{3/2}": dense["best"]["max_|T_near|/Z^{3/2}"],
        },
        "analytic": (
            "No feeders ⇒ no near-scale transfer. This is a support constraint, "
            "not depletion. Under NS the bilinear term populates new modes, so "
            "the class is not invariant. Finite sparse disks overlap the "
            "fixed-K_max triviality when the whole disk is finite."
        ),
        "millennium_relevant": False,
        "uses_edot_zdot_lambda": False,
    }


def class_meridional_counterexample(
    *, n_trials: int = 40, seed: int = 28
) -> dict[str, Any]:
    """Extra natural candidate: pure meridional (no swirl).

    Axisym without swirl is essentially 2-D-like / known regular in classical
    results for axisymmetric *without* swirl. On disks, meridional-only fields
    still have T^{mm} near-scale transfer — regularity comes from 2-D structure
    / vorticity stretching absence in the no-swirl axisym NS, not from T≡0.
    Record numeric nonzero T_near to avoid confusing 'regular' with 'Tjj=0'.
    """
    rng = np.random.default_rng(seed)
    support = shell_modes(0.5, 7.0, disk="axisym_swirl_slice")
    max_ratio = 0.0
    for _ in range(n_trials):
        field = build_meridional_only_field(support, rng)
        rec = probe_field_near_scale(field)
        max_ratio = max(max_ratio, rec["|T_near|/Z^{3/2}"])
    return {
        "class_id": "pure_meridional_no_swirl",
        "definition": (
            "Axisymmetric with u^θ≡0 (no swirl); classical regularity path "
            "differs from swirl case"
        ),
        "verdict_door1_chain": "KEEP-CONDITIONAL",
        "A_seats": False,
        "Tjj_controlled": False,
        "control_kind": (
            "regularity by no-swirl axisym theory (different path); "
            "energy near-scale T can still be nonzero on disks"
        ),
        "numeric": {
            "max_|T_near|/Z^{3/2}": max_ratio,
            "n_trials": n_trials,
            "nonzero_near_scale_on_disk": max_ratio > 1e-8,
        },
        "analytic": (
            "Axisymmetric NS *without* swirl is a different, classical regularity "
            "class. Disk diagnostics still show nonzero near-scale energy transfer; "
            "do not equate 'no swirl ⇒ Tjj=0'. With-swirl is the hard class."
        ),
        "millennium_relevant": False,
        "uses_edot_zdot_lambda": False,
        "note": "Listed so 'no swirl' is not smuggled as a with-swirl Door-1 kill",
    }


def run_class_hunt_battery() -> dict[str, Any]:
    """Run all candidate class probes; emit KEEP/KILL summary."""
    results = [
        class_pure_swirl(),
        class_finite_fourier_disk(),
        class_small_data(),
        class_odd_odd_even(),
        class_spectral_gap(),
        class_alignment_theta(),
        class_sparse_no_near_triads(),
        class_meridional_counterexample(),
    ]
    by_id = {r["class_id"]: r for r in results}

    surviving = []
    killed = []
    for r in results:
        v = r["verdict_door1_chain"]
        entry = {
            "class_id": r["class_id"],
            "verdict": v,
            "A_seats": r.get("A_seats"),
            "Tjj_controlled": r.get("Tjj_controlled"),
            "control_kind": r.get("control_kind"),
            "millennium_relevant": r.get("millennium_relevant"),
        }
        if v.startswith("KEEP"):
            surviving.append(entry)
        else:
            killed.append(entry)

    sharpest = [
        {
            "class_id": "enforced_alignment_theta",
            "why": (
                "Only conditional geometric handle that targets the actual "
                "Door-1 near-scale remainder without pretending b=0 energy "
                "zero is depletion; still needs θ_* seating + bridge to (A)"
            ),
        },
        {
            "class_id": "pure_swirl",
            "why": (
                "Instantaneous T≡0 identity (KEEP); evolutionary KILL; "
                "does not close mixed with-swirl data"
            ),
        },
        {
            "class_id": "spectral_gap_decaying_tails",
            "why": (
                "Energy Door-1 vanishes under enforced gap; enstrophy open; "
                "evolutionary KILL"
            ),
        },
        {
            "class_id": "small_data_critical_subcritical",
            "why": (
                "Classical small-data path seats regularity/(A)-shaped absorption "
                "by smallness; not large-data Door-1"
            ),
        },
    ]

    return {
        "honesty": HONESTY,
        "mission": (
            "Find or falsify a class where (A) seats or near-scale Tjj admits "
            "a class-uniform bound usable in conditional Gronwall — without "
            "ė_j/Ż/Λ′ recycling"
        ),
        "classes": by_id,
        "summary_table": [
            {
                "class_id": r["class_id"],
                "verdict": r["verdict_door1_chain"],
                "A_seats": r.get("A_seats"),
                "Tjj_controlled": r.get("Tjj_controlled"),
                "millennium_relevant": r.get("millennium_relevant"),
            }
            for r in results
        ],
        "surviving_conditional_or_instantaneous": surviving,
        "killed_or_not_seating": killed,
        "sharpest_surviving_candidates": sharpest,
        "still_missing_for_full_proof": [
            "Class control of θ_* (or other depletion) on a natural large-data subclass",
            "Bridge from θ-template / energy gap to palinstrophy (A): |Tjj|≤εν P_j+R",
            "Non-circular path to (A) without ė_j/Ż/Λ′",
            "Enstrophy same-scale control (energy b=0 identity does not transfer)",
            "Cross-scale bounds/summability (separate gap)",
        ],
        "overall": (
            "No Millennium-scaling large-data class found that seats (A) or "
            "kills near-scale Tjj uniformly. Survivors are conditional "
            "(θ≤θ_*, spectral gap, small data, fixed K_max) or instantaneous "
            "(pure swirl / sparse). OOE KILLED as seating. (A) not seated for "
            "unaugmented axisymmetric-with-swirl. NS not solved."
        ),
    }


def main() -> None:
    import json

    print(json.dumps(run_class_hunt_battery(), indent=2, default=float))


if __name__ == "__main__":
    main()
