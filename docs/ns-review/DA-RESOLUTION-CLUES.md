# DA Resolution Clues — Actionable Only

**Date:** 2026-08-27  
**Scope:** What DA says to **add** or **split** — not sympathy, not "everything open."

Artifacts: `/opt/cursor/artifacts/da-full-resolution/incompleteness-key.json`, `gap-closure-all.json`

---

## Clue 1 — Split theorem structure (STRUCTURAL — DA validates)

**Broken joint:** Briefing glues Theorem H (SND-C | X≤M) → Clay B / SND-U.

**DA says:** Publish two explicit arrows:

1. **Theorem H (kept):** `(X≥δ_*, X≤M, ρ≤ρ₀) ⇒ SND-C` with `C_*=C_*(ν,δ_*,M,ρ₀,C_S)`.
2. **Closure target (open):** Either remove M from C_*/c_*, or derive M from data before invoking H.

**Registry fix applied:** `THM-H001` ↔ `CLAY-B001` INCOMPATIBLE; `--gap-closure` refuses glue (exit 2).

**Honesty:** Split alone does **not** close Clay B. It stops the naming fraud.

---

## Clue 2 — Bootstrap lemma at role λ / E (ANALYTIC — candidate completion)

**Broken joint:** X≤M is assumed **inside** the keystone, smuggling the H¹ bound Clay must produce.

**DA says add at role `scale_response` + `environment`:**

> **Lemma (Bootstrap-M)** *(OPEN — registry `BOOT-M001`)*  
> For suitable H¹ divergence-free u₀ on T³, ∃ M = M(‖u₀‖_{H¹}, ν, geometry) such that  
> `sup_{t∈[0,T)} X(t) ≤ M`  
> using only energy/enstrophy identities available to Leray–Hopf solutions — **without** assuming smoothness or regularity.

**Then:** Feed Theorem H with **derived** M, not assumed M.

**DA incompleteness candidate (bootstrap string):**
```
Broken weld: Bootstrap M from H¹ data is the candidate slot to de-circularize Theorem H input — still open
Suggested closure: Prove bootstrap lemma: ∃ M=M(||u₀‖_{H¹}) with X(t)≤M on [0,T*)
```

**Success test:** `BOOT-M001` ↔ `SND-C001` COMPATIBLE_DISTINCT; H→Clay **still refused** until c_* drops M (TH-H3).

**Fake closure:** Using smooth Q1 approximant enstrophy as Leray–Hopf a priori bound.

---

## Clue 3 — Q1 limit-passing route (ANALYTIC — structurally aligned)

**Broken joint:** Q1 holds SND for ε>0; limit may silently lose it.

**DA compare:** NS-B vs Q1 shares **all 6 organizational roles** (admissibility, interaction, state, scale_response, realized_output, environment).

**DA says add at book `NS-Q1` extra `snd_limit_passage`:**

> **Lemma (SND liminf)** *(OPEN — TH-H7-Q1)*  
> For Q1 approximants u_ε with ε-uniform `J_ε/X_ε ≥ c_* > 0`, prove  
> `liminf_{ε→0} ρ_ε(t) ≥ c_*`  
> for the Leray–Hopf limit u, without assuming smoothness of the limit.

**Incompleteness flags:** Q1 book missing extra `snd_limit_passage (not established)`.

**Fake closure:** Identifying smooth approximant SND with weak-limit law.

---

## Clue 4 — M-free c_* after SND-C (ANALYTIC — Theorem G weld)

**Broken joint:** Theorem G: (SND-C) ⇒ [SND] with `c_* = c_*(ν,δ_*,M,C_S)` — M still in the conclusion.

**DA says at role `realized_output` (Φ ≈ spectral gap signal):**

> **Target:** ∃ c_* > 0 depending only on (ν, δ_*, geometry) such that J/X ≥ c_* whenever SND-C hypotheses hold — **without** M in c_*.

**Registry note:** Even with Bootstrap-M, this slot remains open until proved.

---

## Clue 5 — Dominant-shell propagation (ANALYTIC — Theorem G ODE)

**Broken joint:** ρ̇>0 argument assumes SND-C + M already.

**DA says add reconstruction extra:**

> `dominant_shell_propagation_proved` — differential inequality on ρ using only Leray–Hopf identities, no X≤M in the inequality input.

**Book:** NS-B + spectral extras; not Ring-BVB alone.

---

## Forbidden completions (DA refuses)

| Claim | Break ID | Action |
| --- | --- | --- |
| Ring+BVB ⇒ Clay B | TH-H6 | Keep toolkit; forbid rescue routing |
| c\*=6/π² ⇒ fluids SND | TH-H5 | Arithmetic only; `CSTAR-ARITH001` RETIRE |
| SFE ⇒ NS | registry | INCOMPATIBLE; no glue |
| H (X≤M) ⇒ Clay B | TH-H1 | Split; refuse |
| Q1 alone ⇒ Clay | TH-H7-Q1 | Need liminf lemma |

---

## Lemma template DA can audit (copy-paste)

```text
Theorem H-split (conditional, valid):
  Hypotheses: X≥δ_*, X≤M, ρ≤ρ₀
  Conclusion: |Π_{j*}| ≤ C_*(ν,δ_*,M,ρ₀,C_S)  [SND-C]

Bootstrap-M (open slot BOOT-M001):
  From u₀∈H¹ div-free, derive M=M(‖u₀‖_{H¹},ν) with X(t)≤M on [0,T*)
  without circular regularity.

SND-liminf-Q1 (open slot TH-H7-Q1):
  ε-uniform J/X≥c_* ⇒ liminf_{ε→0} ρ_ε≥c_* for Leray–Hopf limit.

M-free-cstar (open slot TH-H3):
  Remove M from c_* in Theorem G conclusion.

Clay-B: NOT claimed until SND-U + clean SND⇒regularity arrow, no hidden X≤M.
```

---

## Commands to verify clues

```bash
python3 -m domain_architect --gap-closure \
  'Bootstrap lemma OPEN: M = M(||u0||_{H^1}) s.t. X(t)<=M without circular input to Theorem H SND-C'

python3 -m domain_architect --compare \
  'partial_t omega = (omega * nabla) u + nu Delta omega' \
  'Q1 hyperdissipative: partial_t u + (u·nabla)u = -grad p + nu Delta u - epsilon (-Delta)^{1+delta} u; claim SND passes as epsilon->0'

python3 -m domain_architect --gap-closure \
  'Ring Lemma + BVB on E_c implies Clay Statement B resolved'

python3 -m domain_architect --incompleteness-json \
  'SND-C (conditional): under X<=M, rho=J/X<=rho_0, X>=delta_*: |Pi_{j*}| <= C_*(nu,delta_*,M,rho_0) in spread regime'
```
