# Gate D FFT solver corrections — 9 October 2026

**Valid target; lemma not stamped. Not (17).**

Binding text: review check against commit `18a267f3` (ZIP not on this mount).
HEAD with fixes: `3f82c8fa`. Prior unpadded / double-counted / H-filtered FFT
rows are **provisional — not Gate D evidence**.

---

## Checklist vs workspace

| Check | At `18a267f3` | At HEAD (`3f82c8fa`) |
|---|---|---|
| \(B_I=\int d\,dt\) only (no extra \((b-a)d(a)\)) | Fail — added boundary on top of ∫d | **Pass** — `B_IH = B_direct` |
| Nonlinear product dealiased at used cutoff | Fail — \(N=512\), \(k_{\max}=252\) | **Pass** — default \(N=\texttt{next_dealias_n}(k_{\max})\ge 3k_{\max}\) (768) |
| Fixed \(K\), full \(X,Y\); score \(B_I/\mathcal R_I\) | Fail — \(H\)-filter \(X_H,Y_H\) | **Pass** — `K2_fixed=1`, `D=T_{\mathrm{sc}}-\nu Y/4`, `d=D/X` |

“\(D\) rising” on the old partial run stays **provisional**.

---

## 1. Episode cost — no double count

\[
B_I=\int_a^b d(t)\,dt
\]
is already the episode cost when \(d=D/X\) is integrated directly.

\[
\int_a^b d(t)\,dt=(b-a)d(a)+\int_a^b(b-s)d'(s)\,ds
\]
reconstructs that **same** integral. Adding \((b-a)d(a)\) after the direct
integral counts the initial boundary twice. Use one side only.

Code: `B_IH = B_direct`; field
`boundary_term_for_dprime_reconstruction_only` is documentation only.

---

## 2. Dealias at the cutoff actually used

Quadratic product of modes through cutoff \(252\) reaches wavenumber \(504\).
On unpadded \(512^3\):

| Quantity | Value |
|---|---|
| Nyquist | \(256\) |
| \(2/3\) keep | \(\lfloor 512/3\rfloor=170\) |
| Cutoff \(252\) vs keep \(170\) | **fails** |

So interactions fold back into the retained band. Initial smoke agreement
does not control accumulated alias.

Orszag fix used here: \(N/3\ge k_{\max}\) ⇒ \(N\ge 756\) ⇒ **\(N=768`**
(\(N/3=256\ge 252\)). Padding (or a cutoff that actually satisfies the rule)
must be in the trajectory RHS before extending any run.

---

## 3. Target: fixed \(K\), full \(X,Y\)

Recovered Gate D / episode-balance diagnostic:

\[
D=T_{\mathrm{sc}}-\nu Y/4,\qquad d=D/X,
\]

fixed \(K\) (default \(K^2=1\)), **full** \(X,Y\). Not an \(H\)-dependent
high-pass with \(X_H,Y_H\). Those can match at \(t=a\) and separate under
evolution, so a rise in filtered \(D\) does not read as a rise in the stated
diagnostic. Recorded score: \(B_I/\mathcal R_I\).

---

## Status

| Item | Status |
|---|---|
| Three corrections in FFT + sparse solvers | **In HEAD** |
| Review ZIP on this mount | **Absent** (`scratch/ec43035008f2/` empty) |
| Alias self-test / grid sizes | **Pass** — \(N_{\mathrm{dealiased}}=768\) for \(k_{\max}=252\) |
| FFT smoke @ \(4H\) / \(N=768\) on 16 GiB | **Host-blocked** (OOM or memmap I/O stall) |
| FFT smoke @ \(2H\) / \(N=384\) | Orszag OK; **packet truncated** — not adversary evidence |
| Sparse corrected full episode | **In progress** (raise mode budget) |
| Pre-correction FFT partial / smoke | **PROVISIONAL_INVALID** |

## STATUS

CORRECTIONS VERIFIED IN WORKSPACE VS `18a267f3` CHECK.
PRIOR FFT EVIDENCE DEMOTED.
GATE D: ACTIVE — RESOURCE-WEIGHTED TURNOVER (LEMMA NOT STAMPED).
NS NOT SOLVED.
