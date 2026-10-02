# Attack 9B / 9D — counting and Cauchy–Schwarz exclusion (fixed outputs)

**Date:** 10 September 2026  
**Status:** **Analytic exclusion** of one proposed kill mechanism. Lemma★ **OPEN**. Kill lane **LIVE** for a *different* family. **NS not solved.**  
**Does not prove** \(\sup K_{\alpha,\beta}<\infty\) or \(\sup\mathcal R_\star<\infty\).

This note locks a counting error in the screenshot that proposed \(\Theta(m^2)\) pairs landing on **one**, or a **fixed number** of, output modes.

---

## Counting (exact)

For a **fixed** output wavevector \(k\),
\[
p+q=k\qquad\Longrightarrow\qquad q=k-p.
\]
Each input \(p\) has only one possible partner. If the input support has \(m\) keys, there are **at most \(m\) ordered pairs** onto that output.

Total ordered pairs into a set of \(s\) outputs is therefore \(\le sm\). A \(\Theta(m^2)\) pair count requires \(s=\Theta(m)\). It **cannot** happen for \(s=O(1)\).

This is combinatorial. It does not depend on phases or polarizations.

---

## Phase-independent size bound

Incompressibility: \(p\cdot w_p=0\), so
\[
q\cdot w_p=(k-p)\cdot w_p=k\cdot w_p.
\]
The Fourier nonlinearity \(\widehat{B(w,w)}_k=i\,P_k\sum_{p+q=k}(q\cdot w_p)w_q\) therefore satisfies, by Cauchy–Schwarz and \(\|P_k\|\le 1\),
\[
\bigl|\widehat{B(w,w)}_k\bigr|
\le |k|\sum_p|w_p|\,|w_{k-p}|
\le |k|\,\|w\|_2^2.
\]
This bound **survives every choice of phases and polarizations**.

---

## Fixed-\(s\) bound on \(K_{\alpha,\beta}\)

If the projected interaction occupies \(s\) output keys on shell \(\beta\),
\[
\|\Pi_\beta B(w,w)\|_2^2
=\sum_{|k|^2=\beta}\bigl|\widehat B_k\bigr|^2
\le s\cdot\beta\,\|w\|_2^4,
\]
hence
\[
K_{\alpha,\beta}(w)
=\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}
\le s\frac{\beta^2}{\alpha^2}.
\]
Two inputs on shell \(\alpha\) can only produce
\[
\beta=|p+q|^2=2\alpha+2p\cdot q\le 4\alpha,
\]
so \(\beta^2/\alpha^2\le 16\) and
\[
K_{\alpha,\beta}(w)\le 16s.
\]

**Exclusion:** the screenshot’s **fixed-number-of-outputs** version of 9D **cannot** produce unbounded \(K\). This is analytic, independent of numerical samples.

Growing the **number of output modes** remains legitimate: their squared amplitudes add in \(\|\Pi_\beta B\|_2\). That does **not** make coherence “fake.”

---

## Correct uniform target (full 9B family)

Uniform boundedness of \(K_{\alpha,\beta}\) on exact-shell \(w\) is equivalent to
\[
\|\Pi_\beta B(w,w)\|_2
\le C\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2
\]
for a geometric \(C\) independent of \(\alpha,\beta,w\). Then \(K\le C^2\).

A bound \(\|\Pi_\beta B(w,w)\|_2\le C\alpha\|w\|_2^2\) (the screenshot form, missing \(1/\sqrt{\beta}\)) is **insufficient**: it only gives \(K\le C^2\beta\), which may grow with the output shell.

---

## What remains live

| Mechanism | Status |
|---|---|
| \(\Theta(m^2)\) pairs onto **one** output | **Impossible** (counting) |
| \(\Theta(m^2)\) pairs onto **fixed** \(s\) outputs | **Impossible** (counting); \(K\le 16s\) |
| Natural same-shell ensemble (9C) | **Not a kill** (SoT) |
| AP fan (9A) | **Not a kill** |
| Finite 9B sample \(\max K\approx 0.641\) | **Not a kill**; not a proof |
| Growing **input and output** supports, full complex polarizations, **frequency factors retained** | **LIVE test** of the \(\alpha/\sqrt{\beta}\) target — [`ATTACK_9D_THETA_M2_LOCKED_PHASE.md`](./ATTACK_9D_THETA_M2_LOCKED_PHASE.md) |

This narrows the search by proving which proposed mechanism **cannot** work. It does **not** close Lemma★.

**NS not solved.**
