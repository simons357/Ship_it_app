# Modular Platform — Lego Architecture

**Date:** 2026-08-28  
**Branch:** `cursor/tao-snd-h-panel-a0eb`  
**Repo:** `simons357/Ship_it_app`  
**Related:** [`SEARCH-ENGINE-INTEGRATION-REPORT.md`](SEARCH-ENGINE-INTEGRATION-REPORT.md), [`CHATVAULT-HOOKUP.md`](CHATVAULT-HOOKUP.md), [`../KEEP-CUT-INVENTORY.md`](../KEEP-CUT-INVENTORY.md)

---

## Executive answer

**Yes — we can start the platform spine in this git repo now.**  
**No — we cannot unify every product runtime here without external wiring.**

Jonathan’s portfolio today runs on **competing operating systems**: Replit (Field Lock, NAV-42), Base44 (ChatVault shell, Solenne, Maritime), GitHub branches (Ship It, Kyrana), Zenodo + local math corpus (this repo), and unknown hosts (cosmos app). Each product re-implements auth, config, search, branding, and link catalogs in isolation.

**The fix:** One **platform spine** (shared kernel modules) + many **Lego skins** (product-specific UI and domain logic). Products do not get their own full stack — they plug into the spine via registry entries, thin SDK calls, and connectors.

---

## 1. Repo audit — what exists today

### In this repo (`Ship_it_app`, current branch)

| Asset | Path | Role | Duplication risk |
| --- | --- | --- | --- |
| Harmonic Blueprint Experiment 01 | `hb_ringdown_test.py`, `nodes.json` | Closed GW ringdown null test | Standalone script OS |
| Zenodo spectral mirror | `docs/papers/zenodo-spectral/INDEX.json` | 14 DOI machine index | **Seed for search module** |
| Math / audit corpus | `docs/math/*`, `docs/KEEP-CUT-INVENTORY.md` | Truth map, DA ledger | **Seed for ledger module** |
| Spells (pattern hunters) | `scripts/sfe_bh_overlay_spells.py`, etc. | Cross-domain correlation | **Seed for spell module** — no registry yet |
| Submit pack | `docs/papers/submit/` | Tier-1 publishable papers | Indexed by PFPI plan |
| Ship It assets | `assets/shipit_*.png` | Branding only | App code on `cursor/ship-it-app-e279` |
| **New scaffold** | `packages/shared_core/` | Product registry, config, link resolver | **Platform spine v0** |

### Referenced externally (not in this repo)

| Product | Host | Live URL | Tier | In repo? |
| --- | --- | --- | --- | --- |
| **Field Lock** | Replit | https://field-lock.replit.app/ | 1 | No — crypto kiosk + NDA depth |
| **Ship It** | GitHub / Next.js | `cursor/ship-it-app-e279` branch | 1 | Partial — assets only here |
| **NAV-42** | Replit | https://nav-42.replit.app/ | 1 | No — freeze false drag claims |
| **Vigilant Patch** | TBD | clinical lane | 1 | No — FDA path first |
| **AquaQuarts** | brochure branches | `cursor/aquaquartz-*` | 1 | No |
| **ChatVault** | Base44 route | https://primefield.tech/chatvault | 2 | **Hollow shell** — see hookup doc |
| **Kyrana** | GitHub | https://github.com/simons357/kyrana-oracle | 2 | No |
| **Solenne / Maritime / SFE-RH** | Base44 | `*.base44.app` | 2 | No — permissions often broken |
| **ExoRatio** | Base44 | exo-ratio URL | 2 | **CUT** — do not promote |
| **Cosmos app** | Unknown | — | — | **Not found in git** — needs URL/repo |
| **SpectraLock / FieldEncrypt** | Field Lock bundle | — | 2 | Same lane as Field Lock |

### Duplication patterns (competing OS symptoms)

