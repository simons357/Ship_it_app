"""B42 — exact first-order coefficient on the T2 starvation ray.

Independent analysis of the rationalized 20-row quotient used in B41.
The six integer row identities and the certificate y_A live in a Library
JSON that is not in this checkout; they are checked when that JSON or
the locked TSV pair is present. Canonical locked-r2 identity and the
symmetrized coefficient convention remain unverified.

Classical Navier–Stokes remains open. This ray is not a trajectory,
not a drag reduction, and not a close.
"""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[2]

LIBRARY_JSON_SHA256 = (
    "87745b3cb585e138b6768ab5b9e330f3f045ff4d4ad82ba6f71f0b6fe86be898"
)

K_ROWS = tuple(range(14))
J_ROWS = tuple(range(14, 20))

# Integer identities: weak row = sum of integer coefficients times strong rows.
# Zero-based JSON row indices, as stated in B42.
WEAK_IDENTITIES: Dict[int, Dict[int, int]] = {
    14: {1: -1, 3: 1, 12: 1},
    15: {0: 1, 1: -1, 2: -1, 3: 1, 5: -1, 7: 1, 10: 1},
    16: {0: 1, 1: -1, 2: -1, 4: 1, 5: -1, 7: 1, 10: 1},
    17: {0: -1, 3: 1, 12: 1},
    18: {0: -1, 4: 1, 12: 1},
    19: {2: -1, 4: 1, 5: -1, 7: 1, 10: 1},
}

# Phase errors at the B40 certificate, in units of π/12, rows 14–19.
PI12_ERRORS: Tuple[int, ...] = (20, -4, 16, 8, 4, 4)

# Sprint 01 parallelogram (p+q=k), used only as a negative reconstruction check.
HETEROCHIRAL_SIGMA: Tuple[Tuple[int, int, int], ...] = (
    (1, 1, -1),
    (-1, -1, 1),
    (1, -1, 1),
    (-1, 1, -1),
    (-1, 1, 1),
    (1, -1, -1),
)
PARALLELOGRAM_PQK: Tuple[Tuple[str, Tuple[int, int, int], Tuple[int, int, int], Tuple[int, int, int]], ...] = (
    ("T1", (1, 0, 0), (0, 1, 0), (1, 1, 0)),
    ("T2", (1, 0, 0), (0, 0, 1), (1, 0, 1)),
    ("T3", (1, 1, 0), (0, 0, 1), (1, 1, 1)),
    ("T4", (1, 0, 1), (0, 1, 0), (1, 1, 1)),
)

SEARCH_ROOTS: Tuple[Path, ...] = (
    ROOT,
    ROOT / "data",
    ROOT / "data" / "b42",
    ROOT / "results",
    Path("/tmp"),
)


def d_phase(frac: float) -> float:
    """Deficit 1 − cos(2π θ) for a phase error θ modulo 1."""
    return 1.0 - math.cos(2.0 * math.pi * frac)


def wrap01(x: float) -> float:
    return float(x - math.floor(x))


def pi12_to_fraction(n: int) -> Fraction:
    """n units of π/12 as a fraction of a turn: angle 2π·(n/24)."""
    return Fraction(n, 24)


def cos_of_pi12(n: int) -> Fraction:
    """Exact cosine of n·π/12 for the six B42 residues.

    n is taken modulo 24. The B42 tuple (20,−4,16,8,4,4) lands on
    {4,8,16,20}, whose cosines are {±1/2}.
    """
    n_mod = int(n) % 24
    table = {
        4: Fraction(1, 2),
        8: Fraction(-1, 2),
        16: Fraction(-1, 2),
        20: Fraction(1, 2),
    }
    if n_mod not in table:
        raise ValueError(f"cosine table does not include n={n} (mod 24={n_mod})")
    return table[n_mod]


def weak_cosines() -> Tuple[Fraction, ...]:
    return tuple(cos_of_pi12(n) for n in PI12_ERRORS)


def weak_deficits() -> Tuple[Fraction, ...]:
    return tuple(1 - c for c in weak_cosines())


def D_A(C: Sequence[float]) -> float:
    """Upper/exact weak deficit at the B40 residues: [C14+C15+C18+C19+3(C16+C17)]/2."""
    C = list(C)
    if len(C) < 20:
        raise ValueError("need 20 channel coefficients")
    return 0.5 * (
        C[14] + C[15] + C[18] + C[19] + 3.0 * (C[16] + C[17])
    )


