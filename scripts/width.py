"""Score relative spectral width and the r~κ^{-1/2} comparison. Not a close.

r² = D_s/(Λ Y) = D_s/(X Λ²) is the squared relative width of
the |k|²-measure. D_s/Y = Λ r². The comparison
    r ≳ κ^{-1/2}  ⇔  D_s/Y ≳ κ,   κ=√Λ
is an equivalence of three writings of one threshold.
It is not a theorem that BROAD is paid by viscosity.

r is scale-invariant. κ^{-1/2} is not. Do not stamp
the crossover. No sitting primitive for S_Γ on this desk.

Does not overwrite stokes_moments.py.
Does not restore ★.
Does not seat B★.
Does not start leftover 1.
Does not adopt SAG, JGC, or DA-NS-2 as seated.
Does not invent B^prim.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from centered_barycenter import modes_to_moments, two_triad_strike  # noqa: E402
from centered_ledger import two_shell_moments  # noqa: E402

OUT = ROOT / "results" / "width.json"


def width_row(x: float, y: float, z: float) -> dict:
    lam = y / x
    d_s = z - lam * y
    r2 = d_s / (lam * y) if lam > 0 and y > 0 else float("nan")
    r2_alt = d_s / (x * lam * lam) if x > 0 and lam > 0 else float("nan")
    kappa = math.sqrt(lam) if lam > 0 else float("nan")
    d_s_over_y = d_s / y if y > 0 else float("nan")
    lam_r2 = lam * r2
    thresh = kappa ** (-0.5) if kappa > 0 else float("nan")
    return {
        "X": x,
        "Y": y,
        "Z": z,
        "Lambda": lam,
        "Ds": d_s,
        "r2": r2,
        "r": math.sqrt(r2) if r2 >= 0 else float("nan"),
        "r2_from_X": r2_alt,
        "kappa": kappa,
        "Ds_over_Y": d_s_over_y,
        "Lambda_r2": lam_r2,
        "kappa_inv_sqrt": thresh,
        "identities_ok": abs(r2 - r2_alt) < 1e-12 * max(1.0, abs(r2_alt))
        and abs(d_s_over_y - lam_r2) < 1e-12 * max(1.0, abs(lam_r2)),
        "broad_by_threshold": r2 >= 0 and math.sqrt(r2) + 1e-15 >= thresh,
    }


def scale_eigenvalues(a: list[float], mass: list[float], ell: float) -> dict:
    """Scale |k| by ell, so eigenvalues a = |k|² become ell² a."""
    a2 = [ell * ell * ai for ai in a]
    m0 = modes_to_moments(a, mass)
    m1 = modes_to_moments(a2, mass)
    w0 = width_row(m0["X"], m0["Y"], m0["Z"])
    w1 = width_row(m1["X"], m1["Y"], m1["Z"])
    return {
        "ell": ell,
        "r0": w0["r"],
        "r1": w1["r"],
        "kappa0": w0["kappa"],
        "kappa1": w1["kappa"],
        "thresh0": w0["kappa_inv_sqrt"],
        "thresh1": w1["kappa_inv_sqrt"],
        "r_invariant": abs(w0["r"] - w1["r"]) < 1e-12 * max(1.0, w0["r"]),
        "kappa_scales": abs(w1["kappa"] - ell * w0["kappa"])
        < 1e-12 * max(1.0, ell * w0["kappa"]),
        "thresh_drops": w1["kappa_inv_sqrt"] < w0["kappa_inv_sqrt"] - 1e-15
        if ell > 1.0
        else True,
    }


def conversion_row(r: float, kappa: float) -> dict:
    """δ ≈ r κ / 2 converts |k|-gap to relative |k|² width."""
    delta = r * kappa / 2.0
    old = kappa**2 * delta
    new = (kappa**3) * r
    return {
        "r": r,
        "kappa": kappa,
        "delta": delta,
        "kappa2_delta": old,
        "kappa3_r": new,
        # O(κ² δ) and O(κ³ r) share the leading factor 1/2.
        "ratio": old / new if new else float("nan"),
        "ok": abs(old - 0.5 * new) < 1e-12 * max(1.0, abs(new)),
    }


def ladder(n: int) -> dict:
    """Equal-mass |k|² = 1²,...,n². Width scaling of a growing support."""
    a = [float(m * m) for m in range(1, n + 1)]
    mass = [1.0] * n
    mom = modes_to_moments(a, mass)
    w = width_row(mom["X"], mom["Y"], mom["Z"])
    return {"n": n, **w}


def record() -> dict:
    shells = []
    for alpha, beta, e_a, e_b in (
        (2.0, 4.0, 1.0, 1.0),
        (1.0, 5.0, 0.4, 0.7),
        (3.0, 12.0, 2.0, 0.5),
        (4.0, 4.01, 1.0, 1.0),
    ):
        m = two_shell_moments(alpha, beta, e_a, e_b)
        w = width_row(m["X"], m["Y"], m["Z"])
        w["alpha"] = alpha
        w["beta"] = beta
        shells.append(w)

    scaled = scale_eigenvalues([1.0, 4.0, 9.0], [1.0, 1.0, 1.0], 4.0)
    conv = conversion_row(0.2, 5.0)
    strike = two_triad_strike()
    ladders = [ladder(n) for n in (2, 4, 8, 16)]

    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "bstar_not_seated": True,
        "identities": {
            "r2": "r² = D_s/(Λ Y) = D_s/(X Λ²)",
            "Ds_over_Y": "D_s/Y = Λ r²",
            "crossover": "r ≳ κ^{-1/2}  ⇔  D_s/Y ≳ κ,  κ=√Λ",
            "conversion": "δ ≈ r κ / 2  ⇒  κ² δ = (1/2) κ³ r",
        },
        "two_shell": shells,
        "identities_ok": all(s["identities_ok"] for s in shells),
        "scale": scaled,
        "r_scale_invariant": bool(scaled["r_invariant"]),
        "threshold_not_scale_invariant": bool(
            scaled["kappa_scales"] and scaled["thresh_drops"]
        ),
        "conversion": conv,
        "conversion_ok": bool(conv["ok"]),
        "ladders": ladders,
        "ladder_r_stays_order_one": all(0.1 < row["r"] < 2.0 for row in ladders),
        "ladder_becomes_broad": all(
            row["broad_by_threshold"] for row in ladders if row["n"] >= 8
        ),
        "charge_only_dead": bool(
            abs(strike["Q_sum"]) < 1e-12 and strike["T_sum"] > 0.0
        ),
        "no_primitive_for_S": True,
        "crossover_is_not_a_theorem": True,
        "broad_is_not_a_payment": True,
        "da_ns2_is_not_a_theorem": True,
        "sits_as_useful_K": False,
        "sits_as_g4_death": False,
        "sits_as_da_ns2": False,
        "sits_as_jgc": False,
        "sits_as_bprim": False,
        "g4_stays_open": True,
        "do_not_glue_to_leftover_1": True,
        "do_not_invent_a_bridge": True,
    }
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