| Concern | Where duplicated today | Spine replacement |
| --- | --- | --- |
| Product catalog | `KEEP-CUT-INVENTORY.md`, portfolio branches, outreach lists | `packages/shared_core/product_registry.json` |
| URL truth | Field Lock uses Replit; primefield `/field-lock` empty | `link_resolver.py` — canonical URL policy |
| Search | None deployed; each product is siloed | PFPI module (see search report) |
| Auth | Per-app Replit/Base44 auth | Shared auth module (external — Phase 2) |
| Truth / KEEP-CUT | Markdown only | DA ledger module + search filters |
| Pattern spells | Ad-hoc Python scripts | `spell_registry.json` + PFPI `/spells/run` |
| Branding | Per-product assets | `packages/shared_core/branding/` (future) |

---

## 2. Design — one spine, many Lego blocks

### Principle: no competing OS

```text
                    ┌─────────────────────────────────────┐
                    │         PLATFORM SPINE (kernel)      │
                    │  auth · config · search · vault ·    │
                    │  telemetry · branding · link resolver │
                    └──────────────────┬──────────────────┘
                                       │ plug-in API
         ┌─────────────┬───────────────┼───────────────┬─────────────┐
         ▼             ▼               ▼               ▼             ▼
   ┌──────────┐  ┌──────────┐   ┌──────────┐   ┌──────────┐  ┌──────────┐
   │Field Lock│  │ Ship It  │   │ChatVault │   │ Math/DA  │  │ NAV-42   │
   │  skin    │  │  skin    │   │  skin    │   │  skin    │  │  skin    │
   │ Replit   │  │ Next.js  │   │ Base44/  │   │ scripts  │  │ Replit   │
   │          │  │          │   │ Vercel   │   │ + docs   │  │          │
   └──────────┘  └──────────┘   └──────────┘   └──────────┘  └──────────┘
```

**Skins** own domain UX and business logic. **Spine** owns cross-cutting concerns once.

### Kernel modules (shared base functions)

| Module | Responsibility | v0 in repo? | External dependency |
| --- | --- | --- | --- |
| **config** | Load registry, env overrides, feature flags | ✅ `packages/shared_core/config.py` | — |
| **link_resolver** | Canonical URLs; warn on hollow/dead routes | ✅ `packages/shared_core/link_resolver.py` | — |
| **product_registry** | Single catalog: tier, status, modules, URLs | ✅ `product_registry.json` | — |
| **search (PFPI)** | Full-text + tags + optional vectors | ✅ `tools/pfpi/` SQLite FTS5 | Meilisearch optional Phase 2 |
| **ledger (DA)** | KEEP/CUT/LEAD/KILLED truth tags | ✅ `tools/pfpi/ledger.json` | Sync from new DA reports |
| **spells** | Pattern-hunter registry + run API | ✅ registry + `spell_runner.py` + `/v1/spells/run` | MCP adapter Phase 3 |
| **vault_export** | Chat/thread import schema | Schema only | ChatVault MVP host |
| **auth** | OAuth, API keys, partitions (public/partner/clinical) | No | Supabase/Clerk/Replit auth |
| **telemetry** | Product events, spell runs, search queries | No | PostHog / self-host |
| **branding** | Logos, tokens, Prime Field voice | Partial — `assets/` | Design system package |

Registry file: `packages/shared_core/product_registry.json`.

### Product Lego blocks (plug-in contract)

Each product declares in `product_registry.json`:

```json
{
  "id": "field-lock",
  "modules": ["auth", "search", "link_resolver", "telemetry"],
  "connector": "replit",
  "skin_host": "https://field-lock.replit.app/"
}
```

**Block types:**

| Block type | Examples | Hosts on |
| --- | --- | --- |
| **Live demo skin** | Field Lock kiosk, NAV-42 coating demo | Replit |
| **Workflow skin** | Ship It dispatch, ChatVault archive UI | Next.js / Vercel / Base44 |
| **Corpus skin** | Math panel, DA dashboard, spell runner | This repo + PFPI |
| **Oracle skin** | Kyrana NL front-end | GitHub → PFPI API |
| **Clinical skin** | Vigilant Patch teaching | Separate HIPAA partition |
| **Brand skin** | Harmonic Blueprint, primefield.tech hub | Static / Base44 |

