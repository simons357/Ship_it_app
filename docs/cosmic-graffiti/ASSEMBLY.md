# Assembly desk — how Jon puts a chapter out

Adult plain English. One workspace. Not a swarm of agents. Not ten
thousand staff. A rundown, cue cards, and empty trays.

**Cosmic Graffiti** is the magazine. **The Frequency** is the news.
**VAL8000** is the resident commentator in a *little box* on the entry —
never the story lead. **Domain Architect** is the local lab, not a public
website.

Live magazine (do not smash this):
[cosmic-graffiti-magazine.vercel.app](https://cosmic-graffiti-magazine.vercel.app/)

Substack (this Jonathan, not the education-policy namesake):
[jonathansimonscrna.substack.com](https://jonathansimonscrna.substack.com)

Skool: the classroom that already has Issue 1. Paste into the thread.

Paywall stays **off**. Domain Architect does **not** file patents.

---

## What this desk is

Each magazine chapter/entry is a **card**. You assemble it once, then
export three ways:

| Out | What you get | Where it lives |
|---|---|---|
| **Magazine** | HTML/markdown in the live navy/gold chrome | `entries/<slug>/magazine.md` and the local board |
| **Substack** | Paste-ready title, dek, body, image list, alt text | `entries/<slug>/substack.md` |
| **Skool** | Shorter hook, images, “ask in this thread” | `entries/<slug>/skool.md` |

Machine rundown: [`desk/rundown.json`](desk/rundown.json).  
Local board (workspace, not a second brand):
[`desk/public/index.html`](desk/public/index.html).

Print paste-ready copy without opening a dozen folders:

```bash
python3 scripts/cg_desk.py list
python3 scripts/cg_desk.py show issue-1
python3 scripts/cg_desk.py substack issue-1
python3 scripts/cg_desk.py skool issue-1
```

Open the board in a browser. If pictures do not load from a double-click,
from the repo root:

```bash
python3 -m http.server 8766 --directory docs/cosmic-graffiti/desk/public
```

Then visit `http://127.0.0.1:8766/`. That is a **local preview**. It is
not a live deploy.

---

## How to add a chapter

1. Pick a **slug** — short, lowercase, hyphens. Example: `coffee-swirl`.
2. Make a folder `docs/cosmic-graffiti/desk/entries/<slug>/`.
3. Put three files in it:
   - `magazine.md` — the story, Issue 1 quality. Wonder first. Labels loud.
   - `substack.md` — title, dek, body, image list with alt text.
   - `skool.md` — shorter hook, images, a line that says **ask in this thread**.
4. Drop pictures in `entries/<slug>/assets/`. Every picture earns a caption
   and alt text. Teaching pictures first. Decorative noise last.
5. Optional: `val.md` — VAL8000’s comment **after** the news. A little box.
   Not the headline. Not the masthead lead. Funny is allowed. Deep is
   allowed. Fake theorems are not.
6. Add a row to `desk/rundown.json`:
   - `status`: `live` (already on the public magazine), `draft` (assembled
     here, not the live homepage), or `tray` (empty slot).
7. Check it:

```bash
python3 scripts/cg_desk.py show <slug>
python -m unittest tests.test_cg_assembly_desk
```

8. Paste. Substack does not read this git folder — upload the PNGs/JPEGs
   yourself. Same for Skool.

If you do not have a story yet, leave it in **trays**. Empty is honest.

---

## The three outs (what “done” looks like)

**Magazine.** Feels like Issue 1: dark navy, gold type, honest labels,
pictures that teach. Reported is not certified. A pair of posters is a
pair. Do not ship a “closed” card without its open companion when those
are different statements.

**Substack.** Someone can paste into
[jonathansimonscrna.substack.com](https://jonathansimonscrna.substack.com)
without rewriting. Title. Dek. Body. Image list. Alt text. VAL, if any,
comes **after** the body.

**Skool.** Shorter. A hook a person will actually read in a group. The
pictures. Then: **ask in this thread.** No subscribe-to-unlock.

---

## VAL8000 — the little box, not the lead

Public name: **VAL8000**. Face on this desk: a red circular eye and a
mouth that is a line (a smile when the joke lands). Rare metal teeth stay
**off** the masthead. VAL comments **after** the news.

VAL is available on the entry. VAL is not the magazine. VAL is not Domain
Architect. VAL cannot certify a theorem.

If a VAL-in-a-box widget is being built elsewhere, do not overwrite it
from this folder. This desk only needs a place to drop the comment copy.

Weekend Update is an empty tray until you have one.

---

## Labels that stay loud

- **Reported ≠ certified.** Issue 1 stays *reported · not DA-certified*.
- **Unaugmented leftover OPEN.** Classical unaugmented swirl is not closed.
  **DA-VC-01** remains **FAIL**.
- **Correspondence ≠ physical equivalence.** Sharing a role is not being
  the same object.
- **Letters collide.** Swirl \(\Phi = u_\theta/r\) is not Domain Architect
  output \(\Phi\) and not gravity \(\Phi_g\). Same tuxedo, different guest.
- **Paywall off.** The subscriber table in Frequency is a **plan**.
- **No patents from DA.** Historical archive is archive.

House line, already on the site: *for the record / not the last word.*

---

## What not to do

- Do not deploy over the live Vercel magazine as the only deliverable.
  This folder is the assembly workspace.
- Do not invent a second brand or a second physics engine.
- Do not turn Domain Architect into a public website.
- Do not glue Cosmo Evolution, Ask the Desk, or Frequency into one
  theorem. They are drawers. Keep the drawers.
- Do not fill trays with childhood autobiography or coincidence diaries.
- Do not stamp `TRANSFORMABLE` without a real morphism and witness.
- Do not claim the Riemann hypothesis is proved.
- The commentator is VAL8000. That is the public name.

---

## Cue cards already on the board

Seeded so the desk is not empty:

- **Issue 1 — Ten thousand agents** (live)
- **Open Progress** (live)
- **Teaching pictures — the periodic box and one shell** (draft, using
  diagrams that already exist)

Also on the rundown: For the Record (live inventory), Frequency 14 Sep
(draft working chapter), Ask the Desk (tray), Cosmo Evolution (tray),
VAL Weekend Update (tray), plus empty trays for later Frequency items,
Jon’s photos, and Jon’s stories.

One rundown. You add the next card.
