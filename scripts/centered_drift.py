"""Centered-drift algebra: identities and the formal DI.

Not a close. Unrestricted star stays killed. K(t) is a remainder
coefficient, not a term in the PDE.
"""

from __future__ import annotations

from fractions import Fraction

from centered_barycenter import log_lambda_prime, modes_to_moments


def spectral_cauchy(e: Fraction, x: Fraction, y: Fraction) -> bool:
    """X^2 <= E Y  =>  X <= E Lambda."""
    return x * x <= e * y


def lambda_prime_ceiling(k: Fraction) -> Fraction:
    """If T_c <= θν D_s + K X with θ<1, then Λ' <= 2K."""
    return 2 * k


def y_remainder_log_ceiling(k_y: Fraction) -> Fraction:
    """If T_c <= θν D_s + K_Y Y with θ<1, then (log Λ)' <= 2 K_Y."""
    return 2 * k_y


def tautological_k(t_c: Fraction, theta_nu_ds: Fraction, x: Fraction) -> Fraction:
    """K = (T_c - θν D_s)_+ / X. Makes the estimate an identity."""
    if x <= 0:
        raise ValueError("X must be positive")
    gap = t_c - theta_nu_ds
    return gap / x if gap > 0 else Fraction(0)


def two_mode_moments() -> dict[str, float]:
    """Sanity: D_s matches the factored form."""
    return modes_to_moments([1.0, 4.0], [3.0, 1.0])


def identity_matches_log_derivative() -> bool:
    t_c, nu, d_s, y = 2.0, 1.0, 3.0, 5.0
    return abs(log_lambda_prime(t_c, nu, d_s, y) - 2.0 * (t_c - nu * d_s) / y) < 1e-15


def main() -> None:
    m = two_mode_moments()
    print("Lambda", m["Lambda"], "D_s", m["D_s"], "D_s_fact", m["D_s_fact"])
    print("cauchy", spectral_cauchy(Fraction(4), Fraction(2), Fraction(2)))
    print("Lambda' ceiling K=3", lambda_prime_ceiling(Fraction(3)))
    print("tautological K", tautological_k(Fraction(5), Fraction(1), Fraction(2)))
    print("log identity", identity_matches_log_derivative())


if __name__ == "__main__":
    main()
