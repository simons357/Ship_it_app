# Lemma★ — canonical shape form (exact lock)

**Date:** 10 September 2026. Filed 24 September 2026.
**Source branch:** `cursor/ns-five-lane-lemma-star-1390` (PR #48).
**Lock:** Truth only. **NS is NOT solved.** Lemma★ is **OPEN**.
This note locks formulas. It does **not** prove ★.

**Do not alter** the 24 Sep RMS/SBP gate, the static-frontier lock, or
the Fourier-triangle audit (separate PRs). Do not splice ★ into
DA-NS-2. Do not splice ★ into the missing scalene theorem (17).

Machine: [`scripts/ns_attacks/stokes_moments.py`](../scripts/ns_attacks/stokes_moments.py).
Lock: [`data/lemma_star_shape_form_2026-09-10.json`](../data/lemma_star_shape_form_2026-09-10.json).

---

## Reframe (lock)

Lemma★ is no longer a viscosity statement. It is a **shape** statement.

Change only the size of a fixed shape \(v\) via \(u=av\). Optimize over
size. The worst size cancels \(\nu\). What remains is pure geometry on
the shape.

Code aliases: \(E=\|v\|_2^2\), \(T_c=\mathcal T_c\), \(D_s=\mathcal D_s\),
`ratio_R_star_shape`\(=\mathcal R_\star\).

Legacy `ratio_star` \(=T_c/(E X\Lambda)\) is a **different** post-Young
object (scales as \(1/a\)). It is **not** \(\mathcal R_\star\).

Do not compare legacy reported values \(0.065\), \(0.073\),
\(1.93\times10^{-3}\) unless each used exactly this \(\mathcal R_\star\)
formula.

---

## Status

| Item | Bucket |
|---|---|
| Moments, \(\mathcal D_s\) equivalences, two-shell form | **EXACT** |
| Signed \(T_c\), \(\Lambda'\) identity | **EXACT** |
| Homogeneity and dilation invariance of \(\mathcal R_\star\) | **EXACT** |
| Boxed shape inequality / \(\sup\mathcal R_\star<\infty\) | **OPEN** — this is ★ |
| Viscosity packaging | **DERIVED**, not primary |
| Near-shell \(K_{\alpha,\beta}\) | **restricted family only** — not the full lemma |
| Kill lane | **LIVE** |
| “The kill lane is closed” | **FALSE** (retired) |
| DA-NS-2 | **OPEN** (distinct route) |

---

## Setup and moments

\[
\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3,
\qquad
v(x)=\sum_{k\in\mathbb Z^3\setminus\{0\}}v_k e^{ik\cdot x},
\quad
k\cdot v_k=0,\quad
v_{-k}=\overline{v_k}.
\]
\[
\lambda_k=|k|^2,\qquad A=-P\Delta,\qquad (Av)_k=\lambda_k v_k.
\]
\[
E=\|v\|_2^2=\sum|v_k|^2,\quad
X=\|A^{1/2}v\|_2^2=\sum\lambda_k|v_k|^2,
\]
\[
Y=\|Av\|_2^2=\sum\lambda_k^2|v_k|^2,\quad
Z=\|A^{3/2}v\|_2^2=\sum\lambda_k^3|v_k|^2,\quad
\Lambda=Y/X.
\]

---

## Centered spectral dissipation

Do not invent a second \(\mathcal D_s\). All of the following are the
same nonnegative object:

\[
\mathcal D_s
=Z-\Lambda Y
=Z-Y^2/X
=\|(A-\Lambda)A^{1/2}v\|_2^2
=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2
=\frac1{2X}\sum_{k,\ell}\lambda_k\lambda_\ell(\lambda_k-\lambda_\ell)^2|v_k|^2|v_\ell|^2
\ge0.
\]

Two-eigenvalue shells \(\alpha,\beta\) with energies
\(e_\alpha=\sum_{\lambda_k=\alpha}|v_k|^2\):

\[
\mathcal D_s
=\frac{\alpha\beta(\alpha-\beta)^2\,e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}.
\]

---

## Nonlinear transfer (signed)

\[
B(v,v)=P[(v\cdot\nabla)v],
\qquad
\widehat B_k
=iP_k\sum_{p+q=k}(q\cdot v_p)v_q,
\qquad
P_k=I-\frac{k\otimes k}{|k|^2}.
\]
\[
T_k(v)
=-\operatorname{Re}\bigl(\widehat B_k\cdot\overline{v_k}\bigr)
=\sum_{p+q=k}
\operatorname{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

Keep the signed complex triad sum. **Do not** replace \(\operatorname{Im}\)
by absolute values.

\[
N=-\langle B,Av\rangle=\sum\lambda_k T_k,
\qquad
M=-\langle AB,Av\rangle=\sum\lambda_k^2 T_k,
\]
\[
T_c
=M-\Lambda N
=\sum_k\lambda_k(\lambda_k-\Lambda)T_k
=\sum_{p+q=k}
\lambda_k(\lambda_k-\Lambda)\,
\operatorname{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

With \(k=p+q=-r\) so \(p+q+r=0\):

\[
T_c
=\sum_{p+q+r=0}
\lambda_{-r}(\lambda_{-r}-\Lambda)\,
\operatorname{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_{-r}})\bigr].
\]

Equivalent cyclic writings that keep the same signed \(\operatorname{Im}\)
are allowed. Absolute-value rearrangements are not.

HH→L channel splits can identify a mechanism. Only the **complete**
signed \(T_c\) enters the kill criterion for ★.

From the Galerkin identities \(X'=-2\nu Y+2N\), \(Y'=-2\nu Z+2M\):

\[
\Lambda'=\frac2X\bigl(T_c-\nu\mathcal D_s\bigr).
\]

---

## Canonical shape quotient

When \(\mathcal D_s(v)>0\), \(\|v\|_2>0\), \(Y(v)>0\), with
\((T_c)_+=\max(T_c,0)\):

\[
\mathcal R_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}{\mathcal D_s(v)\,\|v\|_2^2\,Y(v)}.
\]

When \(T_c\ge0\), \((T_c)_+^2=T_c^2\). Kill cares about stretching
\(T_c>0\). Compression \(T_c<0\) gives \(\mathcal R_\star=0\) under the
\((T_c)_+\) form and is not a stretching counterexample.

Boxed shape inequality (canonical ★): there exists one geometric
constant \(C_{\mathrm{geom}}\) (independent of amplitude and of \(\nu\))
such that for every divergence-free \(v\) on \(\mathbb T^3\),

\[
\boxed{
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,
\mathcal D_s(v)\,
\|v\|_2^2\,
Y(v).
}
\]

That is \(\sup_v\mathcal R_\star<\infty\), with that supremum equal to
\(C_{\mathrm{geom}}\) when the sup is finite. **Existence of a finite
\(C_{\mathrm{geom}}\) is OPEN.**

Homogeneity (\(a>0\)) — exact invariance, not “the ratio gets smaller”:

\[
T_c(av)=a^3 T_c(v),\quad
\mathcal D_s(av)=a^2\mathcal D_s(v),\quad
\|av\|_2^2=a^2\|v\|_2^2,
\]
\[
Y(av)=a^2 Y(v),\quad
\Lambda(av)=\Lambda(v),\quad
\mathcal R_\star(av)=\mathcal R_\star(v).
\]

Uniform Fourier dilation \(v(n\cdot)\) (mode \(k\mapsto nk\)) likewise
leaves \(\mathcal R_\star\) exactly invariant. Claims that amplitude or
frequency makes the ratio smaller concern an older non-optimized
budget, not \(\mathcal R_\star\).

Viscosity packaging (derived, not primary). Young / AM–GM on the
amplitude line recovers, for fixed \(0<\theta<1\),

\[
T_c\le\theta\nu\mathcal D_s+C_0(\theta)\nu^{-1}\|v\|_2^2\,Y,
\qquad
C_0(\theta)=C_{\mathrm{geom}}/(4\theta).
\]

---

## Near-shell \(K_{\alpha,\beta}\) is not the full lemma

\[
K_{\alpha,\beta}
=\sup_{Aw=\alpha w}
\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4},
\qquad
\lim_{\varepsilon\to0}\mathcal R_\star(w_\alpha+\varepsilon z_\beta)=K_{\alpha,\beta}(w).
\]

This is a restricted exact-shell + infinitesimal closing family.
Bounding or sampling \(K\) is **not** equivalent to proving or
falsifying ★ over all smooth divergence-free mean-zero fields.

---

## Kill / survive table

| Outcome | Verdict |
|---|---|
| Some shapes make \(\mathcal R_\star\) arbitrarily large | no finite \(C_{\mathrm{geom}}\) → **★ dead** |
| \(\mathcal D_s=0\) (one Fourier shell) and \(T_c>0\) | **★ dead** on that field |
| Pure single shell, both sides vanish (\(T_c=0=\mathcal D_s\)) | vacuous — not a kill |
| Live kill attempt | almost-single-shell / near two-shell / exact-shell + closing (9B \(K_{\alpha,\beta}\)); designed \(\Theta(m^2)\) locked-phase (9D, stub) |
| AP packet fan (9A) / fixed-gap natural ensemble (9C) | **Did not kill ★** — 9C: \(\mathcal R_\star\) falls \(0.11\to 0.031\), not \(m^{1/2}\) |
| Every shape has \(\mathcal R_\star\le K\) | that number is ★ (up to \(4\theta\)) — **not proved** |
| A list of fields with small \(\mathcal R_\star\) | **NOT** that number — those shapes did not kill it |
| Failure to find a numerical counterexample | does **NOT** close the kill lane — falsification **LIVE**, proof **LIVE** |

Retired false claim: “The kill lane is closed.” — **FALSE.**

Do not confuse with post-Young \(R_{\mathrm{post}}=T_c/(\|v\|_2^2 Y)\)
(scales as \(1/a\)) or pre-Young \(R_{\mathrm{pre}}=T_c/(\|v\|_2 X\Lambda)\).
Those older budgets are where “amplitude makes the ratio smaller” can
appear. They are not \(\mathcal R_\star\).

Route N / Q6 / LP-shell floors are **not** Lemma★.

---

## What a proof would have to be

Reason from how signed triads add that stretching cannot get large
unless spectrum also spreads or phases cancel. HH→L is the channel
that could refuse that. That reason is **NOT written**.

**NS not solved.**
