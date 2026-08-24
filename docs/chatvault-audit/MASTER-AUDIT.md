# ChatVault Master Audit — Grok 4.6

**Prepared for:** Jonathan Robert Simons, CRNA, MBS  
**Primary contact:** jonathansimons357@proton.me  
**Audit UTC:** 24 August 2026  
**Agent run:** https://cursor.com/agents/bc-01a031a9-7def-7853-a7d3-228d61203618  
**Workshop repo:** `github.com/simons357/Ship_it_app` (this is not a ChatVault source repo)

---

## Decision (required language)

The canonical ChatVault build is Base44 app `6a58e103fedcde66a0a7710e` (preview host `https://preview--6a58e103fedcde66a0a7710e.base44.app/`, HTML title **ChatVault — AI conversation vault**, tagline **OS for your AI**). This designation is based on live HTTP probes, SHA-256 of the preview JS/HTML/CSS bundles, side-by-side comparison with the two other named Base44 records, browser exercise of vault/ingest/search/tags/books/dashboard/export/disclaimer, and a JSON export of one conversation. Version **v1.19 is unverified**. The following limitations remain: Jonathan has not visually confirmed this is the ChatVault he recognizes; the intended `ChatVaultEntry` research schema is absent; the public `*.base44.app` host 404s; the editor preview is a login wall; the preview host is unauthenticated and writable; exported `raw_content` was null on a demo record; artifacts extraction is empty; there is no bulk export; source is not in git; Claude-origin HTML/React/Replit archives described in the brief were not present in this environment; security, privacy, Apple, and patent reviews are not passed.

**This is a `CANONICAL-CANDIDATE`, not a production certification.**

---

## 1. Canonical recommendation

**Label:** `CANONICAL-CANDIDATE`  
**Exact candidate:** Base44 app ID `6a58e103fedcde66a0a7710e`  
**Runnable URL tested:** https://preview--6a58e103fedcde66a0a7710e.base44.app/  
**Why this one, and not the newest-timestamp heuristic alone:**

1. It is the only named candidate that both **renders** and **behaves as a conversation vault**. Candidate 2 is a marketing page plus Drive sign-in. Candidate 3 is a different product (Paper Vault) with 0 papers.
2. Its visible subtitle is **OS for your AI**, matching the newest ready Base44 description in the intake brief.
3. Browser tests stored and retrieved records: 14 demo conversations were already indexed; a paste ingest created a 15th; search found “rate limiter”; a tag edit survived refresh; per-conversation JSON downloaded.
4. Bundle identity is frozen: JS SHA-256 `720a21e0e061997909f4ea6ca85caeff60a08af8b1d5157081746a76ff6ba8de` (1,150,051 bytes).

It is **not** selected because of the filename, because of `v1.19`, or because it was updated at 02:28 UTC. It is selected because it is the closest *working* ChatVault product among reachable artifacts.

It is **not** the complete product described in the intake concept (ChatGPT/Claude/Grok provenance, theorems, proof gaps, CLAIM_LEDGER, private/public split). That specification exists in git copy (`prime-field/PORTFOLIO.md` on branch `cursor/linkedin-crna-brand-kit-0311`, 3 August 2026) and in the intake brief. It is **not implemented** in this candidate’s UI or JSON export.

Jonathan was not available in this run to point at a screenshot and say “that is the real one.” If he later identifies the Claude HTML/GTD vault, the 3D React prototype, or the Flask/Replit archive as the recognized product, this label must be revisited. Until those sources are exported into this workshop, Candidate 1 is the only maintainable *runnable* baseline.

---

## 2. Historical baseline

**Label:** `HISTORICAL-BASELINE`  
**Exact candidate:** Claude-origin ChatVault, first version Jonathan named as the real one (“made by Claude last year”).  
**Location in this environment:** **not found.**

Preservation instructions (do this; do not delete anything):

