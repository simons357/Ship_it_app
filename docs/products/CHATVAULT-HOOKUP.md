# ChatVault — safe hookup guide

**Date:** 2026-08-28  
**Branch evidence:** `cursor/tao-snd-h-panel-a0eb` (math/audit repo) + portfolio history on `intro-portfolio-e279` / `work-showcase-b71c` / `gh-pages`  
**Platform context:** ChatVault is a **vault + search Lego block** on the shared platform spine, not a standalone stack. See [`MODULAR-PLATFORM-LEGO.md`](MODULAR-PLATFORM-LEGO.md). Registry entry: `packages/shared_core/product_registry.json` → `chatvault` (`status: hollow`).  
**Direct answer:** **No — not “just a link.”** A URL alone is not a safe or honest hookup today. Ship a working MVP, verify public access, then link from catalog/outreach with explicit auth and secrets rules.

---

## 1. What ChatVault appears to be in Jonathan’s stack

| Signal | Evidence |
| --- | --- |
| **Product concept** | “The Evernote of AI conversations” — vault agent threads and return to them cleanly |
| **Tier** | Tier 2 in `docs/KEEP-CUT-INVENTORY.md`: *“Hollow public URL — Ship a real MVP or drop from catalog”* |
| **Public route** | `https://primefield.tech/chatvault` (Base44 SPA route on `primefield.tech`, not a standalone repo in this workspace) |
| **Implementation in repo** | **None.** No ChatVault source, API, env, or tests on this branch. Only inventory/catalog mentions. |
| **Mirrored shell** | `gh-pages` → `apps/primefield/chatvault/index.html` is a generic Prime Field Technologies SEO shell (company blurb + empty `#root`), not a working archive UI |
| **Search report** | `partner-packet/REPORT-lattice-paint.md` (lattice/resin paint search, not ChatVault-specific) lists `/chatvault` as an existing primefield.tech route with **no product content** |
| **Stack neighbors** | Same hosting lane as other Base44 apps (Maritime, ExoRatio, Solenne); contrast with **Field Lock** (live Replit kiosk + NDA depth) and **Kyrana** (GitHub repo) |

**Bottom line:** ChatVault is a **named catalog item and route placeholder**, not a shippable product in this repo yet.

---

## 2. Is “just a link” sufficient?

**No.**

| If you only paste a link | What goes wrong |
| --- | --- |
| Today’s `primefield.tech/chatvault` | Documented as **hollow / empty shell** — bad first impression, looks broken |
| Base44 permission state (2026-07) | Strangers may see *“Couldn't load the app / You may not have permissions”* — same class of failure as other `*.base44.app` apps (`BASE44-PUBLIC.md`) |
| AI chat archive product | Storing/searching conversations implies **auth, encryption, retention, and secret-handling** — none of which a naked URL provides |
| Outreach policy | Portfolio commits explicitly say **do not cold-send** ChatVault until a **working live URL** is pasted and verified |

**Minimum safe hookup (when MVP exists):**

1. Build/publish a real ChatVault app (Base44, Replit, or dedicated host).
2. Confirm in **incognito / logged-out** browser that strangers see the product, not permissions or empty shell.
3. Paste the verified URL into address lists (`ADDRESSES.md`, showcase) — replace `_______________` placeholders.
4. Document **who can sign up**, **what gets stored**, and **what must never be pasted into chats**.
5. Only then add to cold outreach (optional fourth link), partner packet, or site entry list.

Until then: **name it on a call** or **drop from catalog** per KEEP-CUT-INVENTORY.

---

## 3. Security checklist

### Auth & access

- [ ] **Public publish verified** — incognito load succeeds (see `BASE44-PUBLIC.md` fix steps).
- [ ] **User accounts** — email/OAuth or magic link; no shared demo login in outreach.
- [ ] **Per-user isolation** — users cannot read others’ vaults (row-level security if using Supabase/Base44 backend).
- [ ] **Session TTL** — short-lived tokens; logout everywhere option.

### Tokens & API keys

- [ ] **Server-side secrets only** — LLM provider keys, Supabase service role, encryption keys in env — **never** in client bundle or git.
- [ ] **Scoped API keys** — if importing from ChatGPT/Claude/etc., use vendor OAuth or export flows; don’t ask users to paste long-lived keys into the UI unless encrypted client-side with clear warnings.
- [ ] **No keys in repo** — follow Field Lock pattern: public kiosk/demo; **NDA vault** for architecture depth (`FIELD-LOCK.md` guardrail).

### Secrets in chat history (critical for a “chat vault”)

Chat archives are a **secret leakage surface**. Treat stored threads like credential stores:

- [ ] **Block or warn** on paste patterns: API keys, `sk-…`, `Bearer …`, private keys, `.env` dumps, JWTs, passwords.
- [ ] **Redact on ingest** — scan at import time; optional manual “mark as sensitive” tag.
- [ ] **No training on customer vault** without explicit opt-in (if using third-party models).
- [ ] **Export controls** — encrypted export; warn that exported files contain conversation secrets.
- [ ] **Deletion** — hard delete + retention policy documented in UI.

### HIPAA / clinical (Prime Field context)

ChatVault is **not** documented as a clinical product (unlike **Vigilant Patch**, **Solenne**, CRNA/OR lane).

