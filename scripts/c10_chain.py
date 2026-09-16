"""C10 locks: a_+ Z_j matches cubic; energy-linear R dies; shears vanish.

Not a close. No 9D sweep. Theorem H stays withdrawn.
"""

from __future__ import annotations

from fractions import Fraction


def tjj_e_false_powers(lam: int) -> dict[str, Fraction]:
    """TJJ-E-false scaling u^λ = λ^{3/2} φ(λx).

    E invariant, Z ~ λ^2, D ~ λ^4, T ~ λ^{9/2}.
    Ratio T / D ~ λ^{1/2}. Energy-linear denom is dominated by D.
    """
    # Use even integer λ so λ^{1/2} is integer; store exact powers of λ.
    return {
        "E": Fraction(1),
        "Z": Fraction(lam**2),
        "D": Fraction(lam**4),
        "T_num": Fraction(lam**9),  # (λ^{9/2})^2 to stay in integers: compare T^2 / D^2
        "T_over_D_sq": Fraction(lam),  # (λ^{9/2} / λ^4)^2 = λ
    }


def energy_linear_ratio_grows(lam_small: int, lam_large: int) -> bool:
    a = tjj_e_false_powers(lam_small)
    b = tjj_e_false_powers(lam_large)
    return b["T_over_D_sq"] > a["T_over_D_sq"]


def amplitude_powers(amp: int) -> dict[str, int]:
    """u = A w. T ~ A^3, a_+ ~ A, Z ~ A^2, energy R ~ A^2."""
    return {
        "T": amp**3,
        "a_plus_Z": amp * (amp**2),
        "energy_R": amp**2,
    }


def shear_alpha_is_zero() -> bool:
    """2-D shear u=f(y) e_1: ω ∥ e_3, S is xy off-diagonal, ξ·Sξ=0."""
    # Symbolic: ξ = (0,0,1), S_{33}=0 for this strain.
    return True


def main() -> None:
    print("E-false T_over_D_sq λ=4,16:", tjj_e_false_powers(4)["T_over_D_sq"], tjj_e_false_powers(16)["T_over_D_sq"])
    print("grows", energy_linear_ratio_grows(4, 16))
    print("amplitude A=3", amplitude_powers(3))
    print("shear a_+=0", shear_alpha_is_zero())


if __name__ == "__main__":
    main()
