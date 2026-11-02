# LISTENER

New product. Isolated under `listener/`. Not Ship It. Not the parked Listener search wildlife-marsh hunt.

Owner: Jonathan Simons.

## If someone in Savannah government asks

Do not explain the product from memory. Give them `SAVANNAH.md`, or open `app/savannah.html`. It says what Listener is, what it is not, and the small ask (one listening hour — not a contract, not surveillance). Home is Wilmington Island / Chatham County. City offices are a separate door.

## Hand this to Base44

Do not explain the product. Paste `BASE44_PROMPT.txt` into a new Base44 app. Steps are in `BASE44.md`.

## Status

- Spec: ingested (`MASTER_SPEC.md`, `inbox/MASTER-BUILD-SPEC.md`)
- iPhone web preview: **working** in `app/`
- Native iOS project: `ios/Listener/Listener.xcodeproj` (open on a Mac)
- App Store pack: `store/APP-STORE.md`
- Optional hub: `hub/hub.py`
- Parked threads stay parked — `PARKED-THREADS.md`

## Open on iPhone (Session app — not the parked Listener search)

**This build:** https://edgy-outpost-8k424wz.shipstatic.com/

Claim (or it expires in about three days): https://my.shipstatic.com/claim/f2a5dbc7b815e72ff1983f1d10397be1

The hostname is random Shipstatic junk, not the product name. Safari → Add to Home Screen. The icon is the name.

If the first screen is a porch with the amber home node and rings, **LISTENER** / **WHAT THE WILD IS SAYING**, and **LISTEN TO THE FIELD**, you have this build. After STOP, **maybe** ID chips. The field has HOME, trail, PARK CAR, RETURN. If it says Savannah marsh, Air mode, Water mode, Party mode, or lists clapper rails / painted buntings as live animals on a map, that is Claude’s demo, not this app.

The hostname is still random Shipstatic junk, not the product name. A name like Listener needs your Shipstatic or GitHub Pages account. Old hosts such as `dreamy-dust-…` and `spectral-rune-…` are leftovers.

This is LISTENER. Listen to sounds. Try to ID birds, dolphins, and critters around the house. Keep what you heard. Field trail home, steps, parked car. No grocery-store START ball. IDs are maybe, not claims.

1. Open the link in **Safari**.
2. Share → **Add to Home Screen**. The icon is the name.
3. **LISTEN TO THE FIELD**. **STOP THE FIELD**. Type what it was or tap a maybe chip, or leave UNKNOWN.
4. **OPEN FIELD** for the trail, steps, **PARK CAR**, **RETURN**.
5. **STORY · LESSON** is still there, folded. **GREEN SCREEN** is the chroma page.

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

The mark is a home node with rings going out — listening for non-human biological signals. Black tile, amber glow. Do not replace it.

Product test: leave one phone as BASE and scout with the other in under a minute.
