# VR Surgeon / AI Surgeon — story locator

**Date:** 2026-08-28  
**Branch audited:** `cursor/tao-snd-h-panel-a0eb` (+ all remote branches, full git history)  
**Question:** Where is Jonathan Simons' **AI Surgeon story about his son**, written like a movie script / storyboard?

---

## Executive answer

| Target | Found on this branch? | Found anywhere in git? |
| --- | --- | --- |
| **Son-specific movie script / storyboard** | **No** | **No** — zero matches for `my son`, `his son`, `father`, `son` + surgeon narrative |
| **AI Surgeon VR animation / trailer script** (scene-by-scene, generic “young player”) | **No** (not on this branch) | **Yes** — see [Partial match](#partial-match-ai-surgeon-vr-animation-script-not-the-son-story) |
| **VR Surgeon Unreal production pipeline** (awaiting storyboard) | **Yes** | **Yes** — `docs/products/VR-SURGEON-UNREAL-PIPELINE.md` |
| **Clinical / Vigilant products** | Partial refs only | Anesthesia package on other branches; not the son story |

**Bottom line:** The **personal father–son movie script** is **not in this repository**. The closest in-repo artifact is a **LinkedIn Surgeon X / ProVR pitch trailer script** that uses a generic “young player” — not Jonathan’s son by name or as autobiography.

---

## 1. Son story — NOT FOUND

### Search performed

- Grep (case-insensitive): `surgeon`, `VR surgeon`, `AI surgeon`, `son`, `storyboard`, `screenplay`, `movie script`, `my son`, `his son`, `father`, `ProVR`, `Surgeon X`, `HoloBase`
- Glob: `*surgeon*`, `*screenplay*`, `*storyboard*`, `*story*`, `*vr*`
- Directories: `docs/products/`, `docs/`, `docs/papers/zenodo-spectral/`, `KEEP-CUT-INVENTORY.md`
- Git: `git log --all -S"son" -S"storyboard" -S"AI Surgeon"`, branch file trees, `git grep` across all commits
- Branches: all `origin/cursor/*`, `origin/gh-pages`, `origin/main`
- VM paths: `/home/ubuntu/Desktop`, `~/Desktop` — **empty / not mounted**
- Cloud agent transcripts — no son + surgeon story reference

### Likely external homes (user must upload or paste path)

| Location | Why |
| --- | --- |
| **User Desktop / local PC** | Prior agent notes: “whole computer/Drive not in VM” |
| **Google Drive** | Same pattern as `NS_FINAL_MERGED_UNCONDITIONAL.tex`, lecture decks, sim scenarios |
| **LinkedIn — Surgeon X project** | Animation script cites this as **Source** (Jul 2026) |
| **ProVR / Simons Medical Innovations notes** | Patent-pending haptics; paired with AI Surgeon VR in inventory |
| **Text-to-video / animation tool exports** | Script was written *for* paste into those tools |

**To bring it here:** Upload PDF, markdown, Figma link, or images to:

```text
docs/products/vr-surgeon-storyboard/
```

or paste the file into a Cloud Agent message and ask to save as `docs/products/vr-surgeon/SON-STORY-SCREENPLAY.md`.

---

## 2. Partial match — AI Surgeon VR animation script (NOT the son story)

This **is** written like a short movie / storyboard (scenes, VO, SFX, shot list). It **is not** the son autobiography; log line uses **“A young player”** with no family relationship.

### Paths (other branches only — **not on `cursor/tao-snd-h-panel-a0eb`**)

| Path | Branches |
| --- | --- |
| `partner-packet/AI-SURGEON-VR-animation-script.md` | `origin/cursor/intro-portfolio-e279`, `work-showcase-b71c`, `prime-field-portfolio-561a` |
| `docs/anesthesia/AI-SURGEON-VR-animation-script.md` | `origin/cursor/abandon-early-apps-599f`, `david-intro-onepagers-599f`, `snd-gnc-bridge-rigor-memo-b71c` |

### Git provenance

- **Commit:** `dc9c41f` — *Add AI Surgeon VR animation trailer script for text-to-video tools* (2026-07-14)
- **Message:** “Built from the LinkedIn Surgeon X / ProVR pitch; playable build URL still blank.”
- **Follow-up:** `1e365b3` — optional “I AM” God-reference close on Scene 6

### Excerpt (log line + Scene 1)

```markdown
## LOG LINE

A young player boots into a VR operating theater. An AI Attending coaches in real time.
Haptic tools bite like metal. Team surgery turns practice into a tournament.
Gaming skill becomes medical readiness.

### SCENE 1 — BLACK → BOOT
**Visual:** Black screen. Heart-monitor beep once. VR headset lights ignite. HUD boots: `AI SURGEON VR`.
**VO (calm, confident):** The OR used to be somewhere you only watched.
```

### How to retrieve on your machine

```bash
git show origin/cursor/intro-portfolio-e279:partner-packet/AI-SURGEON-VR-animation-script.md
```

Or merge/copy onto current branch:

```bash
git checkout origin/cursor/intro-portfolio-e279 -- partner-packet/AI-SURGEON-VR-animation-script.md
# or anesthesia copy:
git checkout origin/cursor/abandon-early-apps-599f -- docs/anesthesia/AI-SURGEON-VR-animation-script.md
```

---

## 3. Related in-repo docs (NOT the narrative)

| File | What it is |
| --- | --- |
| `docs/products/VR-SURGEON-UNREAL-PIPELINE.md` | Unreal Engine production plan; **asks for storyboard upload**; no narrative content |
| `docs/products/MODULAR-PLATFORM-LEGO.md` | “VR Surgeon — no storyboard in repo” |
| `docs/KEEP-CUT-INVENTORY.md` | “ProVR / AI Surgeon VR / games — Long-cycle; hobby or partner only” |
| `docs/products/SEARCH-ENGINE-INTEGRATION-REPORT.md` | Patent filings: HoloBase, ProVR — NDA partition; Vigilant clinical lane |
| `packages/shared_core/product_registry.json` | No `vr-surgeon` product entry; `cosmos` URL unknown |

### zenodo-spectral

No surgeon, VR, son, or screenplay content in the 14-record mirror.

### gh-pages

No surgeon / storyboard files. Hosts Base44 app bundles (explorer, field-lock, maritime, solenne, nav-42) — not VR Surgeon narrative.

### Base44 / primefield / cosmos

| Surface | VR Surgeon / son story? |
| --- | --- |
| `primefield.tech/games` | Hub named in inventory; **no script in git** |
| Base44 apps (SFE-RH, ExoRatio, Solenne, Maritime) | Unrelated |
| **Cosmos app** | **Zero matches** in repo and history — URL/repo needed from Jonathan |

---

## 4. Distinguishing three different “VR Surgeon” artifacts

| Artifact | Format | Son story? | On `tao-snd-h-panel-a0eb`? |
| --- | --- | --- | --- |
| **Son movie script / storyboard** (sought) | Screenplay / panels | **Expected yes** — **not found** | No |
| **AI-SURGEON-VR-animation-script.md** | 6-scene trailer + shot list | No — generic young player | No (other branches) |
| **VR-SURGEON-UNREAL-PIPELINE.md** | Engineering / UE5 pipeline | No — meta-doc | Yes |
| **Vigilant Patch / anesthesia package** | Clinical briefs | No | No (other branches: `docs/anesthesia/`) |

---

## 5. References that mention AI Surgeon (inventory only)

From `partner-packet/INVENTORY.md` (portfolio branches):

- Games in production: strategy title, Pac-Man retro-3D, **AI Surgeon VR**
- Hub: https://primefield.tech/games
- Animation script path: `partner-packet/AI-SURGEON-VR-animation-script.md`
- **ProVR Tools** — patent-pending haptic Bluetooth training instruments

From `partner-packet/ADDRESSES.md` (group **J. Games**):

```markdown
| AI Surgeon VR | Animation script: partner-packet/AI-SURGEON-VR-animation-script.md · playable: _______________ |
```

Playable build URL was **blank** as of 2026-07.

---

## 6. Recommended next steps for Jonathan

1. **Search local machine / Drive** for: `surgeon`, `ProVR`, `Surgeon X`, `storyboard`, `screenplay`, son’s name if used in filename.
2. **Check LinkedIn Surgeon X** project media and attachments — cited as animation script source.
3. **Upload** any found file to `docs/products/vr-surgeon-storyboard/` or attach to a Cloud Agent run.
4. **Optional:** Cherry-pick `AI-SURGEON-VR-animation-script.md` onto this branch if the trailer script (not son story) is enough for Unreal pipeline work.
5. **Reply with:** “This is the son story” vs “This is the trailer only” so agents do not merge the two.

---

## 7. Audit commands (reproducible)

```bash
# Current branch
rg -i 'surgeon|storyboard|screenplay|my son|his son' docs/

# All branches — surgeon files
for b in $(git branch -r); do
  git ls-tree -r --name-only "$b" 2>/dev/null | rg -i 'surgeon|storyboard|screenplay' && echo "  ^ $b"
done

# Animation script from portfolio branch
git show origin/cursor/intro-portfolio-e279:partner-packet/AI-SURGEON-VR-animation-script.md | head -40
```

---

*Locator maintained for PFPI / modular platform work. Update when son story or storyboard lands in repo.*
