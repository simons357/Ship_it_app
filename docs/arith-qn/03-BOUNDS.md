# Bounds: what is proved, what is open, what does not transfer

## Candidate

The object to test is

\[
\Bigl|\sum_{\lambda\in\sigma(Q_N)}\lambda\,\operatorname{Tr}(D_NP_\lambda)\Bigr|
\le C_\varepsilon N^{1/2+\varepsilon}.
\]

**Status: OPEN.** As written, this is the Mertens target expressed in spectral coordinates. It becomes a useful transfer argument only if it is derived from independently established properties of \(Q_N\), without assuming an equivalent cancellation bound.

The software constant `arith_qn.identity.BRIDGE_COMPLETE` is `False`. A tractable spectrum does not flip that flag.

## Why eigenvalue information is not enough

In an orthonormal eigenbasis,

\[
M(N)=\sum_j\lambda_j w_j,
\qquad
1\le w_j\le N,
\qquad
\sum_j w_j=\frac{N(N+1)}{2}.
\]

The \(w_j\) record how each eigenvector is distributed across the arithmetic indices. Two operators with the same eigenvalues can produce different weighted sums once those index weights change. For repeated eigenvalues the invariant quantity is \(\operatorname{Tr}(D_NP_\lambda)\), which is still an index-weighted mass on the eigenspace, not a function of \(\lambda\) alone.

A lower spectral floor or a gap therefore does not close the estimate. The retired claim \(\lambda_{\min}(Q_N)>-1/2\) was about a different matrix in any case (\(\widetilde Q_N=1/\gcd\)), and it is already false.

## Crude spectral-norm bound

Because the weights are nonnegative,

\[
|M(N)|
\le\|Q_N\|_{\mathrm{op}}\sum_j w_j
=\|Q_N\|_{\mathrm{op}}\frac{N(N+1)}{2}.
\]

The first column of \(Q_N\) is the all-ones vector: \(Q_N(i,1)=\mu(\gcd(i,1))/\gcd(i,1)=1\). Hence

\[
\|Q_N\|_{\mathrm{op}}\ge\|Q_Ne_1\|_2=\sqrt{N}.
\]

A sharper visible property: \(Q_N(i,j)=1\) on every coprime pair, and the density of those pairs is \(6/\pi^2\). The survey measures \(\|Q_N\|_{\mathrm{op}}/N\approx 6/\pi^2\), so

\[
\|Q_N\|_{\mathrm{op}}=\Theta(N)
\]

and the crude bound is \(\Theta(N^3)\). That is weaker than the trivial estimate \(|M(N)|\le N\) coming from \(|\mu|\le 1\). It supplies **no** useful square-root cancellation. The leading eigenmode is a delocalized coprime-ones vector; its index weight stays \(\Theta(N)\), so the large eigenvalue is not hidden by \(w_j\).

The congruence packaging \(A_N=D_N^{1/2}Q_ND_N^{1/2}\) does not repair this: \(|M(N)|\le N\|A_N\|_{\mathrm{op}}\) still needs an independent bound on \(\|A_N\|_{\mathrm{op}}\) that already encodes the same cancellation.

## What a useful transfer would require

Any of the following, established **without** assuming a Mertens-strength bound, would be a genuine input:

- a decay law for the signed measure \(\lambda\mapsto\operatorname{Tr}(D_NP_\lambda)\) that is not equivalent to \(M(N)=O(N^{1/2+\varepsilon})\);
- an independent estimate of the correlation between \(\lambda_j\) and the index weights \(w_j\);
- a closed-form orthonormal eigenbasis of \(Q_N\) whose coordinate sizes can be bounded by elementary number theory;
- moment or restriction bounds on \(Q_N\) that force cancellation in \(\sum\lambda_j w_j\).

Numerical checks that \(|M(N)|\) is smaller than \(\sqrt{N}\) on \(N\le 512\) are consistent with the target at tiny height. They are not a transfer. The classical Mertens conjecture \(|M(N)|<\sqrt{N}\) is false for some enormous \(N\) (Odlyzko–te Riele); the \(N^{1/2+\varepsilon}\) form remains the RH-equivalent statement and is not claimed here.

## Recorded negative

`NULL-ARITH-OPNORM` in `data/domain_architect/null_results.json`: the operator-norm estimate does not yield square-root cancellation. That is a negative about this method, not a disproof of the Mertens target.

## Routing

Keep this book separate from:

- FRA role letters \(P,H,\psi,\lambda,\Phi\);
- retired SFE-HAM / inverse-GCD floor claims;
- Hilbert–Pólya (missing independent Hamiltonian);
- Navier–Stokes / swirl notes.

Domain Architect may *route* to this folder. It may not treat \(Q_N\) as a permission projector or \(D_N\) as a coupling.
