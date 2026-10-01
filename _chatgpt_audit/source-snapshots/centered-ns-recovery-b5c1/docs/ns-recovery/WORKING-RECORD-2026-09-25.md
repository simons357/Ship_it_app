# Working record — 25 September 2026

Internal filing of the later report. **Not a share-ready close.**
Ordinary NS is not solved. Soft X silent.
Do not put \(K(t)\) in the PDE.
This page does **not** alter the locked SBP / \(\phi/d\) / low-tail /
sign / \(S_{pq}\) / shape-form packets.

Clock: [`CENTERED-EQUATION.md`](CENTERED-EQUATION.md).
Freeze: [`CENTERED-RESIDUAL-BOARD.md`](CENTERED-RESIDUAL-BOARD.md).
Young \(\nu\) lock:
[`../../packets/DA-GATE-YOUNG-OCCUPATION-NU-2026-09-25.md`](../../packets/DA-GATE-YOUNG-OCCUPATION-NU-2026-09-25.md).
Q4-0 plan (DA must approve; **not run**):
[`../../packets/DA-GATE-Q4-0-SIX-MODE-CALIBRATION-2026-09-25.md`](../../packets/DA-GATE-Q4-0-SIX-MODE-CALIBRATION-2026-09-25.md).

---

## How this page is to be read

The report holds together. Most of it matches what is already on
this tree. One missing factor and two sourcing gaps are fixed
here before the report goes to DA or anyone else.

Checks that sit on disk are marked **SITS**.
Algebra that the report used, now written with the \(\nu\) kept,
is marked **LOCKED**.
Claims whose source files are not on this tree are marked
**NOT ON DISK** and are **not proved internally**.
Do not promote a **NOT ON DISK** line by rewriting it as a theorem.

---

## Checks that pass

### The clock — SITS

This book already has

\[
\Lambda'=\frac{2}{X}(T_c-\nu D_s).
\]

Dividing by \(\Lambda=Y/X\) gives exactly

\[
(\log\Lambda)'=\frac{2}{Y}(T_c-\nu D_s).
\]

Page: [`CENTERED-EQUATION.md`](CENTERED-EQUATION.md).
This is the identity, not Young and not Need★.

### A8-R criticality — SCALING SITS; construction NOT ON DISK

Homogeneity already inventoried
([`CENTERED-DRIFT-INVENTORY.md`](CENTERED-DRIFT-INVENTORY.md)):

\[
T_c(au)=a^3 T_c(u),\qquad D_s(au)=a^2 D_s(u).
\]

Under the reported profile \(u=a\nu t^{-2}U_t\),

\[
T_c\sim a^3\nu^3 t^{-6}\,T_c(U_t),
\qquad
\nu D_s\sim a^2\nu^3 t^{-4}\,D_s(U_t),
\]

so

\[
\frac{T_c}{\nu D_s}
=
a\,t^{-2}\,\frac{T_c}{D_s}(U_t).
\]

If \(T_c/D_s\sim C t^2\) holds on the profile, the ratio is
\(\sim aC\), order one. That arithmetic sits. The leading
coefficient is still unproved, as the report says.

The A8-R construction file itself is **not on this tree**.
The scaling check is not a substitute for that file.

### Separated \(K,K,L\) gain — REPORTED; regrouping file NOT ON DISK

A gain of \(L/K\) after full regrouping does not contradict the
23 Sep findings. The \(2^{i/2}\) bound traced earlier was derived
before centering, so the fiber/commutator gain was marked as not
yet spent. The reported \(L/K\) gain is that unspent piece.

Until the regrouping file is on disk, the board **cannot** list
this as proved internally. The fiber verdict for separated scales
stays **NEUTRAL**. If the file arrives and checks, that verdict
moves to **GAIN** with \(e=-1\). Do not move it on a report
sentence.

The comparable \(K,K,K\) channel stays the open one either way.

### The rest — FITS THE RECORD; none reopens a failed route

- Phase-only sign reversal sits on the six-mode evaluator
  ([`CENTERED-DRIFT-TRIAD-SPLIT.md`](CENTERED-DRIFT-TRIAD-SPLIT.md)):
  aligned closer \(\max T_c=16/5\), \(\min T_c=-16/5\). Sign is phase.
- \(T_c=-\langle F,g\rangle\) is already the inventory identity
  \(T_c=-\langle B(u,u),A(A-\Lambda)u\rangle\). That is an
  alignment question. It is not a new estimate.
