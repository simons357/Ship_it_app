# Spectral floor: what still stands after the retraction

The mixup was the **matrix and the constant**, not the idea of a floor.

- \(\lambda_{\min}(Q_N)>-1/2\) and \(\lambda_{\min}(\widetilde Q_N)>-1/2\) are false. Stay withdrawn.
- \(\lambda_{\min}(H_N)\ge-3/14\) is also false (\(H_4\approx-0.2249\)).
- \(H_N\) **does** have a full-spectrum floor: \(\lambda_{\min}(H_N)\ge-1\), by a two-line pairing. That is the only unrestricted eigenvalue bound in the trio that is actually a theorem.
- On prime-supported vectors, \(\widetilde Q\) itself sits above \(-1/4\). That is the useful restricted floor (Theorem P).

No Goldbach, no RH, no Navier–Stokes map. Do not reattach this to SND or GNC. SFE, Harmonic Blueprint, and Millennium-packaged notes are shelved (`docs/SHELF.md`).

Sources I could actually read: August inverse-GCD (22045478), August errata (22045484), August Ring+SND (22045474), June T2 PDF, May T³ TeX (archive only). Zenodo HTML/API is 403 from this machine. There is no phone corpus, no extra GitHub math repo, and no local store of older drafts beyond `/tmp/simons-papers`.

---

## Status

| Statement | Status |
|---|---|
| \(\lambda_{\min}(Q_N)>-1/2\) for all \(N\) | **False.** \(Q_{10}\approx-1.90\), \(Q_{200}\) dives further |
| \(\lambda_{\min}(\widetilde Q_N)>-1/2\) for all \(N\) | **False.** \(\widetilde Q_{20}\approx-0.505\), \(\widetilde Q_{200}\approx-0.845\) |
| \(\lambda_{\min}(H_N)\ge-3/14\) | **False.** \(H_4\approx-0.2249\) |
| \(\lambda_{\min}(H_N)\ge-1\) | **Proved below** (full index) |
| \(\lambda_{\min}(H_N)\ge-1/4\) | Numeric through \(N=200\) (worst \(H_4\approx-0.225\)); not a theorem |
| Bridge\(^*\): \(R(e_p-e_q)>-1/2\) on \(\widetilde Q\) | **Proved** (August note, Thm 3.1) |
| \(v\ge 0\Rightarrow v^\top\widetilde Q v\ge 0\) | **Proved** |
| Prime-supported \(\lambda_{\min}(\widetilde Q\big|_P)\ge-1/4\) | **Proved below** |
| Multi-rep Bridge\(^*\) \(\ge-c_0\) with \(c_0<1/2\) | Open. Through \(N=200\) the worst vector is just the pair \((3,5)\) on \(k=8\), \(R\approx-0.183\) |
| Squarefree principal of \(\widetilde Q\) | Still above \(-1/2\) at \(N=120\) (\(\approx-0.433\)); drifting down |
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

## 4. Degree-normalized \(H_N\): the actual full-spectrum floor

\(H_N=D^{-1/2}\widetilde Q_N D^{-1/2}\) with \(D=\mathrm{diag}(\widetilde Q\mathbf 1)\). The Rayleigh quotient of \(H\) is

\[
\frac{v^\top H v}{v^\top v}=\frac{w^\top\widetilde Q w}{w^\top D w},\qquad w=D^{-1/2}v.
\]

**Theorem H-floor.** \(\lambda_{\min}(H_N)\ge-1\) for every \(N\ge 1\).

**Proof.** Let \(d_i=\sum_j\widetilde Q_{ij}\). Then

\[
w^\top\widetilde Q w+w^\top Dw
=\sum_{i,j}\widetilde Q_{ij}w_iw_j+\sum_{i,j}\widetilde Q_{ij}w_i^2
=\frac12\sum_{i,j}\widetilde Q_{ij}(w_i+w_j)^2\ge 0,
\]

because every entry of \(\widetilde Q\) is positive. Hence \(w^\top\widetilde Q w\ge-w^\top Dw\).

This is the unrestricted floor that survives. It is the same bound any positive kernel gets after degree-normalization (\(H\) is similar to the reversible walk \(D^{-1}\widetilde Q\), so the spectrum lies in \((-1,1]\)). The mixup was writing this as \(\lambda_{\min}(Q)>-1/2\) or \(\lambda_{\min}(H)\ge-3/14\).

