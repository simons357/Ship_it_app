# VR Surgeon — Unreal Engine Pipeline (stub)

**Date:** 2026-08-28  
**Status:** Awaiting storyboard / script upload  
**Branch:** `cursor/tao-snd-h-panel-a0eb`

---

## Purpose

This document is a placeholder for translating a VR Surgeon storyboard into Unreal Engine C++ / Blueprint stubs. No storyboard file was found in the repository at audit time.

---

## What to upload

Provide one or more of:

| Asset | Format | Use |
| --- | --- | --- |
| Storyboard | PDF, Figma link, or `docs/products/vr-surgeon-storyboard/` | Scene flow, camera beats, UI panels |
| Shot list | Markdown or spreadsheet | Level sequence names, durations |
| Interaction script | Markdown | Grab, cut, suture, feedback loops |
| Reference meshes | `.fbx` / Unreal project zip | Anatomy proxy, tool meshes |

Drop files under `docs/products/vr-surgeon/` or link a Figma / Drive URL in an issue.

---

## Planned code output (after upload)

When a storyboard exists, the agent will generate:

```text
unreal/vr-surgeon/
├── README.md
├── Source/VrSurgeon/
│   ├── VrSurgeonGameMode.h/.cpp
│   ├── VrSurgeonPawn.h/.cpp
│   └── Procedures/          # one class per storyboard beat
└── Content/Blueprints/      # BP stubs matching shot list
```

Each storyboard panel maps to:

1. **Level sequence** or sub-level name  
2. **Blueprint** event graph stub (BeginPlay → step N)  
3. **C++** hook if performance-critical (tool collision, haptics)

---

## Integration with platform spine

VR Surgeon is a **clinical skin** (see `MODULAR-PLATFORM-LEGO.md`). When built:

- Product entry in `packages/shared_core/product_registry.json`  
- PFPI partition: `clinical` (separate from public Zenodo index)  
- Telemetry: procedure step events via spine module (Phase 3)

---

## Next step

**Upload the VR Surgeon storyboard** (PDF, images, or markdown shot list). Reply with the path or URL and ask to "translate storyboard to Unreal stubs."

Until then, no C++/Blueprint code is generated — there is no source material to translate.

---

*Related: `MODULAR-PLATFORM-LEGO.md`, `SEARCH-ENGINE-INTEGRATION-REPORT.md` (clinical partition § Vigilant)*
