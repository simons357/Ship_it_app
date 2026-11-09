# DECISIONS.md

**Date:** 24 August 2026  
**Repo:** `github.com/simons357/Ship_it_app` (workshop). This is **not** a dedicated ChatVault product repo. A fresh GitHub repo was requested; this agent cannot create one.

**Which build won:** The morph-glass Base44 app `6a58e103fedcde66a0a7710e` is the canonical **look** (OS for your AI). The git tree `chatvault/` is the canonical **engine / data model** (ChatVaultEntry, CLAIM_LEDGER, hybrid ranker, atlas). Glass is a skin. It does not win the backend.

**Format (6 Nov 2026):** Not Evernote. Home screen is an atlas (constellation + ranked beams). Search is `chatvault-hybrid-0.2.0`, not a notebook filter.

**Memory (6 Nov 2026):** Search memory is on-device (queries, opens, last project).
It may nudge same-project hits ×1.05 and last-opened ×1.02 **after** the ranker.
It must not hide a ranker regression. Ranker additions are gated on
`chatvault/bench/BASELINE.json` (nDCG@5 = 1, MRR = 1, mean ≤ 250 ms, every
fixture case hits). Weekly observation is `docs/chatvault-audit/WEEKLY-BENCH.md`.
Do not lower the baseline to pass a weaker ranker. Do not invent a cloud memory.

**Why not let Base44 glass win outright:** It holds ~14 conversation records, but they read as SaaS seed data (rate limiter, CRM, investor deck), not Jonathan’s research corpus. Seed data must be archived, not used as “live content wins.” Its `Conversation` schema has no claims, theorems, gaps, or ledger. Rebuilding that model later is the expensive mistake. C2 is a landing page plus Drive OAuth. C3 is an empty paper vault. Claude’s original is historical and still not in this workshop.

**No hassle (12 Sep 2026):** Owner does not want people hassling him. Binding. ChatVault is a personal tool, not a public product, until he says otherwise. See `NO-HASSLE.md`.

**Apple (12 Sep 2026):** Owner has an Apple Developer membership. That is recorded. It is not permission to wrap Base44 or to submit. Combined with the hassle constraint: no public App Store listing, no support inbox, no TestFlight public link.

**What this agent refuses:** exporting Base44 by guessing credentials; tagging `Ship_it_app` `main` as `v0.1-canonical`; fabricating `build-a` / `build-b-glass` / `build-legacy` branches without source (HTML snapshots already live under `docs/chatvault-audit/evidence/`); turning on Stripe; wrapping the Base44 preview in Capacitor; deleting any Base44 record; submitting this web vault to App Review.
