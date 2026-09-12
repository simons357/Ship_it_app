# Warrior Surgeon — what the novel locked, and what it did not

Desk map of the 28 Aug 2026 Warrior Surgeon Word drops. Independent of ChatVault, Domain Architect, RH, and NS. **Not a medical-device claim.**

Both uploads are the **same file** (`md5 08bca7fbdf5ed9f27da7bdf13e80ddc3`). They were not two drafts. Split by **voice**, not by filename:

| File | Voice |
|---|---|
| [`warrior-surgeon/Warrior_Surgeon.docx`](warrior-surgeon/Warrior_Surgeon.docx) | Canonical copy of the identical blob |
| [`warrior-surgeon/Warrior-Surgeon.extracted.txt`](warrior-surgeon/Warrior-Surgeon.extracted.txt) | Full extracted text |
| [`THEIRS-medical-big-picture.md`](THEIRS-medical-big-picture.md) | ACC / trauma / assistant / look-then-cut |
| [`HARRISONS-arthurian-lady-of-the-lake.md`](HARRISONS-arthurian-lady-of-the-lake.md) | Oracle, Lake, songs, “Become the warrior” |
| [`warrior-surgeon/MANIFEST.txt`](warrior-surgeon/MANIFEST.txt) | Hashes and split rule |

## What Warrior Surgeon locked (docs only)

- **Title tension:** the novel is *Warrior Surgeon*; Solomon says there is no Warrior, only the Surgeon. The shipped game title stays **AI Surgeon**.
- **Military frame:** Air Combat Command surgical unit; fighter-pilot blank slate; soldier patients; a tent that does not pause for a briefing.
- **Identify before you cut:** examine, then irrigate or reduce, then cut. Transparent anatomy is a later-floor gift, not a skip.
- **Seats:** an assistant on every early case (fetch, hold, watch). Not a metaverse. Not two products.
- **Trauma is the hard clock:** live deterioration, death on the table as a teaching rule.
- **Harrison’s voice is the Lady of the Lake** (mythic authority that gives the sword). Hub/about: **one** atmosphere beat. Not a fantasy reskin of the OR. Not grey textbook chrome.

## Conflicts with AI Surgeon final+cites / 2026 storyboard

Keep **both**. Do not collapse them.

| Topic | Warrior Surgeon (this drop) | AI Surgeon final+cites / 2026 desk |
|---|---|---|
| What the thing is | Sci-fi novel: Tower, harmonics, transmission, Giza-as-anchor | Civilian phone-first residency game; 2025 investor bible + August 2026 storyboard |
| Who the learner is | F-22 pilot, blank slate, ACC | Anyone on a phone; clinical content by Jonathan Simons, CRNA |
| Module list | Floors 1023 / 1029; jungle suture; Roman trauma; Civil War amputation | Hub years: skills lab, finger I&D, **12 open appendectomy**, lap chole, hernia, anastomosis, **21 tube thoracostomy**, cric, DCL, CABG, craniotomy |
| Hardware | Tower sim, “Bluetoothed” body, metal key | Phone → tablet + mat → VR. Same codebase |
| Money | Denarii / whisky on the key; instruments cost | Schools / hospitals / STEM grants; **no checkout on the hub** |
| Warrior | Oracle: become the warrior. Solomon: there is no Warrior | Product name is AI Surgeon. Chronogate is the house |
| Seats | Surgeon + assistant (no anaesthesia seat in the early floors) | Surgeon / anaesthesia / scrub; playable HTML is still single-seat + AI attending |
| Citations | None. Fiction | Named 2025 sources in `CITATIONS.md` — do not treat this novel as one |

**Playable UI follows the HTML prototypes + `ai-surgeon-systems.js`.** Hub copy may reuse the overlapping ideas (trauma clock, identify-before-cut, seats) in the 2026 desk voice. It must not become an unplayable lore dump.

## HTML prototypes vs this novel

The 28 Aug HTML drops (`ai-surgeon-prototype_f349.html`, `ai-surgeon-module02-trauma_c2d0.html`) are **not richer** than the sibling tree already on this branch:

- Upload prototype: CDN `three.js`, no hub back-link, no local `vendor/three.min.js`.
- Upload trauma: no `ai-surgeon-systems.js`, no `trauma_physiology.js`, no ask-the-attending, no handover, no profiles. Finish copy still pretends “Module 03 damage-control laparotomy is unlocked.”
- Repo modules: local three.js, shared `AISS` engine, live physiology extracted for tests, residency hub links, Chronogate chrome.

**The repo HTML won.** Physiology numbers from the upload (needle decays, tube holds, arrest window) already live in `trauma_physiology.js`. Do not paste the upload over the sibling modules.

## What stayed stub

Unchanged pitch cards: skills lab 00.1–00.5, finger I&D, lap chole, inguinal hernia, bowel anastomosis, cricothyroidotomy, damage-control laparotomy, CABG, craniotomy, anaesthesia track, tablet+mat, playable Surgery Verse seats, real Teach One (supervise a junior). Jungle suture / Roman cellar / Civil War tent are **not** hub modules and must not be faked as playable links.

Teach One in HTML is still the multiple-choice placeholder. Field-demo MP4 is still missing. Anatomy in the 3D modules is still placeholder geometry.
