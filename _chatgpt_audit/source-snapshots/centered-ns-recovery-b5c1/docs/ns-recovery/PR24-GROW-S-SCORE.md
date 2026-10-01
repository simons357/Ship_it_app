# PR #24 grow-\(s\) landing — scored on this book

**Date:** 12 September 2026  
**Source (do not merge books):** https://github.com/simons357/Ship_it_app/pull/24  
Pages there: `docs/ATTACK-9D-GROW-S.md`, `docs/LEMMA-STAR-REASON.md`, `docs/NEED-STAR-HH-L-DUAL.md`  
JSON there: `results/attack9b_grow_s/grow_s.json`

**This book does not recompute the sweep.** Numbers below are checked against that JSON. **NS not solved. Lemma★ OPEN.**

---

## 1. Attack 9D — grow \(s\) (secondary)

Same \(B\) as 9B. Target \(\|\Pi_\beta B\|_2\le C\alpha\beta^{-1/2}\|w\|_2^2\) iff \(\sup K<\infty\). Growing input and output, full complex polarizations, \(|k|\) kept. Fixed-output \(\Theta(m^2)\) excluded. Designed \(\Theta(m^2)\) stays dead. `attack9d_theta_m2_locked_phase.py` was not written.

Seed 1390, \(k_{\max}=8\): 2084 input fields, 39853 occupied \((\alpha,\beta)\) rows.

| Quantity | Value |
|---|---|
| \(\max K\) | \(0.45583\) at \((\alpha,\beta)=(16,32)\), \(s=4\), \(m=4\) |
| \(\max\sqrt{K}\) | \(0.67515\) |
| \(\max s\) | 192 |
| \(\max m\) | 120 |
| Pairs / CS / \(K\le 16s\) fails | 0 / 0 / 0 |
| \(\max K\) on \(s\le 8\) | \(0.456\) |
| \(\max K\) on \(s\ge 24\) | \(0.239\) |

Larger occupancy did not raise \(K\) on this draw.

**Do not merge** with the aligned 9B search \(\max K\approx 0.641\) at \((4,8)\). Different probe (random polarizations / growing supports vs aligned closer). A finite max is not \(C_0\). This draw **did not kill ★**.

Setup lock here: [`docs/math/ns_attacks/ATTACK_9D_SETUP.md`](../math/ns_attacks/ATTACK_9D_SETUP.md).

## 2. The ★ reason — map, not a theorem

Keep \(\mathrm{Im}\). HH→L is the dangerous channel (weight \(\sim\beta\cdot\alpha\); Attack 12 vertex carries \(\sqrt{\beta}\)). Cheap CS returns occupancy — the same hole as \(K\le 16s\).

Until that sentence is a theorem, or \(\mathcal R_\star\to\infty\), **leftover 4 stays OPEN**. That leftover is Need★: the signed dual on HH→L after gap-cancel \(T_c=M-\Lambda N\). Still **MISSING**. Do not invent it. Do not turn Attack 12’s table into the sentence.

## Status after this landing

| Item | This book |
|---|---|
| Grow-\(s\) draw (seed 1390, \(k_{\max}=8\)) | **Scored.** Finite. Not a kill. |
| Aligned 9B \(\max K\approx 0.641\) | **Already scored.** Do not redo. Do not merge. |
| Need★ signed dual | **Still MISSING.** Primary. |
| Soft X | Silent |
| Kill lane | **LIVE** |

DA path: this 9D draw has landed. Score it as a finite sample. Do not send a close.

Board: [`WHAT-ELSE.md`](WHAT-ELSE.md).
