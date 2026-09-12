# ChatVault — evidence report for Claude

**Prepared:** 26 August 2026  
**Handed by:** Jonathan (owner). This document is the briefing.  
**Repo / branch:** `github.com/simons357/Ship_it_app` @ `cursor/chatvault-build-a44c`  
**HEAD at writing:** `41817c1bb71affa2208c04159986120bb2fc1b8b` (“Fix steel-vault primary button ink and bump PWA cache to 0.4.1”) plus this report commit.  
**PR:** https://github.com/simons357/Ship_it_app/pull/33  
**Audience:** a skeptical reviewer who will look for overclaims, vaporware, and mixed products.

This report is ChatVault only. It does not discuss other workshop tracks. It does not certify production, App Store, patents, revenue, or scientific results. Where a claim is made, the file that would falsify it is named.

**What this is, in one sentence:** a real local hybrid information-retrieval engine with a human claim ledger, plus a local PWA, plus an older hosted look demo that is a different schema.

---

## A. What ChatVault is / is not

### Two surfaces (do not collapse them)

| Surface | What it actually is | Where |
| --- | --- | --- |
| **Git PWA (this PR)** | Local-only static app: `index.html` + ES modules. Steel-vault skin (solid charcoal, sharp type, amber accent, no `backdrop-filter`). Engine: `ChatVaultEntry`, `CLAIM_LEDGER`, hybrid ranker `chatvault-hybrid-0.2.0`. | `chatvault/` served with `python3 -m http.server 4173` → `http://127.0.0.1:4173/` |
| **Base44 glass preview** | Hosted React SPA with morph-glass UI. Tagline **OS for your AI**. Entity model is `Conversation` / `Book` / `Artifact`, **not** `ChatVaultEntry`. Seed chats look like SaaS demos. Preview is unauthenticated and writable. | https://preview--6a58e103fedcde66a0a7710e.base44.app/ — app id `6a58e103fedcde66a0a7710e`. Do **not** send `app.base44.com/.../editor/preview` (login wall). Published host `https://6a58e103fedcde66a0a7710e.base44.app/` 404s. |

Jonathan reversed the morph-glass look lock on 25 August 2026. Git chrome is steel vault. Base44 is still glass. Same tagline on both: **OS for your AI**. That is branding, not an operating-system claim.

A 24 August audit (`docs/chatvault-audit/MASTER-AUDIT.md`) labelled the Base44 preview `CANONICAL-CANDIDATE` for *look*. That label is dated. Current git decisions (`chatvault/DECISIONS.md`) keep glass as an archived Base44 look and treat `chatvault/` as the canonical engine and data model. Do not quote the 24 August look lock as current.

### Tagline

Locked product line: **OS for your AI**.  
Earlier public copy used “Evernote of AI conversations.” That line belongs to a historical HTML dump (`docs/chatvault-audit/CHATVAULT-EVERNOTE-TRIAGE.md`). It is not the live tagline.

### Local-only

The git app stores records in the browser (`localStorage` keys `chatvault.engine.v1` and `chatvault.books.extra.v1`). There is no ChatVault cloud account in this engine. There is no auth. There is no hosted git deploy.

### Not App Store

README, Privacy view, and this PR state the same limit: no signed iOS binary, no Apple submission, no Capacitor wrapper of Base44. iOS home-screen install, if used, is Safari Share → Add to Home Screen against a local origin.

### Stripe off

No Stripe client, no `stripe_helper`, no checkout. A missing Replit zip is labelled FEATURE-SOURCE and is instructed not to import billing. A pasted “PRODUCTION-READY MVP REVIEW” that talks about Stripe and Year-1 revenue is untrusted marketing about a different or imagined build (`docs/chatvault-audit/evidence/html-snapshots/PRODUCTION-READY-MVP-REVIEW.paste.md`). Do not treat it as a description of this tree.

### What it is not

