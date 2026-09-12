# ChatVault hybrid ranker — internals

**Audience:** Jonathan Simons (and any product that might import only the ranker).  
**Date:** 26 August 2026  
**Source of truth:** `chatvault/js/search.mjs`  
**Version string (literal):** `chatvault-hybrid-0.2.0`  
  (`export const SEARCH_ENGINE_VERSION` at line 22 of `chatvault/js/search.mjs`; returned as `result.engine` from `searchVault`.)

This file describes the **ranker**, not the PWA. It is not a license agreement. It is not a claim that a lawyer reviewed anything.

License-unit API (import example, record shape, what you do not get): `chatvault/js/ENGINE.md`.

---

## Module boundary

| File | Role |
| --- | --- |
| `chatvault/js/search.mjs` | Ranker. Zero imports. No DOM. No `localStorage`. This is the licensed unit. |
| `chatvault/js/engine.mjs` | ChatVault product: `ChatVaultEntry` schema `chatvault-engine-0.3.0`, ingest, CLAIM_LEDGER, store. Re-exports a **subset** of the ranker (`SEARCH_ENGINE_VERSION`, `searchEntries`, `searchVault`, `parseQuery`, `tokenize`, `buildIndex`, `ndcgAt`). |
| `chatvault/js/app.js` | PWA. `rankedSearch()` is a **local function** (not exported) that calls `searchVault(store.list(), state.query, activeFilters())`. Other products should not import `app.js`. |
| `chatvault/js/drain.mjs` | ChatGPT JSON walker, DA drain pull, file-drop ingest. Not ranking. |
| `domain_architect/static/da-home.js` | Homepage dock. Imports `searchVault` from `/chatvault/js/engine.mjs`, not from `search.mjs` directly. |

There is no function named `rankedSearch` in `search.mjs`. The public ranking entry point is `searchVault`. `searchEntries` is `searchVault(…).hits.map(h => h.entry)`.

Public exports from `search.mjs`:

`SEARCH_ENGINE_VERSION`, `K1`, `RRF_K`, `SEARCH_FIELDS`, `RANK_FIELDS`, `tokenize`, `stem`, `editDistanceAtMost`, `charNgrams`, `fieldText`, `entryFields`, `parseQuery`, `idf`, `reciprocalRankFusion`, `bestWindow`, `buildIndex`, `searchVault`, `searchEntries`, `ndcgAt`, `mrr`.

---

## Ordered pipeline (`searchVault`)

`searchVault(entries, query, filters = {}, { index } = {})` in `chatvault/js/search.mjs`.

1. `parseQuery(query)`
2. `buildIndex(entries)` unless the caller passes `{ index }`
3. Hard filters (`passesFilters`)
4. Boolean match gate (`queryMatches`) — skipped for empty query
5. Three independent lists: BM25F, character 3-gram BM25, field-weighted TF-IDF cosine
6. Reciprocal Rank Fusion, `k = 60`
7. Optional RM3 (up to 2 docs, 3 terms) then fuse **four** lists
8. Display score `rrf * 100 + tieBreak(ingested_at)`

Empty query (`parsed.mode === "empty"`): filters only, `score: 0`, no snippets, order is index/document order (the order `entries` were indexed). Tests in `chatvault/tests/search.test.mjs` assert this matches `DEMO_ENTRIES` order.

---

## 1. Query parse: AND / OR / phrases / `field:`

`parseQuery` / `parseAndClause` in `chatvault/js/search.mjs`.

- Empty / whitespace → `{ mode: "empty", raw }`.
- Split on `\s+OR\s+` or `\s+\|\s+` (case-insensitive). More than one part → `{ mode: "or", clauses: [...] }`.
- Otherwise `{ mode: "and", …parseAndClause(raw) }`. There is **no** `AND` keyword. Whitespace-separated tokens are AND.
- Token regex: `/(?:(\w+):)?(?:"([^"]+)"|(\S+))/g`
  - `"quoted phrase"` → `phrases[]`
  - otherwise → `terms[]`
  - optional `field:` prefix
- Field names go through `resolveField`: lowercased, then `FIELD_ALIASES`, else the raw name.
- Aliases (literal map): `raw|body|text` → `content`; `claims` → `claim`; `theorems` → `theorem`; `gaps` → `gap`; `questions` → `question`; `actions` → `action`; `tags` → `tag`; `books` → `book`; `visibility` → `visibility`; `real|designation` → `origin`; `all` → `all`.
- `origin:` terms are normalized: `ai|generated|ai_generated` → `ai_generated`; `human|real|record|human_record` → `human_record`.

