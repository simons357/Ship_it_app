"""Route A locks: pairing is cubic; L^inf a_+ is BKM; energy-linear dies.

Not a close. No 9D sweep. Theorem H stays withdrawn.
"""

from __future__ import annotations

from fractions import Fraction


def pairing_le_a_plus_z(a_plus: int, z: int) -> bool:
    """∫(α)_+ |Δ_j ω|² ≤ a_+ Z_j by definition of a_+."""
    pairing_majorant = a_plus * z
    return pairing_majorant == a_plus * z and pairing_majorant >= 0


def amplitude_powers(amp: int) -> dict[str, int]:
    """u = A w. Pairing ~ A^3, a_+ Z ~ A^3, energy ~ A^2."""
    return {
        "pairing": amp**3,
        "a_plus_Z": amp * (amp**2),
        "energy": amp**2,
    }


def energy_linear_fails_amplitude(amp_small: int, amp_large: int) -> bool:
    a = amplitude_powers(amp_small)
    b = amplitude_powers(amp_large)
    return (b["pairing"] / b["energy"]) > (a["pairing"] / a["energy"])


def tjj_e_false_t_over_d_sq(lam: int) -> Fraction:
    """Same scaling as C1: T/D ~ λ^{1/2}, stored as (T/D)^2 = λ."""
    return Fraction(lam)


def embedding_a_plus_is_bkm() -> bool:
    """a_+ ≤ ||∇u_loc||_∞ is the BKM packaging, not an a priori."""
    return True


def tautological_k(pairing: int, rem: int, z: int) -> int:
    """K = (P + C − εν D)_+ / Z is an identity, not a proof."""
    if z <= 0:
        raise ValueError("Z must be positive")
    return max(pairing + rem, 0) // z


def main() -> None:
    print("pairing ≤ a_+ Z", pairing_le_a_plus_z(3, 4))
    print("amplitude A=3", amplitude_powers(3))
    print("energy-linear fails", energy_linear_fails_amplitude(2, 6))
    print("E-false λ=16", tjj_e_false_t_over_d_sq(16))
    print("embedding is BKM", embedding_a_plus_is_bkm())
    print("tautological K", tautological_k(12, 0, 4))


if __name__ == "__main__":
    main()
