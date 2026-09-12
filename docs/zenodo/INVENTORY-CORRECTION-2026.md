# Zenodo inventory correction — 2026-09-12

**Author deposits:** Jonathan R. Simons / Simons, Jonathan*  
**Source of truth:** live Zenodo API fetch (`scripts/zenodo_inventory_live_fetch.py`)  
**Settled dispositions:** `data/zenodo/deposit_metadata.json` (Aug 2026 KEEP/PARK pack) + PhiRenorm June 30 `21071991` as conditional KEEP

---

## Is the Aug 14 Numbers dump the newest?

**No.** `ZENODO_INVENTORY_JONATHAN_SIMONS_2026-08-14` is **stale and internally corrupted**.

| Finding | Detail |
| --- | --- |
| File-column shift | **Confirmed.** DOI/title columns did not line up with `files`. Example: live `21071991` holds `Simons_PhiRenorm_Swirl_2026-06-30.{tex,pdf}`; Aug 14 attached `THREE_IN_ONE_NS_RH_GOLDBACH.*` to that DOI. The PhiRenorm files sat on empty DOI/title rows. |
| Empty leading rows | 3 rows with blank `record_id` / `doi` / `title` but populated files |
| Missing vs live | Aug 14 lacked the settled KEEP concept versions published later: `22050962`, `22050963`, `22050965`, `22050974`, `22050975`, `22050976`, `22050978`, plus earlier concept `19842060` and related ids `20183673`, `20184148` |
| Missing from live | None of the Aug 14 DOIs are gone from Zenodo |
| Title banners | Live titles currently have **no** leading `[Claim withdrawn]` / `[Superseded]` banners (0 `NEEDS_TITLE_CLEAN`). Aug 23 remediation pack still documented banners; either cleaned since, or pack snapshot differed |

Do **not** use the Aug 14 sheet for citations, file lists, or KEEP decisions.

---

## Corrected inventory paths

| File | Use |
| --- | --- |
| `data/zenodo/ZENODO_INVENTORY_CORRECTED_LIVE.csv` | Canonical corrected CSV |
| `data/zenodo/ZENODO_INVENTORY_CORRECTED_LIVE_numbers.csv` | Same data, UTF-8 BOM — open in Apple Numbers / Excel |
| `data/zenodo/ZENODO_INVENTORY_CORRECTED_LIVE.json` | Full payload + comparison block |
| `data/zenodo/ZENODO_INVENTORY_COMPARISON_AUG14.json` | Aug 14 vs live diff only |
| `data/zenodo/deposit_metadata.json` | Settled KEEP/PARK metadata pack (from remediation branch) |
| `scripts/zenodo_inventory_live_fetch.py` | Re-run against Zenodo API |

Regenerate:

```bash
python3 scripts/zenodo_inventory_live_fetch.py
```

---

## What was wrong

1. **Column misalignment in the Numbers export** — files shifted relative to DOI/title (classic spreadsheet paste / column-drag failure). Proven by live API file keys.
2. **Stale cutoff** — Aug 14 predates the corrected KEEP concept DOIs (`2205096x` / `2205097x`) and the public status index.
3. **No disposition column** — sheet mixed cite-worthy conditional work with withdrawn Millennium / unconditional packaging.

---

## How it was corrected

1. Queried Zenodo (`creators.name:"Simons, Jonathan*"`, `owners:1627782`) and fetched every known Aug 14 + settled record id.
2. Dropped false positives (unrelated creators named `Jonathan, Jonathan`).
3. Wrote live `record_id`, `doi`, `url`, `title`, `publication_date`, `version`, `creators`, `files`, `file_count`, `access`, `updated`.
4. Applied dispositions from the settled honest inventory only (no new KEEP inventions).

### Disposition rules used

| Disposition / flag | Meaning |
| --- | --- |
| **KEEP** | Cite these: Q6 (no RH), Φ-renorm algebra (`22050974`/`75`), Ring+SND conditional (`22050976`), T2 under SND, Route C exploratory, status index, PhiRenorm June 30 **conditional** (`21071991`, open \(\|u^r/r\|_\infty\)) |
| **PARK/ARCHIVE** | History only: unconditional NS, Quantum Lens, Millennium glue, Triple Lock, SFE→NS/RH, superseded concept versions |
| **REVIEW** | Present live but not in settled KEEP/PARK list — human call still needed |
| **NEEDS_TITLE_CLEAN** | Live title still has errata/withdrawn banner (count **0** at fetch time) |
| **NEEDS_AUDIT_FIX** | `21071991` TeX still contains \(\dot H^{2.6}\) labels (Aug 22 audit follow-up) |

---

## Counts (live fetch)

See `comparison_to_aug14.counts` in the JSON for the exact stamp. At correction time:

- **KEEP:** 8  
- **PARK/ARCHIVE:** 17  
- **REVIEW:** 6  
- **NEEDS_TITLE_CLEAN:** 0  
- **NEEDS_AUDIT_FIX:** 1 (`21071991`)

### KEEP set (cite)

| Record | DOI | Note |
| --- | --- | --- |
| 22050962 | 10.5281/zenodo.22050962 | Q6 operator — no RH claim |
| 22050974 | 10.5281/zenodo.22050974 | Φ-renorm algebra (long) |
| 22050975 | 10.5281/zenodo.22050975 | Φ-renorm algebra (short) |
| 22050976 | 10.5281/zenodo.22050976 | Ring + SND **conditional** |
| 22050965 | 10.5281/zenodo.22050965 | T2 under SND |
| 22050963 | 10.5281/zenodo.22050963 | Route C exploratory — RH not proved |
| 22050978 | 10.5281/zenodo.22050978 | Status index (live title now “August 2026 status note…”) |
| 21071991 | 10.5281/zenodo.21071991 | PhiRenorm June 30 **conditional**; `NEEDS_AUDIT_FIX` |

---

## PhiRenorm TeX follow-up (`21071991`)

Downloaded to `docs/papers/phi-renorm/Simons_PhiRenorm_Swirl_2026-06-30.tex`.

`\dot H^{2.6}` sites present (non-exhaustive): lines ~408, 415, 426, 522, 561, 675, 768, 820–823, 907. Treat as audit follow-up; do not cite as cleaned algebra paper (that role is `22050974` / `22050975`).

---

## What Jonathan must do

1. **Open** `data/zenodo/ZENODO_INVENTORY_CORRECTED_LIVE_numbers.csv` in Numbers — replace the Aug 14 sheet.
2. **Merge this PR** so the corrected inventory lives in the repo.
3. **Zenodo token** only if you still want description/title edits via `scripts/zenodo_metadata_remediation.py` (live titles currently lack banners; description errata blocks may still need work).
4. **Decide REVIEW rows** (`20552682` BSD, early GCD/Ramanujan notes, `20183673` diffuse cascade, `20184148` Montgomery “resolved” packaging) — likely PARK unless you explicitly want one kept.
5. **Optional:** scrub \(\dot H^{2.6}\) wording on `21071991` or point readers to KEEP Φ-renorm algebra DOIs.
