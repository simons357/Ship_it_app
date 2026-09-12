# Engine team — budget cartoon, not a wasted Unreal bill

**Question:** write the storyboard as code, feed Unreal or similar, Japanese Speed Racer look, then stand up a team for a real game engine? Add skills: sword? kung fu? tai chi as actual exercise while you fake-fight?

**Answer:** yes to the pipeline. No to buying Unreal first. The same JSON is the contract.

| Layer | What | Cost |
|---|---|---|
| **Storyboard JSON** | `engine/storyboard.json` — 12 manga beats + dojo skills | Already written |
| **Play now** | `dojo.html` — Speed Racer cel (leopard / tai chi / broom-ribbon-sand / bow-then-palms), camera optional | This repo, port 8770 |
| **Budget team engine** | Godot 4 project in `engine/godot/` — free, the JSON loads as data | Hire 1–2 Godot people when you want |
| **Later studio** | Unreal 5 imports the **same** JSON as a DataTable | Only when there is a real art/animation bill |

Do not rebuild the plot in Unreal, then again in Godot, then again on the web. That is waste.

## Why Godot first

Unreal is the right hammer for a funded cinematic. This is a **budget cartoon** for a daughter who loves Japanese things, plus a son, plus exercise. Godot is free. Cel look is cheaper than nanite flesh. Japanese pilots fly F-35s; Jun’s sky cadet is already in the story — we do not need a $500M jet sim to respect that.

When a studio exists, they do not invent a new plot. They read `storyboard.json`.

## What the dojo is

Solomon: there is no Warrior. Just the Surgeon.  
Kirana: 武は守り — fight *for* life.

So the combat chapter is **exercise pretending to be a fight**:

- **Leopard stance** — hold still. Squeeze the ground. That is legs and breath.
- **Tai chi wave** — eight slow counts. Fast movement is a miss (camera frame-diff, or honest keyboard holds if the camera is off).
- **What is around you** — broom, crimson ribbon, sand, empty hands. No toy-samurai mall sword.
- **Three exchanges** — bow, one palm (click), bow. Cartoon. Nobody is wasted.

Hand language is the **same Pen**: twist / click / squeeze. Apple Pencil on iPad until the custom pen exists. Body on the phone camera is the cheap motion path.

This is not David Carradine’s show and not that trademark. It is bare-hand, surroundings, old wandering-hero pictures. Kung fu (leopard, tai chi) in a Japanese cel frame is a student learning, not a joke about a people.

## Team (when you hire)

1. **Storyboard owner** — this JSON + the manga. Does not rewrite Solomon.
2. **Godot gameplay** — loads JSON, plays the four dojo skills (`engine/godot/scripts/Dojo.gd`). Does not re-author the twelve chapters.
3. **Cel art** — Speed Racer limited palette. No photoreal organs in the cartoon.
4. **Move coach (optional)** — real tai chi / karate teacher to check the eight counts are not harmful. Not a medical device. Not PT.

Do not hire an Unreal environment artist before the dojo loop is fun on a phone.

## Run

```bash
python3 -m ai_surgeon
# cartoon dojo:  http://127.0.0.1:8770/dojo.html
# storyboard:    http://127.0.0.1:8770/engine/storyboard.json
# manga:         http://127.0.0.1:8770/manga/
```

Godot: open `engine/godot/project.godot` in Godot 4.x (not installed on this VM). Unreal import notes: `engine/unreal/README.md`.

Not a medical device. Not ChatVault. Not Domain Architect.
