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

**Phone URL:** https://listener-session.surge.sh/

This is the LISTENER Session PWA (field instrument). It is not the parked Listener search wildlife-marsh hunt.

1. Open the HTTPS link in **Safari** (not Chrome).
2. Share → **Add to Home Screen**.
3. Tap **START**. Allow the microphone if asked. Tap **STOP** when you are done.
4. The recording stays on the phone. UNKNOWN stays UNKNOWN. Not a species. Not sent anywhere unless you opt in.
5. **Field instrument** is a small later link. You do not need it to record.

The same PWA is also on the random shipstatic hosts (fallback): https://nova-bolt-57jc24t.shipstatic.com/ and the earlier https://shaped-bit-57sa6gs.shipstatic.com/. Shipstatic named hosts like `listener.shipstatic.com` need an account; they 404 until someone claims a deploy and runs `ship domains set listener.shipstatic.com <deployment>`. Claim the latest shipstatic copy so it stays live past 3 days: https://my.shipstatic.com/claim/ae3b1170565c1686b8f9e820f0bd3266

The same app is on `origin/gh-pages` under `listener/` (existing Pages apps were left in place). The stable GitHub Pages name is https://simons357.github.io/Ship_it_app/listener/ after Pages is enabled in the repo: Settings → Pages → Deploy from a branch → `gh-pages` / root. This environment cannot turn Pages on (`has_pages: false`). Until then that github.io path 404s — use the surge phone URL above.

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