Products **must not** re-implement: catalog, canonical URL policy, KEEP/CUT filters, or cross-product search — they call spine APIs.

---

## 3. How named products fit as modules (not separate stacks)

### ChatVault → vault + search modules

Not a standalone “chat OS.” ChatVault is:

1. **vault_export** block — ingest schema for Claude/ChatGPT/MD exports, secret redaction
2. **auth** block — per-user isolation
3. **search (PFPI)** block — `source_type:chatvault` index partition

See [`CHATVAULT-HOOKUP.md`](CHATVAULT-HOOKUP.md). Until MVP ships, registry marks `status: hollow`.

### Search engine (PFPI) → spine module, not a product

PFPI is **infrastructure inside the spine**, not a ninth competing app. Every skin embeds a thin search client:

```javascript
// 5-line embed in any skin
const hits = await fetch(`${PFPI_URL}/search?q=${q}&product=field-lock`, {
  headers: { Authorization: `Bearer ${PFPI_KEY}` }
});
```

Corpus search, spell search, and DA ledger search are three **views** on one index (see search report § “three layers”).

### DA / spells → executable modules on the spine

| Today | Tomorrow |
| --- | --- |
| `scripts/sfe_bh_overlay_spells.py` run by hand | `POST /spells/run {name: "sfe_bh_overlay", args: {Nmax: 500}}` |
| `docs/math/DA-REPORT-*.md` read by humans | `GET /ledger?status=LEAD` |
| Spellbook markdown | `spell_registry.json` + PFPI facet `tag:lattice:gcd` |

Math corpus stays in this repo; **execution and discovery** move to spine APIs.

### Field Lock / NAV-42 → skins + connector metadata

Replit apps stay on Replit. They **stop owning**:

- Partner doc search → PFPI embed widget
- Product URL in outreach → `link_resolver.canonical("field-lock")`
- Catalog tier/status → read from registry (or sync webhook)

Connector: Replit deployment posts metadata to PFPI ingest (title, tags, `product:field-lock`).

### Ship It → workflow skin on spine

Branch `cursor/ship-it-app-e279` becomes a skin that calls:

- PFPI — “attach from index” when shipping notes
- link_resolver — never ship dead Base44 links
- config — feature flags for dispatch modes

### Cosmos app → TBD shell

Zero matches in git. When URL/repo supplied, register as **dashboard skin** aggregating PFPI + product registry — not a new stack.

---

## 4. Folder proposal

```text
Ship_it_app/
├── packages/
│   └── shared_core/                 # Platform spine v0 (this branch)
│       ├── __init__.py
│       ├── config.py                # Registry + env loader
│       ├── link_resolver.py         # Canonical URL policy
│       ├── product_registry.json    # Single product catalog
│       └── spell_registry.json      # Spell script registry
├── tools/
│   └── pfpi/                        # Phase 1 — search spine ✅
│       ├── ingest.py                # SQLite FTS5 ingest
│       ├── search.py                # CLI search
│       ├── serve.py                 # FastAPI GET /v1/search, POST /v1/spells/run
│       ├── ledger.json              # Parsed from DA report
│       └── ledger.py                # Ledger loader/filter
├── connectors/                      # Phase 2 — external ingest (planned)
│   ├── zenodo_sync.py
│   ├── github_ingest.py
│   └── replit_metadata.yaml
├── docs/
│   └── products/
│       ├── MODULAR-PLATFORM-LEGO.md # This document
│       ├── SEARCH-ENGINE-INTEGRATION-REPORT.md
│       └── CHATVAULT-HOOKUP.md
├── scripts/                         # Existing spells (indexed by registry)
└── tests/
    └── test_shared_core.py
```

**Monorepo pattern:** `packages/shared_core` is importable by scripts, PFPI tools, and (via copy or npm/pip publish later) external skins.

---

## 5. Implementation roadmap

### CAN do in this git repo now (no Codex/Replit required)

