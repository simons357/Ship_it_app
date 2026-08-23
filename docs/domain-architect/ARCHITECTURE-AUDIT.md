# Architecture audit — Domain Architect v1.0 code vs v1.0 paper

**Status:** audit only. No rewrite in this revision.  
**Auditor:** implementation critic (Grok), 2026-08-23  
**Canonical reference:** [`docs/DOMAIN-ARCHITECT.md`](../DOMAIN-ARCHITECT.md)  
**Code under review:** `domain_architect/` on `cursor/domain-architect-v1-f929`

This note answers the request: audit the existing software against the
new canonical definition **before** refactoring. It is deliberately
adversarial. Agreement with the paper is not the goal. The goal is to
stop leftover Harmonic Blueprint assumptions from surviving as “DA” by
renaming, and to stop ordinary numerical methods from being reported as
if they were a new architecture.

---

## 0. Verdict in one paragraph

The current package is a **thin orchestrator around four hardcoded
demonstrations**, plus a still-live FRA/HB laboratory that was labeled
“archive” but not isolated. The paper’s three verbs are the right
product surface. Most of the mathematics that actually runs is
**standard**: dimensional analysis, typed interface matching, the 1933
mechanical–electrical analogy, equation-error system identification,
RK4, saturated PD, and grid search. DA **does not yet differ** from
those methods except as a labeling and gating policy — and several of
those gates are paperwork (`Transformation` object present ⇒
`TRANSFORMABLE`; string tags named `passivity` or `causality` that are
never computed). Prime indexing was not deleted, but it was also **not
generalized**: it is still a privileged special case inside
`selectors.py` and `index_audit.py`. QStack and QNav **do not exist in
this repository**; they cannot be renamed from here.

Do not rewrite until the proposed architecture in §8 is accepted or
amended. The previous v1.0 commit already moved faster than this audit
allows.

---

## 1. What should remain unchanged

These pieces do real work and already use ordinary mathematical names.
Keep the algorithms. Stop advertising them as Domain Architect itself.

| Asset | Why it stays | Honest name |
|---|---|---|
| `parser.py` | Recursive-descent AST; no role inference | expression parser |
| `checks.check_dimensions` | SI 7-tuple equality on an equality AST | dimensional analysis |
| `checks.check_types` / free-index check | Tensor variance hygiene | type / index check |
| `checks.classify_permission` with `P² = P` | Distinguishes projector, selector, filter | operator classification |
| `identifiability.py` | Local Jacobian rank; refuses “identifiable” | local identifiability |
| `protocol.py` | Frozen hash; train / validation / held-out | experimental protocol |
| `gravity.solve_periodic_poisson` | Zero-mode / solvability is correct elliptic hygiene | periodic Poisson solver |
| `dynamics.rk4_step` / `simulate` | Standard IVP + constrained input | state-space simulation |
| `residual` OLS on `{1, x, ẋ}` | Works; recovers `ζ` on the toy | equation-error identification |
| Language sanitizer / forbidden claim phrases | Prevents overclaim | claim filter |
| Historical JSON + `registry.py` | Immutable originals | archive store |
| Equal-budget comparison idea in `selectors.py` | The *lab design* is sound | selector comparison protocol |

The closed HB ringdown experiment (`hb_ringdown_test.py`, `nodes.json`,
`docs/archive/hb-ringdown/`) should remain reproducible and **outside**
the DA import graph.

---

## 2. What should be renamed

Rename by **demonstrated function**, not by historical brand and not by
euphemism.