- Not a truth engine, verifier, or journal.
- Not an LLM app. The git UI never calls a model (`connect-src 'self'`; no `fetch` to Anthropic/OpenAI in `chatvault/js/`).
- Not the lost Replit Flask `search_engine.py`.
- Not public GitHub projects that collide on the name ChatVault (other people’s RAG/WhatsApp tools).
- Not Base44 candidates 2 and 3 (Drive landing page; empty Paper Vault).
- Not ChatVault 2 React-CDN HTML, not the Evernote-tagline HTML.

---

## B. Status as of 26 August 2026

| Fact | Evidence |
| --- | --- |
| Working **local prototype** | `cd chatvault && python3 -m http.server 4173`. Not a hosted product. |
| Tests | `cd chatvault && node --test tests/*.mjs` → **32/32 pass, 0 fail** (re-run 26 Aug 2026 on this HEAD). |
| Draft PR | https://github.com/simons357/Ship_it_app/pull/33 — `isDraft: true`, base `main`, head `cursor/chatvault-build-a44c`. Title at writing: “ChatVault steel-vault skin; hybrid engine unchanged.” |
| Not hosted | No Vercel/production URL for the git app. `primefield.tech/chatvault` was an in-app 404 on 24 Aug 2026. Published `*.base44.app` hosts 404. |
| Steel-vault skin on git | `chatvault/css/app.css` (`--bg: #101112`, `--accent: #ffbf1a`). PWA cache name `chatvault-engine-v0.4.1` in `chatvault/sw.js`. Asset query `?v=0.4.1` on CSS/JS in `index.html`. |
| Base44 still glass | Preview host above; freeze hashes in `docs/chatvault-audit/VERSION-MANIFEST.json` (JS SHA-256 `720a21e0e061997909f4ea6ca85caeff60a08af8b1d5157081746a76ff6ba8de`, 1,150,051 bytes, bundle `index-DXcRcOPA.js`). If that hash changed, the freeze is stale. |
| Schema / search versions | `SCHEMA_VERSION = "chatvault-engine-0.2.0"` (`engine.mjs`). `SEARCH_ENGINE_VERSION = "chatvault-hybrid-0.2.0"` (`search.mjs`). These are **not** the PWA cache `0.4.1`. Three version strings; do not conflate them. |
| Fixtures, not owner corpus | Git ships three demo entries (Euler identity, Navier–Stokes status note, private clinical fragment). Search eval uses a seven-document graded fixture. Neither is Jonathan’s research archive. |
| Claude-origin 2025 source | Still not in this workshop. Label: historical baseline, unlocated. |
| Replit `search_engine.py` | Still missing. Live host `chat-vault-winchesterane.replit.app` was up on 25 Aug 2026 with full-text/OpenAI copy in the public JS; editor source 404s. That host is not this git engine. |

Honest status line: **a tested local prototype on a draft PR, not a shipped service.**

---

## C. Data model

### Git: `ChatVaultEntry` (`chatvault/js/engine.mjs` `emptyEntry`)

Every record is normalized through `emptyEntry`. Extra hostile keys on ledger rows are dropped (`onclick` etc. are not copied).

| Field | Role |
| --- | --- |
| `schema_version` | `chatvault-engine-0.2.0` |
| `id` | Sanitized `^[A-Za-z0-9._-]{1,80}$` or regenerated |
| `title` | Display title |
| `source_type` | `conversation` \| `markdown` \| `json` \| `pdf` \| `docx` \| `image` \| `csv` \| `code` \| `html` \| `other` — enum exists; **ingest of pdf/docx/image is not implemented** |
| `source_ai` | `ChatGPT` \| `Claude` \| `Grok` \| `Base44` \| `human` \| `unknown` |
| `source_file` | Filename when ingested from a file |
| `raw_content` | **Immutable** after ingest. `updateEntry` throws if patched. Summaries are forbidden from equalling raw. |
| `content_text` | Body after structured-line parse (or a copy of raw) |
| `summary` | Optional. Must not replace raw. |
| `key_claims` / `theorems` / `open_gaps` | Ledger arrays of `{id, text, status, human_reviewed}` |
| `action_items` / `open_questions` | String arrays (not ledger-statused except artifacts treat actions as `OPEN`) |
| `related_projects` | Books |
| `search_tags` / `project_tags` / `project_category` | Tags / project |
| `visibility` | `private` \| `professional` (default professional) |
| `starred` / `archived` | Booleans |
| `harmonic_note` | Preserved on import/export as notes. **Not indexed. Not scored.** |
| `item_date` / `ingested_at` / `updated_at` | Dates |

