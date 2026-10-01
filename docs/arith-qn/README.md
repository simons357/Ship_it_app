# Arithmetic book: Möbius–GCD matrix and Mertens

**Status:** exact identity proved; cancellation estimate **OPEN**  
**Book:** arithmetic. Not FRA, not SFE, not Hilbert–Pólya, not Clay.  
**Do not merge** with the retired inverse-GCD matrix \(\widetilde Q_N(i,j)=1/\gcd(i,j)\) or with \(H_N=D^{-1/2}\widetilde Q_N D^{-1/2}\).

This folder records the matrix-to-Mertens identity for the stated kernel

\[
Q_N(i,j)=\frac{\mu(\gcd(i,j))}{\gcd(i,j)},
\qquad
D_N=\operatorname{diag}(1,2,\ldots,N).
\]

| Document | Role |
|---|---|
| [01 — Identity](01-IDENTITY.md) | Diagonal proof, spectral form, projector weights, \(Q_6\) |
| [02 — Experiment](02-EXPERIMENT.md) | Computational survey of identities, weights, and crude bounds |
| [03 — Bounds](03-BOUNDS.md) | Why eigenvalue data alone do not close \(N^{1/2+\varepsilon}\) |

Software:

```bash
python -m arith_qn --identity 6
python -m arith_qn --spectral 32
python -m arith_qn --survey --max-n 512 --out results/mertens_spectral
python -m unittest tests.test_mertens_spectral
```

Rule against a false bridge: a tractable spectrum of \(Q_N\) does not complete the argument. The candidate

\[
\Bigl|\sum_{\lambda\in\sigma(Q_N)}\lambda\,\operatorname{Tr}(D_NP_\lambda)\Bigr|
\le C_\varepsilon N^{1/2+\varepsilon}
\]

is the Mertens target in spectral coordinates until it is derived from independently established properties of \(Q_N\).