Unknown `field:` names are not rejected at parse time. At score time, `fieldsForTerm` falls back to `RANK_FIELDS` if the name is not in `SEARCH_FIELDS` (except `status`, which is allowed as a fielded query). `fieldText` on an unknown key returns the unfielded `all` haystack.

---

## 2. Inverted index

`buildIndex(entries)` builds, per document:

- Per-field token TFs (`fieldTfs`) via `tokenize`
- Per-field token sets (`fieldTokens`)
- Per-field character 3-gram TFs (`fieldNgramTfs`) via `charNgrams`
- Field lengths (token counts) and n-gram lengths
- Collection DF (`df`), stem DF (`stemDf`), n-gram DF (`ngramDf`)
- Average field length / n-gram length
- A field-weighted TF-IDF vector (`doc.tfidf`) and its squared L2 (`tfidfNorm`)

`tokenize`: lowercased; split on `[^a-z0-9π∞=+\-*/^_{}()[\]|]+`; empty tokens dropped. Hyphens split (`navier-stokes` → `navier`, `stokes`).

Collection stats: `index.N` = number of documents. A term’s DF is the number of **documents** that contain that exact token at least once (any field). Stem DF is the number of documents that contain that stem.

The index is in-memory. It is not persisted. Callers may reuse it via `{ index }`.

`entryFields` indexes every key in `SEARCH_FIELDS`, including `status` and `origin`. Those fields exist so `status:` and `origin:` queries have postings. They are **not** in the unfielded `all` haystack (see §10).

---

## 3. Hard filters vs match gate

**Hard filters** (`passesFilters(entry, filters)`), applied before ranking:

| `filters` key | Effect |
| --- | --- |
| `includeArchived` | Archived entries dropped unless this is truthy |
| `visibility` | Exact `entry.visibility` |
| `source_ai` | Exact `entry.source_ai` |
| `source_type` | Exact `entry.source_type` |
| `origin_class` | Exact `entry.origin_class` |
| `project` | Exact `entry.project_category` |
| `starred` | Requires `entry.starred` |
| `tag` | Case-insensitive exact tag in `search_tags` ∪ `project_tags` |
| `book` | Case-insensitive exact name in `related_projects`; `"(unfiled)"` matches entries with no books |

These are UI / caller filters, not query syntax.

**Match gate** (`queryMatches`): boolean. AND of terms and phrases inside a clause; OR of clauses. A document that fails the gate is **not ranked** (it is omitted). Empty query skips the gate.

A **term** is present if any of:

1. Field haystack (lowercased) `.includes(term)`
2. Exact token in the field token set
3. Stem match, if `stem(term).length >= 4`
4. One-edit typo against a token, if `term.length >= 4` and token lengths differ by at most 1

A **phrase** is present only if the field haystack `.includes(phrase)` (lowercased exact substring). No stem/typo on the phrase as a whole.

Unfielded terms use field `"all"`. `fieldHaystack(doc, "all")` is `doc.allText` = `fieldText(entry, "all")` (see §10).

---

## 4. BM25F (K1, fields, stem / substring / one-edit)

Constants: `K1 = 1.2`. Per-field `boost` and `b` live in `SEARCH_FIELDS`.

Unfielded scoring uses `RANK_FIELDS` = `SEARCH_FIELDS` minus `status` and `origin`. Fielded `status:` scores only `status`. Fielded `origin:` scores only `origin` (because `origin` is in `SEARCH_FIELDS`).

**Field-weighted TF** (`weightedTf`): for each allowed field,

```
norm = 1 - b + b * (len / avgLen)
tfw += (boost * tf) / max(norm, 1e-9)
```

Then **one** BM25 saturation on the sum:

```
score += idf(term) * (tfw * (K1 + 1)) / (tfw + K1)
```

This is weight-after-sum BM25F, not per-field saturation. IDF is:

```
idf = log(1 + (N - n + 0.5) / (n + 0.5))
```

with `n = df(term) || stemDf(stem(term)) || 0`. The `+1` inside the log keeps IDF non-negative.

**Term frequency fallbacks** (`fieldTermFrequency`), first hit wins:

| Match | TF used |
| --- | --- |
| Exact token | raw TF, weight 1 |
| Else substring: count of tokens with `tok.includes(term)` | that count × `SUBSTRING_TF` (0.4) |
| Else stem, if stem length ≥ 4 | sum of matching token TFs × `STEM_TF` (0.85) |
| Else one-edit, if term length ≥ 4 | first matching token’s TF × `FUZZY_TF` (0.65) |

