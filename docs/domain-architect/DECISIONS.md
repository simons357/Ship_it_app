# Domain Architect — decisions to mark

**For:** Jonathan Simons  
**Date:** 2026-08-24  
**Branch:** `cursor/sfe-rewrite-domain-architect-9d6b`  
**Draft PR:** https://github.com/simons357/Ship_it_app/pull/31  
**Canonical paper:** [`docs/DOMAIN-ARCHITECT.md`](../DOMAIN-ARCHITECT.md)  
**Auditor brief (do not treat as already decided):** [`GROK-SPEC-AUDIT.md`](GROK-SPEC-AUDIT.md)  
**Earlier brief (stale; dump claimed to implement it):** [`ARCHITECTURE-AUDIT.md`](ARCHITECTURE-AUDIT.md)

This file is the human decision log. Nothing in it is implemented by being written here. An unmarked row is **not** an accept.

**Recorded 2026-08-24.** Jonathan Simons: `accept grok table`.

| ID | Recorded mark |
|---|---|
| **P1** | `ACCEPT rewrite` |
| **A1** | `AMEND` — isolate UI/CLI too; archive is not a product pane |
| **A2** | `REJECT as done` / `ACCEPT as still required` — prime is one optional selector |
| **A3** | `REJECT as done` — drop `valid_for_physical_prime_test` |
| **A4** | `AMEND` — real `run_cycle` state machine; named demos call it and are examples |
| **A5** | `REJECT dump T` / `ACCEPT requirement` — morphism + witness, or no `TRANSFORMABLE` |
| **A6** | `REJECT dump deletion` — restore unawardable `structure_preserving_equivalence` |
| **A7** | `REJECT as done` / still required — `StateSpace` / `Dynamics` / `OutcomeModel` |
| **A8** | `ACCEPT` no QStack/QNav modules; `AMEND` pluginize `classify.py` |
| **A9** | `ACCEPT` sentence; `REJECT` sufficiency — method-first reports |
| **A10** | `ACCEPT` — `m` is inertial parameter, not state transition |
| **A11** | `ACCEPT` — cut gravity / Einstein / `y=abx` from default decompose |
| **A12** | `ACCEPT` — empty default `KNOWN_UNITS` |
| **A13** | `ACCEPT` — inverse design fail-closed |
| **A14** | `ACCEPT` — no generic role-name maps |
| **A15** | `REJECT` folder-first rewrite |
| **A16** | `ACCEPT` — blocking rows decided; implement them; no extra features |