1. Leave all three Base44 records (`6a58e103…`, `6a58f25d…`, `6a362391…`) untouched in Base44. Do not rebuild them in place as a way to “clean up.”
2. Export each Base44 app (source + entity schema + data) to a dated zip or a dedicated private GitHub repo. Store the zip *alongside* this packet, never as a silent overwrite of another candidate.
3. If the Claude-origin files, `/app/chatvault`, `356582767_chatvault_source2.zip`, `/app/ARCHIVE/chatvault_old/CHATVAULT_V*.html`, or `/app/CHATVAULT_V7.html` still exist on another machine, copy them read-only into `docs/chatvault-audit/archive/` in a later follow-up. Filename `V7` is not a version: the brief already warns it titles itself `ChatVault v6 · GTD`.
4. Keep the July 2026 git trail in this repo as dated evidence that ChatVault was publicly listed, then marked hollow:
   - `138eb99` (14 Jul 2026) listed ChatVault as “the Evernote of AI conversations” at https://primefield.tech/chatvault
   - `fc119c3` (21 Jul 2026) stopped cold-linking that URL because it was a hollow shell
   - live check 24 Aug 2026: in-app **404** “The page `chatvault` could not be found in this application.”

Nearest dated *concept* snapshot (not running source): `origin/cursor/linkedin-crna-brand-kit-0311:prime-field/PORTFOLIO.md` (3 Aug 2026) describes ChatVault as deployed research memory with a `ChatVaultEntry` entity, 20+ fields, and CLAIM_LEDGER statuses `PROVED | CONDITIONAL | NUMERICAL | CONJECTURAL | OPEN | WITHDRAWN`. That text is a product claim. This audit did not find a running app that implements it.

---

## 3. Version manifest

Full machine record: [`VERSION-MANIFEST.json`](VERSION-MANIFEST.json). Hashes: [`evidence/hashes/SHA256SUMS.txt`](evidence/hashes/SHA256SUMS.txt).

### What this workshop could and could not see

This cloud agent booted on `Ship_it_app`. Paths from the intake brief (`/app/chatvault`, `/app/ARCHIVE/chatvault_old/`, `/app/CHATVAULT_V7.html`, `356582767_chatvault_source2.zip`) **do not exist here**. GitHub user `simons357` has three public repos (`Ship_it_app`, `ship-it-code`, `kyrana-oracle`); none contain ChatVault source. No `v1.19` manifest was found in git, HTML titles, or JS version strings.

Unrelated public Base44 hosts that collided on name search and are **not** Jonathan’s product:

- https://chat-vault.base44.app/ → Aegis Messenger (`69dd04ce17b86e8662f2f5b8`)
- https://knowledge-vault.base44.app/ → Knowledge Weaver (`69a8887802b9617f96cfee90`)

### Candidate 1 — conversation vault (canonical candidate)

| Item | Value |
| --- | --- |
| App ID | `6a58e103fedcde66a0a7710e` |
| Reported version | none in UI; **v1.19 unverified** |
| Verified version | **unverified** |
| HTML title | ChatVault — AI conversation vault |
| OG title | ChatVault — Operating System for your AI |
| Disclaimer date inside app | 16 July 2026 |
| Demo record `created_date` | 16 July 2026 14:33:42 UTC (`6a58ebc636455b7a18e85f91`) |
| Runtime | Base44-hosted React SPA |
| Data model | `Conversation`, `Book`, `Artifact` (not `ChatVaultEntry`) |
| Import | paste, `.txt/.md/.json/.csv/.html`, images/videos |
| Search | Plain keyword + Semantic toggle |
| Export | per-conversation JSON only |
| Auth on preview host | none observed (world-readable and writable) |
| Auth on editor URL | Base44 login wall |
| Published `*.base44.app` | 404 App not found |

### Candidate 2 — landing + Drive (feature source)

Marketing home: “The operating system for your knowledge.” `/drive` asks to sign in to Google Drive. JS SHA-256 `bf8b3cd13a99f74a55504d7515608bbce26f8b8735839382fee21299e7a2f043`. Entity `Document`. Not a complete vault.

### Candidate 3 — Paper Vault (processing / feature source / archive)

UI title **Your Paper Vault**. Filters All/Latest/Draft/Archived all at 0. Supreme Search over 0 papers. Entity `Paper`. JS SHA-256 `ba579c77de0a1f6c4962f6b4a565c65d220e3c1a7cd6743059a263a17455894c`. Do not promote to canonical while it remains an empty paper product, even though the preview now renders.

