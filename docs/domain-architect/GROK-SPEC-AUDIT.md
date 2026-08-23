# GROK spec audit — current working tree vs DA paper + refactor spec

**Auditor:** Grok (independent implementation critic), 2026-08-23  
**Tree:** `/workspace` on `cursor/sfe-rewrite-domain-architect-9d6b`  
**Canonical paper:** `docs/DOMAIN-ARCHITECT.md`  
**Operational math:** `docs/domain-architect/OPERATIONAL-MATH.md`  
**Rival brief (do not treat as source):** `docs/domain-architect/ARCHITECTURE-AUDIT.md` — a prior critic wrote it; a later “SFE/HB dump” performed *wording compliance*. This audit is of the files as they are, not of that decision log.

This is a challenge document. Agreement with Jon, the other agent, the paper’s self-description, or the dump is not the goal.

---

## 0. Verdict

The live package is a **three-verb UI** (`DECOMPOSE → TRANSLATE → SYNTHESIZE`) wrapped around a **three-pattern classifier** (second-order-ish ODE, Poisson, wave) and **four scripted demos**. The dump isolated some SFE *strings* and added `cycle.py` / `realization.py` as hollow objects; it did **not** make Domain Architect mathematically agnostic, did **not** generalize primes into one selector among many on the live path, and did **not** implement the paper’s cycle. Most running mathematics is Firestone analogy, equation-error OLS on `{1,x,ẋ}`, RK4, saturated PD, FFT Poisson, and an invented drag polynomial. DA differs from those methods only as a **labeling and stamp policy**, and the stamps are now *worse* than a missing feature: `Transformation.apply` remaps dictionary keys, and attaching any such object — even across mismatched roles and unknown types — yields `TRANSFORMABLE` plus `mathematical_correspondence`. Inverse design ignores the target string. First-order ODEs are branded `second_order_linear_ode`. The flagship drag example does not parse. This is not a domain-architecture engine. It is a claim-control layer over textbook demos, with a gravity/FRA ontology still sitting in `schema.py` and `checks.KNOWN_UNITS`.

---

## 1. What should remain unchanged

Keep the algorithms. Stop advertising them as DA. Do not “extract” them into `realization.py` wrappers just to claim the SFE function was migrated.

| Asset | Demonstrated function | Honest name |
|---|---|---|
| `parser.py` | Recursive-descent AST; `NAME_GUARD` refuses H/P/λ/Φ auto-identity | expression parser |
| `checks.classify_permission` with `P² = P` | Distinguishes projector / selector / filter | linear-algebra operator test |
| `identifiability.py` | Local Jacobian rank; refuses “the parameters are identifiable” | local identifiability |
| `protocol.py` | SHA-256 freeze; train / val / held-out | experimental protocol |
| `dynamics.rk4_step`, `pd_control`, `simulate` | Standard IVP + box-constrained PD | state-space simulation |
| `residual.recover_missing_damping` | `R = ẍ + ω²x`, regress on `ẋ` | equation-error identification |
| `gravity.solve_periodic_poisson` zero-mode reject | Correct periodic-elliptic hygiene | FFT Poisson solver — **example**, not core |
| `report.sanitize_language` / `FORBIDDEN_CLAIM_PHRASES` | Overclaim filter | claim filter |
| `registry.py` immutability of `original_expression` | Archive integrity | historical store |
| Equal-budget *idea* in `selectors.py` | Fair comparison lab | selector protocol — **not** a DA primitive |
| `docs/archive/hb-ringdown/` + `hb_ringdown_test.py` | Closed, failed HB experiment | leave reproducible and **off** the DA import graph |
| Paper’s three-way distinction analogy / correspondence / structure-preserving equivalence | The *requirement* | keep as a scientific distinction; the dump deleted the third kind instead of implementing it |

The dump’s useful residue is the refusal path in `synthesize()` when a report is already `INCOMPATIBLE`, and the explicit “hypothesis, not physical equivalence” sentences. Those are policy. They are not an architecture.

---

## 2. What should be renamed (by demonstrated function, not brand)

The dump renamed slogans (`ORGANIZING_GRAMMAR` → alias of `PRIMARY_OPERATIONS`; `CANONICAL_SFE_STATUS` moved to `historical.py`). It left the **functional misnames** that the spec actually cares about.