| Current | Does | Rename to |
|---|---|---|
| `audit_expression` / `AuditReport` | DECOMPOSE + a few special-case labs | `decompose_expression` / `DecompositionReport` |
| `ORGANIZING_GRAMMAR` | A slogan, not a grammar | `PRIMARY_OPERATIONS` |
| `CANONICAL_SFE_STATUS` in live `schema.py` | Archive flag leaking into the core | move to `historical/` |
| `EvidenceLevel` 0–6 | FRA rectification ladder | keep only if mapped onto `ValidationGate`; otherwise historical |
| `ScaleResponseSubtype` (`κ` vs `R`) | HB “scale-response” ontology | `SpectralObjectKind` inside an optional spectral module |
| `PermissionSubtype` | Old `P` role | `SelectionOperatorKind` |
| `newtonian_fra_map` / `role_map` | Labels on a known PDE | delete alias; keep solver |
| `RecoveryKind` / `recovery.py` | “representation vs derivation” from the SFE fight | `RewriteKind` in historical, or drop |
| `valid_for_physical_prime_test` | Index invariance question | `index_is_object_invariant` |
| `cycle_*` demos | Scripted scenarios | `examples/` or `demos/`, not `pipeline.py` as if it were the engine |
| Comment “Newton primes” for `x'`, `x''` | Derivative notation | “Newton prime notation” is fine in the parser; do not say “prime” in DA reports |

UHF / DHFA / SFE **names** should not be preserved as renamed universal
objects. Their *functions*, where justified, should be extracted:

| Legacy name | Justified function | DA object |
|---|---|---|
| UHF as “configuration layer” | admissible states and the space they live in | `State`, `StateSpace`, `AdmissibleSet` (selection / constraint) |
| DHFA as “evolution layer” | how state changes | `Dynamics` / `StateTransition` (`ẋ = F(x,u,t)` or a discrete map) |
| SFE as “realization layer” | how an architecture produces an outcome | `OutcomeModel` / `RealizationMap` (`y = H(x)` or `Φ = realization(architecture)`) — **not** a field equation |
| FRA compact grammar `Φ = ℱ(P,H,ψ,λ;E)` | a fixed five-slot schema | **do not revive**. The paper’s open role list replaces it. |

That extraction is **not** done in the current code. Archiving the
strings is not the same as migrating the functions.

---

## 3. What should be generalized

This is the load-bearing instruction: **do not merely delete primes.
Generalize them.**

### 3.1 Selection is a role; prime is one mechanism

`selectors.py` still treats prime as the reference plan:

- default budget = number of prime indices;
- conclusion text is always about “Prime selection …”;
- `select_prime` is first-class, other masks are “controls.”

That is HB framing with extra controls. The generalization:

```
SelectionMechanism : IndexSet → Mask
```

with a **catalog** of selectors that all obey the same interface and the
same budget:

- lowest-index / cutoff
- odd / even / composite
- random (seeded)
- energy / magnitude optimal
- threshold / sparsity
- **prime-index** (optional)
- user-supplied predicate

The equal-budget lab stays. The null-result discipline stays. Prime
becomes one row in the catalog, role = `selection`, not a DA primitive.

### 3.2 Index audit is about invariance, not primality

`index_audit.py` is actually a good piece of mathematics: array position
is not an invariant; degeneracy makes labels basis-dependent. That
argument applies to **any** discrete selector, including “keep the first
five modes.” Generalize the output to:

> Is the proposed index an invariant of the mathematical object under
> the declared equivalence (basis change, units, ordering, symmetry)?

Prime membership is one predicate you might apply **after** that
question is answered yes.

### 3.3 Compatibility tags must become checks or be marked unchecked

`INVARIANT_KEYS` lists linearity, passivity, causality, conservation,
stability-adjacent adjectives. The implementation never computes a
Lyapunov function, a divergence, a passivity inequality, or a CFL
condition. Either:

- implement a check (even a cheap necessary condition), or
- record `status=not_evaluated`.

A string that says `passivity` is how a universal theory sneaks back in.

### 3.4 Decomposition templates must become a pattern library

`classify.py` hardcodes three shapes: Poisson, wave, second-order linear
ODE. That is fine as a **starter library**. It is not DECOMPOSE. Next
patterns (ordinary names): first-order ODE, conservation law, transfer
function, graph flow, unconstrained optimization, stochastic SDE. No
pattern ⇒ `UNRESOLVED`, not a fake five-level tree.

