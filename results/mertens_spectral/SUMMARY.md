# Spectral Mertens survey

**Book:** arithmetic (Möbius–GCD matrix). Not FRA, not SFE, not Clay.
**Identity:** proved. **Cancellation estimate:** OPEN.
**Bridge complete:** `False`.
**Useful transfer:** `False`.

The candidate bound `|Σ λ Tr(D_N P_λ)| ≤ C_ε N^{1/2+ε}` is the Mertens
target in spectral coordinates. This survey tests the exact identity
and shows that the crude operator-norm estimate does not produce
square-root cancellation.

## Why the crude bound fails

For an orthonormal eigenbasis, `1 ≤ w_j ≤ N` and `Σ w_j = N(N+1)/2`.
Therefore `|M(N)| ≤ ||Q_N||_op N(N+1)/2`. The first column of `Q_N`
is the all-ones vector, so `||Q_N||_op ≥ √N`. The coprime pairs, where
`Q_N=1`, have density `6/π² ≈ 0.60793`, and the
measured `||Q_N||_op` is `Θ(N)`. The crude bound is then `Θ(N³)` —
weaker than the trivial `|M(N)| ≤ N`, with no `N^{1/2+ε}` information.

## Survey table

| N | M(N) | ‖Q‖_op | ‖Q‖/N | crude/|M| | |M|/√N | cancel. ratio | min w | max w | lead w | |λ|–w corr |
|---|------|--------|-------|-----------|-------|---------------|-------|-------|--------|-----------|
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | — |
| 2 | 0 | 1.5 | 0.75 | 4.5 | 0 | ∞ | 1.2 | 1.8 | 1.2 | -1 |
| 6 | -1 | 3.725 | 0.621 | 78.2 | 0.408 | 33.6 | 2.8 | 4.98 | 2.8 | -0.175 |
| 10 | -1 | 6.139 | 0.614 | 338 | 0.316 | 97.6 | 3.47 | 7.31 | 4.8 | -0.0379 |
| 12 | -2 | 7.528 | 0.627 | 294 | 0.577 | 72.2 | 4.31 | 9.02 | 5.9 | -0.0149 |
| 16 | -1 | 9.838 | 0.615 | 1.34e+03 | 0.25 | 271 | 4.99 | 12 | 7.81 | 0.00932 |
| 20 | -3 | 12.84 | 0.642 | 899 | 0.671 | 145 | 6.58 | 18.1 | 10.2 | 0.0132 |
| 24 | -2 | 15.06 | 0.628 | 2.26e+03 | 0.408 | 325 | 6.28 | 21.6 | 12 | 0.0236 |
| 32 | -4 | 20.48 | 0.64 | 2.7e+03 | 0.707 | 299 | 7.33 | 30.1 | 16.3 | 0.0223 |
| 48 | -3 | 30.08 | 0.627 | 1.18e+04 | 0.433 | 970 | 9.54 | 45.8 | 24.1 | 0.0265 |
| 64 | -1 | 39.87 | 0.623 | 8.29e+04 | 0.125 | 5.39e+03 | 15.1 | 60.2 | 32 | 0.0301 |
| 80 | -4 | 50.03 | 0.625 | 4.05e+04 | 0.447 | 2.21e+03 | 16.2 | 77.6 | 40.2 | 0.0318 |
| 96 | 2 | 59.29 | 0.618 | 1.38e+05 | 0.204 | 6.59e+03 | 13 | 87.4 | 47.7 | 0.0334 |
| 128 | -2 | 79.89 | 0.624 | 3.3e+05 | 0.177 | 1.2e+04 | 15.5 | 125 | 64.3 | 0.0239 |
| 160 | 0 | 99.34 | 0.621 | 1.28e+06 | 0 | ∞ | 28.1 | 156 | 79.9 | 0.0234 |
| 192 | -5 | 119.3 | 0.622 | 4.42e+05 | 0.361 | 1.16e+04 | 22.1 | 189 | 96 | 0.0232 |
| 256 | -1 | 158.9 | 0.621 | 5.23e+06 | 0.0625 | 1.07e+05 | 29 | 249 | 128 | 0.0195 |
| 320 | -4 | 199.3 | 0.623 | 2.56e+06 | 0.224 | 4.29e+04 | 33.8 | 316 | 160 | 0.0171 |
| 384 | -2 | 239 | 0.622 | 8.83e+06 | 0.102 | 1.26e+05 | 33.9 | 382 | 192 | 0.0152 |
| 512 | -4 | 318.6 | 0.622 | 1.05e+07 | 0.177 | 1.17e+05 | 52 | 508 | 256 | 0.014 |

## Residuals

Trace, spectral, and congruence (`A_N = D_N^{1/2} Q_N D_N^{1/2}`) residuals stay at floating-point scale. The identities hold.

- max `|Tr(D Q) − M(N)|` = `0.000e+00`
- max `|Σ λ_j w_j − M(N)|` = `3.638e-11`
- max `|Σ α_k − M(N)|` = `1.164e-10`

## Transfer rule

- M(N) = Tr(D_N Q_N) is proved from the diagonal.
- M(N) = Σ λ_j w_j is the same identity in an orthonormal eigenbasis.
- 1 ≤ w_j ≤ N and Σ w_j = N(N+1)/2, so weights carry the index distribution.
- The crude bound |M(N)| ≤ ||Q_N||_op N(N+1)/2 supplies no square-root cancellation.
- A lower spectral floor or a gap does not replace the missing weight estimate.
- The candidate |Σ λ Tr(D_N P_λ)| ≤ C_ε N^{1/2+ε} is the Mertens target in spectral coordinates and remains OPEN.
- No independently established Q_N property was supplied, so the rewrite is not a transfer argument.

## Q_6 lock

See `q6.json`. `M(6) = −1 = Tr(D_6 Q_6)`. The 6×6 matrix is the
stated Möbius–GCD kernel, not the inverse-GCD matrix `1/gcd`.

## Coprime-density note

`Q_N(i,j)=1` whenever `gcd(i,j)=1`. The density of coprime pairs is `6/π² ≈ 0.60793`. The measured `‖Q_N‖_op / N` tracks that constant, so the leading eigenvalue is a delocalized coprime-ones mode of size `Θ(N)`. The crude bound is then `Θ(N³)`, which is still not a square-root estimate. The leading weight stays `Θ(N)` rather than `O(1)`, so the large eigenvalue is not suppressed by the index weights.

