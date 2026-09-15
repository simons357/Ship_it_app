"""Shear-family arithmetic for the SND-H review.

Locks the exact shell weights and the displayed-ratio table
from the 15 September 2026 specialist packet. Not a close.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50

# Normalized torus (R/2πZ)^3. Packet conventions.
# |sin(n y)|_2^2 = 1/2.


def shell_weights(q: Fraction, n: int) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """a = 2q/(N+2), b = q/(N+2), X = a + N b, J = a."""
    a = Fraction(2 * q, n + 2)
    b = Fraction(q, n + 2)
    x = a + n * b
    j = a
    return a, b, x, j


def viscous_tail(nu: Fraction, b: Fraction, n: int, k: int) -> Fraction:
    """S_K = ν b (sum_{j=1}^{N-1} 4^j + 4^K)."""
    low = sum((4**j for j in range(1, n)), Fraction(0))
    return nu * b * (low + 4**k)


def displayed_ratio(
    nu: Fraction,
    q: Fraction,
    n: int,
    k: int,
) -> Decimal:
    """|Π_{j_*}| / (ν 4^{j_*} J + sqrt(X D)) on the shear family.

    j_* = 0, Π = -S_K, D = ν a + S_K.
    """
    a, b, x, j = shell_weights(q, n)
    s = viscous_tail(nu, b, n, k)
    d = nu * a + s
    denom = nu * (4**0) * j + (x * d) ** Fraction(1, 2)
    # Exact square root is not rational; evaluate at high precision.
    s_dec = Decimal(s.numerator) / Decimal(s.denominator)
    a_dec = Decimal(a.numerator) / Decimal(a.denominator)
    x_dec = Decimal(x.numerator) / Decimal(x.denominator)
    d_dec = Decimal(d.numerator) / Decimal(d.denominator)
    den_dec = a_dec + (x_dec * d_dec).sqrt()
    return s_dec / den_dec


# Packet table: ν = q = 1, N = 20, ρ_0 = 0.1.
PACKET_NU = Fraction(1)
PACKET_Q = Fraction(1)
PACKET_N = 20
PACKET_TABLE = {
    24: Decimal("3.57924234e6"),
    28: Decimal("5.72307770e7"),
    32: Decimal("9.15690113e8"),
}


def packet_row(k: int) -> Decimal:
    return displayed_ratio(PACKET_NU, PACKET_Q, PACKET_N, k)


def main() -> None:
    a, b, x, j = shell_weights(PACKET_Q, PACKET_N)
    print(f"a={a} b={b} X={x} J={j} rho={j / x}")
    print("K  ratio")
    for k in PACKET_TABLE:
        r = packet_row(k)
        print(f"{k}  {r:.11e}")


if __name__ == "__main__":
    main()