def D_A_from_deficits(C: Sequence[float]) -> float:
    defs = weak_deficits()
    return float(sum(Fraction(str(C[14 + i])) * defs[i] for i in range(6)))


def F_15_16(C15: float, C16: float) -> float:
    """Two-row four-cycle lower bound, relative phase π/3."""
    if C15 <= 0.0 or C16 <= 0.0:
        raise ValueError("need positive C15, C16")
    return C15 + C16 - math.sqrt(C15 * C15 + C16 * C16 + C15 * C16)


def two_row_min_numeric(C15: float, C16: float, n: int = 20000) -> float:
    """Grid minimum of C15(1−cos θ)+C16(1−cos(θ+π/3))."""
    thetas = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    vals = C15 * (1.0 - np.cos(thetas)) + C16 * (1.0 - np.cos(thetas + math.pi / 3.0))
    return float(np.min(vals))


def check_identities(M: np.ndarray) -> Dict[str, Any]:
    """Direct integer arithmetic: each weak row equals the stated Z-combination."""
    M = np.asarray(M, dtype=object)
    if M.shape != (20, 12):
        return {
            "ok": False,
            "reason": f"expected shape (20, 12), got {tuple(M.shape)}",
        }
    mismatches = []
    for j, coeffs in WEAK_IDENTITIES.items():
        pred = np.zeros(12, dtype=object)
        for i, a in coeffs.items():
            pred = pred + a * M[i]
        got = M[j]
        if any(pred[c] != got[c] for c in range(12)):
            mismatches.append(
                {
                    "row": j,
                    "predicted": [int(x) for x in pred],
                    "got": [int(x) for x in got],
                }
            )
    return {
        "ok": not mismatches,
        "n_checked": 6,
        "mismatches": mismatches,
    }


def weak_residue_mod1(
    identity: Mapping[int, int],
    beta: Sequence[float],
    weak_index: int,
) -> float:
    """On Z_K, M_j y ≡ Σ a_i β_i (mod 1). Residue of the weak phase error is
    {Σ a_i β_i − β_j}."""
    s = 0.0
    for i, a in identity.items():
        s += a * float(beta[i])
    return wrap01(s - float(beta[weak_index]))


def synthetic_matrix(seed: int = 42) -> np.ndarray:
    """A 20×12 integer matrix that obeys the six identities by construction."""
    rng = np.random.default_rng(seed)
    M = np.zeros((20, 12), dtype=int)
    M[:14] = rng.integers(-2, 3, size=(14, 12))
    for j, coeffs in WEAK_IDENTITIES.items():
        acc = np.zeros(12, dtype=int)
        for i, a in coeffs.items():
            acc = acc + a * M[i]
        M[j] = acc
    return M


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _looks_like_20x12(arr: Any) -> bool:
    try:
        A = np.asarray(arr)
    except Exception:
        return False
    return A.ndim == 2 and A.shape == (20, 12)


def extract_20x12(obj: Any) -> Optional[np.ndarray]:
    """Walk a JSON-like object for a 20×12 array."""
    if _looks_like_20x12(obj):
        return np.asarray(obj)
    if isinstance(obj, dict):
        for key in (
            "M",
            "m",
            "matrix",
            "rows",
            "quotient",
            "M_rationalized",
            "M20",
        ):
            if key in obj and _looks_like_20x12(obj[key]):
                return np.asarray(obj[key])
        for v in obj.values():
            found = extract_20x12(v)
            if found is not None:
                return found
    if isinstance(obj, list) and obj and isinstance(obj[0], dict):
        for item in obj:
            found = extract_20x12(item)
            if found is not None:
                return found
    return None


def find_hashed_library(roots: Iterable[Path] = SEARCH_ROOTS) -> Dict[str, Any]:
    hits = []
    scanned = 0
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".json", ".JSON"}:
                continue
            if path.stat().st_size > 50_000_000:
                continue
            scanned += 1
            digest = sha256_file(path)
            if digest == LIBRARY_JSON_SHA256:
                hits.append(str(path))
    return {
        "sha256": LIBRARY_JSON_SHA256,
        "found": bool(hits),
        "paths": hits,
        "json_files_scanned": scanned,
    }