| # | Deliverable | Status |
| --- | --- | --- |
| 1 | Product registry JSON synced to KEEP-CUT-INVENTORY | ✅ v0 scaffold |
| 2 | Link resolver with Field Lock / ChatVault URL policy | ✅ v0 scaffold |
| 3 | Config loader + env overrides | ✅ v0 scaffold |
| 4 | Spell registry pointing at existing scripts | ✅ v0 scaffold |
| 5 | Architecture docs (this file + search report) | ✅ |
| 6 | PFPI SQLite ingest of `docs/**` + `INDEX.json` | ✅ `python3 -m tools.pfpi.ingest` |
| 7 | `ledger.json` parser from DA report | ✅ `tools/pfpi/ledger.json` |
| 8 | Static PFPI demo page | ✅ `docs/products/pfpi-demo.html` |
| 9 | Unit tests for spine modules | ✅ `tests/test_shared_core.py`, `tests/test_pfpi.py` |
| 10 | Spell runner + REST API | ✅ `scripts/run_spell.py`, `tools/pfpi/serve.py` |

### NEEDS external Codex / Replit / connectors

| # | Deliverable | Who wires it |
| --- | --- | --- |
| A | Field Lock Replit → PFPI embed widget | Replit app + API key in env |
| B | NAV-42 Replit → PFPI + drag-claim suppression | Replit app |
| C | ChatVault MVP (auth + storage + import) | Base44/Replit/Vercel new app |
| D | Ship It Next.js → PFPI “attach from index” | `ship-it-code` repo branch |
| E | Base44 apps → export JSON or fix public permissions | Base44 dashboard |
| F | Shared auth (OAuth, partitions) | Supabase/Clerk + per-skin SDK |
| G | Cosmos app registration | Jonathan supplies URL/repo |
| H | Clinical partition (Vigilant) | HIPAA review + separate index |
| I | MCP server exposing PFPI to Cursor/Kyrana | Cursor MCP or self-host |
| J | Google Drive tex ingest | Manual drop or Drive connector |

### Phase timeline (technical, not calendar)

```text
Phase 0 (now)     Registry + link resolver + docs + spell registry
Phase 1 (repo)    PFPI SQLite ingest + ledger + demo search page
Phase 2 (connect) Replit/Base44/GitHub connectors + REST API keys
Phase 3 (platform) Auth module + ChatVault vault block + vector search
Phase 4 (skins)   Thin embeds in Field Lock, Ship It, Kyrana, cosmos
```

---

## 6. Direct Codex or connectors — what to wire where

### MCP (Model Context Protocol)

**What it is:** A standard way for AI tools (Cursor, Codex, Kyrana) to call **tools** — search, run spell, get ledger — without each product building custom integrations.

**Wire here:** PFPI exposes MCP tools (`search_prime_field`, `run_spell`, `get_ledger`, `resolve_link`). Cursor agents and Kyrana oracle call the **same namespace**.

**Do not wire in:** Individual Replit apps (they use REST embed + API key, not MCP directly).

### API gateway

**What it is:** One HTTPS entry (`api.primefield.tech` or similar) routing to PFPI, auth, vault.

**Wire here:** Phase 2 — FastAPI or Cloudflare Worker in repo or infra repo.

**Products call:** `GET /v1/search`, `GET /v1/products/{id}/url`, `POST /v1/vault/import`.

### Monorepo pattern (this repo)

**What it is:** Shared Python/JSON packages versioned with math corpus; external skins consume via pip, npm, or copied JSON.

**Wire here:** `packages/shared_core` — already started.

**External skins:** Import registry JSON or call hosted API; do not fork catalog.

### Replit connectors

**What:** Field Lock, NAV-42 stay on Replit. Add env vars `PFPI_URL`, `PFPI_KEY`. Footer widget calls search. Optional webhook on deploy → PFPI ingest metadata.

**Jonathan/Codex action:** Open Replit project → add fetch to PFPI → no spine code in Replit repo required if using REST only.

### Base44 connectors

**What:** ChatVault, Solenne, Maritime — export app JSON or fix public publish; PFPI ingests static export. Live sync needs Base44 API if available.

