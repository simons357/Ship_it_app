# Grok ChatVault research hunt

**Date:** 25 August 2026 (re-opened same day)  
**Trigger:** Jonathan: “found something else on chatvault research in grock” (xAI Grok; typo *grock*). Follow-up: take ChatVault only; you look like Grok — strip non-ChatVault stuff. Exception: check whether E8 was discussed as **experimental** when they designed a **“harmonic search engine”** for ChatVault.

**Dump found.** Not a grok.com HTML/JSON export on this VM. The salvageable dump is the ChatVault-as-search-engine design already in this PR, plus live Base44 Harmonic Watch evidence. No E8 ranker spec.

Locked product (unchanged):

- Look: Base44 morph-glass https://preview--6a58e103fedcde66a0a7710e.base44.app/ — tagline **OS for your AI**
- Engine: `chatvault/` ChatVaultEntry, CLAIM_LEDGER never auto-PROVED, hybrid search `chatvault-hybrid-0.2.0`
- Stripe off. No browser Anthropic. No Clay/NS/RH/Nav42/Overleaf claims in ChatVault.

---

## Salvage (ChatVault only)

| Item | What it is | Where |
| --- | --- | --- |
| ChatVault-as-search-engine | Hybrid ranker: BM25F + n-grams + TF-IDF + RRF(k=60) + RM3. Lost Replit `search_engine.py` still missing. | `chatvault/js/search.mjs`, `chatvault/SEARCH.md` |
| Harmonic Watch / `harmonic_note` | Live glass **panel that prints an LLM ingest string**. Not a ranker, not an index. Git hybrid does not score it. Field kept on import/export as notes. | Base44 `index-DXcRcOPA.js`; `SEARCH.md` “Stack that is actually proven”; `engine.mjs` `harmonic_note` |
| E8 as experimental retrieval | **Not found** as a ChatVault design note. Archive only: **EXPERIMENTAL / not shipped**. Do not implement. Would need to beat hybrid eval on Jonathan’s corpus (no such eval here). | `chatvault/SEARCH.md` EXPERIMENTAL section; `EXPERIMENTAL-NOT-SHIPPED.md` |

## Discarded from ChatVault

These showed up in the same Grok/workshop cloud as ChatVault. They do **not** belong on PR #33 or in `docs/chatvault-audit/`. GAP1/RH belongs on `cursor/overleaf-value-audit-a44c` if at all.

| Discard | Why it is not ChatVault |
| --- | --- |
| Nav42 / CBFD / NS pathway | Fluids archive. Different product. |
| 2.2 Hz paint / propofol notes | Clinical/geometry session material. Not a vault ranker. |
| RH GAP1 | Riemann/Overleaf paper track. Not ChatVault. |
| Overleaf value audit | Separate branch. Do not copy into this PR. |
| Autobiography / Grok personal flags | Personal. Not in git. |
| Domain Architect / SFE / AquaQuarts Grok notes | Paper/decanter track. Near-misses only (see below). |
| `vault_search.py` as a Grok replacement for hybrid | Forbidden. Hybrid stays. |

Nothing from the discard list was copied into `chatvault/` or `docs/chatvault-audit/` on this pass. Prior audit files already had no Nav42 / 2.2 Hz / GAP1 / Overleaf / autobiography text.

---

## What was searched

| Place | What turned up |
| --- | --- |
| This PR worktree (`cursor/chatvault-build-a44c`) | Hybrid engine + glass PWA + audit packet. Harmonic Watch honesty restored into `SEARCH.md`. |
| `chatvault/SEARCH.md`, `js/search.mjs`, `js/engine.mjs` | Ranker is hybrid. Ledger status is a field query, not a quality score. No E8. |
| `docs/chatvault-audit/` | `harmonic_note` on the Base44 Conversation schema and one JSON export (`null`). Not a score. |
| Live glass bundle (earlier freeze `index-DXcRcOPA.js`) | Harmonic Watch UI prints `harmonic_note`. Semantic search is `InvokeLLM` id-rank. |
| Git history of `chatvault/` + `docs/chatvault-audit/` | No E8 ranker, no Nav42, no GAP1, no Overleaf, no autobiography. |
| `/tmp/jonathan-papers/GROK-SPEC-AUDIT.md` | Domain Architect / SFE. **Discard.** |
| Agent store swirl handoff | E8/H4 folding is a **different geometry book**, with an explicit “do not put this into ChatVault.” **Discard.** Not a retrieval spec. |
| grok.com / x.com export, Desktop, Downloads | Still absent. Paste if you have the thread. |

---

## Near-misses — ignore (already better, or wrong product)

| Path | Why it is not the dump |
| --- | --- |
| Cursor Grok 4.6 `MASTER-AUDIT.md` (24 Aug) | This workshop’s ChatVault audit, not an xAI grok.com research paste. |
| ChatVault 2 + Evernote HTML | Already snapshotted. Substring search. Hybrid+glass already better. |
| `SOURCE_AI: Grok` in `engine.mjs` | Provenance enum, not research notes. |
| Live `index.html` / `search.mjs` | Not replaced. Not a Grok `vault_search.py`. |

Hybrid `chatvault-hybrid-0.2.0` and glass look stay canonical.
