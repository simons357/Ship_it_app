# Apple Store and acquisition path

Status on 24 August 2026: **not ready to submit to Apple. not an acquisition close.**
The Base44 “OS for your AI” vault is the product look to keep. This git engine is
the first maintainable backend for that look.

## Best version (reconfirmed)

Live preview hash of Base44 `6a58e103fedcde66a0a7710e` still matches the audit freeze:

`720a21e0e061997909f4ea6ca85caeff60a08af8b1d5157081746a76ff6ba8de`

Keep that Base44 record. Do not delete it. Do not treat its public preview as
the private product.

## What has to be true to beat clipper competitors

Clippers already store chats. The engine that can be sold is:

1. Raw conversation never replaced by a summary.
2. Source AI and source file stay attached.
3. Claims / theorems / gaps are first-class and searchable.
4. Ledger statuses are human-reviewed. Nothing auto-PROVED.
5. Private material can be excluded from a professional export.

That stack is in `chatvault/js/engine.mjs` with tests.

## Apple blockers that still remain

| Item | Now | Still needed |
| --- | --- | --- |
| Stable UI | local PWA-style web app | signed iOS wrapper (Capacitor or similar) |
| Account creation | none (local-only) | only if you ship accounts |
| Privacy policy | in-app Privacy view | hosted URL Apple can fetch |
| Account deletion | wipe local vault | if accounts exist, server-side deletion |
| Data export | full + professional JSON | keep this |
| Payments | none | do not add Stripe to get into the store |
| Crash / offline | browser localStorage | TestFlight crash reports, explicit offline banner |
| IP / licenses | this original engine | inventory Base44/Recharts if you wrap that UI |

A web preview is not an App Store product. Do not upload this folder to App Store Connect.

## Acquisition blockers that still remain

- No users, no revenue, no usage metrics.
- Base44 preview is world-writable; do not pitch it as a secure vault.
- Inventorship of the Base44 UI vs this engine vs Claude-origin code is unset.
- Do not pitch ChatVault as a truth engine or a solved-math product.
- Counsel has to look at public disclosure (portfolio + live preview) before any IP talk.

## Recommended next 5 product steps

1. Export the Base44 app source and keep it archived next to this engine.
2. Connect this engine to the glass UI, or restyle this UI until it matches the morph-glass look 1:1.
3. Add authenticated hosting (not the public `preview--` host).
4. Add PDF/DOCX ingest without dropping raw bytes.
5. Only then talk TestFlight / acquirer demo with a scripted vault of *your* research, not the SaaS seed chats on Base44.
