# ATTACK 2 — Triad / K=0 kill / \(C_* X^{3/2}\Lambda\)

**Status:** numeric probe only. **NS is not solved.**

## Targets

1. **K=0 absorption** \(T_c\le\theta\nu D_s\): expected **DEAD** (ratio \(T_c/D_s\) grows with amplitude). Viscosity alone on spread cannot absorb cubic stretching.
2. **Survivor** \(T_c\le\theta\nu D_s+C_* X^{3/2}\Lambda\) with \(K\sim\sqrt{X}\), Leray-integrable if \(\int X<\infty\).
3. **Shape-★ check on the triad:** fixed-shape amplitude sweeps must leave
   \[
   \mathcal{R}_\star=\frac{(T_c)_+^2}{D_s\,E\,Y}
   \]
   invariant (scripts: `ratio_R_star_shape`). That invariance is **required** by the shape reframe; it is **not** a proof that \(\sup\mathcal{R}_\star<\infty\). See [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md).

Aliases: \(T_c=\mathcal{T}_c\), \(D_s=\mathcal{D}_s\), \(E=\|v\|_2^2\).

## Method

Fixed-shape high triad amplitude sweep; \(X=1\) shape scan; scale-separated triads.
Script: `scripts/ns_attacks/attack2_triad_k0_cstar.py`.

## Live result (2026-09-10)

**K=0 DEAD** (\(\lvert T_c\rvert/D_s\sim B\)). **\(C_*\approx0.004058\)** amp-invariant on fixed triad. See `attack2.json`.

**Shape lesson:** \(u=av\) on this triad cancels \(\nu\) and leaves a finite \(\mathcal{R}_\star\) for **this** shape only. That does not certify a uniform geometric constant over all divergence-free fields.
