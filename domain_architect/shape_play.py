"""Play with a shape: if a symmetry is in the object, fill the other side and measure.

Some shapes complete by identity (strain eigenvalues sum to zero). Some do
not (the tube wall is a cut, not a mirror of Navier–Stokes). For those you
may still *play*: impose a completion, fill the missing side, measure the
wall. That measurement is extra environment, not a lemma.

Not a regularity proof. Filling CLIP-T3-OUTER by reflection does not fill
CLIP-T3-WELD. CosmoEvolution is not this lab.
"""

from __future__ import annotations

from typing import Any, Final

import numpy as np

from .ns_tube import hardy_wall_ratio


BLOCKS: Final[str] = " ▁▂▃▄▅▆▇█"


def sparkline(values: np.ndarray, width: int = 20) -> str:
    """Nonnegative sparkline for a radial profile."""
    y = np.asarray(values, dtype=float)
    if y.size == 0:
        return ""
    if y.size > width:
        idx = np.linspace(0, y.size - 1, width).astype(int)
        y = y[idx]
    peak = float(np.max(y))
    if peak <= 0.0:
        return BLOCKS[0] * int(y.size)
    last = len(BLOCKS) - 1
    out: list[str] = []
    for v in y:
        k = int(round(last * float(v) / peak))
        out.append(BLOCKS[max(0, min(last, k))])
    return "".join(out)


IDENTITY_SHAPES: Final[tuple[dict[str, str], ...]] = (
    {
        "id": "STRAIN",
        "shape": "traceless strain eigenframe",
        "symmetry": "λ1 + λ2 + λ3 = 0",
        "if_you_have": "two eigenvalues",
        "you_fill": "the third, λ3 = −λ1 − λ2",
        "status": "identity",
        "clip_id": "—",
        "notes": "Visual: three bars that must sum to a flat line. Not depletion.",
    },
    {
        "id": "DIV-FREE",
        "shape": "divergence-free field on T^3",
        "symmetry": "k · û(k) = 0",
        "if_you_have": "two Fourier components of û(k)",
        "you_fill": "the third, along k",
        "status": "identity",
        "clip_id": "—",
        "notes": "Leray projector. Already used in B1.",
    },
)

PLAY_SHAPES: Final[tuple[dict[str, str], ...]] = (
    {
        "id": "CYLINDER",
        "shape": "tube wall r=δ (two-sided cylinder)",
        "symmetry": "none forced by NS; δ is a cut you chose",
        "if_you_have": "h on the inside r≤δ with h(0)=0",
        "you_fill": "a chosen outside: even reflect, invert, or refuse",
        "status": "play",
        "clip_id": "CLIP-T3-OUTER",
        "notes": (
            "Even reflection across the wall manufactures h(2δ)=h(0)=0. "
            "Young then fires. That is extra environment, not the torus."
        ),
    },
)

CANNOT_FILL: Final[tuple[dict[str, str], ...]] = (
    {
        "id": "THREE-SHELL",
        "shape": "dyadic packet P_{j*} = X_{j*-1}+X_{j*}+X_{j*+1}",
        "symmetry": "none — three independent masses",
        "if_you_have": "two shells",
        "you_fill": "you do not fill the third",
        "status": "cannot_fill",
        "clip_id": "CLIP-B2-OCCUPATION",
        "notes": "Bernstein treats them as one scale. It does not determine the masses.",
    },
    {
        "id": "I-OFF",
        "shape": "swirl source (Γ ∂_z Γ) ω^r / r³",
        "symmetry": "not a radial profile of h=Γ/r",
        "if_you_have": "the filled radial h, even by reflection",
        "you_fill": "you do not fill ∂_z Γ or ω^r",
        "status": "cannot_fill",
        "clip_id": "CLIP-T3-WELD",
        "notes": "Radial play can buy T3a. It cannot buy T3b. Different fields.",
    },
)


def _inside_profile(delta: float = 0.5, n: int = 80) -> tuple[np.ndarray, np.ndarray]:
    """Axis-vanishing h on (0, δ]. Default h = r, so the wall value is live."""
    r = np.linspace(delta / n, delta, n)
    h = r.copy()
    h[0] = 0.0
    return r, h