def find_locked_tsvs(roots: Iterable[Path] = SEARCH_ROOTS) -> Dict[str, Any]:
    names = {"M.tsv": None, "b_exact.tsv": None}
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.name in names and path.is_file():
                names[path.name] = str(path)
    return {
        "M_tsv": names["M.tsv"],
        "b_exact_tsv": names["b_exact.tsv"],
        "both_present": names["M.tsv"] is not None and names["b_exact.tsv"] is not None,
    }


def load_tsv_matrix(path: Path) -> np.ndarray:
    rows = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.replace(",", "\t").split()
        rows.append([Fraction(p) for p in parts])
    return np.array(rows, dtype=object)


def odd_leg(sigma: Sequence[int]) -> str:
    sk, sp, sq = (int(sigma[0]), int(sigma[1]), int(sigma[2]))
    if sk != sp and sk != sq:
        return "k"
    if sp != sk and sp != sq:
        return "p"
    return "q"


def parallelogram_helicity_20x12() -> np.ndarray:
    """20 live channels: drop T1/T2 odd-k Vandermonde zeros. Columns = (mode, ±)."""
    names = ["P", "Q", "R", "K", "M", "N"]
    cols = [(n, s) for n in names for s in (1, -1)]
    name_of = {
        (1, 0, 0): "P",
        (0, 1, 0): "Q",
        (0, 0, 1): "R",
        (1, 1, 0): "K",
        (1, 0, 1): "M",
        (1, 1, 1): "N",
    }
    rows = []
    for tname, p, q, k in PARALLELOGRAM_PQK:
        kn, pn, qn = name_of[k], name_of[p], name_of[q]
        for sig in HETEROCHIRAL_SIGMA:
            if tname in ("T1", "T2") and odd_leg(sig) == "k":
                continue
            r = [0] * 12
            for name, s in zip((kn, pn, qn), sig):
                r[cols.index((name, int(s)))] += 1
            rows.append(r)
    return np.array(rows, dtype=int)


def first_order_numeric(
    t_values: Sequence[float] = (1e-2, 1e-3, 1e-4, 1e-5),
    n_grid: int = 4001,
) -> Dict[str, Any]:
    """Synthetic 1-D check of lim_{t↓0} (1−Γ(t))/t = m_J / C_K.

    F_K(y)=1−cos(2π y) vanishes at y=0, F_J(y)=1−cos(2π(y−1/6)),
    so m_J = 1−cos(π/3)=1/2. Coefficients C_K=3, C_2=2.
    """
    C_K = 3.0
    C_2 = 2.0
    # Cluster at the unique Z_K point y=0: the minimizer is O(t).
    near = np.linspace(-0.02, 0.02, n_grid)
    y = np.mod(near, 1.0)
    F_K = 1.0 - np.cos(2.0 * np.pi * y)
    F_J = 1.0 - np.cos(2.0 * np.pi * (y - 1.0 / 6.0))
    m_J = 1.0 - math.cos(math.pi / 3.0)
    target = m_J / C_K
    samples = []
    for t in t_values:
        num = F_K + t * F_J
        gamma_def = float(np.min(num) / (C_K + t * C_2))
        samples.append(
            {
                "t": t,
                "deficit": gamma_def,
                "deficit_over_t": gamma_def / t,
                "abs_err_to_target": abs(gamma_def / t - target),
            }
        )
    return {
        "m_J": m_J,
        "C_K": C_K,
        "C_2": C_2,
        "target": target,
        "samples": samples,
        "max_abs_err_smallest_t": samples[-1]["abs_err_to_target"],
        "ok": samples[-1]["abs_err_to_target"] < 5e-4,
    }


def four_cycle_relative_phase() -> Dict[str, Any]:
    """Exact min of two cosine deficits with relative angle π/3."""
    checks = []
    for C15, C16 in ((1.0, 1.0), (2.0, 1.0), (5.0, 3.0), (math.pi, math.e)):
        exact = F_15_16(C15, C16)
        numeric = two_row_min_numeric(C15, C16)
        checks.append(
            {
                "C15": C15,
                "C16": C16,
                "exact": exact,
                "numeric": numeric,
                "abs_err": abs(exact - numeric),
                "positive": exact > 0.0,
            }
        )
    return {
        "formula": "C15+C16-sqrt(C15^2+C16^2+C15 C16)",
        "relative_phase": "pi/3",
        "checks": checks,
        "ok": all(c["abs_err"] < 1e-6 and c["positive"] for c in checks),
    }


