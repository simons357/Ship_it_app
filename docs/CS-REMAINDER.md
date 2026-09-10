# CS remainder is false. Target A is false.

10 September 2026. **NS not solved.** Lemma★ does not close unaugmented NSE.

N-shell maximizer (\(N=2,3,4,5\)) saturates: `docs/RSTAR-SHELL-CLIMB.md`.
That family cannot concentrate in space. It is not a bound.

## Counterexample field

On \(\mathbb{T}^3\), for \(\lambda\in\mathbb{N}\),
\[
\mathrm{ABC}_\lambda(x)
=
\bigl(\sin(\lambda z)+\cos(\lambda y),\;
\sin(\lambda x)+\cos(\lambda z),\;
\sin(\lambda y)+\cos(\lambda x)\bigr),
\]
\[
\widehat{\gamma}_\lambda(k)=\exp\bigl(-|k|^2/(2\lambda^2)\bigr),
\qquad
v_\lambda
=
-
\frac{P(\gamma_\lambda\,\mathrm{ABC}_\lambda)}
{\|P(\gamma_\lambda\,\mathrm{ABC}_\lambda)\|_2}.
\]
(The raw windowed field has \(T_c<0\); the minus sign is the reverse.)

Script: `scripts/ns_attacks/cs_remainder_bump.py`
JSON: `results/cs_remainder_bump/cs_remainder.json`

## Table

| \(\lambda\) | \(\|A^{1/2}B\|_2/\sqrt{EY}\) | \(\mathcal R_\star(-v)\) |
|---|---|---|
| 2 | 2.492 | 0.00517 |
| 3 | 4.607 | 0.0173 |
| 4 | 7.104 | 0.0409 |
| 5 | 9.934 | 0.0798 |
| 6 | 13.062 | 0.138 |
| 8 | 20.114 | 0.327 |

\(\|A^{1/2}B\|_2/\sqrt{EY}\sim 0.88\,\lambda^{3/2}\).
\(\mathcal R_\star\sim 6.47\times 10^{-4}\,\lambda^3\).

A curl-Gaussian has the same CS climb and \(T_c=0\) (orthogonal).
Localized ABC is CS-aligned: \(T_c\sim\lambda^{13/2}\), so
\(\mathcal R_\star=T_c^2/(\mathcal D_s EY)\) climbs.

This is spatial concentration on a fixed torus
(\(u(x)=\lambda^{3/2}\varphi(\lambda x)\)), **not** the
Fourier dilation \(v(n\cdot)\). The latter leaves \(\mathcal R_\star\)
invariant. This family does not.

## What dies

\[
\|A^{1/2}B(v,v)\|_2
\le
C\sqrt{EY}
\]
is false. No \(C\) works.

\[
\sup_v\mathcal R_\star(v)<\infty
\]
is false. Target A is false. Lemma★ does not close unaugmented NSE.

Uniform Fourier dilation of a fixed shape is a different family.
N-shell samples remain bounded. They are not this field.

Stay in this chat.
