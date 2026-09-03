"""Energy as a visual object: see the outside, guess the shape, measure.

Bernstein is an identity: shell kinetic energy fills that shell's enstrophy
(X_j = 2^{2j} E_j). The energy ladder and the enstrophy ladder are the same
object warped by a weight.

Guessing the tube interior from off-axis energy is play. Guessing X ∈ L^∞
from Leray energy is a failed close (B6). Two packets can share a tail and
disagree in the core.

Not a regularity proof. CosmoEvolution is not this lab.
"""

from __future__ import annotations

from typing import Any, Final

import numpy as np

from .shape_play import sparkline


ENERGY_OBJECT: Final[str] = """
        frequency                         physical
  outside = high-j tail              outside = r ≥ δ
  E_j  ▁▁▂▃█▂▁  you see this         e(r) off-axis  you see this
  X_j  ▁▂▅█▆▂▁  Bernstein fill       tube r < δ     live shape
       2^{2j} warps the pile              even-reflect of e_off
                                          is play, not NS
"""


def _rel_l2(guess: np.ndarray, truth: np.ndarray) -> float:
    num = float(np.linalg.norm(guess - truth))
    den = float(np.linalg.norm(truth))
    return num / max(den, 1e-30)


def play_bernstein(
    e_shells: tuple[float, ...] | None = None,
) -> dict[str, Any]:
    """Have E_j (kinetic in a shell) → fill X_j = 2^{2j} E_j."""
    e = np.array(e_shells if e_shells is not None else (0.18, 0.22, 0.16, 0.10, 0.06, 0.04, 0.03), dtype=float)
    js = np.arange(len(e), dtype=float)
    x = (2.0 ** (2.0 * js)) * e
    j_e = int(np.argmax(e))
    j_x = int(np.argmax(x))
    return {
        "shape": "SHELL-LADDER",
        "status": "identity",
        "not_a_lemma": False,
        "have": "E_j = ‖Δ_j u‖_2²  (the energy you can see, per shell)",
        "fill": "X_j = 2^{2j} E_j  (enstrophy of that shell)",
        "e_spark": sparkline(e, width=len(e)),
        "x_spark": sparkline(x, width=len(x)),
        "peak_energy_shell": j_e,
        "peak_enstrophy_shell": j_x,
        "warped": j_x != j_e,
        "notes": (
            "Seeing the energy pile fills the enstrophy pile. The weight 2^{2j} "
            "can move the peak to the right. Same object, warped texture. "
            "This does not fill occupation time or I_tube."
        ),
        "clip_still_open": "CLIP-B2-OCCUPATION",
    }


def play_guess_inside_from_outside(delta: float = 0.4, n: int = 160) -> dict[str, Any]:
    """You see e(r) for r≥δ. Even-reflect to guess the tube. Measure vs truth."""
    r = np.linspace(0.0, 1.2, n)
    inside = r < delta
    outside = r >= delta

    # Truth A: even across the wall — the symmetry the eye wants.
    s = np.abs(r - delta)
    even_truth = np.exp(-((s / 0.25) ** 2))
    # Truth B: energy lives in the tube (the NS-looking case).
    tube_truth = np.exp(-((r / 0.18) ** 2))

    def even_guess(truth: np.ndarray) -> np.ndarray:
        guess = truth.copy()
        r_out = r[outside]
        e_out = truth[outside]
        # For each interior point, sample the mirrored exterior.
        r_mirror = 2.0 * delta - r[inside]
        guess[inside] = np.interp(r_mirror, r_out, e_out, left=e_out[0], right=0.0)
        return guess

    even_g = even_guess(even_truth)
    tube_g = even_guess(tube_truth)
    even_err = _rel_l2(even_g[inside], even_truth[inside])
    tube_err = _rel_l2(tube_g[inside], tube_truth[inside])
    return {
        "shape": "ENERGY-BLOB",
        "status": "play",
        "not_a_lemma": True,
        "have": "e(r) on r≥δ  (the outside of the energy)",
        "guess": "even reflect across r=δ to fill the tube",
        "spark_outside": sparkline(even_truth[outside]),
        "spark_even_truth_in": sparkline(even_truth[inside]),
        "spark_even_guess_in": sparkline(even_g[inside]),
        "spark_tube_truth_in": sparkline(tube_truth[inside]),
        "spark_tube_guess_in": sparkline(tube_g[inside]),
        "error_when_even": even_err,
        "error_when_tube_concentrated": tube_err,
        "even_guess_works": even_err <= 0.15,
        "tube_guess_fails": tube_err >= 0.5,
        "extra_E": True,
        "buys": "a guess of the interior when the blob really is even",
        "does_not_buy": "I_tube, Γ, or the NS energy when it sits in the tube",
        "notes": (
            "If the energy blob is even, the outside fills the inside and you "
            "can see it. If the energy sits in the tube (the live NS cut), "
            "the outside is the cheap part and the guess of the interior is "
            "wrong. Track B lives in that second case."
        ),
        "clip_id": "CLIP-T3-OUTER",
    }


def play_shared_tail() -> dict[str, Any]:
    """Same high-j tail, two different cores — the outside does not name the packet."""
    tail = np.array([0.05, 0.03, 0.02], dtype=float)
    core_a = np.array([0.04, 0.08, 0.40, 0.18], dtype=float)
    core_b = np.array([0.22, 0.30, 0.12, 0.06], dtype=float)
    a = np.concatenate([core_a, tail])
    b = np.concatenate([core_b, tail])
    ja = int(np.argmax(a))
    jb = int(np.argmax(b))
    return {
        "shape": "SPECTRAL-TAIL",
        "status": "cannot_fill",
        "not_a_lemma": True,
        "have": "the outside of the energy in frequency (high-j tail)",
        "cannot_fill": "j* or σ = P_{j*}/X",
        "spark_a": sparkline(a, width=len(a)),
        "spark_b": sparkline(b, width=len(b)),
        "jstar_a": ja,
        "jstar_b": jb,
        "same_tail": True,
        "same_peak": ja == jb,
        "notes": (
            "Two packets, identical tails, different cores. Seeing the outside "
            "of the energy does not guess the packet. Occupation stays a clip."
        ),
        "clip_id": "CLIP-B2-OCCUPATION",
    }