### 3.5 Residual discovery must be a method, not “the” DA algorithm

`R ~ {1, x, ẋ}` is equation-error SID with a three-regressor library.
Generalize to: role class → operator family → estimator. Families can
grow. Unrestricted symbolic regression stays **out** of the core unless
someone opts in.

---

## 4. What should become optional modules

Move these out of the implicit core import surface. The CLI may still
reach them as `--module` / `--example`.

| Module | Contents | Why optional |
|---|---|---|
| `historical/` | `registry`, SFE JSON, FRA recovery language, `CANONICAL_SFE_*` | archive |
| `mechanisms/selection/` | prime and other selectors + index invariance | optional mechanism |
| `domains/gravity_poisson.py` | periodic Poisson lab | one elliptic example |
| `domains/lumped_analogy.py` | mechanical ↔ electrical map | one known `T`, not a discovery engine |
| `domains/fluids_surrogate.py` | drag grid search | schematic only |
| `examples/` | missing-damping, inverse PD, analog, drag | demos |
| spectral / QNM | `hb_ringdown_test.py`, `nodes.json` | closed experiment |
| `ScaleResponseSubtype` stack | κ vs R(κ) | spectral module, not core ontology |

**QStack:** not present. If it appears from another app, audit it as
possibly several things (controller, validator, constraint monitor) —
do not assume one rename.

**QNav:** not present. If it appears, audit it as a possible **router /
classifier** (which mathematical backend does this problem need?). Do
not assume the historical reading. Until the code exists, do not invent
a QNav module just to have the name.

---

## 5. What should be removed from the live core

Remove means “not imported by `decompose` / `translate` / `synthesize`.”
Do not delete history.

- `CANONICAL_SFE_STATUS` and every report line that still mentions SFE
  as if the user asked.
- Privileged Poisson / Einstein / `y=abx` branches inside the default
  decompose path (`audit.py`). Those become example adapters.
- Award of `STRUCTURE_PRESERVING_EQUIVALENCE` from “same role, same
  type, same SI, no `T`.” That is not an equivalence.
- Award of `TRANSFORMABLE` from “a `Transformation` dataclass was
  attached,” without checking that `T` intertwines the operators.
- Treating `domain == "unspecified"` as an interface match (current
  hole in `compatibility.py`).
- Self-awarded `COMPUTATIONAL` gate on the drag surrogate.
- Empty `provenance=[]` on the flagship missing-damping candidate while
  the paper requires a chain.
- Five-level architecture trees that wrap every symbol as
  ROLE → MECHANISM → OPERATOR → PARAMETER regardless of whether those
  levels exist. That is not recursive decomposition; it is padding.
- Live package docstring / CLI that still frames the product as an
  auditor of historical candidates.

---

## 6. What functionality is missing

Relative to the paper, the gaps are not cosmetic.

1. **A real cycle engine.** `pipeline.py` is four scripts. There is no
   object that takes `target + constraints` and walks
   DECOMPOSE → TRANSLATE → COMPATIBILITY → SYNTHESIZE → PREDICT → TEST
   → RESIDUAL → ITERATE unless a human picks a demo name.
2. **Inverse design that is not a template.**
   `required_roles_for_target` is three booleans. The paper’s question
   — *what functional roles must exist for this target to be
   achievable?* — is not computed from `x★` and `g(x)≤0`.
3. **A mechanism catalog that participates in search.** `catalog.py`
   exists. Synthesis does not search it except by listing IDs in the
   drag demo.
4. **Checked transformations.** `T` must be an object that can be
   applied: `T(M_B) = M̃_B`, with a test that the transformed interface
   matches. Today `T` is a dictionary of letter names.
5. **Compatibility checks the paper lists:** boundary conditions,
   conservation, stability, regularity, positivity. All absent as
   computations.