| Current | What the code demonstrably does | Rename to |
|---|---|---|
| `FunctionalRole.STATE_TRANSITION` on symbol `m` in `classify._assign_second_order_ode` | Coefficient of `ẍ`. That is an **inertial parameter**, not a state-transition map | `parameter` of operator `d²/dt²`, or role `inertia` if you insist on a role word. `ẋ = F(x,u,t)` is the state transition. **This assignment is test-locked** in `tests/test_domain_architect_v1.py::test_second_order_roles`. |
| `FunctionalRole.CONSTRAINT` on `"Laplacian"` | Elliptic operator `∇² : H² → L²` | `elliptic_operator` / `state_to_source_map`. A constraint is `g(x)≤0` or a gauge. The paper’s constraint role is an admissible-set mechanism, not Poisson. |
| `SUBSYSTEM: second_order_linear_ode` (`decompose.decompose`) | Pattern tag, not a subsystem | `pattern` attribute. A subsystem is a part that itself decomposes. |
| `OPERATOR: dynamic_state` under state `x` | The state is not an operator | delete this child; `x` is `STATE` / `PARAMETER` of the trajectory |
| `audit_expression` served as `/api/decompose` and CLI default | Kitchen-sink: parse + classify + optional Poisson solve + `y=abx` identifiability + Einstein string match | `analyze_expression`. Decompose is `decompose.py` only. |
| `pipeline.py` titled “The Domain Architect cycle” | Four named scripts | `examples/` / `demos/` |
| `cycle.run_cycle` | Optional callbacks in a fixed order; **no iterate**, no compatibility step | `run_scripted_pass` until it is a state machine |
| `realization.realize_second_order` | Calls `free_oscillator_trajectory` / `simulate` | do not exist as a separate “SFE function.” The comment *“the one SFE function worth keeping”* is brand laundering. |
| `Transformation` | `dict` key rename; `applied=True` after one comprehension | `NameMap` until it is a morphism |
| `CorrespondenceKind.MATHEMATICAL_CORRESPONDENCE` awarded in `classify_compatibility` whenever a `Transformation` object is present | Stamp | `named_map_supplied` |
| `PermissionSubtype` / “permission object” (`schema.py`, `audit.py`) | FRA `P` vocabulary | `SelectionOperatorKind` in an optional module |
| `ScaleResponseSubtype` (`κ` vs `R(κ)`) | FRA/HB `λ` split | spectral-module types, not core ontology |
| `valid_for_physical_prime_test` (`index_audit.py`) | Index invariance under degeneracy | `index_is_object_invariant` — and stop saying “prime” in the field name |
| `EvidenceLevel.REPLICATED_GENERAL_PHYSICAL_THEORY` | Unification ladder | historical only |
| `RecoveryKind` / `recovery.py` | “representation vs derivation” from the SFE fight | archive, or `RewriteKind` |
| `newtonian_fra_map` | Alias | delete |
| `SOURCE_STATE_WARNING` in live `schema.py` | P/H/ψ product split | archive |
| `EquationRegistry.canonical_sfe_status` | Live method on the store the app loads | archive-only API |
| Desktop tab “Archive” as a first-class product pane | Surfaces SFE IDs through `/api/archive` | opt-in CLI only, not a peer of Decompose |

UHF / DHFA / SFE **must not** be preserved as renamed universal objects. Their *functions*, where a function actually exists in this tree:

| Legacy name | Justified function in *this* tree | Honest object | What the dump did instead |
|---|---|---|---|
| UHF “configuration” | Almost nothing. No `StateSpace`, no admissible set type. `FunctionalSignature.domain` is a string (`"state_space"`, `"time"`, `"unspecified"`) | `State`, `StateSpace`, `AdmissibleSet` — **missing** | Left strings |
| DHFA “evolution” | `dynamics.second_order_field` / `rk4_step` | `Dynamics: (x,u,t)→ẋ` | Already existed; was not extracted from HB |
| SFE “realization” | `realize_second_order` is RK4 with a new file header | `OutcomeModel` only if it maps *architecture → y* for more than one plant | Added a comment that this *is* the SFE function |

Extracting functions is not writing `realization.py`. The dump treated the rival’s item 7 as a rename task. It was not.

---

## 3. What should be generalized (especially primes → optional selection)

The spec’s load-bearing line: **do not merely delete primes; generalize them.** The dump did neither deletion nor generalization on the live path. `selectors.py` / `index_audit.py` are imported by tests and the historical suite, **not** by `decompose`, `translate`, `synthesize`, `cycle`, or `pipeline`. Prime is shelfware with HB framing, not an optional mechanism the architecture can select.

### 3.1 Selection is a role; prime is still the reference *experiment*

`selectors.run_selector_lab`:

- default `budget = prime_indices(n).size`;
- plan list leads with `("prime", select_prime(...))`;
- conclusion text is always “Prime selection outperformed / did not…”;
- `negative = not (prime.reconstruction_error < mean_random)`.

That is an HB experiment with extra controls. Generalization is a **common interface**, not a longer comment:

```
SelectionMechanism : (Indexable, Budget, Protocol) → Mask
```

Catalog rows, all first-class: cutoff / low-index, odd, even, composite, random(seed), energy/magnitude, threshold/sparsity, **prime-index (optional)**, user predicate. The lab compares **whichever rows are registered**. Prime is not the subject of the sentence.

`FunctionalRole.SELECTION` exists in the enum and is **never assigned** by `classify.py`. Until decompose can emit `selection` for a mask/projector/admissible-set, “prime as optional mechanism” is a file sitting next to the product, not in it.

### 3.2 Index audit is invariance, not primality

`audit_canonical_index` is real mathematics (degeneracy ⇒ label is not an object invariant). The output field `valid_for_physical_prime_test` re-specializes it. Generalize to: *is the proposed index invariant under the declared equivalence (basis, units, ordering, symmetry)?* Primality is a predicate you may apply **after** that answer is yes. The dump left the prime-specific field and the historical test that asserts it (`test_historical_archive.py`).

### 3.3 Derivative-order → role is a *classifier plugin*, not DECOMPOSE

`classify._assign_second_order_ode` maps order 2/1/0 → `STATE_TRANSITION` / `DISSIPATION` / `INTERACTION`. That is one pattern. It is hardcoded as the live meaning of “functional architecture.” Generalize to a **registered pattern library** with an explicit `UNRESOLVED` default. First-order, conservation form, transfer function, graph flow, constrained optimization, SDE — none exist.

Worse: `_looks_like_second_order_ode` is `max(derivative_order) >= 1`. Live result:

