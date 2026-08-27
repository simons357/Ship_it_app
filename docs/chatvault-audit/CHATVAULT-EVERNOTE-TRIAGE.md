# ChatVault Evernote-tagline HTML — triage

**Archived:** 25 August 2026  
**Snapshot:** [`evidence/html-snapshots/CHATVAULT_EVERNOTE.html`](evidence/html-snapshots/CHATVAULT_EVERNOTE.html)  
**SHA-256:** `a18bae982aa57e7cfdbe20e47d72e3109e5fae51f32fbde2d97ec5ec89ed0997`  
**Source:** Jonathan paste in the ChatVault build thread (prefix `Chatvault`). Chat markdown fences were stripped; the React/Tailwind body is otherwise the paste.  
**This is not the live product.** Canonical look remains Base44 morph-glass “OS for your AI”. Canonical engine remains git `chatvault/` (CLAIM_LEDGER + hybrid BM25F). Stripe stays off.

Distinct from ChatVault 2 (`CHATVAULT_V2_REACT_CDN.html`): that later paste is the purple “Intelligence Platform” with an Anthropic `fetch`. This file is the earlier/lighter sidebar demo.

## Blunt status

| Claim in the paste | Reality |
| --- | --- |
| “The Evernote of AI Conversations” | Marketing tagline. Same line already appeared in git on 14 Jul 2026. Not a moat. |
| Search | `String.includes()` on `title`, `preview`, and `tags`. No index, no ranker, no operators. |
| `tag:work platform:chatgpt` | **Copy only.** The assistant suggests that syntax. The filter does not parse it. |
| Floating 🤖 assistant / “would call Claude API” | Comment is false in this file. `setTimeout(…, 1000)` plus `generateAssistantResponse` if/else on keywords (`import`, `search`, `export`, `organize`/`tag`, `help`/`how`). Scripted FAQ. Not Claude. |
| Import | Modal: platform, title, content, tags. Content becomes one user message. No LLM extract. |
| Export | `JSON.stringify` of the in-memory `conversations` array. No persistence (`localStorage` unused). Reload wipes imports. |
| Seed data | Three demos dated **2024-11-06..08**: “Building a React App” (ChatGPT), “Marketing Strategy Ideas” (Claude), “Python Data Analysis” (Gemini/CSV). Not owner research. |
| CLAIM_LEDGER / BM25 / harmonic engine | **Absent.** |

## What is useful

UX history only: light sidebar + main pane, purple `#667eea → #764ba2` header, platform badges, star, import modal, JSON dump. Keep as a read-only snapshot.

## What must not happen

- Do not replace `chatvault/index.html` with this file.
- Do not wire the floating bot to Anthropic from the browser.
- Do not treat canned replies as a search engine or as “AI organization.”
- Do not enable Stripe from any sibling “production-ready” paste.

## Verdict

Earlier/lighter prototype. Archive it. Ship the glass PWA + hybrid ranker.
