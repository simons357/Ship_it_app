# Arbiter app — locator

**Date:** 2026-09-04  
**Branch evidence:** `cursor/tao-snd-h-panel-a0eb` + live URL probe + all remote branches grepped  
**Direct answer:** **Yes — live Base44 app.** Open https://arbiter.base44.app/ (not the hollow hub route).

---

## 1. Found?

| Check | Result |
| --- | --- |
| Workspace `rg -i arbiter` | **No matches** (before this doc) |
| `product_registry.json` | **Not listed** (before this update) |
| `docs/KEEP-CUT-INVENTORY.md` | **No Arbiter row** |
| `docs/products/` prior docs | **None** |
| Partner inventory / ADDRESSES (portfolio branches) | **Not listed** (Aug 2026 scrape) |
| App portfolio census (`APP-PORTFOLIO-2026-08.md`) | **Not among 26 named software products** |
| `git log --all --grep=arbiter` / `*arbiter*` paths | **Empty** |
| Live hosts | **Yes** — Base44 + hollow primefield hub route |

---

## 2. Exact URL(s) / paths

| Location | URL / path | Role |
| --- | --- | --- |
| **Canonical (use this)** | https://arbiter.base44.app/ | Live Base44 SPA |
| Hub route (do not cold-send) | https://primefield.tech/arbiter | Hollow title-only shell |
| Replit probes | `arbiter.replit.app`, `arbiter-app.replit.app` | **404** |
| In-repo source | **None** | No `*arbiter*` files on any remote branch |
| Base44 app id (from page telemetry) | `69a1d61a35e5ca69629e7491` | Hosted on Base44/Supabase assets |

### Public pages advertised by the SPA SEO snapshot

`/AdminCleanup`, `/ArbiterPanel`, `/Friends`, `/ManageTournament`, `/MyGames`, `/MyTournaments`, `/PlayerOverview`, `/Settings`, `/Tournament`, `/MyClubs`, `/ClubDetails`

---

## 3. Status

| Surface | Status |
| --- | --- |
| **arbiter.base44.app** | **Live** — HTTP 200, title `Arbiter`, real product meta/description, PWA manifest, JS bundle |
| **primefield.tech/arbiter** | **Hollow** — same ChatVault/Marsh pattern: company blurb + Home / Manage Panels only |
| Catalog / KEEP-CUT | **Previously unknown** — missing from inventory until this locator |
| This git repo | **No implementation** — external Base44 host only |

**Caveat (shared with other Base44 apps):** strangers may still hit permission walls depending on Base44 publish settings. Verify in **incognito** before outreach. Prefer the `*.base44.app` canonical URL over the hollow hub route (same policy as Field Lock → Replit).

---

## 4. What Arbiter is supposed to do

From live meta description / SEO snapshot on https://arbiter.base44.app/ (not from in-repo docs — none existed):

> A streamlined application for organizing and tracking **chess tournaments**. Players can sign in, view their game schedule, enter match results, and report issues, while **arbiters** manage accounts, oversee results, and resolve disputes.

Role split implied by routes: player views (`MyGames`, `MyTournaments`, `PlayerOverview`) vs arbiter/admin (`ArbiterPanel`, `ManageTournament`, `AdminCleanup`) plus clubs/friends/settings.

**Not** related to Field Lock crypto, Millennium math, or the sports-officials “ArbiterSports” consumer apps on app stores.

---

## 5. How to open it

1. Open **https://arbiter.base44.app/** in a browser (incognito for a fair public-access check).
2. Do **not** send https://primefield.tech/arbiter as the product — that route is a hollow Prime Field shell.
3. There is **no** local clone/run path in this repo (`npm start` / `python -m http.server` will not boot Arbiter).
4. Base44 dashboard (if you own the workspace): https://app.base44.com/ — app id `69a1d61a35e5ca69629e7491`.

---

## 6. Registry / inventory follow-ups

- Entry added under `packages/shared_core/product_registry.json` → `arbiter`.
- Optional later: Tier-2 row in `docs/KEEP-CUT-INVENTORY.md` and partner `ADDRESSES.md` once public permissions are confirmed.