def _even_reflect(r_in: np.ndarray, h_in: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Mirror across r=δ. Then h(2δ)=h(0)=0. Manufactures T3a extra E."""
    delta = float(r_in[-1])
    r_out = (2.0 * delta - r_in[-2::-1]).copy()
    h_out = h_in[-2::-1].copy()
    return r_out, h_out


def _invert(r_in: np.ndarray, h_in: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Hardy dual: ρ = δ²/r. Pull h across the wall by inversion."""
    delta = float(r_in[-1])
    r_out = (delta**2 / r_in[-2::-1]).copy()
    h_out = h_in[-2::-1].copy()
    return r_out, h_out


def _trap(y: np.ndarray, x: np.ndarray) -> float:
    if hasattr(np, "trapezoid"):
        return float(np.trapezoid(y, x))
    return float(np.trapz(y, x))


def _outside_trace(
    h_wall: float, r_out: np.ndarray, h_out: np.ndarray, eps: float = 1.0
) -> dict[str, Any]:
    """Young on [δ, R] using the wall value as h(δ). Variable grids allowed."""
    dr = float(r_out[1] - r_out[0]) if r_out.size > 1 else 1e-6
    r0 = float(r_out[0] - dr)
    if r0 <= 0.0:
        r0 = max(dr, 0.5 * float(r_out[0]))
    r_full = np.concatenate(([r0], r_out))
    h_full = np.concatenate(([h_wall], h_out))
    hp = np.gradient(h_full, r_full)
    lhs = float(h_full[0] ** 2)
    rhs = (
        eps * _trap((hp**2) * r_full, r_full)
        + (1.0 / eps) * _trap((h_full**2) / np.maximum(r_full, dr), r_full)
        + float(h_full[-1] ** 2)
    )
    ratio = lhs / rhs if rhs > 0.0 else float("inf")
    outer_h = float(h_full[-1])
    return {
        "young_lhs_over_rhs": ratio,
        "young_holds": ratio <= 1.05,
        "h_at_wall": h_wall,
        "h_at_outer": outer_h,
        "outer_vanishes": abs(outer_h) <= 0.05 * max(abs(h_wall), 1e-12),
    }


def play_cylinder(delta: float = 0.5, n: int = 80) -> dict[str, Any]:
    """Fill the other side of the cylinder three ways and measure."""
    r_in, h_in = _inside_profile(delta=delta, n=n)
    h_wall = float(h_in[-1])
    hardy_in = hardy_wall_ratio(h_in, r_in)
    spark_in = sparkline(h_in)

    even_r, even_h = _even_reflect(r_in, h_in)
    even_m = _outside_trace(h_wall, even_r, even_h)

    inv_r, inv_h = _invert(r_in, h_in)
    inv_m = _outside_trace(h_wall, inv_r, inv_h)

    return {
        "shape": "CYLINDER",
        "status": "play",
        "not_a_lemma": True,
        "delta": delta,
        "inside": {
            "hardy_lhs_over_rhs": hardy_in,
            "hardy_holds": hardy_in <= 1.05,
            "h_at_axis": float(h_in[0]),
            "h_at_wall": h_wall,
            "spark": spark_in,
        },
        "completions": [
            {
                "id": "even_reflect",
                "rule": "h(δ+s) = h(δ−s)  ⇒  h(2δ)=h(0)=0",
                "spark": spark_in + "|" + sparkline(even_h),
                "extra_E": True,
                "buys": "T3a / CLIP-T3-OUTER on this manufactured outside",
                "does_not_buy": "CLIP-T3-WELD (no ∂_z Γ, no ω^r)",
                **even_m,
            },
            {
                "id": "invert",
                "rule": "ρ = δ²/r  (Hardy dual / inversion in the disk)",
                "spark": spark_in + "|" + sparkline(inv_h),
                "extra_E": True,
                "buys": "a dual copy of the inside, not NS off-axis",
                "does_not_buy": "CLIP-T3-WELD",
                **inv_m,
            },
            {
                "id": "refuse",
                "rule": "leave the outside unfilled — the actual NS cut",
                "spark": spark_in + "|░░░░░░░░░░░░",
                "extra_E": False,
                "buys": "honesty: δ is a cut, not a mirror",
                "does_not_buy": "T3a and T3b both stay open as welds to NS",
                "young_lhs_over_rhs": None,
                "young_holds": False,
                "h_at_wall": h_wall,
                "h_at_outer": None,
                "outer_vanishes": False,
            },
        ],
        "verdict": (
            "You can play: even reflection fills the other side and Young "
            "measures. That fill is extra E (CLIP-T3-OUTER), not Navier–Stokes. "
            "Radial play never fills I_off (CLIP-T3-WELD)."
        ),
    }


def play_strain(
    lam1: float = 1.0,
    lam2: float = 0.4,
    mu: tuple[float, float, float] = (0.5, 0.3, 0.2),
) -> dict[str, Any]:
    """If you have two strain eigenvalues, the shape fills the third."""
    lam3 = -lam1 - lam2
    eigs = (lam1, lam2, lam3)
    stretching = float(sum(l * m for l, m in zip(eigs, mu)))
    return {
        "shape": "STRAIN",
        "status": "identity",
        "not_a_lemma": False,
        "given": {"λ1": lam1, "λ2": lam2},
        "filled": {"λ3": lam3},
        "sum": float(sum(eigs)),
        "sum_is_zero": abs(sum(eigs)) <= 1e-12,
        "stretching_Σλμ": stretching,
        "spark_abs": sparkline(np.array([abs(lam1), abs(lam2), abs(lam3)]), width=3),
        "notes": (
            "The missing eigenvalue is filled because the shape is traceless. "
            "Alignment / depletion (CLIP-B3b-ALIGN) is not filled."
        ),
        "clip_still_open": "CLIP-B3b-ALIGN",
    }


def play_three_shell(x: tuple[float, ...] | None = None) -> dict[str, Any]:
    """Two shells do not determine the third."""
    masses = list(x) if x is not None else [0.08, 0.12, 0.40, 0.18, 0.10, 0.07, 0.05]
    jstar = int(np.argmax(masses))
    known = {
        "j*-1": masses[jstar - 1] if jstar else None,
        "j*": masses[jstar],
        "j*+1": masses[jstar + 1] if jstar + 1 < len(masses) else None,
    }
    return {
        "shape": "THREE-SHELL",
        "status": "cannot_fill",
        "not_a_lemma": True,
        "jstar": jstar,
        "have": known,
        "missing": "none — all three are independent data",
        "spark": sparkline(np.array(masses, dtype=float), width=len(masses)),
        "notes": (
            "You cannot fill a neighbor shell from the other two. "
            "Occupation stays a clip."
        ),
        "clip_id": "CLIP-B2-OCCUPATION",
    }


def shape_play() -> dict[str, Any]:
    cyl = play_cylinder()
    strain = play_strain()
    shells = play_three_shell()
    even = next(c for c in cyl["completions"] if c["id"] == "even_reflect")
    return {
        "title": "Play with the shape — fill the other side, then measure",
        "not_a_regularity_proof": True,
        "rule": (
            "If the symmetry is in the object, fill and measure (identity). "
            "If you put the symmetry in, you may still play, but the fill is "
            "extra E. Listing a filled side is not walking past GAP-T3."
        ),
        "identity_shapes": [dict(s) for s in IDENTITY_SHAPES],
        "play_shapes": [dict(s) for s in PLAY_SHAPES],
        "cannot_fill": [dict(s) for s in CANNOT_FILL],
        "strain": strain,
        "cylinder": cyl,
        "three_shell": shells,
        "gap": {
            "id": "GAP-T3",
            "even_reflect_buys_T3a": bool(even["young_holds"] and even["outer_vanishes"]),
            "even_reflect_buys_T3b": False,
            "still_missing": "CLIP-T3-WELD — I_off is not a radial profile of h",
        },
        "next": (
            "Play is allowed. Do not promote even-reflect T3a to a torus lemma. "
            "The live missing piece is still CLIP-T3-WELD."
        ),
    }


def format_shape_play(report: dict[str, Any] | None = None) -> str:
    data = report or shape_play()
    lines = [
        data["title"],
        "Not a regularity proof. " + data["rule"],
        "",
        "Identities (the shape really fills the other side)",
    ]
    for row in data["identity_shapes"]:
        lines.append(f"  {row['id']}  [{row['status']}]  {row['shape']}")
        lines.append(f"      have {row['if_you_have']} → fill {row['you_fill']}")
        lines.append(f"      {row['notes']}")
    st = data["strain"]
    lines.append(
        f"      demo: λ1={st['given']['λ1']}, λ2={st['given']['λ2']} "
        f"→ λ3={st['filled']['λ3']:.2f}  sum={st['sum']:.1e}  "
        f"{'ok' if st['sum_is_zero'] else 'FAIL'}"
    )
    lines.append("")
    lines.append("Play (you put the symmetry in, then measure)")
    for row in data["play_shapes"]:
        lines.append(f"  {row['id']}  [{row['status']}]  {row['shape']}")
        lines.append(f"      {row['notes']}")
    cyl = data["cylinder"]
    inside_flag = "ok" if cyl["inside"]["hardy_holds"] else "FAIL"
    lines.append(f"      inside Hardy [{inside_flag}]  {cyl['inside']['spark']}")
    for comp in cyl["completions"]:
        if comp["id"] == "refuse":
            flag = "—"
        elif comp.get("young_holds"):
            flag = "ok"
        else:
            flag = "no"
        lines.append(f"      {comp['id']:13} [{flag}]  {comp['spark']}")
        lines.append(f"          {comp['rule']}")
        lines.append(f"          buys: {comp['buys']}")
        lines.append(f"          does not: {comp['does_not_buy']}")
    lines.append("")
    lines.append("Cannot fill (the obvious symmetry is not there)")
    for row in data["cannot_fill"]:
        lines.append(f"  {row['id']}  [{row['status']}]  {row['clip_id']}")
        lines.append(f"      {row['notes']}")
    sh = data["three_shell"]
    lines.append(f"      packet {sh['spark']}  j*={sh['jstar']}")
    lines.append("")
    gap = data["gap"]
    lines.append(
        f"GAP-T3: even reflect buys T3a? {gap['even_reflect_buys_T3a']}. "
        f"Buys T3b? {gap['even_reflect_buys_T3b']}."
    )
    lines.append("  still missing: " + gap["still_missing"])
    lines.append("Next: " + data["next"])
    return "\n".join(lines)
