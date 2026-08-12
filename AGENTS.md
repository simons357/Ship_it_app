# Notes for Cursor agents

## Read this first

The GitHub repo is still named `Ship_it_app`. That name is **historical only**.

**Ship it** (the app) was abandoned. Do **not** rebuild it, invent Ship It product pages, or treat branding under `assets/shipit_*` as a product to revive.

Also abandoned — do not revive:

- **Planet Hunter** / ExoRatio-as-app framing
- **Scallion** logo / branding

If a draft PR is mainly Ship It, Planet Hunter, or Scallion: leave it closed / alone unless Jonathan explicitly reverses this.

## What this repo actually is

Jonathan’s working vault for agent experiments and drafts that survive review. Different threads share one GitHub repo; they are **not** one product.

### Currently on `main`

Harmonic Blueprint Experiment 01 (closed null result):

- Protocol / report under `docs/`
- Runner: `hb_ringdown_test.py`
- Data: `data/qnm_events.csv`, `nodes.json`
- Results: `results/`

```bash
pip install -r requirements.txt
python -m unittest tests/test_hb_ringdown.py
```

### Other live threads (in draft PRs — not abandoned)

Examples: anesthesia / Operator Assist lane, AquaQuartz, portfolio, rigor memos, Cursor setup advisor, TITAN-X plan. Ask Jonathan which thread to extend when unclear.

## Cursor Cloud

`.cursor/environment.json` installs Python deps from `requirements.txt` when present, and npm only if a `package.json` appears after a future merge.

Do **not** invent a Next.js Ship It app to “complete setup.”

## How to work

1. One task → one branch → one PR.
2. Prefer extending the thread Jonathan named in the prompt.
3. Keep secrets out of git.
4. Explain changes in plain language in the PR body — Jonathan is learning the workflow.
5. Human map for repos/agents: `docs/GETTING-STARTED.md`.
