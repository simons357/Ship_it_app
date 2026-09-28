"""NA-2B — exact cancellation / assembly unit test.

Relabel: this is not evidence about optimizer performance.
It checks that image points assemble and that incompatible
targets are certified by the integer left kernel.
"""

from __future__ import annotations

import math
from typing import Sequence

from ns_attacks.torus_p2 import (
    assemble_from_phases,
    left_kernel_primitive,
    torus_reachability,
)

TWOPI = 2.0 * math.pi


def exact_assembly(M: Sequence[Sequence[int]], theta: Sequence[float]) -> dict:
    """Forward assembly: b = M θ is reachable by construction."""
    b = assemble_from_phases(M, theta)
    cert = torus_reachability(M, b)
    return {
        "label": "NA-2B",
        "role": "exact cancellation/assembly unit test",
        "not_optimizer_evidence": True,
        "theta": [float(x) for x in theta],
        "b": b,
        "reachable": cert["reachable"],
        "r_cyc": cert["r_cyc"],
        "conditions": cert["conditions"],
        "pass": cert["reachable"] is True,
    }


def exact_incompatibility(
    M: Sequence[Sequence[int]],
    *,
    delta: float = 0.5 * math.pi,
) -> dict:
    """If r_cyc ≥ 1, a primitive generator c certifies a forbidden b.

    Take b = (δ / ||c||_∞) c  (supported on the cycle). Then
    c^T b = δ ||c||_2² / ||c||_∞ which is not a multiple of 2π
    for the small default δ. The kernel certificate is the test;
    no optimizer is run.
    """
    ker = left_kernel_primitive(M)
    if not ker:
        return {
            "label": "NA-2B",
            "role": "exact cancellation/assembly unit test",
            "not_optimizer_evidence": True,
            "tree": True,
            "pass": True,
            "note": "TREE: ker_Z M^T = {0}, every b is reachable. No incompatibility to certify.",
        }
    c = ker[0]
    ninf = max(abs(v) for v in c) or 1
    b = [float(delta) * float(v) / float(ninf) for v in c]
    cert = torus_reachability(M, b)
    pairing = cert["conditions"][0]["cTb_mod_2pi"]
    incompatible = not cert["reachable"]
    return {
        "label": "NA-2B",
        "role": "exact cancellation/assembly unit test",
        "not_optimizer_evidence": True,
        "primitive_c": c,
        "b": b,
        "cTb_mod_2pi": pairing,
        "reachable": cert["reachable"],
        "pass": incompatible,
        "note": (
            "incompatibility certified by ker_Z M^T, not by a local max"
            if incompatible
            else "FAIL: expected a kernel obstruction"
        ),
    }


def na2b_unit_report(M: Sequence[Sequence[int]], theta: Sequence[float]) -> dict:
    assembly = exact_assembly(M, theta)
    cancel = exact_incompatibility(M)
    return {
        "label": "NA-2B",
        "role": "exact cancellation/assembly unit test",
        "not_optimizer_evidence": True,
        "not_scale_rate": True,
        "assembly": assembly,
        "incompatibility": cancel,
        "pass": bool(assembly["pass"] and cancel["pass"]),
    }