```
decompose("xd + a*x = u") → pattern = "second_order_linear_ode"
decompose("c*xd + k*x = f") → pattern = "second_order_linear_ode"
```

A first-order plant is labeled second-order. Generalizing “the ODE template” without fixing the predicate is how a special case becomes a fake universal.

### 3.4 Role-restricted residual search is circular

`classify_missing_mechanism` correlates `R` with `{1, x, ẋ}` and then “restricts” the operator class to the winner. The restriction **is** the classification. This is not “DA restricts SINDy.” It is SINDy with library `{1,x,ẋ}` and role-colored output. Generalize only if the role class is supplied **independently** of the regressors (architecture hypothesis → operator family → estimator). Unrestricted symbolic regression stays out of core.

### 3.5 Compatibility tags must become checks

`INVARIANT_KEYS` lists linearity, passivity, self-adjointness, causality, positivity, hyperbolic, elliptic, conservation. Nothing computes a storage function, a divergence, a spectrum, or a CFL number. `shared_invariants={"linearity": True, ...}` is passed in by `translate._translate_second_order` because the author already decided the pair is LTI. Generalize: each named invariant is `checked | failed | waived | not_evaluated`. A string that says `passivity` is how a universal theory returns.

### 3.6 `KNOWN_UNITS` must become a context, not a relativity table

`checks.KNOWN_UNITS` hardcodes `c` = speed of light, `k`/`kappa` = wavenumber, `G`, `Phi`, `rho`. On `m*xdd + c*xd + k*x = f`, `c` and `k` are silently given light-speed and inverse-length units; `m`,`x`,`f` are unknown, so the checker shrugs. Supply mechanical units for only the unknowns and the leftover HB table will **lie**. Generalize: units come from the caller’s context. The gravity 7-tuples belong in `examples/poisson/`.

---

## 4. What should become optional modules

Optional means: not imported by the analysis/synthesis path; CLI/app may reach them as `--example` / `--archive`.

| Module | Why it is not core |
|---|---|
| `historical.py`, `registry.py`, `data/domain_architect/*.json` | SFE/UHF/DHFA inventory. `cli.py` and `app.py` still import them. |
| `selectors.py`, `index_audit.py` | Prime lab. Optional **selection** package after §3.1. |
| `gravity.py` | Periodic Poisson. `audit.py` imports it on the live decompose path. |
| `recovery.py` | SFE-fight “representation vs derivation” |
| `identifiability.py` | Honest linear algebra; not a DA operation |
| `protocol.py` | Experimental hygiene for selector/QNM labs |
| `catalog.drag_surrogate` / `optimize_drag_surrogate` | Invented `0.12 (1−e^{−4h})…` |
| `translate.mechanical_electrical_translation` | One known `T`, not a discovery engine |
| `pipeline.cycle_*` | Demos |
| `app.py` + `static/` | UX |
| `schema.ScaleResponseSubtype`, `PermissionSubtype`, `EvidenceLevel` 3–6 | FRA ontology |
| `hb_ringdown_test.py`, `docs/archive/` | Closed history |

The rival audit proposed `historical/`, `mechanisms/selection/`, `domains/`. Folder moves without cutting the `audit.py → gravity.py` import and the `app.py → registry.py → historical.py` chain are the dump again.

---

## 5. What should be removed from the live core

Remove = not imported by `decompose` / `translate` / `compatibility` / `synthesize` / the default CLI decompose. Do not delete history.

1. **`audit.py` special cases:** `_looks_like_poisson` → `solve_periodic_poisson`; `_looks_like_einstein` (the test is `"G" in text and "T" in text and "mu"` — `G_{mu nu} = 8 pi T_{mu nu}` appends a GR essay); `_looks_like_linearized_gravity`; `_looks_like_product_abx` → `analyze_product_abx(np.array([1,2,3]))` with **canned numbers**, not the user’s data. These are HB/FRA defensive labs wired into “DECOMPOSE.”
2. **`KNOWN_UNITS` relativity table** in the default dimensional environment.
3. **`CANONICAL_SFE_STATUS` on the live `EquationRegistry`** used by `/api/archive` and `--archive` as if archive were a core mode.
4. **`realization.py` as an SFE extraction.** It is a second door into `dynamics.py`.
5. **Award of `TRANSFORMABLE` / `MATHEMATICAL_CORRESPONDENCE` from `T.apply` succeeding.** `apply` cannot fail on a dict. Live hole (executed):

   ```
   classify_compatibility("a", DISSIPATION/UNKNOWN/unspecified,
                          "b", FORCING/UNKNOWN/unspecified,
                          transformation=Transformation("magic", {"a":"b"}))
   → TRANSFORMABLE, mathematical_correspondence, interface_match=False
   ```

   Opposite hole: a matching pair with an **identity** `T` becomes `INCOMPATIBLE`, because `DIRECTLY_COMPATIBLE` requires `transformation is None` and `TRANSFORMABLE` requires `broken or not identity`.
