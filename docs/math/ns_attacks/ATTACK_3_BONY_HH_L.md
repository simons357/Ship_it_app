# ATTACK 3 — Bony HH→L bottleneck

**Status:** diagnostic only. **NS is not solved.**

## Target

Partition the bilinear form driving \(\mathfrak T_c\) into parent-wavevector channels HH / HL / LL (Bony-style). Prior analytic note proposed a product bound toward
\[
|T_c|\le C\|u\|_2 X^{3/2}.
\]
That estimate is **false as a universal bound** (left side \(\sim a^3\), right side \(\sim a^4\) under \(u=av\)). Discard it. HH→L remains a diagnostic split of complete signed \(T_c\), not a map that closes ★.

## Method

`scripts/ns_attacks/attack3_bony_hh_l.py`.

## Live result (2026-09-10)

HH is the sole channel on a pure high triad; random HH frac p90 \(\approx0.51\). **No closure.** See `attack3.json`.
