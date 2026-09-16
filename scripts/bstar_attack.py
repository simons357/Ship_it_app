"""Attack B★: [T_c]_+ ≤ C X Λ^{1/2} D_s^{1/2} on T^3.

Prove or disprove by families first. Not a close. ★ stays killed.
Do not overwrite stokes_moments.py.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "ns_attacks"))

from stokes_moments import (  # noqa: E402
    enforce_reality,
    high_triad_field,
    hh_l_fan_field,
    hh_l_one_key_field,
    k_norm2,
    make_divfree_amp,
    nonlinear_B,
    probe,
    random_field,
    scale_field,
    three_shell_field,
)
from verify_pr24_closure_review import growing_layer_field  # noqa: E402


def bstar_ratios(pr) -> dict:
    """R_B uses |T_c|: T_c is odd, so [T_c]_+ on {u,-u} is |T_c|."""
    tc_plus = max(float(pr.Tc), 0.0)
    tc_abs = abs(float(pr.Tc))
    x, y, ds, lam, e = pr.X, pr.Y, pr.Ds, pr.Lambda, pr.E
    denom = x * math.sqrt(lam) * math.sqrt(ds) if x > 0 and lam > 0 and ds > 0 else float("nan")
    denom_sq = x * y * ds if x > 0 and y > 0 and ds > 0 else float("nan")
    return {
        "E": e,
        "X": x,
        "Y": y,
        "Z": pr.Z,
        "Lambda": lam,
        "Ds": ds,
        "N": pr.N,
        "M": pr.M,
        "Tc": pr.Tc,
        "Tc_plus": tc_plus,
        "R_star": pr.ratio_box,
        "R_B": tc_abs / denom if denom == denom and denom > 0 else float("nan"),
        "R_B_sq": (tc_abs * tc_abs) / denom_sq if denom_sq == denom_sq and denom_sq > 0 else float("nan"),
        "E_over_X": e / x if x > 0 else float("nan"),
    }


def ahalf_B_norm(pr) -> float:
    """||A^{1/2} B||_2 from the stored B_L2 is ||B||_2, not H^1. Recompute if needed.

    ProbeResult.B_L2 is ||B||_2. CS door uses ||A^{1/2} B||_2.
    Callers that need it should pass the field. This stub is unused.
    """
    return float("nan")


def ahalf_B_from_field(field: dict) -> float:
    buu = nonlinear_B(field)
    s = 0.0
    for k, v in buu.items():
        kn2 = k_norm2(k)
        s += kn2 * float(np.vdot(v, v).real)
    return math.sqrt(max(s, 0.0))


def score(field: dict, label: str) -> dict:
    field = enforce_reality(field)
    pr = probe(field, label=label)
    row = bstar_ratios(pr)
    row["label"] = label
    row["modes"] = len(field)
    row["AhalfB"] = ahalf_B_from_field(field)
    x, y = row["X"], row["Y"]
    row["AhalfB_over_sqrtXY"] = (
        row["AhalfB"] / math.sqrt(x * y) if x > 0 and y > 0 else float("nan")
    )
    return row


def shear_field() -> dict:
    """u = (sin y, 0, 0). (u·∇)u = 0."""
    field = {}
    k = (0, 1, 0)
    field[k] = np.array([0.5j, 0.0, 0.0], dtype=np.complex128)
    return enforce_reality(field)


def one_shell_field(n: int = 1) -> dict:
    """Beltrami-like single shell |k|^2 = n²+(something). Use (n,0,0) pair."""
    field = {}
    k = (n, 0, 0)
    field[k] = make_divfree_amp(k, (0.0, 1.0, 0.0))
    return enforce_reality(field)


def separated_triad(m: int, amp_low: float = 1.0, amp_high: float = 1.0) -> dict:
    """Exact triad (1,0,0), (0,m,0), (1,m,0). Widely separated as m grows."""
    keys = ((1, 0, 0), (0, m, 0), (1, m, 0))
    amps = (amp_low, amp_high, amp_high)
    seeds = ((0.0, 1.0, 0.2), (1.0, 0.0, 0.3), (0.2, 0.5, 1.0))
    phases = (0.0, 0.5 * math.pi, -0.3)
    field = {}
    for k, amp, seed, phase in zip(keys, amps, seeds, phases):
        v = make_divfree_amp(k, seed)
        nrm = np.linalg.norm(v)
        if nrm < 1e-15:
            continue
        field[k] = (amp * np.exp(1j * phase) / nrm) * v
    return enforce_reality(field)


def phase_scan_separated(m: int, n_phase: int = 8) -> dict:
    """Scan phases on the separated triad; keep max R_B."""
    best = None
    keys = ((1, 0, 0), (0, m, 0), (1, m, 0))
    seeds = ((0.0, 1.0, 0.3), (1.0, 0.0, 0.2), (0.3, 0.6, 1.0))
    grid = np.linspace(0.0, 2.0 * math.pi, n_phase, endpoint=False)
    for ph0 in grid[::2]:
        for ph1 in grid:
            for ph2 in grid[::2]:
                field = {}
                for k, seed, phase in zip(keys, seeds, (ph0, ph1, ph2)):
                    v = make_divfree_amp(k, seed)
                    nrm = np.linalg.norm(v)
                    if nrm < 1e-15:
                        continue
                    field[k] = (np.exp(1j * phase) / nrm) * v
                row = score(field, f"sep_triad_m{m}_ph")
                if best is None or (
                    row["R_B"] == row["R_B"] and row["R_B"] > best["R_B"]
                ):
                    best = row
    assert best is not None
    best["label"] = f"sep_triad_m{m}_best"
    return best


def hh_energy_split(k_low, alpha: int, energy_high: float) -> dict:
    """HH→L one-key with a chosen high-shell energy fraction."""
    field, _meta = hh_l_one_key_field(k_low=k_low, alpha=alpha)
    if not field:
        return {}
    mk = (-k_low[0], -k_low[1], -k_low[2])
    highs = [k for k in field if k not in (k_low, mk)]
    out = {}
    if k_low in field:
        v = field[k_low]
        nrm = float(np.linalg.norm(v))
        if nrm > 0:
            out[k_low] = math.sqrt(max(1.0 - energy_high, 1e-8)) * v / nrm
    if highs:
        share = math.sqrt(max(energy_high, 1e-8) / len(highs))
        for k in highs:
            v = field[k]
            nrm = float(np.linalg.norm(v))
            if nrm > 0:
                out[k] = share * v / nrm
    return enforce_reality(out)


def abc_field(a: float = 1.0, b: float = 1.0, c: float = 1.0) -> dict:
    """Periodic ABC: three orthogonal Beltrami modes."""
    field = {
        (0, 1, 0): np.array([0.5j * a, 0.0, 0.0], dtype=np.complex128),
        (0, 0, 1): np.array([0.0, 0.5j * b, 0.0], dtype=np.complex128),
        (1, 0, 0): np.array([0.0, 0.0, 0.5j * c], dtype=np.complex128),
    }
    return enforce_reality(field)


def two_scale(low_k, high_k, amp_low: float, amp_high: float) -> dict:
    field = {}
    for k, amp, seed in (
        (low_k, amp_low, (0.0, 1.0, 0.2)),
        (high_k, amp_high, (1.0, 0.0, 0.3)),
    ):
        v = make_divfree_amp(k, seed)
        nrm = np.linalg.norm(v)
        if nrm < 1e-15:
            continue
        field[k] = (amp / nrm) * v
    return enforce_reality(field)


def finite(x: float) -> bool:
    return x == x and abs(x) < 1e300


def max_rb(rows: list[dict]) -> float:
    vals = [r["R_B"] for r in rows if finite(r.get("R_B", float("nan")))]
    return max(vals) if vals else float("nan")


def run() -> dict:
    rows: list[dict] = []

    # 1. Growing layer: ★ dies, B★ should not.
    vn = []
    for n in range(1, 9):
        row = score(growing_layer_field(n), f"v_{n}")
        rows.append(row)
        vn.append(row)

    # 2. Amplitude invariance on a fixed triad.
    base = high_triad_field(amp=1.0)
    amp_rows = []
    for a in (1.0, 3.0, 9.0):
        row = score(scale_field(base, a), f"triad_A{a:g}")
        rows.append(row)
        amp_rows.append(row)

    # 3. Shear and one shell: T_c = 0.
    rows.append(score(shear_field(), "shear"))
    rows.append(score(one_shell_field(2), "one_shell"))

    # 4. Widely separated exact triads + phase scan.
    sep = []
    for m in (1, 2, 4, 8, 12, 16):
        row = score(separated_triad(m), f"sep_triad_m{m}")
        rows.append(row)
        sep.append(row)
        best = phase_scan_separated(m, n_phase=6)
        rows.append(best)
        sep.append(best)

    # 5. Two-scale amplitude ratios.
    ts = []
    for m in (4, 8, 16):
        for al, ah in ((1.0, 0.05), (1.0, 1.0), (0.05, 1.0), (1.0, 0.2)):
            row = score(two_scale((1, 0, 0), (0, m, 0), al, ah), f"twoscale_m{m}_al{al}_ah{ah}")
            rows.append(row)
            ts.append(row)

    # 6. Three-shell and dilated high triad.
    for k0, e in (((1, 0, 0), (0, 1, 0)), ((2, 1, 0), (0, 0, 1)), ((4, 2, 1), (1, 0, 0))):
        rows.append(score(three_shell_field(k0, e), f"threeshell_{k0}_{e}"))
    for scale in (1, 2, 4):
        k1 = (4 * scale, 2 * scale, scale)
        k2 = (-3 * scale, scale, scale)
        rows.append(score(high_triad_field(amp=1.0, k1=k1, k2=k2), f"dilate_triad_{scale}"))

    # 7. HH→L one-key, growing high sphere.
    hhl = []
    for alpha in (5, 13, 25, 41):
        field, meta = hh_l_one_key_field(k_low=(2, 0, 0), alpha=alpha)
        if not field:
            continue
        row = score(field, f"hhl_one_a{alpha}")
        row["n_pairs"] = meta.get("n_pairs")
        rows.append(row)
        hhl.append(row)

    for alpha in (5, 13, 25):
        for eh in (0.1, 0.5, 0.9):
            field = hh_energy_split((2, 0, 0), alpha, eh)
            if not field:
                continue
            row = score(field, f"hhl_split_a{alpha}_eh{eh}")
            rows.append(row)
            hhl.append(row)

    rng = np.random.default_rng(1390)
    for n_pairs in (2, 4, 8):
        row = score(hh_l_fan_field(n_pairs, rng=rng), f"hhl_fan_{n_pairs}")
        rows.append(row)
        hhl.append(row)

    rows.append(score(abc_field(), "ABC"))

    # 8. Random many-mode.
    rnd = []
    for kmax, n_modes in ((2, 8), (3, 16), (4, 24), (5, 36)):
        row = score(random_field(rng, kmax=kmax, n_modes=n_modes), f"rand_k{kmax}_n{n_modes}")
        rows.append(row)
        rnd.append(row)

    # 9. Extra random search: many draws, keep max R_B.
    hunt = []
    for i in range(40):
        kmax = int(rng.integers(2, 6))
        n_modes = int(rng.integers(4, 20))
        row = score(random_field(rng, kmax=kmax, n_modes=n_modes), f"hunt_{i}")
        hunt.append(row)
        rows.append(row)

    finite_rb = [r["R_B"] for r in rows if finite(r.get("R_B", float("nan")))]
    finite_cs = [
        r["AhalfB_over_sqrtXY"]
        for r in rows
        if finite(r.get("AhalfB_over_sqrtXY", float("nan")))
    ]
    vn_rb = [r["R_B"] for r in vn if finite(r["R_B"])]
    amp_rb = [r["R_B"] for r in amp_rows if finite(r["R_B"])]

    verdict = {
        "max_R_B": max(finite_rb) if finite_rb else None,
        "max_AhalfB_over_sqrtXY": max(finite_cs) if finite_cs else None,
        "n_rows": len(rows),
        "vn_R_B": vn_rb,
        "vn_R_star": [r["R_star"] for r in vn],
        "vn_R_B_decreases": vn_rb == sorted(vn_rb, reverse=True) and vn_rb[-1] < vn_rb[0],
        "amplitude_invariant": (
            max(amp_rb) - min(amp_rb) < 1e-8 * max(1.0, max(amp_rb)) if amp_rb else False
        ),
        "shear_Tc": next(r["Tc"] for r in rows if r["label"] == "shear"),
        "one_shell_Ds": next(r["Ds"] for r in rows if r["label"] == "one_shell"),
        "sep_max_R_B": max_rb(sep),
        "twoscale_max_R_B": max_rb(ts),
        "hhl_max_R_B": max_rb(hhl),
        "rand_max_R_B": max_rb(rnd + hunt),
    }
    # Kill if R_B grows without bound on a named family. Finite max is not a proof.
    verdict["killed"] = False
    verdict["survived_these_families"] = True
    return {"verdict": verdict, "rows": rows}


def main() -> None:
    out = run()
    dest = ROOT / "results" / "bstar_attack"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "bstar.json"
    # Drop huge rows' raw floats only; keep all rows.
    path.write_text(json.dumps(out, indent=2, default=str))
    v = out["verdict"]
    print("max_R_B", v["max_R_B"])
    print("max_CS", v["max_AhalfB_over_sqrtXY"])
    print("vn_R_B", v["vn_R_B"])
    print("vn_R_star", v["vn_R_star"])
    print("vn_decreases", v["vn_R_B_decreases"])
    print("amp_inv", v["amplitude_invariant"])
    print("sep_max", v["sep_max_R_B"], "twoscale", v["twoscale_max_R_B"])
    print("hhl_max", v["hhl_max_R_B"], "rand_max", v["rand_max_R_B"])
    print("wrote", path)


if __name__ == "__main__":
    main()