6. **`STRUCTURE_PRESERVING_EQUIVALENCE` deleted from `CorrespondenceKind`.** The dump “fixed” the rival by removing the paper’s third kind. Removal from the enum is not removal of a false award; it is non-conformance with Part A / paper §6–10.
7. **Test lock** `roles["m"] == STATE_TRANSITION`. It cements a wrong ontology.
8. **Default translate fallback** in `cli._print_translate` and `app.handle_api("/api/translate")`: if the user omits `--example` and omits one side, the mechanical–electrical pair runs anyway. That trains the product to be Firestone.
9. **Prime-centric conclusion text** if `selectors.py` remains importable from the package root.
10. **Five-level *padding* was not the right deletion.** The dump’s `test_mechanism_is_not_wrapped_in_dummy_parameter` celebrates `PARAMETER ∉ tree`. The paper requires `SYSTEM → … → PARAMETER` when a parameter exists. `m`, `c`, `k` *are* parameters. They are stored as `MECHANISM`. That is a category error, not honesty.

---

## 6. What functionality is missing relative to the paper + spec

Gaps are architectural, not cosmetic.

1. **The cycle.** Spec: `TARGET + CONSTRAINTS → DECOMPOSE → FUNCTIONAL ARCHITECTURE → CROSS-DOMAIN TRANSLATION → COMPATIBILITY → SYNTHESIZE → PREDICT → TEST → RESIDUAL → ITERATE`.  
   `cycle.run_cycle` optionally decomposes a plant string, optionally runs a caller-supplied translator, then `inverse_design_architecture` if no synthesizer, optionally predicts, optionally residuals. **No compatibility step. No iterate.**  
   `pipeline.cycle_missing_damping` / `cycle_inverse_control` / `cycle_drag_reduction` **do not call `run_cycle`**. They build `CycleReport(...)` by hand. The “engine” is unused by the product demos. `/api/inverse-cycle` is the only caller.

2. **Recursive decomposition.** `decompose()` builds one `SYSTEM`, optionally one `SUBSYSTEM` named after the pattern, then groups hypotheses. `ArchitectureNode` cannot be re-entered. There is no `SYSTEM → SUBSYSTEM → …` recursion over independently functioning parts. Depth is a wrapper.

3. **Inverse design from `x★` and `g,h`.** `required_roles_for_target` is three booleans, all hardcoded `True`/`bool(constraints)` in `inverse_design_architecture`. Executed:

   ```
   inverse_design_architecture("maximize profit", ["tax law"])
   inverse_design_architecture("x=1", ["|u|<=6"])
   ```

   **Identical** component lists: `state / measure / compare / PD-ish u=K / ẋ=F / saturation`. The target is interpolated into a sentence. Constraints are not parsed. There is no `g_i(x)≤0` object.

4. **Checked `T`.** Paper: `M_B --T--> M̃_B` and then interface tests of `M̃_B` against `M_A`. Code: `Transformation.apply` returns `{mapping.get(k,k): v}`. Synthesis substitutes **symbol strings** (`replacements={"c":"R"}`); it does not apply `T` to an operator.

5. **Paper’s compatibility checklist:** dimensional consistency of the *map*, mathematical type, domain/codomain of `T`, boundary conditions, invariants, symmetry, conservation, stability. Absent as computations. `domain`/`codomain` are informal strings (`"force_like"` vs `"voltage"`). ODE coefficients are all given `domain="state_space"`, `codomain="force_like"` in `classify.py`, so mechanical mass and electrical inductance **interface-match** before any Firestone map.

6. **Cross-domain discovery.** `translate()` has two branches: both patterns `second_order_linear_ode` → letter pairing by role; else `_translate_generic` first-match on role name, confidence 0.2, **no compatibility reports**. Executed generic map:

   ```
   m*xdd+c*xd+k*x=f  vs  ∇²Φ=4πGρ
   → {x:Phi, k:G, f:rho}, kind=analogy
   ```

   State↔potential, stiffness↔Newton G, force↔density. That is ontology matching by enum equality. It should not emit a mapping.

7. **Mechanism catalog search.** `catalog.default_catalog()` is eight frozen entries. `synthesize` does not query it. Drag copies IDs into `components` and leaves `provenance=[]`.

8. **State space / admissible set / outcome model as types.** No `StateSpace`. No constraint set `C` except `np.clip` in PD. No `y = realization(architecture)` that takes a `CandidateArchitecture`.

9. **Open role list.** Paper: deliberately open. Code: `FunctionalRole` enum is the only assignment target. New roles cannot be declared without a code change. That is a closed ontology — how `P,H,ψ,λ` returns as `selection, interaction, state, scale`.

10. **Provenance completeness.** `Provenance.original_domain` is set to `report.right` (the **symbol**, e.g. `"R"`). `cycle_drag_reduction` ships `provenance=[]`. `cycle_missing_damping` now has a record (dump fix) whose `source` is `"equation-error OLS…"`.

11. **Mathematical routing.** Agnosticism requires a dispatcher: IVP, BVP, DAE, stochastic, graph, program, optimization. `classify.py` routes to three HB-era shapes. That is a captured router, not agnosticism.

12. **Empirical gate.** Correctly never self-awarded. Also unimplemented. `protocol.py` is not wired to any DA cycle.

13. **Forward *and* inverse as duals.** Analysis mode is “paste an equation.” Synthesis mode is “always emit a PD loop.” Neither consumes the other’s architecture object as a first-class value except the analog demo’s string swap.

14. **QStack / QNav functions** — see §10. Missing as modules; the *routing* function exists in a harmful form.

---

## 7. Claims stronger than the implementation