Structured paste lines (optional): `TITLE`, `SUMMARY`, `SOURCE_AI`, `SOURCE_TYPE`, `SOURCE_FILE`, `VISIBILITY`, `PROJECT`, `TAG`, `BOOK`, `CLAIM`, `THEOREM`, `GAP`, `ACTION`, `QUESTION`. Unmatched lines remain in the body. `CLAIM:` starts `UNREVIEWED`. `GAP:` starts `OPEN`. Nothing on ingest is `PROVED`.

### Immutable `raw_content`

`ingestPaste` always stores the original paste as `raw_content`. Tests: “ingest keeps raw text and will not let a summary replace it”; “raw_content is immutable after ingest.”

### `CLAIM_LEDGER` statuses

```
UNREVIEWED, OPEN, CONJECTURAL, NUMERICAL, CONDITIONAL, PROVED, WITHDRAWN
```

Unknown statuses become `UNREVIEWED`.

### Never auto-`PROVED`

`assertNotAutoProved(status, { humanReviewed })` rewrites `PROVED` to `UNREVIEWED` unless `humanReviewed` is true. Ingest, import, and `reviewLedgerItem(..., { humanReviewed: false })` cannot keep auto-`PROVED`. Import of a poisoned export with `status: "PROVED"` and `human_reviewed: false` becomes `UNREVIEWED`. The UI review `<select>` passes `humanReviewed: true` — that is the only path to `PROVED` in this app. `PROVED` here means “a person marked it proved inside this vault,” not that a journal agrees (`renderDisclaimer` in `app.js`).

### Books / projects

Books are `related_projects` strings plus optional extra names in `localStorage`. `(unfiled)` is the bucket for records with no book. This is not a second database.

### Provenance `SOURCE_AI`

First-class enum on the entry. Ingest form default `unknown` does not clobber a `SOURCE_AI:` line in the paste; a non-unknown form choice does. Test: “form defaults do not clobber SOURCE_AI structured lines.”

### Contrast: Base44 `Conversation` schema

Frozen export of seed chat “Designing a rate limiter…” (`docs/chatvault-audit/evidence/exports/designing_a_rate_limiter_that_won_t_break_the_api.json`):

| Base44 `Conversation` | Git `ChatVaultEntry` |
| --- | --- |
| `title`, `summary`, `labels`, `project`, `book_ids`, `starred` | Rough analogues exist |
| `source: "pasted"` | Git has `source_ai` + `source_type` |
| `clean_content` holds User/Assistant text | Git `content_text` / `raw_content` |
| **`raw_content`: `null`** on that export | Git treats null-raw as a defect of B, not a feature |
| `harmonic_note`: `null` | Git stores the string, never scores it |
| `readiness_score`: 85 | **Absent** in git. Not a ranker. |
| `is_sample`: false on SaaS-looking seed | Misleading if treated as owner research |
| No claims / theorems / gaps / ledger | Git has them |
| `created_by_id`: service principal | Git has no accounts |

Base44 also has Semantic search (`InvokeLLM` id reorder) and a Harmonic Watch panel that prints `harmonic_note`. Those are glass features. They are not the git ranker.

---

## D. Functions (what the UI actually does)

Source of UI behavior: `chatvault/js/app.js`. Views: vault, detail, ingest (single / bulk / files), books, tags, artifacts, dashboard, export, guide, privacy, disclaimer.

### What it does

