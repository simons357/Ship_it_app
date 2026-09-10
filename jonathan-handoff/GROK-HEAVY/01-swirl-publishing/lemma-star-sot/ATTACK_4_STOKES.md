# ATTACK 4 — Stokes-moment calculus

**Status:** identity + absorption diagnostic. **NS is not solved.**

## Target

Sanity-check Foias–Temam moments
\[
X=\|A^{1/2}u\|_2^2,\quad Y=\|Au\|_2^2,\quad Z=\|A^{3/2}u\|_2^2,\quad\Lambda=Y/X,\quad\mathcal D_s=Z-\Lambda Y\ge0,
\]
homogeneity under \(u\mapsto Bu\), and the necessity of a remainder beyond \(\theta\nu\mathcal D_s\).

## Method

`scripts/ns_attacks/attack4_stokes.py`.

## Live result (2026-09-10)

\(\mathcal D_s\ge0\) identity OK; homogeneity OK; pure viscous absorption insufficient. See `attack4.json`.
