# Prototype dump 3 — Evernote HTML

**Archived:** 25 August 2026  
**Snapshot:** [`chatvault-evernote-prototype.html`](chatvault-evernote-prototype.html)  
**Source:** Jonathan paste titled “Chatvault” in the ChatVault build thread. Markdown fences that split `<style>` / `<script>` were stripped; the React/Tailwind body is otherwise the paste.  
**This is not the live product.**

Canonical **look:** selectable skins in `chatvault/css/app.css` (Steel default: charcoal + amber). Morph-glass is **not** a selectable skin. Tagline stays **OS for your AI**.  
Canonical **engine:** git `chatvault/` — `ChatVaultEntry`, `CLAIM_LEDGER`, `chatvault-hybrid-0.2.0`.  
Stripe stays off.

This dump is **not** ChatVault 2, **not** the live steel-vault PWA, and **not** Replit. ChatVault 2 (if present) lives as its own snapshot — do not overwrite it. Do not replace `chatvault/index.html`, `js/app.js`, `js/engine.mjs`, or `js/search.mjs` with this file.

Standing rule: top-of-market, not a thinner Evernote. **This paste is the thinner Evernote.** Archive only.

---

## What it actually is

Single-file React-in-HTML:

- React 18 UMD + ReactDOM + Babel standalone + Tailwind CDN
- **No Lucide. No Anthropic API. No `localStorage`.**
- Purple gradient `#667eea → #764ba2` (same hex as ChatVault 2; **not** morph glass)
- Light gray sidebar + main pane (Evernote-ish list/detail), not `bg-gray-900`, not Base44 grain
- Seeded with **3 hardcoded** chats: Building a React App / ChatGPT, Marketing Strategy Ideas / Claude, Python Data Analysis / Gemini (dates 2024-11-06..08 — demo, not owner research)
- In-memory `useState` only. Reload wipes imports.

`chatvault/index.html` ships `Content-Security-Policy: default-src 'self'`. This file cannot load under that CSP (CDN + `unsafe-eval` Babel). That is a reason not to merge it.

---

## Real vs claimed

| Surface | Implemented in this HTML | Claimed only (assistant COPY or comments) |
| --- | --- | --- |
| Sidebar search | `title` / `preview` / `tags` `.includes()` | Advanced search, quotes for exact phrases |
| Field operators | **Absent.** Query is a raw substring. | `tag:work platform:chatgpt` |
| Platform filter | `<select>` chatgpt / claude / gemini / all | — |
| All vs Starred | Two buttons. `viewMode === 'starred'` filters `conv.starred` | Archive view: `viewMode` comment lists `archived` and the filter checks `conv.archived`, but there is **no Archive button** and seeds have no `archived` field |
| Import | Modal: platform, title, paste content, comma tags → prepends one `{ role: 'user' }` message | “Paste your conversation or **upload JSON**” — no file input |
| Export | `JSON.stringify(conversations)` download of the in-memory array | Markdown export, PDF export, “Select All”, per-conversation export |
| Star / delete | List star toggle + detail-pane star + confirm-delete | — |
| Detail pane | Renders `messages[]` as You / Assistant bubbles | — |
| Folders / projects | **Absent** | “Use folders for projects” |
| Tag editing after import | Tags only on import (comma-separated). No tag icon on a saved chat. | “Add tags (click the tag icon)” |
| Floating 🤖 assistant | `setTimeout(..., 1000)` + `generateAssistantResponse` if/else on `import`/`add`, `search`/`find`, `export`, `organize`/`tag`, `help`/`how` | Comment: “in production, this would call Claude API”. It does not. |
| Keyboard / context menu | **Absent** | Cmd/Ctrl+F, right-click for more options |
| Persistence | None | Implied by “your data” export copy |
| CLAIM_LEDGER / BM25 / hybrid search | **Absent** | — |
| Tagline | “The Evernote of AI Conversations” | Conflicts with locked glass tagline **OS for your AI** |

---

## What this has that ChatVault 2 and glass do not

Keep these as **archive observations**, not a port list.

- **Canned floating assistant.** ChatVault 2 calls Anthropic from the browser (forbidden). Glass uses `InvokeLLM` for a semantic id-ranker and Harmonic Watch copy. Neither ships a 🤖 FAQ bubble with a 1s fake “typing” delay.
- **Import as a modal overlay** (platform + title + paste + comma tags → prepend). Glass/git ingest is a full page (single/bulk/files, source AI, visibility, book). ChatVault 2 is drop-zone + LLM extract into `summary` / `codeBlocks` / `actionItems`.
- **Hardcoded 3-platform seed list** with chatgpt / claude / gemini **badges**, already visible with no storage. ChatVault 2 boots empty from `localStorage`. Glass seed is SaaS demos (rate limiter, CRM), not these three titles.
- **In-memory only** (explicitly no `localStorage`). ChatVault 2 persists. Git vault persists. Glass is a hosted preview.
- **All vs Starred** as the primary list mode. ChatVault 2 has a star field among many filters (tags, date range, code-only, action-items, projects). Glass is a conversation grid, not this All/Starred pair.
- **Light list/detail Evernote chrome** (not ChatVault 2 dark “Intelligence Platform”, not morph glass).
- **Overclaiming assistant COPY** as a specimen of features this HTML does not implement. Useful as a “do not treat marketing as a spec” artifact.

---

## What not to port

- **Canned assistant as product.** Keyword if/else plus a fake delay is not an LLM, not a guide, and not search. Do not wire it to Anthropic from the browser either.
- **“The Evernote of AI Conversations” tagline.** Locked product line is **OS for your AI**. This paste is the thinner Evernote; we are not shipping that positioning.
- **Substring-only search.** `.includes()` on title/preview/tags is a yes/no filter in array order. Canonical search remains `js/search.mjs` (`chatvault-hybrid-0.2.0`). Do not replace it. Do not add a `tag:work platform:chatgpt` parser that the assistant merely *talks about*.

Also do not port: Lucide-free is fine but irrelevant; no persistence is a demo constraint not a product goal; seed dates from 2024 are not research memory; `ReactDOM.render` + Babel-in-browser is not the PWA stack.

---

## Optional later (UX only, if it beats the current vault form)

The **import modal** is the one piece that might be worth stealing *as a pattern*, not as code:

- Overlay: platform select, title, paste, comma tags, Import / Cancel
- Prepends to the list and selects nothing until the user clicks the new row
- Cheaper than navigating away to a full ingest page for a one-off paste

Compare to git ingest (`js/app.js` `renderIngest`): dedicated view, source AI, professional/private, optional Book, Extract & index into `ChatVaultEntry` / ledger. That form is the product. If the modal ever lands, it must still call `ingestPaste` (immutable raw, provenance, ledger UNREVIEWED) — not `messages: [{ role: 'user', content: importContent }]`.

Do not take: JSON-upload copy that has no file input, alert() success toasts, or storing the paste as a single user turn.

---

## Verdict

Third HTML dump. Distinct from ChatVault 2 (Lucide + Anthropic + `localStorage` + projects/analytics) and from glass (morph, Drive, Harmonic Watch, LLM rank). Archive it under `chatvault/prototypes/`. Ship the steel-vault PWA + hybrid ranker.
