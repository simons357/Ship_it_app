# The House — Cosmic Graffiti as the front door

Jonathan Simons wants **one site** that does two jobs:

1. A **portfolio an investor can walk** — everything that is real, labeled.
2. A **fun, informative house** (science, music, art) that can later charge
   about **$99** for a studio door: cleaned apps, books/papers, conceptual
   ideas, patent-style archive.

This file is the architecture. It is not a live Stripe checkout.

Live lab remains **Domain Architect**
(`DECOMPOSE → CROSS-DOMAIN TRANSLATE → SYNTHESIZE`). Cosmic Graffiti is
the magazine. VAL8000 is Weekend Update. The house is the building.

## Three doors (not three companies)

| Door | Who | Price now | What they get |
|---|---|---|---|
| **Street** | anyone | free | The Frequency, wonder essays, humor, VAL8000, Ask the Desk. Science / music / art as *public* rooms. |
| **Table** | investor / partner | free walk | Honest catalog, Domain Architect (local demo), paper faces with OPEN/conditional labels, turbulence program, what is parked. |
| **Studio** | subscriber | **$99 plan** | Cleaned apps that actually run, books/papers packet, conceptual ideas, historical patent-style docs Jon chooses to share. **Not wired.** No paywall in this repo. |

Domain Architect does **not** file patents. A $99 packet of old
patent-style PDFs is an archive share, not “we patented the universe.”
Jon has said he is not suing. AquaQuarts, as of the 17 Aug 2026
portfolio read, had **no patent filed**. Do not sell a filing you do
not have.

## What “cleaned and running on the site” means this week

**Running now**

- Cosmic Graffiti HTML: [cosmic-graffiti-magazine.vercel.app](https://cosmic-graffiti-magazine.vercel.app/)
- This working magazine: `docs/cosmic-graffiti/`
- Domain Architect: local desktop, `python3 -m domain_architect app` → `http://127.0.0.1:8765/` (not a public website)

**Not running on this site this week**

- The 26 named software products from the August 2026 portfolio census.
  Many are Base44-gated, Replit kiosks, hollow shells, or abandoned.
  Putting all of them on one Vercel origin without cleaning is how the
  catalog got too wide.
- A charged $99 gate. Copy can name the door. Code must not fake the lock.

**Cleaning rule:** an app goes on the Street or in the Studio only if
(1) it runs, (2) it is labeled shipped / demo / archive, (3) it does not
get imported into `domain_architect/*.py` if it is NAV-42, Fluid-Q,
Chat Vault, 2.2 Hz, Q OS, or resonant paint.

The August 2026 independent read still holds: **too-wide catalog**. An
investor should see three fundable slots, not forty-seven names.
Recommended book then: AquaQuarts (first dollar, no FDA), Operator
Assist (founder-fit), one B2B demo (Field Lock *or* maritime). Math
papers are a **shelf**, not the cash engine.

## Dual use, without lying

**Investor walk.** Start at [`public/index.html`](public/index.html) →
Table. They see DA, the magazine, the paper faces, the OPEN leftovers,
the parked names. Credibility is the product.

**Public house.** Street door: Frequency, coffee-swirl physics, music
and art *as themselves* (not childhood coincidence diaries in git).
VAL8000 jokes. Writers’ room for the magazine.

**Studio later.** $99 unlocks a zip/packet Jon actually curates:
runnable demos, books, conceptual sketches, patent-style archive with
the retraction notes taped on. Until Stripe (or Skool, or Substack)
exists, the door is a sign. Do not charge air.

## Commands

```
python3 scripts/cg_house.py doors
python3 scripts/cg_house.py catalog
```

Catalog: [`CATALOG.md`](CATALOG.md), machine file [`catalog.json`](catalog.json).
