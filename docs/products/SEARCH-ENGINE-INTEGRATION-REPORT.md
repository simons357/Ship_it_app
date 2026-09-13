# Search Engine Integration Report

**For:** Jonathan Robert Simons (Prime Field Technologies LLC)  
**Prepared:** 2026-08-28  
**Repo audited:** `simons357/Ship_it_app` (branch `cursor/tao-snd-h-panel-a0eb`)  
**Purpose:** Hand this document to a Domain Architect (DA) or collaborator who will design, build, and wire a unified search / pattern-finding layer across all Prime Field products.

---

## Executive summary

Jonathan Simons operates a **multi-domain portfolio** spanning cryptography (Field Lock), maritime coatings (NAV-42), clinical anesthesia (Vigilant Patch), luxury product (AquaQuarts), developer tooling (Ship It), spectral math research (SND / Q6 / Bridge\*), expository brand (Harmonic Blueprint), and exploratory Base44 apps (Primefield Explorer, ExoRatio, Solenne, Maritime Dashboard). His stated philosophy treats **pattern-finding across domains** as core intellectual work: the same structural motifs (inverse-GCD lattice, critical-line weights \(n^{-1/2}\), spectral floors, concentration vs delocalization) recur in Navier–Stokes, Riemann Hypothesis analogies, black-hole ringdown, and anesthesia coherence.

**Critical finding from this audit:** There is **no deployed search engine** in the `Ship_it_app` repository or any checked git branch. No Elasticsearch, OpenSearch, Pinecone, Qdrant, ChromaDB, FAISS, Meilisearch, Typesense, or semantic-embedding pipeline exists here. What *does* exist is a **proto-search stack** made of:

1. **Machine indexes** — `docs/papers/zenodo-spectral/INDEX.json` (14 Zenodo records with DOI, title, files, keywords, descriptions).
2. **Verification spells** — Python scripts (`scripts/sfe_bh_overlay_spells.py`, `bridge_floor_verify.py`, etc.) that hunt cross-domain structural rhymes and emit JSON artifacts.
3. **Deep Analysis (DA) ledgers** — markdown reports (`docs/math/DA-REPORT-2026-08-28.md`) that classify claims as CLOSED / KILLED / LEAD / HARD.
4. **External product surfaces** — live Replit demos (Field Lock, NAV-42), Base44 explorers (SFE–RH, ExoRatio), GitHub repos (Ship It, Kyrana), and Zenodo DOIs — none wired to a shared index.

The **cosmos app** referenced in recent conversation context does **not appear anywhere** in this repo or its git history. Treat it as external (another repo, Base44 app, or planned work) until a URL or repo is supplied.

**Recommendation in one sentence:** Build a **Prime Field Pattern Index (PFPI)** — a shared metadata + full-text + optional vector layer — and embed thin search clients in each product, starting with the research corpus (Zenodo mirror + spells + DA ledger) and Ship It (GitHub dispatch), then Field Lock / NAV-42 partner docs, then clinical Vigilant content on a separate compliance partition.

---

## Current product inventory

### A. In this repo (`Ship_it_app`, current branch)

| Asset | Path / entry | Role | Search relevance |
| --- | --- | --- | --- |
| **Harmonic Blueprint Experiment 01** | `hb_ringdown_test.py`, `nodes.json`, `data/qnm_events.csv` | Closed null-test on GW ringdown vs node families | Frozen experiment; index node families + results for cross-ref |
| **Zenodo spectral mirror** | `docs/papers/zenodo-spectral/` + `INDEX.json` | Local copy of 14 DOIs | **Primary corpus** — already has machine index |
| **Math / audit docs** | `docs/math/*`, `docs/BRIDGE-*.md`, `docs/KEEP-CUT-INVENTORY.md` | Truth map, DA reports, spellbooks | High-value markdown to index with status tags |
| **Submit pack** | `docs/papers/submit/*.tex`, `*.pdf` | Tier-1 corrected papers for Zenodo | Source of truth for publishable claims |
| **Spells (pattern hunters)** | `scripts/sfe_bh_overlay_spells.py`, `sfe_phase_flow_spell.py`, `route_c_gap_a_verify.py`, etc. | Cross-domain correlation scripts | Executable “queries”; output JSON should be indexed |
| **Tests** | `tests/test_*.py` | Regression for spells + Bridge\* | CI artifacts, not user-facing search |
| **Ship It assets only** | `assets/shipit_*.png` | Branding | No app code on this branch |

**What this repo is NOT:** It is not Field Lock, NAV-42, Ship It (Next.js app), Vigilant clinical package, AquaQuarts, or cosmos app. The README describes HB Experiment 01, not a product catalog.

### B. Referenced externally (from `KEEP-CUT-INVENTORY.md`, portfolio branch `cursor/prime-field-portfolio-561a`)

#### Tier 1 — live or nearest to cash

