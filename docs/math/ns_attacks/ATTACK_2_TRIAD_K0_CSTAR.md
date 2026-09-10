# ATTACK 2 — Triad / K=0 kill / \(C_* X^{3/2}\Lambda\)

**Status:** numeric probe only. **NS is not solved.**

## Targets

1. **K=0 absorption** \(\mathfrak T_c\le\theta\nu\mathcal D_s\): expected **DEAD** (ratio \(\mathfrak T_c/\mathcal D_s\) grows with amplitude).
2. **Survivor** \(\mathfrak T_c\le\theta\nu\mathcal D_s+C_* X^{3/2}\Lambda\) with \(K\sim\sqrt{X}\), Leray-integrable if \(\int X<\infty\).

## Method

Fixed-shape high triad amplitude sweep; \(X=1\) shape scan; scale-separated triads.
Script: `scripts/ns_attacks/attack2_triad_k0_cstar.py`.

## Live result (2026-09-10)

**K=0 DEAD** (\(\lvert T_c\rvert/\mathcal D_s\sim B\)). **\(C_*\approx0.004058\)** amp-invariant on fixed triad. See `attack2.json`.