### Blank-preview defect — explained

`https://app.base44.com/apps/6a58e103fedcde66a0a7710e/editor/preview` is not the app. Unauthenticated GET returns the Base44 editor shell (Monaco). In a browser it is a **login wall** (“Welcome to Base44”). The 23 August “blank white screen” is therefore an **environment/auth/preview-host mistake**, not proof that Candidate 1 is empty. The working surface is `preview--<id>.base44.app`. That host was not a white screen on 24 August 2026.

---

## 4. Feature matrix

Legend: **P** present and exercised · **~** partial · **B** broken or unsafe · **A** absent · **U** untested here (source missing)

| Intended capability | C1 conversation vault | C2 landing/Drive | C3 paper vault | Claude HTML / React 3D / Flask |
| --- | --- | --- | --- | --- |
| First launch / empty vs loaded | P (14 demo chats) | P (marketing) | P (empty paper shell) | U |
| Create / ingest | P (paste/bulk/media) | A (Drive OAuth only) | ~ Upload button, not fully exercised | U |
| Edit | P (tag add persisted) | A | U | U |
| Delete (confirmed) | ~ `confirm` + `deleteMany` in JS; not clicked | A | U | U |
| Search full text | P Plain | A | ~ Supreme Search UI, 0 papers | U |
| Semantic search | P toggle | A | ~ | U |
| Phrase / OR / field search | A (no operators in UI) | A | U | U |
| Date / source / extraction filters | ~ Source/Importance/Project/Book filters; date often blank | A | ~ Latest/Draft/Archived | U |
| ChatGPT / Claude / Grok / Base44 ingest | ~ generic paste + files; source stored as `pasted` / `image` / `video` | Drive | papers | U |
| PDF / DOCX / OCR / CSV / code | ~ txt/md/json/csv/html + images/videos; **no DOCX/OCR in accept=** | Drive | papers (claimed) | U |
| Raw text preserved | ~ UI shows Conversation; **export `raw_content` was null** on demo record | A | U | U |
| Human-reviewed summaries | ~ AI summary generated; no review workflow | A | U | U |
| Claims / theorems / gaps / action items | **A** | A | A | U |
| CLAIM_LEDGER statuses | **A** | A | A | U |
| Source AI + source file provenance | ~ `source` string only | A | U | U |
| Project categorization | P books/project/location | A | drafts/archive | U |
| Related files / entities | ~ Artifacts page empty stub | A | version compare copy | U |
| Export / portability | ~ per-item JSON | A | U | U |
| Re-import of export | U | A | U | U |
| Privacy private vs public | **A** | A | A | U |
| Offline / failed-load distinct from empty | **A** (no offline banner found) | A | empty copy exists | U |
| Mobile layout | P (narrow viewport still usable) | U | U | U |
| Account isolation | **B** public preview | login for Drive | public empty | U |

---

## 5. Defect list

Severity: **S0** stop-ship for any public/canonical use · **S1** high · **S2** moderate · **S3** polish