| Product | URL / repo | Status (per inventory) | In repo? |
| --- | --- | --- | --- |
| **Field Lock** | https://field-lock.replit.app/ · https://primefield.tech/field-lock | Live kiosk; presence-bound keys; PUF/CTW spine | **No** — Replit |
| **Ship It** | https://github.com/simons357/ship-it-code · branch `cursor/ship-it-app-e279` has Next.js app | GitHub shipping tool for non-git users | **Partial** — assets here; app on other branch/repo |
| **NAV-42** | https://nav-42.replit.app/ | Coating demo; freeze false % drag claims | **No** — Replit |
| **Vigilant Patch** | (clinical lane; papers on other branches per `PUBLISHABLE-PAPERS.md`) | CRNA domain authority; FDA path before deep disclosure | **No** |
| **AquaQuarts** | (brochure branches: `cursor/aquaquartz-*`) | Luxury water; productizable without Clay | **No** |

#### Tier 2 — fix permissions or kill

| Product | URL | Issue |
| --- | --- | --- |
| **ExoRatio** | https://exo-ratio-014dea2d.base44.app/ | **CUT** — negative null audit |
| **Primefield Explorer / SFE–RH** | https://sfe-rh-explorer-v1-07f8121c.base44.app/ | Base44 permissions broken for strangers |
| **Solenne** | https://solenne.base44.app/ | AI beauty / telehealth |
| **Maritime Coherence Dashboard** | https://maritime-coherence-dashboard-100b68c0.base44.app/ | Maritime partner demo |
| **ChatVault** | https://primefield.tech/chatvault | Hollow public URL |
| **Kyrana** | https://github.com/simons357/kyrana-oracle | Small oracle app |
| **SpectraLock / FieldEncrypt** | Bundle under Field Lock | Same lane |
| **QStack** | https://primefield.tech/qstack | Code-only recipe; source TBD |

#### Tier 3 — brand / expository (not monetized via Millennium math)

| Asset | URL | Role |
| --- | --- | --- |
| **Prime Field Technologies** | https://primefield.tech/ | Company site |
| **Harmonic Blueprint book** | https://www.theharmonicblueprint.com/ | Expository brand (ISBN 9798289278081) |
| **Zenodo author corpus** | https://zenodo.org/search?q=creators.name%3A%22Simons%2C%20Jonathan%22 | 20+ preprints (many CUT from promotion per audit) |

#### Not found anywhere in git

| Name | Notes |
| --- | --- |
| **Cosmos app** | Zero matches in repo, all branches, or git history. Likely external or planned — **needs URL/repo from Jonathan**. |
| **UHF / DHFA** | Mentioned in `PAPER-01-ZENODO.md` as “do not touch” product lanes; no code here. |
| **FieldPredict Stocks/Sports** | Named in portfolio; no public URL |
| **NS_FINAL_MERGED_UNCONDITIONAL.tex** | Drive-only per `ARCHON-NS-FINAL-REVIEW-PANEL.md` |

---

## What “the search engine” likely is / should be

### What it is NOT (honest)

- Not a finished product in this repo.
- Not Clay/NS/RH “solved” retrieval — audit explicitly kills full-spectrum Bridge and prize packaging.
- Not ExoRatio (cut from catalog).
- Not a single Base44 app — explorers are siloed UIs without shared backend.

### What Jonathan’s philosophy implies

From conversation context and repo evidence, “the search engine” is really **three layers**:

#### Layer 1 — **Corpus search** (traditional)

Find documents, DOIs, scripts, product pages, partner one-pagers, clinical teaching notes, patent summaries, and Drive files by keyword, tag, domain, and date.

**Existing seed:** `docs/papers/zenodo-spectral/INDEX.json` — JSON array of records with `id`, `doi`, `title`, `date`, `creators`, `files[]`, `keywords`, `desc`.

#### Layer 2 — **Pattern / spell search** (domain-specific)

Find **structural rhymes** across NS, Q6, SFE, black holes, anesthesia:

- Same operator family? (\(\widetilde Q_N\), \(H_N\), \(Q^{\mathrm{raw}}\))
- Same critical weight? (\(n^{-1/2}\), \(s=\tfrac12\))
- Same spectral constant? (\(-1/2\) vs \(-1/(2\pi)\))
- Same concentration metric? (Herfindahl, SND shell fraction, BIS proxy)

**Existing seed:** `scripts/sfe_bh_overlay_spells.py` — builds profiles, Pearson-correlates against BH templates, writes `/opt/cursor/artifacts/sfe_bh_overlay_spells.json`. The spellbook (`docs/math/SFE-BH-OVERLAY-SPELLBOOK.md`) documents the ontology.

#### Layer 3 — **Truth / status search** (DA ledger)

Every claim tagged: **CLOSED**, **KILLED**, **LEAD**, **HARD**, **KEEP**, **CUT**, **COLD ARCHIVE**. Search must not surface KILLED claims as facts.

**Existing seed:** `docs/math/DA-REPORT-2026-08-28.md`, `docs/KEEP-CUT-INVENTORY.md`, `docs/math/CREDIT-LIST.md`.

### Proposed name and scope: **Prime Field Pattern Index (PFPI)**

A unified index that serves:

| Consumer | Query type | Example |
| --- | --- | --- |
| Jonathan / DA | “Show LEAD rhymes between Route C and SFE ground state” | Spell + ledger |
| Partner (Field Lock) | “Find NDA-safe crypto one-pagers, no Clay language” | Filtered corpus |
| Ship It user | “Find my shipped notes about NAV-42” | User-scoped full-text |
| Clinical collaborator | “Vigilant teaching on when BIS lags the room” | Partitioned clinical index |
| Math referee | “What is proved vs conditional for Bridge\*?” | DA status search |

