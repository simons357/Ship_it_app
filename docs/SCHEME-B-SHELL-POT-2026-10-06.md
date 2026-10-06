# SCHEME B — once-per-shell pot for all Fourier-triangle shapes

6 October 2026.
**Attack design + probe. Not (17). NS not solved.**

Parents:
[`ALL-SHAPE-SHELL-POT-BLANK-2026-10-06.md`](ALL-SHAPE-SHELL-POT-BLANK-2026-10-06.md),
[`TRUTH-RUN-CAVEATS-2026-10-06.md`](TRUTH-RUN-CAVEATS-2026-10-06.md),
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md) (7)–(8), (11), (14)–(17).

Probe:
`scripts/ns_attacks/scheme_b_shell_pot_probe.py`
→ `SCHEME-B-SHELL-POT-PROBE.json`.

---

## Terminology

A **shell** is an exact Fourier squared-radius set
\(\{k\in\mathbb Z^3:\lvert k\rvert^2=a\}\).
Geometry in frequency space — **not** a physical shell
or hole in the fluid.

A **shape** is an admissible scalene multiset
\(\{a,b,c\}\) of three distinct shell labels.

---

## RESULT

| Scheme | Status |
|---|---|
| **A** — bound each \(\int\lvert\mathcal T_{abc}\rvert\), sum on shapes | **FAILED** (truth run) |
| **A′** — Young-split the shape sum onto shells after the fact | **FAILED as a close** — still deposits shape-degree mass on each shell (probe) |
| **B** — regroup signed \(\mathcal T_{\mathrm{sc}}\) at mode / exact-sphere level; charge each \(e_a\) \(O(1)\) times; compare to \(\nu Y/4\) | **OPEN — plow** |

(17) remains **OPEN**. This page replaces the blank’s
“need a pot” with a concrete bookkeeping target and kills
one false shortcut.

---

## 1. Why SCHEME A / A′ cannot be patched by division

Census (probe, \(c\le 30\)): **631** shapes; busiest
shells sit in **≥100** shapes. From \(r_{\max}=20\to 30\):

| Proxy | Growth factor |
|---|---|
| #shapes | \(3.30\) |
| Degree-inflated shell mass \(\sum_a\mathrm{touch}(a)\,a^{3/2}\) | \(6.20\) |
| Once-per-shell mass \(\sum_a a^{3/2}\) | \(2.51\) |
| Ratio (degree-inflated) / (once-shell) | \(31\to 76\) |

So any majorant that secretly carries a factor of
\(\mathrm{touch}(a)\) diverges with the cutoff.

**Naive Young (SCHEME A′).** Starting from a shapewise
Hölder face
\(\lvert\mathcal T_{abc}\rvert\le\kappa\sqrt{c}\,(e_a e_b e_c)^{1/2}\)
and splitting
\(\sqrt{e_a e_b e_c}\) equally onto \(\{a,b,c\}\) still
asks shell \(a\) for \(\sim\mathrm{touch}(a)\) deposits.
Under a model tail \(e_a=1/a^2\), the worst shells are
over-asked by factor \(\sim 6\) at \(r_{\max}=20\) and
\(\sim 9\) at \(r_{\max}=30\) relative to a once-face
\(a^{3/2}e_a^{3/2}\). Young-after-shape-sum is **not**
the pot.

Dividing each shape’s charge by \(\mathrm{touch}(a)\)
makes the majorant too small unless the prefactor grows
with degree — returning to A.

---

## 2. SCHEME B — the pot (target inequality)

Keep the **signed** sum first (as in (7) and the
two-shell assembly (TS)):

\[
\mathcal T_{\mathrm{sc}}(u)
=\sum_{\substack{a<b<c\\ \text{admissible}}}
\mathcal T_{abc}(u).
\]

Do **not** pass to \(\sum\lvert\mathcal T_{abc}\rvert\)
as the primary object.

