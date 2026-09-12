# Freeze triage (Step 2)

Owner-reported symptom: the app freezes. Investigation order from the
handoff brief, applied to the three inspected builds.

## Named root cause (as of 2026-08-24)

**The freeze that is proven is the Base44 editor / login wall on a
phone**, not a proven React main-thread lock in the public preview.

Confirmed:

- Editor URL `app.base44.com/apps/<id>/editor/preview` is a login wall
  and is the URL Jonathan said not to send. That is the freeze he
  reported from the field.
- Public preview `preview--6a58e103….base44.app` loaded, ingested, and
  exported in this VM’s browser without hanging.
- Minified bundle SHA-256
  `720a21e0e061997909f4ea6ca85caeff60a08af8b1d5157081746a76ff6ba8de`
  (1,150,051 bytes) is unchanged after re-fetch.

## Brief’s six causes, scored against build B’s bundle

| # | Cause | Score against B glass | Action |
|---|---|---|---|
| 1 | Unbounded re-render / `useEffect` identity | **Cannot confirm from minified code.** Source is not exported. | Export Base44 source; audit every `useEffect`. |
| 2 | Unpaginated list | **Likely contributing if corpus grows.** `Conversation.list(-created_date, 200)` / `500`. No virtualization in the bundle. ~14 records: not enough to lock. | Pagination or `react-window` on canonical UI. |
| 3 | Waterfall / N+1 in render | **Possible.** `Conversation.filter` + `Book.list` + `Artifact.list` + `base44.entities.Conversation.get`. | Loaders; batch. |
| 4 | Full bodies in state | **Possible.** List pages pull full Conversation objects. One export had `raw_content: null`. | Summaries + on-demand body. |
| 5 | No error boundary | **Likely.** Production Base44 often swallows render throws into a blank screen. | Top-level ErrorBoundary on canonical. |
| 6 | Missing DB index | **Not applicable until we own Postgres.** B is Base44 entities, not our Supabase. | Index `created_at` / `owner_id` when we migrate. |

## Canonical git app (`chatvault/`)

This app is not React. There is no `useEffect`. Freeze vectors that
still apply, and what this pass changed:

- Rendering every vault entry as a full DOM card → **paginated at 50**.
- Holding every raw blob in `localStorage` → quota freeze at large
  corpora (not yet; export is the escape hatch).
- Uncaught render throw → top-level `try/catch` plus `window.error` /
  `unhandledrejection` now render a fatal panel instead of a blank screen.

## Reproduction note

1. Do **not** open `https://app.base44.com/apps/6a58e103fedcde66a0a7710e/editor/preview` on a phone. That is the editor freeze.
2. Use `https://preview--6a58e103fedcde66a0a7710e.base44.app/` to exercise the glass app.
3. For the git engine: `cd chatvault && python3 -m http.server 4173` → `http://127.0.0.1:4173/`.

## What is not claimed

I have not proven a React infinite loop. Claiming that without source
would be guesswork. The first cheap check (re-render loop) remains
**open until Base44 source is exported**.