| ID | Sev | Finding | Reproduction |
| --- | --- | --- | --- |
| D1 | S0 | Preview host is unauthenticated. Anyone with the URL can read demo chats and **ingest new records**. This audit created conversation “Audit probe equation”. | Open https://preview--6a58e103fedcde66a0a7710e.base44.app/ without login. Use Ingest → Extract & index. |
| D2 | S0 | Intended `ChatVaultEntry` schema is not in C1. Theorems, key claims, open gaps, action items, open questions, related entities, extraction types, source_ai, CLAIM_LEDGER: absent in UI, JS identifiers, and JSON export. | Open any conversation. Inspect right rail and export JSON. |
| D3 | S1 | `raw_content` is null in the exported demo conversation while `clean_content` holds the User/Assistant text. Raw preservation is not proven for existing records. | Download JSON from “Designing a rate limiter…”. See `evidence/exports/designing_a_rate_limiter_that_won_t_break_the_api.json`. |
| D4 | S1 | Published host 404s. `https://6a58e103fedcde66a0a7710e.base44.app/` → `{"message":"App not found"}`. Public company URL `https://primefield.tech/chatvault` is an in-app 404. | `curl -i` both URLs. Screenshot: `evidence/screenshots/primefield_chatvault_404.webp`. |
| D5 | S1 | Editor preview URL is a login wall, which previously looked like a blank app. | https://app.base44.com/apps/6a58e103fedcde66a0a7710e/editor/preview |
| D6 | S1 | Conversation list uses `Conversation.list("-updated_date", 200)` (dashboard 500). No pagination loop. Records beyond the cap would be silently omitted. Better than an infinite malformed-pagination loop; still a truncation defect from the V6 audit family. | Read minified JS; vault view calls list with 200. |
| D7 | S2 | Artifacts extraction is a stub: 0 items after 15 conversations, including after ingest. | Open `/artifacts`. |
| D8 | S2 | No bulk export, no Markdown/CSV export. Per-item JSON omits human book names (IDs only) and had null `raw_content`. | Vault and conversation chrome; only a JSON button. |
| D9 | S2 | Source AI is not first-class. Ingest UI shows `SOURCE: PASTED`. Export `source: "pasted"`. ChatGPT/Claude/Grok/Base44 are not selectable provenance. | `/ingest` screenshot `chatvault_03_ingest_single.webp`. |
| D10 | S2 | Dates are often unset (`conversation_date: null`, UI “Date: —”). Ingestion date exists as `created_date` but is not the item date users see. | Same JSON export. |
| D11 | S2 | Search is keyword or semantic; no phrase/OR/field operators; no result highlighting of escaped HTML. AND-only history from V6 is **not fully re-proven**, but operators are absent. | Search “rate limiter”; result card has no highlighted snippet. |
| D12 | S2 | No distinct offline/network-failure empty state on C1. V6 item 6 remains open. | Disconnect was not fully simulated; no banner exists in the loaded UI. |
| D13 | S2 | `user.json` 401 in console. Preview runs without a user entity. Isolation untested. | DevTools on any C1 page. `chatvault_14_devtools_console.webp`. |
| D14 | S3 | PWA manifest warnings (`start_url` / `scope` / manifest v2). | Console. |
| D15 | S3 | Builder-bridge “no parent window” on preview host (expected outside the editor). | Console. |
| D16 | S3 | Demo conversations look like SaaS seed data (rate limiter, CRM, investor deck) with `is_sample: false`. Misleading if treated as Jonathan’s research corpus. | Vault grid. |
| D17 | — | Historical V6 defects 2–3 (status desync, delete ghost): delete path awaits `deleteMany` then reloads; failure `alert`s. **Not clicked.** Treat as unverified-fixed, not closed. | JS: `confirm` → `deleteMany` → `q()`. |
| D18 | — | Stripe helper in the missing Replit zip: **not activated**. C1 “stripe” hits are Recharts grid stripes, not payments. | n/a |

---

## 6. Security and privacy report

Scope: public HTTP + browser of preview hosts. No Base44 admin credentials. No Stripe keys. No attempt to access other users’ private Base44 accounts.

### Authentication and session

- C1 preview: **no login**. Create/read of `Conversation` worked from this agent.
- C1 editor URL: Base44 platform login (Google/Apple/GitHub/email).
- C2 `/drive`: explicit Google OAuth sign-in before Drive import.
- `GET https://app.base44.com/api/apps/6a58e103fedcde66a0a7710e` → 401 JSON. Platform API is gated; **the preview app API is not**, from the user’s browser.

### Authorization / row-level access

- Export shows `created_by_id: "service_3d25a80a-6eda-4b6b-ab72-cdd30b63eff8"` — a service principal, not Jonathan’s user id.
- No `created_by` filter in the vault `list()` calls inspected.
- Cross-user leakage: **not disproven**. Treat C1 preview data as **public demo**, not a private research vault.

### Private files / signed URLs

- Media ingest writes `media_url`. Signed-URL expiry and ACL were not tested. Do not store private clinical or defense files in this preview.

