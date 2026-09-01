# RH Track B — Möbius–GCD (Domain Architect attack)

**Date:** 26 August 2026  
**Book:** RH Track B (Möbius–GCD)  
**Not:** classical NS Track B (inventory `NS-B`), inverse-GCD Q6, Route C, SND, GNC, Goldbach, or the Harmonic Blueprint  
**RH status:** **not claimed**

Locked operator:

\[
Q_N(i,j)=\frac{\mu(\gcd(i,j))}{\gcd(i,j)},\qquad 1\le i,j\le N.
\]

Realization (target, not an input):

\[
M(N)=\sum_{n\le N}\mu(n)=O_\varepsilon\!\left(N^{1/2+\varepsilon}\right)
\quad\text{for every }\varepsilon>0.
\]

That bound is the classical Littlewood–Mertens criterion. It is equivalent to RH. Domain Architect does not assume it.

## Output class

**Obstruction** for the listed dual / Hölder / spectral-floor / tautological-split routes, plus one **isolated conditional** that is *not* a reduction.

No uniform proof. No public RH claim.

Run:

```bash
python -m domain_architect --track-b-mobius
python -m domain_architect --track-b-mobius 32 --json -o /tmp/track-b.json
python -m domain_architect "Q_N(i,j) = μ(gcd(i,j))/gcd(i,j)"
python -m unittest tests.test_track_b_mobius
```

## Exact inputs (finite algebra)

Let \(f(n)=\mu(n)/n\), \(h=f*\mu\), \(u_d(n)=\mathbf 1_{d\mid n}\). Then \(h\) is multiplicative with

\[
h(1)=1,\quad
h(p)=-\Bigl(1+\frac1p\Bigr),\quad
h(p^2)=\frac1p,\quad
h(p^k)=0\ (k\ge 3).
\]

Cubefree rank-one form, and the quadratic identity, hold as rational-matrix equalities (checked exactly through \(N=36\)):

\[
Q_N=\sum_{d\le N}h(d)\,u_d u_d^{\mathsf T},
\qquad
x^{\mathsf T}Q_N x
=\sum_{d\le N}h(d)
\Bigl(\sum_{\substack{n\le N\\ d\mid n}}x_n\Bigr)^2.
\]

First row of \(Q_N\) is identically \(1\), so

\[
M(N)=e_1^{\mathsf T}Q_N\boldsymbol\mu_N.
\]

With \(S_d(N)=\sum_{d\mid n\le N}\mu(n)\),

\[
\boldsymbol\mu_N^{\mathsf T}Q_N\boldsymbol\mu_N
=M(N)^2+\sum_{d=2}^{N}h(d)S_d(N)^2.
\]

\(S_d=0\) unless \(d\) is squarefree. These identities are not RH-dependent.

\(Q_N\) is real symmetric and **indefinite** for every \(N\ge 2\) (checked through \(N=20\); both edges scale like \(N\) at accessible \(N\)).

## Missing bridge

Need a noncircular theorem

\[
\text{Track B operator control}
\Longrightarrow
|M(N)|\le C_\varepsilon N^{1/2+\varepsilon}.
\]

Generic first-row control is only \(O(N)\). That misses the RH scale by a square root. The inequality-direction problem on the quadratic split is the obstruction, not a missing constant.

## Routes

| Route | Verdict |
|---|---|
| First-row Hölder / dual \(\ell^p\) | **Obstruction.** \(Q_N e_1=\mathbf 1\). Hölder on \((\boldsymbol\mu_N,\mathbf 1)\) is \(\Theta(N)\) for every \(p\in[1,\infty]\). The rest of the spectrum is invisible to this identity. |
| Q-inner-product / Schur dual | **Obstruction.** \(Q_N\) is indefinite, so the Q-form is not a norm. Cauchy–Schwarz there does not upper-bound \(\lvert M(N)\rvert\). |
| Naive \(\lambda_{\min}/\lambda_{\max}\) | **Obstruction.** Edges of order \(N\) and \(\lVert\boldsymbol\mu_N\rVert_2^2=\Theta(N)\) give \(O(N^2)\) for the quadratic form. A lower bound on \(\boldsymbol\mu^{\mathsf T}Q\boldsymbol\mu\) is not an upper bound on \(M(N)^2\). Floors \(-1/2\) and \(-1/(2\pi)\) are quarantined (wrong operator). |
| Signed cubefree remainder as an independent estimate | **Obstruction.** \(S_d\) is a Mertens-type coprime subsum of length \(N/d\). Bounding it at RH scale assumes the target. |
| New weighted norm | **Open / conditional search.** No \(\lVert\cdot\rVert_*\) was found whose dual estimate is independent of Möbius cancellation yet multiplies to \(O_\varepsilon(N^{1/2+\varepsilon})\). Random \(\pm 1\) squarefree vectors already have \(\lvert\mathbf 1^{\mathsf T}x\rvert\) on the \(\sqrt N\) scale. |

Isolated statement, **not a reduction:**

> If \(\lvert\boldsymbol\mu_N^{\mathsf T}Q_N\boldsymbol\mu_N\rvert\le C_\varepsilon N^{1+2\varepsilon}\) and \(\lvert\sum_{d\ge 2}h(d)S_d(N)^2\rvert\le C_\varepsilon N^{1+2\varepsilon}\), then \(\lvert M(N)\rvert\le\sqrt{2C_\varepsilon}\,N^{1/2+\varepsilon}\).

Under the exact quadratic identity this is equivalent to Littlewood–Mertens. DA does not treat it as independent operator control.

## Quarantine

Rejected as inputs: Route C \(-1/(2\pi)\); \(\lambda_{\min}>-1/2\); swapping to \(1/\gcd\), \(1/(\gcd\sqrt{ij})\), or \(\gcd/\sqrt{ij}\); converting a lower Rayleigh bound into an upper Mertens bound without a sign theorem; finite-\(N\) numerics as an all-\(N\) theorem; RH or Mertens as a lemma; SND / GNC / Goldbach / NS / Harmonic Blueprint glue.

## Acceptance

This attack supplies one operator, exact identities, and obstruction theorems that do **not** depend on RH. It does **not** supply a uniform Mertens bound, a complete implication to Littlewood–Mertens, or a public RH claim.

Smallest remaining object: a genuinely stronger, independently provable estimate on this locked \(Q_N\) that upgrades \(O(N)\) control of \(M(N)\) to \(O_\varepsilon(N^{1/2+\varepsilon})\).
