"""MIN-CYCLE — canonical-input gated cycle test.

Acceptance is algebraic, not pictorial:

- TREE means r_cyc = 0.
- A genuine one-cycle closure is r_cyc : 0 → 1, with unique
  primitive c in ker_Z M^T.
- The one-cycle loss law is a prediction → measurement test.
- Finite-size incompatibility (ρ(H) < 1, or r_cyc ≥ 1) does
  not imply a scale-decaying defect. 0.15 is a convention,
  not a derived exponent. Scale-rate remains OPEN.

Canonical inputs are integer matrices. Pictures of triangles
are not an acceptance record.
"""

from __future__ import annotations

from typing import List

from ns_attacks.na2b_assembly import na2b_unit_report
from ns_attacks.one_cycle_loss import (
    heavy_one_cycle_test,
    prediction_measurement_test,
    quadratic_minimizer,
)
from ns_attacks.torus_p2 import (
    cycle_rank,
    integer_rank,
    is_tree,
    left_kernel_primitive,
    tree_to_loop_control,
)

# Canonical TREE: three independent channels on T^3.
CANONICAL_TREE: List[List[int]] = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
]

# Integer combination of the first two rows: no new independent phase.
TREE_TO_LOOP_COEFFS = [1, 1, 0]

# NS parallelogram incidence, mode order (P,Q,R,K,M,N).
# This is an integer matrix, not a drawing of a loop.
PARALLELOGRAM_M: List[List[int]] = [
    [1, 1, 0, -1, 0, 0],  # T1: P + Q - K
    [1, 0, 1, 0, -1, 0],  # T2: P + R - M
    [0, 0, 1, 1, 0, -1],  # T3: K + R - N
    [0, 1, 0, 0, 1, -1],  # T4: M + Q - N
]

# First three parallelogram rows: a TREE (rank 3, m = 3).
PARALLELOGRAM_TREE: List[List[int]] = PARALLELOGRAM_M[:3]
PARALLELOGRAM_LOOP_COEFFS = [1, -1, 1]  # T4 = T1 - T2 + T3


def algebraic_tree_to_loop() -> dict:
    """Positive control for MIN-CYCLE. Not 'looks like a loop'."""
    ctrl = tree_to_loop_control(CANONICAL_TREE, TREE_TO_LOOP_COEFFS)
    c = ctrl["primitive_c"]
    w = [1.0] * len(c)
    delta = 0.1
    loss = quadratic_minimizer(c, w, delta)
    pred = prediction_measurement_test(c, w, delta)
    heavy = heavy_one_cycle_test(c, w, delta)
    na2b = na2b_unit_report(ctrl["M_loop"], [0.3, -0.2, 0.1])
    return {
        "control": ctrl,
        "one_cycle_loss": loss,
        "prediction_measurement": pred,
        "heavy": {
            "stamp": heavy["stamp"],
            "pass_small_delta": heavy.get("pass_small_delta"),
            "pass_channels": heavy.get("pass_channels"),
            "pass_off_cycle": heavy.get("pass_off_cycle"),
            "one_minus_rho2": heavy["one_minus_rho2"],
            "one_minus_rho4": heavy["one_minus_rho4"],
            "measurement": heavy.get("measurement"),
            "principal_branch": heavy["exact"].get("principal_branch"),
        },
        "na2b": na2b,
        "accepted": (
            ctrl["r_cyc_before"] == 0
            and ctrl["r_cyc_after"] == 1
            and pred["pass_small_delta"]
            and heavy.get("pass_small_delta") is True
            and na2b["pass"]
        ),
    }


def parallelogram_tree_to_loop() -> dict:
    """Same control on the locked NS parallelogram incidence matrix.

    Adding T4 does not add an independent phase constraint: it is
    T1 - T2 + T3 over Z, so r_cyc : 0 → 1 with primitive
    c = (1, -1, 1, -1).
    """
    ctrl = tree_to_loop_control(PARALLELOGRAM_TREE, PARALLELOGRAM_LOOP_COEFFS)
    return ctrl


def min_cycle_acceptance() -> dict:
    """Gated acceptance record. Scale-rate is not accepted here."""
    alg = algebraic_tree_to_loop()
    par = parallelogram_tree_to_loop()
    tree_ok = is_tree(CANONICAL_TREE)
    loop_rank = integer_rank(par["M_loop"])
    return {
        "gate": "MIN-CYCLE",
        "canonical_input": "integer matrix M, not a picture of triangles",
        "tree_definition": "r_cyc = m - rank M; TREE iff r_cyc = 0",
        "one_cycle_definition": "r_cyc : 0 → 1 with rank_Z ker M^T = 1",
        "positive_control": alg["control"]["acceptance"],
        "parallelogram_control": par["acceptance"],
        "na2b_relabel": "exact cancellation/assembly unit test, not optimizer evidence",
        "one_cycle_loss_law": alg["prediction_measurement"]["boxed"],
        "one_cycle_quartic": "δ²/(2WS) − Q δ⁴/(24 W S⁴) + O(δ⁶)",
        "heavy_stamp": alg["heavy"]["stamp"],
        "heavy_channels": alg["heavy"]["pass_channels"],
        "exact_solver": "branch-enumerated; does not accept the first root",
        "torus_lemma": "standard / proved (Pontryagin duality; Smith form)",
        "finite_p2_compatibility": "exact integer algebra",
        "scale_rate_defect": "OPEN",
        "threshold_015": (
            "0.15 is a threshold/convention, not a derived exponent, "
            "until provenance establishes otherwise"
        ),
        "finite_size_does_not_imply_scale_decay": True,
        "rho_less_than_one_is_not_a_rate": True,
        "tree_ok": tree_ok,
        "parallelogram_loop_rank": loop_rank,
        "parallelogram_r_cyc": cycle_rank(par["M_loop"]),
        "parallelogram_c": par["primitive_c"],
        "algebraic_control_accepted": alg["accepted"],
        "na2b_pass": alg["na2b"]["pass"],
        "prediction_measurement_pass": alg["prediction_measurement"]["pass_small_delta"],
        "heavy_pass": alg["heavy"].get("pass_small_delta"),
        "ns_solved": False,
        "ker_tree": left_kernel_primitive(CANONICAL_TREE),
        "accepted_on_this_gate": bool(
            alg["accepted"]
            and par["r_cyc_after"] == 1
            and par["primitive_c"] in ([1, -1, 1, -1], [-1, 1, -1, 1])
        ),
        "not_accepted": [
            "scale-decaying defect",
            "derived exponent 0.15",
            "optimizer ρ < 1 as a rate",
            "Gate-C novelty for the torus lemma",
            "TREE/LOOP inferred from a drawing",
        ],
    }


def report() -> dict:
    return min_cycle_acceptance()
