# Zenodo public-record restore pack

**Fastest way to take the crime tape off the public titles:** log into zenodo.org yourself and paste the restore titles (~15 minutes). This cloud agent cannot sign into zenodo.org as Jonathan Simons. It will never ask for the account password.

Intended public layout:

1. Public-facing paper = honest corrected work with a **clean title** (no withdrawn/superseded stamp).
2. Page 1 of the PDF references the status/errata note and explains **why** August 2026 happened (prize-claim language walked back; files were never tombstoned).
3. Errata on **page 2** (walked-back prize language, not a tombstone).
4. Publish **without** “withdrawn” plastered on Zenodo titles.

Fact check, 26 August 2026: records still `status=published`, `access=open`. Titles were stamped ~21 August 2026 12:42–12:44 UTC. Owner id `1627782`. Record `20518058` is HTTP 410 GONE — skip it; do not file a deletion/takedown on the rest.

This repository does **not** write to zenodo.org. Domain Architect is a local FRA classifier (inquiry). ChatVault is search. Neither withdrew these deposits.

## Fast path — titles only (~15 min)

Do this first. It is what the public sees in search results.

1. Open https://zenodo.org and log in as the owner.
2. Keep this table (or `out/PASTE_TITLES.md`) in another tab.
3. For **each version URL** below — not only the concept URL, which often shows the latest version:
   1. Open the version URL.
   2. Click **Edit**.
   3. Click the **Title** field. Select all.
   4. Paste the restore title. (Strip `[Claim withdrawn - see errata]` / `[Superseded - see errata]` and any stray trailing `"`.)
   5. In **Description**, delete the screaming August 2026 paragraph that says claims are withdrawn. Keep the original scientific abstract. Paste the calm pointer once (below).
   6. Click **Publish**. Confirm if asked.
   7. Reload the public page. The title must have no bracket prefix.
4. Do **not** click Request deletion / Takedown.

### Restore these titles (exact original wording)

| Version URL | Paste this title |
| --- | --- |
| https://zenodo.org/records/20405526 | Global Regularity of the Navier-Stokes Equations on T3: Spectral Non-Dispersal, the Ring Lemma, Phi-Renormalization, and the Shell-Conditioned Commutator Estimate |
| https://zenodo.org/records/20269843 | The Quantum Lens: A Spectral Framework Connecting the Millennium Prize Problems |
| https://zenodo.org/records/20405593 | The Montgomery–Dyson Coincidence as a Q6 Prime Lattice Eigenvalue Identity |
| https://zenodo.org/records/20518294 | Route C: Spectral Closure of the Zero-Density Law — Conditional on Two Analytic Gaps |
| https://zenodo.org/records/20518250 | Route C: Spectral Closure of the Zero-Density Law — Conditional on Two Analytic Gaps |
| https://zenodo.org/records/20552400 | A Universal Non-Concentration Principle: SND ≡ GNC ≡ Bridge |
| https://zenodo.org/records/20552682 | The Prime Lattice as a Prototype for the BSD Hamiltonian: Rank as Spectral Multiplicity and the Zeta-Function Case of the Birch and Swinnerton-Dyer Conjecture |
| https://zenodo.org/records/20552171 | A Quantum Field Theory on the Prime Manifold: Navier–Stokes, Riemann, and Goldbach Under a Single Hamiltonian |
| https://zenodo.org/records/20552223 | A Quantum Field Theory on the Prime Manifold: Navier–Stokes, Riemann Hypothesis, and Goldbach Under a Single Hamiltonian |
| https://zenodo.org/records/19842060 | Borromean Triads, the Ring Lemma, and Spectral Non-Dispersal |
| https://zenodo.org/records/20272545 | Spectral Non-Concentration Implies Global Regularity for 3D Navier–Stokes on T³ |
| https://zenodo.org/records/20405591 | The Q_N Operator: Self-Adjointness, Spectral Floor, and a Route to the Riemann Hypothesis via Renormalized GCD Eigenvalues |
| https://zenodo.org/records/20271457 | The Ramanujan–Möbius Identity and Prime Lattice Spectral Theory: GCD Operators, Spectral Floors, and the Arithmetic Casimir Constant |
| https://zenodo.org/records/20272622 | The Quantum Millennium: A Spectral Unification of the Navier–Stokes Problem and the Millennium Prize Conjectures |
| https://zenodo.org/records/20405585 | Borromean Triads, the Ring Lemma, and Spectral Non-Dispersal: A Conditional Regularity Framework for 3D Navier-Stokes |
| https://zenodo.org/records/20405599 | The GCD Spectral Attractor: A Unified Structural Framework for Navier-Stokes, the Riemann Hypothesis, and the Simons Field Equation |
| https://zenodo.org/records/20269536 | Spectral Non-Concentration Criteria for Navier–Stokes Regularity on T³ |

