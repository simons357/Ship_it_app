#!/usr/bin/env python3
"""B41 phase-convention audit: four π-offset targets vs generator / lock.

Exact Fraction arithmetic on data/R2 (G3 computed-evidence pair).

Does **not** claim G6-A transfer, DA stamp, or classical NS regularity.
Re-run: python3 scripts/b41_phase_convention_audit.py
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from r2_lock_tsvs import (  # noqa: E402
    WEAK_IDENTITIES,
    load_tsv_matrix,
    sha256_file,
    wrap01,
)

R2 = ROOT / "data" / "R2"
OUT_DIR = ROOT / "results" / "b41"
ART_DIR = Path("/opt/cursor/artifacts")

# Rows where G3 turn = -1/2 and the Exact-Certificate / lock comparison stores 0.
PI_OFFSET_ROWS: Tuple[int, ...] = (0, 5, 10, 11)


def _rref(
    A: List[List[Fraction]], rhs: List[Fraction]
) -> Tuple[List[List[Fraction]], List[Fraction], List[Tuple[int, int]]]:
    A = [row[:] for row in A]
    rhs = list(rhs)
    m, n = len(A), len(A[0])
    row = 0
    pivots: List[Tuple[int, int]] = []
    for col in range(n):
        piv = None
        for r in range(row, m):
            if A[r][col] != 0:
                piv = r
                break
        if piv is None:
            continue
        A[row], A[piv] = A[piv], A[row]
        rhs[row], rhs[piv] = rhs[piv], rhs[row]
        pv = A[row][col]
        A[row] = [x / pv for x in A[row]]
        rhs[row] /= pv
        for r in range(m):
            if r == row:
                continue
            fac = A[r][col]
            if fac == 0:
                continue
            A[r] = [A[r][c] - fac * A[row][c] for c in range(n)]
            rhs[r] -= fac * rhs[row]
        pivots.append((row, col))
        row += 1
        if row == m:
            break
    return A, rhs, pivots


def solvable_mod1(
    M: Sequence[Sequence[int]], delta: Sequence[Fraction]
) -> Dict[str, object]:
    Ar, rr, pivs = _rref(
        [[Fraction(M[r][c]) for c in range(12)] for r in range(20)],
        list(delta),
    )
    inconsistent = [
        {"row": r, "rhs": str(rr[r])}
        for r in range(20)
        if all(Ar[r][c] == 0 for c in range(12)) and wrap01(rr[r]) != 0
    ]
    free = sorted(set(range(12)) - {c for _, c in pivs})
    y = [Fraction(0)] * 12
    for prow, pcol in pivs:
        val = rr[prow]
        for c in free:
            val -= Ar[prow][c] * y[c]
        y[pcol] = val
    My = [sum(Fraction(M[r][c]) * y[c] for c in range(12)) for r in range(20)]
    ok = (not inconsistent) and all(
        wrap01(My[r] - delta[r]) == 0 for r in range(20)
    )
    return {
        "solvable_mod1": ok,
        "inconsistent_rows": inconsistent,
        "particular_y": [str(v) for v in y],
        "pivots": [{"row": r, "col": c} for r, c in pivs],
        "free_cols": free,
    }


def check_identities(M: Sequence[Sequence[int]]) -> bool:
    for j, coeffs in WEAK_IDENTITIES.items():
        acc = [0] * 12
        for i, a in coeffs.items():
            for c in range(12):
                acc[c] += a * int(M[i][c])
        if acc != [int(x) for x in M[j]]:
            return False
    return True


def main() -> None:
    M = [[int(x) for x in row] for row in load_tsv_matrix(R2 / "M.tsv")]
    b_g3 = [row[0] for row in load_tsv_matrix(R2 / "b_exact.tsv")]
    js = json.loads((R2 / "g3_corrected_channel_quotient.json").read_text())
    labels = [g.get("labels") for g in js["Gamma"]]

    assert check_identities(M)

    # Identify exact half-turn G3 targets.
    half_turn_rows = [
        i for i, b in enumerate(b_g3) if wrap01(b) == Fraction(1, 2) or b == Fraction(-1, 2)
    ]
    assert tuple(half_turn_rows) == PI_OFFSET_ROWS
    for i in PI_OFFSET_ROWS:
        assert b_g3[i] == Fraction(-1, 2)

    # Lock-side comparison used by Exact-Certificate (Reported): same β as G3
    # except those four rows store 0 instead of -1/2.
    b_lock = list(b_g3)
    for i in PI_OFFSET_ROWS:
        b_lock[i] = Fraction(0)

    delta_strong_only = [wrap01(b_g3[i] - b_lock[i]) for i in range(20)]
    assert all(
        (delta_strong_only[i] == Fraction(1, 2)) == (i in PI_OFFSET_ROWS)
        for i in range(20)
    )

    # A) Strong-only π map — audit case (weak targets held fixed).
    abs_A = solvable_mod1(M, delta_strong_only)

    # B) Identity-consistent extension of the same strong Δβ onto weak rows.
    delta_id = list(delta_strong_only)
    for j, coeffs in WEAK_IDENTITIES.items():
        delta_id[j] = wrap01(sum(a * delta_id[i] for i, a in coeffs.items()))
    abs_B = solvable_mod1(M, delta_id)

    # Global convention probes on G3 β (compare to lock reconstruction).
    def mismatches(b_try: Sequence[Fraction]) -> List[int]:
        return [i for i in range(20) if wrap01(b_try[i] - b_lock[i]) != 0]

    conj = [wrap01(-b) for b in b_g3]
    global_pi = [wrap01(b + Fraction(1, 2)) for b in b_g3]
    local_pi = list(b_g3)
    for i in PI_OFFSET_ROWS:
        local_pi[i] = wrap01(local_pi[i] + Fraction(1, 2))
        assert local_pi[i] == 0

    # Frozen weak-error shift on Z_K if strong β get +π and weak β stay put.
    weak_error_shift = {}
    for j, coeffs in WEAK_IDENTITIES.items():
        shift = wrap01(
            sum(a * Fraction(1, 2) for i, a in coeffs.items() if i in PI_OFFSET_ROWS)
        )
        weak_error_shift[str(j)] = str(shift)

    generator_notes = js.get("notes", [])

    payload = {
        "status_labels": {
            "rerun": "arithmetic in this script",
            "source_backed": "G3 JSON notes; data/R2 PROVENANCE; Exact-Certificate report in parent chat",
            "reported": "y_A, y_B, cycles, six T2 errors PASS vs rationalized JSON",
            "open": "Library JSON 87745…; Exact-Certificate ZIP bytes not in this checkout",
        },
        "artifacts": {
            "M.tsv_sha256": sha256_file(R2 / "M.tsv"),
            "b_exact.tsv_sha256": sha256_file(R2 / "b_exact.tsv"),
            "g3_json_sha256": sha256_file(R2 / "g3_corrected_channel_quotient.json"),
            "note": (
                "These hashes are the G3 transcription locks in PROVENANCE.json "
                "(COMPUTED_EVIDENCE_ONLY), not the absent Library JSON."
            ),
        },
        "generator_convention": {
            "formula": "b = π/2 - arg(g_sym), g_sym = g_ord(p,q) + g_ord(q,p)",
            "json_notes": generator_notes,
            "equivalent_local_flip": (
                "arg(-g_sym) = arg(g_sym)+π ⇒ b ← b-π ≡ b+π (mod 2π) "
                "on a channel whose g_sym sign is flipped"
            ),
        },
        "four_pi_offset_targets": [
            {
                "row": i,
                "labels": labels[i],
                "triads": js["Gamma"][i].get("triads"),
                "g3_turn": str(b_g3[i]),
                "g3_radians": "−π",
                "lock_turn": "0",
                "difference": "π",
            }
            for i in PI_OFFSET_ROWS
        ],
        "global_convention_probes": {
            "conjugation_beta_to_minus_beta_mismatches": mismatches(conj),
            "global_plus_pi_mismatches": mismatches(global_pi),
            "local_plus_pi_on_four_mismatches": mismatches(local_pi),
        },
        "mode_phase_absorption": {
            "A_strong_only_delta": {
                "description": (
                    "Δβ = 1/2 turn on rows 0,5,10,11 only; weak Δβ = 0. "
                    "This is the Exact-Certificate comparison shape."
                ),
                "delta_turns": [str(x) for x in delta_strong_only],
                **abs_A,
            },
            "B_identity_consistent_delta": {
                "description": (
                    "Same strong Δβ, weak Δβ forced by WEAK_IDENTITIES. "
                    "Would be a pure mode-phase gauge — but the generator "
                    "assigns weak targets from their own g_sym, and the audit "
                    "held weak targets fixed."
                ),
                "delta_turns": [str(x) for x in delta_id],
                **abs_B,
            },
        },
        "weak_T2_error_shift_if_strong_only_map": weak_error_shift,
        "identities_on_disk_M": True,
        "classification": {
            "code": "hybrid_a_local_generator_b_blocks_G6A",
            "summary": (
                "(Local generator) The four offsets equal sign(g_sym) flips under "
                "b=π/2−arg(g_sym). (Not global) Conjugation and global +π do not "
                "reproduce the lock match. (Not mode-phase gauge) Strong-only Δβ "
                "is inconsistent mod 1 on weak rows 15–18. Therefore G6-A cannot "
                "transfer through an asserted raw r2 identity."
            ),
        },
        "g6a_transfer": {
            "via_raw_r2_identity": False,
            "via_strong_only_local_bridge": False,
            "via_identity_consistent_gauge": (
                "Would equate β systems by a mode-phase, but that is not the "
                "audit mismatch (weak targets were not remapped), and it is not "
                "how the G3 generator writes weak b."
            ),
            "scope": (
                "Fixed finite network only. Evolving NSE / classical regularity: Open."
            ),
        },
        "certificate_posture": {
            "y_A_y_B_cycles_T2_vs_JSON": "Reported PASS (Exact-Certificate conversation)",
            "same_y_under_strong_only_mapped_beta": (
                "Fails on the four rows: residual picks up 1/2 turn"
            ),
            "T2_frozen_errors_under_strong_only_map": (
                "Shift by the weak_T2_error_shift table on Z_K; upper-bound "
                "residues are not automatically preserved"
            ),
        },
        "sibling_pr": {
            "number": 169,
            "branch": "cursor/b41-phase-convention-0cc5",
            "agreement": "Same four rows and local +π / sign(g_sym) story",
            "this_branch_adds": (
                "Exact mod-1 obstruction for strong-only absorption; "
                "identity-consistent gauge contrast; global-map negatives"
            ),
        },
        "ns_regularity": "open",
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ART_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "phase_convention_audit.json"
    out.write_text(json.dumps(payload, indent=2) + "\n")
    art = ART_DIR / "b41_phase_convention_audit.json"
    art.write_text(json.dumps(payload, indent=2) + "\n")

    # Hard asserts for CI/local rerun
    assert abs_A["solvable_mod1"] is False
    assert abs_A["inconsistent_rows"], "expected weak-row obstruction"
    assert abs_B["solvable_mod1"] is True
    assert mismatches(local_pi) == []
    assert mismatches(conj) != []
    assert mismatches(global_pi) != []

    print(json.dumps(payload, indent=2))
    print(f"wrote {out}")
    print(f"wrote {art}")


if __name__ == "__main__":
    main()
