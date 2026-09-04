# H_N lock — degree-normalized inverse-GCD

**Date:** 2026-08-02  
**Source of definition:** user paste (corrected Bridge operator).  
**Status:** definition locked; **−3/14 is not a proved universal floor** (fails at some small N).

---

## Definitions (use these; do not mix)

\[
\widetilde Q_N(i,j)=\frac{1}{\gcd(i,j)\sqrt{ij}}.
\]

\[
d_i=\sum_{k=1}^{N}\widetilde Q_N(i,k)
=\sum_{k=1}^{N}\frac{1}{\gcd(i,k)\sqrt{ik}},
\qquad
D_N=\mathrm{diag}(d_1,\ldots,d_N).
\]

\[
\boxed{H_N=D_N^{-1/2}\,\widetilde Q_N\,D_N^{-1/2}}
\]

Entrywise:

\[
\boxed{H_N(i,j)=\frac{\widetilde Q_N(i,j)}{\sqrt{d_i d_j}}
=\frac{1}{\gcd(i,j)\sqrt{ij\,d_i d_j}}}.
\]

**Wrong operator (do not mix):** \(Q_N(i,j)=\gcd(i,j)/\sqrt{ij}\).

**Separate object:** dynamic shell-helical NS operator \(H_N[u(t)]\) is **not** automatically this static matrix.

---

## What numerics show (`scripts` / ad hoc check 2026-08-02)

| Fact | Status |
| --- | --- |
| \(\lambda_{\max}(H_N)=1\) (Perron / degree-normalized) | Holds in checks |
| \(\lambda_{\min}(H_N)\) near \(-0.21\) for moderate \(N\) | Observed |
| \(\lambda_{\min}(H_N)\ge -3/14\) for **all** \(N\) | **False** — e.g. \(N=4\): \(\approx -0.225\); also \(N=10,16\) slightly below |
| \(\lambda_{\min}(H_N)\ge -1/2\) | Holds in checks through \(N=1500\) (much weaker than −3/14; still **not** a theorem here) |
| This \(H_N\) closes NS / Triple Lock / Clay | **No** — definition ≠ proof |

Gap to −3/14 for large \(N\) is small and positive in samples (\(N=1500\): gap \(\approx +0.002\)). That is a **numeric candidate**, not a proof.

---

## Relation to Bridge\* on \(\widetilde Q\)

- Bridge\* (restricted Rayleigh of Goldbach vectors on \(\widetilde Q\)) is a **different** claim from \(\lambda_{\min}(H_N)\ge c\).
- Degree normalization changes the quadratic form; do not copy thresholds across operators without re-proof.

---

## Trust rule for this file

Only the **boxed definition** is locked.  
Any sentence of the form “therefore NS / RH / Goldbach” is **not** locked and should be treated as ARCHIVE noise unless a separate proof is checked line-by-line with a verifier.

---

## Panel update (2026-08-15)

See `docs/math/TAO-MATH-PANEL-SND-H.md`.

- Fluids **Theorem H** (shell commutator / SND-C) ≠ this matrix \(H_N\).
- Re-check through \(N=400\): \(\lambda_{\min}(H_N)>-1/2\) still holds numerically; \(-3/14\) still fails at small \(N\).
- Closing \(\lambda_{\min}(H_N)\) does **not** solve Navier–Stokes.