### Secrets

- No `.env` or Stripe keys in this repo.
- Replit `stripe_helper.py` was **not present** and must not be turned on.

### Prompt injection

- Ingest sends pasted text to an extraction LLM (“Extract & index”). Imported documents can steer titles, tags, summaries, and book assignment. The Euler probe was auto-filed into Product Strategy / Engineering Notes / Research & Ideas / Marketing & Growth. That is expected LLM behavior and a real injection surface.

### Logging

- Preview HTML posts to `/api/app-logs/<appId>/log-user-in-app/<page>`. Page names (not full conversation bodies) are sent. Whether Base44 logs prompt content server-side is **unknown**.

### Deletion

- UI copy on disclaimer: **no guarantee of retention or deletion completeness**. JS has `deleteMany` with “cannot be undone.” Account deletion UI was **not found**.

### Third-party scope

- C2 Drive: Google Drive import, OAuth. Do not connect a Drive with private research until C1 is behind real auth.
- Payments: out of scope. Do not enable.

**Privacy conclusion:** Candidate 1 must not be used as a private knowledge vault in its current preview posture. The product concept requires a private/public split; this build does not provide one.

---

## 7. Data migration plan

Do **not** merge products by renaming Base44 apps.

### Freeze first

1. Export C1, C2, C3 source + data from Base44 (zip or GitHub sync). Store as `ARCHIVE-DO-NOT-DELETE`.
2. Locate Claude-origin / HTML V2–V7 / React `/app/chatvault` / Replit zip. Hash and store read-only.
3. Keep Candidate 1 preview data as-is, including the 24 Aug 2026 “Audit probe equation” record (`id` `6a8bb4662294623e44a3e0af` from the test URL). Deleting it is optional and only on Jonathan’s explicit request.

### Map C1 → intended `ChatVaultEntry`

| C1 `Conversation` | Intended `ChatVaultEntry` | Rule |
| --- | --- | --- |
| `title` | `title` | copy |
| `source` (`pasted`/`image`/`video`) | `source_type` | map; do not invent `source_ai` |
| *(absent)* | `source_ai` | empty until user sets ChatGPT/Claude/Grok/Base44 |
| `clean_content` | `content_text` | copy; if `raw_content` is non-null prefer raw |
| `raw_content` | `content_text` backup | if null, do not fabricate |
| `summary` | `summary` | copy; mark `ai_generated` |
| `labels` | `search_tags` | copy |
| `project` | `project_category` / `project_tags` | copy into both until split |
| `book_ids` | `related_projects` | resolve IDs to Book titles |
| `media_url` | `file_url` / `linked_files` | copy |
| `conversation_date` or `created_date` | `item_date` | never rewrite; prefer conversation_date when set |
| *(absent)* | `key_claims`, `theorems`, `open_gaps`, `action_items`, `open_questions`, `related_entities`, `extraction_types` | empty arrays; do not auto-fill from summary |
| `harmonic_note` | notes | keep as extra field, do not drop |

### Other sources

- **C2 Drive:** keep as an ingest connector, not a second database.
- **C3 Paper:** migrate `Paper` rows into `ChatVaultEntry` with `source_type=pdf/paper` if/when data exists. Preserve version/draft/archive as status, not as CLAIM_LEDGER.
- **HTML GTD V6/V7:** if recovered, treat as HISTORICAL-BASELINE UX. Port GTD lists into `action_items` only after a field-level diff.
- **React 3D:** FEATURE-SOURCE for visualization only. Do not make Three.js the system of record.
- **Flask/Replit:** FEATURE-SOURCE for search_engine and auth. Do not copy `stripe_helper` into canonical without a separate review.
- **CLAIM_LEDGER:** add as a field on claims/theorems, default `UNREVIEWED`, never auto-`PROVED`.

### What not to migrate

- Demo SaaS seed chats, unless Jonathan wants them as fixtures.
- Aegis Messenger / Knowledge Weaver (foreign Base44 apps).
- Marketing claims from C2 (“encrypted, private, always under your control”) until encryption and auth are real.

---

## 8. Test results and reproducibility

### What was tested (24 August 2026)

