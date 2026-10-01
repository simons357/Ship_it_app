# Audit board — 24 September 2026 (REPORTED)

Source: Grok Heavily screenshots of a 24 Sep run. The full board file
`run_audit_board_2026-09-24.txt` is **not on this tree**. Numbers
below are **REPORTED**, not recomputed here.

This book’s locked SBP / \(\phi/d\) / low-tail / sign gates are
**not** altered by filing the report.

**Not a closure theorem.** Ordinary NS is not solved. Soft X silent.

---

## Group summary (REPORTED)

| Group | Result |
|---|---|
| 1 TRIANGLE_GEOMETRY | **FAIL** (one missing input) |
| 2 EXACT_SHELL_INCIDENCE | **PASS** |
| 3 ARITHMETIC_REALIZABILITY | **MISSING** (one unstamped count) |
| 4 SIGNED_CENTERED_TRANSFER | **OPEN** |

Reported totals: PASS 27, FAIL 1, OPEN 2, MISSING 1. Exit code 1.

---

## Missing / fail-closed (as reported)

1. **Equation (1), the \(S_{pq}\) decomposition.** No formula or
   script on that disk, so G1.(1) failed closed. The formula is in
   the 20 Sep note. **Now seated on this book:**
   [`../../packets/FOURIER-TRIANGLES-S-PQ-2026-09-20.md`](../../packets/FOURIER-TRIANGLES-S-PQ-2026-09-20.md).
   That seats the missing input. It does not rerun their 27 tests.

2. **\(\alpha=98\), \(P=(3,5,-8)\), \(Q=(-8,3,5)\), \(K=(-5,8,-3)\),
   432 ordered realizations.** No stamp in any source file on this
   tree. **Not computed. Not invented.**

3. **Equation (3).** Only its title was on that disk; their test
   still passed using an existing exact check. The equal-length form
   is now written next to (1) on this book.

4. **Discrete \(L_{1}\) gate / BOTH-SIGNS family.** No definition or
   fixture on that disk; stub stays **OPEN**. Same on this book:
   [`../../packets/DA-GATE-ARITHMETIC-SIGN-REALIZABILITY-2026-09-24.md`](../../packets/DA-GATE-ARITHMETIC-SIGN-REALIZABILITY-2026-09-24.md).
   Armed, not run. A fixture without a checker fails closed.

5. **Schulze–Pillot citations behind (12).** Not on disk. DA already
   stamps them BLOCKED-ON-SOURCE. The audit does not depend on them.

---

## Notes on the passing tests (REPORTED)

- Group 1 items other than (1) passed (equal-length form, (4) defect,
  300 integer triangles, mixed-shell defect, three-radius identity).
- Group 2: pairing bounds, attack9d \(D\le F^2\), rational weights,
  inc8 max ratio 1.50 against bound 3, shear \(K=2/3\).
- Group 3: Hilbert-symbol implementations agree; witnesses
  \((96,96,0)\) fail \(\{2,3\}\), \((2,3,1)\) fail \(\{2,5\}\),
  \((14,14,-7)\) pass. Census 30140 vs fixture. The \(\alpha=98\)
  stamp is the missing line.
- Group 4: \(0,+24,-24\) fields \(E,X,Y,Z=6,52,532,59800\);
  generated mode \((3,-2,0)\); (18) \(\Lambda'=2(T_c-\nu D_s)/X\) on
  a 26-mode Galerkin field. Theorem (17) **OPEN**.

Two cautions from that run, kept as reported:

- The (16) tests pass with slack because they use **random** fields,
  not adversarial ones.
- A helper `hilbert_gram.relevant_primes` can return composites
  (e.g. 20 for \((2,3,1)\)). That helper is **not on this tree**.

---

## What remains OPEN regardless of this board

Classical 3-D NS global regularity. Unrestricted Lemma★ is already
dead on \(v_n\) here; the formula lock is separate.
Theorem (17). The \(L_1\) / BOTH-SIGNS family.
(16)+(17) and (18) are separate sufficient routes; neither is proved.

**NS not solved.**
