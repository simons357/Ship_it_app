# Field Lock — snapshot

This directory is a **snapshot of a live public kiosk**, not a rewrite.

| | |
| --- | --- |
| **Live demo** | https://field-lock.replit.app/ |
| **What it is** | Learning kiosk: presence-bound, single-use keys from real-world conditions (acoustic excite → sense → prime-frequency bins / PUF-style fingerprint). Auth, not a medical app. |
| **Owner evidence** | Named Field Lock in Jonathan’s partner packet (`partner-packet/FIELD-LOCK.md` on `cursor/intro-portfolio-e279`) and Aug 2026 portfolio census. Same Replit SPA pattern as Chat Vault. Anesthesia notes on this VM mention “maritime/Field Lock.” |
| **Replit editor** | Private / gone. `/__repl` → `https://replit.com/replid/27679f17-7419-4521-a669-7f5923de7d64` → `{"message":"Repl not found"}` (26 Aug 2026). |
| **GitHub source repo** | None under `simons357`. Do not confuse with other people’s `field-lock` GitHub projects. |
| **Already mirrored** | `origin/gh-pages` `apps/field-lock/` (same `index-DtSAhZIZ.js` / `index-B0L9Do6D.css` hashes as the live host). |
| **Not this** | `https://primefield.tech/field-lock` — Base44 company shell, not the kiosk. `https://voice-analysis.replit.app/` is **Navia** (thenavia.com), not Jonathan. |

## What is in this snapshot

- `snapshot/index.html` — public HTML from the live host (Last-Modified 16 Dec 2025).
- `snapshot/api/scenarios.json` — public `GET /api/scenarios` (six teaching scenarios). This is the only unique content that is not a minified React vendor bundle.

Full frontend JS/CSS (~364 KB minified) stays in `/tmp/engine-hunt/fieldlock/` on the hunt VM. It is already on `gh-pages`. Not re-vendored here.

## Hashes (26 Aug 2026 fetch)

```
53cd8b403a1813ef2b34b63895f6212412916bc5969df5578f1943b1e928572c  index.html
ff3daeef485c8e55bb2946afc6748f63efa024182e9f450fd1a4588d582619fb  api/scenarios.json (raw)
735d468f461238ee0461103171442a080a68c7aae1962a8bc12a676e8f7964db  assets/index-DtSAhZIZ.js
6a70e835faf57a88e7758d13ebd250b03ae5a2a6fc4228b291e9a753d53b4f20  assets/index-B0L9Do6D.css
```

## API (public)

| Path | Result |
| --- | --- |
| `/api/scenarios` | 200, six scenarios |
| `/api/auth/me` | 401 `{"error":"Not authenticated"}` |
| `/api/auth/login` | SPA fallback (no public login page dump) |
