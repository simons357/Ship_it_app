# ChatVault is operational — briefing for other AIs

**Date:** 26 August 2026  
**Owner:** Jonathan Simons  
**Repo:** `github.com/simons357/Ship_it_app`  
**Branch / PR:** `cursor/chatvault-build-a44c` / https://github.com/simons357/ship_it_app/pull/33  
**Tagline (locked, use loudly):** **OS for your AI**  
**Do not** market Evernote, Stripe, auto-PROVED ledger rows, or Domain Architect as a proof engine.

When a chat is done, drain it into ChatVault. When a paper, letter, picture, or movie shows up, drain that too — with a different designation so people can tell AI text from real records. Both are searchable in one vault.

---

## 1. Is ChatVault hooked to Domain Architect?

**Yes, as a drain. Not as DA’s brain.**

ChatVault can sit on the same loopback origin as a Domain Architect homepage so a finished FRA audit can land in the vault. Domain Architect remains an auditor. ChatVault remains **OS for your AI**.

| Path | What it does |
| --- | --- |
| Shared export | `{ "format": "chatvault-export", "schema_version": "chatvault-engine-0.3.0", "entries": [...] }` |
| CLI | `python -m domain_architect --drain-chatvault "∇²Φ = 4π G ρ" -o audit.json` |
| Loopback drain | `python -m domain_architect --drain-server` then ChatVault **Ingest → Drain → Pull** (`127.0.0.1:7847`) |
| One-origin site | `python -m domain_architect --site` → [http://127.0.0.1:8765/](http://127.0.0.1:8765/) (DA homepage) and [http://127.0.0.1:8765/chatvault/](http://127.0.0.1:8765/chatvault/) (the PWA). Same `localStorage` origin. |
| Homepage dock | ChatVault logo + search. Typing a query **opens the app** (`/chatvault/?q=…`) unless the user picks “Show hits here.” |

Domain Architect remains a Functional Role Analysis auditor. Canonical SFE status stays **unresolved**. A DA audit lands in ChatVault as `source_type: da_audit`, `origin_class: human_record`, `source_ai: DomainArchitect`. Nothing is auto-PROVED. DA does not prove Navier–Stokes or Riemann.

The DA homepage ChatVault dock is live search/ingest, not a “coming soon” placeholder.

---

## 2. Will it work?

**Yes for text chats, ChatGPT `conversations.json`, DA audit JSON, and snippets.**  
**Partial for binaries.** Pictures under ~12 MB can store as data URLs. Movies, audio, PDF, DOCX become **searchable stubs** (filename, type, size) — not a media locker.  
**No hosted cloud.** Records live in this browser’s `localStorage` (`chatvault.engine.v1`). Paste cap is 50 million characters; browser quota is still often 5–10 MB. Export JSON when the quota banner appears. IndexedDB is the next persistence step.  
**No silent auto-drain from ChatGPT/Claude/Grok products.** When a conversation is finished, slide the whole thread (or the official export JSON) onto ingest / the DA search drop zone. Other AIs should emit ChatVault export JSON at the end of a session.

Standalone PWA (engine only):

```bash
cd chatvault && python3 -m http.server 4173
# http://127.0.0.1:4173/
```

DA + ChatVault together (homepage search opens the app):

```bash
python -m domain_architect --site
# http://127.0.0.1:8765/
```

---

## 3. What is on the engine?

File: `chatvault/js/search.mjs`  
Version: **`chatvault-hybrid-0.2.0`**

Pipeline, in order:

1. Parse (AND / OR / `"phrases"` / `field:`)
2. Inverted index
3. Hard filters (visibility, AI, type, origin, book, tag, project, starred)
4. Boolean match gate
5. BM25F (K1=1.2) with stem / substring / one-edit discounts
6. Character 3-gram BM25
7. Field-weighted TF-IDF cosine
8. Reciprocal Rank Fusion, **k=60**
9. Optional RM3 (up to 2 docs, 3 terms) fused again
10. Display `rrf*100` plus a tiny `ingested_at` tie-break

**Ranked fields:** title, claim, theorem, gap, question, action, tag, book, summary, content, ai, source.  
**Not scores:** ledger status, `harmonic_note`, E8 / lattice.  
**Origin field** is searchable (`origin:ai` / `origin:human`) and is **not** an unfielded quality boost.

Schema: **`chatvault-engine-0.3.0`**. PWA cache: **`chatvault-engine-v0.6.1`**.

License unit (ranker only, not the PWA): `chatvault/js/search.mjs`. Import API: `chatvault/js/ENGINE.md`. Internals: `docs/chatvault-audit/CHATVAULT-ENGINE-INTERNALS.md`. DA homepage catalog: `#da-engines`.

---

## 4. Origin split (AI vs real)

| `origin_class` | What |
| --- | --- |
| `ai_generated` | AI conversations / transcripts (ChatGPT, Claude, Grok, Base44, …) |
| `human_record` | Papers, letters, apps, pictures, movies, audio, PDFs, DA audits, human notes |

Search: `origin:ai` · `origin:human` · UI filter “AI conversations” / “Real records”.  
Do not advertise a general note-taking brand. The product line is **OS for your AI** that also files real-world records so you can look everything up.

---

## 5. Drain protocol for other AIs

When your conversation with Jonathan is complete:

1. Emit JSON `{ "format": "chatvault-export", "schema_version": "chatvault-engine-0.3.0", "entries": [ ChatVaultEntry, … ] }`.
2. Keep `raw_content` immutable. Never put PROVED on a ledger row unless a human reviewed it.
3. Set `origin_class: "ai_generated"` for the chat itself.
4. Drop the file on ChatVault ingest, or on the DA homepage drop zone, or POST to `http://127.0.0.1:7847/queue` / `http://127.0.0.1:8765/api/drain/queue` if that listener is up.

Quick capture (not a whole chat): paste a snippet on the DA dock and **Index snippet**. Still a vault record.

Non-AI bytes (sound, video, scans): drop the file. ChatVault indexes a stub or a small image so it is findable next to the chats.

---

## 6. How it can be improved (honest backlog)

1. **IndexedDB** so a large vault survives past localStorage quota.
2. **PDF/DOCX text extract** (stubs exist; OCR does not).
3. **Browser extension** to auto-drain ChatGPT/Claude/Grok without a manual drop.
4. **Dense MiniLM/E5 + cross-encoder** into the same RRF, only if it beats this eval on Jonathan’s corpus.
5. **Multi-device sync** via export/import or a real backend. There is no ChatVault cloud today.
6. **Web search** on the DA dock is a DuckDuckGo tab, not an in-vault crawler. Do not pretend otherwise.

---

## 7. Two surfaces — do not collapse

| Surface | Reality |
| --- | --- |
| Git PWA (`chatvault/`) | Canonical engine + data model. Steel default; Ink / Signal / Day skins. Glass is not selectable. |
| Base44 preview | Morph-glass look demo, different schema (`Conversation`). Not this engine. |

Tests: `cd chatvault && node --test tests/*.mjs`  
DA + drain: `python -m unittest tests.test_chatvault_bridge tests.test_domain_architect_units`
