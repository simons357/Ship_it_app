# QStack Reference — unique product source

**Almost-production #1.** Date seen: **19 November 2026**.

| Field | Value |
| --- | --- |
| Live URL | https://qstack-spectral-flow.base44.app |
| Base44 app | QStack Reference `6a19046b717521480f6b9543` |
| Slug | `qstack-spectral-flow` |
| Created | 2026-05-29 |
| Last deployed | **2026-05-30** |
| App stage | ready |
| Visibility | public_with_login (custom auth enrolled) |
| Branch | `main` only |
| Editor GitHub | `base44dev/qstack-spectral-flow` (clone 404 from this VM) |

## Why this one is “almost production”

This is the only **published** QStack with a real product UI: operator dashboard (Q1–Q6 / Q-N tabs), 3D structure explorer, math gallery, and an ΩStack (`/rh`) tab. It is not the thin `primefield.tech/qstack` or gh-pages company-hub shell, and it is not the April 2026 Replit paper.

Live GET on 19 Nov 2026 returned HTTP 200, title `QStack Reference`.

## What was copied

Unique product files only, via Base44 `read_file` / sandbox export — **not** a minified SPA dump:

- `src/App.jsx` — routes `/`, `/rh`, `/gallery`, `/explorer`
- `src/pages/` — `QStackDashboard`, `OmegaStackDashboard`, `MathGallery`, `StructureExplorer`, plus unrouted `NSViewer`
- `src/components/qstack/`, `explorer/`, `gallery/`, `rh/`, `ns/`, `shared/`
- `base44/entities/Collection.jsonc`
- `package.json` (platform Vite app; not runnable as a standalone tree)

Auth/shadcn boilerplate (`Login`, `Register`, `MFA`, `ForgotPassword`, `ResetPassword`, `OAuthConsent`, `components/ui`, `lib/AuthContext`) was **not** copied.

## Honest gaps

- Last deploy is **May 2026**, not “today’s” code.
- `NSViewer.jsx` exists and is **not routed** in `App.jsx`.
- ΩStack / RH tabs are product UI. They do **not** prove RH or NS. This snapshot does not adopt those claims.
- No CFD solver, no backend functions, no SDK. This is a visualization / reference SPA on Base44.
- Tree is not a complete runnable Vite app without the omitted Base44 platform files.
