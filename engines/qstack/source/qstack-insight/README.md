# QStack Insight — unique product source

**Almost-production #2** (unpublished editorial dashboard). Date seen: **19 November 2026**.

| Field | Value |
| --- | --- |
| Published URL | none (`last_deployed_at` is null) |
| Base44 app | QStack Insight `69e3fb761bccedecaf393b70` |
| Slug | `qstack-proof-flow` |
| Created | 2026-04-18 |
| Last deployed | **never** |
| App stage | ready |
| Visibility | public_without_login |
| Branch | `main` only |

A Base44 editor preview exists; the JWT is **not** committed. Use the Base44 editor for this app.

## Why this one is “almost production”

Complete unpublished UI: project report (theorems A–H table, paper comparison, next steps) plus a research dashboard (Gantt, LaTeX viewer, version history, endorsement tracker). Real pages, not an empty War Board. Older than Reference (April vs May 2026) and never published, so it is #2.

This is an **editorial / program-status** app, not a CFD SDK.

## What was copied

Unique product files via Base44 `read_file`:

- `src/App.jsx` — routes `/` (Report) and `/dashboard`
- `src/pages/Report.jsx`, `src/pages/Dashboard.jsx`
- `src/components/report/*`, `src/components/dashboard/*`
- `src/SNDC_proof_detailed.md`
- `base44/entities/PaperVersion.jsonc`, `User.jsonc`
- `package.json`

Auth/OAuthConsent boilerplate was **not** copied.

## Honest gaps

- Never deployed. Not a live product URL.
- Copy inside the UI (“8 / 8 Theorems Proved”, Clay / arXiv readiness) is **his artifact**. This workshop does **not** adopt those claims and does **not** treat QStack as an RH/NS proof.
- The report itself flags ℝ³ / Clay as still open.
- No CFD solver. No operator visualization (that lives in Reference).
- Tree is not a complete runnable Vite app without omitted Base44 platform files.
