# ChatVault Hybrid Search — license unit

**File:** `chatvault/js/search.mjs`  
**Version:** `chatvault-hybrid-0.2.0` (`SEARCH_ENGINE_VERSION`)  
**Runtime:** ES module. Node 18+ (`node --test`) or a browser `<script type="module">`.  
**No DOM. No `localStorage`. No network.**

This is the ranker. It is not the ChatVault PWA, not CLAIM_LEDGER, not Domain Architect. This note is an API surface, not a commercial license agreement and not legal advice.

Do not add a separate npm package in this tree: the PWA is static files. Import the module by path.

---

## Import

```js
import {
  SEARCH_ENGINE_VERSION,
  searchVault,
  searchEntries,
  buildIndex,
  parseQuery,
} from "./search.mjs";
// or: from "/chatvault/js/search.mjs" on the DA/ChatVault origin
```

Do **not** import `../js/app.js` (PWA). `rankedSearch` there is a local wrapper around `searchVault` and is not part of this unit.

`../js/engine.mjs` re-exports `searchVault` plus ingest/ledger. Import that only if you want ChatVault records, not if you want the ranker alone.

Runnable copy for another product: `examples/search-engine-hook/hook.mjs` (`node examples/search-engine-hook/hook.mjs`).

---

## What you must supply

A corpus: an array of records. The ranker does not create documents. `fieldText` in `search.mjs` reads ChatVault-shaped fields (missing values are treated as empty):

| Field on the record | Indexed as |
| --- | --- |
| `title` | `title` |
| `raw_content`, `content_text` | `content` |
| `summary` | `summary` |
| `search_tags`, `project_tags` | `tag` |
| `key_claims[].text` | `claim` |
| `theorems[].text` | `theorem` |
| `open_gaps[].text` | `gap` |
| `open_questions[]` | `question` |
| `action_items[]` | `action` |
| `related_projects[]` | `book` |
| `source_type`, `source_file`, `media_path` | `source` |
| `source_ai` | `ai` |
| `key_claims\|theorems\|open_gaps[].status` | `status` (fielded `status:` only; not unfielded rank) |
| `origin_class` | `origin` (fielded `origin:` only; not unfielded rank / not in `all`) |

Also read for **filters / display**, not unfielded `all`: `id`, `visibility`, `archived`, `starred`, `project_category`, `ingested_at` (tiny tie-break). `harmonic_note` may exist on a ChatVaultEntry; it is **never** indexed or scored.

Minimum useful record:

```js
const records = [
  {
    id: "doc-1",
    title: "Euler identity as a definitional fact",
    content_text: "e^{iπ} + 1 = 0",
    raw_content: "e^{iπ} + 1 = 0",
    summary: "",
    search_tags: ["euler"],
    project_tags: [],
    key_claims: [{ text: "definitional identity", status: "UNREVIEWED" }],
    theorems: [],
    open_gaps: [],
    open_questions: [],
    action_items: [],
    related_projects: [],
    source_type: "conversation",
    source_file: "",
    source_ai: "Grok",
    origin_class: "ai_generated",
    visibility: "professional",
    archived: false,
    starred: false,
    ingested_at: "2026-08-26T00:00:00.000Z",
  },
];

const { engine, hits } = searchVault(records, "euler identity");
// engine === "chatvault-hybrid-0.2.0"
```

Reuse an index:

```js
const index = buildIndex(records);
const again = searchVault(records, "claim:definitional", {}, { index });
```

Query syntax: AND by whitespace; `OR` or `|`; `"phrases"`; `field:term` (`claim:`, `gap:`, `ai:`, `origin:ai`, `origin:human`, `status:OPEN`, …). Filters object: `visibility`, `source_ai`, `source_type`, `origin_class`, `project`, `starred`, `tag`, `book`, `includeArchived`.

---

## What you get back

```
{
  engine: "chatvault-hybrid-0.2.0",
  parsed: { mode, raw, terms?, phrases?, clauses? },
  took_ms: number,
  total: number,
  hits: [
    {
      entry,          // the record you passed in
      score,          // rrf*100 + tiny ingested_at tie-break
      snippets,       // up to 2 windows with marks + optional ledger_status
      matched_fields, // BM25F fields that contributed
      signals: { bm25, ngram, cosine, rrf, expanded? }
    }
  ]
}
```

Pipeline (short): match gate → BM25F (K1=1.2, stems, substring, one-edit) → char 3-gram BM25 → field-weighted TF-IDF cosine → RRF k=60 → optional RM3. Internals: `docs/chatvault-audit/CHATVAULT-ENGINE-INTERNALS.md`.

---

## What you do not get

- ChatVault PWA (`chatvault/index.html`, skins, `app.js`)
- CLAIM_LEDGER rules / no-auto-PROVED (`engine.mjs`)
- Domain Architect FRA auditor
- Drain walkers (`drain.mjs`), homepage dock, localStorage vault
- A MiniLM/E5 model, a web crawler, E8 ranking, Harmonic Watch as a score

Ledger status, `harmonic_note`, and E8 are never ranking signals in this file.

This is a local ranker over **your** array of records. It does not crawl the web.

---

## Hosting / CORS

- **Copy `search.mjs` into the other app** (recommended). The module has no network. Same-origin or `file:` / Node import — CORS does not apply.
- **Same origin as Domain Architect** (`python3 -m domain_architect --site`): `import { searchVault } from "/chatvault/js/search.mjs"` works. DA homepage currently imports `searchVault` from `/chatvault/js/engine.mjs` because it also uses the vault store.
- **Separate host, `<script type="module">` import of this repo’s URL:** browsers require CORS on the **GET** of the `.mjs` file and a JavaScript MIME type. `site_server.py` sends `Access-Control-Allow-Origin: *` on **OPTIONS** only; static GET does **not**. Cross-origin import from the loopback site will fail until you copy the file or add CORS on GET. DA/ChatVault CSP is `script-src 'self'` / `connect-src 'self'` — that is their shell, not a CDN for yours.

---

## Tests

```bash
cd chatvault
node --test tests/search.test.mjs tests/search-eval.test.mjs
```
