"""Algebra lock of the recovered Gate-5 polynomials.

Does not define u, m, d. Does not search the danger chamber.
Does not reopen the Gate roadmap. NS is not solved.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


def C0(u: Fraction, m: Fraction) -> Fraction:
    bracket = (
        m**4
        + 2 * m**3 * u
        + 4 * m**3
        + m**2 * u**2
        + 4 * m**2 * u
        + 4 * m**2
        + 2 * m * u**3
        + 2 * m * u**2
        + 2 * u**3
        + 2 * u**2
    )
    return 2 * (m + 1) * (u + 1) * bracket


def C1(u: Fraction, m: Fraction) -> Fraction:
    bracket = (
        -20 * m**3
        + 4 * m**2 * u
        - 32 * m**2
        + 6 * m * u**2
        + 24 * m * u
        + 2 * u**2
        + 9 * u
        + 5
    )
    return (u + 1) * bracket


def C2(u: Fraction, m: Fraction) -> Fraction:
    return 16 * m**2 + 2 * m * u + 18 * m - 4 * u**2 - 10 * u - 2


def D_plus(u: Fraction, m: Fraction) -> Fraction:
    """Recorded: D_+ = 4 C0 C2 - C1^2 = -disc(P_0)."""
    c0, c1, c2 = C0(u, m), C1(u, m), C2(u, m)
    return 4 * c0 * c2 - c1 * c1


def z_star(u: Fraction, m: Fraction) -> Fraction | None:
    c2 = C2(u, m)
    if c2 == 0:
        return None
    return -C1(u, m) / (2 * c2)


def P0(u: Fraction, m: Fraction, z: Fraction) -> Fraction:
    return C0(u, m) + C1(u, m) * z + C2(u, m) * z * z


def z_max(u: Fraction, m: Fraction) -> Fraction:
    return min(m * m, (1 + u) * (3 + 4 * m - u) / 4)


def vertex_identity(u: Fraction, m: Fraction) -> bool:
    zs = z_star(u, m)
    if zs is None:
        return True
    lhs = P0(u, m, zs)
    rhs = D_plus(u, m) / (4 * C2(u, m))
    return lhs == rhs


SAMPLES = (
    (Fraction(1, 2), Fraction(1, 2)),
    (Fraction(1), Fraction(2)),
    (Fraction(3, 2), Fraction(1)),
    (Fraction(2), Fraction(3)),
    (Fraction(1, 5), Fraction(7, 3)),
)


def run() -> dict:
    rows = []
    for u, m in SAMPLES:
        zs = z_star(u, m)
        rows.append(
            {
                "u": str(u),
                "m": str(m),
                "C0": str(C0(u, m)),
                "C1": str(C1(u, m)),
                "C2": str(C2(u, m)),
                "D_plus": str(D_plus(u, m)),
                "z_star": None if zs is None else str(zs),
                "z_max": str(z_max(u, m)),
                "vertex_identity": vertex_identity(u, m),
            }
        )
    return {
        "ns_solved": False,
        "reopened": False,
        "D_plus_is": "4*C0*C2 - C1^2",
        "D_plus_is_not": "C1^2 - 4*C0*C2",
        "definitions_of_u_m_d": "missing",
        "definition_of_c": "missing",
        "definition_of_plus_plus_plus": "missing",
        "six_permutation_identity": "missing",
        "numerical_protocol": "missing",
        "chamber_search": False,
        "samples": rows,
        "all_vertex_identities": all(r["vertex_identity"] for r in rows),
        "note": (
            "Transcription lock of recovered Gate-5 algebra only. "
            "Does not define u,m,d and does not reopen the roadmap. "
            "NS not solved."
        ),
    }


def main() -> int:
    payload = run()
    out = Path(__file__).resolve().parents[1] / "results" / "gate5_recovered_algebra.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2), flush=True)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
