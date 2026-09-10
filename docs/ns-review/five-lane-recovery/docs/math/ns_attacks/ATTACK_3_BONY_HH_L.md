# ATTACK 3 — Bony HH channel diagnostic (not strictly HH→L)

**Status:** diagnostic only. **NS is not solved.**  
**Bookkeeping:** [`FIVE-LANE-BOOKKEEPING.md`](../../../../FIVE-LANE-BOOKKEEPING.md).

## Target

Partition the bilinear form driving \(\mathfrak T_c\) into parent-wavevector channels HH / HL / LL (Bony-style). Prior analytic note: an **HH→L** channel blocks a clean product bound toward
\[
|\mathfrak T_c|\le C\|u\|_2 X^{3/2}.
\]

## Precision lock (USER)

| Claim | Verdict |
|-------|---------|
| Attack 3 filters high-frequency **inputs** (parents vs cutoff) | **TRUE** |
| Attack 3 restricts bilinear **output** to a low shell | **FALSE** |
| Therefore the probe is **strictly HH→L** | **FALSE** — **not strictly HH→L** |
| Kill decisions may use HH→L-only \(T_c\) | **FALSE** — use **complete signed** \(T_c\) |

The script name / historical label “HH→L” records the **analytic bottleneck story**. The implemented Galerkin split only tags **parent** scales; it does **not** enforce low-frequency **output**. Do not cite Attack 3 numerics as a proved HH→L map.

## Method

`scripts/ns_attacks/attack3_bony_hh_l.py` (`bony_channel_split` / `Tc_by_channel`).

## Live result (2026-09-10)

HH is the sole channel on a pure high triad; random HH frac p90 \(\approx0.51\). **No closure.** See `attack3.json`.

## Related (shell transfer direction)

For exact-shell Attack **9B**, a pair with \(\beta>\alpha\) is **higher-shell** transfer, **not** HH→L. Genuine HH→L subfamily needs \(\beta<\alpha\). See [`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md).
