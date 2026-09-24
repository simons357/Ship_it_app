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

## Notes on results (as Heavy listed, now tightened)

- The (16) **trajectory** test never exercises the bound’s key term.
  \(S\) stayed at \(0\) along that run, so
  \([\mathcal T_{\mathrm{sc}}-\nu Y_N/4]_+\) was never tested.
  Rerun on a 20 September trajectory with \(S>0\):
  \(\nu=3/2\), \(K=1\), \(N^2=12\) or \(20\). Those \(S(1)\) values
  were reported, not rerun here. The random pointwise tests at
  \(2.65\times10^{-6}\) are loose for the same reason. Slack is not
  a proof of (16), and it is not (17).
- Fix `hilbert_gram.relevant_primes` **in the source**, not around
  it. The source is now [`scripts/hilbert_gram.py`](../scripts/hilbert_gram.py).
  Callers in this tree: `scripts/fourier_triangles_audit.py` and
  `tests/test_fourier_triangles_heavy_board.py`. For Gram
  \((2,3,1)\), \(\Delta=5\), \(2a\Delta=20\), the primes are
  \(\{2,5\}\), not \(\{20\}\). `hilbert_symbol` rejects a composite
  \(\ell\).

G4.odd’s closed form \(8A^2(6A-133)\) is right:
\(48A^3-1064A^2\) factors to exactly that. At \(A=24\) this is
\(X'=50688\). The conventions block agrees with (13).

---

## L1 / BOTH SIGNS fixture spec — still OPEN

[`data/l1_both_signs_fixture_spec.json`](../data/l1_both_signs_fixture_spec.json).
A BOTH SIGNS result is not admissible unless all three pre-run
conditions hold:

1. \(R_{2,N}\) scales in \(\varepsilon\) with exponent above about
   \(1.8\).
2. Signs are classified only after removing the trivial symmetries
   \(u\to-u\), phase gauge, and parity.
3. Normalization stays uniform in \(N\), and signs are decided in
   exact arithmetic.

Without these, BOTH SIGNS can come purely from \(u\to-u\). A fixture
present without a checker **FAILS CLOSED**. No family is invented
here.

---

## Expected board after the three seated files

| Group | Expected |
|---|---|
| 1 Triangle geometry | **PASS** (equation (1) DA script seated) |
| 2 Exact-shell incidence | **PASS** |
| 3 Arithmetic realizability | **PASS** only if the α=98 / 432 fixture is stamped. It is **not** stamped here |
| 4 Signed / centered transfer | **OPEN** — L1 gate and (17) |
| 5 Static uniform \(\mathcal R_\star\) | **PASS** as a kill of the uniform shape bound, on the separate Attack 10 localized-bump filing. NS is still open |

That expected exit code is 0 **only after** G3’s α=98 fixture exists
and G5 is accepted as a static kill, not a close of NS. This packet
does not invent the α=98 count and does not merge Attack 10.

---

## What stays OPEN regardless of this board

- Classical 3-D NS global regularity
- Theorem (17)
- L1 / BOTH SIGNS family (until a fixture meets the three pre-run conditions)
- (16) as a uniform estimate (the \(S\equiv0\) trajectory does not test it)
- DA-NS-2

**NS not solved.**
