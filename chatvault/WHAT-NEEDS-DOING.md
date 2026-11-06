# What needs to be done

Owner ask, 6 November 2026: assure the search engine is amazing; mix the
format so it is not Evernote; make the repo a versatile work of art with
visualizations that show where everything is.

This file is the work list. The atlas in the app is the picture.

## Done in this pass

1. **Ranked hybrid search** (`js/search.mjs`, `chatvault-hybrid-0.2.0`).
   Boolean syntax is the match gate. Ranking is BM25F + character 3-grams +
   field-weighted TF-IDF cosine, fused with RRF (k=60), optional RM3.
   Title outranks a body mention. `"phrases"` and `claim:` / `gap:` / `theorem:`
   are hard gates. Ledger status is **never** a score.
2. **Atlas, not notebooks.** Default surface is a constellation: clusters by
   project, star size = claims+theorems+gaps, edges = shared tags. Ranked
   beams sit beside the sky. There is no notebook stack.
3. **Map of the tree** — this file, `js/ENGINE.md`, and the canvas atlas.

## Do next (ordered, cheapest first)

| # | Work | Why | Difficulty |
|---|---|---|---|
| 1 | Export Base44 glass source yourself | Archive the look. We cannot log in. | 15 min, you |
| 2 | Open the atlas locally and ingest a week of *your* chats | Search quality is proven on *your* corpus, not fixtures | Low |
| 3 | Private GitHub repo named `chatvault` | `Ship_it_app` is a workshop. Do not tag `main` as the product | Low |
| 4 | IndexedDB instead of localStorage | Quota freeze on a real corpus | Medium |
| 5 | Port morph-glass *skin* onto this atlas | Skin only. Do not copy Base44 list/LLM logic | Medium |
| 6 | PDF/DOCX text extract | Stubs exist conceptually; OCR is not here | High |
| 7 | Private HTTPS origin for the PWA | Add to Home Screen off localhost, still no public site | Medium |
| 8 | Dense MiniLM/E5 into the same RRF | Only if it beats this eval on your corpus | High |
| 9 | Genuine native layer / private TestFlight | After 2–7. Not a Base44 wrapper. Not a store listing | High |

## Three products mixed in the last ask (do not fuse them)

| You asked | What it actually is | Verdict |
| --- | --- | --- |
| Personal atlas + hybrid search + skins | This repo | **Do this.** Mobile = PWA on the phone. |
| “Run like a top / stunning / lots of skins” | Design pass on the PWA | **In progress** (Nocturne, Vellum, Observatory, Steel, Ink, Signal, Day). |
| App Store native, accepted faster because mobile | A second product | **No.** A wrapper is slower and likelier to be rejected (Guideline 4.2). Native tabs + on-device search is the only honest store path, and it is a rebuild, not a shortcut. |

Weekly search evals, persistent memory beyond this device, and a public address are **not** in the PWA until you want a hosted private origin.

## Will not do (locked policy)

- App Store listing, Stripe, support inbox, circulating the Base44 preview URL.
- LLM “semantic” toggle that invents ranks.
- Calling the ledger spectrum a truth meter.
- Evernote notebooks, yellow notes, or a clipper grid as the home screen.

## How to see it

```bash
cd chatvault
node --test tests/*.mjs
python3 -m http.server 4173
```

http://127.0.0.1:4173/ — type `claim:definitional`, `"finite-time blow-up"`, `gap:blow-up`.
The sky should dim non-hits. The beam list should rank.