### Gaps to flag for DA

| Gap | Severity |
| --- | --- |
| No embedding model or vector store chosen | High — needed for semantic “pattern” queries |
| No API gateway | High — each product is a separate URL today |
| No auth / tenancy model | High — clinical vs public vs NDA partitions |
| Cosmos app location unknown | Medium — cannot integrate until located |
| Drive files (`SND_FORMAL_PROOFS.tex`, etc.) not in repo | Medium — index must ingest from Google Drive or manual drop |
| Base44 apps have broken public permissions | Medium — fix or scrape offline copies |
| Replit apps (Field Lock, NAV-42) closed source here | Medium — index metadata + marketing copy only unless repos linked |
| No Notion integration in repo | Low — MCP available in Cursor environment but not wired to products |

---

## Integration architecture

### Target topology

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                        INGESTION (connectors)                            │
├──────────────┬──────────────┬──────────────┬──────────────┬──────────────┤
│ Zenodo API   │ GitHub repos │ Drive drop   │ Replit meta  │ Base44 export│
│ + local mirror│ Ship_it_app │ docs/papers/ │ field-lock   │ explorer JSON│
│ INDEX.json   │ kyrana, etc. │ Vigilant MD  │ nav-42       │              │
└──────┬───────┴──────┬───────┴──────┬───────┴──────┬───────┴──────┬───────┘
       │              │              │              │              │
       ▼              ▼              ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              NORMALIZE → tag(domain, status, product, doi)               │
