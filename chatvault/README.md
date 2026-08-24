# ChatVault — OS for your AI

Local-first engine for the ChatVault product. This is the version-controlled
build that can actually be maintained, tested, and shown to an acquirer.

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
node --test tests/engine.test.mjs
```

## What this is

The live Base44 app `6a58e103fedcde66a0a7710e` is the recognized **OS for your AI**
UI (glass, conversation vault). That host is not source-controlled and is not
private. This folder is the **engine** that has to sit behind the tagline if
ChatVault is going to be more than a chat clipper:

- immutable raw text
- source AI / source file provenance
- CLAIM_LEDGER (`UNREVIEWED` … `PROVED` / `WITHDRAWN`) that never auto-PROVED
- fielded search (AND, OR, `"phrases"`, `claim:`, `theorem:`, `gap:`, `ai:`)
- private vs professional export
- round-trip JSON restore

Base44 records were not deleted or overwritten. Claude-origin HTML archives
remain the historical baseline if/when they are exported.

## Honest limits

- No accounts, no iOS package, no paid subscription.
- Ingest is structured paste, not OCR/PDF/DOCX yet.
- Demo fixtures are labeled research-memory examples, not solved theorems.
