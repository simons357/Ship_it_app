# DECISIONS.md

**Date:** 24 August 2026  
**Repo:** `github.com/simons357/Ship_it_app` (workshop). This is **not** a dedicated ChatVault product repo. A fresh GitHub repo was requested; this agent cannot create one.

**Which build won:** The morph-glass Base44 app `6a58e103fedcde66a0a7710e` is the canonical **look** (OS for your AI). The git tree `chatvault/` is the canonical **engine / data model** (ChatVaultEntry, CLAIM_LEDGER, fielded search). Glass is a skin. It does not win the backend.

**Why not let Base44 glass win outright:** It holds ~14 conversation records, but they read as SaaS seed data (rate limiter, CRM, investor deck), not Jonathan’s research corpus. Seed data must be archived, not used as “live content wins.” Its `Conversation` schema has no claims, theorems, gaps, or ledger. Rebuilding that model later is the expensive mistake. C2 is a landing page plus Drive OAuth. C3 is an empty paper vault. Claude’s original is historical and still not in this workshop.

**What this agent refuses:** exporting Base44 by guessing credentials; tagging `Ship_it_app` `main` as `v0.1-canonical`; fabricating `build-a` / `build-b-glass` / `build-legacy` branches without source (HTML snapshots already live under `docs/chatvault-audit/evidence/`); turning on Stripe; wrapping the Base44 preview in Capacitor; deleting any Base44 record.
