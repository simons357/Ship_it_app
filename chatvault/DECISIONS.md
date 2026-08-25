# DECISIONS.md

**Date:** 24 August 2026  
**Repo:** `github.com/simons357/Ship_it_app` (workshop). This is **not** a dedicated ChatVault product repo. A fresh GitHub repo was requested; this agent cannot create one.

**Which build won:** The morph-glass Base44 app `6a58e103fedcde66a0a7710e` is the canonical **look** (OS for your AI). The git tree `chatvault/` is the canonical **engine / data model** (ChatVaultEntry, CLAIM_LEDGER, BM25F fielded retrieval). Glass is a skin. It does not win the backend.

**Search engine:** Public GitHub “ChatVault” repos (rajz3006 hybrid Chroma, marcoshernanz WhatsApp BERT+BM25, Chrome exporters) are other people’s products. Jonathan’s Replit zip `356582767_chatvault_source2.zip` / `search_engine.py` is still missing. This tree now ships `chatvault/js/search.mjs` — hybrid RRF over BM25F, character n-grams, TF-IDF cosine, stems/typos, and RM3. Ledger status is never a ranking signal. `harmonic_note` is Base44 Harmonic Watch copy, not a score. E8/lattice ranking is **EXPERIMENTAL / not shipped** and is not in this engine. A MiniLM/cross-encoder layer waits on a local model and Jonathan’s corpus. Do not paste a Base44 Semantic toggle over this.

**Brand marks:** The owner vault-door logos from that glass app are now local files under `chatvault/assets/` (light original upload, dark UI mark, morph-glass backdrop). Do not replace them with a CSS dial. Do not hotlink Base44.

**Why not let Base44 glass win outright:** It holds ~14 conversation records, but they read as SaaS seed data (rate limiter, CRM, investor deck), not Jonathan’s research corpus. Seed data must be archived, not used as “live content wins.” Its `Conversation` schema has no claims, theorems, gaps, or ledger. Rebuilding that model later is the expensive mistake. C2 is a landing page plus Drive OAuth. C3 is an empty paper vault. Claude’s original is historical and still not in this workshop.

**What this agent refuses:** exporting Base44 by guessing credentials; tagging `Ship_it_app` `main` as `v0.1-canonical`; fabricating `build-a` / `build-b-glass` / `build-legacy` branches without source (HTML snapshots already live under `docs/chatvault-audit/evidence/`); turning on Stripe; wrapping the Base44 preview in Capacitor; deleting any Base44 record.