**Target (OPEN to prove).** Absolute constants
\(C_\star\) (from exact-sphere geometry (8), not from
\#shapes) such that, for every mean-zero divergence-free
field,

\[
\boxed{
\lvert\mathcal T_{\mathrm{sc}}(u)\rvert
\le
C_\star\,X\sqrt{Y}.
}
\tag{B1}
\]

Each shell energy \(e_a\) enters only through the
moments

\[
X=\sum_a a\,e_a,\qquad Y=\sum_a a^2 e_a
\]

— **once per shell**, independent of
\(\mathrm{touch}(a)\). This is the same charge pattern
that already succeeded for repeated radius in (11)
(\(\lvert\mathcal T_{\mathrm{rep}}\rvert\le(\sqrt3/2)X\sqrt Y\)).

**Budget bridge (OPEN).** With Young’s inequality at
the viscosity share reserved for scalene in (15),

\[
C_\star X\sqrt Y
\le
\frac\nu4\,Y+\frac{C_\star^2}{\nu}X^2,
\]

hence

\[
\bigl[\mathcal T_{\mathrm{sc}}-\nu Y/4\bigr]_+
\le
\frac{C_\star^2}{\nu}X^2
\quad\text{whenever (B1) holds with room for the share.}
\]

Then

\[
\mathcal S_{K,N}(T)
\le
\frac{C_\star^2}{\nu}\int_0^T X_N\,dt
\le
\frac{C_\star^2 E_0}{2\nu^2},
\tag{B2}
\]

using \(E'+2\nu X=0\). That would give (17) with any
fixed \(K\) (e.g. the datum cutoff already on file).

**Tags.** (B1)–(B2) are **OPEN** attack targets, not
claims. Shears give \(\mathcal T_{\mathrm{sc}}=0\), so they
do not obstruct (B1); they remain the rejection test
that energy-only \(L^3\) strengthenings failed.

---

## 3. How to prove (B1) — exact-sphere regrouping

The repeated-radius proof of (11) did **not** sum
per-shape constants. It:

1. assembled signed channels on exact spheres,
2. applied the sphere incidence bound (8)
   (\(\sum L_k^2\le 3F^2\), no fiber-occupancy factor),
3. weighted Cauchy–Schwarz into \(\sum a^{3/2}e_a\le\sqrt{XY}\).

**SCHEME B plow (same pattern for three distinct radii):**

1. Expand \(\mathcal T_{\mathrm{sc}}\) in ordered
   mixed-input channels
   \(j_{\gamma\leftarrow\alpha\beta}\) with
   \(\alpha,\beta,\gamma\) pairwise distinct, keeping
   receiver / radius-difference factors from (7)
   **before** absolute values (mirror (SC)–(SB)).
2. For each ordered donor pair \((\alpha,\beta)\), assemble
   the convolution **across all output modes first**.
   Unrestricted Plancherel gives
   \(\sum_k L_k^2=e_\alpha e_\beta\) exactly for
   \(L_k=\sum_{p+q=k}r_p s_q\); restricting to scalene
   outputs \(\gamma\neq\alpha,\beta\) only decreases the
   left side. Per-shape incidence counting is never
   used.
3. Apply one global Cauchy–Schwarz per donor pair
   against the receiving shell energies, then sum
   donor pairs with radius weights into
   \(\sum a\,e_a=X\) and \(\sum a^2 e_a=Y\)
   (weighted CS as after (11)) — **once per shell**.
4. High-pass: restrict to triads with
   \(\sqrt a,\sqrt b,\sqrt c>K\) for \(\mathcal T_{\mathrm{sc}}(h_K)\);
   cross terms stay in the seated complement \(C\).

**Why Plancherel is the pot.** The identity
\(\sum_k L_k^2=e_\alpha e_\beta\) charges shells
\(\alpha,\beta\) once for that donor pair, independent
of how many scalene shapes touch them. Summing
donor pairs is then a sum over shell **pairs**, which
weighted CS collapses to moments of \(\{e_a\}\). That
is the structural difference from SCHEME A’s sum over
shapes.

**Forbidden shortcuts (already killed):**

- Summing (P1)-style faces over all shapes (SCHEME A).
- Young on \(\sum_{abc}\sqrt{c}\sqrt{e_a e_b e_c}\) without
  regrouping (SCHEME A′ / probe).
- Thick-annulus occupancy counts.
- Crude \(\lvert\widehat B_k\rvert\le\lvert k\rvert E\) before
  signed assembly.

**Allowed inputs:**

- Exact identity (7); block ODE (14) for time evolution
  after a spatial pot exists.
- Exact-sphere lemma (8); repeated-radius template (11).
- Fixed-pair (P1)–(P3) as **special cases** once (B1)
  exists — not as a summation basis.
- Datum cutoff \(K(u_0,\nu)\) from the two-shell note.

---

## 4. Probe facts that steer the plow

From `SCHEME-B-SHELL-POT-PROBE.json`:

- Shape degree and degree-inflated mass grow faster
  than once-shell mass → forbids shape charging.
- Raw mode-completion counts still grow with
  \(r_{\max}\) (max \(308\to 630\) from 20 to 30). That
  is a **count of partner lattice points**, not the
  \(\ell^2\) convolution bound (8). The plow must use
  the quadratic form bound, not raw completion counts.
- Oriented triples per shape stay finite (max 216 at
  \(r_{\max}=30\)) — compatible with occupancy-free
  Hölder **inside one shape**, which is how (P1)’s
  block works; the obstruction is only the **sum over
  shapes**.

From `SCHEME-B-B1-RATIO-PROBE.json` (NUMERICAL, not a proof):

- On random divergence-free shell fields at
  \(r_{\max}=12\) and \(16\), the observed ratio
  \(\lvert\mathcal T_{\mathrm{sc}}\rvert/(X\sqrt Y)\) stayed
  \(\le 0.016\), with max ratio **not growing** from 12 to 16.
- Calibration: the vault’s single-triad example
  (\(a,b,c)=(4,9,13)\), \(\mathcal T=24\), \(X=52\),
  \(Y=532\)) reproduces exactly in the probe code and
  has ratio \(\approx 0.020\).
- So (B1) is **numerically comfortable** relative to the
  repeated-radius constant \(\sqrt3/2\approx 0.866\) in (11).
  The missing step is still the exact-sphere proof, not a
  search for a different moment scale.

---

## 5. Immediate next lemmas (ordered)

0. **Lemma B-bilinear (OPEN; numerically soft).**
   For nonnegative \(r_p\) on shell \(\alpha\), \(s_q\) on
   shell \(\beta\neq\alpha\), set
   \(L_k=\sum_{p+q=k}r_p s_q\). Then for every output
   shell \(\gamma\),
   \[
   \sum_{\lvert k\rvert^2=\gamma}L_k^2
   \le C_{\mathrm{bil}}\,e_\alpha e_\beta
   \]
   with \(C_{\mathrm{bil}}\) absolute (candidate \(1\) or
   \(3\), matching (8)’s spirit). Spot checks on 80
   shapes with \(c\le 20\) gave
   \(\sum L_k^2/(e_\alpha e_\beta)\le 0.91\). This is the
   distinct-shell cousin of (8) — necessary, **not**
   sufficient for (B1) by itself (shape-sum of the
   resulting Hölder faces is still SCHEME A′).

1. **Lemma B-spatial (OPEN).** Prove (B1) for a
   single field — all admissible scalene shapes,
   signed sum, exact spheres. Mirror the (11) write-up:
   assemble first, apply B-bilinear inside the sum,
   weighted CS into \(X\sqrt Y\) **once**.
2. **Lemma B-highpass (OPEN).** Same with
   \(\mathcal T_{\mathrm{sc}}(h_K)\); absorb cross-shell
   feed into \(C\) or into the \(\nu Y/4\) bookkeeping
   without reintroducing shape degrees.
3. **Lemma B-time (OPEN).** Pass from the snapshot
   pot to \(\mathcal S_{K,N}(T)\) via (B2) / Duhamel on
   the assembled object (not per-shape Duhamel summed).
4. Only then claim (17).

Until Lemma B-spatial exists, do not announce a
constant \(C_\star\) as proved. Numerical faces of the
ratio probe are steering only.

---

## STATUS

SCHEME A: FAILED.
SCHEME A′ (YOUNG AFTER SHAPE SUM): FAILED AS A CLOSE (PROBE).
SCHEME B TARGET (B1): \(\lvert\mathcal T_{\mathrm{sc}}\rvert\le C_\star X\sqrt Y\) — OPEN.
BUDGET BRIDGE (B2) ⇒ (17): CONDITIONAL ON (B1) — OPEN.
SHELL = EXACT FOURIER \(\lvert k\rvert^2\) SET (NOT PHYSICAL).
NS NOT SOLVED.