- Reusing a quartic term as a rotation diagnostic fits that
  alignment reading. The named 54/46 quartic test file is
  **not on this tree** and is not invented.

None of these reopens unrestricted Lemma★, charge-only coercivity,
or any other killed route.

---

## Fix before sharing: section 5 was missing a factor of \(\nu\)

The stated local envelope is

\[
\alpha\chi\kappa^{3/2}X D_s^{1/2}.
\]

Young / AM–GM with the viscous slot gives

\[
\alpha\chi\kappa^{3/2}X D_s^{1/2}
\le
\tfrac12\nu D_s
+
\frac{\alpha^2\chi^2\kappa^3 X^2}{2\nu}.
\]

Dividing the remainder by \(Y=\kappa^2 X\) leaves

\[
\frac{\alpha^2\chi^2\kappa X}{2\nu}.
\]

Constants do not change integrability. The occupation condition
must therefore read

\[
\int\frac{\alpha^2\chi^2\kappa X}{\nu}\,dt<\infty,
\]

unless \(\nu=1\) is being assumed. With the \(\nu\) in place the
integrand is dimensionless in parabolic time, which is what makes
the critical-scaling claim even well-posed.

The \(K\)-candidate score sheet on this book used \(\theta=1/2\),
\(\nu=1\) as a **scoring convention**. That is not a license to
drop \(\nu\) from the occupation line.

This lock does **not** prove the local envelope, and it does
**not** prove that occupation holds. It only restores the missing
factor. Machine:
`scripts/da_gate_young_occupation_nu.py`.

---

## Two sourcing gaps — board cannot list either as proved internally

| Claim in the report | Named source | On this tree? | Board |
|---|---|---|---|
| I3 weighted theorem recovered | `I3_WEIGHTED_TARGET_2026-09-20.md` | **No** | not proved internally |
| Separated \(K,K,L\) regrouping | the regrouping file | **No** | fiber stays **NEUTRAL** |

A nearby remote `origin/cursor/fourier-triangle-i3-88af` has a
weighted-incidence write-up marked CLAIMED, specialist pending.
That is **not** the named 20 Sep target file. It is not imported
and is not treated as an internal proof.

Until those files are dropped onto this disk, do not list either
claim as proved internally.

---

## Disk check — also missing, not invented

Searched this tree and the listed sibling remotes. None of the
following is here:

| Asked-for file | Status |
|---|---|
| `I3_WEIGHTED_TARGET_2026-09-20.md` | **absent** |
| \(K,K,L\) regrouping file | **absent** |
| A8-R construction | **absent** |
| cube-field run | **absent** |
| 54/46 quartic test | **absent** |

What *is* on this tree and was used to check the report:

- Centered clock and inventory.
- Six-mode evaluator, note triad, separated triad, \(v_n\).
- Locked SBP / \(\phi/d\) / low-tail / sign / \(S_{pq}\) packets.
- Homogeneity \(T_c\sim a^3\), \(D_s\sim a^2\).

A sibling remote `origin/cursor/narrow-danger-parameter-f37a`
has a 24 Sep Young / \(\nu\) algebra packet for a *different*
narrow-danger ratio. It is not imported. It is not an occupation
proof. It is noted only so the \(\nu\) factor is not treated as
new lore.

---

## Board after this filing

**CLOSED-INTERNAL / exact.** Unchanged: clock, \(D_s\ge 0\),
six-mode identities, \(S_{pq}\), frozen SBP, \(\phi/d\).

**LOCKED today.** Occupation integrand keeps \(\nu\).
A8-R scaling arithmetic (not the construction).

**NOT PROVED INTERNALLY.** I3 weighted theorem.
Separated \(K,K,L\) gain (fiber stays NEUTRAL).
A8-R construction and leading coefficient.
Cube-field run. 54/46 quartic test.

**OPEN, unchanged.** Comparable \(K,K,K\).
DA-NS-2. Arithmetic sign realizability (armed, not run).
Low-tail capacity \(+\) charge \(+\) epoch motion.
First missing implication: comparable / near-shell signed
\(T_c\Rightarrow K\in L^1_{\mathrm{loc}}\) from admissible data.

**NEXT, not a run.** Q4-0 six-mode calibration **plan** only.
DA must approve before anything executes.

No new estimate is claimed. No continuation criterion.
**NS not solved.**
