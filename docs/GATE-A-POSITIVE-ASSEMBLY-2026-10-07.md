# Gate A — positive shared-budget all-shape load

7 October 2026.
**CLOSED — Outcome B (kill certificate). Not (17).**

Parents:
[`NS-HANDOFF-2026-10-07.md`](NS-HANDOFF-2026-10-07.md),
[`SHARED-BUDGET-32-SHAPE-EXTENSION-2026-10-06.md`](SHARED-BUDGET-32-SHAPE-EXTENSION-2026-10-06.md).

Probe:
`scripts/ns_attacks/rho_formula_and_growth_probe.py`
→ `RHO-FORMULA-AND-GROWTH-PROBE.json`.

Program order:
[`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).

---

## RESULT — Outcome B

| Item | Status |
|---|---|
| Finite-family mechanism (17/32/51) | Real and exact at stated scope — **laboratory**, not the all-shape route |
| Further 52/70/100 family extensions | **PARKED** — do not add |
| Charging convention | **FROZEN** (F1 family / F2 all-shape diagnostic) |
| Explicit \(\rho_a\) at fixed \(c_\star=25\) | Reproduces \(\rho_5,\rho_9,\rho_{13}\) **exactly** (**Rerun here**) |
| General-\(c\) \(\rho\) | **Authorized** for Gate A (same face, variable output shell) |
| Aggregate load \(\mathcal A(c)=\sum\rho_a(c)\) | **Growing** (matches author table) |
| Load vs \(c^{-1/2}\) viscous gain \(\mathcal R=\mathcal A/\sqrt{c}\) | **Not uniformly controlled** (\(0.94\to 3.43\) on author spine) |
| Straight positive summation → all shapes | **KILL CERTIFICATE** — Outcome B |
| Next | **Gate B** — shared-energy correction; extract exact missing exponent |

Two useful outcomes only; this filing is **B**:
weighted load diverges too fast under the frozen positive assembly.
Never spend another day extending finite families by brute force.

---

## 1. Frozen charging convention

Ambiguity killed: “multiplicity 4 vs 5,” which shells pay, whether the
low anchor is paid from global energy.

### Direct answers

| Question | Frozen answer |
|---|---|
| Largest shell only? | **No.** Dissipation bookkeeping is not a private largest-only share. |
| Largest + middle? | **Third labels \(b\) + family endpoints \(c_\star\)** share dissipation when dilated labels coincide. Middle/third coincidence is the primary multiplicity witness. |
| Low anchor from global energy? | **Yes.** Present high-pass faces give each family coefficient a full \(\sqrt{E_0}\) factor — deliberately crude. That is exactly Gate B. |
| Multiplicity 4 vs 5? | **Never 5.** Use **literal 6** (pre zero-prune) vs **zero-pruned 4** (witness \(R=216\)). Third-shell coincidence ≠ endpoint coincidence. |

### Convention F1 — fixed-anchor family (17/32/51 laboratory)

- A **family** is a fixed ordered anchor pair \((a_\star,c_\star)\)
  (examples: \((5,25)\), \((9,25)\), \((13,25)\)) plus active third
  labels \(B\).
- Shape: \((a_\star,b,c_\star)\) and dilations
  \((a_\star n^2, bn^2, c_\star n^2)\).
- **\(c_\star\) is the family output / high-pass endpoint**, not
  necessarily \(\max\{a_\star,b,c_\star\}\). Third labels may exceed
  \(c_\star\) (e.g. \(B_5\) up to 52, \(B_9\) up to 62, \(B_{13}\) up to 74).
- Zero-transfer / collinear endpoints removed from \(B\) before charge counts.
- **Dissipation multiplicity** (zero-pruned): number of distinct
  \((\mathrm{family},b,n)\) with **third-shell** physical radius
  \(bn^2=R\). Witness: \(R=216\) has multiplicity **exactly 4**.
- Literal multiplicity **6** (before zero-prune) is a separate accounting
  (ZIP charge-groups); do not conflate with 4.
- Endpoint \(c_\star\) is charged separately when both families hit the
  same dilated endpoint.
- Family coefficient:
  \[
  \rho_{a_\star}
  =\frac1{2c_\star}
  \left(\sum_{b\in B}
  \frac{C_{a_\star,b;c_\star}^2}{b^2}\right)^{1/2},
  \]
  with
  \[
  C_{a,b;c}
  =
  \sqrt{3\Delta_{a,b;c}}
  \left(
  \frac{\lvert c-b\rvert}{\sqrt a}
  +\frac{\lvert c-a\rvert}{\sqrt b}
  +\frac{\lvert b-a\rvert}{\sqrt c}
  \right).
  \]

### Convention F2 — largest-shell diagnostic (all-shape stress test)

- Fix geometric largest squared radius \(c\) (so \(a<b<c\)).
- Group by smallest shell \(a\); \(B_a=\{b:(a,b,c)\text{ active}\}\).
- \(\rho_a(c)\) by the same formula with this \(c\).
- Aggregate equal-allocation family charge:
  \[
  \mathcal A(c)=\sum_{a}\rho_a(c),\qquad
  \mathcal R(c)=\mathcal A(c)\,/\,\sqrt{c}.
  \]

**Rerun here** (matches author diagnostic table on the spine):

| \(c\) | \#shapes \(a<b<c\) | \(\mathcal A(c)\) | \(\mathcal R(c)\) |
|---:|---:|---:|---:|
| 25 | 47 | 4.6857 | 0.937 |
| 50 | 226 | 9.8482 | 1.393 |
| 101 | 973 | 20.5423 | 2.044 |
| 200 | 1636 | 26.2789 | 1.858 |
| 401 | 11078 | 68.7256 | 3.432 |

Author faces \(4.69,\ 9.85,\ 20.54,\ 68.73\) and relatives
\(0.94,\ 1.39,\ 2.04,\ 3.43\) — same convention at \(c\in\{25,50,101,401\}\).
(The \(c=200\) row is an extra probe point; \(\mathcal R\) dips locally
then rises again — **no uniform control**.)

### What is paid where

| Factor | Paid from | Notes |
|---|---|---|
| Third label \(b\) (dilated) | Shell dissipation / \(Y\) shares | Primary multiplicity witness |
| Family endpoint \(c_\star\) | Same dissipation bookkeeping | Extra when families share endpoint |
| Low-anchor amplitudes inside \(\rho\) | Global \(\sqrt{E_0}\) | Gate B forces \(\sum\lvert u_k\rvert^2=E\) |

---

## 2. General \(\rho\) beyond fixed \(c=25\)

### Authorized expression

\[
\boxed{
\rho_a(c)
=
\frac1{2c}
\left(\sum_{b\in B_a(c)}
\frac{C_{a,b;c}^2}{b^2}\right)^{1/2}
}
\]

with \(C_{a,b;c}\) as above. No special role for the numeral 25:
it is only a convenient laboratory endpoint. The same Young /
exact-shell / triple-product face that produces the fixed-\(25\)
coefficients produces the variable-\(c\) face by substituting the
family output shell.

### Fixed-\(c_\star=25\) reproduction (**Rerun here**)

| Anchor | \(B\) | Target | Computed | Match |
|---|---|---|---|---|
| 5 | 17 labels (handoff) | 0.6318550824 | 0.6318550823987904 | **YES** |
| 9 | 15 active (handoff) | 0.8253067330 | 0.8253067330268598 | **YES** |
| 13 | \(2,4,8,14,18,20,22,26,36,38,40,50,54,56,58,62,68,72,74\) | 1.0833160571 | 1.0833160571479… | **YES** |

Prior miss on \(\rho_{13}\) was an enumeration bug (capping \(b\le c_\star\));
package lists for \(B_5,B_9\) already allow \(b>c_\star\).

---

## 3. Kill certificate (Outcome B)

**Claim (positive all-shape assembly).** Under Convention F2 and the
authorized general-\(c\) coefficient, the equal-allocation load
\(\mathcal A(c)=\sum_a\rho_a(c)\) grows with the high shell, and the
ratio to available high-frequency viscous gain
\(\mathcal R(c)=\mathcal A(c)/\sqrt{c}\) is **not uniformly bounded**
on the computed spine (author table reproduced; \(\mathcal R\) from
\(0.94\) at \(c=25\) to \(3.43\) at \(c=401\)).

**Structural spine (source-backed, not re-proved here):**
\[
W\ge\sum_a 2\rho_a\sqrt{m_{a,1}}.
\]
If those positive terms diverge over an infinite extension, that
Young-allocation method cannot produce a finite \(W\).

**Ruling.** Straight positive shared-budget summation **cannot** be
the all-shape route. Finite-family success (17/32/51) remains real at
stated scope and is **not** withdrawn — it is laboratory evidence of
a mechanism that works when the network is finite and overlaps are
controlled. What fails is **naive infinite positive assembly**.

**Do not:** add a 52nd / 70th / 100th family; fish random phases;
promote B41 into NSE dynamics; substitute swirl for the 3-D target;
revive Ring without a dynamical bridge.

---

## 4. Immediate next — Gate B

Force low-frequency factors to share actual energy
\[
\sum_k\lvert u_k\rvert^2=E
\]
instead of each borrowing a full \(\sqrt{E_0}\). Redo the aggregate.
Extract the **exact missing exponent** (schematic target:
\(\mathcal T_{\mathrm{bad}}\lesssim\nu Y\cdot\Lambda^{1/2}\)
⇒ need a half derivative of cancellation / geometric gain).
That number becomes the sole target for Gate D structural attacks.

---

## STATUS

GATE A: **CLOSED — OUTCOME B (KILL CERTIFICATE).**
CHARGING: F1 + F2 FROZEN; MULTIPLICITY LANGUAGE FIXED (6 LITERAL / 4 ZERO-PRUNED).
ρ₅, ρ₉, ρ₁₃: RERUN MATCH.
GENERAL-\(c\) ρ: AUTHORIZED FOR GATE A STRESS TEST.
POSITIVE ALL-SHAPE ASSEMBLY: DOES NOT SCALE.
NEXT: GATE B (SHARED ENERGY) → GATE C (EXACT DEFICIT) → GATE D (STRUCTURE ON THAT DEFICIT ONLY).
NO MORE FINITE FAMILY EXTENSIONS.
(17) NOT CLAIMED.
NS NOT SOLVED.
