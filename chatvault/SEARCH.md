# ChatVault search engine

Aiming to be the best is the standard. This file records the hunt for the
lost component and what now ships.

## What was searched (25 August 2026)

| Place | Result |
| --- | --- |
| This workshop (`Ship_it_app`) | No `search_engine.py`. Mentions only in `docs/chatvault-audit/` as a **missing** Replit zip. |
| `simons357` GitHub | `Ship_it_app`, `ship-it-code`, `kyrana-oracle`. Zero ChatVault source. GitHub code search for `search_engine` under the user: empty. |
| Named archive | `356582767_chatvault_source2.zip` with `app.py`, `models.py`, **`search_engine.py`**, `stripe_helper.py`, `replit_auth.py`. Labelled FEATURE-SOURCE. **Not in this environment.** Stripe stays off. |
| Claude-origin / HTML V2–V7 / `/app/chatvault` | Still missing. Historical baseline if recovered. |
| Linear / Notion | MCP servers unauthenticated here. Not searched. |
| Public GitHub name collision | Other people’s products. Not Jonathan’s engine. Do not copy them. |

Public name collisions (do not merge, do not vendor):

- [rajz3006/ChatVault](https://github.com/rajz3006/ChatVault) — SQLite + Chroma + RAG for chat exports
- [marcoshernanz/ChatVault](https://github.com/marcoshernanz/ChatVault) — WhatsApp, in-browser BERT + BM25-style hybrid
- Chrome / SillyTavern / PDF exporters also named ChatVault

Web search for “search engine component for Chat Vault” and `search_engine.py ChatVault` did **not** surface Jonathan’s Replit file. The filename `search_engine.py` is generic (student Flask BM25 homework shows up). Memory of “BM25 or something” is the right *class* of algorithm. It is not a recovered file.

If the zip, Replit project, or Claude export is found: hash it, store read-only, diff it against `js/search.mjs`. Do not overwrite this engine blindly. Do not import `stripe_helper`.

## What ships now

`js/search.mjs` — `chatvault-bm25f-0.1.0`

- Fielded inverted index over title, claims, theorems, gaps, questions, actions, tags, books, summary, raw/content, source AI, ledger status, source file
- **BM25F** (Robertson / Zaragoza): per-field boost + length normalization, then IDF
- Hard match gate: AND (default), `OR` / `|`, `"phrases"`, `claim:` `theorem:` `gap:` `ai:` and aliases
- Ranked hits with scores
- Snippets with mark offsets; ledger rows keep their status in the hit
- Ledger status is **never** a ranking signal (OPEN must not sink below PROVED)
- Eval: `tests/search-eval.test.mjs` (nDCG@5 / MRR on a graded fixture)

This is Phase 1 of retrieval. It is a search engine. The previous in-memory boolean filter was not.

## What is not here yet (and should not be faked)

- Dense embeddings + RRF fusion + cross-encoder rerank (Phase 2). Needs a local model and an eval set built from *your* corpus, not SaaS seed chats.
- ChatGPT / Claude export parsers feeding the index
- Recovered Replit `search_engine.py` (still lost)

Phase 2 is allowed only when it beats BM25F on the eval set. A Semantic toggle that buries claims is a regression.
