"""Seat equation (1): the S_pq pair-vector decomposition.

Source: origin/cursor/fourier-triangles-audit-f37a
packets/FOURIER-TRIANGLES-AUDIT-2026-09-20.md
That formula was written 20 Sep 2026. This book previously omitted it.
The 24 Sep Grok Heavily audit failed G1.(1) closed for that omission.

No sympy. Elementary numpy checks only.
Does not invent alpha=98 / 432 realizations.
Does not invent a BOTH-SIGNS family.
Does not alter the SBP / phi-d / low-tail / sign gates.
NS is not solved.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def frame(a: float, b: float, c: float) -> dict:
    s = (c - a - b) / 2.0
    delta = a * b - s * s
    if delta <= 0 or a <= 0 or b <= 0 or c <= 0:
        raise ValueError("need a nondegenerate triangle")
    x = (c + a - b) / (2.0 * np.sqrt(c))
    y = (c + b - a) / (2.0 * np.sqrt(c))
    h = np.sqrt(delta / c)
    e0 = np.array([1.0, 0.0, 0.0])
    e1 = np.array([0.0, 1.0, 0.0])
    e2 = np.array([0.0, 0.0, 1.0])
    p = x * e0 + h * e1
    q = y * e0 - h * e1
    k = p + q
    return {
        "a": a,
        "b": b,
        "c": c,
        "s": s,
        "delta": delta,
        "x": x,
        "y": y,
        "h": h,
        "e0": e0,
        "e1": e1,
        "e2": e2,
        "p": p,
        "q": q,
        "k": k,
    }


def polarizations(fr: dict, A1, A2, B1, B2) -> tuple[np.ndarray, np.ndarray]:
    e0, e1, e2 = fr["e0"], fr["e1"], fr["e2"]
    x, y, h, a, b = fr["x"], fr["y"], fr["h"], fr["a"], fr["b"]
    u_p = A1 * (h * e0 - x * e1) / np.sqrt(a) + A2 * e2
    u_q = B1 * (h * e0 + y * e1) / np.sqrt(b) + B2 * e2
    return u_p, u_q


def S_direct(fr: dict, u_p: np.ndarray, u_q: np.ndarray) -> np.ndarray:
    raw = (np.dot(fr["q"], u_p)) * u_q + (np.dot(fr["p"], u_q)) * u_p
    return raw - np.dot(raw, fr["e0"]) * fr["e0"]


def S_formula(fr: dict, A1, A2, B1, B2) -> np.ndarray:
    """Boxed (1)."""
    a, b, c, h = fr["a"], fr["b"], fr["c"], fr["h"]
    e1, e2 = fr["e1"], fr["e2"]
    return (h * (b - a) / np.sqrt(a * b)) * A1 * B1 * e1 + (
        np.sqrt(c) * h * (A1 * B2 / np.sqrt(a) + A2 * B1 / np.sqrt(b))
    ) * e2


def S_equal_formula(alpha: float, beta: float, A1, A2, B1, B2, e2: np.ndarray) -> np.ndarray:
    """Boxed (3), a=b=alpha, c=beta."""
    return np.sqrt(beta * (1.0 - beta / (4.0 * alpha))) * (A1 * B2 + A2 * B1) * e2


def defect_rhs(fr: dict, u_p: np.ndarray, u_q: np.ndarray) -> complex:
    """Boxed (4): ((b-a)/c) (k·u_p)(k·u_q)."""
    a, b, c, k = fr["a"], fr["b"], fr["c"], fr["k"]
    return ((b - a) / c) * np.dot(k, u_p) * np.dot(k, u_q)


def check_identity(a=5.0, b=8.0, c=9.0, A1=1.2 + 0.3j, A2=-0.4 + 0.7j, B1=0.5 - 0.2j, B2=1.1 + 0.1j) -> dict:
    fr = frame(a, b, c)
    u_p, u_q = polarizations(fr, A1, A2, B1, B2)
    Sd = S_direct(fr, u_p, u_q)
    Sf = S_formula(fr, A1, A2, B1, B2)
    residual = np.linalg.norm(Sd - Sf)
    Pk_p = fr["p"] - np.dot(fr["p"], fr["e0"]) * fr["e0"]
    lhs4 = np.dot(Pk_p, Sd)
    rhs4 = defect_rhs(fr, u_p, u_q)
    return {
        "residual_1": float(residual),
        "identity_1": bool(residual < 1e-10),
        "div_p": float(abs(np.dot(fr["p"], u_p))),
        "div_q": float(abs(np.dot(fr["q"], u_q))),
        "p_on_shell": bool(abs(np.dot(fr["p"], fr["p"]) - a) < 1e-12),
        "q_on_shell": bool(abs(np.dot(fr["q"], fr["q"]) - b) < 1e-12),
        "k_norm2": bool(abs(np.dot(fr["k"], fr["k"]) - c) < 1e-12),
        "q_dot_up_is_k_dot_up": bool(abs(np.dot(fr["q"], u_p) - np.dot(fr["k"], u_p)) < 1e-12),
        "defect_4": float(abs(lhs4 - rhs4)),
        "identity_4": bool(abs(lhs4 - rhs4) < 1e-10),
    }


def check_equal_length(alpha=5.0, beta=4.0) -> dict:
    fr = frame(alpha, alpha, beta)
    A1, A2, B1, B2 = 0.8 + 0.1j, -0.3j, 1.0, 0.6 + 0.2j
    u_p, u_q = polarizations(fr, A1, A2, B1, B2)
    Sd = S_direct(fr, u_p, u_q)
    Se = S_equal_formula(alpha, beta, A1, A2, B1, B2, fr["e2"])
    in_plane = abs(np.dot(Sd, fr["e1"]))
    return {
        "residual_3": float(np.linalg.norm(Sd - Se)),
        "identity_3": bool(np.linalg.norm(Sd - Se) < 1e-10),
        "in_plane_cancels": bool(in_plane < 1e-10),
    }


def run() -> dict:
    samples = []
    ok = True
    for a, b, c in ((5.0, 8.0, 9.0), (2.0, 2.0, 2.0), (13.0, 5.0, 8.0), (4.0, 4.0, 4.0)):
        rec = check_identity(a, b, c)
        samples.append({"a": a, "b": b, "c": c, **rec})
        ok = ok and rec["identity_1"] and rec["identity_4"] and rec["p_on_shell"]
    eq = check_equal_length()
    ok = ok and eq["identity_3"] and eq["in_plane_cancels"]
    return {
        "ns_solved": False,
        "source": "packets/FOURIER-TRIANGLES-AUDIT-2026-09-20.md on origin/cursor/fourier-triangles-audit-f37a",
        "seats_G1_1": True,
        "alpha_98_432_invented": False,
        "both_signs_invented": False,
        "samples": samples,
        "equal_length": eq,
        "all_identities_ok": bool(ok),
        "note": (
            "Boxed (1)(3)(4) sit. This was the 24 Sep G1.(1) missing input. "
            "alpha=98 / 432 realizations remain unstamped. "
            "BOTH-SIGNS family remains not on this tree. NS not solved."
        ),
    }


def main() -> int:
    payload = run()
    out = Path(__file__).resolve().parents[1] / "results" / "fourier_triangle_s_pq.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2), flush=True)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
