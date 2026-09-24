# Centered spectral barycenter

**24 September 2026.** Next calculation after the \(K\)-candidate
score sheet. The unused identity sat on
`origin/cursor/unaug-ns-unified-status-a7a2:scripts/centered_barycenter.py`
as mass-only algebra. This page pairs it with signed \(T_k\) on the
live families.

Internal checkpoint. **Not a closure theorem.** Ordinary NS is not
solved. Soft X silent. Do not put \(K(t)\) in the PDE.
Do not redo K=0, the §4 triad, the \(\varepsilon\)-scan, or the
slot score sheet as if they were this page.

Machine: `scripts/centered_spectral_barycenter.py`.
JSON: `results/centered_spectral_barycenter.json`.
The centered equation stays [`CENTERED-EQUATION.md`](CENTERED-EQUATION.md).

Sheet parameters: \(\theta=1/2\), \(\nu=1\), band
\(\lvert\lambda-\Lambda\rvert/\Lambda\le 1/2\). Scoring only.

---

## I. Exact identities

Enstrophy measure on the occupied eigenvalues:

\[
p_k=\frac{\lambda_k\lvert u_k\rvert^2}{X},
\qquad
\sum_k p_k=1,
\qquad
\Lambda=\sum_k p_k\,\lambda_k.
\]

Then \(D_s\) is \(X\) times the variance of \(\lambda\):

\[
D_s
=X\sum_k p_k(\lambda_k-\Lambda)^2
=X\,\mathrm{Var}_p(\lambda).
\]

The other-branch script already had this. It did not touch \(T_c\).

Signed stretching per mode energy, on occupied modes:

\[
t_k=\frac{T_k}{\lvert u_k\rvert^2}.
\]

The same weights give

\[
\mathbb E_p[t]=\frac{N}{X},
\qquad
T_c
=X\sum_k p_k(\lambda_k-\Lambda)\,t_k
=X\,\mathrm{Cov}_p(\lambda,t).
\]

Hence

\[
\frac{T_c}{D_s}
=\beta_{t\sim\lambda}
=\frac{\mathrm{Cov}_p(\lambda,t)}{\mathrm{Var}_p(\lambda)}
\]

is the OLS slope of \(t\) on \(\lambda\). Cauchy–Schwarz on \(p\) is
the identity

\[
\lvert T_c\rvert
\le
\sqrt{X\,D_s}\,\sigma_t
=\rho_{\lambda,t}\,\sigma_t\,\sqrt{X\,D_s},
\]

where \(\sigma_t=\sqrt{\mathrm{Var}_p(t)}\) and
\(\rho_{\lambda,t}\) is the correlation. Two-shell support forces
\(\lvert\rho\rvert=1\).

Absorption \(T_c\le\theta\nu D_s\) is exactly \(\beta\le\theta\nu\).
That is a rewrite, not a bound on \(\beta\). Amplitude \(u=av\)
leaves \(\mathrm{Var}_p(\lambda)\) fixed and sends \(\beta\mapsto a\beta\).
The slope is **not** a shape invariant. That is the K=0 kill in
barycenter units. Do not rebuild it.

Relative width:

\[
\frac{\sigma_\lambda}{\Lambda}
=\frac{\sqrt{D_s/X}}{\Lambda}
=\frac{\sqrt{X D_s}}{Y}.
\]

---

## II. Numbers

**§4 note triad.** Slope \(4/3\). Correlation \(0.963\). Relative
width \(0.350\). All of \(D_s\) and \(T_c\) sit in the barycenter
band. Not absorbed at \(\theta=1/2\). Amplitude \(\times 2\): slope
\(\to 8/3\), variance unchanged.

**Separated \(L=8\).** Slope \(0.179\). Correlation \(0.103\).
Wings hold \(98\%\) of \(D_s\) and almost none of the net \(T_c\).
Absorbed. Weaker face.

**Growing layer \(v_n\)** (aspect 6; comparable; \(N=0\) so
\(\mathbb E_p[t]=0\)).

| \(n\) | slope | \(\sigma_\lambda/\Lambda\) | \(\rho\) | \(\sigma_t\) | band \(D_s\) | absorbed |
|---:|---:|---:|---:|---:|---:|---|
| 1 | \(0.215\) | \(0.268\) | \(0.250\) | \(1.17\) | \(0.53\) | yes |
| 2 | \(0.189\) | \(0.270\) | \(0.268\) | \(3.76\) | \(0.40\) | yes |
| 4 | \(0.178\) | \(0.270\) | \(0.280\) | \(13.3\) | \(0.42\) | yes |
| 8 | \(0.172\) | \(0.270\) | \(0.286\) | \(49.9\) | \(0.37\) | yes |

Relative width is frozen at \(\approx 0.270\). Slope decreases.
Correlation stays \(\approx 1/4\). Fat around the barycenter, not
collapsed onto it. Unrestricted \(\star\) still dies on this family.
Absorption at \(\theta=1/2\) does not.

**Near-shell annular \((\alpha,\beta)=(5,4)\).** Almost two-shell.

| \(\varepsilon\) | slope | \(\mathrm{Var}_p(\lambda)\) | \(\sigma_\lambda/\Lambda\) | \(\rho\) | \(\sigma_t\) |
|---:|---:|---:|---:|---:|---:|
| \(0.20\) | \(1.26\) | \(0.0300\) | \(0.0349\) | \(0.912\) | \(0.240\) |
| \(0.10\) | \(2.45\) | \(0.00787\) | \(0.0178\) | \(0.975\) | \(0.223\) |
| \(0.05\) | \(4.86\) | \(0.00199\) | \(0.00893\) | \(0.993\) | \(0.218\) |
| \(0.025\) | \(9.70\) | \(0.000500\) | \(0.00447\) | \(0.998\) | \(0.217\) |

Variance and relative width collapse. Correlation goes to \(1\).
\(\sigma_t\) stays. Slope is \(\Theta(\varepsilon^{-1})\). Not
absorbed. This is barycenter collapse with coherent stretching:
the enstrophy measure concentrates at \(\Lambda\) while \(t\) stays
aligned with \(\lambda\).

Identities hold on every row.

---

## III. What this does to the remainder

The live face is not “many modes” and is not a uniform energy slot.
It is **small \(\mathrm{Var}_p(\lambda)\) with \(\lvert\rho_{\lambda,t}\rvert\)
near \(1\)**.

- \(v_n\) cannot do that: aspect 6 freezes \(\sigma_\lambda/\Lambda\).
  It kills every uniform \(C\) of \(\star\) scaling and *helps*
  absorption at this \(\theta\).
- The aligned closer does that. Slope blows because the variance
  in the denominator vanishes faster than the covariance.
- Tautological \(K=(\beta-\theta\nu)_+\,\mathrm{Var}_p(\lambda)\) is
  the same coefficient in barycenter units. Content is still
  \(\int K<\infty\) from admissible data.
- No bound on \(\sigma_t\) or on \(\rho\) is written. Need★ is still
  the two-shell signed dual and is still unwritten.

The first missing implication is unchanged:

\[
T_{\mathrm{comp}}+T_{\mathrm{HH}\to\mathrm{L}}
\;\Longrightarrow\;
K\in L^1_{\mathrm{loc}}
\text{ from admissible data, no }H^1/L^\infty/\mathrm{BKM}.
\]

Its geometric face is now named: control \(\beta_{t\sim\lambda}\) when
the enstrophy measure sits near its barycenter.

No new estimate is claimed. No continuation criterion.
**NS not solved.**