Also open the concept URL if it still shows a stamped title (concept IDs often resolve to latest): `20405525`, `20269842`, `20405592`, `19842059`, `20272544`, `20405590`, `20272621`, `20405584`, `20405598`, `20269535`, `20269737`. If the concept page is already the version you just edited, you are done for that pair.

If a search hit still starts with a bracket prefix and is not in this table, paste the original title with the prefix removed. Do not leave the stamp. Do not request deletion.

### Rename the status note (not a restore-to-original)

| Version URL | Paste this title |
| --- | --- |
| https://zenodo.org/records/22050978 | August 2026 status note: live stack and walked-back prize language |
| https://zenodo.org/records/22045484 | August 2026 status note: live stack and walked-back prize language |

Do **not** leave “What Stands and What Is Withdrawn” on the public title.

### Leave these titles alone

Titles are already clean. Optional: add the calm pointer to the description only.

| DOI | Title now |
| --- | --- |
| 10.5281/zenodo.22050963 | Route C: A Spectral Approach to Zero-Density Estimates, Conditional on Two Analytic Gaps |
| 10.5281/zenodo.22050974 | Phi-Renormalization for Axisymmetric Navier-Stokes with Swirl: Algebraic Cancellation of the 1/r^4 Axis Term |
| 10.5281/zenodo.22050975 | same Phi paper (sibling version) |
| 10.5281/zenodo.21071991 | Phi-Renormalization for Axisymmetric-with-Swirl Navier–Stokes: A Conditional Reduction of Global Regularity |
| 10.5281/zenodo.20518388 | Route C title already clean; optional: strip the stray trailing `"` |
| 10.5281/zenodo.22050962 | Inverse-GCD Q_N note (already cleaner than 22045478) |

### Optional title cleanup

https://zenodo.org/records/22045478 — currently includes “Withdrawal of Full-Spectrum Floor Claims”. Paste:

`The Inverse-GCD Operator Q_N: Definitions and a Restricted Rayleigh Bound`

Latest sibling `10.5281/zenodo.22050962` is already cleaner.

### Calm description pointer

Paste this in place of any “Claim withdrawn” / “claims are withdrawn” / “full-spectrum spectral floor claims are withdrawn” paragraph. Keep the original abstract.

```html
<p>August 2026: prize-claim language in this deposit is walked back. The file remains published and open. See page 2 of the status note <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a>. Live Route C: <a href="https://doi.org/10.5281/zenodo.22050963">10.5281/zenodo.22050963</a>. Live Φ-renormalization: <a href="https://doi.org/10.5281/zenodo.22050974">10.5281/zenodo.22050974</a>. Unconditional 3D Navier–Stokes, the Riemann hypothesis, and Goldbach are not claimed.</p>
```

Status-note description (for 22050978 / 22045484):

```html
<p>Author status sheet for the 2026 spectral preprint stack. Page 1 states the live exploratory work and why the August 2026 action happened: prize-claim language was walked back; the files were never unpublished and never tombstoned. Page 2 is the errata. Public titles should be the original wording, without a retraction stamp. This is not a Zenodo takedown. Live Route C: <a href="https://doi.org/10.5281/zenodo.22050963">10.5281/zenodo.22050963</a>. Live Φ-renormalization: <a href="https://doi.org/10.5281/zenodo.22050974">10.5281/zenodo.22050974</a>. Unconditional 3D Navier–Stokes, the Riemann hypothesis, and Goldbach are not claimed.</p>
```

