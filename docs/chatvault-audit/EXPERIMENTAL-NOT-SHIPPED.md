# EXPERIMENTAL / not shipped

ChatVault-only archive. These ideas are **not** in the live product and **must not** be implemented on this PR without beating hybrid eval on Jonathan’s real corpus.

## E8 / lattice ranking

**Status:** EXPERIMENTAL / not shipped. **Not implemented.**

Searched (25 August 2026): `chatvault/`, `docs/chatvault-audit/`, `SEARCH.md`, `engine/search` JS, git history of those paths, frozen Base44 glass strings, Grok ChatVault hunt.

No ChatVault design note treated E8 (root lattice, H4 folding, or similar) as a retrieval feature. The phrase “harmonic search engine” in the live glass app is **Harmonic Watch**: a panel that prints `harmonic_note` (LLM ingest copy). That is not a ranker.

If a later note proposes E8 as experimental retrieval: keep it in this file. Do not add it to `js/search.mjs`. It does not have eval data here and will not beat `chatvault-hybrid-0.2.0` on a vault of chats without that evidence.

## Harmonic Watch (shipped as copy, not as search)

Shipped in Base44 glass as UI copy only. Git hybrid must not score `harmonic_note` or ledger status. See `chatvault/SEARCH.md`.