def cosine_and_DA_check() -> Dict[str, Any]:
    cosines = [float(c) for c in weak_cosines()]
    defs = [float(d) for d in weak_deficits()]
    expected_cos = [0.5, 0.5, -0.5, -0.5, 0.5, 0.5]
    expected_def = [0.5, 0.5, 1.5, 1.5, 0.5, 0.5]
    C = [float(i + 1) for i in range(20)]
    da = D_A(C)
    da_from_def = D_A_from_deficits(C)
    lower = F_15_16(C[15], C[16])
    return {
        "pi12_errors": list(PI12_ERRORS),
        "cosines": cosines,
        "deficits": defs,
        "cosines_match": cosines == expected_cos,
        "deficits_match": defs == expected_def,
        "D_A": da,
        "D_A_from_deficits": da_from_def,
        "D_A_agrees": abs(da - da_from_def) < 1e-12,
        "two_row_lower": lower,
        "exact_strictly_above_two_row": da > lower,
        "ok": (
            cosines == expected_cos
            and abs(da - da_from_def) < 1e-12
            and da > lower
        ),
    }


def identity_implication_check() -> Dict[str, Any]:
    """Integer identities pin weak phases on Z_K; F_J is then constantly D_A."""
    M = synthetic_matrix()
    ident = check_identities(M)
    y = np.array(
        [0.0, 1 / 24, 2 / 24, 5 / 24, 7 / 24, 0.1, 0.3, 0.4, 0.7, 1 / 3, 5 / 8, 11 / 12]
    )
    beta = np.array([wrap01(float(M[i] @ y)) for i in range(20)])
    # Strong rows vanish at y by construction of beta.
    strong_ok = all(
        abs(d_phase(wrap01(float(M[i] @ y) - beta[i]))) < 1e-12 for i in K_ROWS
    )
    residues = [
        wrap01(float(M[j] @ y) - beta[j]) for j in J_ROWS
    ]
    from_id = [
        weak_residue_mod1(WEAK_IDENTITIES[j], beta, j) for j in J_ROWS
    ]
    # Shift beta_J so residues equal the B42 π/12 errors, then F_J = D_A.
    target_frac = [float(pi12_to_fraction(n) % 1) for n in PI12_ERRORS]
    beta_adj = beta.copy()
    for k, j in enumerate(J_ROWS):
        # Want {M_j y - beta_j} = target_frac[k]
        beta_adj[j] = wrap01(float(M[j] @ y) - target_frac[k])
    C = np.ones(20)
    F_J = sum(
        C[j] * d_phase(wrap01(float(M[j] @ y) - beta_adj[j])) for j in J_ROWS
    )
    return {
        "identities_on_synthetic_M": ident["ok"],
        "Z_K_nonempty_by_construction": strong_ok,
        "residues_match_identity": all(
            min(abs(wrap01(a - b)), 1.0 - abs(wrap01(a - b))) < 1e-12
            for a, b in zip(residues, from_id)
        ),
        "F_J_at_certificate": F_J,
        "D_A": D_A(C),
        "F_J_equals_D_A": abs(F_J - D_A(C)) < 1e-12,
        "ok": ident["ok"]
        and strong_ok
        and abs(F_J - D_A(C)) < 1e-12
        and all(
            min(abs(wrap01(a - b)), 1.0 - abs(wrap01(a - b))) < 1e-12
            for a, b in zip(residues, from_id)
        ),
    }


def parallelogram_reconstruction_check() -> Dict[str, Any]:
    M = parallelogram_helicity_20x12()
    ident = check_identities(M)
    return {
        "shape": list(M.shape),
        "convention": (
            "Sprint 01 parallelogram p+q=k, 6 heterochiral σ, "
            "drop T1/T2 odd-k Vandermonde zeros, columns=(mode,helicity), "
            "K=T1 live+T2 live+T3, J=T4"
        ),
        "identities_hold": ident["ok"],
        "mismatches": ident.get("mismatches", []),
        "note": (
            "A natural 20-row live parallelogram quotient does not reproduce "
            "the six JSON identities. Do not identify that incidence with the "
            "Library JSON until the hashed file or locked TSVs are compared."
        ),
    }


