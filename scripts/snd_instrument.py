"""SND instrument: frozen-shell diagnostics. No persistence claim.

Partition: X_j masses labeled by integer shells. J, rho, j_*, packet,
tail, F_j, barycenter, peak migration. Not a theorem.
"""

from __future__ import annotations

from fractions import Fraction
from math import log2

from snd_h_review import PACKET_N, PACKET_Q, shell_weights


def diagnose(masses: dict[int, Fraction]) -> dict:
    """Exact diagnostics on a frozen mass vector. Missing shells are zero."""
    if not masses:
        raise ValueError("empty mass vector")
    x = sum(masses.values())
    if x <= 0:
        raise ValueError("X must be positive")
    j_star = min(j for j, v in masses.items() if v == max(masses.values()))
    peak = masses[j_star]
    rho = peak / x
    packet = sum(masses.get(j, Fraction(0)) for j in (j_star - 1, j_star, j_star + 1))
    sigma = packet / x
    jbar = sum(j * v for j, v in masses.items()) / x
    tail = sum(v for j, v in masses.items() if j > j_star) / x
    gamma = envelope_gamma(masses, j_star, peak)
    return {
        "X": x,
        "J": peak,
        "rho": rho,
        "j_star": j_star,
        "P": packet,
        "sigma": sigma,
        "j_bar": jbar,
        "tail_mass": tail,
        "gamma": gamma,
        "outside": 1 - rho,
    }


def envelope_gamma(masses: dict[int, Fraction], j_star: int, peak: Fraction) -> Fraction:
    """Largest γ >= 0 with X_j <= J * 2^{-γ(j-j_*)} on listed j > j_*.

    γ = 0 if the tail does not decay, or if there is no tail.
    """
    if peak <= 0:
        return Fraction(0)
    gamma = None
    for j, v in masses.items():
        if j <= j_star or v <= 0:
            continue
        # v/J <= 2^{-γ dj}  <=>  γ <= -log2(v/J) / dj
        ratio = float(v / peak)
        dj = j - j_star
        if ratio >= 1:
            return Fraction(0)
        bound = -log2(ratio) / dj
        gamma = bound if gamma is None else min(gamma, bound)
    if gamma is None:
        return Fraction(0)
    # Keep a short exact-ish Fraction from a binary expansion.
    return Fraction(gamma).limit_denominator(10_000)


def migrate(before: dict, after: dict) -> dict:
    return {
        "delta_j_star": after["j_star"] - before["j_star"],
        "delta_j_bar": after["j_bar"] - before["j_bar"],
    }


def packet_shear_masses(q: Fraction = PACKET_Q, n: int = PACKET_N, k: int = 24) -> dict[int, Fraction]:
    """Audit shear: peak at 0, N equal mid shells, one far shell at K."""
    a, b, _x, _j = shell_weights(q, n)
    masses = {0: a}
    for j in range(1, n):
        masses[j] = b
    masses[k] = b
    return masses


def equal_shell_masses(length: int, j0: int = 0) -> dict[int, Fraction]:
    return {j0 + i: Fraction(1) for i in range(length)}


def high_tail_one_peak(j_star: int, j_tail: int, rho: Fraction) -> dict[int, Fraction]:
    """One peak plus one far shell. rho can be large while j_tail is arbitrary."""
    if not (0 < rho < 1):
        raise ValueError("rho in (0,1)")
    if j_tail <= j_star:
        raise ValueError("tail must sit above the peak")
    return {j_star: rho, j_tail: 1 - rho}


def shear_flux_is_zero(masses: dict[int, Fraction]) -> dict[int, Fraction]:
    return {j: Fraction(0) for j in masses}


def main() -> None:
    shear = diagnose(packet_shear_masses())
    print("shear", {k: shear[k] for k in ("rho", "j_star", "tail_mass", "gamma")})
    eq = diagnose(equal_shell_masses(11))
    print("v_L", {k: eq[k] for k in ("rho", "j_star")})
    tail = diagnose(high_tail_one_peak(2, 40, Fraction(9, 10)))
    print("high-tail", {k: tail[k] for k in ("rho", "j_star", "tail_mass", "gamma")})
    moved = diagnose({2: Fraction(1), 5: Fraction(3)})
    print("migrate", migrate(shear, moved))


if __name__ == "__main__":
    main()
