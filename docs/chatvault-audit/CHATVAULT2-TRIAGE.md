# ChatVault 2 HTML — honest triage

**Date:** 25 August 2026  
**Label:** `FEATURE-SOURCE` / `HISTORICAL HTML`. **Not** the live product.  
**Canonical look:** Base44 morph-glass “OS for your AI”.  
**Canonical engine:** `chatvault/` (ChatVaultEntry, immutable raw, CLAIM_LEDGER, hybrid BM25F).

Recovered from a paste titled “Chatvault 2” in the Chat Vault agent thread. Title in the document: **ChatVault - AI Conversation Organizer**.

| File | What it is |
| --- | --- |
| [evidence/html-snapshots/CHATVAULT_V2_REACT_CDN.html](evidence/html-snapshots/CHATVAULT_V2_REACT_CDN.html) | Readable reconstruction (markdown fences that had split JSX/template strings were closed). Still contains the client Anthropic `fetch`. Do not serve as the app. |
| [evidence/html-snapshots/CHATVAULT_V2_REACT_CDN.paste.txt](evidence/html-snapshots/CHATVAULT_V2_REACT_CDN.paste.txt) | Exact user paste, fences and all. |
| [evidence/html-snapshots/PRODUCTION-READY-MVP-REVIEW.paste.md](evidence/html-snapshots/PRODUCTION-READY-MVP-REVIEW.paste.md) | Earlier paste. **Untrusted marketing**, not a review of this HTML or of `chatvault/`. |

This prototype is **not production-ready**. It was **not** ported onto the git engine. Stripe stays off. Anthropic is not called from the browser in `chatvault/`.

---

## What this code actually is

Single-file React-in-HTML:

- Tailwind CDN (`cdn.tailwindcss.com`)
- React 18 + ReactDOM UMD (`unpkg.com`)
- Babel standalone (`unpkg.com/@babel/standalone`) compiling `text/babel` in the browser
- Lucide UMD (`cdn.jsdelivr.net/npm/lucide@0.263.1`)
- Inter from Google Fonts
- Purple gradient (`#667eea` → `#764ba2`), `bg-gray-900`, a `.glass` class that is **not** the Base44 morph-glass skin

`chatvault/index.html` ships `Content-Security-Policy: default-src 'self'` (no CDN, no `unsafe-eval` for Babel). This file cannot load under that CSP. That is a reason not to merge it, not a reason to loosen the policy.

---

## Search — boolean substring, not an engine

`filteredChats` is a `useMemo` over `chats.filter`. The query path is:

```text
chat.summary.toLowerCase().includes(query)
|| chat.content.toLowerCase().includes(query)
|| chat.tags.some(tag => tag.toLowerCase().includes(query))
|| chat.keywords.some(kw => kw.toLowerCase().includes(query))
```

That is a yes/no filter in array order. No inverted index, no BM25F, no field boosts, no ranking, no snippets, no `claim:` / `gap:` / `"phrase"` / `OR`. `useMemo` only avoids recomputing the filter. It is not a search engine.

The git engine remains `chatvault/js/search.mjs` (`chatvault-hybrid-0.2.0`).

---

## Ingest — forbidden credential-leak pattern

```javascript
await fetch("https://api.anthropic.com/v1/messages", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ model: "claude-sonnet-4-20250514", ... })
})
```

No `x-api-key`, no `anthropic-version`, no proxy. Either it is broken (Anthropic will 401) or the next edit puts a key in the page. **Both are defects.** Client-side Anthropic is forbidden to ship. The git engine does not call Anthropic (or any LLM) from the browser.

The prompt asks the model to invent `summary`, `tags`, `codeBlocks`, `actionItems`, `keyDecisions`, `questions`, `keywords`, `suggestedProjectName`. Raw text is kept as `content` but is not an immutable `raw_content` field and is not the product of record.

---

## Storage and schema

| This paste | Git engine |
| --- | --- |
| `localStorage` keys `chatVaultChats` / `chatVaultProjects` | `chatvault` vault JSON |
| `JSON.parse` on first load **with no try** | parse with fallback |
| Chat object: `summary`, `tags`, `codeBlocks`, `actionItems`, `keyDecisions`, `questions`, `keywords`, `platform`, `projectId`, `starred` | `ChatVaultEntry`: immutable raw, provenance, CLAIM_LEDGER, `related_projects` (Books) |
| No `CLAIM_LEDGER` | Ledger statuses, never auto-PROVED |
| No `raw_content` immutability | Raw frozen after ingest |
| No `harmonic_note` even | Glass field was LLM copy anyway; not a ranker |

Export is `{ chats, projects, version: '1.0' }` as a JSON download. The git engine already exports full and professional JSON.

---

## “PRODUCTION-READY MVP REVIEW” is not about this file

That paste claims, among other things:

- Status: production-ready; security/legal/UX checkmarks
- DOMPurify, rate limiting, CSP meta tags, error boundaries
- Market readiness **85%**; needs Stripe and cloud backup
- Product Hunt Tuesday; Form LLC THIS WEEK
- Year 1 revenue **$100K–$1M** (optimistic **$1.2M**)

**None of that is true of the HTML that followed.** This snapshot has no DOMPurify, no Stripe, no CSP, no LLC, no Product Hunt. First-load `JSON.parse` is still naked. The review’s “before: client-side API calls / after: fixed” is a claim about a different or imagined build. The HTML still does the client-side call.

Treat the review as untrusted marketing. Do not copy its checklists into a launch plan.

---

## Ideas worth porting later (not done in this change)

Already in the git engine — **do not duplicate**:

- **Projects** → Books (`related_projects`). Guide already treats books as first-class.
- **Starred** → `entry.starred` + starred filter.
- **Export JSON** → full / professional / per-record.
- **Analytics counts** → Dashboard (`vaultStats`: totals, by AI, by ledger, by project).
- **Platform detect** → `source_ai` on ingest (explicit, not a substring guess).

Maybe later, only if they do not dilute CLAIM_LEDGER / hybrid search / glass look:

- Code-block extraction as **artifacts** derived from records (not an LLM `codeBlocks` array). Git artifacts today come from CLAIM / THEOREM / GAP / ACTION lines.
- Richer project metadata (color, description) on Books — optional, low value.

**Not ported (and must not be):**

- Browser `fetch` to `api.anthropic.com`
- Tailwind/React/Babel/Lucide CDNs
- Purple-gradient restyle over morph-glass
- Stripe, Product Hunt, fake revenue, “85% ready”
- Substring `.includes()` search replacing hybrid BM25F
- LLM summary as the stored record

---

## Owner status

Useful recovered prototype. Not a launch. Search is substring. Anthropic in the browser is not shippable. We archived it. Hybrid engine + glass look stay canonical. Stripe stays off.