Visual log: [`evidence/visual-test-log.md`](evidence/visual-test-log.md)  
Screenshots: [`evidence/screenshots/`](evidence/screenshots/)

| Test | Result |
| --- | --- |
| C1 first launch | Vault with 14 conversations, 3 starred |
| C1 ingest paste | Created “Audit probe equation”; AI summary added; conversation text still visible |
| C1 search “rate limiter” | Found the expected card |
| C1 tag edit | “TestTag” persisted after refresh |
| C1 JSON export | 1,587-byte file; `raw_content` null |
| C1 disclaimer | Five liability/no-warranty boxes; last updated 16 Jul 2026 |
| C1 mobile viewport | Layout usable |
| C1 editor URL | Login wall |
| C1 public host | 404 |
| C2 home | Marketing landing |
| C2 /drive | Google sign-in required |
| C3 preview | Empty Paper Vault |
| primefield.tech/chatvault | In-app 404 |
| Concurrent edits / session expiry / large DOC / DOCX / OCR | **Not tested** |
| Network failure banner | **Not tested** |
| Account isolation | **Failed by default** (no accounts on preview) |

### Reproduce

```bash
curl -sS -D- -o /tmp/c1.html https://preview--6a58e103fedcde66a0a7710e.base44.app/
# title should contain: ChatVault — AI conversation vault
curl -sS -o /tmp/c1.js https://preview--6a58e103fedcde66a0a7710e.base44.app/assets/index-DXcRcOPA.js
sha256sum /tmp/c1.js
# expect: 720a21e0e061997909f4ea6ca85caeff60a08af8b1d5157081746a76ff6ba8de
```

Open the preview host in a browser. Do **not** use `app.base44.com/.../editor/preview` unless logged into Jonathan’s Base44 account.

If the JS hash changes, the live app has been rebuilt and this packet’s freeze is stale. Re-hash before any legal or store action.

---

## 9. GitHub / Cursor handoff plan

1. **This PR is documentation only.** It does not contain ChatVault application source. `Ship_it_app` remains a research/workshop repo (Harmonic Blueprint / Domain Architect). Do not dump a Base44 SPA onto `main` as if this were the product.
2. Create a **new private repo** (recommended name `chatvault`) after Base44 export. Put Candidate 1 source on `main`, tagged `snapshot-2026-08-24-c1` with the JS hash above in the tag message.
3. Put C2, C3, HTML V-series, React 3D, and Replit zip on branches or `archive/` directories. Never delete them.
4. Add CI: `sha256sum` of build output, plus tests for: create → read → export round-trip of `raw_content`; auth denied without session; CLAIM_LEDGER fields rejected if the schema is added.
5. Cursor rule for future agents: **do not treat update timestamps or `v1.19` as identity.** Identity is bundle hash + entity schema + Jonathan’s screenshot confirmation.
6. Do not enable GitHub Pages for the preview snapshot (it would republish demo chats).
7. After Jonathan exports sources, run a second audit against the git tree (this audit could only freeze CDN bundles).

---

## 10. Patent-readiness issues

No patentability conclusion. The broad idea of an “AI knowledge vault” is crowded (ChatGPT history, Notion, Rewind, and several unrelated products already named ChatVault).

Dated evidence this audit *did* freeze:

- 14 Jul 2026: public listing of ChatVault on the portfolio
- 16 Jul 2026: C1 disclaimer date and demo `created_date`
- 21 Jul 2026: public URL declared hollow
- 3 Aug 2026: ChatVaultEntry + CLAIM_LEDGER written into portfolio copy
- 24 Aug 2026: C1/C2/C3 preview hashes

Before any filing:

- Counsel must separate inventorship (Jonathan vs Claude/Base44/Cursor/Grok generated code).
- Do not file on taglines (“OS for your AI”, “Evernote of AI conversations”).
- Possibly-discussable technical claims, **if** a real implementation and prior-art search support them later: provenance-preserving multi-AI ingest; structured extraction of claims/equations/gaps/action items that stay distinct from summaries; CLAIM_LEDGER that cannot auto-promote to PROVED; private/public split with row-level auth. **Candidate 1 does not currently implement those.**
- Public preview of C1 may count as disclosure of whatever is in that UI. Preserve hashes before wider publication.