6. **Mathematical routing (agnosticism).** No dispatcher to ODE,
   spectral, stochastic, graph, optimization, or discrete backends.
   Agnosticism without a router is a slogan. This is the only
   legitimate job a future “QNav” might have — if that code appears.
7. **Realization / outcome model.** Forward analysis produces roles.
   Nothing named and tested implements `y = realization(architecture)`.
   That is the one SFE-function worth keeping, under an ordinary name.
8. **Recursive decomposition.** No subsystem can be decomposed again
   from a child node. Depth is always the same wrapper.
9. **Cross-domain discovery.** The analog pair is **looked up**, not
   found. A second pair cannot be proposed unless a developer writes
   another function.
10. **Provenance completeness** on every synthesized node.
11. **Empirical gate** wired to held-out data. Correctly never
    self-awarded — and also unimplemented.
12. **General selection module** (see §3.1). This is the prime-migration
    task.

---

## 7. Claims stronger than the implementation

| Claim in paper or v1.0 code | What the code does | Overclaim |
|---|---|---|
| CROSS-DOMAIN TRANSLATE | Applies a known Firestone / impedance map | Does not discover correspondences |
| Compatibility examines symmetry, conservation, stability, causality | Copies string tags; optional `shared_invariants` dict | Checklist ≠ theorem |
| `TRANSFORMABLE` | `if transformation is not None` | Paperwork |
| `STRUCTURE_PRESERVING_EQUIVALENCE` | Role + type + SI match | Not an isomorphism or functor |
| Recursive SYSTEM→…→PARAMETER | Always emits the same four child levels | Cosmetics |
| Role confidence 0.55–0.85 | Fixed heuristics | Not calibrated |
| Missing-mechanism discovery | 3-regressor OLS on a known linear ODE | SINDy-class special case |
| Inverse design | Hardcoded PD + `u_ff = ω² x★` | Gains and plant parameters are not taken from the decomposition |
| Drag `COMPUTATIONAL` | Grid search on `0.12 (1−e^{−4h}) …` | Surrogate is invented |
| Mathematical agnosticism | Second-order ODE + Poisson + toy objective | Three problem classes |
| Provenance for every synthesis | Missing on the main benchmark | Policy not enforced |
| Functional correspondence is tested | One pair, author-supplied `T` | Not a test of the hypothesis |

The missing-damping number (`ζ̂ ≈ 0.15`) is **not** an overclaim. It is
a correctly computed least-squares coefficient. The overclaim is calling
that success “Domain Architect recovering a mechanism” rather than
“equation-error identification with a three-term library.”

---

## 8. Challenge: which standard methods is this?

The paper asks DA to be more than disciplinary vocabulary. The
implementation is not yet more than the following, except as a wrapper.

### Already-standard methods inside the repo

| Operation | Standard name | Where in code | Does DA differ? |
|---|---|---|---|
| Units on both sides of `=` | Dimensional analysis | `checks.check_dimensions` | No |
| Domain / codomain / type | Interface / type checking | `signature`, `compatibility` | No, and `"unspecified"` is treated as a match |
| `m,c,k ↔ L,R,1/C` | Bond graphs / Firestone analogy / port-Hamiltonian lumped models (1930s–) | `translate.mechanical_electrical_translation` | **Fails to differ.** This is the textbook example of cross-domain functional roles. DA adds a stamp (`TRANSFORMABLE`) and a warning about SI. Bond graphs already distinguish effort/flow/inertia/capacitance/resistance **and** compose them. |
| `R = ẍ + ω²x`, regress on `ẋ` | Equation-error SID; special case of SINDy / sparse regression | `residual.py` | **Policy difference only:** library is role-restricted. Algorithm is OLS. |
| `ẋ = F(x,u,t)`, RK4, PD + saturation | Model-based control / state-space design | `dynamics.py` | No |
| `max D_R(θ)` s.t. mass | Constrained surrogate optimization | `catalog.optimize_drag_surrogate` | No |
| `P² = P` | Linear algebra | `classify_permission` | No |
| Jacobian rank | Local identifiability | `identifiability.py` | No; language is already honest |
| AST + pattern templates | Computer algebra / program analysis | `parser` + `classify` | No |
| Frozen train/test hash | Experimental hygiene | `protocol.py` | No |
| Role labels on terms | Lightweight ontology / annotation | `FunctionalRole` | Ontology mapping, not inference |