| Surface | Behavior |
| --- | --- |
| **Ingest — single** | Paste → `ingestPaste`. Structured lines optional. Source AI, visibility, optional book from the form. No LLM. Lands on detail. |
| **Ingest — bulk** | Chunks split on a line of `---` or `===`. Per-chunk errors are counted, not silent. |
| **Ingest — files** | `.txt .md .markdown .json .csv .html .htm` only. ChatVault export JSON restores a bundle. Other text becomes a new entry with `source_file` set. `.png` throws. |
| **Search** | Calls `searchVault`. AND by default; `OR` / `\|`; `"phrases"`; `field:term` (`claim:`, `gap:`, `ai:`, …). Filters: starred, visibility, source AI, source type, project, book, tag chips. Pagination 50. Scores and matched fields shown while querying. Snippets with `<mark>`. Empty vault copy is distinct from “no matches” and from the render error boundary. |
| **Vault list** | Cards: source AI, visibility, a ledger badge, star, title, summary-or-snippet, tags. |
| **Ledger UI** | Detail page lists claims / theorems / gaps with a status `<select>`. Human review path. Raw content in a `<pre>`. |
| **Export** | Full vault JSON (`format: "chatvault-export"`). Professional export omits `visibility=private`. Per-record JSON from detail. Restore from JSON replaces the store. |
| **Tags** | Derived from `search_tags` + `project_tags`. Add/remove on detail. Tags view lists unique tags and their conversations. |
| **Starred** | Toggle on card/detail; starred filter on vault. |
| **Books** | List + “new book” prompt + assign on detail. Opening a book filters the vault. |
| **Artifacts** | Flattened claims/theorems/gaps/actions. **Derived from records. No extraction LLM.** |
| **Dashboard** | Counts: total, starred, private, claims, theorems, gaps; bars by source AI, ledger status, project. Not a readiness score. |
| **Guide** | Explains provenance + retrieval; search syntax; states ChatVault 2 HTML is not this product. |
| **Privacy** | Local-first disclosure; wipe-all. |
| **Disclaimer** | “Not a truth engine.” |

### What it does **not** do

| Missing | Notes |
| --- | --- |
| Official ChatGPT / Claude zip parser | No conversations.json walker. Generic text/JSON only. A ChatGPT export that is not `format: "chatvault-export"` is ingested as a pasted JSON blob. |
| Auth / accounts / RLS | Local-only. No two-user isolation. |
| PDF / DOCX / OCR | Enum lists `pdf`/`docx`/`image`; file ingest rejects them. |
| LLM in the git app | Banner: “No LLM is called.” CSP forbids CDN and third-party `connect`. |
| Google Drive import | That is Base44 candidate 2. |
| Media ingest | Glass has a media UI (partial). Git does not. |
| Semantic / LLM rank toggle | Intentionally absent from git. Present on glass as `InvokeLLM`. |
| Stripe / subscriptions | Off. |
| Hosted multi-device sync | Export/restore is the portability story. |
| MiniLM / E5 / cross-encoder | Documented as future only if it beats this eval on a real corpus. Not shipped. |

---

## E. Search engine — fine details for a skeptic

**Version:** `chatvault-hybrid-0.2.0` (`export const SEARCH_ENGINE_VERSION` in `chatvault/js/search.mjs`).

**File:** `chatvault/js/search.mjs` (~890 lines). Re-exported from `engine.mjs`.

This is a classical hybrid lexical stack. It is not embeddings. It is not an LLM. It is not the missing Replit module.

### Ordered pipeline (`searchVault`)

1. **Parse** — `parseQuery`: empty / AND / OR (` OR ` or ` | `). Terms and `"phrases"` with optional `field:` prefix. Aliases: `raw|body|text` → `content`; `claims` → `claim`; `all` → `all`; etc.
2. **Index** — `buildIndex` unless a caller reuses one. Per-field tokens, TFs, character 3-grams, DF / stem-DF / ngram-DF, field-weighted TF-IDF vectors.
3. **Filters** — archived (hidden unless `includeArchived`), visibility, `source_ai`, `source_type`, project, starred, tag, book / `(unfiled)`.
4. **Match gate** — boolean. AND of terms/phrases (OR of clauses). A term is present if substring, exact token, stem match (stem length ≥ 4), or one-edit typo (term length ≥ 4). Phrases are exact substring of the field haystack. **No ranking if the gate fails.** Empty query skips scoring and returns store order at score 0.
5. **Three ranked lists, independently:**
   - **BM25F** on words (with stem / substring-TF / one-edit TF discounts) over allowed fields.
   - **Character 3-gram BM25** (`NGRAM = 3`).
   - **Field-weighted TF-IDF cosine** of query terms vs the document vector.
