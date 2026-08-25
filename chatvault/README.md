# ChatVault — OS for your AI

Local-first vault for AI conversations and research notes. Glass look from
the Base44 app **OS for your AI**; engine and data model from this folder.

It is **not** an App Store binary and **not** a certified production release.

## What to open

```bash
cd chatvault
python3 -m http.server 4173
```

Then open http://127.0.0.1:4173/

Installable as a PWA from that origin (manifest + `sw.js`). iOS home-screen
install still requires Safari’s Share → Add to Home Screen; there is no App
Store binary.

## Engine tests

```bash
cd chatvault
node --test tests/engine.test.mjs tests/search.test.mjs tests/search-eval.test.mjs
```

## Brand marks

The CSS vault dial is gone. The product uses the owner marks copied into
`assets/` (see `assets/README.md`):

- sidebar / favicon: dark vault-door mark
- dashboard: original light-field upload
- backdrop: morph-glass grain from the Base44 skin

They are local files. The app does not hotlink `media.base44.com`.

## What this is

The live Base44 app `6a58e103fedcde66a0a7710e` is the recognized **OS for your AI**
UI (glass, conversation vault). That host is not source-controlled and is not
private. This folder is the **engine** behind the tagline:

- immutable raw text
- source AI / source file provenance
- CLAIM_LEDGER (`UNREVIEWED` … `PROVED` / `WITHDRAWN`) that never auto-PROVED
- Hybrid ranked search (BM25F + n-grams + TF-IDF + RRF + RM3) over title, claims, theorems, gaps, and raw text, with snippets
- books, tags, and artifacts derived from records (no extraction LLM)
- bulk paste and txt/md/json/csv/html ingest
- private vs professional export
- round-trip JSON restore

Base44 records were not deleted or overwritten. Claude-origin HTML archives
remain the historical baseline if/when they are exported.

## Honest limits

- No accounts, no iOS package, no paid subscription.
- Ingest is structured paste and text files, not OCR/PDF/DOCX yet.
- Demo fixtures are labeled research-memory examples, not solved theorems.
- Semantic / LLM search from the Base44 skin is intentionally absent. Hybrid RRF is in. A dense model is next only if it beats this eval.
- Jonathan’s Replit `search_engine.py` was not in this environment. See `SEARCH.md`.
