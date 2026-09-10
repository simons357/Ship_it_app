# Lemma★ — canonical shape form (exact lock)

**Date:** 2026-09-10  
**Branch:** `cursor/ns-five-lane-lemma-star-1390`  
**Lock:** Truth only. **NS is NOT solved.** Lemma★ is **OPEN**. This note locks formulas; it does not prove ★.

## Reframe (lock)

**Lemma★ is no longer a viscosity statement. It is a shape statement.**

Change only the size of a fixed shape \(v\) via \(u=av\). Optimize over size. Worst size cancels \(\nu\). What remains is pure geometry on the shape.

Scripts: `scripts/ns_attacks/stokes_moments.py` (aliases: \(E=\|v\|_2^2\), `Tc`\(=\mathcal T_c\) / \(T_c\), `Ds`\(=\mathcal D_s\), `ratio_R_star_shape`\(=\mathcal R_\star\)).

---

## Torus / Stokes setup

\[
\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3
\]
\[
v(x)=\sum_{k\in\mathbb{Z}^3\setminus\{0\}} v_k e^{ik\cdot x},\quad
k\cdot v_k=0,\quad
v_{-k}=\overline{v_k}.
\]
\[
\lambda_k=|k|^2,\qquad
A=-P\Delta,\qquad
(Av)_k=\lambda_k v_k.
\]

---

## Linear moments

\[
\|v\|_2^2=\sum|v_k|^2,\quad
X=\|A^{1/2}v\|_2^2=\sum\lambda_k|v_k|^2,\quad
Y=\|Av\|_2^2=\sum\lambda_k^2|v_k|^2,\quad
Z=\|A^{3/2}v\|_2^2=\sum\lambda_k^3|v_k|^2,
\]
\[
\Lambda=Y/X.
\]

(Code alias: \(E=\|v\|_2^2\).)

---

## Centered spectral dissipation \(\mathcal D_s\) (3 equivalent forms)

\[
\mathcal{D}_s
=Z-\Lambda Y
=Z-Y^2/X
=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2
=\frac1{2X}\sum_{k,\ell}\lambda_k\lambda_\ell(\lambda_k-\lambda_\ell)^2|v_k|^2|v_\ell|^2.
\]

In particular \(\mathcal D_s\ge 0\).

### Two-eigenvalue shells

Shells \(\alpha,\beta\) with energies \(e_\alpha,e_\beta\) (here \(e_\alpha=\sum_{\lambda_k=\alpha}|v_k|^2\)):

\[
\mathcal{D}_s
=\frac{\alpha\beta(\alpha-\beta)^2\,e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}.
\]

---

## Nonlinear transfer

\[
B(v,v)=P[(v\cdot\nabla)v],\quad
\widehat{B(v,v)}_k
=i\,P_k\sum_{p+q=k}(q\cdot v_p)v_q,\quad
P_k=I-\frac{k\otimes k}{|k|^2}.
\]
\[
T_k(v)
=-\mathrm{Re}\bigl(\widehat{B}_k\cdot\overline{v_k}\bigr)
=\sum_{p+q=k}\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

**Caution:** keep the **signed** complex triad sum. Do **not** replace \(\mathrm{Im}(\cdots)\) by absolute values.

\[
N=-\langle B,Av\rangle=\sum\lambda_k T_k,\quad
M=-\langle AB,Av\rangle=\sum\lambda_k^2 T_k,
\]
\[
T_c
=M-\Lambda N
=\sum_k\lambda_k(\lambda_k-\Lambda)T_k
=\sum_{p+q=k}\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

### Ordered triad / \(p+q+r=0\) form

With \(k=p+q=-r\) (so \(p+q+r=0\)):

\[
T_c
=\sum_{p+q+r=0}
\lambda_{-r}(\lambda_{-r}-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_{-r}})\bigr].
\]

(Equivalent cyclic writings that keep the same signed \(\mathrm{Im}\) are allowed; absolute-value rearrangements are not.)

HH→L channel splits can **identify** a mechanism; only the **complete** signed \(T_c\) enters the kill criterion for ★.

---

## Sign check (spectral drift)

From the Galerkin identities \(X'=-2\nu Y+2N\), \(Y'=-2\nu Z+2M\):