def play_energy_tank() -> dict[str, Any]:
    """Leray energy is the tank you can see. The leak does not bound the height of X."""
    tstar = 1.0
    t = np.linspace(0.0, tstar - 1e-3, 400)
    x = (tstar - t) ** (-0.5)
    # Kinetic energy stays bounded in the Leray class; model it as constant.
    energy = np.ones_like(t)
    leak = x  # stand-in for a dissipation-like spike compatible with integrable X
    if hasattr(np, "trapezoid"):
        integ = float(np.trapezoid(x, t))
    else:
        integ = float(np.trapz(x, t))
    return {
        "shape": "ENERGY-TANK",
        "status": "cannot_fill",
        "not_a_lemma": True,
        "have": "kinetic energy E (bounded) and sometimes the leak",
        "cannot_fill": "X = ‖ω‖_2² ∈ L^∞",
        "spark_energy": sparkline(energy),
        "spark_enstrophy": sparkline(x),
        "truncated_integral_X": integ,
        "X_unbounded": True,
        "notes": (
            "You can see the energy tank. A spike in X can have finite area and "
            "infinite height. That is B6. Integrable enstrophy is not a shape bound."
        ),
        "clip_id": "CLIP-B6-SPIKE",
    }


def energy_play() -> dict[str, Any]:
    bern = play_bernstein()
    blob = play_guess_inside_from_outside()
    tail = play_shared_tail()
    tank = play_energy_tank()
    return {
        "title": "Energy as a visual object — see the outside, guess the shape",
        "not_a_regularity_proof": True,
        "rule": (
            "Put energy in a representative shape. If a weight or symmetry is "
            "in the object, the outside fills an inside (Bernstein). If you "
            "only put the symmetry in, it is play. Two cores can share a tail."
        ),
        "diagram": ENERGY_OBJECT,
        "identity": bern,
        "play": blob,
        "cannot_fill": [tail, tank],
        "gap": {
            "id": "GAP-ENERGY",
            "bernstein_fills_shell_enstrophy": True,
            "outside_fills_tube": False,
            "outside_fills_packet": False,
            "energy_fills_X_infty": False,
            "still_missing": (
                "CLIP-T3-WELD / CLIP-B4b-ITUBE — off-axis energy is not I_tube; "
                "CLIP-B6-SPIKE — seeing E does not bound X"
            ),
        },
        "next": (
            "Bernstein is the honest fill: energy ladder → enstrophy ladder. "
            "Do not guess the tube from the outside of the energy. "
            "Do not guess X ∈ L^∞ from the tank."
        ),
    }


def format_energy_play(report: dict[str, Any] | None = None) -> str:
    data = report or energy_play()
    bern = data["identity"]
    blob = data["play"]
    lines = [
        data["title"],
        "Not a regularity proof. " + data["rule"],
        "Energy object" + data["diagram"],
        "Identity (the energy you see fills an enstrophy shape)",
        f"  {bern['shape']}  [{bern['status']}]  have {bern['have']}",
        f"      fill {bern['fill']}",
        f"      E_j {bern['e_spark']}  peak j={bern['peak_energy_shell']}",
        f"      X_j {bern['x_spark']}  peak j={bern['peak_enstrophy_shell']}"
        f"  {'  (warped by 2^{2j})' if bern['warped'] else ''}",
        f"      {bern['notes']}",
        "",
        "Play (guess the inside from the outside of the energy)",
        f"  {blob['shape']}  [{blob['status']}]  extra E={blob['extra_E']}",
        f"      outside {blob['spark_outside']}",
        f"      even truth in {blob['spark_even_truth_in']}  guess {blob['spark_even_guess_in']}"
        f"  err={blob['error_when_even']:.3f}  "
        f"{'ok' if blob['even_guess_works'] else 'no'}",
        f"      tube truth in {blob['spark_tube_truth_in']}  guess {blob['spark_tube_guess_in']}"
        f"  err={blob['error_when_tube_concentrated']:.3f}  "
        f"{'fails as it should' if blob['tube_guess_fails'] else 'UNEXPECTED'}",
        f"      {blob['notes']}",
        "",
        "Cannot fill",
    ]
    for row in data["cannot_fill"]:
        lines.append(f"  {row['shape']}  [{row['status']}]  {row['clip_id']}")
        if row["shape"] == "SPECTRAL-TAIL":
            lines.append(f"      A {row['spark_a']}  j*={row['jstar_a']}")
            lines.append(f"      B {row['spark_b']}  j*={row['jstar_b']}")
            lines.append(f"      same tail, same peak? {row['same_peak']}")
        else:
            lines.append(f"      E {row['spark_energy']}")
            lines.append(f"      X {row['spark_enstrophy']}  unbounded={row['X_unbounded']}")
        lines.append(f"      {row['notes']}")
    gap = data["gap"]
    lines.append("")
    lines.append(
        f"GAP-ENERGY: Bernstein fill? {gap['bernstein_fills_shell_enstrophy']}. "
        f"Outside fills tube? {gap['outside_fills_tube']}. "
        f"Energy bounds X? {gap['energy_fills_X_infty']}."
    )
    lines.append("  still missing: " + gap["still_missing"])
    lines.append("Next: " + data["next"])
    return "\n".join(lines)