6. **RRF** — `reciprocalRankFusion(lists, k=60)`: score `1/(k + rank)` per list, summed. `k = 60` (`RRF_K`).
7. **RM3** — take up to two docs with BM25 ≥ 60% of the top BM25; pull up to three distinctive terms from `content` and `claim` (df cap; claim weight 1.4); score those as an `expanded` list; **fuse again** over four lists (bm25, ngram, cosine, expanded).
8. **Display score** — `rrf * 100 + tieBreak(ingested_at)` where tie-break is `Date.parse(ingested_at)/1e15` (tiny). Sort by that score, then title.

Constants: `K1 = 1.2`. Phrase bonus `2.4` on BM25F. Substring TF weight `0.4`. Stem TF `0.85`. Fuzzy TF `0.65`. Snippet window 220 characters. Snippets are **display**; a `+0.25` when a snippet has a ledger status affects snippet *ordering*, not document rank.

### Field boosts (`SEARCH_FIELDS`)

| Field | boost | b (length norm) | In unfielded rank (`RANK_FIELDS`)? |
| --- | --- | --- | --- |
| `title` | 4.0 | 0.4 | yes |
| `claim` | 3.6 | 0.5 | yes |
| `theorem` | 3.6 | 0.5 | yes |
| `gap` | 3.2 | 0.5 | yes |
| `tag` | 3.0 | 0.3 | yes |
| `ai` | 2.8 | 0.2 | yes |
| `question` | 2.4 | 0.5 | yes |
| `status` | 2.4 | 0.2 | **no** |
| `book` | 2.2 | 0.3 | yes |
| `action` | 2.0 | 0.5 | yes |
| `summary` | 1.6 | 0.7 | yes |
| `source` | 1.4 | 0.3 | yes |
| `content` | 1.0 | 0.75 | yes |

`RANK_FIELDS` is `SEARCH_FIELDS` minus `status`. Unfielded queries score only `RANK_FIELDS`. `status:OPEN` is a **field query** (match gate + BM25F on the status field). `PROVED` is not a quality boost. Test: “status: remains a field query and is not an unfielded quality boost”; “OPEN can outrank PROVED”.

`fieldText(..., "all")` concatenates title, content, summary, ai, source, tag, claim, theorem, gap, question, action, book. It does **not** include `harmonic_note` or `status`. Status tokens still enter the inverted index because `entryFields` builds a `status` field for `status:` queries. That can move document-frequency of the token `open` slightly. It is not a per-document PROVED multiplier.

### Typo / stem rules

**Stem** (`stem()`): words of length ≤ 4 unchanged. Else suffix rules: `ational`→`ate`, `tional`→`tion`, `ies`→`y`, `sses`→`ss`, trailing `s` (not `ss`, length > 4), `ing` (length > 6) then optional doubled-consonant trim, `ed` (length > 5) similarly, `er` (length > 6). This is a small in-house stemmer, not Porter in full.

**Typos:** `editDistanceAtMost(a,b,1)` — substitution or single insertion/deletion. Applied when the query term length is ≥ 4 and token lengths differ by at most 1. Weighted `FUZZY_TF = 0.65`.

**Substring:** if no exact TF, count of tokens that `includes(term)`, times `0.4`.

Tests: `eulr identity` still ranks Euler first; `rate limiters` finds the limiter note.

### What is NEVER a score

| Signal | Treatment |
| --- | --- |
| Ledger status | Label on the card / snippet. `status:` is a filter-like field query. Not an unfielded quality term. |
| `harmonic_note` | Not in `SEARCH_FIELDS`. Not in `fieldText("all")`. Test: identical scores with and without a note that repeats the query. |
| E8 / lattice / geometry rankers | **Not implemented.** `docs/chatvault-audit/EXPERIMENTAL-NOT-SHIPPED.md`. Comment in `search.mjs`: “E8 / lattice ranking is not implemented.” Do not invent one from other workshop notes. |

