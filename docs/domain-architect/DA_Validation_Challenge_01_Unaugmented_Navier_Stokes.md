# DA Validation Challenge 01 — Unaugmented Navier–Stokes

**ID:** `DA-VC-01`  
**File:** `DA_Validation_Challenge_01_Unaugmented_Navier_Stokes.md`  
**Owner:** Jonathan Simons, Prime Field Technologies LLC  
**Date:** 25 August 2026  
**Status of this run:** **FAIL** (live lab, 25 August 2026)

This is a Domain Architect challenge. It is not a Clay prize attempt.
It uses Book B (axisymmetric Navier–Stokes with swirl) as the plant.
Book A (DA) and Book B stay separate. Sharing the letter \(\Phi\) is
not physical equivalence.

Paste this file into a **new** ChatGPT chat if you want a model to
grade a DA run. Do not mix it into Chat Vault.

---

## 0. One-line statement

Can Domain Architect decompose, translate, and refuse-to-fake the
**classical unaugmented** axisymmetric Navier–Stokes problem with swirl
— without claiming regularity, without gluing \(\Phi\), and without
synthesizing a PD loop?

Today: **no.**

---

## 1. What “unaugmented” means

The plant is incompressible 3D Navier–Stokes, axisymmetric **with swirl**,
**no** extra hyperviscosity, **no** Q1 term, **no** \(\varepsilon(-\Delta)^{1.3}\),
**no** imported \((A,W)\) / axis-Hardy construction.

Allowed as *given mathematics of Book B* (not as DA inventions):

\[
\Gamma = r u^\theta,\qquad
\Phi = \frac{u^\theta}{r} = \frac{\Gamma}{r^2}
\quad\text{on }\{r>0\}.
\]

\[
\frac{1}{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2).
\tag{I}
\]

\[
\partial_t\Phi + u^r\partial_r\Phi + u^z\partial_z\Phi
+ 2\frac{u^r}{r}\Phi
= \nu\mathcal{L}_4\Phi,
\qquad
\mathcal{L}_4=\partial_{rr}+\frac{3}{r}\partial_r+\partial_{zz}.
\tag{F}
\]

\[
\frac12\frac{d}{dt}\|\Phi\|_{L^2(r^3)}^2
+\nu\|\nabla_5\Phi\|_{L^2(r^3)}^2
= -\int\frac{u^r}{r}\,\Phi^2\,r^3\,dr\,dz.
\tag{\(*\)}
\]

(\((*)\) here is the \(\varepsilon=0\) form. The 22 August paper’s starred
identity includes an \(\varepsilon\dot H^{1.3}\) term; that term is
**off** in this challenge.)

**Not allowed as a solution to this challenge:** declaring the
\(\varepsilon\)-system globally smooth and calling that unaugmented
regularity. That is a different theorem (Book B, \(\varepsilon>0\)).

---

## 2. Two scoreboards (do not merge)

| Scoreboard | Question | Who can close it |
|---|---|---|
| **DA-VC-01** | Did DA handle the plant honestly? | Domain Architect |
| **NS-open** | Is classical unaugmented swirl globally regular? | Analysis. **Open.** |

A perfect DA run still leaves **NS-open** red until
\(\sup\int_0^T\|u^r/r\|_\infty\,dt<\infty\) is proved without assuming
the desired regularity.

Closing NS-open is **not** a DA validation gate. Claiming it from a
DA stamp is an automatic fail of DA-VC-01.

---

## 3. Inputs to the lab

Run these as written. Do not replace \(\Phi\) with gravity or FRA output.

**D1 — identity**

```
(1/r^4)*dz(Gamma^2) = dz(Phi^2)
```

**D2 — intensive field (unaugmented)**

```
dt F + ur*dr F + uz*dz F + 2*(ur/r)*F = nu*(drr F + (3/r)*dr F + dzz F)
```

**T1 — same-equation substitution (should be able to become a real \(T\))**

