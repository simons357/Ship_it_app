# ATTACK 3 — Bony HH→L bottleneck

**Status:** diagnostic only. **NS is not solved.**

## Target

Partition the bilinear form driving \(\mathfrak T_c\) into parent-wavevector channels HH / HL / LL (Bony-style). Prior analytic note: HH→L is the channel that blocks a clean product bound toward
\[
|\mathfrak T_c|\le C\|u\|_2 X^{3/2}.
\]

## Method

`scripts/ns_attacks/attack3_bony_hh_l.py`.

## Live result (2026-09-10)

HH is the sole channel on a pure high triad; random HH frac p90 \(\approx0.51\). **No closure.** See `attack3.json`.
