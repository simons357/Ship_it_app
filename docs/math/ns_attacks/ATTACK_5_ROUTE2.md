# ATTACK 5 — Route 2 / Lemma★ kill drill

**Status:** adversarial numeric search. **NS is not solved.**

## Target

Kill or bound the **shape** constant
\[
\mathcal R_\star(v)=\frac{\bigl(\mathfrak T_c(v)\bigr)^2}{\mathcal D_s(v)\,E(v)\,Y(v)}
\]
([`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md)). Also track pre-Young \(R_{\mathrm{pre}}=\mathfrak T_c/(\|u\|_2 X\Lambda)\) and alternate remainders (Route 2):
- \(\mathcal D_s\,E\,Y\) (shape ★ denominator)
- \(\|u\|_2^2 X\Lambda\) (viscosity / post-Young packaging)
- \(X^{3/2}\Lambda\) (Attack-2 survivor)
- \(\mathcal D_s\) (K=0)
- Young-style \(\|B(u,u)\|_2\) products

Families: random fields, triads, scale separations, two-shell data, and **almost-single-shell** perturbations (live kill attempt: \(\mathcal D_s\to0^+\) while stretching stays alive).

## Kill criterion

| Signal | Verdict |
|--------|---------|
| \(\sup\mathcal R_\star\to\infty\) (or \(\gg 10^3\)) on smooth Galerkin families | Lemma★ \(C_{\mathrm{geom}}\) **KILLED** |
| \(\mathcal D_s=0\) and \(\mathfrak T_c>0\) | **★ dead** on that field |
| Pure single shell, \(\mathfrak T_c=0=\mathcal D_s\) | vacuous — not a kill |
| Bounded \(\mathcal R_\star\) / \(R_{\mathrm{pre}}\) on the search | **SURVIVE numeric** — still **not a proof**; sample list ≠ uniform constant |

## Method

`scripts/ns_attacks/attack5_route2_kill.py` (includes `almost_single_shell` / mono+eps probe reporting `max_R_star_shape`).

## Live result (2026-09-10)

**SURVIVE numeric.** Shape-form re-run: \(n=1242\); \(\max\mathcal R_\star\approx0.0227\); almost-shell (\(n=740\)) \(\max\mathcal R_\star\sim3.6\cdot10^{-6}\); pure-shell kills \(0\); max \(\lvert R_{\mathrm{pre}}\rvert\approx5.09\); max \(\lvert C_*\rvert\approx0.0406\); Lemma★ \(C_{\mathrm{geom}}\) / \(C_0\) **not killed**. Artifacts: `/opt/cursor/artifacts/ns_five_lane_shape_star/attack5.json`. Sample list ≠ uniform constant. **NS not solved.**
