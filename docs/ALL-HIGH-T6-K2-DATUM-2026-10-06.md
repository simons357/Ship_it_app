# All-high regeneration: local \(t^6\) for the \(K=2\) datum

6 October 2026.
**Local Taylor of \(\mathcal T_{\mathrm{sc}}(h_2)\) on the PR #165 two-sphere datum.
Not a proof of (17). Not a positive budget episode.
NS not solved.**

Parents:
[`DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md`](DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md)
(full-field \(\mathcal T_{\mathrm{sc}}'(0)=28\); not \(\mathcal T_{\mathrm{sc}}(h_2)\)),
[`SIGNED-SCALENE-NEXT-ATTACK.md`](SIGNED-SCALENE-NEXT-ATTACK.md),
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md) (15)–(17).

Desk twin:
[`ALL-HIGH-T6-K2-DATUM.md`](ALL-HIGH-T6-K2-DATUM.md).

---

## RESULT

For the exact two-sphere datum of the datum-cutoff write,
with frozen cutoff \(K=2\) (admissible for every \(\nu>0\)
because \(h_2(0)=0\)), the regenerated **all-high**
scalene transfer has vanishing Taylor coefficients
through order \(t^5\), and

\[
\boxed{
\mathcal T_{\mathrm{sc}}\bigl(h_2(t)\bigr)
=\frac{15084}{1625}\,t^6+O(t^7).
}
\]

The first nonzero contribution comes from the
three-distinct-radius blocks with squared-radius
multisets

\[
(5,8,25)\qquad\text{and}\qquad(5,10,25).
\]

Those blocks appear once the Galerkin cutoff admits
squared radius \(5\) (and the higher receivers they
feed). Exact arithmetic certifies the **same**
coefficient \(15084/1625\) for every Galerkin cutoff
\(N\ge 5\).

This identifies **genuine all-high regeneration**
\(\mathcal T_{\mathrm{sc}}(h_{K,N})\) on this named
datum with \(K=2\) fixed. It remains **below the
budget’s viscous threshold initially**, so the
integrand \([\mathcal T_{\mathrm{sc}}(h)-\nu Y/4]_+\)
need not turn on from the \(t^6\) onset alone. It
does **not** settle (17).

---

## 1. Datum and cutoff (recall)

Modes (negatives by conjugation), as in the
datum-cutoff write:

\[
\widehat u(1,0,0)=(0,1,1),\quad
\widehat u(0,1,0)=(1,0,1),\quad
\widehat u(-1,-1,0)=i(1,-1,1).
\]

Exact moments: \(E=14\), \(X=20\), \(Y=32\),
\(J=4\), full-field \(\mathcal T=4\),
full-field \(\mathcal T_{\mathrm{sc}}(0)=0\),
full-field \(\mathcal T_{\mathrm{sc}}'(0)=28\).
Squared radii initially \(\{1,2\}\).
\(K=2\) gives \(h_2(0)=0\).

The full-field derivative \(28\) is **not** the
all-high object. The all-high object starts later
in the jet.

---

## 2. Viscosity independence of the leading coefficient

The leading coefficient \(15084/1625\) is
**independent of \(\nu\)**.

Exact arithmetic certifies viscosity independence
and the same coefficient for Galerkin cutoffs
\(N\ge 5\). (Reported method: the all-high
coefficient is a polynomial in \(\nu\) of degree at
most three; four exact rational evaluations at
distinct viscosities certify the constant
\(15084/1625\).) Contributing radius blocks remain
\((5,8,25)\) and \((5,10,25)\).

Tag: **EXACT** for this named datum’s local jet
(finite Fourier / ODE Taylor algebra). Authoritative
packet ZIP name from the author:
`All-High-Regeneration-First-Nonzero.zip` (file into
`packets/` when the upload is present). Independent
recompute of the rational \(15084/1625\) remains
appropriate. Not a numerical ODE fit. Not a positive
budget episode. Not (17).

---

## 3. What this does and does not show

| Object | Status |
|---|---|
| All-high \(\mathcal T_{\mathrm{sc}}(h_2)\) can be nonzero for this datum with \(h_2(0)=0\) | **Yes** — first at order \(t^6\) |
| Orders \(t^0,\ldots,t^5\) of \(\mathcal T_{\mathrm{sc}}(h_2)\) | **Vanish** (this datum) |
| Leading coefficient \(15084/1625\) | **Independent of \(\nu\)**; same for all \(N\ge 5\) |
| Source blocks | \((5,8,25)\), \((5,10,25)\) |
| Positive budget integrand \([\mathcal T_{\mathrm{sc}}-\nu Y/4]_+\) initially | **No** — remains below viscous threshold initially |
| Criterion (17) / \(\sup_N\mathcal S_{K,N}(T)<\infty\) | **OPEN** |
| Failure of (17) on this datum | **Not claimed** |
| Shear filter / two-shell spatial (TS)/(SB) | **Unaltered** |

---

## 4. Relation to the next attack

Gate 3’s first concrete all-high regeneration
witness is now written as a local expansion, not
only as full-field \(\mathcal T_{\mathrm{sc}}'(0)=28\).

Still missing for (17):

1. Control of the integrated positive budget, not
   just the jet of \(\mathcal T_{\mathrm{sc}}(h)\).
2. Uniformity in \(N\) for general smooth data after
   the frozen \(K(u_0,\nu)\) choice — this page is
   one datum.
3. Whether \([\mathcal T_{\mathrm{sc}}(h_2)-\nu Y/4]_+\)
   is ever positive here (compare \(\nu Y/4\) along
   the same jet).

Do not cash \(t^6\) onset as a budget blowup or as
a close.

---

## Companion note (angle / \(\rho_2\))

The filed angle note
[`TWO-TRIANGLE-NORMAL-ANGLE-2026-10-06.md`](TWO-TRIANGLE-NORMAL-ANGLE-2026-10-06.md)
correctly uses \(1/\sqrt2\). Near-antiparallel
cancellation holds for the stated fixed phases.
When partner phases are optimized, the maximum
depends on \(\lvert\cos\theta\rvert\), so either
nearly parallel orientation can approach full
compatibility. That refinement does not restore
\(1/\sqrt2\) as a universal constant.

---

## STATUS

ALL-HIGH \(\mathcal T_{\mathrm{sc}}(h_2)\): LOCAL \(t^6\) ONSET
WITH COEFFICIENT \(15084/1625\), \(\nu\)-INDEPENDENT.
ORDERS \(\le t^5\): VANISH (THIS DATUM).
BLOCKS: \((5,8,25)\), \((5,10,25)\).
BUDGET THRESHOLD / (17): NOT SETTLED.
NS NOT SOLVED.