A sharper full-index statement, \(\lambda_{\min}(H_N)\ge-1/4\), holds through \(N=200\) (values sit near \(-0.21\) after \(N=20\); the worst small-\(N\) point is \(H_4\approx-0.2249\)). The pairing that proves \(-1\) does **not** prove \(-1/4\): writing the \(-1/4\) form as a combination of \((w_i\pm w_j)^2\) produces a negative coefficient. So \(-1/4\) on \(H\) stays a conjecture. Do not revive \(-3/14\).

---

## 4½. Why composites kill \(\widetilde Q\) (Möbius)

The identity \(1/\gcd(i,j)=\sum_{k\mid\gcd(i,j)}c_k\) with \(c_n=n^{-1}\sum_{d\mid n}d\,\mu(d)\) makes the sign pattern visible. For a prime, \(c_p=(1-p)/p<0\). Those negative modes, once you allow composite indices, are what drive \(\lambda_{\min}(\widetilde Q_N)\) through \(-1/2\). Restricting to primes removes every \(k\) that is not a single prime (and on that block the rank-one split of Theorem P takes over). Squarefree support is not enough: the squarefree principal minor is already \(-0.43\) at \(N=120\) and still falling.

---

## 5. Renormalized growth, not a floor

\(\lambda_{\min}(\widetilde Q_N)/\log N\) is about \(-0.18\) at \(N=10\) and \(-0.16\) at \(N=80\). That is compatible with a finite limit, which is the shape of the old Route C “spectral-limit” gap. It does **not** put \(\lambda_{\min}\) above \(-1/2\). \(Q_N\) itself dives (\(\approx-12\) at \(N=80\)); do not mix the three matrices.

---

## 6. What this does for the hypothesis

You can keep a spectral floor. You cannot keep the one that was retracted.

The live arithmetic claim is now:

1. **Full index, weak:** \(\lambda_{\min}(H_N)\ge-1\) (proved).
2. **Prime block, useful:** Theorem P, \(\lambda_{\min}(\widetilde Q\big|_P)\ge-1/4\) (proved). Bridge\(^*\) is the two-sparse case of the same matrix.
3. **Full index, sharp (open):** \(\lambda_{\min}(H_N)\ge-1/4\). Numeric through \(N=200\). This is the right remaining hypothesis if you want a floor on every coordinate, not only primes.
4. **Goldbach-shaped (open, easy numerically):** multi-rep vectors through \(N=200\) never undercut the single pair \((3,5)\).

The May T³ file still says “Geometric Bridge” and “\(Q_6\) with \(\gamma>3/2\) enforces SND.” That is the withdrawn glue. Non-concentration in this stack is the Ring Lemma / 3-CONC / SPREAD package. It is a fluids hypothesis about Littlewood–Paley mass. It does not imply (1)–(3), and (1)–(3) do not imply it.

Analogy, not an identification: the \(\widetilde Q\)-floor fails on composite support and holds on prime support. That is the same *shape* as “spread vs concentrated,” and it is why the triple lock felt natural. It is not a theorem relating \(\rho=J/X\) to \(\lambda_{\min}\).

---

## Access note

| Place | What I could use |
|---|---|
| August PDFs already extracted | Inverse-GCD, errata, Ring+SND |
| June T2 PDF, May T³ TeX | Archive; T³ still carries the old closure language |
| Zenodo API / record HTML | 403 from this environment |
| GitHub `simons357` | `Ship_it_app`, empty-ish `ship-it-code`, `kyrana-oracle` (not math) |
| Phone / other local notes | None in this workspace or the agent store |

---

## First scan

| \(N\) | \(\lambda_{\min}(\widetilde Q)\) | \(\lambda_{\min}(H)\) | prime block | multi-rep |
|---:|---:|---:|---:|---:|
| 10 | \(-0.415\) | \(-0.215\) | \(-0.235\) | \(-0.183\) |
| 20 | \(-0.505\) | \(-0.203\) | \(-0.235\) | \(-0.183\) |
| 40 | \(-0.609\) | \(-0.209\) | \(-0.235\) | \(-0.183\) |
| 80 | \(-0.709\) | \(-0.208\) | \(-0.235\) | \(-0.183\) |
| 200 | \(-0.845\) | \(-0.210\) | \(-0.235\) | \(-0.183\) (\(k=8\), pair \(3+5\)) |
