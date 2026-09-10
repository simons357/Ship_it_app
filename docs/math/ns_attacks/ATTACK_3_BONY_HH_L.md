# ATTACK 3 — Bony HH→L bottleneck

**Status:** diagnostic only. **NS is not solved.**

The older target
\[
|\mathfrak T_c|\le C\|u\|_2 X^{3/2}
\]
is **false as a universal estimate**. Under \(u=av\) the
left side scales as \(a^3\) and the right as \(a^4\). For any
field with \(T_c(v)\ne 0\), \(a\to 0\) contradicts it.
Discarded by algebra. Not an open product gap toward ★.
Do not apply this death to Attack-2
\(|T_c|\le C_* X^{3/2}\Lambda\).

## What remains

Partition the bilinear form driving \(\mathfrak T_c\) into
parent-wavevector channels HH / HL / LL (Bony-style).
HH→L is a **diagnostic of channels**. It is not a path to
the false \(a^4\) bound, and it is not a proof of
\(\sup\mathcal R_\star<\infty\).

Working claim: [`LEMMA_STAR_CANONICAL.md`](./LEMMA_STAR_CANONICAL.md).

## Method

`scripts/ns_attacks/attack3_bony_hh_l.py`.

## Live result (2026-09-10)

HH is the sole channel on a pure high triad; random HH frac p90 \(\approx0.51\).
Channel split only. See `attack3.json`.