**Stemmer** (`stem`): in-house, not full Porter. Length ≤ 4 unchanged. Else suffix rules: `ational`→`ate`, `tional`→`tion`, `ies`→`y`, `sses` drop `es`, trailing `s` (not `ss`, length > 4), `ing` (length > 6) then optional doubled-consonant trim, `ed` (length > 5) similarly, `er` (length > 6).

**One-edit** (`editDistanceAtMost(..., 1)`): substitution, or single insertion/deletion. Length difference > 1 is rejected immediately.

**Phrases on the BM25F list:** if the phrase substring is present, add `PHRASE_BONUS` (2.4) × `idf(first phrase token)` × BM25 saturation of a presence-weighted `phraseTfw` (`boost/norm` once per matching field, not phrase TF). Then also add ordinary BM25F of each token in the phrase.

OR queries: score each matching clause; keep the max BM25F clause score.

---

## 5. Character 3-gram BM25

`NGRAM = 3`. `charNgrams` lowercases, collapses whitespace, wraps with spaces, then emits every 3-character window (so hyphens and misspellings still overlap).

N-gram BM25 uses the same K1 and the same field `boost`/`b`, with n-gram TF / n-gram length / `avgNgramLen` / `ngramIdf` (same IDF formula on `ngramDf`).

Field set for n-grams: first term’s field in the clause, else first phrase’s field, else `RANK_FIELDS`. OR takes the max clause n-gram score.

This is a **separate ranked list**, not a term in the word BM25F score.

---

## 6. Field-weighted TF-IDF cosine

At index time, for each token in `doc.allTokens`:

```
w = boostedTermWeight(doc, term) * idf(term)
```

`boostedTermWeight` sums `RANK_FIELDS` only (`boost * fieldTermFrequency`). Stored under both the raw term and `stem(term)` at 0.5×. `tfidfNorm` is Σ w² (raw-term contributions).

At query time, unique query terms (from terms and tokenized phrases):

```
q = idf(term)
d = tfidf(term) + 0.85 * tfidf(stem(term))
cosine = dot(q, d) / (||q|| ||d||)
```

This is a **second vector signal**, fused by RRF. It is not embeddings. It is not an LLM.

---

## 7. RRF k=60

`RRF_K = 60`. `reciprocalRankFusion(rankedIdLists, k)`:

```
score[id] += 1 / (k + idx + 1)
```

`idx` is 0-based, so rank 1 contributes `1/61`. Ties on a list are broken by `id` string compare after the numeric key.

First fusion is three lists: BM25F, n-gram, cosine. Documents that win more than one list accumulate more RRF. Test: `chatvault/tests/search.test.mjs` “RRF prefers documents that win more than one list”.

---

## 8. Optional RM3

After the first RRF sort:

- Keep rows with `bm25 >= 0.6 * top.bm25`, take at most **2** documents.
- From those, collect expansion terms (`rm3Terms`, limit 3):
  - `content` tokens length ≥ 4, not already in the query, DF ≤ `max(2, N * 0.5)`
  - `claim` tokens length ≥ 4, not in the query (no DF cap); weight × 1.4
  - Score `tf * idf`; take top 3 terms
- If any extra terms exist: BM25F them over `RANK_FIELDS` as `expanded`, then **fuse again** over four lists (bm25, ngram, cosine, expanded).
- If no extra terms, the first three-list RRF stands.

There is no UI toggle in the ranker. “Optional” means “runs when expansion terms exist.” The homepage Recommendations card may mention exposing a toggle; that is not implemented in `search.mjs`.

Expanded terms are returned on each hit as `signals.expanded` (the term list, not a per-doc expanded score).

---

## 9. What is NEVER a score

| Signal | What the code does |
| --- | --- |
| Ledger status (`UNREVIEWED` … `PROVED`) | Displayed on cards/snippets (`ledger_status`). `status:` is a **field query** (match gate + BM25F on the `status` field only). `status` is **not** in `RANK_FIELDS`. Unfielded queries do not treat PROVED as quality. Tests: “OPEN can outrank PROVED”; “status: remains a field query”. |
| `harmonic_note` | Stored on the ChatVaultEntry in `engine.mjs`. **Not** in `SEARCH_FIELDS`. **Not** in `fieldText("all")`. Identical scores with and without a note that repeats the query. |
| E8 / lattice / geometry | **Not implemented.** File comment: “E8 / lattice ranking is not implemented.” See `docs/chatvault-audit/EXPERIMENTAL-NOT-SHIPPED.md`. |

