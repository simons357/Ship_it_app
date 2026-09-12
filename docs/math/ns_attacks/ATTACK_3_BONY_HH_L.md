# ATTACK 3 — Bony HH channel diagnostic (not strictly HH→L)

**Status:** diagnostic only. **NS is not solved.**  
**SoT lock:** Attack 3 is **NOT** a strict HH→L estimate.

## Target

Partition the bilinear form driving \(T_c\) (alias \(\mathcal{T}_c\)) into parent-wavevector channels HH / HL / LL (Bony-style). Prior analytic note: the **HH** channel is the live bottleneck for closing a clean product bound toward
\[
|T_c|\le C\|u\|_2 X^{3/2}.
\]

## Precision — not strictly HH→L

**CRITICAL bookkeeping:** Attack 3 filters **high-frequency inputs** (parent wavevectors in the HH / HL / LL split). It does **not** restrict the **output** frequency of \(B(u,u)\) / \(T_c\) to a low shell.

| Claim | Verdict |
|-------|---------|
| Attack 3 is a strict HH→L (high×high → low) map | **FALSE** |
| Attack 3 diagnoses HH as an input-channel bottleneck | **TRUE** (diagnostic) |
| Kill criterion for Lemma★ uses HH→L-only \(T_c\) | **FALSE** — use **complete** signed \(T_c\) |

Naming residue: docs/scripts still say “Bony HH→L” historically; that label means “HH-channel product gap,” **not** a proved high→low output restriction. For genuine HH→L as an **output** subfamily in exact-shell closing, see Attack 9B with \(\beta<\alpha\) ([`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md)).

## Method

`scripts/ns_attacks/attack3_bony_hh_l.py`.

## Live result (2026-09-10)

HH is the sole channel on a pure high triad; random HH frac p90 \(\approx0.51\). **No closure.** See `attack3.json`.

**NS not solved.** Kill lane **LIVE**.
