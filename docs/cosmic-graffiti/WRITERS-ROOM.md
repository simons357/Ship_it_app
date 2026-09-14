# Cosmic Graffiti writers’ room

Jon’s brief: a **group of writers producing content for the magazine**, like
the writers’ table at Saturday Night Live. Not a swarm. Not Skynet. Not
ten thousand agents each filming their own show.

The show is **Cosmic Graffiti**. The live lab stays Domain Architect.

## How SNL actually works (and why ours failed)

At SNL, a bunch of writers sit at **one table**. They pitch. The
showrunner picks. Each sketch gets a slot on **one rundown**. They rewrite
the same cue cards. They do not each rent a different studio.

What we did instead: each agent got a git branch and wrote a private
magazine. That is six writers disappearing into six basements. Funny
people, no show.

## The table

| SNL job | Cosmic Graffiti job | Who |
|---|---|---|
| Showrunner | picks the rundown, kills a sketch that fakes a theorem | Jon |
| Head writer | one coordinator; assigns slots; does not spawn a swarm | one agent |
| Weekend Update news | sourced headlines with dates and URLs | The Frequency |
| Weekend Update jokes | rap / one-liners **after** the news | VAL8000 |
| Sketch writers | Around us, Cosmo Evolution, Ask the Desk, Humor, Apps | named slots |
| Cue cards | the issue markdown everyone pastes into | `issues/YYYY-MM-DD-the-frequency.md` |
| Dress rehearsal | jokes must not close NS or RH | tests |

## Rules of the room

1. **One rundown.** `writers-room/RUNDOWN.md` is this week’s show. If it
   is not on the rundown, it is not in the magazine.
2. **One cue-card file.** Writers paste into the issue. They do not open
   a new branch “to be helpful.”
3. **News before jokes.** Frequency prints. VAL8000 comments. Same order
   as Weekend Update: the story, then the laugh.
4. **Kill the close.** If a sketch claims unaugmented Navier–Stokes is
   solved, or RH is proved, or Cosmo Evolution glued primes to ringdown,
   it is cut at the table. Humor is allowed. Lying is not.
5. **Terminator / Skynet:** punchlines. VAL8000 may say “I’ll be back —
   after the footnote.” He does not launch anything.
6. **Audio mouth:** ElevenLabs clone only. Stock voices are not VAL8000.
7. **Panel mouth:** line by default; smile for jokes; metal teeth rare,
   never the masthead.

## Commands

```
python3 scripts/cg_newsroom.py table
python3 scripts/cg_newsroom.py status
```

`table` prints the rundown like a cue sheet. Tonight’s packet:

- [`writers-room/RUNDOWN.md`](writers-room/RUNDOWN.md)
- [`writers-room/cold-open.md`](writers-room/cold-open.md)
- [`writers-room/weekend-update.md`](writers-room/weekend-update.md)

Paste Weekend Update under Frequency items. Paste the cold open at the
top of Humor, or as a cold open before Masthead if Jon wants a cold open.

When Jon says “writers’ room,” fill **empty slots on this rundown**. Then
stop. That is a comedy staff. That is not a network of private magazines.
