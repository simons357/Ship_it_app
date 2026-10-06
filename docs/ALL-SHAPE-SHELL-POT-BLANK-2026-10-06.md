# Unfinished blank: all Fourier-triangle shapes, one energy pot

6 October 2026.
**Terminology + remaining obstacle. Not (17). NS not solved.**

Parents:
[`TRUTH-RUN-CAVEATS-2026-10-06.md`](TRUTH-RUN-CAVEATS-2026-10-06.md),
[`BLOCK-5825-PARTIAL-BOUNDS-2026-10-06.md`](BLOCK-5825-PARTIAL-BOUNDS-2026-10-06.md),
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md).

---

## What “shell” means here

In this program a **shell** is an **exact squared-radius
sphere in frequency space**:

\[
\bigl\{\,k\in\mathbb Z^3:\ \lvert k\rvert^2=a\,\bigr\},
\qquad a\in\mathbb N.
\]

It is **geometry on the Fourier lattice**, used to group
modes that share the same \(\lvert k\rvert^2\) in the
triangle identities (6)–(7) and the block ODE (14).

It is **not**:

- a physical shell, cavity, or hole in the fluid,
- a thick dyadic annulus in physical space,
- a material surface in \(\mathbb T^3\).

When we say “shell energy” we mean the \(\ell^2\) mass of
Fourier coefficients on that squared-radius set, e.g.
\(e_a=\sum_{\lvert k\rvert^2=a}\lvert u_k\rvert^2\).
When we say “triangle shape” we mean a scalene multiset
of three distinct squared radii \(\{a,b,c\}\) that admits
integer wavevectors \(p+q+r=0\).

---

## What remains unfinished

Accounting for **all** such triangle shapes **together**,
without repeatedly spending the same frequency-shell’s
energy allowance.

Fixed-pair bounds for \((5,8,25)\) and \((5,10,25)\)
(including outside inputs) may stand on their own.
**SCHEME A** — charge once per shape and sum — fails as
a path to (17), because the number of shapes diverges and
shared frequency shells are overcounted.

What is still needed toward (17): a bookkeeping pot that
lets every admissible scalene shape draw on shell energies
(or on \(X,Y\)) **without paying the same shell over and
over**. That is the open blank. It is a frequency-geometry
assembly problem, not a physical-shell problem.

**Attack now on file:** SCHEME B — prove
\(\lvert\mathcal T_{\mathrm{sc}}\rvert\le C_\star X\sqrt Y\)
by exact-sphere regrouping (same charge pattern as (11)),
then Young into \(\nu Y/4\). Naive Young-after-shape-sum
is **not** enough (probe). See
[`SCHEME-B-SHELL-POT.md`](SCHEME-B-SHELL-POT.md).

---

## STATUS

SHELL = EXACT FOURIER SQUARED-RADIUS SET (NOT PHYSICAL).
SCHEME A / A′: FAILED.
SCHEME B (B1) ONCE-PER-SHELL POT: OPEN → (17).
NS NOT SOLVED.
