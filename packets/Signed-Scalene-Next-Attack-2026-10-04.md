# Signed Scalene Next Attack — 4 October 2026

Desk twin: [`docs/SIGNED-SCALENE-NEXT-ATTACK.md`](../docs/SIGNED-SCALENE-NEXT-ATTACK.md).

**Packaging + precise status. Not a proof of (17).
Not a close. NS not solved. Not Clay. No RH.**

Jonathan agreed to move ahead on the path:
return priority to the original signed scalene
budget / criterion (17) — not another energy-only
\(S^{(3)}\) bound. L3-5 energy-only strengthening
was falsified by the exact shear obstruction
(PR #159 / `docs/L3-5-Exact-Shear-Obstruction-2026-10-03.md`).
L3-5 as quantified in PR #153 remains OPEN.
Repeated-radius, (17), and global regularity are
not refuted.

Sources on this branch (cherry-picked; not full
PR merges; no claim-ledger / aerostat):

| Source | Objects |
|---|---|
| PR #153 head `ce8b1ee5…` | `FOURIER-TRIANGLE.md`, `L3-BUDGET-GATES.md`, `SIGNED-ASSEMBLY-GATE.md`, dated L3 / Fourier packets |
| PR #159 | Exact shear obstruction note + desk pointer + packet |

---

## 1. STATUS board

| Object | Status | Quantifiers / notes |
|---|---|---|
| Triad geometry (1)–(7); signed transfer (5); block ODE (14); centered clock (18) | **PROVED** | EXACT identities on \(\mathbb{T}^3\), unaugmented NSE. Keep hypotheses. |
| Exact-sphere (8)–(9); repeated-radius \(\lvert\mathcal T_{\mathrm{rep}}\rvert\le(\sqrt3/2)X\sqrt Y\) | **CLAIMED / seated** | Working analytic estimates. Not global regularity. |
| Fixed-low + repeated-radius complement \(C\); Young allocation; conditional \(X\) bound (16) given \(S\) | **PROVED** (conditional algebra) | Bound on \(X_N(t)\) once \(\mathcal S_{K,N}(T)\) is controlled. |
| (L3-1): \(\lvert\langle B(v,v),Av\rangle\rvert\le C_S\lVert v\rVert_3 Y\) | **PROVED** | Classical; cutoff-uniform. |
| (L3-4): \(S\le C_S S^{(3)}+\mathrm{controlled}\) | **PROVED** | **One-way only.** |
| (L3-5) fixed-datum high-mode \(L^3\) budget | **OPEN** | \(\forall u_0,\nu\ \exists K(u_0,\nu)\ \forall T:\ \sup_N S^{(3)}_{K,N}(T)<\infty\). Not refuted by shears. |
| **Criterion (17)** signed scalene budget | **OPEN — PRIORITY** | Same quantifier shape as (L3-5), different integrand. |
| Two-shell complete signed assembly \(\mathcal T=(b-a)(j_{b\leftarrow aa}-j_{a\leftarrow bb})\) | **Spatial test survives** | No occupancy. Full write [`DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md`](../docs/DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md) |
| Frozen \(K\) from initial \(\dot H^{1/2}\) tail | **Written** | \(K=\min\{n\ge1:C_0\|P_{>n}u_0\|_{\dot H^{1/2}}\le c\nu/2\}\). Uniform in \(N\) at \(t=0\) only. |
| Regenerated all-high scalene in time | **Local jet written / (17) OPEN** | \(K=2\) datum: \(\mathcal T_{\mathrm{sc}}(h_2)=(15084/1625)t^6+O(t^7)\); orders \(\le t^5\) vanish; \(\nu\)-independent; same for \(N\ge 5\); below \(\nu Y/4\) initially. Blocks \((5,8,25)\), \((5,10,25)\). [`ALL-HIGH-T6-K2-DATUM.md`](../docs/ALL-HIGH-T6-K2-DATUM.md) |
| Universal energy-only \(F(E_0,\nu,K,T)\) bounding \(S^{(3)}\) for all smooth data of energy \(E_0\) | **KILLED** | Exact shear family, 3 Oct 2026. |
| Reverse comparison \(S^{(3)}\le C\,S+F(E_0,\nu,K,T)\) | **KILLED** | Same family: \(S=0\), \(S^{(3)}\) arbitrarily large. |
| Unrestricted \(\sup\mathcal R_\star<\infty\); charge-only close; Theorem H as NS close | **KILLED** | Prior desks; do not reopen here. |
| Global regularity of 3D NSE / Clay Millennium | **NOT CLAIMED** | Even a proof of (17) would still need the standard continuation + Galerkin steps; none of that is asserted here. |
| Riemann Hypothesis | **OUT OF SCOPE** | Explicit non-goal. |

---

## 2. Precise statement of (17) as it exists in the vault

Conventions (normalized torus
\(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\)):
\(A=-P\Delta\), \(X=\lvert A^{1/2}u\rvert_2^2\),
\(Y=\lvert Au\rvert_2^2\), Galerkin field \(u_N\),
high-pass \(h_{K,N}=P_{\lvert k\rvert>K}u_N\).

From `docs/FOURIER-TRIANGLE.md` §11:

\[
\mathcal S_{K,N}(T)
=\int_0^T
\frac{\bigl[\mathcal T_{\mathrm{sc}}(h_{K,N})-\nu Y_N/4\bigr]_+}{X_N}\,dt.
\tag{15}
\]

Here \(\mathcal T_{\mathrm{sc}}\) sums complete triads
with **three distinct exact radii**. The positive
part is taken after that sum and the specified
viscosity subtraction. \(X_N,Y_N\) are moments of
the **full** field; \(h\) is not autonomous. On the
zero trajectory the integrand is defined as zero.

The already controlled complement
\(C=\mathcal T(u_N)-\mathcal T_{\mathrm{sc}}(h)\)
obeys the seated fixed-low + repeated-radius estimate
leading to the conditional bound

\[
X_N(t)
\le X_N(0)\exp\Biggl[
\frac{6C_K\sqrt{E_0}}{\nu}(1-e^{-\nu T})
+\frac{E_0}{4\nu^2}
+2\mathcal S_{K,N}(T)
\Biggr],
\quad 0\le t\le T.
\tag{16}
\]

The missing theorem is

\[
\boxed{
\forall u_0\in C^\infty_{\mathrm{div}},\
\forall\nu>0,\quad
\exists K=K(u_0,\nu)<\infty:\quad
\forall T<\infty,\quad
\sup_N\mathcal S_{K,N}(T)<\infty.
}
\tag{17}
\]

**Quantifiers (read carefully):**

- **Datum-sensitive:** \(K\) may depend on the fixed
  smooth initial datum \(u_0\) and on \(\nu\). The
  finite bound on \(\sup_N S\) may depend on
  \(u_0,\nu,T\).
- **Uniform in the Galerkin cutoff:** for that fixed
  \(K\), the bound must be independent of \(N\).
- **Not energy-only universal:** a single
  \(F(E_0,\nu,K,T)\) for all data of energy \(E_0\)
  is a stronger claim; for the \(L^3\) rewrite it is
  already **false** (shear obstruction). Do not
  smuggle that strengthening back into (17).
- **No a-priori smoothness:** the proof of (17) must
  not assume the desired uniform \(H^1\) / ESS bound
  it is meant to produce through (16).

If (17) holds, (16) gives uniform \(H^1\) control,
then standard strong-solution continuation and
Galerkin-limit steps apply. **None of that chain
is claimed proved here.**

Relation to (L3-5): `L3-BUDGET-GATES.md` derives
\(S\le C_S S^{(3)}+\mathrm{controlled}\) and names
(L3-5) as an \(L^3\) form that would imply (17).
That comparison is **one-way**. Criterion-level
equivalence through regularity (if either holds,
smoothness follows, hence both budgets stay finite)
is qualitative, not an algebraic interchange of
integrands. Priority returns to **(17)** directly.

---

## 3. Why shears are a rejection test the signed route already passes

Exact family (`L3-5-Exact-Shear-Obstruction-2026-10-03.md` §2):

\[
u_{m,L}(x,y,z,t)
=\bigl(\operatorname{Re} g_{m,L}(y,t),\;0,\;\operatorname{Im} g_{m,L}(y,t)\bigr),
\]

with \((u\cdot\nabla)u=0\) identically, heat evolution
in \(y\), and every ordered Fourier interaction factor
\(q\cdot u_p=0\). Consequently every transfer block
vanishes:

\[
\mathcal T_{\mathrm{sc}}(h)=\mathcal T_{\mathrm{rep}}(h)=\mathcal T(u)=0,
\qquad
\mathcal S_{K,N}(T)=0.
\]

At the same time, for fixed \(E_0=a^2\), \(\nu\), \(K\), \(T\),
growing occupancy makes \(S^{(3)}_{K,N}(T)\) arbitrarily
large. Therefore:

1. Any proposed **energy-only** bound on \(S^{(3)}\)
   (or reverse \(S^{(3)}\lesssim S+F(E_0,\nu,\ldots)\))
   fails on an explicit smooth NSE family — **KILLED**.
2. The **signed** integrand already records zero
   nonlinear production on those same trajectories —
   the rejection test is passed, not failed.
3. (17) and fixed-datum (L3-5) are **not** refuted:
   each shear datum has finite individual budgets;
   choosing \(K\) past the support makes both budgets
   identically zero.

**Corollary (restatement, not new analysis).**
If \(B(u,u)=0\) on a time interval, then
\(\mathcal T_{\mathrm{sc}}=\mathcal T=0\) and the
integrand of (15) vanishes there. Parallel shears
are the explicit infinite-dimensional family realizing
this. Use them as a mandatory filter on any future
replacement budget: the replacement must vanish
(or stay controlled) when nonlinear production vanishes.

---

## 4. Ordered next gates

Attack in this order. Do not skip to Gronwall.
Do not rename the positive remainder and call it done.

### Gate 0 — Freeze the rejection filter (**PROVED**)

**Statement.** Any proposed universal / energy-only
strengthening of an \(L^3\) (or other unsigned) budget
that can charge the shear family while signed
production is zero is rejected without further work.

**Quantifiers.** Universal in data at fixed
\((E_0,\nu,K,T)\): **forbidden** as a target.
Datum-sensitive (17): **allowed** as a target.

**Status.** Done by PR #159. Do not reopen.

### Gate 1 — Keep the seated complement → (16) (**PROVED**, conditional)

**Statement.** With
\(C=\mathcal T(u_N)-\mathcal T_{\mathrm{sc}}(h_{K,N})\)
controlled by fixed-low + repeated-radius + Young,
the exponential bound (16) holds whenever
\(\mathcal S_{K,N}(T)\) is finite.

**Quantifiers.** For each fixed \(K<\infty\), each
Galerkin \(N\), each \(T<\infty\). Constants depend on
\(\nu,E_0,K\) as written in the vault.

**Status.** Seated on the Fourier-triangle desk.
Not the blank. Do not “re-prove” (16) as the main
attack; cite it.

### Gate 2 — Signed assembly of all-high scalene transfer (**OPEN** in time; two-shell spatial instance **survives**)

**Statement (snapshot form).** Control

\[
\bigl[\mathcal T_{\mathrm{sc}}(h_{K,N})-\nu Y_N/4\bigr]_+
\]

without replacing the assembled imaginary products by
\(\lvert\widehat B\rvert\) early, and without assuming
a uniform bound on \(X_N\) or \(\lVert u\rVert_{L^\infty_t L^3_x}\).

**Inputs allowed.** Exact triad geometry (1)–(7);
polarization / phase structure; equal-length and
repeated-radius cancellations already seated;
divergence-free constraints.

**Inputs forbidden as hypotheses.** ESS-class
smallness; the conclusion of (16); energy-only
universal constants depending only on
\((E_0,\nu)\).

**Quantifiers.** Prefer a **datum-sensitive**
estimate (constants may depend on \(u_0\) through
its smooth Fourier profile and on \(K(u_0,\nu)\)).
A universal energy-only snapshot bound is the wrong
strength (shear filter).

**Relation to Signed Assembly Gate.**
`SIGNED-ASSEMBLY-GATE.md` names the assembly blank
before old Gate 5 / \(T_c\). It is **not** a
substitute for (17). Gate 2 here is the scalene /
\(\mathcal T_{\mathrm{sc}}\) instance of that blank on
the high-pass field.

**6 Oct 2026 update.** Two-shell **spatial** complete
assembly
\(\mathcal T=(b-a)(j_{b\leftarrow aa}-j_{a\leftarrow bb})\)
survives with no occupancy factor (receiver
compensation and flat-triangle cancellation visible).
That does **not** close all-high scalene in time.
See [`DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md`](../docs/DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md).

### Gate 3 — Regenerative forcing along the NSE (**OPEN — now the plow**)

**Statement.** For distinct-radius blocks, the vault
has

\[
\dot{\mathcal T}_{abc}+\nu(a+b+c)\mathcal T_{abc}
=\mathcal Q_{abc,N},
\tag{14}
\]

with quartic \(\mathcal Q\) not confined to the
displayed triangle or to the high-pass. Bound the
contribution of \(\mathcal Q\) to the integrated
normalized positive budget without a Duhamel
denominator fantasy that ignores regeneration.

**Quantifiers.** Along actual Galerkin / NSE
trajectories; uniform in \(N\) after \(K=K(u_0,\nu)\)
is fixed. Datum-sensitive constants allowed.

**Status.** Local all-high jet on the \(K=2\) datum
**written** (6 Oct):
\(\mathcal T_{\mathrm{sc}}(h_2)=(15084/1625)t^6+O(t^7)\),
orders \(\le t^5\) vanish, coefficient independent of
\(\nu\), blocks \((5,8,25)\) and \((5,10,25)\).
Full-field \(\mathcal T_{\mathrm{sc}}'(0)=28\) remains a
separate witness. **Plow now:** whether
\([\mathcal T_{\mathrm{sc}}-\nu Y/4]_+\) is positive, and
general (17). Not \(\sup_N\) control yet.

### Gate 4 — High-pass consistency (**OPEN**, bookkeeping)

**Statement.** \(\mathcal T_{\mathrm{sc}}\) is evaluated
on \(h_{K,N}\), while \(X_N,Y_N\) are full-field
moments and \(h\) is not autonomous. Show that
low/high cross terms created by projecting before
forming scalene sums are either absorbed into the
seated complement \(C\) or controlled by the same
\(K(u_0,\nu)\) choice (initial high-tail smallness /
spectral gap of the smooth datum).

**Quantifiers.** Datum-sensitive \(K(u_0,\nu)\).
This is where initial high-frequency concentration
of a **fixed** smooth \(u_0\) is allowed to enter —
explicitly — without pretending the constant depends
only on \(E_0\).

**6 Oct recipe (written, not a time bound):**

\[
K=\min\{n\ge1:C_0\|P_{>n}u_0\|_{\dot H^{1/2}}\le c\nu/2\}.
\]

Uniform in \(N\) at \(t=0\). Later high modes are
Gate 3.

### Gate 5 — Integrate to criterion (17) (**OPEN** — main target)

**Statement.** Exactly (17) as boxed above:
for each smooth divergence-free \(u_0\) and each
\(\nu>0\), produce \(K(u_0,\nu)<\infty\) such that
for every finite \(T\),

\[
\sup_N\mathcal S_{K,N}(T)<\infty.
\]

**Depends on.** Gates 2–4 (assembly, regeneration,
high-pass bookkeeping) plus Gate 1 (seated).

**Does not depend on.** A reverse bound through
\(S^{(3)}\); RH; Clay rhetoric.

### Gate 6 — Continuation after uniform \(X\) (**STANDARD**, not the blank)

**Statement.** From uniform \(X_N\) via (16), run the
ordinary strong-solution continuation and
Galerkin-limit argument on \(\mathbb{T}^3\).

**Status.** Classical once Gate 5 is won. Do not
package Gate 6 as the research contribution.
Do not claim Gate 6 here.

---

## 5. What was tightened vs plan-only

| Item | Advanced? |
|---|---|
| New estimate proving any case of (17) | **No** |
| New estimate on \(\mathcal Q_{abc}\) or assembled \(\mathcal T_{\mathrm{sc}}\) | **No** |
| Restatement of (17) with explicit quantifiers and STATUS board | **Yes** (packaging) |
| Shear vanishing corollary as mandatory rejection filter for future budgets | **Yes** (restatement of PR #159 + definitions; not new analysis) |
| Deprioritization of (L3-5) / energy-only \(S^{(3)}\) relative to (17) | **Yes** (desk decision; matches obstruction Consequence) |
| Lemma A / first-variation sign gate | **Unaltered** — not touched |
| Two-shell complete signed assembly, no occupancy | **Yes** (6 Oct) — spatial test survives; not (17) |
| Regenerated all-high scalene in time | **No** — named as the remaining blank |

**Verdict as of 4 Oct:** plan-only on the mathematical blank.

**Verdict as of 6 Oct:** two-shell **spatial** signed
assembly is no longer the thing to re-prove (occupancy
not forced). The remaining blank is regenerated
all-high scalene in time (Gate 3), toward (17).
No fake proof of (17). Shear filter still applies.

---

## 6. Explicit non-goals

1. **No** energy-only universal
   \(F(E_0,\nu,K,T)\) on \(S^{(3)}\).
2. **No** reverse inequality
   \(S^{(3)}\le C S+F(E_0,\nu,\ldots)\).
3. **No** Riemann Hypothesis content on this desk.
4. **No** Clay / “Navier–Stokes solved” claim.
5. **No** mixing of claim-ledger or aerostat packs
   into this branch.
6. **No** revival of unrestricted \(\star\),
   charge-only close, or Theorem H as a close.
7. **No** cashing fixed-data \(S(1)\) samples as
   \(\sup_N\mathcal S_{K,N}(T)<\infty\).

---

## 7. Suggested immediate work items (operators)

1. Do not restart occupancy counting on two shells.
   The spatial signed assembly already survives.
2. Enumerate which parts of \(\mathcal Q_{abc,N}\)
   in (14) are high–high–high versus mixed with
   modes \(\le K\), using the frozen cutoff
   \(K=\min\{n\ge1:C_0\|P_{>n}u_0\|_{\dot H^{1/2}}\le c\nu/2\}\).
3. Control regenerated all-high
   \(\mathcal T_{\mathrm{sc}}(h_{K,N}(t))\) without
   assuming (16). The \(K=2\to\) radius-\(5\) datum
   is the rejection test for “initial tail small
   \(\Rightarrow\) later tail small.”
4. Keep the shear filter on every replacement
   integrand. Do not open a new \(L^3\) energy-only
   program.

---

## Lock

Priority: signed scalene criterion **(17)**.
Energy-only \(S^{(3)}\) reverse: **KILLED**.
Two-shell spatial signed assembly: **survives**.
All-high \(t^6\) jet on \(K=2\) datum: **written**;
integrated budget / (17): **OPEN — plow**.
Fixed-datum (L3-5): **OPEN**, not priority.
Repeated-radius / (16) complement: **seated**.
Global regularity: **not claimed**.
NS not solved. Not Clay. No RH.
