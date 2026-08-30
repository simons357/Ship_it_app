# LISTENER

New product. Isolated under `listener/`. Not Ship It. Not the parked Listener search wildlife-marsh hunt.

Owner: Jonathan Simons.

## Status

- Spec: ingested (`MASTER_SPEC.md`, `inbox/MASTER-BUILD-SPEC.md`)
- iPhone web preview: **working** in `app/`
- Native iOS project: `ios/Listener/Listener.xcodeproj` (open on a Mac)
- App Store pack: `store/APP-STORE.md`
- Optional hub: `hub/hub.py`
- Parked threads stay parked — `PARKED-THREADS.md`

## Open on iPhone (Session app — not the parked Listener search)

**Phone URL:** https://dreamy-dust-7649kh8.shipstatic.com/

Claim so it stays live past 3 days: https://my.shipstatic.com/claim/43045a75608088880245004639157041

Do not use leftover random hosts such as `spectral-rune-…`. Those are old free deploys, not the product name. A name like Listener needs your Shipstatic or GitHub Pages account.

This is LISTENER. One **START** button. It becomes **STOP**. No mode quiz.

1. Open the link in **Safari**.
2. Share → **Add to Home Screen**.
3. Tap **START**. Allow the microphone. Put the phone down.
4. Tap **STOP**. If it does not know the sound, type what it was (rain) and tap **KEEP**.

Later: your weather and ChatVault can plug in through `app/js/plugins.js`. Not now.

The same app is on `origin/gh-pages` under `listener/` (existing Pages apps were left in place). The stable GitHub Pages name is https://simons357.github.io/Ship_it_app/listener/ after Pages is enabled in the repo: Settings → Pages → Deploy from a branch → `gh-pages` / root. This environment cannot turn Pages on (`has_pages: false`). Until then that github.io path 404s — use the `/listener` phone URL above.

## Local preview (this VM only — the phone cannot reach it)

```bash
cd listener/app
python3 -m http.server 4173
```

Then open http://127.0.0.1:4173/  
Add `?paired=1` to try “Another Listener is available. LEAVE AS BASE?”

## Optional local hub

```bash
python3 listener/hub/hub.py
```

Hub listens on http://127.0.0.1:7744  
Point the preview at it with `localStorage.setItem('listener.hub','http://127.0.0.1:7744')`.

## Tests

```bash
python3 -m unittest listener.tests.test_listener_core
node --test listener/tests/test_core.mjs
```

Or from this folder:

```bash
cd listener && python3 -m unittest tests.test_listener_core && node --test tests/test_core.mjs
```

## Layout

| Path | Role |
| --- | --- |
| `app/` | Working iPhone PWA (copy the prototype look; real session data) |
| `ios/` | SwiftUI / MapKit / SwiftData Xcode project |
| `hub/` | Optional Session/Node presence + sync queue |
| `store/` | App Store listing + honest upload steps |
| `inbox/` | Owner spec + ChatGPT prototype |
| `PARKED-THREADS.md` | Hard stop on Listener search |
| `AGENTS.md` | Isolation rules |

## Design law

Complex underneath. Obvious on top. No networking vocabulary unless the user opens diagnostics.

Product test: leave one phone as BASE and scout with the other in under a minute.