---

## 11. Apple-readiness issues

A web preview is not an App Store product. Blockers:

- No stable public URL (published host 404; preview host is an unpublished Base44 preview).
- No account creation/sign-in on C1 preview; therefore no account deletion.
- Disclaimer denies retention guarantees and tells users not to use ChatVault as a sole repository — incompatible with presenting it as a vault people depend on.
- No privacy policy link on the disclaimer page.
- No tested offline mode, crash telemetry, or iOS packaging (Capacitor/PWA/native).
- Third-party license inventory of Base44, Recharts, and LLM extraction stack: **not done**.
- Payments: none enabled; keep it that way for this step.
- Recommend a **responsive authenticated web app first**. Wrapper/PWA/App Store only after auth, export, deletion, and the research schema (if that is still the product) exist.

---

## 12. Claims and features that must not be marketed as established

Do not say or imply any of the following until a later audit closes them:

1. ChatVault is production-ready, complete, or “the real shipped OS for your AI.”
2. Version **v1.19** (unverified).
3. Filename versions V2–V7 identify distinct certified builds.
4. The newest Base44 timestamp is the authentic product.
5. `primefield.tech/chatvault` is a live ChatVault.
6. Candidate 1 implements `ChatVaultEntry`, theorems, proof gaps, patent-idea extraction, or CLAIM_LEDGER.
7. Raw text is always preserved (`raw_content` was null on the exported demo record).
8. Source AI (ChatGPT/Claude/Grok/Base44) is captured as provenance.
9. Data is encrypted, private, or “always under your control” (C2 marketing).
10. Search is scientifically complete (equations, citations, phrase/OR/field, highlighting).
11. Artifacts (patents/code/media extraction) work.
12. ChatVault is an autonomous truth engine, verifier, or guaranteed scientific-validation system.
13. AI summaries are human-reviewed.
14. Row-level access control or private/public split exists.
15. Apple distribution readiness.
16. Patentability, market demand, valuation, or revenue.
17. The 3D React prototype, Flask/Replit app, or HTML GTD vault is this same product (they were not available to compare).
18. Candidate 3 is unusable solely because Base44 said “Processing” — the preview renders, but it is a paper vault, not the conversation product.

---

## Labels (summary)

| Artifact | Label |
| --- | --- |
| Base44 `6a58e103fedcde66a0a7710e` | **CANONICAL-CANDIDATE** |
| Claude-origin ChatVault (unlocated) | **HISTORICAL-BASELINE** |
| Base44 `6a58f25d90370ad28d426a88` | **FEATURE-SOURCE** (landing + Drive) |
| Base44 `6a36239133fe30857adcef89` | **PROCESSING** + **FEATURE-SOURCE** + **ARCHIVE-DO-NOT-DELETE** |
| ChatVaultEntry / CLAIM_LEDGER spec in portfolio copy | **FEATURE-SOURCE** (specification, not a build) |
| `/app/chatvault` React 3D (not present) | **EXPERIMENTAL** |
| Replit/Flask zip (not present) | **FEATURE-SOURCE** (do not activate Stripe) |
| HTML V2–V7 (not present) | **ARCHIVE-DO-NOT-DELETE** |
| `primefield.tech/chatvault` | hollow / 404 — do not cold-send |
| Aegis Messenger / Knowledge Weaver | unrelated — ignore |

---

## What Jonathan should do next

1. Look at `evidence/screenshots/chatvault_01_main_vault.webp`. Reply whether that dark “Conversation Vault / OS for your AI” UI is the ChatVault he recognizes.
2. Export the three Base44 apps and, if they still exist, the Claude/HTML/React/Replit trees. Attach them to a follow-up. Do not delete Base44 records.
3. Treat Candidate 1 as a **demo conversation OS** to fork from, and the ChatVaultEntry schema as a **repair backlog**, unless he explicitly wants to abandon the research-memory product.

No production certification. No patentability conclusion. No App Store readiness conclusion.