| Claim | Where | What runs |
|---|---|---|
| “computational framework for computer-aided system architecture” / “reasoning across mathematical, scientific, engineering and organizational domains” | paper abstract; `schema.PRODUCT_DESCRIPTION` | Three patterns + four demos, all LTI/Poisson/toy |
| `DECOMPOSE` is recursive `SYSTEM→…→PARAMETER` | paper §6; `decompose` docstring “Depth follows independently functioning parts” | One wrapper; `PARAMETER` omitted; `m` stored as `MECHANISM` |
| `TRANSLATE` searches for correspondences | `translate.translate` docstring | Lookup of matching derivative order, or role-name join |
| Compatibility checks interface, dimensions, named invariants | `OPERATIONAL-MATH.md` §4 | String equality + optional SI 7-tuple + author-supplied `shared_invariants` |
| `TRANSFORMABLE` requires executable `T` and `T.apply()` success | `compatibility.py` header; dump tests `test_apply_remaps_coefficients` | Key rename; vacuous T awards correspondence |
| “A transformable mechanism must carry an explicit transformation `M_B --T--> M̃_B`” | paper §6–10 | `M̃_B` is a new letter |
| Inverse: `DESIRED OUTCOME → REQUIRED ARCHITECTURE` | paper §4; `/api/synthesize`; desktop hint | Constant PD architecture |
| Drag notes: “TARGET → DECOMPOSE → TRANSLATE → SYNTHESIZE → SIMULATE → OPTIMIZE” | `pipeline.cycle_drag_reduction` | `translation=None`, pattern `unclassified`, parser splits `D_R` into `D` and `R`, grid search on an invented scalar |
| “This is ordinary least squares… not symbolic regression” used as if that made it DA | `OPERATIONAL-MATH.md` §5; missing-damping notes | It is OLS. Calling it “not SR” does not make it DA. |
| Mathematical agnosticism; primes/HB “not part of the live mathematics” | `OPERATIONAL-MATH.md` §8; README | Live `KNOWN_UNITS` is a gravity table; live `audit_expression` special-cases Poisson/GR; live schema still carries FRA subtypes; app Archive pane loads SFE IDs |
| `run_cycle`: “Callers supply the methods; DA supplies the order” | `cycle.py` | Named product cycles bypass it |
| Version `1.1.0` | `__init__.py`, `/api/status` | Dump increment, not a capability increment |
| Confidence 0.55–0.85 | `classify.py` | Fixed literals |
| Desktop: “legal map records… executable T” | `static/index.html` | Firestone default |
| `registry._would_merge_silently` | `registry.py` | `return False` — dead guard |
| Two letter-renamed oscillators are a mathematical correspondence | `_translate_second_order` on `m,c,k` vs `M,b,q` | Same pattern ⇒ same stamp as mech/electrical |

The missing-damping number `ζ̂ ≈ 0.15` is a correctly computed coefficient. The overclaim is *“Domain Architect recovered a missing role.”* The classifier was handed `R ∝ ẋ` on a plant the author already knew.

---

## 8. Standard-method challenge table

If an operation is already a named method, say so. DA’s job is to differ or to admit it does not.

| Standard method | Where in this tree | Does DA differ? |
|---|---|---|
| Dimensional analysis (SI 7-tuple / Buckingham-style side check) | `checks.check_dimensions` | **No.** Weaker: no Π-groups; default env is a relativity table; unknown ⇒ shrug. |
| Tensor free-index hygiene | `checks.check_types` | **No.** |
| Firestone / mobility / impedance analogy (1930s); linear graph modeling | `translate.MECHANICAL_ELECTRICAL_MAP`, `mechanical_electrical_translation` | **Fails to differ.** Textbook `m,c,k,f ↔ L,R,1/C,v`. DA adds a stamp and an SI warning. Bond graphs already distinguish effort/flow/inertia/capacitance/resistance **and compose them**. DA `synthesize` is a list `replace`. Until ports/junctions exist, DA is strictly weaker than 1960s bond graphs. |
| Port-Hamiltonian / Modelica interconnection | nowhere | **Fails to exist.** |
| Ontology alignment / schema matching | `translate._translate_generic` | **No.** First role-name join. Emits `x→Φ`, `k→G` across ODE vs Poisson. |
| Equation-error system identification | `residual.equation_residual`, `recover_missing_damping` | **No.** |
| SINDy / sparse library regression | `classify_missing_mechanism` on `{1,x,ẋ}` | **Policy claim only.** Library is three terms. No sparsity. Role colors the winner. **Circular with the ODE role template.** |
| Symbolic regression / program synthesis | `synthesize` | **No.** String-list assembly; `inverse_design_architecture` is a template. |
| Model-based design / SysML FBS | `ArchitectureNode` tree | **No.** Labels, not ports, contracts, or allocations. |
| Classical state-space control; saturated PD | `dynamics.pd_control`, `cycle_inverse_control` | **No.** Gains `kp=8, kd=3` and `u_ff=ω² x★` are not taken from the decomposition. |
| RK4 | `dynamics.rk4_step` | **No.** `realization.py` admits this in `method`. |
| Spectral Poisson / FFT | `gravity.solve_periodic_poisson` | **No.** Correct numerical analysis, wrong product layer. |
| Projector identity `P²=P` | `checks.classify_permission` | **No.** |
| Local identifiability (rank `J`) | `identifiability.py` | **No.** Language already honest. |
| Constrained grid search | `catalog.optimize_drag_surrogate` | **No.** Objective is invented. |
| AST pattern matching / compiler passes | `parser.py` + `classify.py` | **No.** Three patterns. |
| Claim / evidence gating (PROV-lite) | `Provenance`, `ValidationGate`, `sanitize_language` | **This is the only software product.** It is workflow policy, not domain architecture. Ordinary in scientific workflow systems. |
| TRIZ / C-K / function–behavior–structure | nowhere as search | Paper’s organizational cousins. DA is below them in capability. |
| QNM / spectral family test | `hb_ringdown_test.py` | Archived HB experiment. Not DA. |

