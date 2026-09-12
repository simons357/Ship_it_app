#!/usr/bin/env python3
"""Product-bound probe for Lemma★ packaging (finite-sample ceilings).

Measures how large |T_c| is relative to the classical product scales
    ||v||_2 * X^{3/2}
and the shape quotient R_★ = (T_c)_+^2 / (D_s E Y).

Does NOT prove Lemma★. Does NOT claim NS regularity.
Finite samples ≠ supremum; numerics ≠ proof.
Probes subordinate to analysis (not an HPC arms race).
See docs/ns-review/RESEARCH-POLICY.md.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ns_lemma_star_core import Field, R_star, project_perp, shell_wavevectors  # noqa: E402


OUT = Path("/opt/cursor/artifacts/ns-scientific-report")
OUT.mkdir(parents=True, exist_ok=True)


def _rand_perp(k, rng):
    w = rng.normal(size=3) + 1j * rng.normal(size=3)
    return project_perp(k, w)


def two_shell_field(
    n1: int, n2: int, rng: np.random.Generator, amp2: float = 1.0, per_shell: int = 4
) -> Field:
    """Several modes per shell so triad sums can produce nonzero T_c."""
    f = Field()
    for n, amp in ((n1, 1.0), (n2, amp2)):
        ks = shell_wavevectors(n, canonical_only=True)
        if not ks:
            raise ValueError(f"empty shell n={n}")
        pick = list(ks)
        rng.shuffle(pick)
        for k in pick[: max(1, min(per_shell, len(pick)))]:
            f.set_mode(k, amp * _rand_perp(k, rng))
    return f.normalize(1.0)


def random_band_field(kmax: int, rng: np.random.Generator, n_modes: int = 8) -> Field:
    f = Field()
    chosen = set()
    guard = 0
    while len(chosen) < n_modes and guard < 5000:
        guard += 1
        k = tuple(int(x) for x in rng.integers(-kmax, kmax + 1, size=3))
        if k == (0, 0, 0) or k in chosen or tuple(-x for x in k) in chosen:
            continue
        # Prefer lattice points that actually appear in low shells
        if k[0] * k[0] + k[1] * k[1] + k[2] * k[2] > kmax * kmax:
            continue
        chosen.add(k)
        f.set_mode(k, _rand_perp(k, rng))
    if len(chosen) < 3:
        raise ValueError("could not build a rich enough random band field")
    return f.normalize(1.0)


def ratios(field: Field) -> dict:
    rec = R_star(field, verify=True)
    E = float(rec["E"])
    X = float(rec["X"])
    Y = float(rec["Y"])
    Z = float(rec["Z"])
    Lam = float(rec["Lambda"])
    Tc = float(rec["T_c"])
    Ds = float(rec["D_s"])
    v2 = float(np.sqrt(max(E, 0.0)))
    prod = v2 * (X ** 1.5) if X > 0 else float("nan")
    prod_alt = v2 * X * Lam if X > 0 else float("nan")
    rs = rec["R_star"]
    return {
        "E": E,
        "X": X,
        "Y": Y,
        "Z": Z,
        "Lambda": Lam,
        "D_s": Ds,
        "T_c": Tc,
        "R_star": float(rs) if rs != float("inf") else None,
        "R_star_inf": bool(rs == float("inf")),
        "vacuous": bool(rec.get("vacuous_single_shell")),
        "abs_Tc_over_v2_X32": (abs(Tc) / prod) if prod and prod > 0 else None,
        "abs_Tc_over_v2_X_Lambda": (abs(Tc) / prod_alt) if prod_alt and prod_alt > 0 else None,
    }


def main() -> int:
    rng = np.random.default_rng(20260912)
    rows = []

    # Structured two-shell probes (near and far)
    for n1, n2, amp2 in [
        (1, 2, 1.0),
        (1, 5, 1.0),
        (2, 8, 0.5),
        (3, 6, 1.0),
        (1, 17, 0.25),
        (5, 10, 1.0),
    ]:
        try:
            f = two_shell_field(n1, n2, rng, amp2=amp2)
            r = ratios(f)
            r["family"] = f"two_shell_{n1}_{n2}_a{amp2}"
            rows.append(r)
        except Exception as e:  # noqa: BLE001
            rows.append({"family": f"two_shell_{n1}_{n2}", "error": str(e)})

    # Random band fields
    for i, kmax in enumerate([2, 3, 4, 5]):
        f = random_band_field(kmax, rng, n_modes=6 + i)
        r = ratios(f)
        r["family"] = f"random_band_kmax{kmax}"
        rows.append(r)

    finite = [r for r in rows if r.get("abs_Tc_over_v2_X32") is not None]
    summary = {
        "n_rows": len(rows),
        "n_measured": len(finite),
        "max_abs_Tc_over_v2_X32": max((r["abs_Tc_over_v2_X32"] for r in finite), default=None),
        "max_R_star": max(
            (r["R_star"] for r in finite if r.get("R_star") is not None),
            default=None,
        ),
        "note": (
            "Finite sample ceilings only. Does not prove Lemma★ / uniform R_★. "
            "Numerics ≠ proof."
        ),
    }

    payload = {"summary": summary, "rows": rows}
    out_json = OUT / "product_bound_probe.json"
    out_json.write_text(json.dumps(payload, indent=2))

    lines = [
        "product_bound_probe — finite-sample ceilings (scientific)",
        summary["note"],
        f"measured={summary['n_measured']}  max|Tc|/(||v||2 X^{3/2})={summary['max_abs_Tc_over_v2_X32']}",
        f"max R_star (finite)={summary['max_R_star']}",
        "",
    ]
    for r in rows:
        if "error" in r:
            lines.append(f"{r['family']}: ERROR {r['error']}")
            continue
        lines.append(
            f"{r['family']}: Tc={r['T_c']:.6e}  "
            f"|Tc|/(v2 X^3/2)={r['abs_Tc_over_v2_X32']:.6e}  "
            f"R*={r['R_star']}"
        )
    out_txt = OUT / "product_bound_probe.txt"
    out_txt.write_text("\n".join(lines) + "\n")
    print(out_txt.read_text())
    print(f"wrote {out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