### Harmonic Watch is ingest copy on Base44, not a ranker

Live glass bundle (`index-DXcRcOPA.js`, freeze 24 Aug 2026): Harmonic Watch is a detail panel that renders `conversation.harmonic_note`. Ingest prompt asks the model for “a one-line cross-conversation pattern…”. Seed export has `"harmonic_note": null`. Semantic search on glass is `InvokeLLM` with a prompt to rank conversation ids — **not BM25, not embeddings**. Using that toggle as “better search” is a **regression** relative to `chatvault-hybrid-0.2.0`.

### Eval: fixture nDCG, **not** Jonathan’s corpus

`chatvault/tests/search-eval.test.mjs` builds seven synthetic documents and ten queries. Grades: 3 = intended, 2 unused in this set, 1 = incidental mention. The test asserts each topic’s first hit is grade 3, each nDCG@5 ≥ 0.9, mean nDCG@5 ≥ 0.9, mean MRR ≥ 0.9. A second test shows store-order boolean would rank an incidental “Euler” mention first; BM25F ranks the title hit first.

This is **not** an owner-corpus evaluation. A skeptic should attach real chats before believing retrieval quality beyond this toy set. The file itself says so in a comment.

### Lost Replit `search_engine.py` is still missing

Do not treat this JS engine as a recovery of that file. Hunt record: `chatvault/SEARCH.md`. Named zip `356582767_chatvault_source2.zip` (with `app.py`, `models.py`, `search_engine.py`, `stripe_helper.py`, `replit_auth.py`) was **not in this environment**. GitHub user `simons357` public repos did not contain it. If the zip appears later: hash it, store read-only, diff against `js/search.mjs`. Do not overwrite blindly. Do not import `stripe_helper`.

### Base44 Semantic = `InvokeLLM` id-reorder = regression vs this

Glass: LLM reorders ids. No inverted index, no BM25F, no field operators, no snippets in the 24 Aug exercise. Git hybrid is the stronger lexical stack of the two **on the fixture**. That is not a claim about production IR at web scale.

### Evernote HTML and ChatVault 2 = substring `.includes()`

| Dump | Search | Ingest | Status |
| --- | --- | --- | --- |
| ChatVault 2 React-CDN | `summary/content/tags/keywords` `.includes()` in array order | Browser `fetch("https://api.anthropic.com/v1/messages")` **without API key** — defect; forbidden to ship | Archived: `docs/chatvault-audit/evidence/html-snapshots/CHATVAULT_V2_REACT_CDN.html` |
| Evernote-tagline HTML | `title` / `preview` / `tags` `.includes()`. Assistant COPY mentions `tag:work platform:chatgpt`; **the filter does not parse it.** | Modal paste. No `localStorage`. Reload wipes. Floating 🤖 is `setTimeout(1000)` + keyword if/else, not Claude. | Archived: `CHATVAULT_EVERNOTE.html` and `chatvault/prototypes/` |

Neither dump is the live product. Git CSP (`default-src 'self'`, no `unsafe-eval`) **cannot load** Tailwind/React/Babel CDNs. That is a reason not to merge them, not a reason to loosen CSP.

The companion “PRODUCTION-READY MVP REVIEW” (85% ready, Stripe, Product Hunt, $100K–$1M) does not describe this repository or the HTML that followed.

---

## F. Security / CSP

`chatvault/index.html` meta CSP (single line, quoted from HEAD):

```
default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; connect-src 'self'; worker-src 'self'; base-uri 'none'; form-action 'none'; object-src 'none'
```

Consequences:

- No unpkg / jsdelivr / Google Fonts / Tailwind CDN. ChatVault 2 and Evernote HTML **will not execute** under this policy (they need CDN scripts and Babel `unsafe-eval`).
- No browser Anthropic/OpenAI `fetch`. `connect-src 'self'` blocks it even if someone pasted a call.
- Images: local + `data:`. Base44 media URLs are not hotlinked.
- `script-src 'self'` only — no inline script except none; app is `type="module"` from `./js/app.js`.
- XSS: UI uses `escapeHtml` on interpolated strings. Import sanitizes ledger ids. Tests cover poisoned ids and extra keys. This is not a full security audit.