Machine-readable copy of every paste string: [`titles.json`](titles.json).

## Complete path — upload wrapped PDFs

After the titles are clean (or in the same Edit / New version session):

1. Open the record → **New version**.
2. Upload the matching file from `out/` (table below).
3. Keep any existing `.tex` / figures. Do not delete source files.
4. Confirm the title is the clean restore title.
5. **Publish**.

| Record | Upload this file |
| --- | --- |
| 22050978 (status note) | `out/status_note_public_facing.pdf` |
| 20552400, 20552682, 20552171, 20552223, 19842060, 20272545, 20271457, 20272622 | `out/<id>_public_facing.pdf` (cover + errata + original pages) |
| 20405526, 20269843, 20405593, 20518294, 20518250, 20405591, 20405585, 20405599, 20269536 | `out/notices/<id>_public_facing_notice.pdf` (2-page notice; TeX/webloc-only records) |

Wrapped June PDFs: **page 1** clean public face, **page 2** errata, **page 3+** original draft.

### OPTIONAL — live Route C / Phi reader notice

Titles on `22050963` and `22050974` are already clean. **Prefer a description pointer** so the scientific PDF does not look like a retraction banner.

If you still want a one-page reader notice prepended:

- `out/optional/22050963_with_reader_notice.pdf`
- `out/optional/22050974_with_reader_notice.pdf`

Do not upload these unless you explicitly want that extra first page.

## How to give a later agent permission (token, never password)

This agent cannot sit in your Zenodo session. Two honest options:

**A. You restore the titles** with the paste list above (~15 minutes). That is the straightforward path.

**B. Create a Zenodo personal access token** and tell a later agent to PATCH metadata.

1. Sign in at zenodo.org.
2. Open https://zenodo.org/account/settings/applications/tokens/new/ (Applications → Personal access tokens → New token).
3. Name it something like `title-restore`.
4. Enable scopes **`deposit:write`** and **`deposit:actions`**. Nothing else is required.
5. Create the token. Copy it once. Store it as an environment variable `ZENODO_TOKEN`, not in git.
6. Tell the later agent: “Here is a Zenodo personal access token. PATCH titles from `docs/zenodo-public-record/titles.json`.” Then revoke the token.

**Never paste the zenodo.org account password.** A password is not an API credential. This pack will not collect one.

Metadata-only restore (classic deposit API, after you have a token):

```bash
# Unlock, PUT title, republish. Repeat per version id.
export ZENODO_TOKEN='…'   # personal access token, not a password
ID=20552400
TITLE='A Universal Non-Concentration Principle: SND ≡ GNC ≡ Bridge'

curl -sS -X POST \
  -H "Authorization: Bearer $ZENODO_TOKEN" \
  "https://zenodo.org/api/deposit/depositions/${ID}/actions/edit"

# GET the deposition, merge metadata.title, PUT the full metadata object
# (Zenodo validates if you PUT a partial metadata blob that drops required fields).

curl -sS -X POST \
  -H "Authorization: Bearer $ZENODO_TOKEN" \
  "https://zenodo.org/api/deposit/depositions/${ID}/actions/publish"
```

A later agent should GET each deposition, change only `metadata.title` (and the description paragraph), PUT, then publish. Do not send `metadata.doi` in a way that fails validation. Dry-run first.

## Rebuild the PDFs

```bash
python3 -m pip install pypdf reportlab   # already present in this cloud image
python3 docs/zenodo-public-record/generate_public_record.py
python3 -m unittest tests.test_zenodo_public_record
```

Fonts: DejaVu Serif at `/usr/share/fonts/truetype/dejavu/` (Unicode: ≡, – , ³, Φ). Sources for wraps live in `sources/` so generation does not depend on `/tmp`.

What this generator will not do: log into Zenodo, request deletion, claim RH or Clay NS, or put WITHDRAWN in a new public title.

## Claims this pack does not make

- The Riemann hypothesis is not proved here.
- Clay Navier–Stokes is not proved here.
- Domain Architect is inquiry, not a theorem prover.
- ChatVault is search.