| Scenario | Guidance |
| --- | --- |
| **Personal / business AI memory** | Default stance: **not HIPAA-covered** if no PHI is stored — still avoid patient identifiers in vault by policy. |
| **CRNA / clinical workflows** | **Do not** store patient data, OR records, or identifiable PHI in ChatVault unless you run a full HIPAA program (BAA, audit logs, encryption at rest/transit, access controls). Use **Vigilant Patch / Solenne** regulatory path separately (`VIGILANT-PATCH.md`: FDA path before deep disclosure). |
| **Partner sends** | Same as `DISTRIBUTION-PIPELINE.md` send check: **no vault, no secrets, no clinical claims** in cold email. |

### Outreach & reputation

- [ ] **Send check** before any link leaves (`DISTRIBUTION-PIPELINE.md`): links open, no dead/gated shells, one ask, 5★ business tone.
- [ ] **Do not cold-send** hollow `primefield.tech/chatvault` (documented in OUTREACH / ADDRESSES history).
- [ ] **Label status** — “beta / demo / MVP” honestly; Tier 2 until proven.

---

## 4. Recommended integration pattern (per product in stack)

Patterns observed in repo history — **not ChatVault-specific code**:

| Product | Pattern | Safe hookup |
| --- | --- | --- |
| **ChatVault** (target) | Base44 route on `primefield.tech` + optional gh-pages mirror | **Public SPA deep link** after MVP + auth backend; mirror via `sync_hosted_apps.py` pattern if staying on Base44 |
| **Field Lock** | **Replit live kiosk** + NDA for PUF/CTW | Link `https://field-lock.replit.app/`; skip empty `primefield.tech/field-lock`; depth under NDA (`FIELD-LOCK.md`) |
| **NAV-42** | Replit demo | Direct public URL; provisional claims frozen until metered pilot |
| **Maritime / ExoRatio / Solenne** | Standalone `*.base44.app` | Fix Base44 **Public** publish first; no iframe/OAuth docs in repo |
| **Kyrana** | GitHub repo | Source-visible oracle; link to repo |
| **Ship It** | GitHub tooling in repo family | Clone/install; no hosted vault |
| **FieldEncrypt / DIU** | Name + NDA vault | No public integration — partner packet under NDA |
| **primefield.tech hub** | Base44 platform host | Routes: `/chatvault`, `/field-lock`, `/games` — all gated/empty until republished |

**ChatVault-specific recommendation:**

1. **Host:** Either dedicated Base44 app (like Solenne) **or** Replit/Vercel app with its own URL (cleaner than nested `/chatvault` route).
2. **Integration style:** **Deep link + sign-in** — users bookmark one URL; no iframe embed of third-party chat UIs unless CSP and cookie rules are tested.
3. **Import:** Prefer vendor **export file upload** or **OAuth read-only** (if available) over copy-paste of raw API keys.
4. **Webhooks:** Only if you need live sync from another product; require HMAC signature verification and idempotency — **not present in repo today**; add when MVP scope is clear.
5. **Catalog wiring:** Update `ADDRESSES.md`, showcase `index.html`, `KEEP-CUT-INVENTORY` tier — same playbook as Field Lock URL restore (commit `010ea99`).

---

## 5. Generic safe hookup (chat archive / search vault products)

Use when the product is **not** in repo (current state):

### Architecture minimum

```text
[Browser] → HTTPS → [Your app + auth] → [Encrypted store] → [Optional LLM for search]
                         ↑
                   never log raw secrets
```

### Hookup steps

1. **Choose identity** — OAuth (Google/GitHub) or email magic link; MFA for paid tiers.
2. **Encrypt at rest** — database + object storage; per-user or per-vault keys if feasible.
3. **Ingest pipeline** — import JSON/MD exports; strip secrets; index for search (local or server-side embeddings).
4. **Verify public URL** — incognito, mobile, cold email recipient POV.
5. **Privacy policy + ToS** — what you store, retention, deletion, subprocessors (OpenAI, Anthropic, Supabase, etc.).
6. **One link in catalog** — only after steps 1–5 pass.

### What “just a link” is enough for

- Marketing landing page with **waitlist** (no data stored yet).
- **Private beta** link behind allowlist — send only to named testers, not cold outreach.

### What requires more than a link

- Storing user conversations.
- Search across threads.
- Any claim of “secure vault” or “encrypted archive.”
- Clinical or regulated content.

---

## Quick reference

| Question | Answer |
| --- | --- |
| Is ChatVault in this repo? | **No** — catalog/docs only |
| Current URL | `https://primefield.tech/chatvault` — **hollow / not MVP** |
| Cold-send today? | **No** |
| Just a link when live? | **Link + auth + storage policy + secret redaction + incognito verify** |
| Closest working pattern | Field Lock Replit kiosk + NDA depth (`FIELD-LOCK.md`) |
| Related docs (other branches) | `partner-packet/BASE44-PUBLIC.md`, `FIELD-LOCK.md`, `DISTRIBUTION-PIPELINE.md`, `docs/KEEP-CUT-INVENTORY.md`, [`MODULAR-PLATFORM-LEGO.md`](MODULAR-PLATFORM-LEGO.md) |

---

*When a live ChatVault URL works in incognito, paste it here: _______________ and bump Tier 2 → Tier 1 in KEEP-CUT-INVENTORY.*
