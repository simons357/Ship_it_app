# ChatVault search engine

Aiming to be the best is the standard. This file records the hunt for the
lost component and what now ships.

## What was searched (25 August 2026)

| Place | Result |
| --- | --- |
| This workshop (`Ship_it_app`) | No `search_engine.py`. Mentions only in `docs/chatvault-audit/` as a **missing** Replit zip. |
| `simons357` GitHub | `Ship_it_app`, `ship-it-code`, `kyrana-oracle`. Zero ChatVault source. GitHub code search for `search_engine` under the user: empty. |
| Named archive | `356582767_chatvault_source2.zip` with `app.py`, `models.py`, **`search_engine.py`**, `stripe_helper.py`, `replit_auth.py`. Labelled FEATURE-SOURCE. **Not in this environment.** Stripe stays off. |
| Claude-origin / HTML V2–V7 / `/app/chatvault` | **Partial recover 25 Aug 2026:** React-CDN “ChatVault 2” paste archived as FEATURE-SOURCE / HISTORICAL HTML (`docs/chatvault-audit/evidence/html-snapshots/CHATVAULT_V2_REACT_CDN.html`). Substring `.includes()` search + browser Anthropic `fetch`. **Not** the live product. Other V-series HTML still missing. |
| Jonathan paste “Evernote of AI Conversations” HTML (archived 25 Aug 2026) | Recovered: `docs/chatvault-audit/evidence/html-snapshots/CHATVAULT_EVERNOTE.html`. Assistant is canned `generateAssistantResponse` if/else + `setTimeout`. Search is `.includes()` on title/preview/tags. Not an engine. |
| Live Replit app `https://chat-vault-winchesterane.replit.app/` (probed 25 Aug 2026) | **Up.** Title “Chat Vault - The Smart Repository…”. Author **Prime Field Technologies**. Last-Modified **19 Dec 2025**. SPA `/assets/index-B1k4Rveo.js` (~1.6MB). Client copy: full-text search + OpenAI summaries/tags. **No BM25 / Whoosh / MiniSearch / harmonic string in the browser bundle.** Search implementation is not in this JS; likely server-side or a simple substring. |
| Replit editor `https://replit.com/@winchesterane/Chat-Vault-2` | **`Repl not found` (404).** Profile `@winchesterane` redirects to Replit login. Not a public repo. |
| Live app ` /__repl` | Redirects to `https://replit.com/replid/71d6861a-bc89-4f3e-b8ae-5647ab8e05d4`. That UUID also **404s**. Deployed host is still up; editor source is private, renamed, or deleted. |
| Jonathan’s Mac `Downloads/chatvault_source (1)/pyproject.toml` | Seen as an open local file in Cursor. **Not on this VM.** That folder is the most likely FEATURE-SOURCE zip. Upload or attach it. |
| Public GitHub name collision | Other people’s products. Not Jonathan’s engine. Do not copy them. |

Public name collisions (do not merge, do not vendor):

