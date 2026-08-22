# Spectral floor: what still stands after the retraction

The mixup was the **full-spectrum** claim \(\lambda_{\min}>-1/2\) for \(Q_N\), \(\widetilde Q_N\), or \(H_N\). That is false and stays withdrawn. A floor can still exist on a **restricted class of vectors**. This note records which restrictions survive a scan through \(N=80\), and one new short inequality.

No Goldbach, no RH, no Navier–Stokes map. Do not reattach this to SND or GNC.

Sources used: August inverse-GCD note (22045478), August errata (22045484), August Ring+SND (22045474). Zenodo’s public API is 403 from this environment; those are the PDFs already extracted. There is no other local “phone” corpus in this workspace.

---

## Status

| Statement | Status |
|---|---|
| \(\lambda_{\min}(Q_N)>-1/2\) for all \(N\) | **False.** \(Q_{10}\approx-1.90\), \(Q_{80}\approx-12.15\) |
| \(\lambda_{\min}(\widetilde Q_N)>-1/2\) for all \(N\) | **False.** \(\widetilde Q_{20}\approx-0.505\), \(\widetilde Q_{80}\approx-0.709\) |
| \(\lambda_{\min}(H_N)\ge-3/14\) for all \(N\) | **False.** \(H_4\approx-0.2249<-3/14\) |
| Bridge\(^*\): \(R(e_p-e_q)>-1/2\) on \(\widetilde Q\) | **Proved** (August note, Thm 3.1) |
| \(v\ge 0\Rightarrow v^\top\widetilde Q v\ge 0\) | **Proved** |
| Prime-supported \(\lambda_{\min}(\widetilde Q\big|_P)\ge-1/4\) | **Proved below** |
| Multi-rep Bridge\(^*\) \(\ge-c_0\) with \(c_0<1/2\) | Open. Numeric through \(N=80\): min \(\approx-0.183\) |
| \(\lambda_{\min}(H_N)\ge-1/4\) | Numeric through \(N=80\); not a theorem |
| \(\lambda_{\min}(\widetilde Q_N)/\log N\) has a finite limit | Possible; values sit near \(-0.16\). Not a floor at \(-1/2\) |

Reproduce: `python3 scripts/spectral_floor_explore.py --nmax 80 --out results/spectral_floor_explore.json`

---

## 1. Why the unrestricted floor cannot come back

The counterexamples are not rounding error.

\[
\lambda_{\min}(Q_{10})\approx-1.90,\qquad
\lambda_{\min}(\widetilde Q_{20})\approx-0.505.
\]

On \(\widetilde Q_N\) the bottom eigenvalue keeps dropping through \(N=80\) (\(-0.42\to-0.71\)). Mean-zero restriction does not save it: that Rayleigh tracks the full \(\lambda_{\min}\) and is already \(<-1/2\) at \(N=30\). The minimizer is not a two-spike: 90% of its \(\ell^2\) mass sits on about \(N/2\) coordinates, and clipping \(\|v\|_\infty\le 2N^{-1/2}\) still leaves \(R<-1/2\). So a generic “non-concentration of the test vector” hypothesis does **not** restore the old floor on the full matrix.

The bad direction is structured (composite support). Random mean-zero Gaussians stay above \(-1/2\) in the same scan. That is evidence that the failure is a specific mode, not the typical vector.

---

## 2. What “non-concentration papers” actually are

In this stack, non-concentration is a **fluids** object, not a matrix-floor repair.

- August Ring note (22045474): band-limited vorticity-direction bound, plus SND as a *conditional* \(H^1\) criterion.
- Working note `docs/UNAUGMENTED-R4-VORTICITY-PLAN.md`: 3-CONC / EQ3 / SPREAD on Littlewood–Paley packets.

Those control \(\omega\cdot S\omega\) under a shell hypothesis. They do not bound \(\lambda_{\min}(Q_N)\). Using SND to “deduce the spectral floor” is the same identification that was withdrawn.

---

## 3. Live floors (restricted)

### 3.1 Bridge\(^*\) (already proved)

On \(\widetilde Q\), for distinct primes \(p,q\) and \(v=e_p-e_q\),

\[
R(v)=\frac12\Big(\frac1{p^2}+\frac1{q^2}\Big)-\frac1{\sqrt{pq}}>-\frac12,
\]

because \(pq\ge 6\). The worst pair is \((2,3)\approx-0.2277\). This is a two-line identity. It is not \(\lambda_{\min}\).

### 3.2 Prime-supported block (new, short)

Let \(P\) be any finite set of primes and let \(A\) be the principal submatrix of \(\widetilde Q\) on those indices. For \(p\neq q\),

