"""Finite checks for the 17/32 shared-budget family (handoff 7 Oct 2026).

Recomputes enumerations, dilation overlap witnesses, and displayed
weighted-charge arithmetic from the recovered-package faces.
Not a proof of the analytic inequalities in the audit PDF.

Standard library + numpy optional; this file uses stdlib only.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import isqrt, sqrt
from pathlib import Path
import json


# --- Exact lists from Shared-Budget package / Oct 7 handoff ---
FAMILY_5_25_THIRDS = [
    8, 10, 14, 18, 20, 22, 24, 26, 30,
    34, 36, 38, 40, 42, 46, 50, 52,
]
FAMILY_9_25_THIRDS_ALL = [
    4, 6, 10, 12, 14, 16, 24, 30, 34,
    38, 44, 52, 54, 56, 58, 62, 64,
]
FAMILY_9_25_ZERO_TRANSFER = [4, 64]
FAMILY_9_25_ACTIVE = [
    6, 10, 12, 14, 16, 24, 30, 34,
    38, 44, 52, 54, 56, 58, 62,
]

# Displayed faces from bundled script (handoff)
RHO = 0.6318550823987903
RHO_PRIME = 0.8253067330268596
RHO_PLUS_3_RHO_PRIME = 3.1077752814793693


def radius(k):
    return k[0] * k[0] + k[1] * k[1] + k[2] * k[2]


def lattice_shell(r2: int):
    R = isqrt(r2) + 1
    return [
        (x, y, z)
        for x in range(-R, R + 1)
        for y in range(-R, R + 1)
        for z in range(-R, R + 1)
        if x * x + y * y + z * z == r2
    ]


def admits_triangle(a: int, b: int, c: int, shells=None) -> bool:
    sa, sb, sc = sqrt(a), sqrt(b), sqrt(c)
    if not (
        abs(sa - sb) <= sc <= sa + sb
        and abs(sa - sc) <= sb <= sa + sc
        and abs(sb - sc) <= sa <= sb + sc
    ):
        return False
    if shells is None:
        shells = {a: lattice_shell(a), b: lattice_shell(b), c: lattice_shell(c)}
    for p in shells[a]:
        for q in shells[b]:
            r = (-(p[0] + q[0]), -(p[1] + q[1]), -(p[2] + q[2]))
            if radius(r) == c:
                return True
    return False


def collinear_zero_transfer(a: int, b: int, c: int) -> bool:
    """Endpoints with (√a ± √c)² = b are collinear / zero area."""
    # b == (√a+√c)² or (√a-√c)²
    # Exact: b = a+c+2√(ac) or a+c-2√(ac) ⇒ (b-a-c)² = 4ac
    return (b - a - c) ** 2 == 4 * a * c


def dilation_charges_at(R: int, family_anchor: int, thirds: list[int]):
    """Charges: third-shell label b at dilation n with b*n² = R."""
    out = []
    for b in thirds:
        if R % b != 0:
            continue
        n2 = R // b
        n = isqrt(n2)
        if n * n == n2 and n >= 1:
            out.append({"family_anchor": family_anchor, "label": b, "n": n, "R": R})
    return out


def main():
    errors = []

    # List integrity
    assert len(FAMILY_5_25_THIRDS) == 17
    assert len(FAMILY_9_25_ACTIVE) == 15
    assert set(FAMILY_9_25_ACTIVE) == set(FAMILY_9_25_THIRDS_ALL) - set(
        FAMILY_9_25_ZERO_TRANSFER
    )
    assert len(FAMILY_5_25_THIRDS) + len(FAMILY_9_25_ACTIVE) == 32

    # Zero-transfer endpoints for (9,25)
    for b in FAMILY_9_25_ZERO_TRANSFER:
        if not collinear_zero_transfer(9, b, 25):
            errors.append(f"expected zero-transfer collinear (9,{b},25)")

    # Active thirds are NOT collinear endpoints
    for b in FAMILY_9_25_ACTIVE:
        if collinear_zero_transfer(9, b, 25):
            errors.append(f"active label {b} is collinear zero-transfer")

    # Existence of integer triangles for listed shapes (finite)
    shells_needed = {5, 9, 25} | set(FAMILY_5_25_THIRDS) | set(FAMILY_9_25_THIRDS_ALL)
    shells = {r: lattice_shell(r) for r in sorted(shells_needed)}

    for b in FAMILY_5_25_THIRDS:
        if not admits_triangle(5, b, 25, shells):
            errors.append(f"missing triangle (5,{b},25)")
    for b in FAMILY_9_25_ACTIVE:
        if not admits_triangle(9, b, 25, shells):
            errors.append(f"missing triangle (9,{b},25)")

    # Overlap witness R=216 → multiplicity 4 (zero-pruned)
    charges_216 = dilation_charges_at(216, 5, FAMILY_5_25_THIRDS) + dilation_charges_at(
        216, 9, FAMILY_9_25_ACTIVE
    )
    expected_216 = {
        (5, 24, 3),
        (9, 6, 6),
        (9, 24, 3),
        (9, 54, 2),
    }
    got_216 = {(c["family_anchor"], c["label"], c["n"]) for c in charges_216}
    if got_216 != expected_216:
        errors.append(f"R=216 charges {got_216} != {expected_216}")
    multiplicity_216 = len(charges_216)

    # Literal combined multiplicity 6 at R=14400 (handoff)
    charges_14400 = dilation_charges_at(14400, 5, FAMILY_5_25_THIRDS) + dilation_charges_at(
        14400, 9, FAMILY_9_25_THIRDS_ALL  # literal includes zero-transfer labels if they hit
    )
    # Also count only active for comparison
    charges_14400_active = dilation_charges_at(
        14400, 5, FAMILY_5_25_THIRDS
    ) + dilation_charges_at(14400, 9, FAMILY_9_25_ACTIVE)

    # Weighted charge face
    weighted = RHO + 3 * RHO_PRIME
    if abs(weighted - RHO_PLUS_3_RHO_PRIME) > 1e-12:
        errors.append(f"ρ+3ρ' mismatch: {weighted} vs {RHO_PLUS_3_RHO_PRIME}")

    # Individual multiplicity 3: max over R of charges within one family
    def max_family_mult(anchor, thirds, Rmax_factor=80):
        # scan physical R = b n^2 for n<=Rmax_factor, b in thirds
        from collections import Counter

        ctr = Counter()
        for b in thirds:
            for n in range(1, Rmax_factor + 1):
                ctr[b * n * n] += 1
        return max(ctr.values()) if ctr else 0

    mult5 = max_family_mult(5, FAMILY_5_25_THIRDS)
    mult9 = max_family_mult(9, FAMILY_9_25_ACTIVE)

    payload = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "lists": {
            "family_5_25_thirds_n": len(FAMILY_5_25_THIRDS),
            "family_9_25_active_n": len(FAMILY_9_25_ACTIVE),
            "union_nonzero_shapes": 32,
            "family_5_25_thirds": FAMILY_5_25_THIRDS,
            "family_9_25_active": FAMILY_9_25_ACTIVE,
            "family_9_25_zero_transfer": FAMILY_9_25_ZERO_TRANSFER,
        },
        "constants_faces": {
            "rho": RHO,
            "rho_prime": RHO_PRIME,
            "rho_plus_3_rho_prime": RHO_PLUS_3_RHO_PRIME,
            "reconstruction_ok": abs(weighted - RHO_PLUS_3_RHO_PRIME) <= 1e-12,
        },
        "overlap": {
            "R_216_zero_pruned_multiplicity": multiplicity_216,
            "R_216_charges": sorted(
                charges_216, key=lambda c: (c["family_anchor"], c["label"], c["n"])
            ),
            "R_14400_literal_charge_count": len(charges_14400),
            "R_14400_active_charge_count": len(charges_14400_active),
            "R_14400_literal_charges": sorted(
                charges_14400, key=lambda c: (c["family_anchor"], c["label"], c["n"])
            ),
            "note": (
                "Combined literal multiplicity 6 and zero-pruned 4 are different "
                "accountings (handoff); both refer to specific definitions"
            ),
        },
        "individual_multiplicity_scan": {
            "family_5_max": mult5,
            "family_9_active_max": mult9,
            "handoff_claimed_individual": 3,
            "matches_handoff": mult5 == 3 and mult9 == 3,
        },
        "highpass_cutoff_formula": "K = max{2, 3(M-1)} for the combined family",
        "original_family_cutoff_note": (
            "Original smaller cutoff was max{2, √5 (M-1)} — a product, "
            "not √(5(M-1)); do not reuse for the extension without proof"
        ),
        "scope": (
            "Finite checks only. Restricted-family theorem remains "
            "source-backed at stated scope; not (17)."
        ),
    }

    out = Path(__file__).with_name("VERIFY-FAMILIES.json")
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
