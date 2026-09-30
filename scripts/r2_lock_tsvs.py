#!/usr/bin/env python3
"""Read-only verifier for the R2 synthetic TSV fixture.

`data/R2/M.tsv` and `data/R2/b_exact.tsv` are a synthetic fixture built
from the B42 integer-row identities and the B40 π/12 weak residues.
They are not the missing Library JSON
(SHA-256 87745b3cb585e138b6768ab5b9e330f3f045ff4d4ad82ba6f71f0b6fe86be898)
and they are not a canonical locked-r2 identity.

The default CLI only reads. It never writes the fixture. Classical
Navier–Stokes remains open.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
R2_DIR = ROOT / "data" / "R2"
M_TSV = R2_DIR / "M.tsv"
B_EXACT_TSV = R2_DIR / "b_exact.tsv"
PROVENANCE_JSON = R2_DIR / "PROVENANCE.json"

LIBRARY_JSON_SHA256 = (
    "87745b3cb585e138b6768ab5b9e330f3f045ff4d4ad82ba6f71f0b6fe86be898"
)

N_ROWS = 20
N_COLS = 12
K_ROWS = tuple(range(14))
J_ROWS = tuple(range(14, 20))

# Weak row = integer combination of strong rows (B42, zero-based).
WEAK_IDENTITIES: Dict[int, Dict[int, int]] = {
    14: {1: -1, 3: 1, 12: 1},
    15: {0: 1, 1: -1, 2: -1, 3: 1, 5: -1, 7: 1, 10: 1},
    16: {0: 1, 1: -1, 2: -1, 4: 1, 5: -1, 7: 1, 10: 1},
    17: {0: -1, 3: 1, 12: 1},
    18: {0: -1, 4: 1, 12: 1},
    19: {2: -1, 4: 1, 5: -1, 7: 1, 10: 1},
}

# Phase errors at the B40 certificate, rows 14–19, in units of π/12.
# Angle n·π/12 is the turn-fraction n/24.
PI12_ERRORS: Tuple[int, ...] = (20, -4, 16, 8, 4, 4)


def wrap01(x: Fraction) -> Fraction:
    return x - Fraction(x).numerator // Fraction(x).denominator


def pi12_to_turn(n: int) -> Fraction:
    return Fraction(n, 24)


def strong_rows() -> List[List[int]]:
    """Deterministic integer basis for rows 0–13.

    Rows 0–11 are the 12×12 identity. Row 12 is all ones (appears in
    identities 14, 17, 18). Row 13 alternates ±1 and is unused by the
    six identities; it is kept so the lock is a full 20×12 table.
    """
    rows = [[1 if c == r else 0 for c in range(N_COLS)] for r in range(N_COLS)]
    rows.append([1] * N_COLS)
    rows.append([1 if c % 2 == 0 else -1 for c in range(N_COLS)])
    assert len(rows) == 14
    return rows


def apply_identities(strong: Sequence[Sequence[int]]) -> List[List[int]]:
    M = [list(row) for row in strong]
    for j in J_ROWS:
        acc = [0] * N_COLS
        for i, a in WEAK_IDENTITIES[j].items():
            for c in range(N_COLS):
                acc[c] += a * M[i][c]
        M.append(acc)
    assert len(M) == N_ROWS
    return M


def build_M() -> List[List[int]]:
    return apply_identities(strong_rows())


def build_b_exact(M: Sequence[Sequence[int]]) -> List[Fraction]:
    """Exact rational target phases β_γ as fractions of a turn.

    Certificate y_A = 0. Strong rows then vanish when β_i = 0. Weak
    rows are set so {M_j y_A − β_j} equals the B40 π/12 residues.
    """
    y_A = [Fraction(0)] * N_COLS
    My = [sum(Fraction(M[r][c]) * y_A[c] for c in range(N_COLS)) for r in range(N_ROWS)]
    beta = [Fraction(0)] * N_ROWS
    for k, j in enumerate(J_ROWS):
        target = wrap01(pi12_to_turn(PI12_ERRORS[k]))
        # Want {My_j - beta_j} = target  ⇒  beta_j = My_j - target (mod 1).
        beta[j] = wrap01(My[j] - target)
    return beta


def load_tsv_matrix(path: Path) -> List[List[Fraction]]:
    rows: List[List[Fraction]] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.replace(",", "\t").split()
        rows.append([Fraction(p) for p in parts])
    return rows


def format_fraction(x: Fraction) -> str:
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def write_M_tsv(M: Sequence[Sequence[int]], path: Path = M_TSV) -> None:
    lines = [
        "# data/R2/M.tsv",
        "# SYNTHETIC FIXTURE — not Library JSON, not a canonical lock.",
        "# Integer 20×12 row matrix for the B42 T2-starvation quotient.",
        "# Tab-separated. Rows 0–13 strong (K); rows 14–19 weak (J).",
        "# Columns: phase coordinates y_0 … y_11.",
    ]
    for row in M:
        lines.append("\t".join(str(int(v)) for v in row))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def write_b_exact_tsv(beta: Sequence[Fraction], path: Path = B_EXACT_TSV) -> None:
    lines = [
        "# data/R2/b_exact.tsv",
        "# SYNTHETIC FIXTURE — not Library JSON, not a canonical lock.",
        "# Exact rational target phases β_γ as fractions of a turn.",
        "# One row per channel (20). Tab-separated, comments start with #.",
        "# Strong rows 0–13: 0 at certificate y_A = 0.",
        "# Weak rows 14–19: set so phase errors match (20,-4,16,8,4,4) π/12.",
    ]
    for value in beta:
        lines.append(format_fraction(value))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def write_provenance(M_path: Path = M_TSV, b_path: Path = B_EXACT_TSV) -> Dict[str, Any]:
    rec = {
        "folder": "data/R2",
        "files": {
            "M.tsv": "integer 20×12 row matrix",
            "b_exact.tsv": "exact rational target phases β_γ (turn fractions)",
        },
        "provenance": "synthetic_fixture",
        "verifier": "read-only",
        "not_library_json": True,
        "library_json_sha256_absent": LIBRARY_JSON_SHA256,
        "canonical_r2_identity": "unverified",
        "classical_NS": "open",
        "identities": {str(k): v for k, v in WEAK_IDENTITIES.items()},
        "pi12_errors_rows_14_19": list(PI12_ERRORS),
        "certificate_y_A": [0] * N_COLS,
        "strong_row_convention": (
            "rows 0-11 = I_12; row 12 = all ones; row 13 = alternating ±1"
        ),
        "sha256": {
            "M.tsv": sha256_file(M_path) if M_path.exists() else None,
            "b_exact.tsv": sha256_file(b_path) if b_path.exists() else None,
        },
    }
    PROVENANCE_JSON.write_text(json.dumps(rec, indent=2) + "\n")
    return rec


def check_identities(M: Sequence[Sequence[Any]]) -> Dict[str, Any]:
    if len(M) != N_ROWS or any(len(row) != N_COLS for row in M):
        return {
            "ok": False,
            "reason": f"expected shape (20, 12), got ({len(M)}, {len(M[0]) if M else 0})",
        }
    mismatches = []
    for j, coeffs in WEAK_IDENTITIES.items():
        pred = [Fraction(0)] * N_COLS
        for i, a in coeffs.items():
            for c in range(N_COLS):
                pred[c] += a * Fraction(M[i][c])
        got = [Fraction(M[j][c]) for c in range(N_COLS)]
        if pred != got:
            mismatches.append(
                {
                    "row": j,
                    "predicted": [format_fraction(x) for x in pred],
                    "got": [format_fraction(x) for x in got],
                }
            )
    return {"ok": not mismatches, "n_checked": 6, "mismatches": mismatches}


def check_weak_residues(
    M: Sequence[Sequence[Any]],
    beta: Sequence[Any],
    y: Sequence[Any] | None = None,
) -> Dict[str, Any]:
    if y is None:
        y = [Fraction(0)] * N_COLS
    residues = []
    expected = [wrap01(pi12_to_turn(n)) for n in PI12_ERRORS]
    for k, j in enumerate(J_ROWS):
        My = sum(Fraction(M[j][c]) * Fraction(y[c]) for c in range(N_COLS))
        err = wrap01(My - Fraction(beta[j]))
        residues.append(err)
    ok = residues == expected
    return {
        "ok": ok,
        "residues": [format_fraction(x) for x in residues],
        "expected": [format_fraction(x) for x in expected],
    }


def write_all() -> Dict[str, Any]:
    """Regenerate the synthetic fixture. Not used by the read-only CLI."""
    M = build_M()
    beta = build_b_exact(M)
    write_M_tsv(M)
    write_b_exact_tsv(beta)
    prov = write_provenance()
    loaded_M = load_tsv_matrix(M_TSV)
    loaded_b = [row[0] for row in load_tsv_matrix(B_EXACT_TSV)]
    ident = check_identities(loaded_M)
    residues = check_weak_residues(loaded_M, loaded_b)
    return {
        "wrote": [str(M_TSV.relative_to(ROOT)), str(B_EXACT_TSV.relative_to(ROOT))],
        "identities": ident,
        "weak_residues": residues,
        "provenance": prov,
    }


def verify() -> Dict[str, Any]:
    """Read-only check of the committed synthetic fixture. Does not write."""
    loaded_M = load_tsv_matrix(M_TSV)
    loaded_b = [row[0] for row in load_tsv_matrix(B_EXACT_TSV)]
    ident = check_identities(loaded_M)
    residues = check_weak_residues(loaded_M, loaded_b)
    provenance = None
    if PROVENANCE_JSON.is_file():
        provenance = json.loads(PROVENANCE_JSON.read_text())
    return {
        "read_only": True,
        "synthetic_fixture": True,
        "files": {
            "M.tsv": str(M_TSV.relative_to(ROOT)),
            "b_exact.tsv": str(B_EXACT_TSV.relative_to(ROOT)),
        },
        "identities": ident,
        "weak_residues": residues,
        "sha256": {
            "M.tsv": sha256_file(M_TSV),
            "b_exact.tsv": sha256_file(B_EXACT_TSV),
        },
        "provenance": provenance,
        "canonical_r2_identity": "unverified",
        "classical_NS": "open",
        "ok": bool(ident.get("ok") and residues.get("ok")),
    }


def main() -> None:
    rec = verify()
    print(json.dumps(
        {
            "read_only": rec["read_only"],
            "synthetic_fixture": rec["synthetic_fixture"],
            "identities_ok": rec["identities"]["ok"],
            "weak_residues_ok": rec["weak_residues"]["ok"],
            "canonical_r2_identity": rec["canonical_r2_identity"],
            "classical_NS": rec["classical_NS"],
            "ok": rec["ok"],
        },
        indent=2,
    ))


if __name__ == "__main__":
    main()
