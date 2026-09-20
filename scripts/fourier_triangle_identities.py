#!/usr/bin/env python3
"""Exact Fourier-triangle identities. Not a 9D sweep. Not a bound.

Checks the seated pair geometry:
  p + q = k
  equal-length  => k·p = k·q = |k|^2 / 2
  unequal-length => k·p = (|k|^2 + |p|^2 - |q|^2) / 2  (polarization identity)
  Leray kills the k-component
  signed Im vs absolute value are not interchangeable

Run: python3 scripts/fourier_triangle_identities.py
"""

from __future__ import annotations

import math
import sys


def dot(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def nrm2(a: tuple[int, int, int]) -> int:
    return dot(a, a)


def add(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def leray(k: tuple[int, int, int], v: tuple[float, float, float]) -> tuple[float, float, float]:
    kk = float(nrm2(k))
    if kk == 0.0:
        raise ValueError("k = 0")
    proj = (k[0] * v[0] + k[1] * v[1] + k[2] * v[2]) / kk
    return (v[0] - proj * k[0], v[1] - proj * k[1], v[2] - proj * k[2])


def assert_equal_length() -> list[str]:
    """Integer triangles with |p|^2 = |q|^2."""
    triples = [
        ((2, 0, 0), (0, 2, 0)),
        ((1, 1, 0), (1, -1, 0)),
        ((2, 1, 0), (-1, 2, 0)),
        ((3, 0, 0), (0, 3, 0)),
    ]
    lines = []
    for p, q in triples:
        if nrm2(p) != nrm2(q):
            raise AssertionError("fixture is not equal-length")
        k = add(p, q)
        alpha, beta = nrm2(p), nrm2(k)
        if beta > 4 * alpha:
            raise AssertionError("vacuous pair")
        if dot(k, p) != beta // 2 or dot(k, q) != beta // 2:
            raise AssertionError(f"equal-length cancel failed on {p},{q}")
        if 2 * dot(k, p) != beta:
            raise AssertionError("β not even in the integer pairing")
        k_perp2 = beta - (beta * beta) / (4.0 * alpha)
        expect = beta * (1.0 - beta / (4.0 * alpha))
        if abs(k_perp2 - expect) > 1e-12:
            raise AssertionError("|k_perp|^2 mismatch")
        lines.append(
            f"  p={p} q={q} k={k}  α={alpha} β={beta}  "
            f"k·p=k·q={dot(k, p)}  |k_⊥|²={k_perp2:.6f}"
        )
    return lines


def assert_unequal_length_defect() -> str:
    p, q = (1, 0, 0), (1, 1, 0)
    k = add(p, q)
    beta = nrm2(k)
    left = dot(k, p)
    right = (beta + nrm2(p) - nrm2(q)) / 2.0
    if abs(left - right) > 1e-12:
        raise AssertionError("polarization identity failed")
    if left == beta / 2.0 and nrm2(p) != nrm2(q):
        raise AssertionError("unexpected equal-length on unequal fixture")
    return (
        f"  p={p} q={q} k={k}  |p|²={nrm2(p)} |q|²={nrm2(q)} β={beta}  "
        f"k·p={left}  β/2={beta/2.0}  defect={left - beta/2.0}"
    )


def assert_leray_kills_parallel() -> str:
    k = (2, 1, 0)
    v = (4.0, 2.0, 3.0)  # has a component along k
    pv = leray(k, v)
    if abs(k[0] * pv[0] + k[1] * pv[1] + k[2] * pv[2]) > 1e-12:
        raise AssertionError("Leray residual not ⊥ k")
    return f"  P_k v ⊥ k on k={k}"


def assert_im_is_not_abs() -> str:
    """Two opposite-phase contributions cancel in Im and add in |·|."""
    a, b = 0.3 + 0.4j, 0.3 - 0.4j  # conjugates: Im(a)+Im(b)=0, |a|+|b|>0
    im_sum = a.imag + b.imag
    abs_sum = abs(a) + abs(b)
    if abs(im_sum) > 1e-15:
        raise AssertionError("fixture Im sum should vanish")
    if abs_sum <= 0.0:
        raise AssertionError("abs sum should be positive")
    return f"  Im-sum={im_sum:.2e}  abs-sum={abs_sum:.6f}  (signs cancel; abs does not)"


def main() -> int:
    print("equal-length (EXACT):")
    for line in assert_equal_length():
        print(line)
    print("unequal-length defect (EXACT mismatch):")
    print(assert_unequal_length_defect())
    print("Leray (EXACT):")
    print(assert_leray_kills_parallel())
    print("signed vs absolute (EXACT distinction):")
    print(assert_im_is_not_abs())
    print()
    print("VERDICT")
    print("  Per-triangle equal-length identities sit.")
    print("  Unequal-length legs lose k·p = β/2.")
    print("  Im-sum is not the abs-sum.")
    print("  No I3 object is defined here.")
    print("  No time-dependent bound is claimed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
