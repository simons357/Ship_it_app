# Attack 9B — Exact-shell + closing packet — results

**Attack 9A:** did **NOT** kill Lemma★ (Ds grew faster than Tc).
**Kill lane:** LIVE
**NS solved:** false
**Lemma★:** OPEN
**max K seen:** 0.6410131735094131
**at (α,β):** (4, 8)
**controls_all_pass:** True
**eps_limit_all_pass:** True

| α | β | n_pos | K | Π_βB L2 | Ds(ε=0) | ε-limit OK |
|---|---|-------|---|---------|---------|------------|
| 4 | 8 | 3 | 6.410132e-01 | 1.132266e+00 | 0.0 | True |
| 1 | 2 | 3 | 5.784651e-01 | 5.378034e-01 | 0.0 | True |
| 5 | 10 | 10 | 2.978020e-01 | 8.628470e-01 | 2.842170943040401e-14 | True |
| 2 | 4 | 6 | 2.963302e-01 | 5.443622e-01 | 0.0 | True |
| 13 | 26 | 10 | 2.337365e-01 | 1.232594e+00 | -4.547473508864641e-13 | True |
| 9 | 18 | 10 | 1.789419e-01 | 8.973508e-01 | -5.684341886080801e-13 | True |
| 5 | 6 | 10 | 1.005433e-01 | 6.472483e-01 | 8.526512829121202e-14 | True |
| 9 | 10 | 10 | 6.114836e-02 | 7.037767e-01 | -5.684341886080801e-13 | True |
| 6 | 8 | 10 | 5.269380e-02 | 4.869518e-01 | 5.684341886080802e-14 | True |
| 5 | 2 | 10 | 1.232018e-02 | 3.924313e-01 | -2.842170943040401e-14 | True |
| 3 | 12 | 4 | 2.241841e-33 | 4.100464e-17 | 7.105427357601002e-15 | True |
| 1 | 4 | 3 | 0.000000e+00 | 0.000000e+00 | None | None |
| 2 | 5 | 6 | 0.000000e+00 | 0.000000e+00 | None | None |
| 3 | 6 | 4 | 0.000000e+00 | 0.000000e+00 | None | None |
| 6 | 12 | 10 | 0.000000e+00 | 0.000000e+00 | None | None |
| 8 | 4 | 6 | 0.000000e+00 | 0.000000e+00 | None | None |
| 10 | 5 | 10 | 0.000000e+00 | 0.000000e+00 | None | None |
| 4 | 5 | 3 | 0.000000e+00 | 0.000000e+00 | None | None |
| 8 | 9 | 6 | 0.000000e+00 | 0.000000e+00 | None | None |
| 2 | 8 | 6 | 0.000000e+00 | 0.000000e+00 | None | None |
| 1 | 3 | 3 | 0.000000e+00 | 0.000000e+00 | None | None |
| 1 | 5 | 3 | 0.000000e+00 | 0.000000e+00 | None | None |
| 1 | 6 | 3 | 0.000000e+00 | 0.000000e+00 | None | None |
| 1 | 8 | 3 | 0.000000e+00 | 0.000000e+00 | None | None |

Boxed: K_{α,β}=β‖Π_β B(w,w)‖₂²/(α²‖w‖₂⁴).
ε→0: R_★→K for z_β∥Π_β B. Finite sample max ≠ proof. Kill lane LIVE.
Precision: max at (α,β)=(4,8) has β>α → NOT HH→L (higher-shell). Genuine HH→L needs β<α.
Naming: 9A fail, 9B this, 9C fixed-gap (SoT-only), 9D Θ(m²).
Quotient: ratio_R_star_shape only (not legacy ratio_star).
NS not solved.
