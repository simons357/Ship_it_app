"""Same-scale transfer T_{j←j} attack under axisymmetry-with-swirl.

Class: unaugmented axisymmetric-with-swirl (exact Fourier disks as probes).
Quantity: Door-1 same-scale block T_{j←j}.
Remainder: T_{j←j} itself (still OPEN).
Assumed: [small exact disks / restricted classes only; signed Im form;
no absolute-value Young that destroys the problem; no ė_j / Ż / Λ'
recycling; NS not solved; no invented proofs; spectral-shift ≠ Lemma★].

This module structures the object, runs kill/search numerics, and
records conditional templates. It does NOT seat (A) or close NS.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Iterable, Literal

import numpy as np

from .axisymmetric_shell import (
    COMPACT_SWIRL_SAMPLES,
    THREE_D_FACTS,
    pairing_residual,
)
from .axisym_ac_tests import (
    condition_b_occupancy_alignment,
    occupancy_implication_table,
)

# ---------------------------------------------------------------------------
# A. Sharp definition (Fourier / shell projectors as in the estimate note)
# ---------------------------------------------------------------------------

DEFINITION = {
    "class": "unaugmented axisymmetric-with-swirl (exact-disk probes)",
    "quantity": "Door-1 same-scale block T_{j←j}",
    "remainder": "T_{j←j}",
    "LP_piece": (
        "T_{j←ℓm} := -<P_j((P_ℓ u)·∇(P_m u)), P_j u>, "
        "P_j = Littlewood–Paley projector onto |ξ|~2^j"
    ),
    "same_scale_block": (
        "T_{j←j} := sum_{|ℓ-j|≤b, |m-j|≤b} T_{j←ℓm} "
        "(b = named locality width, grouping cutoff not smallness)"
    ),
    "cross_scale_block": (
        "T_{j←≠j} := sum of pieces with |ℓ-j|>b or |m-j|>b "
        "(includes HH→L and other far interactions); "
        "NOT the same-scale remainder; precise bounds not established here"
    ),
    "Fourier_signed_form": (
        "On a closed triad p+q=k with amplitudes û_p, û_q, û_k "
        "(div-free), the signed contribution into k is "
        "Im[(û_p·q)(û_q·û_k*)]. No absolute-value Young in this diagnostic."
    ),
    "energy_sharp_b0_identity": (
        "For the ENERGY shell with a sharp spectral cutoff and b=0 "
        "(p,q,k all in the same annulus closed under k↔−k), "
        "sum of internal triad energy transfers vanishes: each closed "
        "triad obeys J_p+J_q+J_r=0. So sharp b=0 energy T_{j←j}≡0. "
        "Door-1 same-scale with b≥1 is near-scale leakage, not this zero. "
        "Enstrophy T_{j←j} does not inherit this telescope."
    ),
    "axisym_swirl_kill_or_reduce": {
        "kills": (
            "free helical HHH supported on fully 3-D wavevector "
            "configurations that violate axisymmetry about z"
        ),
        "reduces": (
            "mode support to meridional wavevectors k=(k_x,0,k_z) "
            "with swirl polarization along ê_y allowed"
        ),
        "does_not_kill": (
            "meridional self-stretch T^{mm} on mixed swirl+meridional "
            "fields; near-scale (b≥1) energy transfer; enstrophy same-scale"
        ),
    },
    "known_vs_remainder": {
        "known_or_moved": [
            "pressure drops in the energy pairing",
            "viscous −ν D_j cannot grow Z_j",
            "cross-shell flux T_{j←≠j} is moved by the Door-1 budget "
            "(telescope; precise bounds/summability NOT established)",
            "spectral-shift identity on a listed triad (bookkeeping only)",
            "main local transport vanishes (enstrophy write); only commutator",
            "pure-swirl (u^r=u^z=0) ⇒ T_{j←j}=0 on that field",
            "sharp b=0 ENERGY internal transfer ≡0 (triad pairing)",
        ],
        "remainder": (
            "Door-1 T_{j←j} at b≥1 (near-scale energy) and/or "
            "enstrophy same-scale stretch — still OPEN"
        ),
    },
    "not_lemma_star": True,
    "not_energy_absorption_via_rho": True,
}


DiskClass = Literal["unrestricted_3d", "axisym_swirl_slice"]


@dataclass(frozen=True)
class Mode:
    k: tuple[int, int, int]
    amp: np.ndarray  # complex (3,)


def _norm(k: tuple[int, int, int]) -> float:
    return math.sqrt(float(k[0] * k[0] + k[1] * k[1] + k[2] * k[2]))


def shell_modes(
    k_min: float,
    k_max: float,
    *,
    disk: DiskClass,
) -> list[tuple[int, int, int]]:
    """Integer lattice modes in a radial shell band."""
    out: list[tuple[int, int, int]] = []
    lim = int(math.ceil(k_max)) + 1
    for kx in range(-lim, lim + 1):
        for ky in range(-lim, lim + 1):
            for kz in range(-lim, lim + 1):
                if disk == "axisym_swirl_slice" and ky != 0:
                    continue
                if kx == 0 and ky == 0 and kz == 0:
                    continue
                kn = _norm((kx, ky, kz))
                if k_min <= kn <= k_max:
                    out.append((kx, ky, kz))
    return out


def random_div_free_amp(
    k: tuple[int, int, int],
    rng: np.random.Generator,
    *,
    disk: DiskClass,
) -> np.ndarray:
    """Random complex amplitude with k·û=0.

    On the axisym swirl slice (k_y=0), the swirl polarization ê_y is allowed;
    meridional components lie in the (k, ê_z×k̂_merid) plane.
    """
    kv = np.array(k, dtype=float)
    kn = np.linalg.norm(kv)
    assert kn > 0.0
    khat = kv / kn
    # Two orthonormal vectors perpendicular to k.
    if abs(khat[2]) < 0.9:
        e1 = np.cross(khat, np.array([0.0, 0.0, 1.0]))
    else:
        e1 = np.cross(khat, np.array([0.0, 1.0, 0.0]))
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(khat, e1)
    if disk == "axisym_swirl_slice":
        # Prefer swirl (ê_y) when it is admissible: for k=(kx,0,kz), ê_y ⟂ k.
        ey = np.array([0.0, 1.0, 0.0])
        if abs(float(np.dot(ey, khat))) < 1e-12:
            e_swirl = ey
            e_mer = np.cross(khat, e_swirl)
            e_mer /= np.linalg.norm(e_mer)
            c1 = (rng.normal() + 1j * rng.normal()) / math.sqrt(2.0)
            c2 = (rng.normal() + 1j * rng.normal()) / math.sqrt(2.0)
            return c1 * e_swirl + c2 * e_mer
    c1 = (rng.normal() + 1j * rng.normal()) / math.sqrt(2.0)
    c2 = (rng.normal() + 1j * rng.normal()) / math.sqrt(2.0)
    return c1 * e1 + c2 * e2


def triad_signed_transfer(
    up: np.ndarray,
    uq: np.ndarray,
    uk: np.ndarray,
    q: tuple[int, int, int],
) -> float:
    """Signed Im[(û_p·q)(û_q·û_k*)] for one oriented triad p+q=k."""
    qv = np.array(q, dtype=float)
    scalar = complex(np.dot(up, qv))
    bil = complex(np.vdot(uk, uq))  # û_q · û_k*  via vdot(uk,uq)=sum uk* conj? 
    # np.vdot(a,b) = sum conj(a)*b. We want û_q · û_k* = sum_i uq_i conj(uk_i)
    # = np.vdot(uk, uq).
    return float(np.imag(scalar * bil))


def build_reality_paired_field(
    modes: Iterable[tuple[int, int, int]],
    rng: np.random.Generator,
    *,
    disk: DiskClass,
) -> dict[tuple[int, int, int], np.ndarray]:
    """Build û(-k)=conj(û(k)) field on the listed modes."""
    field: dict[tuple[int, int, int], np.ndarray] = {}
    seen: set[tuple[int, int, int]] = set()
    for k in modes:
        if k in seen:
            continue
        mk = (-k[0], -k[1], -k[2])
        amp = random_div_free_amp(k, rng, disk=disk)
        field[k] = amp
        field[mk] = np.conjugate(amp)
        seen.add(k)
        seen.add(mk)
    return field


def energy_z(field: dict[tuple[int, int, int], np.ndarray]) -> float:
    """Z = (1/2) sum_k |û_k|^2  (Parseval proxy on the disk)."""
    return 0.5 * float(
        sum(float(np.vdot(u, u).real) for u in field.values())
    )


def dissipation_proxy(
    field: dict[tuple[int, int, int], np.ndarray],
) -> float:
    """D = sum_k |k|^2 |û_k|^2  (∇ proxy; not palinstrophy)."""
    total = 0.0
    for k, u in field.items():
        total += (_norm(k) ** 2) * float(np.vdot(u, u).real)
    return total


def enumerate_same_scale_triads(
    modes: list[tuple[int, int, int]],
) -> list[tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]]:
    """Triads p+q=k with p,q,k all in the same mode set (sharp b=0 internal)."""
    mode_set = set(modes)
    triads: list[
        tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]
    ] = []
    for i, p in enumerate(modes):
        for q in modes[i:]:
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k in mode_set and k != (0, 0, 0):
                triads.append((p, q, k))
    return triads


def enumerate_near_scale_feeders(
    target_shell: list[tuple[int, int, int]],
    neighbor_band: list[tuple[int, int, int]],
) -> list[tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]]:
    """Door-1 b≥1 probe: p,q in neighbor band, k=p+q in target shell.

    Includes pure internal (b=0) legs when neighbors contain the shell,
    plus genuine near-scale legs with at least one foot outside the target.
    """
    target_set = set(target_shell)
    triads: list[
        tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]
    ] = []
    for i, p in enumerate(neighbor_band):
        for q in neighbor_band[i:]:
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k in target_set:
                triads.append((p, q, k))
    return triads


def enumerate_hh_to_l_triads(
    high_modes: list[tuple[int, int, int]],
    low_modes: list[tuple[int, int, int]],
) -> list[tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]]:
    """Cross-scale HH→L: two high modes feed a low mode (not same-scale)."""
    low_set = set(low_modes)
    triads = []
    for i, p in enumerate(high_modes):
        for q in high_modes[i:]:
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k in low_set:
                triads.append((p, q, k))
    return triads


def same_scale_transfer(
    field: dict[tuple[int, int, int], np.ndarray],
    triads: list[
        tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]
    ],
) -> float:
    """Signed sum of Im forms over listed triads (no abs Young)."""
    total = 0.0
    for p, q, k in triads:
        up = field.get(p)
        uq = field.get(q)
        uk = field.get(k)
        if up is None or uq is None or uk is None:
            continue
        total += triad_signed_transfer(up, uq, uk, q)
        if p != q:
            # p↔q orientation also contributes when p≠q was only half-listed
            total += triad_signed_transfer(uq, up, uk, p)
    return total


def geometric_factor_theta(
    field: dict[tuple[int, int, int], np.ndarray],
    triads: list[
        tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]
    ],
) -> float:
    """Proxy θ ∈ [0,1]: |signed sum| / sum|contrib| (cancellation factor).

    θ≈1 means little cancellation; θ≪1 means signed cancellation.
    Occupancy/alignment are separate; this is not depletion⇒(A).
    """
    signed = 0.0
    abs_sum = 0.0
    for p, q, k in triads:
        up = field.get(p)
        uq = field.get(q)
        uk = field.get(k)
        if up is None or uq is None or uk is None:
            continue
        c = triad_signed_transfer(up, uq, uk, q)
        signed += c
        abs_sum += abs(c)
        if p != q:
            c2 = triad_signed_transfer(uq, up, uk, p)
            signed += c2
            abs_sum += abs(c2)
    if abs_sum <= 1e-30:
        return 0.0
    return abs(signed) / abs_sum


def maximize_same_scale_ratio(
    *,
    k_min: float = 2.5,
    k_max: float = 4.5,
    neighbor_pad: float = 1.5,
    support_k_min: float = 0.5,
    support_k_max: float = 7.0,
    disk: DiskClass = "axisym_swirl_slice",
    n_trials: int = 200,
    seed: int = 0,
) -> dict[str, Any]:
    """Maximize |T| ratios for sharp b=0 vs Door-1 near-scale (b≥1).

    Sharp b=0 (p,q,k all in target shell): energy internal sum ≡0 by triad
    pairing — recorded as identity check, not depletion.

    Near-scale (Door-1 b≥1 proxy): p,q in neighbor band
    [k_min-pad, k_max+pad], k in target shell — this is the energy remainder
    that can be nonzero.

    HH→L: two high modes feed a low mode — separated from same-scale.

    Scope: this disk / these trials only. Not K_max→∞. Not class ρ_j.
    Does not use ė_j, Ż, or Λ'.
    """
    rng = np.random.default_rng(seed)
    support = shell_modes(support_k_min, support_k_max, disk=disk)
    shell = shell_modes(k_min, k_max, disk=disk)
    neighbors = shell_modes(
        max(support_k_min, k_min - neighbor_pad),
        min(support_k_max, k_max + neighbor_pad),
        disk=disk,
    )
    low_modes = shell_modes(
        support_k_min, max(support_k_min, k_min - 0.25), disk=disk
    )
    internal_triads = enumerate_same_scale_triads(shell)
    near_triads = enumerate_near_scale_feeders(shell, neighbors)
    hh_triads = enumerate_hh_to_l_triads(shell, low_modes)

    best: dict[str, Any] = {
        "max_|T_near|/Z^{3/2}": 0.0,
        "max_|T_near|/(Z * sqrt(D))": 0.0,
        "max_theta_near": 0.0,
        "trial": -1,
    }
    records: list[dict[str, Any]] = []
    for t in range(int(n_trials)):
        field = build_reality_paired_field(support, rng, disk=disk)
        shell_field = {m: field[m] for m in shell if m in field}
        z = energy_z(shell_field)
        d = dissipation_proxy(shell_field)
        if z <= 1e-30:
            continue
        t_internal = same_scale_transfer(field, internal_triads)
        t_near = same_scale_transfer(field, near_triads)
        t_hh = same_scale_transfer(field, hh_triads)
        theta_near = geometric_factor_theta(field, near_triads)
        ratio_z = abs(t_near) / (z ** 1.5)
        ratio_zd = abs(t_near) / (z * math.sqrt(max(d, 1e-30)))
        rec = {
            "trial": t,
            "T_internal_b0": t_internal,
            "T_near_b1": t_near,
            "T_HH_to_L": t_hh,
            "Z_shell": z,
            "D_proxy_shell": d,
            "theta_near": theta_near,
            "|T_near|/Z^{3/2}": ratio_z,
            "|T_near|/(Z*sqrt(D))": ratio_zd,
        }
        records.append(rec)
        if ratio_z >= best["max_|T_near|/Z^{3/2}"]:
            best = {
                "max_|T_near|/Z^{3/2}": ratio_z,
                "max_|T_near|/(Z * sqrt(D))": ratio_zd,
                "max_theta_near": theta_near,
                "T_near_at_best": t_near,
                "T_internal_b0_at_best": t_internal,
                "T_HH_to_L_at_best": t_hh,
                "theta_near_at_best": theta_near,
                "Z_at_best": z,
                "trial": t,
            }

    max_internal = float(
        max((abs(r["T_internal_b0"]) for r in records), default=0.0)
    )
    return {
        "disk": disk,
        "k_min": k_min,
        "k_max": k_max,
        "neighbor_pad": neighbor_pad,
        "support_k_min": support_k_min,
        "support_k_max": support_k_max,
        "n_support_modes": len(support),
        "n_shell_modes": len(shell),
        "n_neighbor_modes": len(neighbors),
        "n_internal_b0_triads": len(internal_triads),
        "n_near_b1_triads": len(near_triads),
        "n_hh_to_l_triads": len(hh_triads),
        "n_trials": n_trials,
        "seed": seed,
        "best": best,
        # Back-compat aliases used by avenues/tests
        "max_|T|/Z^{3/2}": best["max_|T_near|/Z^{3/2}"],
        "mean_|T|/Z^{3/2}": float(
            np.mean([r["|T_near|/Z^{3/2}"] for r in records]) if records else 0.0
        ),
        "mean_theta": float(
            np.mean([r["theta_near"] for r in records]) if records else 0.0
        ),
        "max_|T_internal_b0|": max_internal,
        "mean_|T_internal_b0|": float(
            np.mean([abs(r["T_internal_b0"]) for r in records]) if records else 0.0
        ),
        "energy_sharp_b0_identity_holds": max_internal < 1e-8,
        "hygiene_shell_only_would_telescope": (
            "Sharp b=0 ENERGY internal transfer ≡0 by triad pairing "
            "(Jp+Jq+Jr=0); Door-1 remainder is near-scale b≥1 / enstrophy"
        ),
        "scope": "small exact disk / finite trials; no K_max→∞; not class ρ_j",
        "separates_HH_to_L": True,
        "uses_edot_zdot_lambda": False,
        "claimed_bound": False,
    }


# ---------------------------------------------------------------------------
# B. Attack avenues
# ---------------------------------------------------------------------------

def avenue_axisym_cancellation() -> dict[str, Any]:
    """Avenue 1: axisymmetric structure constants / signed cancellation.

    Status PARTIAL: restriction kills free 3-D HHH support; signed Im form
    is the right object; absolute-value Young refused. Sharp b=0 energy
    internal ≡0 (identity). Near-scale b≥1 remains open. No uniform bound.
    """
    slice_run = maximize_same_scale_ratio(
        disk="axisym_swirl_slice", n_trials=100, seed=1
    )
    full_run = maximize_same_scale_ratio(
        disk="unrestricted_3d",
        n_trials=40,
        seed=2,
        k_min=2.5,
        k_max=3.8,
        neighbor_pad=1.2,
        support_k_min=0.5,
        support_k_max=5.5,
    )
    return {
        "avenue": "axisym_cancellation_structure_constants",
        "status": "PARTIAL",
        "what_axisym_kills": DEFINITION["axisym_swirl_kill_or_reduce"]["kills"],
        "what_remains": DEFINITION["axisym_swirl_kill_or_reduce"]["does_not_kill"],
        "signed_Im_form": DEFINITION["Fourier_signed_form"],
        "energy_sharp_b0_identity": DEFINITION["energy_sharp_b0_identity"],
        "absolute_value_Young": "REFUSED for this avenue",
        "numeric_slice": {
            "max_|T_near|/Z^{3/2}": slice_run["best"]["max_|T_near|/Z^{3/2}"],
            "mean_theta_near": slice_run["mean_theta"],
            "mean_|T_near|/Z^{3/2}": slice_run["mean_|T|/Z^{3/2}"],
            "max_|T_internal_b0|": slice_run["max_|T_internal_b0|"],
            "energy_sharp_b0_identity_holds": slice_run[
                "energy_sharp_b0_identity_holds"
            ],
            "n_shell_modes": slice_run["n_shell_modes"],
            "n_near_triads": slice_run["n_near_b1_triads"],
        },
        "numeric_unrestricted_3d": {
            "max_|T_near|/Z^{3/2}": full_run["best"]["max_|T_near|/Z^{3/2}"],
            "mean_theta_near": full_run["mean_theta"],
            "mean_|T_near|/Z^{3/2}": full_run["mean_|T|/Z^{3/2}"],
            "max_|T_internal_b0|": full_run["max_|T_internal_b0|"],
            "n_shell_modes": full_run["n_shell_modes"],
            "n_near_triads": full_run["n_near_b1_triads"],
        },
        "hygiene": slice_run["hygiene_shell_only_would_telescope"],
        "verdict": (
            "Sharp b=0 energy internal transfer vanishes (triad pairing). "
            "Near-scale (b≥1) signed transfer is the Door-1 energy remainder "
            "and is nonzero on these disks; axisym reduces triad count but "
            "does not kill it. Absolute-value Young refused. No uniform bound."
        ),
        "bound_obtained": None,
    }


def avenue_depletion_to_A() -> dict[str, Any]:
    """Avenue 2: depletion ⇒ (A) without recycling ė_j/Ż/Λ′.

    Kill false candidates with the occupancy/alignment harness.
    """
    occ = occupancy_implication_table()
    b = condition_b_occupancy_alignment()
    # False candidate 1: occupancy 1 ⇒ depletion (killed)
    false_1 = {
        "candidate": "occupancy 1 on HHH ⇒ depletion ⇒ (A)",
        "status": "KILLED",
        "evidence": {
            "occupancy": THREE_D_FACTS["HHH_occupancy_on_orbits_run"],
            "alignment_alpha": THREE_D_FACTS["alignment_alpha"],
            "establishes_depletion": False,
        },
        "why": b["why"],
    }
    # False candidate 2: 1-|α|≈1/2 is already the (A) factor (killed)
    false_2 = {
        "candidate": "factor (1-|α|)≈1/2 from recorded α seats (A)",
        "status": "KILLED",
        "evidence": {
            "depletion_factor_1_minus_|alpha|": b["depletion_factor_1_minus_|alpha|"],
            "needed_for_absorption_shape": "factor small enough that ε<1 after Young",
        },
        "why": (
            "α≈1/2 gives O(1) stretch factor, not a vanishing depletion; "
            "does not imply |Tjj|≤ε ν P_j + R"
        ),
    }
    # False candidate 3: recycle Ż or Λ' into (A) (killed by honesty lock)
    false_3 = {
        "candidate": "bound |Tjj| using Ż or Λ' then call it (A)",
        "status": "KILLED",
        "why": (
            "Step 6 / (A) must not reintroduce the quantity being bounded "
            "via ė_j, Ż, or Λ'"
        ),
    }
    # False candidate 4: sharp b=0 energy zero as depletion (killed)
    false_4 = {
        "candidate": "sharp b=0 energy T_internal≡0 ⇒ depletion ⇒ (A)",
        "status": "KILLED",
        "why": (
            "That zero is the triad energy identity (Jp+Jq+Jr=0), not "
            "geometric depletion; Door-1 remainder is near-scale b≥1 / enstrophy"
        ),
    }
    # Surviving candidate shape (not seated)
    surviving = {
        "candidate": (
            "[θ] geometric/alignment factor with |T_near| ≤ θ · (template "
            "controlled by energy/palinstrophy) and θ small enough ⇒ (A)"
        ),
        "status": "OPEN",
        "hypotheses_required": [
            "[θ-control] measurable geometric factor θ with 0≤θ≤θ_*<1 "
            "uniformly on the class (not just occupancy)",
            "[template] Young/Bernstein template with constants named, "
            "no ė_j/Ż/Λ'",
            "[no-cycle] spectral-shift identity not used as a bound",
            "[right object] apply to near-scale b≥1 / enstrophy, not sharp b=0 energy identity",
        ],
        "seated_for_class": False,
        "why_open": (
            "No class print of θ_*; recorded α≈1/2 and occupancy 1 do not "
            "supply it; exact-disk θ is a diagnostic only"
        ),
    }
    return {
        "avenue": "depletion_implies_A",
        "status": "PARTIAL",
        "killed": [false_1, false_2, false_3, false_4],
        "open_candidate": surviving,
        "occupancy_table_summary": {
            "establishes_depletion": occ["establishes_depletion"],
            "does_not_imply": occ["does_not_imply"][:4],
        },
        "bound_obtained": None,
        "implies_A_for_class": False,
    }


def conditional_theta_bound(
    *,
    theta: float,
    z: float,
    d_proxy: float,
    c_young: float = 1.0,
) -> dict[str, Any]:
    """Conditional template: if geometric factor ≤ θ then |T| ≤ θ C √D Z.

    Not (A) unless rewritten in palinstrophy and ε ν seated. No ė_j/Ż/Λ'.
    """
    theta = float(theta)
    if not (0.0 <= theta <= 1.0):
        return {
            "status": "refused",
            "why": "θ must lie in [0,1]",
            "claimed": False,
        }
    rhs = float(theta) * float(c_young) * math.sqrt(max(float(d_proxy), 0.0)) * float(z)
    return {
        "status": "conditional_template",
        "claimed": False,
        "hypothesis": "[θ] geometric_factor_theta(field) ≤ θ on the disk",
        "form": "|T_same| ≤ θ · C_young · √D · Z",
        "theta": theta,
        "C_young": float(c_young),
        "rhs": rhs,
        "is_condition_A": False,
        "why_not_A": (
            "denominator is energy×√D_proxy, not ε ν palinstrophy P_j; "
            "bridging to (A) needs a named Poincaré/palinstrophy step "
            "and class control of θ — not supplied"
        ),
        "uses_edot_zdot_lambda": False,
    }


def avenue_conditional_theta() -> dict[str, Any]:
    """Avenue 3: conditional bounds under geometric factor θ."""
    run = maximize_same_scale_ratio(
        disk="axisym_swirl_slice", n_trials=120, seed=3
    )
    theta_star = float(run["best"].get("theta_near_at_best", run["mean_theta"]))
    mixed = float(COMPACT_SWIRL_SAMPLES["mixed_m1_n32_max_|Tjj/Xj|"])
    pure = float(COMPACT_SWIRL_SAMPLES["pure_swirl_n32_max_|Tjj/Xj|"])
    cond = conditional_theta_bound(
        theta=min(1.0, max(0.0, theta_star)),
        z=1.0,
        d_proxy=1.0,
        c_young=1.0,
    )
    dangerous = (
        theta_star >= 0.05 and run["best"]["max_|T_near|/Z^{3/2}"] > 1e-6
    )
    return {
        "avenue": "conditional_theta_bound",
        "status": "PARTIAL",
        "conditional_template": cond,
        "disk_best_theta_near": theta_star,
        "disk_max_|T_near|/Z^{3/2}": run["best"]["max_|T_near|/Z^{3/2}"],
        "energy_sharp_b0_identity_holds": run["energy_sharp_b0_identity_holds"],
        "recorded_compact": {
            "pure_swirl_max_|Tjj/Xj|": pure,
            "mixed_m1_n32_max_|Tjj/Xj|": mixed,
            "pure_looks_depleted": pure < 1e-15,
            "mixed_looks_O(1e-3)_not_class_rho": True,
        },
        "same_scale_looks": (
            "near_scale_dangerous_on_axisym_disk_trials"
            if dangerous
            else "near_scale_reduced_but_not_killed"
        ),
        "bound_obtained": (
            f"CONDITIONAL only: if θ≤{theta_star:.4g} then "
            f"|T_near|≤θ C √D Z on that disk diagnostic"
        ),
        "class_bound": None,
        "seats_A": False,
    }


def avenue_numeric_kill_search() -> dict[str, Any]:
    """Avenue 4: maximize |Tjj|/denominators; separate HH→L and b=0 identity."""
    axisym = maximize_same_scale_ratio(
        disk="axisym_swirl_slice", n_trials=150, seed=7
    )
    jp, jq, jr = 0.25, -0.1, -0.15
    max_ratio = float(axisym["best"]["max_|T_near|/Z^{3/2}"])
    nonzero = max_ratio > 1e-8
    return {
        "avenue": "numeric_kill_search",
        "status": "PARTIAL",
        "axisym_disk": axisym,
        "pairing_residual_toy": pairing_residual(jp, jq, jr),
        "findings": [
            "Sharp b=0 ENERGY internal T ≡0 on disk (triad pairing identity)",
            (
                "Near-scale (b≥1) signed transfer is nonzero on axisym disks"
                if nonzero
                else "Near-scale max |T|/Z^{3/2} stayed below gate on these trials"
            ),
            "HH→L triads are enumerated separately and are not the Door-1 remainder",
            "max |T_near|/Z^{3/2} on these trials is a disk fact, not a class bound",
            (
                f"θ_near_at_best="
                f"{axisym['best'].get('theta_near_at_best', float('nan')):.4g}"
            ),
        ],
        "killed_claim": (
            "Claim 'axisymmetry alone forces Door-1 Tjj≈0 on mixed fields' "
            "is KILLED by nonzero near-scale max |T_near|/Z^{3/2}"
            if nonzero
            else "Nonzero near-scale kill not fired on this seed/disk "
            "(inconclusive, not a close)"
        ),
        "killed_artifact": (
            "Claim 'sharp b=0 energy T_internal≡0 proves depletion' is KILLED: "
            "that zero is the triad energy identity, not geometric depletion; "
            "Door-1 remainder lives at b≥1 / enstrophy"
        ),
        "left_for_A": (
            "Need class control of a geometric factor (or other depletion) "
            "on near-scale / enstrophy Tjj that yields |Tjj|≤ε ν P_j+R "
            "without ė_j/Ż/Λ'"
        ),
        "bound_obtained": None,
        "claimed": False,
    }


def run_same_scale_attack_battery() -> dict[str, Any]:
    """One-shot honest battery for the same-scale attack."""
    a1 = avenue_axisym_cancellation()
    a2 = avenue_depletion_to_A()
    a3 = avenue_conditional_theta()
    a4 = avenue_numeric_kill_search()
    return {
        "honesty": {
            "NS_solved": False,
            "clay": "NOT CLAIMED",
            "proofs_invented": False,
            "lemma_star_smuggled": False,
            "principal_unresolved": "T_{j←j}",
            "uses_edot_zdot_lambda_to_bound_Tjj": False,
        },
        "definition": DEFINITION,
        "avenues": {
            "1_axisym_cancellation": a1,
            "2_depletion_to_A": a2,
            "3_conditional_theta": a3,
            "4_numeric_kill_search": a4,
        },
        "summary": {
            "1_axisym_cancellation": a1["status"],
            "2_depletion_to_A": a2["status"],
            "3_conditional_theta": a3["status"],
            "4_numeric_kill_search": a4["status"],
            "overall": (
                "OPEN — sharp b=0 energy internal ≡0 (identity); "
                "near-scale/enstrophy remainder; conditional θ only; (A) not seated"
            ),
            "strongest_honest_progress": (
                "Structured T_{j←j}; separated HH→L; recorded sharp b=0 energy "
                "identity; killed occupancy/α/Ż-recycling and b=0-as-depletion; "
                "conditional |T_near|≤θ C √D Z; near-scale survives on axisym disks"
            ),
        },
    }


def main() -> None:
    import json

    print(json.dumps(run_same_scale_attack_battery(), indent=2, default=float))


if __name__ == "__main__":
    main()
