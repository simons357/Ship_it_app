"""Locks for the repaired F_j / D+ρ assembly.

Not a close. Theorem H stays withdrawn.
A.2 sits. A.3 is an upper Dini bound, not a floor.
"""

from __future__ import annotations

from fractions import Fraction

from snd_h_review import (
    PACKET_N,
    PACKET_Q,
    PACKET_TABLE,
    shell_weights,
)


def xdot_shear(
    nu: Fraction,
    a: Fraction,
    b: Fraction,
    n: int,
    k: int,
) -> Fraction:
    """Exact-mode Ẋ = -2ν Σ 4^j X_j on the audit shear family at t=0."""
    low = sum((4**j for j in range(1, n)), Fraction(0))
    return -2 * nu * (a * 1 + b * (low + 4**k))


def rho_dot_exact_mode(
    nu: Fraction,
    q: Fraction,
    n: int,
    k: int,
) -> tuple[Fraction, Fraction]:
    """Peak-shell identity at t=0, j*=0 unique.

    Returns (ρ̇, A.3 RHS with F_j=0 and κ=1).
    """
    a, b, x, j = shell_weights(q, n)
    rho = j / x
    xdot = xdot_shear(nu, a, b, n, k)
    # J̇ = Ẋ_0 = -2ν a, X=q.
    jdot = -2 * nu * a
    rho_dot = jdot / x - rho * xdot / x
    # A.3 with F_j=0, κ=1, λ_{j*}=4^0=1:
    # D+ρ ≤ -2ν ρ - ρ Ẋ/X
    rhs = -2 * nu * rho - rho * xdot / x
    return rho_dot, rhs


def a2_scales(a: Fraction) -> tuple[Fraction, Fraction]:
    """A.2 RHS at fixed shape: quadratic in A if M fixed; cubic if M∝A².

    Returns (quadratic_factor, cubic_factor) as A^2 and A^3.
    """
    return a**2, a**3


def equal_shell_rho(l: int) -> Fraction:
    """Audit §6: v_L has ρ(0)=1/L at fixed total enstrophy."""
    return Fraction(1, l)


def main() -> None:
    nu = Fraction(1)
    a, b, x, j = shell_weights(PACKET_Q, PACKET_N)
    print(f"a={a} b={b} X={x} J={j} rho={j / x}")
    for k in PACKET_TABLE:
        left, right = rho_dot_exact_mode(nu, PACKET_Q, PACKET_N, k)
        print(f"K={k} rho_dot={left} A3_F0={right} equal={left == right}")
    print("A.2 quadratic/cubic:", a2_scales(Fraction(2)))
    print("v_L rho L=11:", equal_shell_rho(11))


if __name__ == "__main__":
    main()
