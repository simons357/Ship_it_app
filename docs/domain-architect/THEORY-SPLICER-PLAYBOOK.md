# Theory Splicer Playbook

Domain Architect (DA) is a **bullshit destroyer**, not a Millennium proof generator. This playbook maps CRISPR-inspired operations onto mathematical theory books — one theory at a time.

## Philosophy

| CRISPR | DA Theory Splicer |
| --- | --- |
| Cut DNA | **CUT** — remove a claim/role/term from a book |
| Insert gene | **INSERT** — add candidate completion at incompleteness gap |
| Splice chromosomes | **SPLICE** — join two books at a compatible weld |
| Knockout gene | **KNOCKOUT** — RETIRE a claim (gap_closure refuse semantics) |
| Screen library | **SCREEN** — audit all welds; report INCOMPATIBLE vs COMPATIBLE |
| Express protein | **EXPRESS** — reconstruct book from roles; check if inventory closes |

Every operation returns:

- `success` / `fail`
- `weld_id` (when applicable)
- `bullshit_flags`
- `suggested_fix`
- `bullshit_destroyed: true/false` and why

**Honesty rules (enforced in code):**

1. Any operation claiming **PROVED** for a Millennium problem without reconstruction pass → **refuse**
2. **SPLICE** only succeeds if compare/registry says `COMPATIBLE` or `COMPATIBLE_DISTINCT` with explicit weld lemma slot
3. DA does **NOT** prove Navier-Stokes, RH, Yang-Mills, or any Clay problem

## Settled inventory (repo truth)

| Item | Status |
| --- | --- |
| RH | NOT proved |
| Clay NS (Statement B) | NOT proved |
| Q6 arithmetic | KEEP — no RH claim |
| SFE canonical | UNRESOLVED |
| H→Clay glue | **REFUSED** by DA |

## Protocol: one theory at a time

1. **SCREEN** all welds in the problem book
2. **CUT** / **KNOCKOUT** illegal glue claims
3. **INSERT** honest candidate completions at open gaps
4. **SPLICE** only after weld audit passes
5. **EXPRESS** to verify reconstruction — still not a proof

Do not jump between problems until the current book's welds are honest.

---

## NS (Navier-Stokes) — full walkthrough

### Books in registry

| Book | Status | Role |
| --- | --- | --- |
| NS-B | REFERENCE | Classical PDE organizational book |
| SND-C | CONDITIONAL | Theorem H as written (X≤M) |
| SND-U | REFUSE | Claimed unconditional — RETIRE |
| CLAY-B | RETIRE | Millennium packaging — NOT resolved |
| BOOT-M | OPEN | Bootstrap M lemma candidate slot |
| SND-HYP | CONDITIONAL | NS + SND as hypothesis (KEEP) |
| SFE | RETIRE | No SFE→NS glue |

### Step 1: SCREEN NS welds

```bash
python3 -m domain_architect --splice-screen NS
```

Expect **INCOMPATIBLE** welds including:

- `W-NS-SNDC-CLAY` — SND-C assumes X≤M; Clay B needs M-free control (TH-H1)
- `W-NS-SNDC-SNDU` — conditional vs unconditional SND
- `W-NS-THMD-CLAY` — Clay⇔SND equivalence overclaim (TH-H2)
- `W-NS-SFE-NSB` — SFE→NS glue forbidden

### Step 2: CUT Theorem D Clay glue

```bash
python3 -m domain_architect --splice-cut SND-C THM-D-CLAY
```

Removes `Clay Statement B <=> [SND]` equivalence from the SND-C book DNA.

### Step 3: INSERT BOOT-M001 candidate

```bash
python3 -m domain_architect --splice-insert BOOT-M scale_response \
  "Lemma (Bootstrap-M): M=M(||u0||_{H^1}) with sup X(t)<=M on [0,T*)"
```

Open analytic slot — candidate de-circularization for Theorem H input.

### Step 4: Refuse illegal SPLICE SFE→NS

```bash
python3 -m domain_architect --splice-join SFE NS-B
```

Must **fail** with `bullshit_destroyed=true`. SFE prize-packaging ≠ classical NS.

### Step 5: Allow compatible SPLICE BOOT-M ↔ SND-C

```bash
python3 -m domain_architect --splice-join BOOT-M SND-C
```

`COMPATIBLE_DISTINCT` — requires explicit weld lemma; still does not close Clay B (TH-H3: c_* must drop M).

### Step 6: EXPRESS honest conditional book

```bash
python3 -m domain_architect --theory-express SND-C
python3 -m domain_architect --theory-express NS-B
```

Reconstruction inventory check only — **not** Clay Statement B resolution.

---

## RH / Q6 — skeleton walkthrough

### Books

| Book | Status | Notes |
| --- | --- | --- |
| RH-ROUTE-C | OPEN | Exploratory — no proof claim |
| Q6 | REFERENCE | Arithmetic KEEP — explicitly NOT RH |
| RH-MD | REFERENCE | Montgomery-Dyson archive |

### SCREEN RH welds

```bash
python3 -m domain_architect --splice-screen RH
```

### What splice Q6 → RH would require

```bash
python3 -m domain_architect --splice-join Q6 RH-ROUTE-C
```

**Withheld** (`INSUFFICIENT_INFORMATION`). A honest splice would need:

1. Explicit operator→zeta correspondence **lemma** (not prize glue)
2. No withdrawal of Q6 arithmetic KEEP status
3. No revival of Triple Lock / Bridge / inverse-GCD paths to NS or RH proof
4. Registry weld recorded before SPLICE succeeds

### Illegal cross-prize glue Q6 → NS

```bash
python3 -m domain_architect --splice-join Q6 NS-B
```

**Refused** — withdrawn Triple Lock / Q6→NS glue. Arithmetic operator ≠ fluids NS.

---

## Template: remaining Clay problems

For **Yang-Mills**, **P vs NP**, **BSD**, **Hodge**:

1. Add book stubs to `data/domain_architect/millennium_books.json`
2. SCREEN welds (initially empty)
3. INSERT candidates only from repo content — no invented physics
4. REFUSE any PROVED language without reconstruction

**Poincaré** is `SOLVED_REFERENCE` — Perelman proof exists externally. DA marks REFERENCE only; no re-proof.

---

## Demo script

```bash
python3 scripts/da_theory_splicer_demo.py
```

Artifacts: `/opt/cursor/artifacts/da-theory-splicer/`

## CLI reference

```bash
python3 -m domain_architect --list-millennium
python3 -m domain_architect --splice-screen NS
python3 -m domain_architect --splice-cut BOOK CLAIM_ID
python3 -m domain_architect --splice-insert BOOK ROLE CANDIDATE
python3 -m domain_architect --splice-join BOOK_A BOOK_B
python3 -m domain_architect --theory-express BOOK
```

Add `--json` for machine-readable output.

---

## What DA is built for

Jonathan's framing: DA performs **math operations on theory DNA** — compare books, split theorems, detect incompleteness, refuse illegal glue, reconstruct inventory. It is the ultimate bullshit destroyer.

It is **not** built to close Millennium problems. When a weld is INCOMPATIBLE, DA says so and proposes an honest closure **move** — not a fake proof.