Snippet ordering uses `+0.25` when a snippet has a `ledger_status`. That reorders **snippets**, not documents.

Final document score is `rrf * 100 + Date.parse(ingested_at) / 1e15` (the time term is ~10⁻³ or smaller). Then sort by score desc, title asc.

---

## 10. `origin` searchable but not in `RANK_FIELDS` / unfielded `all`

`SEARCH_FIELDS.origin = { boost: 2.4, b: 0.2 }`.

`RANK_FIELDS` explicitly drops `status` **and** `origin` (`search.mjs` lines 44–49). Comment in code: “Unfielded rank uses these. `status:` and `origin:` are designations, not quality boosts.”

`fieldText(entry, "all")` concatenates: title, content, summary, ai, source, tag, claim, theorem, gap, question, action, book. It does **not** include `origin`, `status`, `visibility`, or `harmonic_note`. `source` is `source_type` + `source_file` + `media_path`.

Consequences:

- `origin:ai` / `origin:human` (and aliases) are match-gate field queries. They work.
- Typing unfielded `ai` does **not** match `origin_class: ai_generated` and does **not** rank-boost every AI chat. Test: “origin:ai and origin:human filter; unfielded ai does not rank-boost every AI chat”.
- The `ai` **field** is `source_ai` (`Grok`, `Claude`, …). `ai:Claude` is provenance, not a vibe.

Hard filter `filters.origin_class` is separate from the `origin:` query operator.

---

## 11. Version string

```js
export const SEARCH_ENGINE_VERSION = "chatvault-hybrid-0.2.0";
```

`searchVault` returns `{ engine: SEARCH_ENGINE_VERSION, parsed, took_ms, total, hits }`.

This is **not** `SCHEMA_VERSION` (`chatvault-engine-0.3.0` in `engine.mjs`) and **not** the PWA cache (`chatvault-engine-v0.6.1` in `chatvault/sw.js`).

Eval: `chatvault/tests/search-eval.test.mjs` — synthetic seven-doc set, mean nDCG@5 ≥ 0.9, mean MRR ≥ 0.9. Comment in that file: fixtures, not Jonathan’s research corpus.

---

## 12. Public functions other products could import

Import from `chatvault/js/search.mjs` (not `app.js`, not `engine.mjs` unless you also want the ledger). Copy-paste hook: `examples/search-engine-hook/hook.mjs`.

| Export | Use |
| --- | --- |
| `searchVault(entries, query, filters?, { index }?)` | Rank. Returns `{ engine, parsed, took_ms, total, hits }` where each hit is `{ entry, score, snippets, matched_fields, signals: { bm25, ngram, cosine, rrf, expanded? } }`. |
| `searchEntries(...)` | Same, but an array of entries. |
| `buildIndex(entries)` | Reuse across queries. |
| `parseQuery(q)` | Inspect the match gate. |
| `tokenize` / `stem` / `editDistanceAtMost` / `charNgrams` | Same token rules as the index. |
| `fieldText` / `entryFields` | What gets indexed on a record. |
| `idf` / `reciprocalRankFusion` | Building blocks. |
| `bestWindow(text, needles, window=220)` | Snippet window. |
| `ndcgAt` / `mrr` | Eval helpers. |
| `SEARCH_FIELDS` / `RANK_FIELDS` / `K1` / `RRF_K` / `SEARCH_ENGINE_VERSION` | Constants. |

`rankedSearch` is **not** importable. It is PWA glue in `chatvault/js/app.js`.

You must supply a corpus of records with the fields `fieldText` reads (see `chatvault/js/ENGINE.md`). You do not get the PWA, CLAIM_LEDGER enforcement, Domain Architect, skins, or drain walkers by importing `search.mjs` alone.

---

## Tests that pin this behavior

- `chatvault/tests/search.test.mjs` — version, title vs body, phrase gate, fielded `claim:`/`gap:`, filters, empty query, typos/stems, OPEN vs PROVED, `harmonic_note` not a score, `status:` not an unfielded boost, RRF, `origin:` vs unfielded `ai`.
- `chatvault/tests/search-eval.test.mjs` — fixture nDCG/MRR.

Run: `cd chatvault && node --test tests/*.mjs`
