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
- Eval: `tests/search-eval.test.mjs`

## What is not here yet (and must not be faked)

- Dense MiniLM/E5 + cross-encoder (needs a vendored model and your real corpus)
- ChatGPT / Claude export parsers feeding the index
- Recovered Replit `search_engine.py` (still lost)

A Semantic toggle that buries claims is a regression. The dense layer plugs into the same RRF when it earns its place.