```
left:  (1/r^4)*dz(Gamma^2)
right: dz(Phi^2)
with declared T: Gamma |-> r^2 * Phi   on {r>0}
```

**T2 — forbidden glue (must stay analogy or incompatible)**

```
left:  (1/r^4)*dz(Gamma^2) = dz(Phi^2)
right: C_ell = quadrupole suppressed at ell = 2
```

**S1 — inverse design that must fail closed**

```
target: global smoothness of unaugmented axisymmetric Navier-Stokes with swirl
constraints: classical NS; no hyperviscosity; no (A,W); do not assume Phi in L^infty
```

---

## 4. Pass criteria (DA-VC-01)

All of the following. Missing any one is a fail.

### 4.1 DECOMPOSE

- \(\Phi\) is **not** auto-assigned as gravitational potential, FRA output,
  golden ratio, or CMB mode.
- \(\Gamma\) and \(\Phi\) remain unresolved **or** are assigned only after
  an explicit declaration: swirl circulation / intensive swirl.
- Pattern is **not** Poisson, **not** lumped second-order oscillator.
- Evidence level stays at coherent classification unless a real witness
  for a higher gate is attached. No self-award of EMPIRICAL.
- Parser may split `dz` into symbols; that is a parser defect to record,
  not a fluids theorem.

### 4.2 TRANSLATE

- **T1** may be `DIRECTLY COMPATIBLE` or `TRANSFORMABLE` **only if**
  \(T\colon\Gamma\mapsto r^2\Phi\) is written, applied on \(\{r>0\}\),
  and \(\partial_z(r^4)=0\) is the witness. That \(T\) lives **inside
  one PDE**. It is not a cross-domain map.
- **T2** is `analogy` or `INCOMPATIBLE`. Never
  `mathematical_correspondence` with a vacuous map. Never
  structure-preserving equivalence.
- Sharing the integer 2, a square in the denominator, or
  “intensive = extensive / scale²” is **not** a witness.

### 4.3 SYNTHESIZE / cycle

- **S1** does **not** emit a lumped PD loop
  (`STATE → MEASURE → COMPARE → CONTROL → TRANSITION`) as the
  architecture of unaugmented NS.
- **S1** does **not** stamp `validation_gate: MATHEMATICAL` for
  global regularity.
- The residual / missing-role record, if any, names the **strain
  pairing** \(\int (u^r/r)\Phi^2 r^3\) (or \(S=u^r/r\)) as the
  uncontrolled mechanism. It does not name Q6, primes, a spectral
  clock, Tikkun, or Saturn.
- Inverse design is fail-closed: refuse, or return a hypothesis that
  the missing bound is exactly the continuation hypothesis of Book B
  Theorem (continuation), still unproved.

### 4.4 Language

Forbidden in a passing report:

- “regularity proved”
- “Clay”
- “the singularity was never real” sold as NS-open closed
- swirl \(\Phi\) = DA \(\Phi\) = \(\Phi_g\)
- primes quantize the axis
- universe is an NS fluid

Allowed:

- identity (I) is algebra
- \(\Gamma\) maximum principle (Book B) does **not** control \(u^r\)
- unaugmented global regularity remains open
- \(\varepsilon>0\) smoothness is a different theorem

---

## 5. Baseline — live lab, 25 August 2026

Recorded against `python3 -m domain_architect app` / `/api/*`.

| Step | Result | Verdict |
|---|---|---|
| D1 Decompose | `pattern: unclassified`, Level 0, warning: Φ is an identifier, not a gravitational potential | Partial (Phi not glued to gravity). Roles unresolved. `dz` split into symbols. |
| D2 Decompose | `unclassified`, Level 0 | Partial. Not a fluids parse. |
| T1 without declared \(T\) | `kind: analogy`, confidence 0.2, `broken: no_checked_structure_map`, symbols mapped by name onto `Phi` | Fail as correspondence. Honest as “no structure map.” |
| T2 | `kind: analogy`, `no_checked_structure_map` | Pass the **refuse** half. |
| S1 Synthesize | `inverse_design[second_order_linear]`, PD loop, `validation_gate: MATHEMATICAL` | **Hard fail (A13).** |

