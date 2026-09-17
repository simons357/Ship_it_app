# ATTACK 1 — Covariance / Lemma★ amplitude survival

**Status:** numeric probe only. **NS is not solved.**

## Target

**Canonical ★ is the shape form** ([`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md)):
\[
\bigl(\mathfrak T_c(v)\bigr)^2
\le
C_{\mathrm{geom}}\,
\mathcal D_s(v)\,
E(v)\,
Y(v),
\qquad
\mathcal R_\star(v)
=
\frac{\bigl(\mathfrak T_c(v)\bigr)^2}{\mathcal D_s(v)\,E(v)\,Y(v)}.
\]

Equivalent viscosity packaging uses a geometric \(C_0=C_{\mathrm{geom}}/(4\theta)\):
\[
\mathfrak T_c \le \theta\nu(Z-\Lambda Y)+C_0\nu^{-1}\|u\|_2^2 X\Lambda.
\]

Attack 1 asks whether amplitude scaling \(u\mapsto Bu\) at **fixed shape** only rescales size (so \(\mathcal R_\star\) and the pre-Young ratio stay invariant / post-Young falls), and whether random Galerkin / phase rotations keep these ratios from exploding.

Dimensionless ratios tracked:
\[
\mathcal R_\star=\frac{\mathfrak T_c^2}{\mathcal D_s\,E\,Y}
\quad(\text{shape; amp-invariant}),
\qquad
R_{\mathrm{pre}}=\frac{\mathfrak T_c}{\|u\|_2\,X\Lambda}
\quad(\text{pre-Young}),
\qquad
R_{\mathrm{post}}=\frac{\mathfrak T_c}{\|u\|_2^2 X\Lambda}
\quad(\text{post-Young; falls as }1/B).
\]

## Method

`scripts/ns_attacks/attack1_covariance.py` — Fourier Galerkin Stokes moments on \(\mathbb{T}^3\).

## Kill criterion

- \(\sup\mathcal R_\star\to\infty\) on a controlled **shape** family ⇒ Lemma★ \(C_{\mathrm{geom}}\) / \(C_0\) **KILLED**.
- Fixed-shape \(B\to\infty\) alone does **not** kill shape-★ (worst size already cancelled \(\nu\)); it only checks homogeneity.
- \(\mathcal D_s=0\) with \(\mathfrak T_c>0\) ⇒ **★ dead**; pure single shell (both sides vanish) is vacuous.

## Live result (2026-09-10)

**SURVIVE numeric (NOT proof).** Post-Young \(R_{\mathrm{post}}\) falls as \(B\uparrow\). Pre-Young phase diam \(\approx0.155\). See `/opt/cursor/artifacts/ns_five_lane_2026-09-10/attack1.json` and `ATTACK_SYNTHESIS_SIMULTANEOUS.md`. A list of bounded ratios is **not** a uniform \(C_{\mathrm{geom}}\).
