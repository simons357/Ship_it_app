# Phone handoff — NS / DA research status

**For:** Jonathan’s other phones / quick sync  
**Written:** 7 October 2026 (UTC)  
**Updated:** 7 Oct — regularity-path order after independent recompute  
**Tone:** honest research desk — what is closed, what is open, what was only checked here

---

## 30-second status

| Item | Status |
|---|---|
| Clay / unaugmented NS regularity | **NOT solved** |
| 32-shape bookkeeping | **Clean and correct** — not proportional progress toward (17) |
| All-shape charge **counts** (kill step 1a) | **PASS** — desk 266 / 1254 / 5185 / 58550 matched exactly |
| All-shape **weighted** ρ sum (kill step 1b) | **Blocked** — needs ZIP per-shape ρ formula |
| Shared-budget as route to (17) | **Under kill test** — expect fail; if so stop extending families |
| Live main effort | **Swirl** Γ logarithmic gap / independently controlled \(B(t)\) |
| Ring Lemma | **Parked** until a dynamical bridge exists |

---

## Two grades (do not mix)

| Grade | Verdict |
|---|---|
| As **bookkeeping** | **Good.** Finite claims checked; scope discipline; overclaims walked back. |
| As **progress toward regularity** | **Not yet.** Fixed finite family high-pass absorption is the expected regime. Hard part = uniformity over shapes with low mode arbitrarily far below the high pair. |

**Number to watch:** not “how many shapes covered,” but whether a **summable charge rule** (or signed estimate avoiding the sum) exists.

---

## Accounting convention (state every time multiplicity is quoted)

Zero-pruned combined multiplicity **4** at \(R=216\) holds if only the **third shell \(b\)** and the **\(25\) shell** are charged, low anchor bounded by \(\sqrt{E_0}\).

If low anchors \(5n^2\) and \(9n^2\) are also charged, \(R=3600\) picks up a fifth charge (\(9\cdot 20^2\)) → coefficient \(2\rho+3\rho'\approx 3.7396\) (~20% higher \(M\)).

Cutoff formulas (braces restored):

\[
K=\max\bigl\{2,\ 3(M-1)\bigr\},
\qquad
\rho+3\rho'\approx 3.1077752814793693.
\]

---

## Ordered program (closer to a smooth attack)

Full note: `docs/ns-review/REGULARITY-PATH-2026-10-07.md`

### 1. Kill test — shared-budget route (do first)

| Shell \(c\) | Shapes charging it | 32-package | Rerun |
|---|---|---|---|
| 25 | 266 | 32 | match |
| 50 | 1 254 | 1 | match |
| 101 | 5 185 | 0 | match |
| 401 | 58 550 | 0 | match |

Growth \(\sim 0.4\,c^2\) vs high-pass \(c^{-1/2}\). Need average per-shape constant \(\lesssim c^{-3/2}\).

Script: `scripts/ns_attacks/all_shape_charge_count_kill.py`  
Result: `results/shared_budget/all_shape_charge_count_kill.json`

**Next for this step:** attach ZIP → weighted all-shape ρ sum. Expected fail → **stop extending families**.

### 2. Share energy, not just dissipation

Low modes share one \(\sqrt{E_0}\) budget too. Exposes the true deficit (expected: energy half a derivative below critical).

### 3. Main effort → swirl branch

Only critical quantity bounded for free: \(\Gamma=ru^\theta\) maximum principle. Gap is **logarithmic**:

- Lei–Zhang: \(|\Gamma|\le C|\ln r|^{-2}\)
- Wei: \(|\ln r|^{-3/2}\)
- Equations give \(|\Gamma|\le C\) with **no** log

Open target \(C_F\le\eta\nu D_F+B(t)Q\) with controlled \(\int B\) **is this gap in different notation**.

Success = any criterion weaker than Wei’s, or same by a new method.  
**Caution:** decade of specialist work; even full closure is axisymmetric \(\mathbb{R}^3\), **not** Clay Statement B on \(\mathbb{T}^3\).

### 4. Park Ring until it has a bridge

Natural home: Constantin–Fefferman. Needs frequency cutoff = conclusion, not hypothesis. No route into the budget yet.

---

## What to stop

- Adding shape families as if that approaches (17)  
- Random-phase experiments as worst-case  
- Cutoffs that depend on the **future** solution  
- Describing 32-shape coverage as “progress toward regularity” to reviewers / Dallas  

---

## Shared-Budget 17→32 (finite checks — still good)

- **17** from \((5,b,25)\); **15** active from \((9,b,25)\); union **32**
- Independent recompute of lists, multiplicity witnesses, weighted face, swirl root, Gaussian scalings: **all held**
- High-pass for this **restricted** family only — **not** (17)

PR #166 · `verify_families.py`

---

## File / PR map

| Topic | Path / PR |
|---|---|
| This handoff | `docs/ns-review/PHONE-HANDOFF-2026-10-07.md` |
| Regularity path (ordered) | `docs/ns-review/REGULARITY-PATH-2026-10-07.md` |
| Kill-count probe | `scripts/ns_attacks/all_shape_charge_count_kill.py` |
| Swirl bench | `docs/ns-review/DA-SWIRL-FOUR-DOORS-2026-10-06.md` · PR **#167** |
| Ring visuals | PR **#164** (parked for budget) |

---

## One-screen blurb (copy/paste)

> **7 Oct.** 32-shape bookkeeping is clean — not progress toward (17). All-shape charge counts match desk (266/1254/5185/58550); weighted ρ kill still needs ZIP formula; expect fail → stop extending families. Main effort: swirl Γ log gap / controlled B(t). Park Ring without a dynamical bridge. NS not solved.

---

*End of handoff. No regularity claim.*
