# Cosmic Graffiti newsroom

This is how agents staff the magazine **without pretending to be Skynet**.

Live lab stays Domain Architect. Cosmic Graffiti is the magazine. VAL8000
is the comment voice. He may joke about Terminators. He does not launch
them.

## Why “run your own network” failed

It failed for boring reasons, not mystical ones.

1. **Parallel git branches instead of desks.** Frequency, Ask the Desk,
   Cosmo Evolution, and VAL8000 were each sent to a new branch. They
   could not share a page. They stepped on `docs/cosmic-graffiti/`.
2. **No roster.** Nobody had a file that said who owns what. So everyone
   rewrote the masthead.
3. **“Ten thousand agents” was not us.** Issue 1 reported someone else’s
   Navier–Stokes swarm. That is not a Cosmic Graffiti staff, and it is
   not a close of unaugmented regularity.
4. **No audio mouth.** ElevenLabs never had a key in the agent environment,
   so VAL8000 never actually spoke. Stock TTS is not him. The **panel**
   mouth is separate: a straight line while idle, a smile after he
   answers, metal teeth only as a rare gag.
5. **No post loop.** Substack and Skool were not wired. Files landed in
   git and stopped.

A thousand agents on a thousand branches is not a network. It is a pile.

## How it actually runs

Named desks. One file each. Coordinator (a human, or one agent) assigns
the desk from [`desks.json`](desks.json).

```
The Frequency  →  news (date + URL)
VAL8000        →  rap comment after (jokes allowed)
Ask the Desk   →  reader Q&A
Cosmo Evolution→  sky / attempt / pulled back
Humor          →  VAL8000 can cover this
```

Commands:

```
python3 scripts/cg_newsroom.py status
python3 scripts/cg_newsroom.py why
```

`status` tells you which desk files exist **in this checkout**. Missing
is allowed — those desks live on sibling branches until someone merges
them. Do not invent a second magazine to fill a hole.

## Rules for agents

- Do not checkout another desk’s branch to “help.”
- Do not spawn a swarm because the copy said “network.”
- Do not overwrite Frequency items with rap.
- Do not put Cosmo Evolution inside Domain Architect.
- Do not call Mac `say` VAL8000.
- Terminator / Skynet: jokes. Not a product claim.

When Jon says “run the desk tonight,” one agent reads this file, fills
the empty trays, and stops. That is the network.

The comedy version of the same table — SNL-style writers, one rundown,
Weekend Update = VAL8000 — is [`WRITERS-ROOM.md`](WRITERS-ROOM.md).
`python3 scripts/cg_newsroom.py table`