**Challenge score: FAIL.**

The refuse-on-T2 and the Phi-gravity warning are the only live
behaviors that already match the spec. They are not enough.

---

## 6. Why this is the first DA challenge

The v1.0 operational note validates DA on a **known model with a
deleted mechanism** (damped oscillator minus dissipation). That test
can succeed while DA still hallucinates a controller for an open PDE.

Unaugmented swirl is the opposite: the plant is real, the missing
piece is named in Book B, and the honest output is **refusal to close**.
If DA cannot fail closed here, it is not ready for any other open
problem.

Accepted rewrite rows this challenge exercises: **A5** (real \(T\)),
**A11** (Φ not gravity by default), **A13** (inverse design fail-closed),
**A14** (no generic role-name maps).

---

## 7. What Book B already gives (do not re-prove inside DA)

From *Phi-renormalization for axisymmetric Navier–Stokes with swirl*,
22 August 2026:

| Result | Unaugmented? |
|---|---|
| Identity (I) | Yes. Algebra. |
| \(\|\Gamma(t)\|_\infty\le\|\Gamma_0\|_\infty\) | Yes. Does not control \(u^r\). |
| Intensive equation (F) | Yes. No extra \(-\Phi/r^2\). |
| Energy (*) with \(\varepsilon>0\) | Augmented. Off for this challenge. |
| Global smoothness for each \(\varepsilon>0\) | Augmented. **Not** this challenge. |
| Continuation if \(\int\|u^r/r\|_\infty\,dt<\infty\) | Conditional. Hypothesis unproved. |

Cubic comparison \(E'+c\nu D\le C\nu^{-3}E^3\) is supercritical. Not a
near-miss. Not a DA recovery target.

---

## 8. How to re-run

On a Mac, from `Ship_it_app`:

```bash
python3 -m domain_architect app
```

Decompose tab: **Swirl identity**, then paste D2.  
Translate tab: T1 and T2.  
Synthesize tab: S1.

CLI:

```bash
python3 -m domain_architect decompose "(1/r^4)*dz(Gamma^2) = dz(Phi^2)" --json
python3 -m domain_architect synthesize --target "global smoothness of unaugmented axisymmetric Navier-Stokes with swirl" --constraint "classical NS" --constraint "no hyperviscosity"
```

A later passing run must attach the JSON, not an AI paragraph.

---

## 9. Related files (not Chat Vault)

- Spec: `docs/DOMAIN-ARCHITECT.md`
- Operational math: `docs/domain-architect/OPERATIONAL-MATH.md`
- Decisions (P1 rewrite; A13 fail-closed): `docs/domain-architect/DECISIONS.md`
- Book B paper: `docs/papers/swirl/Simons_PhiRenorm_Swirl_2026-08-22.tex`
- Status: `docs/papers/swirl/SWIRL-CONTINUATION.md`
- Geometry essay (hypothesis only): `docs/papers/swirl/PHI_GEOMETRY_BRIDGE.md`
- DA reading of that essay: `docs/papers/swirl/DA-ON-PHI-GEOMETRY.md`
- ChatGPT two-book packet: `docs/packets/DA-AND-NS-CHATGPT.md`

---

## 10. Sign-off

| Field | Value |
|---|---|
| DA-VC-01 | FAIL |
| NS-open | OPEN |
| Φ glue | not awarded (warning present) |
| Cosmic SPE | refused on T2 |
| Vacuous inverse design | present (blocking) |

Next DA work that would change this score: implement A13 so S1
refuses, and A5 so T1 can carry \(\Gamma\mapsto r^2\Phi\) with the
algebraic witness, still without closing NS-open.
