# Grok rigor handoff — Domain Architect five-finger router

**For:** Grok (adversarial architecture / rigor review)  
**From:** Jonathan’s Domain Architect track (PR #28)  
**Repo:** `simons357/Ship_it_app`  
**Branch:** `cursor/ns-b-five-finger-router-0cc5`  
**PR:** https://github.com/simons357/Ship_it_app/pull/28  
**Tests:** **65** collected (`python3 -m unittest discover -s tests -p 'test_*.py'`)  
**Tone of this note:** architecture first, claims later. Please attack.

This document is a pasteable working note. It is **not** a Theory of Everything, a Clay/Millennium argument, or a Cursor-product identity claim. The software under review is **Domain Architect** (Functional Role Analysis). Informal nicknames (“five fingers,” “DMA”) are historical; the **canonical role set** is Domain Architect / Functional Role Analysis.

---

## 0. What you are being asked to do

Review the **operator / decomposition framework** for rigor:

1. Are role mappings invertible where the code claims closure?
2. Are there hidden assumptions, dimensional holes, or notation-only “decompositions”?
3. Does the workflow honestly refuse overclaim (Clay, hybrid SFE, prime-`P`, `λ_min` bake-in)?

Explicit invite: **attack invalid mappings, hidden assumptions, dimensional holes, noninvertible steps, and notation-only decompositions.** Snapshots (terminal evidence) are linked in §8.

---

## 1. What changed vs old HB

| Old HB reading (risk) | This branch |
|---|---|
| Grammar read as new physical law | Grammar is an **organizational** operator / decomposition framework |
| Informal anatomy metaphors | Prefer: functional role, independently specifiable component, role audit |
| Hidden extras | Declare `E` (geometry, BC, sources, …) instead of smuggling them |
| “Solve” implied by mapping | Loop is **map → reconstruct (inventory) → compare → controls**; solve/discover are later stages with protocol freeze |
| Single merged SFE story | Historical SFE candidates stay archived; status **unresolved**; dual-compare **forbids hybrid** |

Organizing grammar (organizational, not a universal law):

\[
\Phi = \mathcal{F}(P, H, \psi, \lambda; E)
\]

Core roles: admissibility \(P\), interaction/coupling \(H\), state \(\psi\), scale response \(\lambda\), realized output \(\Phi\). Extension roles live in \(E\). The framework does **not** claim every equation has exactly five parts.

---

## 2. Canonical naming (avoid identity confusion)

| Use | Do not treat as |
|---|---|
| **Domain Architect** | Cursor identity / chat persona |
| **Functional Role Analysis (FRA)** | A completed unification |
| **Five fingers** | Physical law; treat as historical nickname for the core role set |
| **DMA** | Separate product; alias for Domain Architect in older notes |

Canonical SFE status string everywhere: **`unresolved`**.

---

## 3. Workflow (architecture)

```
INPUT expression
  → DECOMPOSE / PARSE (AST; no name-only role inference)
  → ASSIGN ROLES (domain book when matched: gravity-poisson or NS-B)
  → RECONSTRUCT (inventory / recombination check — not a PDE solve)
  → COMPARE (unlike books side-by-side; shared letters ≠ shared physics)
  → CONTROLS (tuning export: free dials vs locked structural constraints)
  → (optional) incompleteness candidates from frozen book templates
  → (optional) drill-down module tree + recompose
  → (optional) dual-SFE compare (no hybrid synthesis)
```

Reconstruction answer format is inventory language: required roles present / missing; recomposed summary. It does **not** prove regularity or derive NS from an SFE.

---

## 4. Notation that must stay distinguished

| Symbol | Meaning in FRA | Collision to refuse |
|---|---|---|
| \(P\) | admissibility / permission / projector | **not** “prime” |
| \(p\) | integer or prime (or pressure/momentum if declared) | do not auto-upgrade to \(P\) |
| \(\mathbb{P}\) | set of primes | not the FRA projector |
| \(P = I\) | identity admissibility | **recovers Newtonian gravity** on the Poisson book (representation recovery) |
| \(\lambda\) | scale-response **role**; subtype required | never silently bake \(\lambda_{\min}(Q_N)>-1/2\) into classical NS |
| \(\Phi\) | realized output | not swirl \(\Gamma=ru_\theta\) without alias |

See also: `docs/domain-architect/04-NOTATION-COLLISIONS.md`.

---

## 5. Non-claims (software stance)

| Topic | Stance |
|---|---|
| **NS Track B** | Organizational book only for classical unaugmented NS |
| **Clay / Millennium** | Out of scope; no regularity claim |
| **\(\lambda_{\min}\) bake-in** | Forbidden on NS-B |
| **\(P\) = prime** | Forbidden; primes stay experimental / selector lab |
| **Canonical SFE** | Unresolved; discovering “no single canonical SFE” is valid |
| **Dual SFE** | Compare only; **hybrid synthesis forbidden** |
| **Incompleteness “candidates”** | Frozen **book templates**, labeled heuristic — not new physics |

---

## 6. Where the code lives

| Module | Role |
|---|---|
| `domain_architect/navier_stokes.py` | Classical NS-B five-finger auto-router (organizational) |
| `domain_architect/hb_loop.py` | Map / reconstruct / compare helpers |
| `domain_architect/incompleteness.py` | Gap report + book-template candidates; roles → sketch |
| `domain_architect/decompose.py` | Drill-down module tree + recompose checks |
| `domain_architect/tuning_export.py` | Control-variable / bridge-style dial export |
| `domain_architect/sfe_compare.py` | Dual-SFE / dual-expression audit; no hybrid |
| `domain_architect/cli.py` | CLI entry (`python3 -m domain_architect …`) |
| `domain_architect/audit.py` | Auto-route into domain books + report assembly |
| `domain_architect/gravity.py` | Poisson book; \(P=I\) Newtonian recovery path |
| `data/domain_architect/*.json` | Historical equations, conflicts, null results |

Supporting docs in this folder: `00`–`06`, `OVERNIGHT-DEMO.md`, `GROK-ATTACK-CHECKLIST.md`.

---

## 7. How to run demos

```bash
cd /workspace

# One-shot overnight honest loop
python3 scripts/overnight_honest_loop_demo.py

# Gravity Poisson book
python3 -m domain_architect "nabla^2 Phi = 4 pi G rho"

# Classical NS-B (full vorticity form)
python3 -m domain_architect \
  "partial_t omega = (omega * nabla) u + nu Delta omega"

# Unlike-book compare
python3 -m domain_architect --compare \
  "partial_t omega = (omega * nabla) u + nu Delta omega" \
  "nabla^2 Phi = 4 pi G rho"

# Thin NS → incompleteness (expect missing advection / incompressibility)
python3 -m domain_architect --incompleteness-json \
  "partial_t omega = nu Delta omega"

# Drill-down / recompose tree
python3 -m domain_architect --decompose-json \
  "partial_t omega = (omega * nabla) u + nu Delta omega"

# Tuning / control dials (bridge handoff sketch)
python3 -m domain_architect --tuning-json \
  "partial_t omega = (omega * nabla) u + nu Delta omega"

# Put SFE in twice (expect INCOMPATIBLE; no hybrid)
python3 -m domain_architect --list-sfe
python3 -m domain_architect --sfe-compare SFE-H001 SFE-H002

# Tests
python3 -m unittest discover -s tests -p 'test_*.py'
```

Copy-paste wake-up sheet: [`OVERNIGHT-DEMO.md`](OVERNIGHT-DEMO.md).

---

## 8. Snapshots for Grok (terminal evidence)

Overnight + refreshed CLI snapshots live under `/opt/cursor/artifacts/` on the agent environment (not committed to git). Prefer these for “see the output”:

| Artifact | What it shows |
|---|---|
| `grok_snap_gravity_audit.log` | Poisson book audit; \(P=I\) Newtonian recovery language |
| `grok_snap_ns_b_audit.log` | NS-B five-finger auto-map |
| `grok_snap_ns_vs_gravity.log` | Unlike-book structural compare |
| `grok_snap_ns_incompleteness.json` | Thin-NS gap + book-template candidates |
| `grok_snap_ns_decompose.json` | Drill-down tree + recompose flags |
| `grok_snap_ns_tuning.json` | Control dials vs locked constraints |
| `grok_snap_sfe_h001_vs_h002.log` | Dual-SFE `INCOMPATIBLE`; hybrid forbidden |
| `grok_snap_overnight_demo.log` | Full overnight script stdout |
| `grok_snap_unittest_verbose.log` | Unittest run |
| `grok_snap_test_count.txt` | `collected_tests=65` |
| `overnight_honest_loop_summary.json` | Machine summary of overnight loop |
| `overnight_demo_suite.log` / `overnight_honest_loop_demo.txt` | Prior overnight suite evidence |
| `sfe_put_in_twice_*.log` | Dual-SFE demos |
| `bridge_tuning_handoff_*.txt` | How old UIs would wire dials |
| `ns_decompose.json` / `ns_decompose_tree.mmd` | Drill-down + mermaid sketch |

If you only have the git tree (no `/opt/cursor/artifacts/`), regenerate with the commands in §7.

---

## 9. Suggested attack surface (summary)

Full bullet list: [`GROK-ATTACK-CHECKLIST.md`](GROK-ATTACK-CHECKLIST.md).

High-value targets:

- NS-B role map: is Leray-as-\(P\) forced correctly, or only by string match?
- Gravity recovery: does \(P=I\) actually recover Newtonian structure, or only print the slogan?
- Reconstruct “passed”: inventory closure vs true invertibility of the decomposition
- Compare: does shared `scale_response` falsely suggest physics transfer NS ↔ gravity?
- Incompleteness candidates: smuggled physics vs honest book templates?
- Dual-SFE: any path that could synthesize a hybrid?
- Dimensional / free-index checks: holes on typed roles?
- Stop rules in `decompose.py`: premature stop or infinite descent?

---

## 10. PR / provenance

- **PR #28:** https://github.com/simons357/Ship_it_app/pull/28  
- **Title:** Domain Architect: auto-map, reconstruct, compare, incompleteness, drill-down  
- **Test count at handoff:** 65  
- **Related frozen notes:** `00-AUDITED-BASELINE.md` … `05-RECTIFICATION.md`, `06-OVERNIGHT-HONEST-LOOP.md`

Please reply with: (a) architectural objections, (b) concrete counterexamples or failing inputs, (c) which claims you would strike from the software’s self-description.