### Where DA *could* differ, if implemented

1. **Role-restricted search.** Not symbolic regression over arbitrary
   expressions; search only inside a declared operator class. That is a
   *restriction* of SINDy, not a competitor — useful if and only if the
   role classifier is right more often than an unrestricted library.
2. **Broken-structure records.** Standard analogy hides what fails.
   Forcing `T` plus an explicit “broken: SI, carriers, …” list is the
   one methodological increment worth keeping. It is not implemented as
   a check, only as a note on the analog pair.
3. **Substitution gate.** Refuse synthesis unless compatibility is
   `DIRECT` or `TRANSFORMABLE` with an **applied** `T`. The refuse path
   exists; the `T` is not applied.
4. **Provenance as a product requirement.** Ordinary in workflow
   systems (PROV). Rare in equation toys. Worth keeping if enforced.
5. **Mathematical routing.** If “agnosticism” means a dispatcher —
   this problem is an IVP, that one is a BVP, that one is a program, that
   one is an optimization — then DA is a **research executive**, not a
   new calculus. That layer is missing. Do not call it QNav until the
   function exists.

### Bond graphs are the uncomfortable comparison

If the authors cannot state a difference from bond graphs / linear
graph modeling / port-Hamiltonian interconnection that is **not**
“we also want biology and finance,” then DA is a software UX over a
known modeling discipline. That is allowed. It is not a new theory.
The paper should say so, or the software should do something bond
graphs do not: open roles, residual-driven missing-role search,
enforced broken-structure, and domain modules that are not effort/flow.

TRIZ, C-K design theory, and SysML “function–behavior–structure” are
the organizational cousins. Symbolic regression and program synthesis
are the generative cousins. Modelica is the composition cousin. DA
currently sits below all of them in capability and above them only in
ambition.

---

## 9. HB assumptions still in the live path

These are the smuggling routes.

1. **Prime as reference selector** (`selectors.py`), not one mechanism.
2. **`valid_for_physical_prime_test`** as a core field.
3. **Scale-response ontology** (`κ`, `R(κ)`) still in `schema.py`, used
   by gravity and checks — the old `λ` role under new file names.
4. **`audit.py` special-cases** the same gravity/GR examples the FRA
   rectification used to prove it was not a theory of everything.
   Defensive HB posture, not DA.
5. **NAME_GUARD** still organized around H, P, λ, Φ, φ, ψ — correct
   hygiene, but the symbol set is the old religion.
6. **Five-level tree padding** recreates “every system has the same
   anatomy,” which is what the paper forbids for roles.
7. **Hardcoded open role enum** of nine plus state/parameter. The paper
   says the list is open. An enum that is the only assignment target is
   a closed ontology. That is how `P,H,ψ,λ` returns without the Greek.
8. **SFE status still in live schema** and historical tests imported as
   first-class package constants.
9. **Repo-root HB experiment** still looks like a peer of DA.
10. The v1.0 demos all come from the paper’s own examples (oscillator,
    analog, drag). Fine as tests. Dangerous if they *are* the product.

---

## 10. Proposed software architecture (not yet implemented)

Approve or amend this before any further code move.

