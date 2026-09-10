# DA Gap Closure Playbook — shut the NS/SND/Theorem-H door

**Audience:** Jonathan R. Simons  
**Tool:** Domain Architect (`python3 -m domain_architect --gap-closure …`)  
**Companion verdict:** [`ARCHON-PANEL-ADVERSARIAL-VERDICT.md`](./ARCHON-PANEL-ADVERSARIAL-VERDICT.md)  
**Attack routes (analytic):** [`THEOREM-H-ATTACK-PLAN.md`](./THEOREM-H-ATTACK-PLAN.md)  
**Demo:** `scripts/da_ns_gap_closure_demo.py`

**Rule of this document:** every break is written as **Broken at X → close by Y**.  
No lead sentence is allowed to be “remains open.”

---

## One-sentence weld

**Broken weld:** manuscripts prove (SND-C) under \(X\le M\), then briefing language glues that object to unconditional SND / Clay Statement (B) — Domain Architect now marks that glue **INCOMPATIBLE** and prints a closure move.

---

## How DA locates the break (runtime)

```bash
# Refuse unconditional Clay glue
python3 -m domain_architect --gap-closure \
  'Broken glue claim: Theorem H (X<=M) implies unconditional SND and Clay Statement B'

# Dual: SND-C (conditional) vs SND-U (claimed unconditional)
python3 -m domain_architect --snd-dual

# Ranked closures
python3 -m domain_architect --list-closures

# Registry conflicts
python3 -m domain_architect --registry
```

Exit code **2** means DA refused unconditional Clay / SND-U routing.

---

## Break cards (each weld DA finds)

### TH-H1 — \(X\le M\) circularity weld

| Field | Content |
| --- | --- |
| Break ID | TH-H1 |
| Where (DA) | INCOMPATIBLE books: `SND-C001` / `THM-H001` glued to `SND-U001` / `CLAY-B001`; gap router severity=`refuse` |
| Where (math) | Theorem H hypotheses: \(X\ge\delta_*\), \(X\le M\), \(\rho\le\rho_0\) → \(C_*=C_*(\ldots,M,\ldots)\) |
| Why | Clay (B) needs an \(H^1\) bound from data alone; feeding \(X\le M\) into the keystone smuggles the conclusion. |
| **Closure move** | Split theorems: publish H strictly as (SND-C \| \(X\le M\)); forbid auto-route H→Clay-B until an M-free lemma exists |
| Patch sketch | Replace “H ⇒ Clay B” by (i) H: \((X\le M,\rho\le\rho_0)\Rightarrow\)SND-C; (ii) produce \(M=M(\|u_0\|_{H^1})\) or remove \(M\) from \(C_*\) |
| Success test | CLI `--gap-closure` on glue claim exits 2; registry keeps `SND-C001`↔`CLAY-B001` INCOMPATIBLE; no green “Clay B resolved” |
| Fake-closure risk | Renaming “unconditionally under the definition” as unconditional SND — same circular \(M\) |

**Headline:** Broken at TH-H1 → close by splitting H from Clay-B and forbidding the glue.

---

### TH-H3 — Theorem G still carries \(M\) into \(c_*\)

| Field | Content |
| --- | --- |
| Break ID | TH-H3 |
| Where (DA) | SND-C→SND arrow incomplete: `c_*` annotated M-dependent; refuse when paired with SND-U/Clay markers |
| Where (math) | Theorem G: (SND-C)⇒[SND] with \(c_*=c_*(\nu,\delta_*,M,C_S)\) |
| Why | Even the spectral-gap conclusion still depends on the enstrophy ceiling. |
| **Closure move** | Remove \(M\) from \(c_*\): universal floor \(c_*(\nu,\delta_*)\) or derive \(M\) from \(\|u_0\|_{H^1}\) only |
| Patch sketch | \(\exists\,c_*>0\) depending only on \((\nu,\delta_*,\mathrm{geometry})\) with \(J/X\ge c_*\) without feeding \(M\) back |
| Success test | Dual SND-C vs SND-U no longer needs \(M\) on the U side; incompleteness drops M-dependent candidate |
| Fake-closure risk | Absorbing \(M\) into “universal” constants that still scale with data size |

**Headline:** Broken at TH-H3 → close by an M-free \(c_*\).

---

### TH-H4 — Dominant-shell propagation not Clay-grade