**Base44 preview (glass) is a different posture:** no login on the preview host; this workshop ingested a probe record without credentials (`MASTER-AUDIT.md` D1, S0). Treat that host as a **public demo**, not a private vault. Git localStorage is private to the browser profile, not to a multi-user ACL.

Service worker (`chatvault/sw.js`): cache name `chatvault-engine-v0.4.1`; `skipWaiting` + `clients.claim`; deletes other cache names on activate; network-first GET with cache fallback. A stale SW can keep old JS. Pressure-test with a hard refresh after cache bumps.

No Stripe keys in repo. Replit `stripe_helper.py` absent. Do not enable.

---

## G. Honest gaps and how a skeptic should pressure-test

### Gaps (not a complete list)

- No owner corpus in git. Eval nDCG is fixture-only.
- No ChatGPT zip / official export parser.
- No auth, no hosted deploy, no sync.
- No PDF/OCR.
- No dense retrieval. Cross-encoder not shipped.
- `search_engine.py` not recovered — origin story of “BM25 or something” is class-of-algorithm, not a file.
- Base44 source not in git (API 401 from this workshop). Glass data not migrated.
- Claude-origin 2025 files unlocated.
- `localStorage` will quota-fail on a large vault; freeze triage already flags this.
- Stemmer is ad hoc; one-edit only; no language-aware tokenization beyond a custom split (keeps `π`, `∞`, some math punctuation).
- `source_type` includes pdf/docx/image in the enum while ingest cannot accept them — enum ahead of implementation.
- Workshop lives in `Ship_it_app`, which is not a dedicated ChatVault product repo.
- Draft PR, not merged. Not production-ready. Not App Store. Not “best in the world.”

### Pressure tests (do these; they are cheap)

1. **Attach a real corpus.** Replace fixtures. Re-run `node --test tests/*.mjs`. Add queries you care about. Fixture nDCG ≥ 0.9 does not transfer automatically.
2. **`claim:` / `gap:` / `"phrase"` / `OR`.** Confirm field queries do not leak (birthday “blow-up” vs `gap:blow-up`). Code already tests this on fixtures; repeat on your data.
3. **Confirm OPEN can outrank PROVED.** Create a well-matching OPEN gap and a weakly matching PROVED claim. Query the gap language. First hit should be the OPEN record if the words match better. If PROVED wins because it is PROVED, that is a bug — report query + ids.
4. **Confirm `harmonic_note` does not move rank.** Put the query only in `harmonic_note`. The document must not match (gate uses indexed fields). Putting a redundant note on an already-matching doc must not change `score`.
5. **Hard-refresh the SW.** After pulling `0.4.1`, unregister or hard-reload so `chatvault-hybrid-0.2.0` actually loads. The vault header prints `SEARCH_ENGINE_VERSION` when idle/searching — read it.
6. **Professional export.** Keep a `visibility=private` record. `chatvault-professional.json` must omit it. Search with `{ visibility: "professional" }` must not return the clinical mnemonic.
7. **Auto-PROVED.** Paste `CLAIM: ...` and inspect status: `UNREVIEWED`. Import JSON with `PROVED` + `human_reviewed: false` — must become `UNREVIEWED`.
8. **Do not run ChatVault 2 under this origin.** CSP should block CDNs. Do not relax CSP to make the prototype boot.
9. **Do not treat glass Semantic as an upgrade.** If someone enables it on Base44, they replaced ranking with an LLM id list.

If a result looks wrong, the ranker is a bug in `search.mjs`, not a vibe. Send the query and the record that should have won.

---

## H. File map

Paths relative to repo root on `cursor/chatvault-build-a44c`.

### Git app (`chatvault/`)

