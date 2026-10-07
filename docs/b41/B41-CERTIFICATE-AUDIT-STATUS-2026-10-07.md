# B41 certificate audit — status and next moves

**Date:** 7 October 2026  
**Object:** Fixed finite channel-quotient network (G3 / B41 starvation-ray geometry)  
**Not claimed:** evolving NSE solutions, classical regularity, DA stamp of the note

---

## Where we are

### Already done (editorial)
Current B41 includes:
- Explicit maximization definition of \(\Gamma(t)\)
- Range \(0<t\le\min(C_7,C_8)/c_2\)
- Weighted asymptotic refinement; \(2-\sqrt3\) = equal-weight case

### Certificate audit (reported from Exact-Certificate conversation)

| Check | Result |
|---|---|
| \(y_A\) certificate | **PASS** vs rationalized JSON |
| \(y_B\) certificate | **PASS** |
| Both signed cycle identities | **PASS** |
| Six T2 phase errors (upper bound) | **PASS** |
| All 20 matrix rows vs r2 after column/row/sign alignment | **PASS** |
| Four phase **targets** vs r2 lock | **MISMATCH by \(\pi\)** — mode-phase shift cannot remove under this alignment |

**Consequence:** B41’s independent JSON starvation-ray calculation **survives**.  
We **cannot** transfer **G6-A** through an asserted identity with the r2 lock.

Artifact named in that conversation: `B41-Exact-Certificate-Audit-2026-10-07.zip`  
(TSVs recovered from `PACKET.md`; full hashes matched original locks there.)

### In this repo branch (`cursor/b41-phase-convention-0cc5`)

Imported computed-evidence pair from PR #144 (`data/R2/`):

| File | Role |
|---|---|
| `M.tsv` | 20×12 integer \(\Gamma\) |
| `b_exact.tsv` | targets as turn fractions \(b/(2\pi)\) |
| `g3_corrected_channel_quotient.json` | G3 gate; convention \(b=\pi/2-\arg(g_{\mathrm{sym}})\) |
| `scripts/r2_read_only_verifier.py` | read-only identities + G3 match |

Read-only verifier on this import: **ok** (`identities_ok`, `g3_match_ok`).  
Status remains **`COMPUTED_EVIDENCE_ONLY`** — not the hashed Library JSON  
`87745b3cb585e138b6768ab5b9e330f3f045ff4d4ad82ba6f71f0b6fe86be898`,  
canonical r2 identity still **unverified** in-repo until that lock is mirrored.

---

## What we are trying to secure

For this **fixed finite network**, capacity deficit decreases proportionally to \(t\) as T2’s weights shrink — certifying the **starvation-ray** calculation.

Extending that to **evolving Navier–Stokes** remains a **separate** task.

---

## Next moves (ordered)

### Move 1 — Reconcile the four \(\pi\)-offset targets with the generator convention  ← **DONE (this branch)**

Identified rows **0, 5, 10, 11** with labels
`T3:(+1,-1,+1)`, `T3:(-1,+1,+1)`, `T0:(+1,-1,+1)`, `T0:(+1,-1,-1)`.

G3 turn \(=-1/2\); lock-style zero \(=0\); difference \(=\pi\).

**Map:** \(b\leftarrow b+\pi\) on those four only ≡ flip \(\mathrm{sign}(g_{\mathrm{sym}})\) before
\(b=\pi/2-\arg(g_{\mathrm{sym}})\).

Write-up: [`B41-PHASE-PI-RECONCILIATION-2026-10-07.md`](B41-PHASE-PI-RECONCILIATION-2026-10-07.md).  
Script: `scripts/b41_phase_pi_reconcile.py`.

**G6-A:** still **not** transferred by raw identity — only via an **explicit** bridge citation.

### Move 2 — Write the audit result sheet

Precise table: what passed, what differs, which conclusions each check supports.  
Do **not** stamp DA / G6-A without Move 1 closed.

### Move 3 — Only then: asymptotic / starvation-ray coefficient work (B42 lane)

Keep B42’s first-order \(D_A/C_K\) claim scoped to the rationalized quotient with verified identities — separate from G6-A transfer.

---

## Honesty locks

- No NSE trajectory claim from this finite network  
- No classical regularity  
- \(\pi\) mismatch blocks **asserted r2 identity**, not the internal JSON certificates  
- Do not call triple-product / budget constants “3 and 2” without naming the normalization  

---

## Sibling agent

A parallel cloud agent was launched to reconcile the \(\pi\) offsets:  
https://cursor.com/agents/bc-0d120803-dc37-5b41-b8e4-2a07e151afbb  

Coordinate so both sides do not invent conflicting convention maps.