\[
A_{pq}=\frac1{\sqrt{pq}},\qquad A_{pp}=\frac1{p^2}.
\]

Write \(u_p=p^{-1/2}\). Then \(A=uu^\top+D\) with

\[
D=\mathrm{diag}\Big(\frac1{p^2}-\frac1{p}\Big).
\]

\(uu^\top\) is positive semidefinite, and \(\min_p(1/p^2-1/p)=1/4-1/2=-1/4\) at \(p=2\). Hence for every \(v\) supported on \(P\),

\[
v^\top A v=(u\cdot v)^2+v^\top Dv\ge-\frac14\|v\|_2^2.
\]

**Theorem P.** \(\lambda_{\min}(\widetilde Q\big|_P)\ge-1/4>-1/2\).

This is the natural extension of Bridge\(^*\): the pair bound is the two-sparse case; the prime block is the whole prime subspace. Numerically the bottom of the block sits near \(-0.235\) from \(N=3\) through \(N=80\), just below the \((2,3)\) pair, well above \(-1/4\).

This is still a restricted floor. Composites are excluded. The full-matrix counterexamples live on composite support (\(N=80\) composite block \(\approx-0.525<-1/2\)).

### 3.3 Positive orthant

Every entry of \(\widetilde Q\) is positive, so \(v\ge 0\) implies \(v^\top\widetilde Q v\ge 0\). Floor \(0\), on a cone, not on a subspace.

### 3.4 Multi-representation Bridge\(^*\) (open)

For even \(k\) and \(v_k=\sum_{p+q=k}(e_p-e_q)\), the scan through \(N=80\) stays at \(\approx-0.183>-1/2\). That matches the August remark (numeric through \(N=200\) is not a proof). Still the right open problem if the goal is Goldbach-shaped vectors. It is not needed for Theorem P.

---

## 4. Degree-normalized \(H_N\)

\(H_N=D^{-1/2}\widetilde Q_N D^{-1/2}\) with \(D=\mathrm{diag}(\widetilde Q\mathbf 1)\).

- The old packaged bound \(\lambda_{\min}(H_N)\ge-3/14\) fails at \(N=4,10,16\).
- Through \(N=80\), every computed \(\lambda_{\min}(H_N)\) is \(\ge-0.2249>-1/4\).
- After \(N\approx 20\) the values hover near \(-0.20\) to \(-0.21\).

So \(H_N\) is the only *full-index* matrix in the trio that still looks bounded. That is a numerical hypothesis, not a theorem. If a uniform \(H\) floor is what you want, the honest target is \(\lambda_{\min}(H_N)\ge-1/4\), not \(-3/14\) and not \(-1/2\).

---

## 5. Renormalized growth, not a floor

\(\lambda_{\min}(\widetilde Q_N)/\log N\) is about \(-0.18\) at \(N=10\) and \(-0.16\) at \(N=80\). That is compatible with a finite limit, which is the shape of the old Route C “spectral-limit” gap. It does **not** put \(\lambda_{\min}\) above \(-1/2\). \(Q_N\) itself dives (\(\approx-12\) at \(N=80\)); do not mix the three matrices.

---

## 6. What this does for the hypothesis

You can keep a spectral floor. You cannot keep the one that was retracted.

The live arithmetic claim is now:

1. Bridge\(^*\) on prime pairs (already public).
2. Theorem P: the whole prime-supported block sits above \(-1/4\).
3. Optional, separate: try to prove \(\lambda_{\min}(H_N)\ge-1/4\), or settle multi-rep.

None of these implies SND, GNC, or a bound on \((u\cdot\nabla)u\). The fluids non-concentration tools stay on Track B.

---

## First scan (\(N\le 80\))

| \(N\) | \(\lambda_{\min}(Q)\) | \(\lambda_{\min}(\widetilde Q)\) | \(\lambda_{\min}(H)\) | prime block | Bridge\(^*\) | multi-rep | \(\widetilde Q/\log N\) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | \(-1.90\) | \(-0.415\) | \(-0.215\) | \(-0.235\) | \(-0.228\) | \(-0.183\) | \(-0.180\) |
| 20 | \(-3.32\) | \(-0.505\) | \(-0.203\) | \(-0.235\) | \(-0.228\) | \(-0.183\) | \(-0.169\) |
| 40 | \(-6.24\) | \(-0.609\) | \(-0.209\) | \(-0.235\) | \(-0.228\) | \(-0.183\) | \(-0.165\) |
| 80 | \(-12.15\) | \(-0.709\) | \(-0.208\) | \(-0.235\) | \(-0.228\) | \(-0.183\) | \(-0.162\) |
