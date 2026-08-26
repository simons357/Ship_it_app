# Zenodo public-record restore pack

**Titles were not written on zenodo.org.** This environment has no Zenodo
personal access token (`ZENODO_TOKEN` / `ZENODO_ACCESS_TOKEN`). The agent
will not log in with a password and will not ask for one.

## One action that lets an agent finish

The only permission an agent needs is a Zenodo PAT — not 27 clicks, not
the account password.

1. Sign in at zenodo.org.
2. Create a token at https://zenodo.org/account/settings/applications/tokens/new/
   with scopes **`deposit:write`** and **`deposit:actions`**.
3. Send the token to the agent as `ZENODO_TOKEN` (or `ZENODO_ACCESS_TOKEN`)
   with the words **“use this token”**.
4. The agent runs one command:

```bash
python3 docs/zenodo-public-record/api_restore_titles.py --apply
```

That unlocks each deposition, PUTs the clean title plus a calm description
pointer, and republishes. Dry-run (no writes) is the default without
`--apply`. Revoke the token afterwards.

## Paper layout (locked)

Public-facing PDFs in `out/`:

1. **Page 1** — corrected honest paper face, **clean title**, numbered footnote
   `¹ August 2026 prize-claim language walked back; see errata below / page 2
   of this file and status note 10.5281/zenodo.22050978`.
2. **Page 2** — errata report (underneath the paper, not a title banner).
3. **Page 3+** — original 2026 draft when wrapping a PDF.

No `[Claim withdrawn]`, `[Superseded]`, or `WITHDRAWN` on page 1 or in
restore titles. Domain Architect is inquiry. ChatVault is search. Neither
withdrew these deposits. RH and Clay NS are not claimed.

Rebuild:

```bash
python3 docs/zenodo-public-record/generate_public_record.py
python3 -m unittest tests.test_zenodo_public_record
```

Status note PDF: `out/status_note_public_facing.pdf` (upload to
`10.5281/zenodo.22050978` after the title restore). Wrapped June/May PDFs:
`out/<id>_public_facing.pdf`. TeX-only records: `out/notices/`.

Machine-readable titles: [`titles.json`](titles.json). Job list for the
API script: [`out/RESTORE_JOBS.md`](out/RESTORE_JOBS.md).

## Live cite stack (titles already clean)

- Route C: https://doi.org/10.5281/zenodo.22050963
- Φ-renormalization: https://doi.org/10.5281/zenodo.22050974
- Inverse-GCD / Q6 note: https://doi.org/10.5281/zenodo.22050962
- Ring lemma: https://doi.org/10.5281/zenodo.22050976

Status note `22050978` is still titled “What Stands and What Is Withdrawn”
on zenodo.org until `--apply` runs. Restore title:
**August 2026 status note: live stack and walked-back prize language**.

May 18 GCD Ramanujan `20269738` already has a clean API title (later
version `20271457` is stamped). May 14 **Diffuse Cascade** is `20183673`;
May 14 **Montgomery–Dyson Coincidence Resolved** is `20184148`.
`19842061` is an unrelated paper — not used.

Fact check, 26 August 2026: records still `status=published`, `access=open`.
Stamped ~21 August 2026 12:42–12:44 UTC. Owner id `1627782`. Record
`20518058` is HTTP 410 GONE — skip it; do not file a deletion/takedown.

## PDF upload (optional, after titles)

Titles first. Then, if you want the footnote+errata face on the file:

1. Record → **New version**.
2. Upload the matching `out/` PDF. Keep existing `.tex` / figures.
3. Confirm the title is the clean restore title. **Publish**.

Live Route C / Phi wraps in `out/optional/` are optional. Prefer a
description pointer so those scientific PDFs do not look like a banner.

Fonts: DejaVu Serif at `/usr/share/fonts/truetype/dejavu/`. Sources for
wraps live in `sources/`.

What this pack will not do: log into Zenodo with a password, request
deletion, claim RH or Clay NS, or put WITHDRAWN in a new public title.