│              CHUNK (papers, spells, one-pagers, issues)                  │
│              OPTIONAL: embed (text-embedding-3-small or local e5)        │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    PFPI CORE (pick one stack — see Technical options)    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ Full-text   │  │ Vector      │  │ Structured  │  │ Spell       │    │
│  │ (BM25)      │  │ (semantic)  │  │ (DOI, tags) │  │ registry    │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         PFPI API (REST + optional MCP)                   │
│  GET /search?q=&domain=&status=&product=                                 │
│  GET /patterns?template=inv_r_sqrt&source=sfe                            │
│  GET /ledger?status=LEAD                                                 │
│  POST /spells/run {name, args}  → queue + artifact URL                   │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
       ┌────────────────────────┼────────────────────────┐
       ▼                        ▼                        ▼
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│ Field Lock  │        │ Ship It     │        │ HB / Math   │
│ embed widget│        │ “find ship” │        │ spell panel │
│ partner docs│        │ history     │        │ DA dashboard│
└─────────────┘        └─────────────┘        └─────────────┘
       ▼                        ▼                        ▼
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│ NAV-42      │        │ Vigilant    │        │ Cosmos app  │
│ spec search │        │ clinical    │        │ (TBD)       │
└─────────────┘        └─────────────┘        └─────────────┘
```

### Shared schema (minimum viable document)

Every indexed object should carry:

```json
{
  "id": "zenodo:20405405",
  "title": "Phi-Renormalization Track B",
  "body_text": "...",
  "source_uri": "https://doi.org/10.5281/zenodo.20405405",
  "source_type": "zenodo|github|markdown|spell_artifact|product_page|clinical",
  "domains": ["NS", "fluids"],
  "products": [],
  "da_status": "CLOSED|KILLED|LEAD|HARD|null",
  "keep_cut": "KEEP|CUT|COLD|null",
  "operators": ["Phi-renorm", "Q1"],
  "keywords": ["axisymmetric", "swirl"],
  "file_paths": ["docs/papers/submit/01_phi_renormalization.tex"],
  "updated_at": "2026-08-28T00:00:00Z"
}
```

Extend with `pattern_tags` for spell layer: `["inv_r_sqrt", "lambda_min", "herfindahl", "bis_proxy"]`.

### API layer contract (embed in each product)

Thin clients call PFPI with:

1. **Product API key** (scopes: `public`, `partner`, `clinical`, `internal`).
2. **UI mode:** `inline` (3-result dropdown), `panel` (sidebar), `full` (dedicated search page).
3. **Hard filters:** e.g. Field Lock searches exclude `keep_cut:CUT` and `da_status:KILLED` unless `?include_archived=1`.

### Auth partitions

| Partition | Contents | Who sees it |
| --- | --- | --- |
| **public** | KEEP papers, HB experiment, Field Lock marketing, NAV-42 demo copy (no false drag %) | Internet |
| **partner** | NDA one-pagers, patent summaries, DIU vault index (not full claims) | Authenticated partners |
| **clinical** | Vigilant teaching drafts, CRNA scenarios | HIPAA-aware; separate index |
| **internal** | LEAD/HARD notes, spell raw output, Drive drops | Jonathan + DA |

---

## Per-product integration playbook

### 1. Field Lock (crypto / presence-bound keys)

**Current state:** Live at https://field-lock.replit.app/ — not in this repo.

**Search use cases:**
- Partner finds: “What is CTW spine?”, “NDA demo script”, “SpectraLock vs Field Lock bundle”
- Internal: cross-link to coherence / SFE language without surfacing Clay claims

**Integration steps:**
1. Index Field Lock marketing pages from `primefield.tech/field-lock` (scrape or manual MD).
2. Add `product:field-lock` tag to all crypto-related docs; **exclude** Triple Lock / Quantum Lens CUT papers from default partner search.
3. Embed PFPI widget in Replit app footer: “Search Prime Field docs” → filtered to `product:field-lock OR tag:encryption`.
4. Optional: index GitHub issues/PRs from Field Lock repo when linked.

**Do not:** Auto-suggest “Bridge floor proves security” — KILLED claim.

---

### 2. Ship It (GitHub dispatch tool)

**Current state:** Next.js app on branch `cursor/ship-it-app-e279` / repo `ship-it-code`. This branch has only branding assets.

**Search use cases:**
- “What did I ship about NAV-42 last month?”
- “Find help doc for complexity management” (`docs/operator-systems.md` on ship-it branch)
- Personal archivist: search shipped notes + linked repos

**Integration steps:**
1. Index `docs/HELP.md`, `docs/operator-systems.md`, `docs/complexity-management.md` from ship-it branch.
2. On `/ship` flow, add optional “Attach from Prime Field index” — search PFPI, paste link into ship note.
3. Post-ship webhook: new GitHub issue/commit message → PFPI ingests as `source_type:ship_it_dispatch` with user id.
4. Operator-systems alignment: Ship It’s “determine state → fast loop → emergency mode” maps to PFPI’s `status` filters (surface HARD items in “emergency mode” UI skin).

---

### 3. NAV-42 (maritime coating)

**Current state:** https://nav-42.replit.app/ — provisional IP; **freeze false drag claims** per inventory.

**Search use cases:**
- Metered pilot documentation, coating spec sheets, honest drag audit (`NAV42-DRAG-TRUTH.md` referenced but **not in this repo** — ingest when found)
- Cross-link Phi-renorm / turbulence papers for technical partners (without % improvement claims)

**Integration steps:**
1. Index NAV-42 demo copy + patent-pending notices from portfolio packet.
2. Hard-coded search suppressions: queries matching “% drag reduction” return `KEEP-CUT-INVENTORY` warning card first.
3. Tag maritime dashboard (`maritime-coherence-dashboard` Base44) entries with `product:nav-42`.

---

### 4. Vigilant Patch / clinical lane

**Current state:** Papers “on other branches” (`PUBLISHABLE-PAPERS.md §6`). Anesthesia ↔ SFE mapping exists only in CUT Quantum Lens tex and spellbook **lead** (BIS proxy spell — not proved).

**Search use cases:**
- “When the number lags the room” teaching scenarios
- Crisis checklist content
- FDA/regulatory path docs (before deep disclosure)

**Integration steps:**
1. Create **clinical partition** — separate index collection, no commingling with Zenodo MP drafts in default results.
2. Index Vigilant markdown from anesthesia branches when merged.
3. **Do not** index Quantum Lens anesthesia paragraphs as clinical fact — mark `da_status:KILLED` or exclude.
4. Optional spell: `anesthesia_ipr_spell` (inverse participation ratio vs SFE ground state) — internal LEAD only.

---

### 5. AquaQuarts

**Current state:** Brochure branches only (`cursor/aquaquartz-*`).

**Integration steps:**
1. Index brochure HTML/PDF from those branches.
2. Product tag `aquaquarts`; no math corpus in default search.
3. Partner search: luxury / tableside / partnership keywords only.

---

### 6. Math / research corpus (this repo — highest readiness)

**Current state:** Rich local mirror + spells + DA ledger.

**Integration steps (Tier 1 quick win):**
1. **Bulk ingest** `docs/papers/zenodo-spectral/INDEX.json` + all `.tex` / `.md` under `docs/`.
2. Parse DA tables from `DA-REPORT-2026-08-28.md` into structured `ledger.json`.
3. Register spells in `spell_registry.json`:

   | Spell name | Script | Output artifact |
   | --- | --- | --- |
   | `sfe_bh_overlay` | `scripts/sfe_bh_overlay_spells.py` | `sfe_bh_overlay_spells.json` |
   | `sfe_phase_flow` | `scripts/sfe_phase_flow_spell.py` | stdout / artifact |
   | `route_c_gap_a` | `scripts/route_c_gap_a_verify.py` | txt artifact |
   | `bridge_floor` | `scripts/bridge_floor_verify.py` | stdout |
   | `hb_ringdown` | `hb_ringdown_test.py` | `results/*.json` |

4. Expose `GET /patterns/correlate?template=inv_r_sqrt` returning latest spell artifacts.
5. Build static “DA Dashboard” page querying PFPI for `status=LEAD`.

**Honesty filters:** Any result from CUT papers (Triple Lock `20552400`, three-in-one `20552171`) must show red **CUT — do not cite as proof** banner.

---

### 7. Cosmos app

**Current state:** **Unknown — not in repository.**

**Integration steps (blocked until located):**
1. Jonathan supplies repo URL or Base44/Replit link.
2. Determine if cosmos app is: (a) another explorer UI, (b) unified dashboard, or (c) mobile shell — architecture fork depends on this.
3. If cosmos app = “unified dashboard”, make it the **primary PFPI full UI**; other products embed widgets only.
4. If cosmos app = experiment results viewer, index its result JSON into PFPI with `product:cosmos`.

**Placeholder recommendation:** Treat cosmos as the **PFPI full-search frontend** until defined otherwise.

---

### 8. Zenodo / GitHub public corpus

**Zenodo:** 14 records mirrored; author search returns more. Ingestion via Zenodo REST API (`https://zenodo.org/api/records/{id}`) — meta.json files already cache API shape.

**GitHub:** `simons357/Ship_it_app`, `simons357/ship-it-code`, `simons357/kyrana-oracle`. Index README + docs + issue titles.

**Integration steps:**
1. Nightly job: diff Zenodo author records vs local `INDEX.json`; fetch new versions.
2. Map DOI → `keep_cut` status using table from `KEEP-CUT-INVENTORY.md`.
3. GitHub webhook on push to `docs/**` → re-chunk changed files.

---

### 9. Harmonic Blueprint (book + experiment)

**Book:** https://www.theharmonicblueprint.com/ — expository, not proof.

**Experiment:** Closed null (`HB-RINGDOWN-EXPERIMENT-01-REPORT.md`).

**Integration:**
- Index book site + experiment protocol/report.
- Tag `hypothesis:prime|fibonacci|golden` from `nodes.json` families for pattern search cross-ref with spells.
- Search result snippet must say: “HB Experiment 01 did not reject H0 on held-out TEST.”

---

### 10. Base44 explorers (Primefield Explorer, Solenne, Maritime)

**Current state:** Permission broken for strangers; ExoRatio CUT.

**Integration:**
1. Fix Base44 sharing **or** export static JSON/screenshots into PFPI.
2. Index SFE–RH explorer as `domain:RH, Q6` visualization metadata.
3. **Exclude ExoRatio** from default index (`keep_cut:CUT`).

---

### 11. Kyrana (oracle)

**Repo:** https://github.com/simons357/kyrana-oracle

**Integration:** Kyrana becomes a **natural-language front-end** to PFPI — “Answer · Why it matters · Next steps” maps to search result + DA status + suggested spell. Wire Kyrana to `POST /search` instead of hard-coded responses.

---

### 12. ChatVault

**Current state:** Hollow URL.

**Integration (if revived):** ChatVault conversations become **first-class index sources** with `source_type:chatvault`. PFPI provides retrieval for “what did I ask Claude about Bridge\*?” — high synergy with Jonathan’s workflow.

---

## Data sources to index

### Priority 1 — already in repo

| Source | Path | Est. docs | Notes |
| --- | --- | ---: | --- |
| Zenodo mirror index | `docs/papers/zenodo-spectral/INDEX.json` | 14 records | Machine-ready |
| TeX / PDF submit pack | `docs/papers/submit/` | ~10 papers | Tier-1 truth |
| Math / audit markdown | `docs/math/`, `docs/*.md` | ~30 files | Include DA tags |
| Spell scripts + tests | `scripts/`, `tests/` | 7 scripts | Index docstrings + registry |
| HB experiment | `docs/HB-RINGDOWN-*`, `results/` | 5+ files | Closed null |
| nodes.json | `nodes.json` | 1 | Frozen node families |

### Priority 2 — other git branches

| Source | Branch | Notes |
| --- | --- | --- |
| Partner inventory | `cursor/prime-field-portfolio-561a` | `partner-packet/INVENTORY.md` |
| Ship It help / operator docs | `cursor/ship-it-app-e279` | Product UX copy |
| AquaQuarts brochures | `cursor/aquaquartz-*` | Marketing |

### Priority 3 — external (manual connector)

| Source | Location | Blocker |
| --- | --- | --- |
| Google Drive tex | `SND_FORMAL_PROOFS.tex`, `NS_FINAL_MERGED_UNCONDITIONAL.tex`, `threshold_SND_final.tex` | Not in VM — drop into `docs/papers/` |
| Replit source | Field Lock, NAV-42 | Need repo export or scrape |
| Base44 apps | Multiple URLs | Fix permissions or export |
| Notion workspace | MCP available in Cursor | Not wired; optional |
| Patent filings | NAV-42 provisional, HoloBase, ProVR | NDA partition only |
| Clinical Vigilant package | Other branches | HIPAA review |
| Cosmos app | Unknown | **Needs URL** |
| `NAV42-DRAG-TRUTH.md` | Referenced in inventory | **Not in repo** — locate and ingest |
| `docs/SHOP-SHUTDOWN.md` | Referenced in inventory | **Not in repo** |

### Priority 4 — generated at runtime

| Source | Producer | Refresh |
| --- | --- | --- |
| Spell artifacts | `sfe_bh_overlay_spells.py`, etc. | On-demand or nightly |
| Unit test logs | CI | Optional |
| Zenodo API | New versions | Daily poll |

---

## Technical options

### Option A — Self-hosted minimal (recommended Tier 1)

**Stack:** SQLite + FTS5 (full-text) + JSON spell registry + static file server.

| Pros | Cons |
| --- | --- |
| Zero cloud cost; runs in repo | No native semantic search |
| DA can extend in Python | Single-node scale |
| Matches existing script culture | Manual embedding later |

**Implementation sketch:**
- `tools/pfpi/ingest.py` — walk docs, populate SQLite.
- `tools/pfpi/serve.py` — FastAPI `GET /search`.
- Products call API via fetch + API key in env.

### Option B — Self-hosted unified (recommended Tier 2)

**Stack:** Meilisearch or Typesense (BM25 + faceted tags) + optional Qdrant sidecar for embeddings.

| Pros | Cons |
| --- | --- |
| Fast faceted search (`domain:NS`, `status:LEAD`) | Ops overhead |
| Good embed widget story | Hosting decision |
| Open source | |

**When:** >10k chunks or need sub-50ms partner demo search.

### Option C — Managed API

**Stack:** Algolia / Elasticsearch Cloud / Pinecone serverless.

| Pros | Cons |
| --- | --- |
| Fastest time-to-demo | Monthly cost |
| Built-in analytics | Vendor lock |
| | Clinical data residency questions |

**When:** Revenue from Field Lock / NAV-42 pilots justifies spend.

### Option D — Cursor / Cloud Agents as search (interim)

**Stack:** PFPI = markdown corpus + `AGENTS.md` instructions; agents use `grep`, `INDEX.json`, spell scripts at query time.

| Pros | Cons |
| --- | --- |
| Already works today for DA | Not embeddable in Replit/Base44 |
| No infra | Latency; no partner-facing SLA |
| Good for Jonathan + collaborator | |

**When:** Phase 0 only — parallel to building real PFPI.

### Option E — MCP gateway

Expose PFPI as MCP server (`search_prime_field`, `run_spell`, `get_ledger`). Cursor, Kyrana, and future cosmos app share one tool namespace.

| Pros | Cons |
| --- | --- |
| Matches Jonathan’s Cursor workflow | Non-MCP products need REST adapter |
| Spell execution first-class | |

**Recommendation:** **A → B → MCP adapter**. Start SQLite ingest of existing mirror this week; add Meilisearch when embedding product widgets.

### Embedding model choices (when adding vectors)

| Model | Use case |
| --- | --- |
| `text-embedding-3-small` (OpenAI) | Best semantic quality for papers |
| `e5-small-v2` (local) | No API cost; runs on Replit |
| No embeddings initially | BM25 + tags sufficient for Tier 1 |

**Do not** embed CUT Triple Lock papers without `da_status:KILLED` metadata — risk of RAG hallucinating false proofs.

---

## Phased rollout

### Tier 1 — Quick wins (1–2 weeks of focused DA work)

**Goal:** Search works for Jonathan and math collaborator inside this repo.

| # | Deliverable | Success criterion |
| --- | --- | --- |
| 1 | `tools/pfpi/ingest.py` ingests `INDEX.json` + all `docs/**` | `sqlite3 pfpi.db "SELECT count(*) FROM docs"` > 50 |
| 2 | `ledger.json` parsed from DA report | Query `status:LEAD` returns L1–L4 |
| 3 | `spell_registry.json` + `POST /spells/run` | Web UI or curl runs overlay spell, returns JSON URL |
| 4 | Static search page `docs/products/pfpi-demo.html` | Can find “Bridge* multi-rep” in <500ms |
| 5 | KEEP/CUT banner on CUT DOIs | Triple Lock search shows warning |

**Products touched:** Math corpus only (this repo). No Replit embed yet.

### Tier 2 — Unified index (3–6 weeks)

**Goal:** Partner-safe search across products + GitHub.

| # | Deliverable | Success criterion |
| --- | --- | --- |
| 6 | Meilisearch/Typesense with facets | Filter `product:field-lock` |
| 7 | Ingest portfolio branch + ship-it docs | Partner packet searchable |
| 8 | REST API + API keys (`public`, `partner`) | Field Lock Replit embed prototype |
| 9 | Zenodo nightly sync | New DOI versions appear automatically |
| 10 | Kyrana wired to PFPI | Oracle returns cited PFPI hits |
| 11 | Ship It “attach from index” on `/ship` | End-to-end ship note with PFPI link |

**Products touched:** Field Lock, Ship It, Kyrana, primefield.tech pages.

### Tier 3 — Pattern platform (ongoing)

**Goal:** Cross-domain pattern search as differentiator.

| # | Deliverable | Success criterion |
| --- | --- | --- |
| 12 | Vector layer for semantic “pattern rhymes” | Query “critical line weight black hole” returns SFE spellbook + HB nodes |
| 13 | Clinical partition for Vigilant | HIPAA review sign-off |
| 14 | Cosmos app as PFPI shell (if confirmed) | Single dashboard |
| 15 | ChatVault ingestion | AI conversation search |
| 16 | Drive watcher | Auto-ingest dropped tex into `docs/papers/` |
| 17 | MCP server published | Cursor + agents use one namespace |

---

## Pattern / underbrush layer — how search ties the vision

Jonathan’s “pattern across domains” is not marketing fluff in this repo — it is **operationalized as spells**. The search engine must expose this layer explicitly, not bury it in generic full-text.

### The underbrush ontology (shared tags)

| Tag | Meaning | Example locations |
| --- | --- | --- |
| `lattice:gcd` | Inverse-GCD operator family | Q6, SFE Hamiltonian, Bridge\* |
| `weight:critical_line` | \(n^{-1/2}\) or \(s=\tfrac12\) | SFE free term, BH `inv_r_sqrt` template |
| `floor:half` | \(-1/2\) Rayleigh / phase folklore | Bridge\*, SFE Phase II |
| `floor:two_pi` | \(-1/(2\pi)\) spectral limit | Route C Gap A′ (LEAD) |
| `concentration:snd` | Shell fraction / non-dispersal | NS SND, enstrophy shells |
| `concentration:herfindahl` | IPR / Herfindahl index | SFE ground state, spell output |
| `concentration:bis` | Anesthesia order parameter (LEAD) | Quantum Lens (CUT), spellbook §108 |
| `operator:Q_tilde` | \(\widetilde Q_N(i,j)=1/(\gcd\sqrt{ij})\) | Bridge\* proofs |
| `operator:H_N` | Degree-normalized matrix | `H_N-LOCK.md` |
| `null:held` | Experiment did not reject H0 | HB ringdown TEST |

### How spells become searchable

1. Each spell run produces JSON with numeric series + Pearson table + `leads[]` array.
2. PFPI indexes artifact + extracts `pattern_tags` from matched templates (e.g. `inv_r_sqrt` ↔ `weight:critical_line`).
3. User searches “overlay harmonic black hole” → returns spellbook section + latest artifact + **DA verdict** (“correlation ≠ proof”).

### Cross-domain map (search navigation)

```text
                    ┌───────────────┐
                    │ lattice: gcd  │
                    └───────┬───────┘
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
      ┌──────────┐    ┌──────────┐    ┌──────────┐
      │ NS / SND │    │ Q6 / RH  │    │ SFE / BH │
      │ dominant │    │ Route C  │    │ overlay  │
      │ shell    │    │ Bridge*  │    │ spells   │
      └────┬─────┘    └────┬─────┘    └────┬─────┘
           │               │               │
           └───────────────┼───────────────┘
                           ▼
                  ┌────────────────┐
                  │ weight: n^-1/2 │
                  │ (critical line)│
                  └────────┬───────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       ┌─────────────┐           ┌─────────────┐
       │ HB ringdown│           │ Anesthesia  │
       │ (null held)│           │ BIS (LEAD)  │
       └─────────────┘           └─────────────┘
```

### Product-facing pattern value

| Product | Pattern story (honest) | Search feature |
| --- | --- | --- |
| Field Lock | “Coherence / presence” language without Clay | Search partner docs for “coherence” → crypto results only |
| NAV-42 | Turbulence / lattice coating | Search NS KEEP papers + maritime dashboard |
| Harmonic Blueprint | Teaching metaphor | Search book + HB experiment + nodes.json |
| Vigilant | Operator overload ↔ phase transition (LEAD) | Clinical partition + exclude CUT Quantum Lens claims |
| Ship It | Operator systems architecture | Search operator-systems.md + ship history |

**Fence:** Pattern search must **never** auto-elevate LEAD to CLOSED. UI shows status chip on every hit.

---

## Open questions for DA / collaborator

### Product / scope

1. **What is the cosmos app?** URL, repo, stack, and intended role (dashboard vs experiment viewer)?
2. **Where is Ship It canonical repo?** `Ship_it_app` vs `ship-it-code` — merge strategy?
3. **Field Lock / NAV-42 Replit:** Can source be linked for ingestion, or metadata-only?
4. **NAV42-DRAG-TRUTH.md** and **SHOP-SHUTDOWN.md** — locate and add to repo?
5. **Vigilant clinical content:** Which branch, and what compliance partition rules?
6. **QStack** at primefield.tech/qstack — source repo?

### Architecture

7. **Hosting:** Self-host on Prime Field infra, Replit, or managed (Algolia/Pinecone)?
8. **Auth:** Single Jonathan password vs partner API keys vs OAuth?
9. **Clinical:** Separate Meilisearch index vs row-level `partition:clinical`?
10. **RAG for partners:** Allow LLM answers on public index only, with mandatory citation + status chips?

### Math / honesty

11. **Default search scope:** Exclude all CUT DOIs, or show with warning?
12. **Spell promotion workflow:** Who moves LEAD → CLOSED in ledger — manual DA only?
13. **Drive tex drop:** Workflow to ingest `NS_FINAL_MERGED_UNCONDITIONAL.tex` when found?
14. **H_N vs Q̃ vs Q:** Search must disambiguate operators — maintain `operator:*` facet?

### Integration priority

15. **First embed target:** Field Lock (revenue) vs Ship It (same GitHub org) vs math dashboard (ready corpus)?
16. **Kyrana vs cosmos:** Which becomes the NL search front-end?
17. **Base44:** Fix permissions or abandon and export static?

### Legal / IP

18. **Patent text in index:** NAV-42 provisional — full text or abstract only in partner partition?
19. **Zenodo CUT records:** Index for internal audit but block public API — confirm?

---

## Appendix: domain map

Quick reference for DA tagging. **Status** reflects `DA-REPORT-2026-08-28.md` + `KEEP-CUT-INVENTORY.md`, not prize packaging.

| Code | Domain | Core objects | Key repo sources | DA status (summary) | Product touchpoints |
| --- | --- | --- | --- | --- | --- |
| **NS** | Navier–Stokes / fluids | SND, dominant shell \(j^*\), Ring Lemma, Phi-renorm, T2 Gronwall | `20518057`, `01_phi_renormalization.tex`, `SND-H-STATUS.md` | Phi cancel **CLOSED**; SND unconditional **HARD** | NAV-42, maritime, Harmonic Blueprint |
| **RH** | Riemann Hypothesis analogies | Route C, equidistribution, μ/Möbius | `20518388`, Route C scripts | Conditional; Gap A′ **LEAD** | Primefield Explorer, Zenodo |
| **Q6** | Inverse-GCD / prime lattice | \(Q_N\), \(\widetilde Q_N\), \(H_N\), Bridge\* | `04_q6_inverse_gcd.tex`, `H_N-LOCK.md` | Bridge\* pairs **CLOSED**; full floor **KILLED** | SFE, explorers |
| **SFE** | Simons Field Equation | \(\hat H_{\mathrm{SFE}}\), Phase I/II, gcd interaction | Spellbook, archived Quantum Lens (CUT) | Structural rhymes **LEAD**; not Clay | Harmonic Blueprint, Field Lock coherence language |
| **BH** | Black holes / ringdown | QNM ratios, Schwarzschild templates, HB nodes | `hb_ringdown_test.py`, `nodes.json` | HB experiment **null held** | Harmonic Blueprint, overlay spells |
| **GNC** | Goldbach non-concentration | Goldbach vectors \(v_k\), dark states | `04_q6`, `BRIDGE-STAR-PROOF.md` | Wrong June 5 vector **KILLED**; Bridge\* multi-rep **CLOSED** | Q6 papers (honest subset) |
| **Clinical** | Anesthesia / CRNA | BIS, vigilance, operator overload | Other branches; spellbook anesthesia spell | BIS↔SFE **LEAD** only | Vigilant Patch, Solenne (telehealth) |
| **Crypto** | Presence-bound keys / encryption | Field Lock, CTW, PUF, FieldEncrypt | External Replit | Product **KEEP** (non-math) | Field Lock, SpectraLock |
| **Maritime** | Coatings / drag / coherence | NAV-42 lattice, maritime dashboard | External Replit + Base44 | Freeze false drag **required** | NAV-42, maritime dashboard |
| **Tools** | Developer / workflow | Ship It dispatch, ChatVault, Kyrana | `ship-it-app-e279` branch | Ship It **KEEP** | Ship It, ChatVault, Kyrana |
| **Luxury** | Consumer product | AquaQuarts water story | Brochure branches | **KEEP** (non-math) | AquaQuarts |
| **Expository** | Teaching / brand | Harmonic Blueprint book | theharmonicblueprint.com | Not proof | Book site, HB experiment docs |

### Operator disambiguation (critical for search)

| Symbol | Definition | Search facet |
| --- | --- | --- |
| \(Q^{\mathrm{raw}}_{ij}\) | \(1/\gcd(i,j)\) | `operator:Q_raw` |
| \(\widetilde Q_N\) | \(1/(\gcd(i,j)\sqrt{ij})\) | `operator:Q_tilde` |
| \(H_N\) | \(D^{-1/2}\widetilde Q D^{-1/2}\) | `operator:H_N` |
| \(H_N[u(t)]\) | Dynamic NS shell-helical operator | `operator:H_N_dynamic` — **not** same as static \(H_N\) |

### DOI quick reference (KEEP vs CUT)

| DOI | Title (short) | keep_cut | da_status |
| --- | --- | --- | --- |
| 10.5281/zenodo.20405404 | Phi-renorm Track B | KEEP | CLOSED (cancel) |
| 10.5281/zenodo.19842060 | Ring Lemma | KEEP | CLOSED (skeleton) |
| 10.5281/zenodo.20518388 | Route C | KEEP | conditional |
| 10.5281/zenodo.20552400 | Triple Lock | CUT | KILLED |
| 10.5281/zenodo.20552171 | Three-in-one | CUT | KILLED |
| 10.5281/zenodo.20269843 | Quantum Lens | CUT | KILLED (packaging) |

Full table: `docs/KEEP-CUT-INVENTORY.md`, `docs/papers/zenodo-spectral/README.md`.

---

## Appendix: reproduce audit commands

Commands used to assess repo state (2026-08-28):

```bash
# No vector DB / search engine deps
rg -i 'elasticsearch|pinecone|weaviate|qdrant|chromadb|faiss|meilisearch|typesense' .

# Product name inventory
rg -i 'Field Lock|Vigilant|NAV-42|AquaQuart|Ship It|Prime Field|cosmos' .

# Cosmos — zero matches in repo and all branches
git log --all --oneline -S"cosmos"

# Zenodo index count
python3 -c "import json; print(len(json.load(open('docs/papers/zenodo-spectral/INDEX.json'))))"

# Spell regression
python3 -m unittest tests.test_sfe_bh_spells -v
```

---

## Appendix: suggested first PR for DA

Minimal scoped PR to prove integration path:

1. Add `tools/pfpi/` with ingest + SQLite FTS.
2. Add `docs/products/spell_registry.json` listing seven scripts.
3. Add `docs/products/ledger.json` extracted from DA report.
4. Add `docs/products/pfpi-demo.html` — static search over ingested corpus.
5. Document API in `docs/products/PFPI-API.md` (stub).

Jonathan reviews demo → pick Tier 2 hosting → embed in Field Lock or Ship It.

---

*This report is honest about absences. It does not claim Clay problems are solved. It maps what exists, what is missing, and how a collaborator can extend the pattern-finding vision into a real cross-product search layer.*
