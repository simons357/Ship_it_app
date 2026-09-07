# LISTENER

New product. Isolated under `listener/`. Not Ship It. Not the parked Listener search wildlife-marsh hunt.

Owner: Jonathan Simons.

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

**This build (tonight’s bedtime story + green screen):** https://seamless-dome-ky22y4j.shipstatic.com/

Green screen: https://seamless-dome-ky22y4j.shipstatic.com/bedtime.html

Claim: https://my.shipstatic.com/claim/5d10bed7e23947600972a5373c99449c

**TITAN-X story for an investor (read aloud / LISTEN):** https://precise-prism-3ad673t.shipstatic.com/

Claim that story page: https://my.shipstatic.com/claim/debe8aa2cc7e6c2f1812e61843bcdf9c

If the first screen says **A STORY IS SOMETHING YOU LISTEN TO** and **GREEN SCREEN · READ TO THE CHILDREN**, you have this build. If it says Savannah marsh, Air mode, Water mode, Party mode, or lists clapper rails / painted buntings, that is Claude’s demo, not this app.

The hostname is still random Shipstatic junk, not the product name. A name like Listener needs your Shipstatic or GitHub Pages account. Old hosts such as `dreamy-dust-…` and `spectral-rune-…` are leftovers.

This is LISTENER. Tonight’s bedtime story first — one a day, from famous public-domain books. Then the field. No grocery-store START ball.

1. Open the link in **Safari**.
2. Share → **Add to Home Screen**.
3. Tap **LISTEN** to hear tonight’s story, or **GREEN SCREEN · READ TO THE CHILDREN** to stand in front of the green screen and read it. **I’LL READ** turns the pages. **HIDE BUTTONS** leaves only the words on chroma green.
4. **LISTEN TO THE FIELD** is the wildlife instrument. Allow the microphone. Put the phone down. Tap **STOP THE FIELD**. If it does not know the sound, type what it was (rain) and tap **KEEP**.

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