```
domain_architect/
  core/                     # the only required import surface
    types.py                # FunctionalSignature, RoleHypothesis
    decompose.py            # analysis: system → architecture tree (real recursion)
    translate.py            # correspondence records; does not invent T
    compatibility.py        # DIRECT / TRANSFORMABLE / INCOMPATIBLE
    synthesize.py           # hypothesis assembler; refuses illegal T
    cycle.py                # target+constraints loop; iterate on residual
    provenance.py           # mandatory record; fail closed if missing
    claims.py               # validation gates + claim filter
  math/                     # established methods, named honestly
    parse.py
    dimensions.py
    linop.py                # projector / selector / filter
    identify.py             # equation-error / residual
    ivp.py                  # RK4, controllers
    identifiability.py
    protocol.py
  mechanisms/               # optional; all implement one interface
    selection/              # prime, cutoff, random, energy, …
    dissipation/
    restoring/
    forcing/
    feedback/
  domains/                  # optional validated modules
    lumped_analogy.py
    poisson_periodic.py
    …                       # grow only with a benchmark
  historical/               # no core import
    sfe_uhf_dhfa/
    hb_ringdown/            # move runner + nodes.json here
  examples/                 # not the engine
```

### Core object model (ordinary names)

```
State x ∈ StateSpace
AdmissibleSet ⊂ StateSpace          # selection / constraint
Dynamics: (x, u, t) → ẋ or x⁺       # state transition
Realization: architecture → y       # outcome model
Controller: (x, x★, C) → u
Mechanism: signature + operator + parameters
Correspondence: (M_A, M_B, T?, preserved, broken, kind)
Candidate: components + provenance + gate
Residual: y − ŷ  or  L̂[y]
```

No field equation. No mandatory role count. No prime in `core/`.

### Compatibility rule (stricter than today)

```
DIRECTLY COMPATIBLE
  iff interfaces match
  and dimensions match (unknown ⇒ not direct)
  and required invariants are either checked-pass or explicitly waived

TRANSFORMABLE
  iff an executable T is supplied
  and T(M_B) meets the DIRECT tests against M_A
  and broken structure is non-empty or T is not the identity

INCOMPATIBLE
  otherwise, including “same role word, no T”
```

`STRUCTURE_PRESERVING_EQUIVALENCE` is **not** a software verdict until
someone implements a real equivalence check. Drop it from the enum or
reserve it for tests that exhibit an intertwining relation.

### Prime migration (explicit)

```
mechanisms/selection/prime.py   # optional
mechanisms/selection/lab.py     # equal-budget comparison, any selectors
math/index_invariance.py        # generalized index_audit
```

Core decompose may assign role `selection`. It may not import
`is_prime`.

### What I will not do in the rewrite (if approved)

- Invent QStack or QNav modules to match names that are not in this repo.
- Keep `Φ = ℱ(P,H,ψ,λ;E)` as a compatibility shim.
- Call OLS on three regressors “mechanism discovery” in user reports.
- Award computational or empirical gates on invented surrogates.
- Treat the mechanical–electrical map as evidence that translation
  *works* in general. It is a regression test for the stamp, not a
  scientific result.

---

## 11. Recommended decision for the human audit

Please mark each item accept / amend / reject:

1. Isolate `historical/` so core cannot import SFE/UHF/DHFA/HB.
2. Generalize selectors; prime becomes one optional `selection` mechanism.
3. Generalize index audit to invariance; drop prime-specific fields.
4. Demote `pipeline.py` demos to `examples/`; write a real `cycle.py` or
   admit that v1 is examples-only.
5. Make `T` executable or stop using the word TRANSFORMABLE.
6. Drop `STRUCTURE_PRESERVING_EQUIVALENCE` as a live verdict.
7. Extract UHF/DHFA/SFE *functions* as StateSpace / Dynamics /
   Realization — never as renamed equations.
8. Leave QStack/QNav absent until their code is in-tree.
9. State in the README that lumped analogy and residual OLS are
   standard methods used by DA, not DA itself.
10. Pause further feature work until 1–6 are done.

If 9 is rejected — if the product must claim that those demos *are*
cross-domain architecture — then the paper is making a stronger claim
than any implementation in this repository can support, and the next
rewrite will only polish the overclaim.
