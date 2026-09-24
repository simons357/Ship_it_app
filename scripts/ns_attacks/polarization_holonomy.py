"""Polarization / helical holonomy after the phase gauge is quotiented.

Each mode still has to satisfy k · v_k = 0. In helical coordinates
that is two complex amplitudes a_k^+, a_k^−.

A star can realize any collection of preferred couplings at the
shared vertex (already shown on the two-triad witness). A loop
asks a sharper question:

    does the preferred helicity/polarization state, transported
    around a triadic cycle, return to the same state?

If it does: no static loop defect.
If it returns rotated / flipped: genuine polarization holonomy.

This page computes that discrete transport on the locked
parallelogram and on the archive star. It does not claim a
theorem for every lattice family.

Not a T_c bound. Not DA-NS-2. NS is not solved.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

from ns_attacks.helical import AXES, all_helical_couplings, as_mode
from ns_attacks.loop_gauge import (
    PARALLELOGRAM,
    STAR_WITNESS,
    incidence_matrix,
    left_kernel_basis,
)

Mode = Tuple[int, int, int]
Triad = Tuple[Mode, Mode, Mode]
Sigma = Tuple[int, int, int]


def preferred_assignments(
    triads: Sequence[Sequence[Sequence[int]]],
    axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> List[dict]:
    rows = []
    for t in triads:
        p, q, k = as_mode(t[0]), as_mode(t[1]), as_mode(t[2])
        coup = all_helical_couplings(p, q, k, axis)
        rows.append(
            {
                "triad": (p, q, k),
                "preferred": coup["preferred"]["sigma"],
                "tied_sigmas": coup["tied_sigmas"],
                "abs_g": coup["preferred"]["abs_g"],
                "chi": coup["preferred"]["arg_g"],
            }
        )
    return rows


def _consistent(assign: Dict[Mode, int], triad: Triad, sigma: Sigma) -> bool:
    p, q, k = triad
    want = {p: sigma[0], q: sigma[1], k: sigma[2]}
    for mode, s in want.items():
        if mode in assign and assign[mode] != s:
            return False
    return True


def _apply(assign: Dict[Mode, int], triad: Triad, sigma: Sigma) -> Dict[Mode, int]:
    out = dict(assign)
    p, q, k = triad
    out[p], out[q], out[k] = sigma[0], sigma[1], sigma[2]
    return out


def realize_preferred(
    triads: Sequence[Triad],
    choices: Sequence[Sequence[Sigma]],
) -> Optional[Dict[Mode, int]]:
    """Backtrack over (possibly tied) preferred helicity triples."""

    def rec(i: int, assign: Dict[Mode, int]) -> Optional[Dict[Mode, int]]:
        if i == len(triads):
            return assign
        for sigma in choices[i]:
            if not _consistent(assign, triads[i], sigma):
                continue
            hit = rec(i + 1, _apply(assign, triads[i], sigma))
            if hit is not None:
                return hit
        return None

    return rec(0, {})


def polarization_test(
    triads: Sequence[Sequence[Sequence[int]]],
    axis: Sequence[float] = (0.0, 0.0, 1.0),
    use_ties: bool = True,
) -> dict:
    closed, modes, B = incidence_matrix(triads)
    prefs = preferred_assignments(closed, axis)
    choices: List[List[Sigma]] = []
    for row in prefs:
        if use_ties:
            choices.append([tuple(s) for s in row["tied_sigmas"]])  # type: ignore[misc]
        else:
            choices.append([tuple(row["preferred"])])  # type: ignore[list-item]
    realized = realize_preferred(closed, choices)
    ker = left_kernel_basis(B)
    return {
        "n_triads": len(closed),
        "n_modes": len(modes),
        "dim_ker_BT": len(ker),
        "tree_combinatorial": len(ker) == 0,
        "preferred": prefs,
        "realized": (
            {str(m): s for m, s in realized.items()} if realized is not None else None
        ),
        "preferred_realizable": realized is not None,
        "static_loop_defect": bool(ker) and realized is None,
        "local_hub_conflict": (not ker) and realized is None,
        "reading": (
            "preferred helicity state is globally realizable: "
            "no static polarization holonomy on this family"
            if realized is not None
            else (
                "preferred triples conflict, but ker B^T = 0: this is a "
                "local hub / star conflict, not a loop holonomy. Stars can "
                "still realize some (not necessarily independently preferred) "
                "transverse collection."
                if not ker
                else "preferred helicity state cannot be realized on a genuine "
                "cycle: polarization holonomy on this family"
            )
        ),
        "axis": tuple(axis),
    }


def transport_around_cycle(
    triads: Sequence[Triad],
    c: Sequence[int],
    prefs: Sequence[dict],
) -> dict:
    """Walk the signed cycle and record the helicity forced at each visit.

    A mode that is assigned twice with opposite helicity by the
    preferred triples is a transported flip.
    """
    visits: Dict[Mode, List[int]] = {}
    for e, w in enumerate(c):
        if w == 0:
            continue
        p, q, k = triads[e]
        sig = prefs[e]["preferred"]
        for mode, s in ((p, sig[0]), (q, sig[1]), (k, sig[2])):
            visits.setdefault(mode, []).append(int(s) * (1 if w > 0 else 1))
    flips = []
    for mode, vals in visits.items():
        if any(v != vals[0] for v in vals):
            flips.append({"mode": mode, "helicities": vals})
    return {
        "visits": {str(m): v for m, v in visits.items()},
        "flips": flips,
        "returns_rotated": bool(flips),
    }


def star_polarization() -> dict:
    test = polarization_test(STAR_WITNESS)
    return {
        "family": "two_triad_star_witness",
        "test": test,
        "lock": (
            "Stars can. The archive witness is already one globally "
            "compatible real field. A star is not a polarization loop."
        ),
    }


def parallelogram_polarization() -> dict:
    closed, _, B = incidence_matrix(PARALLELOGRAM)
    tests = []
    for ax in AXES:
        t = polarization_test(PARALLELOGRAM, axis=ax)
        prefs = preferred_assignments(closed, ax)
        walk = transport_around_cycle(closed, [1, -1, 1, -1], prefs)
        tests.append({"axis": ax, "test": t, "transport": walk})
    any_defect = any(row["test"]["static_loop_defect"] for row in tests)
    any_flip = any(row["transport"]["returns_rotated"] for row in tests)
    invariant_defect = all(row["test"]["static_loop_defect"] == tests[0]["test"]["static_loop_defect"] for row in tests)
    return {
        "family": "parallelogram_4cycle",
        "per_axis": tests,
        "defect_on_some_frame": any_defect,
        "transport_flip_on_some_frame": any_flip,
        "defect_frame_invariant": invariant_defect,
        "reading": (
            "polarization holonomy is a static loop defect"
            if any_defect and invariant_defect
            else "no static polarization defect on this parallelogram"
            if not any_defect
            else "defect depends on the helical axis: treat as frame-sensitive, "
            "not a theorem"
        ),
    }
