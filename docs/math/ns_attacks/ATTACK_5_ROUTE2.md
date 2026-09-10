# ATTACK 5 — Route 2 / Lemma★ kill drill

**Status:** adversarial numeric search. **NS is not solved.**

## Target

Maximize \(|R_\star|=|\mathfrak T_c|/(\|u\|_2^2 X\Lambda)\) over random fields, triads, scale separations, two-shell data, and near-monochromatic perturbations. Also compare alternate remainders (Route 2):
- \(\|u\|_2^2 X\Lambda\) (Lemma★)
- \(X^{3/2}\Lambda\) (Attack-2 survivor)
- \(\mathcal D_s\) (K=0)
- Young-style \(\|B(u,u)\|_2\) products

## Kill criterion

Empirical \(\sup|R_\star|\) exploding (\(\gg 10^3\) on smooth Galerkin families) ⇒ Lemma★ \(C_0\) **KILLED**.
Bounded ratios ⇒ **SURVIVE numeric** — still **not a proof**.

## Method

`scripts/ns_attacks/attack5_route2_kill.py`.

## Live result (2026-09-10)

**SURVIVE numeric.** \(n=978\); max \(\lvert R_{\mathrm{pre}}\rvert\approx5.09\); max \(\lvert C_*\rvert\approx0.0406\); Lemma★ \(C_0\) **not killed**. See `attack5.json` and synthesis.