**Where DA *could* differ, if it existed:**

1. **Broken-structure as a checked object** — not a note list on one analog pair. Bond graphs hide the SI break; DA’s only increment is forcing the break into the record. Today the break is hardcoded `broken = ["si_dimensions","physical_carriers"]` in `_translate_second_order` *before* the pair is examined.
2. **Substitution gate with a real morphism** — refuse unless `T` is tested on a witness (transfer-function poles, energy quadratic form, residual class). The refuse path exists; the morphism does not. The dump’s “executable T” test **regressed honesty**.
3. **Role-restricted search with an independent role hypothesis** — useful iff the classifier is not the same heuristic as the library. It currently is.
4. **Mathematical routing** — a research executive, not a calculus. Missing. Do not name it QNav.

If the authors cannot state a difference from bond graphs / linear graph modeling that is **not** “we also want biology and finance,” DA is a UX over a known discipline. That is allowed. It is not a new architecture. The paper should say so, or the software should do what bond graphs do not: open roles, residual-driven *independent* missing-role search, enforced broken-structure checks, and domain modules that are not effort/flow.

---

## 9. HB/SFE assumptions still smuggled into the live path

The dump’s thesis: *strings archived ⇒ assumptions isolated.* False. Smuggling routes in the **current** tree:

1. **`checks.KNOWN_UNITS`** — `c`, `k`, `G`, `Phi`, `rho` as a default live environment. This is the gravity/HB dimensional religion. The oscillator demo lives in this environment.
2. **`audit.py` live special-cases** Poisson, Einstein-by-substring, linearized gravity, `y=abx`. Same examples the FRA rectification used to prove it was “not a theory of everything.” Defensive HB posture wired into Decompose.
3. **`schema.py` FRA ontology** still imported by the core: `ScaleResponseSubtype`, `PermissionSubtype`, `SOURCE_STATE_WARNING`, `REPRESENTATION_NOT_DERIVATION` (hardcoded Newtonian Poisson), `EvidenceLevel` through “replicated general physical theory,” `FORBIDDEN_CLAIM_PHRASES` whose threat model is still “confirms the SFE / validates UHF / prime structure is fundamental.”
4. **`classify.NAME_GUARD`** organized around `H,P,λ,Φ,φ,ψ` — correct hygiene, old symbol set as the center of the universe.
5. **Pattern order in `classify_parse`:** Laplacian → d’Alembertian → ODE. Gravity/wave first. That is HB example order, not a general classifier.
6. **`_assign_wave_like` always inserts symbol `"D"`** as `STATE_TRANSITION` even when `D` is not in the expression; leftover DHFA “evolution operator” slot.
7. **Prime lab still prime-centric** (`selectors.py`, `valid_for_physical_prime_test`). Not imported by decompose, but still a package-root module and a first-class test subject. Generalization did not happen.
8. **`registry.py` imports `historical.CANONICAL_SFE_STATUS`.** `app.py` and `cli.py` import `registry`. The dump test `test_core_modules_do_not_import_historical` **omits** `app.py`, `cli.py`, `registry.py`. Isolation is a loophole.
9. **Desktop Archive pane** is a peer tab of Decompose. Historical SFE IDs are one click from the product surface (`/api/archive` → `SFE-H001`).
10. **`realization.py` header** literally: “the one SFE *function* worth keeping.” That sentence is how a universal equation survives as a rename.
11. **Closed role enum** recreates a mandatory anatomy. The paper forbids a predetermined role count. Nine roles plus state/parameter/output is `P,H,ψ,λ,E` with extra synonyms.
12. **Test-locked `m = STATE_TRANSITION`.** UHF/DHFA extraction was supposed to put transition on `ẋ=F`. The live ontology puts it on mass. The dump extracted the *word* and assigned it to the wrong object.
13. **Repo-root `hb_ringdown_test.py`** still looks like a peer of DA tests.
14. **`OPERATIONAL-MATH.md` §3** claims the analog pair preserves “quadratic energy, passivity when coefficients are positive.” `translate.py` `preserved` list is `second_order_ode, linearity, time_invariance, causal_evolution`. Passivity is not checked. The note is leftover unification language (shared energy form ⇒ deep correspondence).

---

## 10. QStack / QNav audit

**Neither module exists in this repository.** Grep over `*.py, *.md, *.html, *.js` finds the names only in the rival `ARCHITECTURE-AUDIT.md`. I will not invent files to hold the names.

**Do not create `qstack.py` or `qnav.py`.**

Audit of *possible functions* under other names, because the spec asked for an audit, not a shrug:

| Historical name (not in tree) | Closest live code | Verdict |
|---|---|---|
| QStack as state/control stack | `dynamics.ControllerSpec` + `ValidationGate` + `EvidenceLevel` | Three different things. Validation/evidence is a **claim stack**. Control is PD. Residual is OLS. None is a stack datatype. If QStack later appears from another app, split it: do not assume one rename to “State Control.” |
| QStack as constraint/monitor | `np.clip` in `pd_control`; drag `mass ≤ mass_max` | Ad hoc. Not a monitor. |
| QNav as routing/classification | `classify.classify_parse` + `audit_expression` branches | **This is a router.** It routes every parse into `{elliptic_poisson, hyperbolic_wave, second_order_linear_ode, unclassified}`. That is the opposite of mathematical agnosticism: a captured HB router. If a future QNav appears, audit it as “which backend does this problem need?” The live function is already here and should be **demoted to a plugin registry**, not branded QNav. |