Implied by those rows and implemented with them: **C3, C7, C8, C17, C18, C19, C20**. Git **G1–G2** stay unmarked (G1 auditor rec: do not merge #31 as-is — still draft).

**Recorded 2026-08-24 (logo).** Jonathan Simons sent two 3D renders of the chrome open-A + rainbow triskelion (gold DOMAIN vs all-silver) and said he already had a slider program for the mark. **L1** official mark = those renders. **L2** wire through app/favicon/shortcut and put the manipulator in the desktop **Mark** tab. **L3** amended: that triskelion *is* the brand; still no primes / field-equation motifs.

Live software today (verified 2026-08-24 before this rewrite): local desktop app at `http://127.0.0.1:8765/`, CLI, 51 unit tests green. That package was a three-verb UI around Firestone analogy, equation-error OLS, RK4, saturated PD, FFT Poisson, and a three-pattern classifier. This rewrite implements the marked table.

---

## How to mark

Use one of:

| Mark | Meaning |
|---|---|
| `ACCEPT` | Do it as stated. |
| `AMEND: <text>` | Do it, with this change. The amendment is the spec. |
| `REJECT: <keep / do this instead>` | Do not do it. State what to keep or substitute. |
| `DEFER` | Not now. Allowed only on rows that are **not** blocking. |

Write the mark in **Your mark**. Leave **Your notes** blank unless you need a caveat.

You can also reply in chat with a compact dump, for example:

```
P1 ACCEPT rewrite
A1-A16 ACCEPT grok column
L1 AMEND: use my file (attached)
```

or one line: `accept grok table` which means **P1 = rewrite** and **A1–A16 = the Auditor rec column**.

---

## What is blocking

If **P1 = rewrite**, these rows must be marked before any core code change:

`A5`, `A10`, `A11`, `A12`, `A13`, `A14`

`DEFER` is not valid on those six if P1 is rewrite. That is the lesson of the last dump: pausing “until 1–6” and then doing wording compliance produced a worse `TRANSFORMABLE` stamp.

If **P1 = demo-only** or **P1 = freeze**, architecture rows may stay unmarked. Logo and git rows can still be marked.

---

## Shortcut sheet

Fill this first. Details for each ID are below.

| ID | Question (short) | Auditor rec | Blocking if rewrite? | Your mark | Your notes |
|---|---|---|---|---|---|
| **P1** | Fate of this branch: rewrite / demo-only / freeze | rewrite after this sheet | yes (this *is* the fork) | ACCEPT rewrite | |
| **P2** | Keep PR #31 draft until rewrite exists? | yes, keep draft | no | | |
| **P3** | Relationship to phone PR #30 | leave #30 alone; this sheet governs #31 | no | | |
| **L1** | Official mark | wait for your file or pick 1–5 | no | AMEND: chrome A + rainbow triskelion (gold / silver renders) | |
| **L2** | Wire chosen mark through app/favicon/shortcut? | yes, after L1 | no | ACCEPT — Mark studio in the desktop app | |
| **L3** | Forbid primes/harmonics/spirals/field-equation motifs? | yes | no | AMEND: official swirl is the brand; no primes / field equations | |
| **A1** | Isolate historical so app/cli cannot import SFE/HB | AMEND prior accept (isolate UI too) | no | | |
| **A2** | Generalize selectors; prime optional on a common interface | REJECT as done; ACCEPT as still required | no | | |
| **A3** | Drop `valid_for_physical_prime_test`; generalize index audit | REJECT as done | no | | |
| **A4** | Real cycle state machine **or** examples-only README | AMEND (pick one) | no | | |
| **A5** | `T` is a tested morphism **or** retire `TRANSFORMABLE` | REJECT dump T; ACCEPT the requirement | **yes** | | |
| **A6** | Restore `structure_preserving_equivalence` as unawardable kind | REJECT the dump deletion | no | | |
| **A7** | Extract UHF/DHFA/SFE *functions* as StateSpace / Dynamics / OutcomeModel | REJECT as done | no | | |
| **A8** | Do not create QStack/QNav modules; pluginize `classify.py` | ACCEPT names absent; AMEND: pluginize router | no | | |
| **A9** | README names Firestone/OLS/RK4/PD as standard methods used *by* DA | ACCEPT sentence; REJECT sufficiency | no | | |
| **A10** | Unlock `m = STATE_TRANSITION`; inertia ≠ state transition | ACCEPT | **yes** | | |
| **A11** | Cut gravity / Einstein / `y=abx` from default decompose | ACCEPT | **yes** | | |
| **A12** | Empty default `KNOWN_UNITS`; gravity units only in Poisson example | ACCEPT | **yes** | | |
| **A13** | Inverse design fail-closed unless target is a recognized object | ACCEPT | **yes** | | |
| **A14** | Generic translate must not emit role-name maps (`k→G`); INCOMPATIBLE / no-map | ACCEPT | **yes** | | |
| **A15** | Folder-first rewrite (`core/math/mechanisms/…`) | REJECT | no | | |
| **A16** | Pause *feature* work until A5 and A10–A14 are decided | ACCEPT | n/a (process) | | |
| **C1** | Recursive `SYSTEM→…→PARAMETER`; `m,c,k` are parameters, not dummy-free theater | ACCEPT paper tree | no | | |
| **C2** | Open role list vs closed `FunctionalRole` enum | ACCEPT open list | no | | |
| **C3** | First-order plants must not be branded `second_order_linear_ode` | ACCEPT | no | | |
| **C4** | Named invariants are `checked \| failed \| waived \| not_evaluated`, never author-supplied True | ACCEPT | no | | |
| **C5** | Residual / “missing role” search only if the role hypothesis is independent of the regressor library | ACCEPT | no | | |
| **C6** | `Provenance.original_domain` is a domain, not a symbol (`"R"`) | ACCEPT | no | | |
| **C7** | Default `/api/translate` must not fall back to Firestone | ACCEPT | no | | |
| **C8** | Archive pane: peer tab vs opt-in CLI only | Auditor: CLI only | no | | |
| **C9** | `EvidenceLevel` 3–6 / FRA subtypes live vs historical only | historical only | no | | |
| **C10** | Keep FRA compact grammar `Φ=ℱ(P,H,ψ,λ;E)` retired | ACCEPT retired | no | | |
| **C11** | Drag example: keep as dishonest demo, fix, or remove from product surface | remove from default product / examples-only with invented-surrogate label | no | | |
| **C12** | Empirical validation gate: stay unimplemented and never self-awarded, or wire `protocol.py` | never self-award; wire later | no | | |
| **C13** | Version string `1.1.0`: dump increment vs wait for a real capability bump | revert or freeze until rewrite | no | | |
| **C14** | Bond graphs / Firestone: admit DA is weaker until ports exist, or implement ports | admit weaker; do not claim a new architecture | no | | |
| **C15** | Closed HB ringdown experiment stays closed and off the DA import graph | ACCEPT | no | | |
| **C16** | Repo-root `hb_ringdown_test.py`: move under archive tests | ACCEPT | no | | |
| **C17** | `realization.py` as “the SFE function”: delete the file/comment; keep RK4 under dynamics | ACCEPT | no | | |
| **C18** | Wave classifier must not insert symbol `"D"` when `D` is absent | ACCEPT | no | | |
| **C19** | User reports must name the standard method first (OLS, RK4, PD, Firestone, FFT Poisson) | ACCEPT | no | | |
| **C20** | Identity `T` must not flip a matching pair to `INCOMPATIBLE` | ACCEPT (part of A5) | no | | |
| **U1** | Desktop app stays as the product surface during rewrite? | yes, but labels must match honesty | no | | |
| **U2** | macOS/Windows shortcut installers beyond Linux `.desktop` | when you need them on your machine | no | | |
| **G1** | Merge #31 to `main` in the current demo state? | no | no | | |
| **G2** | After rewrite: one PR or stacked PRs? | stacked: honesty/T first, then types, then selectors | no | | |

---

## P — Product fate

### P1. What is this branch for?

**Current.** Draft PR #31 = SFE/HB string dump + desktop app + brand explorations + two audits. App runs. Paper engine does not.

**Options.**

1. `rewrite` — implement the marked architecture on this branch. Demo UI may stay as the shell.
2. `demo-only` — freeze the math. Relabel README/UI as examples-only. Optional logo. No claim of Domain Architect v1.
3. `freeze` — stop work. Close or abandon #31. Paper remains the spec. App remains whatever is already on the branch.

**Auditor rec.** `rewrite` after this sheet is marked. Do not dump again.

**Your mark:**

**Your notes:**

### P2. PR #31 status until a real engine exists

**Current.** Draft. Title still says “SFE rewrite: Domain Architect is the live product.”

**Options.** Keep draft / mark ready / close / retitle to “demo lab + audit, not the engine.”

**Auditor rec.** Keep draft. Retitle if P1 is demo-only or freeze.

**Your mark:**

**Your notes:**

### P3. Phone PR #30 (`cursor/domain-architect-v1-f929`)

**Current.** Separate session, same GitHub account. This sheet does not automatically apply there.

**Options.** Leave #30 alone / close #30 as superseded by #31 / merge strategy you specify.

**Auditor rec.** Leave #30 alone unless you say otherwise. This file governs #31.

**Your mark:**

**Your notes:**

---

## L — Logo and brand

Five earlier spine/cyan presentations remain under `assets/brand/` as exploratory rasters. Existing `assets/shipit_final_*.png` and the UUID JPG are corrupted binaries; they are not usable marks.

### L1. Official Domain Architect mark

**Options.**

1. Square app icon — `assets/brand/da_app_icon.png` + `assets/brand/domain-architect.svg`
2. Wordmark lockup — `assets/brand/da_wordmark.png`
3. Monochrome stamp — `assets/brand/da_mono.png`
4. Micro-icon study — `assets/brand/da_favicon.png`
5. Identity sheet — `assets/brand/da_flat_vector.png`
6. Your file — attach PNG/SVG in chat
7. None yet — keep the vector glyph already in the desktop header; do not declare official

**Auditor rec.** Wait for you. Do not generate more marks.

**Your mark:** AMEND — official mark is the chrome open-A + rainbow triskelion from the two 3D renders (gold DOMAIN vs all-silver). Parametric SVG/canvas in `domain_architect/brand.py` and the desktop Mark tab. Factory files: `assets/brand/domain-architect-wordmark.svg`, `domain-architect-silver.svg`, live icon `assets/domain-architect.svg`. Retired spine glyph saved as `assets/brand/exploratory-spine.svg`.

**Your notes:** The attached pixels were not saved to disk; the studio reconstructs the geometry so sliders can retune it.

### L2. After L1, wire the mark through

App header (`/icon.svg`), favicon, Linux `.desktop` `Icon=`, optional PNG raster for OS launchers.

**Auditor rec.** Yes, after L1. Not a rewrite blocker.

**Your mark:** ACCEPT — header, favicon, shortcut icon, plus Mark studio (`/api/brand/apply`, Gold / All silver / App icon presets, sliders, color pickers, PNG download).

**Your notes:**

### L3. Brand constraints

Current brand README: no primes, harmonics, spirals, or field-equation motifs. Cyan node = translation interface, not a physical claim. Mark may imply D/A; it is not a letter monogram.

**Auditor rec.** Keep those constraints.

**Your mark:** AMEND — the official rainbow triskelion is the brand, not a physical or harmonic claim. Still forbid primes and field-equation motifs. The retired cyan-diamond spine is exploratory only.

**Your notes:**

---

## A — Reopened architecture table (Grok §12)

A prior human mark on 2026-08-23 accepted old items 1–6, 8, 9, 10. The dump then “implemented” several of them as comments, aliases, and loophole tests. **Those accepts are reopened.** Mark again.

### A1. Historical isolation includes product entry points

**Current.** `decompose.py` / `translate.py` / `synthesize.py` do not import `historical`. `app.py`, `cli.py`, and `registry.py` still do. Dump tests omit those files. Desktop Archive tab loads SFE IDs via `/api/archive`.

**Question.** Must `app` / `cli` / default registry be unable to import SFE, UHF, DHFA, or HB except behind an explicit `--archive` that lives outside the product import graph?

**Auditor rec.** **AMEND** the previous accept: isolation that omits the UI is theater.

**Your mark:**

**Your notes:**

### A2. Primes generalized, not deleted and not privileged

**Current.** `selectors.py` still uses prime count as default budget; conclusion text is always about prime. `FunctionalRole.SELECTION` is never assigned. Module is off the live decompose/translate/synthesize path.

**Question.** Is prime one optional `SelectionMechanism` among cutoff / random / energy / user predicate, on a common interface, used only when the role is selection?

**Auditor rec.** **REJECT as done. ACCEPT as still required.** Do not merely delete primes.

**Your mark:**

**Your notes:**

### A3. Index audit is invariance, not primality

**Current.** Field `valid_for_physical_prime_test` remains. Historical tests still assert it.

**Question.** Rename/generalize to “is this index invariant under the declared equivalence?” Primality is a predicate applied *after* invariance is yes.

**Auditor rec.** **REJECT as done.**

**Your mark:**

**Your notes:**

### A4. Cycle engine vs examples-only

**Current.** `cycle.run_cycle` is a callback stub (no compatibility step, no iterate). Named demos in `pipeline.py` build `CycleReport` by hand and **do not** call `run_cycle`. README still presents them as the Domain Architect cycle. `/api/inverse-cycle` is the stub’s only caller.

**Question.** Pick exactly one:

1. Make `run_cycle` the only way product demos run (real state machine, including COMPATIBILITY and ITERATE).
2. Admit v1 is examples-only. Demote `pipeline.py` to `examples/`. README must say so.

**Auditor rec.** **AMEND** — pick one; not both.

**Your mark:**

**Your notes:**

### A5. `T` is a tested morphism, or `TRANSFORMABLE` is retired

**Blocking if P1 = rewrite.**

**Current.** `Transformation.apply` remaps dict keys and cannot fail. Vacuous `T` (“magic”, dissipation vs forcing, unknown types) ⇒ `TRANSFORMABLE` + `mathematical_correspondence`. Matching pair with identity `T` ⇒ `INCOMPATIBLE`. Synthesis substitutes symbol strings; it does not apply `T` to an operator.

**Question.** Either:

- `TRANSFORMABLE` requires a morphism plus a witness (matching residual class, transfer-function poles, quadratic energy form, or an explicit waived-witness with reason), and `T(M_B)` must pass DIRECT tests against `M_A`, or
- the word `TRANSFORMABLE` is removed from live verdicts.

**Auditor rec.** **REJECT the dump’s “executable T.” ACCEPT the requirement.** This is the most dangerous live bug.

**Your mark:**

**Your notes:**

### A6. Third correspondence kind stays, and cannot be awarded

**Current.** Dump deleted `STRUCTURE_PRESERVING_EQUIVALENCE` from `CorrespondenceKind`. Paper §6–10 requires analogy / mathematical correspondence / structure-preserving equivalence.

**Question.** Restore the kind. Software must not award it until an intertwining / functor witness exists.

**Auditor rec.** **REJECT the dump deletion.**

**Your mark:**

**Your notes:**

### A7. Extract functions, not renamed equations

**Current.** No `StateSpace` type. `realize_second_order` is RK4 with an “SFE function” comment. `m` is still `STATE_TRANSITION`.

**Question.** UHF/DHFA/SFE names die. If a function exists in this tree, it becomes ordinary objects: `State` / `StateSpace` / `AdmissibleSet`, `Dynamics: (x,u,t)→ẋ`, `OutcomeModel: Architecture → y`. Never a renamed field equation. Never a wrapper file claiming extraction.

**Auditor rec.** **REJECT as done.** Still required.

**Your mark:**

**Your notes:**

### A8. QStack / QNav names vs the live router

**Current.** Neither module exists. `classify.py` + `audit_expression` already routes every parse into `{elliptic_poisson, hyperbolic_wave, second_order_linear_ode, unclassified}`.

**Question.** Do not create `qstack.py` or `qnav.py`. Demote the live router to a plugin registry with default `UNRESOLVED`. If QStack/QNav later appear from another app, audit them as code, do not assume a rename.

**Auditor rec.** **ACCEPT** (no modules). **AMEND:** pluginize `classify.py`.

**Your mark:**

**Your notes:**

### A9. Honesty about standard methods

**Current.** README has one honest sentence. Tests still treat demo success as DA success (`COMPUTATIONAL` on OLS and PD). Desktop copy still says “executable T.”

**Question.** User-facing reports must name the method first. Tests must not equate “ζ recovered” with “DA recovered a missing role” unless an independent role hypothesis existed.

**Auditor rec.** **ACCEPT the sentence. REJECT sufficiency.**

**Your mark:**

**Your notes:**

### A10. Unlock `m` as inertial parameter

**Blocking if P1 = rewrite.**

**Current.** `tests/test_domain_architect_v1.py::test_second_order_roles` requires `roles["m"] == STATE_TRANSITION`. The coefficient of `ẍ` is inertia. State transition is `ẋ = F(x,u,t)`.

**Question.** Change the test and the classifier.

**Auditor rec.** **ACCEPT.**

**Your mark:**

**Your notes:**

### A11. Default decompose is not a gravity/FRA lab

**Blocking if P1 = rewrite.**

**Current.** `audit_expression` (the desktop Decompose button) special-cases Poisson → FFT solver, Einstein-by-substring `"G"`/`"T"`/`"mu"`, linearized gravity, and `y=abx` with canned numbers.

**Question.** Those branches leave default decompose. They may live under `--example` / `examples/`.

**Auditor rec.** **ACCEPT.**

**Your mark:**

**Your notes:**

### A12. Empty default unit environment

**Blocking if P1 = rewrite.**

**Current.** `checks.KNOWN_UNITS` hardcodes `c` = L/T, `k`/`kappa` = 1/L, plus `G`, `Phi`, `rho`. On `m*xdd + c*xd + k*x = f`, damping `c` and stiffness `k` inherit light-speed and wavenumber.

**Question.** Default environment is empty. Units come from caller context. Gravity 7-tuples live only in the Poisson example.

**Auditor rec.** **ACCEPT.**

**Your mark:**

**Your notes:**

### A13. Inverse design fail-closed

**Blocking if P1 = rewrite.**

**Current.** `inverse_design_architecture("maximize profit", …)` emits the same PD loop as `"x=1"`. Constraints are not parsed. No `g_i(x)≤0` object.

**Question.** Synthesize refuses unless the target is a recognized state/objective object. `"maximize profit"` must not emit a controller.

**Auditor rec.** **ACCEPT.**

**Your mark:**

**Your notes:**

### A14. No generic role-name translation

**Blocking if P1 = rewrite.**

**Current.** Oscillator vs Poisson emits `{x:Φ, k:G, f:ρ}` at confidence 0.2 with no compatibility reports.

**Question.** Generic translate emits `INCOMPATIBLE` / no-map unless a registered, tested `T` exists. Role-name join is not a map.

**Auditor rec.** **ACCEPT.**

**Your mark:**

**Your notes:**

### A15. Folder-first rewrite

**Current.** Rival audit proposed `core/` `math/` `mechanisms/` `domains/`.

**Question.** Allow a folder move as the rewrite, or forbid it as a substitute for A5 and A10–A14?

**Auditor rec.** **REJECT.** DA should be a protocol (interfaces + cycle) plus registered methods. Verbs are not packages. A later layout change is allowed *after* the blocking rows exist as tests.

**Your mark:**

**Your notes:**

### A16. Pause features until blocking rows are decided

**Question.** No new product features (more demos, more domains, more UI) until A5 and A10–A14 are marked and, if P1 is rewrite, implemented.

**Auditor rec.** **ACCEPT.** Logo wiring is not a feature in this sense.

**Your mark:**

**Your notes:**

---

## C — Further architecture decisions (not in §12 as numbered rows)

These are load-bearing in the paper or in the live bugs. Mark them if P1 is rewrite. They may `DEFER` only if you explicitly accept the current bug remaining.

### C1. Decomposition tree and PARAMETER

Paper: recursive `SYSTEM → SUBSYSTEM → FUNCTIONAL ROLE → MECHANISM → OPERATOR → PARAMETER`.  
Dump celebrated `PARAMETER ∉ tree`. `m`, `c`, `k` *are* parameters stored as `MECHANISM`. Depth is a wrapper, not recursion over independently functioning parts.

**Auditor rec.** Implement the paper tree. Do not pad dummy nodes. Do not delete PARAMETER when a parameter exists. Recursion when a part itself decomposes.

**Your mark:**

**Your notes:**

### C2. Open role list

Paper: roles include selection, interaction, transport, feedback, dissipation, forcing, constraint, state transition, measurement; **list is deliberately open**; no predetermined role count.  
Code: closed `FunctionalRole` enum. New roles need a code change. That recreates a mandatory anatomy.

**Auditor rec.** Role is a hypothesis string (or registered name) plus type/domain/codomain/units. Enum may exist as a catalog of *known* names, not as the only assignment target.

**Your mark:**

**Your notes:**

### C3. First-order vs second-order pattern

**Current (executed).** `xd + a*x = u` and `c*xd + k*x = f` classify as `second_order_linear_ode` because `_looks_like_second_order_ode` is `max(derivative_order) >= 1`.

**Auditor rec.** Separate first-order and second-order plugins. Default `UNRESOLVED`.

**Your mark:**

**Your notes:**

### C4. Invariants are checks

`INVARIANT_KEYS` lists linearity, passivity, self-adjointness, causality, positivity, hyperbolic, elliptic, conservation. Nothing computes them. `shared_invariants={"linearity": True}` is passed in because the author already decided the pair is LTI. Firestone `broken` list is hardcoded before the pair is examined. `OPERATIONAL-MATH.md` claims passivity/quadratic energy; `translate.py` does not check passivity.

**Auditor rec.** Each named invariant is `checked | failed | waived | not_evaluated`. Author-supplied True is not a check.

**Your mark:**

**Your notes:**

### C5. Missing-role residual search

`classify_missing_mechanism` correlates `R` with `{1, x, ẋ}` and then “restricts” the operator class to the winner. The restriction **is** the classification. Library is three terms. Not SINDy, not DA.

**Auditor rec.** Role class supplied independently (architecture hypothesis → operator family → estimator). Unrestricted symbolic regression stays out of core.

**Your mark:**

**Your notes:**

### C6. Provenance domain

`Provenance.original_domain` is set to a symbol (`"R"`). Drag cycle ships `provenance=[]`.

**Auditor rec.** `original_domain` is a domain (mechanical, electrical, …). Empty provenance fails closed on synthesize. Drag must not ship empty provenance if it remains a product example.

**Your mark:**

**Your notes:**

### C7. Firestone as silent default

CLI and `/api/translate`: if the user omits `--example` and omits one side, mechanical–electrical runs anyway.

**Auditor rec.** No silent Firestone. Require two systems or an explicit `--example`.

**Your mark:**

**Your notes:**

### C8. Archive as a product pane

Desktop tab “Archive” is a peer of Decompose and surfaces `SFE-H001`.

**Auditor rec.** Opt-in CLI `--archive` only. Not a peer tab.

**Your mark:**

**Your notes:**

### C9. FRA ontology in live `schema.py`

Still imported by core: `ScaleResponseSubtype`, `PermissionSubtype`, `SOURCE_STATE_WARNING`, `REPRESENTATION_NOT_DERIVATION`, `EvidenceLevel` through “replicated general physical theory,” `FORBIDDEN_CLAIM_PHRASES` whose threat model is still “confirms the SFE / validates UHF / prime structure is fundamental.” `EquationRegistry.canonical_sfe_status` is a live method.

**Auditor rec.** Claim filter stays (as a claim filter). Evidence ladder 3–6, FRA subtypes, SFE status API → historical only.

**Your mark:**

**Your notes:**

### C10. Compact grammar stays dead

`Φ = ℱ(P,H,ψ,λ;E)` was the FRA five-slot schema.

**Auditor rec.** Do not revive. Paper’s open role list replaces it. Do not keep it as a shim.

**Your mark:**

**Your notes:**

### C11. Drag example on the product surface

Parser splits `D_R`. Pattern unclassified. `translation=None`. Grid search on invented `0.12 (1−e^{−4h})…`. Notes still describe the paper cycle.

**Options.** Remove from default CLI/app / keep only under `examples/` with “invented surrogate, not CFD” / fix to a real plant you specify.

**Auditor rec.** Off the default product surface. If kept, label the method (constrained grid search on an invented scalar).

**Your mark:**

**Your notes:**

### C12. Empirical gate

Correctly never self-awarded. Also unimplemented. `protocol.py` is not wired to any DA cycle.

**Auditor rec.** Keep “never self-award.” Wiring an empirical protocol is a later, explicit project — not a silent `COMPUTATIONAL` upgrade.

**Your mark:**

**Your notes:**

### C13. Version `1.1.0`

`__init__.py` and `/api/status` report 1.1.0 after the dump. No capability increment.

**Auditor rec.** Do not advertise 1.1 as the engine. Freeze or revert until A5/A10–A14 land; then bump once.

**Your mark:**

**Your notes:**

### C14. Difference from bond graphs / Firestone

Live mechanical↔electrical is textbook `m,c,k,f ↔ L,R,1/C,v` plus a stamp. Bond graphs already distinguish effort/flow/inertia/capacitance/resistance and compose them. DA synthesize is a list replace. No ports, junctions, or Modelica interconnection.

**Question.** Until ports exist, must the paper/README say DA is weaker than 1960s bond graphs on lumped energy systems? Or do you want ports implemented as the DA increment?

**Auditor rec.** Admit weaker. The allowed DA increments, if you want a difference that is not “we also want biology and finance”: checked broken-structure, tested morphism substitution gate, independent missing-role search, open roles, domain modules that are not effort/flow.

**Your mark:**

**Your notes:**

### C15. HB ringdown Experiment 01

Held-out TEST: H0 not rejected. Closed.

**Auditor rec.** Remain reproducible under `docs/archive/hb-ringdown/`. Off the DA import graph. Do not retune after TEST.

**Your mark:**

**Your notes:**

### C16. `hb_ringdown_test.py` at repo root

Looks like a peer of DA tests.

**Auditor rec.** Move under archive test path. Do not run as part of the default DA suite.

**Your mark:**

**Your notes:**

### C17. `realization.py`

Second door into `dynamics.py`. Header claims it is the SFE function worth keeping.

**Auditor rec.** Delete the extraction story. Keep RK4 in `dynamics` (or `methods/ivp`) under its honest name.

**Your mark:**

**Your notes:**

### C18. Phantom evolution operator `"D"`

`_assign_wave_like` always inserts `"D"` as `STATE_TRANSITION` even when `D` is not in the expression.

**Auditor rec.** Stop. That is a leftover DHFA slot.

**Your mark:**

**Your notes:**

### C19. Method-first user reports

Missing-damping notes can be read as “DA recovered a missing role.” What ran is OLS on `R` vs `ẋ` on a plant the author already knew.

**Auditor rec.** Lead with the method. DA, if anything, is the role hypothesis, the broken-structure record, the substitution gate, and provenance — and only when those objects actually exist.

**Your mark:**

**Your notes:**

### C20. Identity-`T` hole

A matching pair with identity `T` becomes `INCOMPATIBLE` because DIRECT requires `transformation is None` and TRANSFORMABLE requires `broken or not identity`.

**Auditor rec.** Fix as part of A5. Identity is DIRECT if ports/SI/invariants pass; it is not a dodge and not an auto-fail.

**Your mark:**

**Your notes:**

---

## U — Desktop app

The app is functional as a local lab: Decompose, Translate, Synthesize, Cycle, Archive. Shortcut on this VM: `Domain Architect.desktop`. Launch: `python3 -m domain_architect app`.

### U1. Keep the desktop shell during a rewrite?

**Auditor rec.** Yes. Honesty of labels must track A9/C19. Do not add features (U2 excepted) until blocking architecture lands if P1 is rewrite.

**Your mark:**

**Your notes:**

### U2. Native installers for your Mac

Current installer writes Linux `.desktop` or macOS `.command`. This cloud VM is Linux.

**Auditor rec.** Only if you need it on your machine. Not a rewrite.

**Your mark:**

**Your notes:**

---

## G — Git and process

### G1. Merge #31 to `main` as-is?

**Auditor rec.** No. `main` would then claim Domain Architect is the live product while the engine is a demo lab.

**Your mark:**

**Your notes:**

### G2. Shape of the rewrite PR(s)

**Auditor rec.** Stacked, tests first:

1. Honesty + A5/C20 (`T` / TRANSFORMABLE) + A13 + A14  
2. A10, A11, A12, C3, C18 (classifier truth)  
3. A6, A7 types, C1–C2  
4. A2/A3 selectors as optional  
5. A1/C8 isolation of archive  
6. Layout only if still wanted after 1–5 (A15 remains reject-as-substitute)

**Your mark:**

**Your notes:**

---

## Paper constraints that are not optional unless you amend the paper

Mark **AMEND** only if you are changing [`docs/DOMAIN-ARCHITECT.md`](../DOMAIN-ARCHITECT.md) itself.

| ID | Constraint | Your mark if you want the paper changed |
|---|---|---|
| S1 | Correspondence is a hypothesis, not physical equivalence | |
| S2 | No new universal field equation | |
| S3 | Analogy ≠ mathematical correspondence ≠ structure-preserving equivalence | |
| S4 | Transformable replacement carries `M_B --T--> M̃_B` | |
| S5 | Validation `MATHEMATICAL → COMPUTATIONAL → EMPIRICAL`; empirical not self-awarded | |
| S6 | Mathematical agnosticism: the problem determines the mathematics | |
| S7 | Public unification language (SFE unifies GR and QM, etc.) stays retired | |
| S8 | Do not merge historical SFE formulas into FRA or into DA core | |

If S1–S8 stay unmarked, they stay as in the paper.

---

## After you mark this file

1. Put the marks in this file (or paste them in chat).  
2. If **P1 = rewrite** and the blocking six are marked, implementation starts from those marks — not from a folder plan, not from another dump.  
3. If **P1 = demo-only**, work is README/UI honesty, optional L1–L2, keep #31 draft.  
4. If **P1 = freeze**, stop.

Do not start from [`GROK-SPEC-AUDIT.md`](GROK-SPEC-AUDIT.md) as if the rec column were already your decision. This file is the decision.
