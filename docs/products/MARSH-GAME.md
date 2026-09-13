# Marsh game — locator

**Date:** 2026-08-29  
**Branch evidence:** `cursor/tao-snd-h-panel-a0eb` + live `primefield.tech` probe + all remote branches grepped  
**Direct answer:** Named public route exists; **no playable game** in this repo or on that URL today.

---

## 1. Exact URL / path

| Location | Result |
| --- | --- |
| **Canonical public route** | https://primefield.tech/marsh |
| **In-repo source / playable build** | **None** (no `*marsh*` files on any remote branch) |
| **`product_registry.json`** | **Not listed** |
| **`docs/KEEP-CUT-INVENTORY.md`** | No “Marsh” row — only generic **ProVR / AI Surgeon VR / games** (long-cycle) |
| **Partner `ADDRESSES.md` (Games)** | Lists hub / risk / pacman / AI Surgeon VR — **not Marsh** |
| **`gh-pages` mirror** | Has `apps/primefield/games/` and `pacman/` — **no `marsh/` folder** |

Related hollow title-only route (not a game either): https://primefield.tech/hop

---

## 2. How to open / run

1. Open **https://primefield.tech/marsh** in a browser (incognito preferred for honesty check).
2. There is **no** local clone/run path in `Ship_it_app` — nothing to `npm start` or `python -m http.server` for Marsh.
3. Closest catalog entry point if you meant “the games hub” instead: https://primefield.tech/games

---

## 3. Status (ChatVault-class)

**Hollow** — same pattern as ChatVault / `/games` / `/pacman` shells:

- HTTP **200** with title **“Marsh \| Prime Field Technologies”** and canonical `/marsh`
- Body is Base44 SPA chrome: empty `#root` + hidden SEO snapshot (company blurb + Home / Manage Panels links)
- Shared JS bundle (`/assets/index-OJJeNk2-.js`) contains **zero** matches for `marsh`, `hopping`, `frog`, `lily`, `pacman`, `chatvault`, `/games`, `/risk`
- Not a shipped MVP; not registered as live in `packages/shared_core/product_registry.json`

Until a real playable build is published and verified logged-out, treat like ChatVault: **do not cold-send**; ship MVP or drop from catalog.

---

## 4. “Hopping” mechanic notes

**None found** in git (this branch or remotes), inventory, registry, or partner packet.

User phrasing (“about to start hopping” / “see if it works”) has no matching GDD, controls doc, or code. The sibling route `/hop` is also a **title-only hollow shell**, not a hop mechanic.

---

## 5. Nearby games (if Marsh was a nickname)

| Name | URL | Playable? |
| --- | --- | --- |
| Games hub | https://primefield.tech/games | Hollow shell |
| Strategy (RISK wink) | https://primefield.tech/risk | Playable blank in ADDRESSES |
| Pac-Man retro-3D | https://primefield.tech/pacman | Playable blank in ADDRESSES |
| AI Surgeon VR | script only under `docs/products/vr-surgeon/` | No playable URL |

---

## 6. Next move (if you still want to hop)

1. Paste a **working** Base44 / Replit / itch / itch-style playable URL when it exists.
2. Verify in **incognito** (no permission wall, real gameplay).
3. Then add to `product_registry.json`, KEEP-CUT, and `ADDRESSES.md` Games section — replace blanks.
