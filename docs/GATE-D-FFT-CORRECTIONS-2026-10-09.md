# Gate D FFT solver corrections — 9 October 2026

**Valid target; lemma not stamped. Not (17).**

Review check on commit `18a267f3`. Prior unpadded / double-counted /
H-filtered FFT rows are **provisional — not Gate D evidence**.

---

## Three binding fixes

### 1. Episode cost — no double count

\[
B_I=\int_a^b d(t)\,dt
=
(b-a)d(a)+\int_a^b(b-s)d'(s)\,ds.
\]

The solver must use **one** of these forms. Adding \((b-a)d(a)\) on top of
the direct integral double-counts. The boundary term belongs only in the
\(d'\) reconstruction.

Code: `B_IH = B_direct` with
`boundary_term_for_dprime_reconstruction_only` recorded separately.

### 2. Dealias the nonlinear product

At cutoff \(k_{\max}=252\) (\(4H\), \(n=1\)), an unpadded \(512^3\) grid
aliases. Orszag requirement: \(N/3\ge k_{\max}\) ⇒ \(N\ge 768\).

| Grid | \(N\) |
|---|---|
| Unpadded (invalid for Gate D) | 512 |
| Dealiased | **768** |

Prior “\(D\) rising” partial run used \(N=512\) — **invalid**.

### 3. Restored diagnostic (fixed \(K\), full \(X,Y\))

Recovered Gate D / episode-balance target:

\[
D=T_{\mathrm{sc}}-\nu Y/4,\qquad d=D/X,
\]

with **fixed** \(K\) (default \(K^2=1\)) and **full** \(X,Y\).
Not an \(H\)-dependent high-pass with \(X_H,Y_H\).

(Initially these agree on the six-box packet; they diverge under evolution.)

---

## Status

| Item | Status |
|---|---|
| Corrections in `gate_d_full_trajectory_fft.py` / sparse twin | **Filed** |
| Alias grid sizes (512 vs 768) | **Documented** |
| Full first episode on dealiased grid | **Unrun** (wall / memmap cost) |
| Prior FFT smoke / partial JSON | **PROVISIONAL_INVALID** |

Author ZIP transfer: still not on this agent disk under
`scratch/ec43035008f2/`; vault pack remains under `handoff/`.

## STATUS

CORRECTIONS FILED; PRIOR FFT EVIDENCE DEMOTED.
GATE D: VALID TARGET; LEMMA NOT STAMPED.
NS NOT SOLVED.
