# VR Surgeon — Unreal Engine Production Pipeline

**Date:** 2026-08-28  
**Branch:** `cursor/tao-snd-h-panel-a0eb`  
**Repo:** `simons357/Ship_it_app`  
**Related:** [`MODULAR-PLATFORM-LEGO.md`](MODULAR-PLATFORM-LEGO.md), [`../KEEP-CUT-INVENTORY.md`](../KEEP-CUT-INVENTORY.md)

---

## Executive answer (the three questions)

| # | Question | Answer | Why |
| --- | --- | --- | --- |
| 1 | If you provide dirty details + a precise storyboard for **VR Surgeon**, can we help describe everything? | **Yes** | Cursor/Cloud Agents excel at structured narrative → design doc, GDD, technical spec, shot list, UX flows, clinical-accuracy notes, and regulatory *positioning* (training sim vs medical device). |
| 2 | Can we feed that knowledge to Unreal Engine and write its code? | **Yes, with limits** | We can produce Unreal-ready C++ stubs, Blueprint logic specs, DataAsset schemas, Python editor utilities, and integration notes. We **cannot** click inside Unreal Editor, compile against your local engine, package builds, or test on a VR headset from this environment. |
| 3 | Can we get maximum workers on it? | **Yes** | Parallel Cloud Agent tracks + a single source-of-truth handoff format (JSON/YAML in-repo) let narrative, systems, UI, level, audio, QA, and docs run concurrently once Discovery inputs land. |