| Path | Role |
| --- | --- |
| `chatvault/index.html` | Shell, CSP, `?v=0.4.1` |
| `chatvault/sw.js` | PWA cache `chatvault-engine-v0.4.1` |
| `chatvault/manifest.webmanifest` | PWA name “ChatVault — OS for your AI”, theme `#101112` |
| `chatvault/css/app.css` | Steel-vault skin |
| `chatvault/js/app.js` | UI |
| `chatvault/js/engine.mjs` | Schema, ingest, ledger, store, export |
| `chatvault/js/search.mjs` | Hybrid ranker |
| `chatvault/tests/engine.test.mjs` | Ingest / ledger / export / store |
| `chatvault/tests/search.test.mjs` | Ranker unit tests |
| `chatvault/tests/search-eval.test.mjs` | Fixture nDCG/MRR |
| `chatvault/README.md` | How to run |
| `chatvault/SEARCH.md` | Hunt + stack honesty |
| `chatvault/DECISIONS.md` | Look/engine split |
| `chatvault/FEATURE-MATRIX.md` | A/B/C/git columns |
| `chatvault/FREEZE-TRIAGE.md` | Editor freeze vs preview |
| `chatvault/OWNER-FILL-IN.md` | Owner identity notes |
| `chatvault/assets/` | Local marks (not Base44 hotlink) |
| `chatvault/prototypes/chatvault-evernote-prototype.html` | Historical dump 3 |
| `chatvault/prototypes/EVERNOTE.md` | Triage of dump 3 |

### Audit packet (`docs/chatvault-audit/`)

| Path | Role |
| --- | --- |
| `docs/chatvault-audit/CHATVAULT-REPORT-FOR-CLAUDE.md` | This file |
| `docs/chatvault-audit/MASTER-AUDIT.md` | 24 Aug freeze (look-lock dated) |
| `docs/chatvault-audit/VERSION-MANIFEST.json` | Hashes, labels |
| `docs/chatvault-audit/GROK-RESEARCH-HUNT.md` | Harmonic Watch vs ranker; missing files |
| `docs/chatvault-audit/EXPERIMENTAL-NOT-SHIPPED.md` | E8 not in product |
| `docs/chatvault-audit/CHATVAULT2-TRIAGE.md` | React-CDN HTML |
| `docs/chatvault-audit/CHATVAULT-EVERNOTE-TRIAGE.md` | Evernote-tagline HTML |
| `docs/chatvault-audit/HANDOFF.md` | Owner return notes (parts pre-steel-vault) |
| `docs/chatvault-audit/evidence/exports/` | Base44 Conversation JSON |
| `docs/chatvault-audit/evidence/html-snapshots/` | C1/C2/C3 previews; V2; Evernote |
| `docs/chatvault-audit/evidence/hashes/SHA256SUMS.txt` | Bundle hashes |
| `docs/chatvault-audit/evidence/screenshots/` | 24 Aug visual log |

### Not in this tree (named so they are not assumed present)

- `search_engine.py` / `356582767_chatvault_source2.zip`
- Claude-origin `/app/chatvault`, `CHATVAULT_V7.html`
- Dedicated `chatvault` GitHub product repo
- Hosted git PWA

---

## Appendix: test command and count

```bash
cd chatvault
node --test tests/*.mjs
```

Result on 26 August 2026 against this branch:

```
# tests 32
# pass 32
# fail 0
```

Breakdown: 14 engine tests, 15 search unit tests, 3 search-eval tests.

---

## Appendix: claims this document refuses

Do not tell a reviewer any of the following:

1. Production-ready, complete OS, or App Store binary.
2. Best search engine in the world / Millennium-adjacent / scientific proof.
3. Recovered Replit `search_engine.py`.
4. Base44 Semantic is stronger than hybrid RRF.
5. Harmonic Watch is a ranker.
6. E8 ranking ships.
7. Evernote HTML or ChatVault 2 is the live product.
8. Fixture nDCG is Jonathan’s corpus.
9. `raw_content` is preserved on Base44 (the frozen export had `null`).
10. Stripe, revenue, 85% ready, or Product Hunt (untrusted paste).
11. `v1.19` (unverified).
12. `primefield.tech/chatvault` is live.

**Acceptable claim:** ChatVault, as of 26 August 2026, is a real local hybrid IR engine with a human claim ledger, plus a steel-vault PWA in this git tree, plus an older hosted morph-glass look demo on Base44 that uses a different schema and must not be mixed into the engine story.
