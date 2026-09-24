# Fourier triangles — Heavy executable-audit board

**24 September 2026.** Board as run. Exit code 1.
This files Heavy’s PASS / FAIL / MISSING / OPEN board. It adds no new
theory. Classical NS stays open. Lemma★ stays **OPEN**. Scalene (17)
stays **OPEN**. The L1 / BOTH SIGNS gate stays **OPEN**.

Reconstruction: [`FOURIER-TRIANGLES-AUDIT-2026-09-20.md`](FOURIER-TRIANGLES-AUDIT-2026-09-20.md).
Equation (1) DA script: [`scripts/fourier_triangle_eq1_S_pq.py`](../scripts/fourier_triangle_eq1_S_pq.py).
Lock: [`data/fourier_triangles_heavy_board_2026-09-24.json`](../data/fourier_triangles_heavy_board_2026-09-24.json).

Passing tests are finite checks of stated identities. They are not
proofs of universal statements.

---

## Board (actual run)

| Group | Result |
|---|---|
| 1 Triangle geometry | **FAIL** on the Heavy run — G1.(1) MISSING INPUT |
| 2 Exact-shell incidence | **PASS** |
| 3 Arithmetic realizability | **MISSING** the unstamped α=98 count |
| 4 Signed / centered transfer | **OPEN** (L1 / BOTH SIGNS stub; (17) unproved) |

Reported totals: PASS 27, FAIL 1, OPEN 2, MISSING 1. Elapsed ~160s.
Exit code 1.

G1.(1) failed closed because Heavy found no on-disk formula / DA
script for \(S_{pq}\). The formula was already in the 20 September
note. This filing seats
[`scripts/fourier_triangle_eq1_S_pq.py`](../scripts/fourier_triangle_eq1_S_pq.py)
so that item is no longer missing input. It does **not** turn the
board into a close.

---

## MISSING (as Heavy listed)

1. **Equation (1), the \(S_{pq}\) decomposition.** Heavy: no formula
   or script on disk, so the test failed closed. The formula is in the
   20 September note. **Now seated** as a named DA script. Symbolic
   residual 0; numeric samples held.
2. **α=98, \(P=(3,5,-8)\), \(Q=(-8,3,5)\), \(K=(-5,8,-3)\), 432
   ordered realizations.** This stamp is not in any source file here.
   **Not computed.** Fail-closed if stamped later without a fixture.
3. **Equation (3).** Only its title was on Heavy’s desk. The equal-length
   check still passed on existing exact code. Our reconstruction already
   has the boxed form; sympy residual 0.
4. **Discrete L1 gate / BOTH SIGNS family.** No definition-as-search
   fixture. The stub stays **OPEN**. A found BOTH SIGNS family becomes
   a permanent Group-4 test. A fixture present without a checker
   **FAILS CLOSED**.
5. **Schulze-Pillot citations behind (12).** Not on disk.
   **BLOCKED-ON-SOURCE.** The Hilbert regressions do not depend on them.

---

## Notes on results (as Heavy listed)

- The (16) checks pass with slack. They used random fields, not
  adversarial ones. That is not a proof of (16) as a uniform estimate,
  and it is not (17).
- A `relevant_primes` helper that returns the product \(2a\Delta\)
  (composite 20 for Gram \((2,3,1)\)) is a defect. This tree factors
  first. For \((2,3,1)\), \(\Delta=5\), \(2a\Delta=20\), the primes
  are \(\{2,5\}\), not \(\{20\}\).

---

## What stays OPEN regardless of this board

- Classical 3-D NS global regularity
- Lemma★
- Theorem (17)
- L1 / BOTH SIGNS family
- (16)+(17) and (18) are separate sufficient routes; neither is proved

**NS not solved.**
