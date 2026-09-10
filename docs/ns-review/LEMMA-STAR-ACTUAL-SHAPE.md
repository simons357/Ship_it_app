# Lemma★ — actual shape (SoT card)

**NS not solved.** Lemma★ is **OPEN**. This is the geometric / shape-form statement only.

---

**This is the shape:**

\[
\boxed{
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,
D_s(v)\,
\|v\|_2^2\,
Y(v)
}
\]

with decisive quotient
\[
\mathcal{R}_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,\|v\|_2^2\,Y(v)}
\qquad\bigl(D_s\|v\|_2^2 Y>0\bigr),
\]
so ★ says \(\sup_v\mathcal{R}_\star<\infty\) and that finite supremum is \(C_{\mathrm{geom}}\) (when it exists).

Code name for this quotient: **`ratio_R_star_shape`**. Do **not** use legacy **`ratio_star`** \(=T_c/(E X\Lambda)\) — different packaging.

---

## What “shape” means

Change only amplitude via \(u=av\); optimize size. Viscosity \(\nu\) cancels. What remains is pure divergence-free geometry of \(v\) on \(\mathbb{T}^3\).

---

## Symbol definitions (absolute)

Torus / Stokes:
\[
\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3,\qquad
v=\sum_{k\neq0}v_ke^{ik\cdot x},\quad k\cdot v_k=0,\quad v_{-k}=\overline{v_k},
\]
\[
\lambda_k=|k|^2,\qquad A=-P\Delta,\qquad (Av)_k=\lambda_k v_k.
\]

Linear moments:
\[
\|v\|_2^2=\sum|v_k|^2,\quad
X=\|A^{1/2}v\|_2^2=\sum\lambda_k|v_k|^2,\quad
Y=\|Av\|_2^2=\sum\lambda_k^2|v_k|^2,\quad
Z=\|A^{3/2}v\|_2^2=\sum\lambda_k^3|v_k|^2,
\]
\[
\Lambda=Y/X.
\]

Centered spectral dissipation \(D_s=\mathcal{D}_s\) (equivalent forms):
\[
D_s
=Z-\Lambda Y
=Z-Y^2/X
=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2
=\frac1{2X}\sum_{k,\ell}\lambda_k\lambda_\ell(\lambda_k-\lambda_\ell)^2|v_k|^2|v_\ell|^2
\ge 0.
\]

Nonlinear transfer (signed triads only):
\[
T_k=\sum_{p+q=k}\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr],
\]
\[
N=\sum\lambda_k T_k,\quad
M=\sum\lambda_k^2 T_k,\quad
T_c=M-\Lambda N=\sum_k\lambda_k(\lambda_k-\Lambda)T_k.
\]

Positive part: \(T_c_+=\max(T_c,0)\).

---

## Viscosity form (derived, not primary)

Young / AM–GM on the amplitude line recovers the original budget packaging:
\[
T_c\le\theta\nu D_s+C_0\nu^{-1}\|v\|_2^2\,Y
=\theta\nu D_s+C_0\nu^{-1}\|v\|_2^2\,X\Lambda,
\]
with \(C_0(\theta)=C_{\mathrm{geom}}/(4\theta)\). After \(u=av\) size optimization, \(\nu\) cancels and the shape inequality above is what remains.

---

## Kill criteria

| Outcome | Verdict |
|---------|---------|
| \(\sup\mathcal{R}_\star=\infty\) | no finite \(C_{\mathrm{geom}}\) → **★ dead** |
| One bad shape: \(D_s=0\) and \(T_c>0\) | **★ dead** on that field |
| Pure single shell, \(T_c=0=D_s\) | vacuous — not a kill |
| Finite small samples of \(\mathcal{R}_\star\) | **≠** uniform bound |

One counterexample shape kills ★. Failure to find one does **not** prove ★.

---

## Attack 9B relation (special family)

Exact-shell + closing \(v_\varepsilon=w_\alpha+\varepsilon z_\beta\) with \(z_\beta\parallel\Pi_\beta B(w_\alpha,w_\alpha)\) gives
\[
\lim_{\varepsilon\to0}\mathcal{R}_\star(v_\varepsilon)=K_{\alpha,\beta}(w),\qquad
K_{\alpha,\beta}=\sup_{Aw=\alpha w}\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}.
\]
So \(K_{\alpha,\beta}\) is \(\mathcal{R}_\star\) on that near-shell family — a special case, not a different lemma.

---

**Sources:** `docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md` (PR #48 / `cursor/ns-five-lane-lemma-star-1390`), `docs/ns-review/LEMMA-STAR-EXACT-FORMULAS.md`, Attack 9B exact-shell closing.

**NS not solved.**