- [rajz3006/ChatVault](https://github.com/rajz3006/ChatVault) — SQLite + Chroma + RAG for chat exports
- [marcoshernanz/ChatVault](https://github.com/marcoshernanz/ChatVault) — WhatsApp, in-browser BERT + BM25-style hybrid
- Chrome / SillyTavern / PDF exporters also named ChatVault

Web search for “search engine component for Chat Vault” and `search_engine.py ChatVault` did **not** surface Jonathan’s Replit file. The filename `search_engine.py` is generic (student Flask BM25 homework shows up). Memory of “BM25 or something” is the right *class* of algorithm. It is not a recovered file.

If the zip, Replit project, or Claude export is found: hash it, store read-only, diff it against `js/search.mjs`. Do not overwrite this engine blindly. Do not import `stripe_helper`.

## Stack that is actually proven (25 Aug 2026)

You asked whether a **harmonic search engine** existed, or whether someone invented it.

**Proven, in the live Base44 glass bundle** (`index-DXcRcOPA.js`):

| Piece | What it is |
| --- | --- |
| Plain search | Client-side keyword filter on the conversation list |
| Semantic search | `InvokeLLM`: “You are ranking conversations by relevance…” — an LLM reorders ids. Not BM25. Not embeddings. |
| **Harmonic Watch** | A detail-page panel. It only renders `conversation.harmonic_note` |
| `harmonic_note` | A **string field**. Ingest prompt: “a one-line cross-conversation pattern or insight this conversation resonates with (e.g. echoes the auth-refactor thread).” |
| Export evidence | Seed chat `designing_a_rate_limiter…` has `"harmonic_note": null` |

So “harmonic engine” in the glass app is **LLM-written resonance copy**, branded Harmonic Watch. It is not a ranker, not an index, and not experimental retrieval. That name collides with Harmonic Blueprint / Domain Architect research in this workshop. Easy to remember as an engine. It was not one.

Git hybrid (`chatvault-hybrid-0.2.0`) does **not** use ledger status or `harmonic_note` as a score. `status:OPEN` is a field query. PROVED vs OPEN is a label on the card. `harmonic_note` is preserved on import/export as notes and is never indexed.

**Named, source still missing (Replit Flask):** `search_engine.py` in zip `356582767_chatvault_source2.zip` / local `Downloads/chatvault_source (1)`. Live host `chat-vault-winchesterane.replit.app` advertises full-text search + OpenAI tags. No `harmonic` / `bm25` string in that public JS. Editor source is private.

If the zip lands and contains a module actually named harmonic-engine, that is new evidence. Until then: you were not crazy, and you were not given a secret ranker. You were given a field and a label.

## What BM25F does (plain language)

You do not have to learn information-retrieval jargon to use this.

- **Index:** every record is broken into words once, like a book index. Search does not reread the whole vault from scratch as a blob dump.
- **Rare words win:** `navier-stokes` matters more than `the` or `note`.
- **Field boosts:** the same word in a **title** or a **claim** outranks the same word mentioned once in a long body. That is the “F” in BM25F.
- **Length fair play:** a short title is not punished for being short; a long paste is not rewarded just for repeating a word.
- **Ranked list:** the best match is first. The old engine was a yes/no filter in store order. That is what “plain jane” felt like.
- **Phrases and fields:** `"finite-time blow-up"` must appear as that phrase. `gap:blow-up` only looks in open gaps. `ai:Claude` is provenance, not a vibe.
- **Ledger status is a label, not a score.** An OPEN gap can outrank a PROVED claim if the words match better. That is deliberate.

You type. The engine ranks. If a result looks wrong, that is a bug in the ranker — tell me the query and the record that should have won.

## What the most powerful tools are

Industry stack for a serious search box, in order:

1. **BM25F** — exact words, field boosts (title / claim beat a long body)
2. **Character n-grams + stems + one-edit typos** — you do not have to spell perfectly
3. **A second vector ranker** — TF-IDF cosine now; a MiniLM/E5 embedding later
4. **RRF (k=60)** — fuse the lists so one lucky signal cannot dominate
5. **RM3** — peek at the top hits, add their distinctive words, search again
6. **Cross-encoder rerank** — needs a local model file (~20–100MB). Not shipped until it beats this eval on *your* corpus
7. **Ask-the-vault RAG** — only with citations to immutable raw. An LLM that ranks or “summarizes away” claims is a downgrade

Evernote-style Semantic and Base44’s LLM toggle are (7) without (1)–(5). That is not “more powerful.”

## What ships now

`js/search.mjs` — `chatvault-hybrid-0.2.0`

- Fielded inverted index
- BM25F + stem + one-edit typo matching
- Character 3-gram BM25
- Field-weighted TF-IDF cosine
- Reciprocal Rank Fusion (k=60)
- RM3 expansion from the top hits
- Hard match gate: AND, `OR`, `"phrases"`, `claim:` / `theorem:` / `gap:` / `ai:`
- Snippets; ledger status shown and never used as a score
- `harmonic_note` stored as notes, never scored
- Eval: `tests/search-eval.test.mjs`

## What is not here yet (and must not be faked)

- Dense MiniLM/E5 + cross-encoder (needs a vendored model and your real corpus)
- ChatGPT / Claude export parsers feeding the index
- Recovered Replit `search_engine.py` (still lost)
- **E8 / lattice ranking** — see below; not shipped

A Semantic toggle that buries claims is a regression. The dense layer plugs into the same RRF when it earns its place.

## EXPERIMENTAL / not shipped — E8 lattice ranking

Searched this PR (`chatvault/`, `docs/chatvault-audit/`, `SEARCH.md`, `js/search.mjs`), git history of those paths, Base44 glass bundle strings, and the Grok ChatVault research hunt.

**Result:** no ChatVault design note proposed E8 (or any root lattice) as a retrieval ranker. The live “harmonic” surface is Harmonic Watch printing `harmonic_note`. Hybrid eval has no E8 signal and no owner-corpus numbers that could justify one.

E8 → H4 folding geometry exists in a **different book** (swirl/geometry session). It is **not** a ChatVault feature. Do not implement E8 ranking unless it clearly beats `chatvault-hybrid-0.2.0` nDCG/MRR on Jonathan’s real vault (that eval set is not here; it will not appear by wishing). Label if revived: **EXPERIMENTAL / not shipped**.

## Recovered “ChatVault 2” HTML (25 Aug 2026)

Jonathan pasted a single-file React-in-HTML titled **ChatVault - AI Conversation Organizer** (CDN Tailwind + React 18 UMD + Babel + Lucide, purple gradient, `localStorage` `chatVaultChats` / `chatVaultProjects`).

That file is **FEATURE-SOURCE / HISTORICAL HTML**, not the live product. Snapshots and triage:

- `docs/chatvault-audit/evidence/html-snapshots/CHATVAULT_V2_REACT_CDN.html`
- `docs/chatvault-audit/CHATVAULT2-TRIAGE.md`

Its search box is `useMemo` + `.includes()` on summary/content/tags/keywords — a boolean filter, not BM25F. Its ingest `fetch("https://api.anthropic.com/v1/messages")` from the browser (no API key in headers) is a defect and is forbidden to ship. A companion “PRODUCTION-READY MVP REVIEW” (DOMPurify, Stripe, Product Hunt, 85% ready, $100K–$1M Year 1) is untrusted marketing about a different/imagined build.

Do not replace this hybrid engine or the glass look with that prototype. Stripe stays off. Projects in that paste are already Books here.

## Prototype dump 3 — Evernote HTML

Archived 25 August 2026 at `prototypes/chatvault-evernote-prototype.html` (notes: `prototypes/EVERNOTE.md`). Third paste. Distinct from ChatVault 2, Base44 glass, and Replit. Not the live product.

Search is `title` / `preview` / `tags` `.includes()` plus a platform select and All vs Starred. No inverted index. The floating 🤖 assistant is `setTimeout(1000)` plus keyword if/else. Its COPY claims Advanced search, `tag:work platform:chatgpt`, folders, archive, PDF export, Cmd+F, and right-click — none of that is in the HTML.

Do not port substring-only search, the “Evernote of AI Conversations” tagline (conflicts with locked **OS for your AI**), or the canned assistant as product. Canonical search remains `chatvault-hybrid-0.2.0`. Canonical look remains glass.

ChatVault 2 files were not overwritten. Live `index.html` / `app.js` / `engine.mjs` / `search.mjs` were not replaced with this dump.