The rival said “leave QStack/QNav absent” and the human accepted. Correct as a **naming** decision. Incorrect as an **architecture** decision if it is used to avoid fixing `classify.py`. The routing layer is present, HB-shaped, and unnamed. Leaving the name absent while leaving the capture in place is how the assumption survives.

---

## 11. Proposed revised software architecture

The rival’s `core/ / math/ / mechanisms/ / domains/` tree is **folder theater**. It would have been the right proposal *before* the dump. After the dump, a folder move will be sold as the rewrite. Reject that.

DA should be a **protocol** (interfaces + a cycle state machine) plus **registered methods**. Verbs are not packages.

```
domain_architect/
  protocol/                 # the only required import surface
    types.py                # State, StateSpace, AdmissibleSet, Mechanism,
                            # Operator, Parameter, FunctionalSignature, RoleHypothesis
    architecture.py         # recursive Node; no padded levels; PARAMETER when a parameter exists
    correspondence.py       # Correspondence record; kinds include
                            # analogy | mathematical_correspondence | structure_preserving_equivalence
                            # (last is not awardable until a witness exists)
    compatibility.py        # DIRECT / TRANSFORMABLE / INCOMPATIBLE — see rule below
    synthesize.py           # refuses illegal maps; provenance fail-closed
    cycle.py                # state machine: the spec loop, including ITERATE
    provenance.py           # original_domain is a domain, not a symbol
    claims.py               # ValidationGate + claim filter only (not EvidenceLevel 0–6)
  classify/                 # optional plugins; default = UNRESOLVED
    registry.py             # pattern → classifier
    ode_lti.py              # first- and second-order as separate patterns
    elliptic.py
    hyperbolic.py
  methods/                  # established methods, named in user reports
    parse.py
    dimensions.py           # empty default env
    equation_error.py
    ivp.py                  # RK4
    pd.py
    identifiability.py
    projectors.py
  select/                   # optional; role = selection
    api.py                  # SelectionMechanism interface
    cutoff.py
    random.py
    energy.py
    prime.py                # optional row
    lab.py                  # equal-budget, subject = registered rows
    index_invariance.py     # generalized index_audit; no prime field names
  examples/
    firestone.py            # mechanical ↔ electrical as a regression test of stamps
    missing_damping.py
    inverse_pd.py
    poisson_periodic.py
    drag_surrogate.py
  historical/               # no import from protocol/ or classify/
    registry.py
    sfe_uhf_dhfa/
    hb_ringdown/
  app/                      # UX; archive is not a peer tab
```

### Object model (ordinary names)

```
State x ∈ StateSpace
AdmissibleSet ⊂ StateSpace              # selection / constraint
Dynamics : (x, u, t) → ẋ or x⁺          # the only thing called state_transition
OutcomeModel : Architecture → y         # not SFE; not a field equation
Controller : (x, x★, C) → u
Mechanism = (signature, operator, parameters)
Morphism T : Mechanism_B → Mechanism_B̃  # must be testable
Correspondence = (M_A, M_B, T?, preserved, broken, kind, checks[])
Candidate = (components, provenance[], gate)
Residual = y − ŷ  or  L̂[y_obs]
```

No field equation. No mandatory role count. **No prime in `protocol/`.** `is_prime` may appear only in `select/prime.py`.

### Compatibility rule (stricter than the dump *and* the rival)

The rival’s rule is still paperwork: “T.apply succeeds” is the dump’s current code. Replace it.

```
DIRECTLY COMPATIBLE
  iff typed ports match (unknown ⇒ not direct)
  and SI dimensions match (unknown ⇒ not direct)
  and every *required* invariant is checked-pass or explicitly waived
  and T is absent or the identity

TRANSFORMABLE
  iff a morphism T is supplied
  and T is not a bare name map unless a witness is attached
  and T(M_B) meets the DIRECT tests against M_A
  and at least one of {ports, SI, invariant} was broken before T
  and a witness is recorded: one of
        matching residual class after T,
        matching transfer-function poles after T,
        matching quadratic energy form after T,
        or an explicit waived-witness with reason

INCOMPATIBLE
  otherwise, including:
        same role word, no T
        T is a dict rename with no witness
        identity T used to dodge DIRECT
        unspecified domain/codomain
```

`STRUCTURE_PRESERVING_EQUIVALENCE` is **not** a software verdict until an intertwining / functor witness exists. **Keep the kind in the enum.** Do not award it. Deleting it (current dump) hides the paper’s distinction.

### Prime migration (explicit, not a mv)

```
select/prime.py          # optional mechanism, role=selection
select/lab.py            # compares registered selectors; prime is not the sentence subject
select/index_invariance.py
```

`classify/` may emit role `selection`. It may not import `is_prime`.  
`protocol/` may not import `select/`.  
If nobody needs selection on a problem, prime is not loaded. That is generalization. Relocating `selectors.py` under `mechanisms/selection/` while it still defaults budget to the prime count is **not**.

### What this proposal refuses