**What to send first:** A **beat sheet + storyboard frames** (even rough), **one fully specified VR interaction** (smallest teachable moment), and **platform/comfort constraints** (Quest 3 vs PCVR, locomotion, seated/standing). See [Input checklist](#6-input-checklist--what-you-must-pasteupload) below.

---

## 0. Scope and honesty boundary

**VR Surgeon** in this pipeline is framed as a **clinical training / procedural rehearsal simulation** — not a cleared medical device.

- **CRNA / clinical background** informs accuracy of workflow, terminology, timing, and haptic/audio cues.
- **We do not claim FDA clearance, CE marking, or diagnostic/therapeutic efficacy** unless you are running a formal regulatory program with counsel and we are explicitly scoped to *documentation support* for that path.
- Language in all outputs uses: *“for training and education only,” “not for clinical decision-making,” “not a substitute for supervised clinical practice.”*
- If the product later targets **SaMD / FDA 510(k) / De Novo**, that becomes a separate workstream (design controls, V&V, cybersecurity, human factors) — we can scaffold doc templates, not substitute for QMS and regulatory counsel.

---

## 1. What we CAN do from Cursor / Cloud Agent

### 1.1 Storyboard → structured design artifacts

| Output | Description | Typical path in repo |
| --- | --- | --- |
| **Design doc / GDD** | Vision, pillars, player roles, session length, success metrics | `docs/products/vr-surgeon/GDD.md` |
| **Technical spec** | Subsystems, performance budgets, networking model, save/load | `docs/products/vr-surgeon/TECH-SPEC.md` |
| **Shot list / beat sheet** | Frame-by-frame intent, camera/POV, emotional beat, learning objective | `docs/products/vr-surgeon/SHOT-LIST.yaml` |
| **UX flows** | Onboarding, pause/comfort, failure/recovery, instructor mode | `docs/products/vr-surgeon/UX-FLOWS.md` |
| **Interaction specs** | Grab, pinch, two-hand tools, sterile field rules, collision priorities | `docs/products/vr-surgeon/interactions/*.yaml` |

**Input quality rule:** “Dirty details” are welcome — we normalize them into structured YAML/Markdown. “Precise storyboard” means each frame has: **POV, user action, system response, audio/haptic cue, fail states.**

### 1.2 Unreal-ready artifacts (no Editor required)

| Artifact | Format | Consumption |
| --- | --- | --- |
| **C++ class stubs** | `.h` / `.cpp` with UCLASS/USTRUCT, component layout, interfaces | Paste into UE project `Source/`; user compiles locally |
| **Blueprint logic pseudocode** | Structured YAML: events, branches, timelines, RPCs | Human or Codex implements in Editor |
| **UML / architecture diagrams** | Mermaid in docs | Onboarding for engineers |
| **DataAsset schemas** | `UDataAsset` field lists + example JSON | Create assets in Editor or via Python |
| **Level design notes** | Blockout dimensions, sightlines, interactable spawn tables | Greybox in Editor |
| **Enhanced Input mapping** | Action/axis map tables | Project Settings → Input |
| **Gameplay Ability System outlines** | If scope warrants GAS | Optional Phase 3+ |

Example stub pattern we emit:

```cpp
// AVRSurgeonToolActor.h — generated stub; compile in your UE5 project
UCLASS()
class VRSURGEON_API AVRSurgeonToolActor : public AActor
{
    GENERATED_BODY()
public:
    UPROPERTY(EditDefaultsOnly, Category = "VR Surgeon")
    TObjectPtr<UStaticMeshComponent> Mesh;

    UFUNCTION(BlueprintCallable, Category = "VR Surgeon")
    void OnGrabbed(AActor* Hand);

    UFUNCTION(BlueprintCallable, Category = "VR Surgeon")
    void OnReleased();
};
```

Example Blueprint spec fragment (`interactions/scalpel_pickup.yaml`):

```yaml
blueprint: BP_ScalpelPickup
parent: AInteractableTool
events:
  - name: OnGrabbed
    conditions:
      - hand.Sterile == true
    then:
      - attach_to: hand.Socket_Grip
      - play_haptic: { hand: grabbing, intensity: 0.4 }
      - play_sound: SFX_Scalpel_Lift
    else:
      - show_toast: "Non-sterile contact — restart sterile field"
      - log_telemetry: { event: sterile_violation }
```

### 1.3 Python / editor utility scripts (when `.uproject` exists)

Once you connect a UE5 project repo (or submodule), we can author:

| Script type | Unreal Python API use |
| --- | --- |
| Batch asset creation | `unreal.EditorAssetLibrary`, `AssetToolsHelpers` |
| Level blockout helpers | Spawn static meshes from CSV spawn tables |
| DataAsset population | Fill `UProcedureStepData` rows from YAML |
| Validation | Check naming conventions, missing refs, LOD counts |
| CI hooks | Export cooked maps list, generate manifest |

**Requirement:** User runs scripts inside Unreal Editor (*Tools → Execute Python Script*) or via `-ExecutePythonScript=` commandlet on a machine with UE installed.

### 1.4 Audio, haptics, UI copy, clinical accuracy layer

| Track | Deliverables |
| --- | --- |
| **Audio** | SFX list, VO script, mix priorities, occlusion rules for OR ambience |
| **Haptics** | Per-interaction amplitude/duration tables (Quest Touch Pro, Index, etc.) |
| **UI copy** | Diegetic monitors, checklist UI, error strings — plain language, no diagnostic claims |
| **Clinical accuracy** | Step order, timeout windows, contraindication *training scenarios* (labeled fictional/composite cases) |
| **Disclaimers** | Splash, settings panel, store listing boilerplate |

---

## 2. What we CANNOT do without your UE5 install / project

| Capability | Blocker | Workaround |
| --- | --- | --- |
| Open Unreal Editor | No GUI UE in Cloud Agent VM | You open project locally; we push git changes |
| Compile C++ / hot reload | No UE toolchain in cloud | GitHub Actions *can* be scaffolded; still needs your engine version pin |
| Author Blueprint graphs visually | Editor-only | We ship YAML pseudocode + node-by-node build instructions |
| Place lighting, bake, Nanite tuning | Editor + GPU | Spec + screenshot review loop |
| Package APK (Quest) / PCVR build | Platform SDK + signing certs | We write packaging checklist + `DefaultEngine.ini` snippets |
| VR headset testing | No physical HMD | You run play-in-VR; paste logs/video; we iterate |
| Live PlayFab / Oculus Platform entitlement | Your dev accounts | We stub interfaces + mock in PIE |

**Honest ceiling:** We can get you to **“open project, compile, implement Blueprints from spec, press Play in VR”** — not to **shipped store build** without your machine and accounts.

---

## 3. Unreal vs Unity (when relevant)

| Factor | Unreal Engine 5 | Unity |
| --- | --- | --- |
| **Visual fidelity / OR lighting** | Strong (Lumen, Nanite) | Good with URP/HDRP; more manual |
| **Quest native** | UE5 + Meta XR plugin | Unity + Meta XR SDK — mature |
| **C++ + designer Blueprints** | Native split we exploit | C# + visual scripting |
| **This pipeline default** | **UE5** — user asked explicitly | Note only; switch costs ~30% rewrite of stubs |

**Recommendation:** Stay on **UE5** if the storyboard targets high-fidelity OR visuals, PCVR + Quest cross-play, or you already have UE experience. Consider Unity if the team is C#-only and scope is Quest-only arcade training.

**Codex / in-Editor AI:** Useful for translating our Blueprint YAML → actual nodes once you are in Editor. Cloud Agents remain **source-of-truth for specs**; Codex is **implementation accelerator on your desk**.

---

## 4. Connectors — repo, LFS, Perforce, CI

### 4.1 Git + Git LFS (recommended for indie/small team)

```text
vr-surgeon-ue/
├── VRSurgeon.uproject
├── Source/VRSurgeon/          ← our C++ stubs land here
├── Content/                   ← LFS-tracked .uasset, .umap, .fbx, .wav
├── Config/                    ← DefaultEngine.ini, input, XR settings
├── Docs/                      ← symlink or submodule to Ship_it_app docs
├── Pipeline/
│   ├── handoff/               ← JSON/YAML SSOT (see §5)
│   ├── python/                ← editor scripts
│   └── ci/                    ← optional BuildGraph / Gauntlet
└── .gitattributes             ← LFS rules
```

**.gitattributes essentials:**

```gitattributes
*.uasset filter=lfs diff=lfs merge=lfs -text
*.umap filter=lfs diff=lfs merge=lfs -text
*.fbx filter=lfs diff=lfs merge=lfs -text
*.wav filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
```

### 4.2 Perforce (recommended for AAA-style binary churn)

If art team exceeds ~5 GB/week of binary commits, use **P4** for `Content/` and **git** for `Source/` + docs — or Helix Core Unreal integration. Cloud Agents commit to **git side**; artists submit to P4; build machine syncs both.

### 4.3 Linking this planning repo

Keep **planning SSOT** in `Ship_it_app/docs/products/vr-surgeon/` until `.uproject` exists, then either:

1. **Submodule** planning repo into UE project `Docs/planning/`, or  
2. **Monorepo** move when scaffold phase starts.

---

## 5. Maximum workers strategy

### 5.1 Parallel tracks (7 agents typical)

| Track ID | Owner focus | Inputs needed | Outputs |
| --- | --- | --- | --- |
| `T1-narrative` | Story, beats, VO, learning objectives | Storyboard, beat sheet | GDD, shot list |
| `T2-gameplay-systems` | Tools, procedures, scoring, failure | Interaction specs | C++ stubs, BP YAML, DataAssets |
| `T3-ui-ux` | Menus, comfort, diegetic UI | UX flows, platform | Widget specs, copy deck |
| `T4-level-blockout` | OR layout, spawn tables, metrics | Art style, procedure list | Blockout dims, level YAML |
| `T5-audio-haptics` | SFX, VO, haptic tables | Shot list timings | Audio manifest, haptic CSV |
| `T6-qa-matrix` | Test cases, comfort, accessibility | All tracks | TEST-MATRIX.yaml |
| `T7-docs-compliance` | Disclaimers, glossary, instructor guide | GDD + clinical notes | COMPLIANCE.md, glossary |

### 5.2 Cursor multitask + Cloud Agents

```text
┌─────────────────────────────────────────────────────────────┐
│  HANDOFF SSOT: pipeline/handoff/vr-surgeon-state.yaml       │
│  (version, phase, track status, file pointers, blockers)    │
└───────────────────────────┬─────────────────────────────────┘
                            │
     ┌──────────────────────┼──────────────────────┐
     ▼                      ▼                      ▼
 Cloud Agent A          Cloud Agent B          Cloud Agent C
 T1 narrative           T2 gameplay            T3 UI/UX
     │                      │                      │
     └──────────────────────┼──────────────────────┘
                            ▼
                   You (Integrator): review merge conflicts
                            ▼
                   UE project repo (when connected)
```

**Rules for parallel work:**

1. **One SSOT file** — agents read/write named sections only (`T2-gameplay-systems`, not free-form duplicates).
2. **File ownership map** — each track owns explicit paths; cross-track edits go through SSOT `requests[]` queue.
3. **Phase gates** — no `T4-level-blockout` dimension locks until `T1` beat for that room is `approved: true`.
4. **Integrator role (you or lead agent):** daily merge, resolve terminology drift, update SSOT `version`.

### 5.3 Handoff format — `vr-surgeon-state.yaml`

```yaml
version: 3
phase: spec  # discovery | spec | scaffold | vertical_slice | polish
project:
  name: VR Surgeon
  engine: UE5.4
  platforms: [Quest3, PCVR_OpenXR]
  locomotion: teleport_smooth_hybrid
  comfort: { vignette: true, snap_turn: 15, seated: supported }

tracks:
  T1-narrative:
    status: in_progress
    owner: cloud-agent-narrative
    outputs:
      - docs/products/vr-surgeon/GDD.md
      - docs/products/vr-surgeon/SHOT-LIST.yaml
  T2-gameplay-systems:
    status: blocked
    blocker: "Waiting for interaction spec: scalpel_pickup"
    outputs: []

requests:
  - from: T2-gameplay-systems
    to: T1-narrative
    type: clarify
    message: "Beat 7 — is sterile gown already donned at scene start?"

glossary:
  sterile_field: "Defined volume around patient drape; violations trigger reset policy v2"
```

**Cross-worker contracts:**

| Contract file | Producer | Consumer |
| --- | --- | --- |
| `SHOT-LIST.yaml` | T1 | T4, T5, T6 |
| `interactions/*.yaml` | T1 + T2 | T2 implementation, T6 tests |
| `DATA-ASSETS.schema.json` | T2 | T2 Python scripts, Editor |
| `LEVEL-SPAWN-TABLE.csv` | T4 | T4 scripts, T6 |
| `UI-COPY.deck.yaml` | T3 | T3 widgets, T7 compliance review |
| `TEST-MATRIX.yaml` | T6 | You, QA play sessions |

---

## 6. Input checklist — what you must paste/upload

### 6.1 Minimum viable kickoff (Day 0)

- [ ] **Beat sheet** — numbered story beats with learning objective per beat
- [ ] **Storyboard frames** — images or ASCII wireframes; per frame: POV, action, system response
- [ ] **One gold-standard interaction** — full detail (e.g., “pick up scalpel, check blade, place on tray”)
- [ ] **Target platform** — Quest 3 standalone, PCVR (Steam/OpenXR), or both
- [ ] **Locomotion + comfort** — teleport / smooth / hybrid; snap turn; seated mode?
- [ ] **Scope statement** — training sim vs gamified arcade; single procedure vs curriculum
- [ ] **Multiplayer?** — solo only, async ghost, instructor spectate, co-op (drives arch early)

### 6.2 Strongly recommended (Week 1)

- [ ] **Art style references** — photo refs, palette, realism level (clinical vs stylized)
- [ ] **Procedure selection** — e.g., “central line prep,” “intubation assist,” “regional block setup”
- [ ] **Audience** — med student, CRNA trainee, attending refresh; session length target
- [ ] **Existing assets repo** — Sketchfab, Megascans, prior UE/Unity project
- [ ] **Audio constraints** — VO talent budget, licensed music yes/no
- [ ] **Hardware targets** — Quest Touch Pro haptics? Index knuckles?

### 6.3 Clinical / legal (when applicable)

- [ ] **Composite vs real case** — confirm fictional patient narrative
- [ ] **Institution review** — IRB not required for pure fiction; note if real protocols copied
- [ ] **Intended use statement** — one paragraph you are comfortable signing
- [ ] **Regulatory intent** — education only vs exploring SaMD (changes T7 scope)

### 6.4 Paste template (copy into first message)

```markdown
## VR Surgeon — Kickoff Packet

**Platforms:** Quest 3 + PCVR
**Locomotion:** Teleport + smooth snap 15°
**Scope:** Single-procedure training sim, 15-min session
**Multiplayer:** Instructor spectate only

**Intended use (draft):** Education and procedural rehearsal for licensed clinicians in training.

**Beat sheet:**
1. ...
2. ...

**Gold interaction — Scalpel pickup:**
- Preconditions: ...
- Steps: ...
- Success: ...
- Fail states: ...

**Storyboard:** [attach images or describe frames 1–N]

**Art style:** Photoreal OR, cool white lighting, minimal gamification

**Existing assets:** [repo URL or "none"]
```

---

## 7. Production phases

### Phase 0 — Discovery (3–7 days wall time, parallelizable)

**Goal:** Shared vocabulary, one procedure chosen, comfort/platform locked.

| Exit criteria | Artifact |
| --- | --- |
| Beat sheet approved | `SHOT-LIST.yaml` v1 |
| Intended use + disclaimers drafted | `COMPLIANCE.md` v0 |
| SSOT initialized | `vr-surgeon-state.yaml` |
| Risk register | `RISKS.md` (motion sickness, scope creep, reg path) |

**Workers:** T1 + T7 primary; T3 for comfort defaults.

---

### Phase 1 — Spec (1–2 weeks, max parallel)

**Goal:** Buildable without opening UE — every interaction has YAML + acceptance test.

| Exit criteria | Artifact |
| --- | --- |
| GDD + tech spec signed off | `GDD.md`, `TECH-SPEC.md` |
| All MVP interactions specified | `interactions/*.yaml` |
| Data model frozen | `DATA-ASSETS.schema.json` |
| Test matrix for vertical slice | `TEST-MATRIX.yaml` |
| C++ module layout | `Source/` tree documented |

**Workers:** All 7 tracks active; integrator merges daily.

---

### Phase 2 — UE project scaffold (user machine + agents)

**Goal:** Empty project runs in VR with one greybox room and placeholder hands.

| Step | Who |
| --- | --- |
| Create UE5 C++ project from spec (OpenXR, Meta XR if Quest) | You |
| Copy C++ stubs from repo | You / CI |
| Run Python blockout script from spawn table | You in Editor |
| Wire Enhanced Input from spec | You |
| Push `.uproject` repo; grant Cloud Agents access | You |

| Exit criteria | Artifact |
| --- | --- |
| PIE VR works — locomotion + comfort | Video capture from you |
| One interactable from BP spec | `BP_ScalpelPickup` working |
| Git LFS or P4 flowing | Clean clone docs |

**Workers:** T2 + T4 lead; T6 begins smoke tests.

---

### Phase 3 — Vertical slice (one complete teachable moment)

**Goal:** One beat from storyboard is shippable-quality proof — not full game.

Scope example: *Enter OR → scrub check → pick up scalpel → sterile violation OR success → debrief UI.*

| Exit criteria | Artifact |
| --- | --- |
| Full beat playable on target HMD | Build hash recorded in SSOT |
| Audio/haptics for slice | Mixed in project |
| Telemetry events fire | JSON log sample |
| QA matrix rows for slice pass | Signed `TEST-MATRIX.yaml` |

**Workers:** All tracks; T5 critical path; T6 gates release.

---

### Phase 4 — Polish (+ production expansion)

**Goal:** Curriculum expansion, art pass, performance, localization, instructor mode.

| Workstream | Notes |
| --- | --- |
| Performance | Quest: 72/90 Hz budget doc; PCVR: super sampling optional |
| Content pipeline | More procedures = duplicate YAML pattern, not rewrite |
| Localization | UI copy deck structure supports i18n keys early |
| Store / deployment | Packaging runbook — **your** signing keys |
| Regulatory fork | If SaMD path opens, freeze feature scope; T7 expands V&V templates |

---

## 8. Suggested repo layout (planning phase, this repo)

Until UE project exists, we store planning under:

```text
docs/products/vr-surgeon/
├── GDD.md
├── TECH-SPEC.md
├── COMPLIANCE.md
├── SHOT-LIST.yaml
├── UX-FLOWS.md
├── TEST-MATRIX.yaml
├── RISKS.md
├── interactions/
│   └── scalpel_pickup.yaml
├── pipeline/
│   └── handoff/
│       └── vr-surgeon-state.yaml
├── schemas/
│   └── DATA-ASSETS.schema.json
├── ue-stubs/                  ← C++ headers/sources pre-UE
│   └── Source/VRSurgeon/
├── python/                    ← editor scripts (run locally)
│   └── blockout_from_csv.py
└── audio/
    └── SFX-MANIFEST.yaml
```

---

## 9. Integration with Ship It platform spine (optional)

If VR Surgeon later needs catalog presence alongside Field Lock, Ship It, etc.:

- Register in `packages/shared_core/product_registry.json`
- Canonical docs link via `link_resolver.py`
- Search index via PFPI when deployed

This is **optional** for UE production; useful for portfolio and investor narrative.

---

## 10. Quick reference — who does what

| Task | Cloud Agent | You (local UE) |
| --- | --- | --- |
| Write GDD from storyboard | ✅ | Review |
| C++ stubs | ✅ | Compile |
| Blueprint graphs | Spec only ✅ | Build in Editor |
| Python asset tools | ✅ | Execute in Editor |
| VR playtest | ❌ | ✅ |
| Quest APK sign | ❌ | ✅ |
| FDA submission | Templates only ✅ | Counsel + QMS ✅ |
| 7 parallel doc/spec tracks | ✅ | Integrate SSOT |

---

## 11. Next action

1. Paste the [kickoff template](#64-paste-template-copy-into-first-message) in a new Cloud Agent thread (or continue this one).
2. Attach storyboard images if available.
3. Name the **one procedure** for vertical slice.
4. We initialize `docs/products/vr-surgeon/` tree + SSOT and spin **T1–T3** immediately; **T2/T4** follow within 24h of gold interaction spec approval.

**Document path:** `docs/products/VR-SURGEON-UNREAL-PIPELINE.md` (this file)
