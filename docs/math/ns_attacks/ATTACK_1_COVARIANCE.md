# ATTACK 1 — Covariance / Lemma★ amplitude survival

**Status:** numeric probe only. **NS is not solved.**

## Target

**Canonical ★ is the shape form** ([`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md)):
\[
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,
D_s(v)\,
\|v\|_2^2\,
Y(v),
\qquad
\mathcal{R}_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,\|v\|_2^2\,Y(v)}.
\]
Aliases: \(T_c=\mathcal{T}_c\), \(D_s=\mathcal{D}_s\), \(E=\|v\|_2^2\). Here \(T_c{}_+=\max(T_c,0)\).

Equivalent viscosity packaging uses a geometric \(C_0(\theta)=C_{\mathrm{geom}}/(4\theta)\):
\[
T_c \le \theta\nu D_s+C_0(\theta)\nu^{-1}\|u\|_2^2 Y
\]
(with \(D_s=Z-\Lambda Y\) and \(Y=X\Lambda\)).

Attack 1 asks whether amplitude scaling \(u\mapsto Bu\) at **fixed shape** only rescales size (so \(\mathcal{R}_\star\) and the pre-Young ratio stay invariant / post-Young falls), and whether random Galerkin / phase rotations keep these ratios from exploding.

Dimensionless ratios tracked:
\[
\mathcal{R}_\star=\frac{(T_c)_+^2}{D_s\,E\,Y}
\quad(\text{shape; amp-invariant}),
\qquad
R_{\mathrm{pre}}=\frac{T_c}{\|u\|_2\,X\Lambda}
\quad(\text{pre-Young}),
\qquad
R_{\mathrm{post}}=\frac{T_c}{\|u\|_2^2 X\Lambda}
\quad(\text{post-Young; falls as }1/B).
\]

## Method

`scripts/ns_attacks/attack1_covariance.py` — Fourier Galerkin Stokes moments on \(\mathbb{T}^3\).

## Kill criterion

- \(\sup\mathcal{R}_\star\to\infty\) on a controlled **shape** family ⇒ Lemma★ \(C_{\mathrm{geom}}\) / \(C_0\) **KILLED**.
- Fixed-shape \(B\to\infty\) alone does **not** kill shape-★ (worst size already cancelled \(\nu\)); it only checks homogeneity.
- \(D_s=0\) with \(T_c>0\) ⇒ **★ dead**; pure single shell (both sides vanish) is vacuous.

## Live result (2026-09-10)

**SURVIVE numeric (NOT proof).** Post-Young \(R_{\mathrm{post}}\) falls as \(B\uparrow\). Pre-Young phase diam \(\approx0.155\). See `/opt/cursor/artifacts/ns_five_lane_2026-09-10/attack1.json` and `ATTACK_SYNTHESIS_SIMULTANEOUS.md`. A list of bounded ratios is **not** a uniform \(C_{\mathrm{geom}}\).