- Another dump that moves `CANONICAL_SFE_*` and adds a wrapper file.
- Inventing QStack or QNav modules.
- Keeping `Φ = ℱ(P,H,ψ,λ;E)` as a shim.
- Calling OLS on three regressors “mechanism discovery” in user-facing reports.
- Treating Firestone as evidence that translation *works*.
- Awarding COMPUTATIONAL on invented surrogates (drag is correctly MATHEMATICAL today; keep that honesty).
- Folder-first PRs.

---

## 12. Recommended accept / amend / reject — for the human, not a rewrite

The prior audit asked the human to accept ten items. The dump then “implemented” several of them as comments, aliases, and loophole tests. **Re-open those decisions.** Mark these:

| # | Item | Recommendation | Why |
|---|---|---|---|
| 1 | Isolate `historical/` so *product entry points* cannot import SFE/UHF/DHFA/HB | **AMEND** the previous accept | `app.py` / `cli.py` / `registry.py` still import `historical`. The dump test excludes those files. Isolation that omits the UI is theater. |
| 2 | Generalize selectors; prime becomes one optional `selection` mechanism **on a common interface, used when the role is selection** | **REJECT as done.** **ACCEPT as still required.** | Prime is still the lab’s subject. `SELECTION` is never assigned. Module is off the live path. |
| 3 | Generalize index audit; drop `valid_for_physical_prime_test` | **REJECT as done.** | Field still present; historical test still asserts it. |
| 4 | Either make `run_cycle` the only way demos run, or admit v1 is examples-only and demote `pipeline.py` | **AMEND** | A callback stub exists. Product cycles bypass it. Pick one: real state machine **or** examples-only README. Not both. |
| 5 | `T` is a tested morphism or the word `TRANSFORMABLE` is retired | **REJECT the dump’s “executable T.”** **ACCEPT the requirement.** | `apply` remaps keys. Vacuous T ⇒ correspondence. Identity T ⇒ incompatible. This is the most dangerous live bug. |
| 6 | Keep `structure_preserving_equivalence` as a **kind the software cannot award**; do not delete it | **REJECT the dump deletion.** | Paper requires the three-way distinction. Deleting the third kind is non-conformance. |
| 7 | Extract UHF/DHFA/SFE *functions* as `StateSpace` / `Dynamics` / `OutcomeModel` — never as renamed equations, never as `realization.py` comments | **REJECT as done.** | `m` is still `STATE_TRANSITION`. `realize_second_order` is RK4. No `StateSpace` type. |
| 8 | Do not create QStack/QNav modules | **ACCEPT** | Names are absent. **AMEND:** treat `classify.py` as the captured router that must be pluginized. |
| 9 | README sentence that Firestone / OLS / RK4 / PD are standard methods used *by* DA | **ACCEPT the sentence.** **REJECT sufficiency.** | Tests still treat demo success as DA success (`test_suite`, `COMPUTATIONAL` on OLS and PD). User reports must name the method first. |
| 10 | Unlock `test_second_order_roles` so `m` is not permanently a state transition | **ACCEPT (new)** | Ontology is frozen wrong. |
| 11 | Cut `audit.py → gravity.py` and Einstein/wave/abx branches from default decompose | **ACCEPT (new)** | Live HB special-cases. |
| 12 | Empty default `KNOWN_UNITS`; gravity units live in the Poisson example | **ACCEPT (new)** | Silent `c`/`k` collision. |
| 13 | Inverse design **fail-closed** unless the target is a recognized state/objective object | **ACCEPT (new)** | `"maximize profit"` must not emit a PD loop. |
| 14 | Generic translate must not emit a mapping from role-name join; emit `INCOMPATIBLE` / no-map | **ACCEPT (new)** | `k→G` is a loaded gun. |
| 15 | Folder-first rewrite (`core/math/mechanisms/…`) | **REJECT** | That is the rival’s leftover plan. It will be used to avoid §5 and §11 items 5, 10–14. |
| 16 | Pause *feature* work until 5, 10–14 are decided | **ACCEPT** | The last “pause until 1–6” produced a dump. Do not dump again. |

**Do not start the rewrite from this file.** If Jon wants a rewrite, he should mark the table. If he re-accepts the old 1–6 without 5 and 10–14, the next agent will polish the overclaim again.

---

## Appendix — executed facts this audit used (not README claims)

```
decompose("xd + a*x = u").pattern == "second_order_linear_ode"
inverse_design_architecture("maximize profit", ...)
  == inverse_design_architecture("x=1", ...)   # same components
translate(oscillator, Poisson) → {x:Phi, k:G, f:rho}  analogy
classify_compatibility(DISSIPATION vs FORCING, unknown types, T="magic")
  → TRANSFORMABLE + mathematical_correspondence
cycle_drag_reduction: pattern unclassified, translation None, provenance []
Provenance.original_domain == "R"   # symbol, not domain
KNOWN_UNITS["c"] == L/T; KNOWN_UNITS["k"] == 1/L
```

Rival brief stale vs this tree (so it is not copied): drag is no longer self-awarded `COMPUTATIONAL`; missing-damping now has a provenance record; `"unspecified"` domains no longer count as an interface match; `STRUCTURE_PRESERVING_EQUIVALENCE` is gone from the enum; `cycle.py` and `realization.py` now exist as objects. Those dump edits do not rescue the architecture. Several of them hide the paper’s requirements or replace a hole with a worse stamp.
