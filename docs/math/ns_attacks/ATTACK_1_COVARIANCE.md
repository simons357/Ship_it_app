# ATTACK 1 — Covariance / Lemma★ amplitude survival

**Status:** numeric probe only. **NS is not solved.**

## Target

Lemma★ claims a geometric constant \(C_0\) such that
\[
\mathfrak T_c \le \theta\nu(Z-\Lambda Y)+C_0\nu^{-1}\|u\|_2^2 X\Lambda.
\]
Attack 1 asks whether the dimensionless ratio
\[
R_\star=\frac{\mathfrak T_c}{\|u\|_2^2 X\Lambda}
\]
stays uniformly bounded under amplitude scaling \(u\mapsto Bu\), phase rotations, and random Galerkin fields.

## Method

`scripts/ns_attacks/attack1_covariance.py` — Fourier Galerkin Stokes moments on \(\mathbb{T}^3\).

## Kill criterion

If \(\sup|R_\star|\to\infty\) on a controlled family (especially \(B\to\infty\) at fixed shape), Lemma★’s uniform \(C_0\) is **KILLED**.

## Live result (2026-09-10)

**SURVIVE numeric (NOT proof).** Post-Young \(R_\star\) falls as \(B\uparrow\). Pre-Young phase diam \(\approx0.155\). See `/opt/cursor/artifacts/ns_five_lane_2026-09-10/attack1.json` and `ATTACK_SYNTHESIS_SIMULTANEOUS.md`.
