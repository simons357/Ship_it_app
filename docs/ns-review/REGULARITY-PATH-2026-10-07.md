# What gets us closer to regularity — honesty order

**Date:** 7 October 2026  
**Premise:** Nothing on the current task list *gets* to regularity.  
The useful goal is to find which branch has a gap small enough to attack, and stop spending effort on the ones that do not.

Agrees with the independent Oct 7 recompute: finite 17/32 bookkeeping is **clean and correct**; that is **not** proportional progress toward criterion **(17)** or Clay.

---

## Two grades (do not mix)

| Grade | Verdict |
|---|---|
| As **bookkeeping** | **Good.** Finite claims checked; scope discipline (rerun / reported / open); overclaims walked back. |
| As **progress toward regularity** | **Not yet.** High-pass absorption of a *fixed finite* family is the expected regime (\(1/|k|\) falloff). The hard part is **uniformity over shapes** whose low mode sits arbitrarily far below the high pair. |

One scaling datum is unfavorable: adding 15 shapes raised the weighted coefficient from \(\sim 3\rho \approx 1.90\) to \(\rho+3\rho'\approx 3.11\). If that trend continues under coverage growth, the cutoff runs off and the method gives nothing in the limit.

**Number to watch:** not “how many shapes covered,” but whether a **summable charge rule** (or a signed estimate that avoids the sum) exists.

---

## Accounting convention to state explicitly

Zero-pruned combined multiplicity **4** at squared radius \(216\) holds if only the **third shell \(b\)** and the **\(25\) shell** are charged, with the low anchor bounded by \(\sqrt{E_0}\).

If the **low anchors** \(5n^2\) and \(9n^2\) are also charged, squared radius \(3600\) picks up a **fifth** charge (\(9\cdot 20^2\)). The coefficient would become
\[
2\rho + 3\rho' \approx 3.7396
\]
raising \(M\) by about \(20\%\).

Any handoff that quotes “multiplicity 4” must name which shells pay.

---

## Ordered program (closer to a smooth attack)

### 1. Kill test on the shared-budget route  ← **do this first**

Count distinct triad shapes charging a single shell once **every** shape is admitted (not just the two families).

**Convention (locked):** fixed high shell \(c=|q|^2\); other legs from lattice triads with \(1\le|p|^2\le c\); unordered \((a,b,c)\); drop collinear / zero-transfer.

Independent desk counts — **reproduced exactly** by `scripts/ns_attacks/all_shape_charge_count_kill.py`:

| Shell (squared radius) | Shapes charging it | Covered by 32-package | Match |
|---|---|---|---|
| 25 | 266 | 32 | yes |
| 50 | 1 254 | 1 | yes |
| 101 | 5 185 | 0 | yes |
| 401 | 58 550 | 0 | yes |

Growth \(\sim 0.4\,c^2\) while high-pass gain is only \(c^{-1/2}\). An all-shape rule needs average per-shape constants to fall faster than about \(c^{-3/2}\).

With the audit’s \(\rho\) formula: compute the **weighted sum over every shape at each shell**.  
**Expected:** fail. If it fails → **stop extending families**; route closed as a standalone argument.

**Count probe:** done (`results/shared_budget/all_shape_charge_count_kill.json`).  
**Weighted sum:** still needs ZIP / audit **per-shape** \(\rho\) definition (face values \(\rho,\rho'\) alone are not enough).

### 2. Share the energy, not just the dissipation

Current accounting shares dissipation across overlapping shapes but appears to give each shape’s low mode the full \(\sqrt{E_0}\). Low modes share one energy budget too. Fix that to expose the true deficit (expected: energy half a derivative below critical). That exponent is what any extra ingredient must supply.

### 3. Move main effort to the swirl branch

Only place in the program with a critical quantity bounded for free: \(\Gamma=ru^\theta\) obeys a maximum principle. Known gap is **logarithmic**, not a power:

- Lei–Zhang: regularity if \(|\Gamma|\le C|\ln r|^{-2}\) near the axis  
- Wei: \(|\ln r|^{-3/2}\)  
- Equations give \(|\Gamma|\le C\) with **no** logarithm  

Your open target \(C_F\le\eta\nu D_F+B(t)Q\) with independently controlled \(\int B\) **is this gap in different notation**.

Concrete steps:
1. Audit the coupled lower-bound argument (normalization, local existence/closeness).  
2. Build \(B\) from \(\|\Gamma\|_\infty\) and the \(G\) energy; record exactly where the logarithm appears.  
3. Success = any criterion weaker than \(|\ln r|^{-3/2}\), or the same by a new method.

**Cautions:** specialists have worked this logarithm for a decade; even full closure is axisymmetric on \(\mathbb{R}^3\), **not** Clay Statement B on \(\mathbb{T}^3\).

### 4. Park the Ring estimate until it has a bridge

Natural home: Constantin–Fefferman (direction Lipschitz where vorticity is large).  
Ring needs a frequency cutoff — which is the *conclusion*, not a hypothesis. Until a dynamical statement removes that circularity, Ring is a supporting tool with **no route into the budget**.

---

## What to stop

- Adding more shape families as if that approaches (17)  
- Random-phase experiments as worst-case input  
- Anything whose cutoff depends on the **future** solution  
- Describing 32-shape coverage as “progress toward regularity” to reviewers / Dallas  

---

## Immediate asks

1. Attach / commit `Shared-Budget-17-Family-Audit-and-9-25-Extension.zip` so the all-shape **weighted** kill (step 1) can use the audit’s \(\rho\) definition.  
2. State the charging convention (third+\(25\) only vs low anchors too) in every multiplicity quote.  
3. After step 1 fails or passes: pivot main analytic hours to swirl \(B(t)\) (step 3).

---

*NS not solved. Criterion (17) open. Clay open.*