| Field | Content |
| --- | --- |
| Break ID | TH-H4 |
| Where (DA) | Propagation extra missing under unaugmented NS-B; warn when dominant-shell + \(X\le M\) + Clay markers co-occur |
| Where (math) | Theorem G proof: \(\dot\rho>0\) when \(\rho\) small, assuming SND-C + \(M\) |
| Why | Propagation is a conditional ODE under a priori bounds, not all-data dynamics. |
| **Closure move** | Propagate dominant shell for Leray–Hopf data without SND-C circular input |
| Patch sketch | Differential inequality on \(\rho\) using only identities available for Leray–Hopf weak solutions |
| Success test | Reconstruction extras include `dominant_shell_propagation_proved` without \(X\le M\) marker |
| Fake-closure risk | Proving propagation only inside the spread regime already conditioned on \(M\) |

**Headline:** Broken at TH-H4 → close by M-free dominant-shell persistence.

---

### TH-H7-Q1 — SND does not free-ride the Q1 limit

| Field | Content |
| --- | --- |
| Break ID | TH-H7-Q1 |
| Where (DA) | `NS-Q1001` INCOMPATIBLE with `CLAY-B001` / `SND-U001`; refuse Q1+Clay claims |
| Where (math) | Q1→Leray–Hopf: uniform SND / \(H^1\) through \(\varepsilon\to 0\) |
| Why | Approximants may hold SND while the weak limit silently loses it. |
| **Closure move** | Pass SND through the Q1 limit: \(\varepsilon\)-uniform \(J/X\ge c_*\) and honest liminf |
| Patch sketch | Prove \(\liminf_{\varepsilon\to 0}\rho_\varepsilon(t)\ge c_*\) without assuming smoothness of the limit |
| Success test | Incompleteness lists `snd_limit_passage`; audits refuse Clay glue via Q1 alone |
| Fake-closure risk | Using smooth approximant SND as if it were the weak-limit law |

**Headline:** Broken at TH-H7-Q1 → close by proving SND liminf as \(\varepsilon\to 0\).

---

### TH-H2 — Naming fraud / status-table green

| Field | Content |
| --- | --- |
| Break ID | TH-H2 |
| Where (DA) | `CLAY-B001` and `SND-U001` dispositions **RETIRE**; standalone unconditional claims refused |
| Where (math) | `20405526` status table vs SND-C definition with \(C_*(\ldots,M,\ldots)\) |
| Why | “Unconditionally under hypotheses” ≠ SND for all \(H^1\) data. |
| **Closure move** | Park Statement-B packaging; keep Zenodo KEEP conditional SND; force RETIRE on Clay-B001 |
| Patch sketch | Public text: “Ring + SND hypothesis / conditional only”; delete Clay-B greens |
| Success test | Registry RETIRE + conflict table; CLI refuses unconditional claim language |
| Fake-closure risk | Keeping the green table with an unread footnote |

**Headline:** Broken at TH-H2 → close by retiring Clay packaging and keeping SND-as-hypothesis.

---

## Ranked top 5 closure ideas (by tractability)

| Rank | Kind | Break | Closure move |
| --- | --- | --- | --- |
| 1 | **structural** | TH-H1 | Split theorems; forbid illegal H→Clay glue in DA/registry |
| 2 | **analytic** | TH-H3 | Remove \(M\) from \(c_*\) (or produce \(M\) from \(\|u_0\|_{H^1}\)) |
| 3 | **analytic** | TH-H4 | Propagate dominant shell without circular SND-C input |
| 4 | **analytic** | TH-H7-Q1 | Pass SND through Q1 \(\varepsilon\to 0\) limit |
| 5 | **structural** | TH-H2 | Retire Clay-B / SND-U packaging; KEEP conditional framing |

At least one structural fix is already **implemented in DA** (rank 1 + registry conflicts + `--gap-closure` refuse path). Analytic ranks 2–4 are the math doors to shut next.

---

## What “closed” looks like in DA

1. Glue claim string → exit code 2 + `Broken weld: … Suggested closure: …`
2. `--snd-dual` → relation `INCOMPATIBLE` between SND-C and SND-U
3. `--registry` shows `CLAY-B001` / `SND-U001` as **RETIRE**
4. Classical NS-B and SND-HYP audits do **not** refuse (honest books stay usable)
5. Incompleteness candidates include `gap_closure_weld` entries pointing at the fix

---

## Explicit non-goals

- DA does not prove Clay Statement (B).
- DA does not invent an M-free analytic estimate.
- DA **does** stop the illegal glue and tell you which door to shut first.