\[
\Lambda'=\frac{2}{X}\bigl(T_c-\nu\mathcal{D}_s\bigr).
\]

---

## Complete quotient / canonical shape★

When \(\mathcal D_s(v)>0\), \(\|v\|_2>0\), \(Y(v)>0\):

\[
\mathcal{R}_\star(v)
=
\frac{
\Bigl[
\sum_{p+q=k}
\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\bigl((q\cdot v_p)(v_q\cdot\overline{v_k})\bigr)
\Bigr]^2
}{
\bigl[\sum\lambda_k(\lambda_k-\Lambda)^2|v_k|^2\bigr]
\bigl[\sum|v_k|^2\bigr]
\bigl[\sum\lambda_k^2|v_k|^2\bigr]
}.
\]

Equivalently
\[
\mathcal{R}_\star(v)=\frac{(T_c(v))^2}{\mathcal{D}_s(v)\,\|v\|_2^2\,Y(v)}.
\]

**Boxed shape inequality (canonical ★):** there exists one geometric constant \(C_{\mathrm{geom}}\) (independent of amplitude and of \(\nu\)) such that for every divergence-free \(v\) on \(\mathbb{T}^3\),
\[
\boxed{
\bigl(T_c(v)\bigr)^2
\le
C_{\mathrm{geom}}\,
\mathcal{D}_s(v)\,
\|v\|_2^2\,
Y(v)
}
\]
i.e. \(\sup_v\mathcal R_\star<\infty\) with that supremum equal to \(C_{\mathrm{geom}}\) (when the sup is finite).

Homogeneity (\(a>0\)):
\[
T_c(av)=a^3 T_c(v),\quad
\mathcal D_s(av)=a^2\mathcal D_s(v),\quad
\|av\|_2^2=a^2\|v\|_2^2,\quad
Y(av)=a^2 Y(v),\quad
\Lambda(av)=\Lambda(v),\quad
\mathcal R_\star(av)=\mathcal R_\star(v).
\]

### Viscosity packaging (derived, not primary)

Young / AM–GM on the amplitude line recovers
\[
T_c\le\theta\nu\mathcal D_s+C_0\nu^{-1}\|v\|_2^2\,Y
=\theta\nu\mathcal D_s+C_0\nu^{-1}\|v\|_2^2\,X\Lambda,
\]
with \(C_0(\theta)=C_{\mathrm{geom}}/(4\theta)\).

---

## Kill / survive table

| Outcome | Verdict |
|---------|---------|
| Some shapes make \(\mathcal R_\star\) arbitrarily large | no finite \(C_{\mathrm{geom}}\) → **★ dead** |
| \(\mathcal D_s=0\) (one Fourier shell) and \(T_c\neq 0\) | **★ dead** on that field |
| Pure single shell, both sides vanish (\(T_c=0=\mathcal D_s\)) | vacuous — not a kill |
| Live kill attempt | almost-single-shell / near two-shell with \(\mathcal D_s\to0^+\) and complete signed \(T_c\) so that \(\mathcal R_\star\to\infty\) |
| Every shape has \(\mathcal R_\star\le K\) | that number is ★ (up to \(4\theta\)) |
| A list of fields with small \(\mathcal R_\star\) | **NOT** that number — those shapes did not kill it |

**Do not confuse** with post-Young \(R_{\mathrm{post}}=T_c/(\|v\|_2^2 Y)\) (scales as \(1/a\)) or pre-Young \(R_{\mathrm{pre}}=T_c/(\|v\|_2\,X\Lambda)\).

## What a proof would have to be

Reason from how **signed** triads add that stretching cannot get large unless spectrum also spreads or phases cancel. HH→L is the channel that could refuse that. That reason is **NOT written**.

**NS not solved.**

## Related

- Status board: [`PROOF_LemmaStar_STATUS.md`](./PROOF_LemmaStar_STATUS.md)
- Synthesis: [`ATTACK_SYNTHESIS_SIMULTANEOUS.md`](./ATTACK_SYNTHESIS_SIMULTANEOUS.md)
- Probe / harness: `scripts/ns_attacks/stokes_moments.py`, `attack5_route2_kill.py`, `lemma_star_near_shell_search.py`