def lock_status() -> Dict[str, Any]:
    lib = find_hashed_library()
    tsv = find_locked_tsvs()
    matrix_check: Dict[str, Any] = {
        "performed": False,
        "ok": False,
        "reason": "Library JSON and locked TSVs are absent from this checkout",
    }
    if lib["found"]:
        path = Path(lib["paths"][0])
        try:
            obj = json.loads(path.read_text())
            M = extract_20x12(obj)
            if M is None:
                matrix_check = {
                    "performed": True,
                    "ok": False,
                    "reason": f"hashed JSON at {path} has no 20×12 array",
                }
            else:
                ident = check_identities(np.rint(np.asarray(M, dtype=float)).astype(int))
                matrix_check = {
                    "performed": True,
                    "ok": ident["ok"],
                    "source": str(path),
                    "identities": ident,
                }
        except Exception as exc:  # noqa: BLE001 — report, do not crash the packet
            matrix_check = {
                "performed": True,
                "ok": False,
                "reason": f"failed to parse hashed JSON: {exc}",
            }
    if tsv["both_present"] and not matrix_check.get("ok"):
        try:
            M = load_tsv_matrix(Path(tsv["M_tsv"]))
            ident = check_identities(M)
            matrix_check = {
                "performed": True,
                "ok": ident["ok"],
                "source": tsv["M_tsv"],
                "identities": ident,
                "b_exact": tsv["b_exact_tsv"],
            }
        except Exception as exc:  # noqa: BLE001
            matrix_check = {
                "performed": True,
                "ok": False,
                "reason": f"failed to read locked TSVs: {exc}",
            }
    return {
        "library_json": lib,
        "locked_tsvs": tsv,
        "matrix_row_check": matrix_check,
        "canonical_r2_identity": "unverified",
        "symmetrized_coefficient_convention": "unverified",
        "classical_NS": "open",
    }


def run_report() -> Dict[str, Any]:
    analysis = first_order_numeric()
    two_row = four_cycle_relative_phase()
    da = cosine_and_DA_check()
    impl = identity_implication_check()
    para = parallelogram_reconstruction_check()
    locks = lock_status()
    independent_ok = (
        analysis["ok"] and two_row["ok"] and da["ok"] and impl["ok"]
    )
    json_identities_ok = bool(locks["matrix_row_check"].get("ok"))
    return {
        "note": "B42",
        "date": "2026-09-29",
        "title": "Exact first-order capacity coefficient on the T2 starvation ray",
        "limit": "lim_{t↓0} (1−Γ(t))/t = m_J(C)/C_K",
        "exact_coefficient_if_identities_and_yA": "D_A/C_K",
        "D_A": "[C_14+C_15+C_18+C_19+3(C_16+C_17)]/2",
        "independent_analysis": {
            "first_order_limit_synthetic": analysis,
            "four_cycle_two_row_bound": two_row,
            "cosine_and_D_A": da,
            "identity_implication_on_synthetic_M": impl,
            "ok": independent_ok,
        },
        "json_row_identities": {
            "claimed": {str(k): v for k, v in WEAK_IDENTITIES.items()},
            "library_sha256": LIBRARY_JSON_SHA256,
            "verified_on_hashed_json_or_locked_tsv": json_identities_ok,
        },
        "parallelogram_reconstruction": para,
        "lock_status": locks,
        "scope": {
            "fixed_positive_channel_coefficients": True,
            "one_instantaneous_amplitude_ray": True,
            "rationalized_JSON_quotient": True,
            "trajectory_follows_the_ray": False,
            "drag_reduction": False,
            "classical_NS_closed": False,
            "canonical_r2_identity": False,
        },
        "all_independent_checks_ok": independent_ok,
        "canonical_statement_ready": False,
        "not_a_close": True,
    }


def main() -> None:
    report = run_report()
    out = ROOT / "results" / "b42_t2_starvation_coefficient.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, default=str) + "\n")
    print(json.dumps({k: report[k] for k in (
        "note",
        "title",
        "all_independent_checks_ok",
        "canonical_statement_ready",
        "not_a_close",
    )}, indent=2))
    print("wrote", out)


if __name__ == "__main__":
    main()