**Jonathan action:** Fix permissions per `BASE44-PUBLIC.md` (portfolio branch) before linking.

### ChatVault-specific

Not “just a link.” Needs auth + encrypted store + PFPI `source_type:chatvault`. See [`CHATVAULT-HOOKUP.md`](CHATVAULT-HOOKUP.md).

---

## 7. Top 3 modular base functions to build first

| Priority | Module | Why first | Repo action |
| --- | --- | --- | --- |
| **1** | **product_registry + link_resolver** | Stops competing URL/catalog OS immediately; Field Lock vs hollow primefield routes | ✅ Done v0 — keep synced with KEEP-CUT-INVENTORY |
| **2** | **search (PFPI) Tier 1** | Unifies math corpus, Zenodo mirror, DA ledger, spells — highest daily value for Jonathan | `tools/pfpi/ingest.py` next |
| **3** | **spell_registry + run API** | Operationalizes “pattern across domains” as spine capability, not ad-hoc scripts | Registry ✅; `/spells/run` with Phase 1 PFPI |

Auth and ChatVault vault are **#4 and #5** — blocked on host choice and MVP scope.

---

## 8. Usage — spine v0 today

```python
from packages.shared_core.config import load_registry
from packages.shared_core.link_resolver import resolve_url, link_status

registry = load_registry()
fl = registry["products"]["field-lock"]
print(resolve_url("field-lock"))  # https://field-lock.replit.app/
print(link_status("chatvault"))   # hollow — do not cold-send
```

```bash
python -m unittest tests/test_shared_core.py
python -m unittest tests/test_pfpi.py -v
```

---

## 10. Implemented — Phase 1 PFPI (2026-08-28)

The modular platform doc has been translated into runnable code:

| Component | Path | Run |
| --- | --- | --- |
| **Ingest** | `tools/pfpi/ingest.py` | `python3 -m tools.pfpi.ingest` |
| **CLI search** | `tools/pfpi/search.py` | `python3 -m tools.pfpi.search "Bridge star" --limit 5` |
| **DA ledger** | `tools/pfpi/ledger.json` | `python3 -c "from tools.pfpi.ledger import filter_ledger; print(len(filter_ledger(status='LEAD')))"` |
| **Spell runner** | `packages/shared_core/spell_runner.py` | `python3 scripts/run_spell.py sfe_bh_overlay 200` |
| **REST API** | `tools/pfpi/serve.py` | `python3 -m tools.pfpi.serve` → `GET /v1/search?q=…` |
| **Demo UI** | `docs/products/pfpi-demo.html` | Open after starting serve on port 8765 |
| **API docs** | `docs/products/PFPI-API.md` | Endpoint reference |

**Still needs external input:**

- **VR Surgeon** — no storyboard in repo; see [`VR-SURGEON-UNREAL-PIPELINE.md`](VR-SURGEON-UNREAL-PIPELINE.md)
- **Cosmos app** — URL/repo unknown
- **ChatVault MVP** — hollow shell; auth + storage host TBD
- **Replit/Base44 connectors** — Phase 2

---

## 9. Cross-references

| Doc | Purpose |
| --- | --- |
| [`SEARCH-ENGINE-INTEGRATION-REPORT.md`](SEARCH-ENGINE-INTEGRATION-REPORT.md) | PFPI detail, embeddings, phased rollout |
| [`CHATVAULT-HOOKUP.md`](CHATVAULT-HOOKUP.md) | ChatVault as vault module, not standalone stack |
| [`../KEEP-CUT-INVENTORY.md`](../KEEP-CUT-INVENTORY.md) | Truth map for registry sync |
| [`../math/DA-REPORT-2026-08-28.md`](../math/DA-REPORT-2026-08-28.md) | Ledger source for PFPI |
| [`../math/SFE-BH-OVERLAY-SPELLBOOK.md`](../math/SFE-BH-OVERLAY-SPELLBOOK.md) | Spell ontology |

---

*When cosmos app URL or ChatVault live MVP exists, update `product_registry.json` and bump tier in KEEP-CUT-INVENTORY.*
