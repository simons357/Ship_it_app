# Zenodo remediation — manual instructions

Generated for deposits that still need a live fix.
Presentation rule: clean title on top; correction notice only in description.

## If you have an API token

```bash
export ZENODO_ACCESS_TOKEN='<token from zenodo.org/account/settings/applications/>'
python3 scripts/zenodo_metadata_remediation.py apply
# optional single record:
python3 scripts/zenodo_metadata_remediation.py apply --record-id 21071991
```

Token scopes needed: `deposit:write` + `deposit:actions`.

## Copy-paste per record

## Record 21071991 — `10.5281/zenodo.21071991`

- Disposition: **KEEP**
- Alias: PhiRenorm June 30 conditional (open ||u^r/r||_∞)

1. Open https://doi.org/10.5281/zenodo.21071991
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `Phi-Renormalization for Axisymmetric-with-Swirl Navier–Stokes: A Conditional Reduction of Global Regularity`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>File correction notice (September 2026)</h3>
<p>This deposit remains in the <strong>KEEP</strong> set. The title is a scholarly title without editorial banners.</p>
<p><strong>File correction:</strong> energy / dual norms previously labeled <code>\dot H^{2.6}</code> are relabeled <code>\dot H^{1.3}</code> (22 Aug 2026 audit). The open barrier <code>||u^r/r||_∞</code> / <code>op:gronwall</code> is unchanged. This is a <em>conditional</em> reduction — not a global regularity proof, not Clay Statement (B).</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Unconditional classical 3D Navier–Stokes global regularity</li><li>Clay / Millennium Statement (B) via this deposit alone</li></ul>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. **Files** — delete the old TeX/PDF on the new version draft, then upload from:
   `data/zenodo/upload_packs/21071991/`
   Replace: Simons_PhiRenorm_Swirl_2026-06-30.tex, Simons_PhiRenorm_Swirl_2026-06-30.pdf
6. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
7. Publish version.

---

## Record 20552400 — `10.5281/zenodo.20552400`

- Disposition: **PARK_ARCHIVE**
- Alias: Triple Lock SND ≡ GNC ≡ Bridge

1. Open https://doi.org/10.5281/zenodo.20552400
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `A Universal Non-Concentration Principle: SND ≡ GNC ≡ Bridge`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>SND ≡ GNC ≡ Bridge identity</li><li>Triple Lock unconditional closure</li><li>Full-spectrum λ_min claims</li><li>SFE→NS/RH glue</li></ul>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20552223 — `10.5281/zenodo.20552223`

- Disposition: **PARK_ARCHIVE**
- Alias: Three-in-one NS/RH/Goldbach (alternate packaging)

1. Open https://doi.org/10.5281/zenodo.20552223
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `A Quantum Field Theory on the Prime Manifold: Navier–Stokes, Riemann Hypothesis, and Goldbach Under a Single Hamiltonian`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Millennium-from-SFE</li><li>Single Hamiltonian solves NS/RH/Goldbach</li></ul>
<p><strong>Corrected public note:</strong> <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20552171 — `10.5281/zenodo.20552171`

- Disposition: **PARK_ARCHIVE**
- Alias: Three-in-one / Prime Manifold Hamiltonian

1. Open https://doi.org/10.5281/zenodo.20552171
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `A Quantum Field Theory on the Prime Manifold: Navier–Stokes, Riemann, and Goldbach Under a Single Hamiltonian`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Millennium-from-SFE</li><li>Single Hamiltonian solves NS/RH/Goldbach</li><li>Full-spectrum λ_min > -1/2 as governing inequality</li></ul>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20552080 — `10.5281/zenodo.20552080`

- Disposition: **PARK_ARCHIVE**
- Alias: T2 + GNC–Goldbach bridge (old)

1. Open https://doi.org/10.5281/zenodo.20552080
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `Explicit Decay Rate and Quantitative Threshold for the SND Gronwall Inequality: T2 Conditional Closure and GNC–Goldbach Bridge`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>GNC–Goldbach bridge as load-bearing</li><li>Unconditional T2 closure without SND</li></ul>
<p><strong>Corrected public note:</strong> <a href="https://doi.org/10.5281/zenodo.22050965">10.5281/zenodo.22050965</a></p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20518388 — `10.5281/zenodo.20518388`

- Disposition: **PARK_ARCHIVE**
- Alias: Route C older spectral-closure packaging

1. Open https://doi.org/10.5281/zenodo.20518388
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `Route C: Spectral Closure of the Zero-Density Law — Conditional on Two Analytic Gaps`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Riemann Hypothesis proved</li><li>Spectral closure of zero-density as unconditional</li></ul>
<p><strong>Corrected public note:</strong> <a href="https://doi.org/10.5281/zenodo.22050963">10.5281/zenodo.22050963</a></p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20518057 — `10.5281/zenodo.20518057`

- Disposition: **PARK_ARCHIVE**
- Alias: Older SND conditional framework (pre-Ring+SND merge)

1. Open https://doi.org/10.5281/zenodo.20518057
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `Spectral Non-Dispersal, the Ring Lemma, and a Conditional Regularity Framework for the Navier–Stokes Equations on T³`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Unconditional NS regularity implied by framework as written</li></ul>
<p><strong>Corrected public note:</strong> <a href="https://doi.org/10.5281/zenodo.22050976">10.5281/zenodo.22050976</a></p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20405599 — `10.5281/zenodo.20405599`

- Disposition: **PARK_ARCHIVE**
- Alias: GCD Spectral Attractor unified / SFE packaging

1. Open https://doi.org/10.5281/zenodo.20405599
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `The GCD Spectral Attractor: A Unified Structural Framework for Navier-Stokes, the Riemann Hypothesis, and the Simons Field Equation`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Unified NS + RH + Simons Field Equation proved</li><li>SFE→NS glue</li><li>Millennium via GCD attractor</li></ul>
<p><strong>Corrected public note:</strong> <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20405597 — `10.5281/zenodo.20405597`

- Disposition: **PARK_ARCHIVE**
- Alias: Older Phi-renorm axisymmetric concept

1. Open https://doi.org/10.5281/zenodo.20405597
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `Phi-Renormalization and Axisymmetric-with-Swirl Navier-Stokes: Algebraic Cancellation of the Axis Singularity`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Unconditional classical 3D NS global regularity</li></ul>
<p><strong>Corrected public note:</strong> <a href="https://doi.org/10.5281/zenodo.22050974">10.5281/zenodo.22050974</a></p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20405593 — `10.5281/zenodo.20405593`

- Disposition: **PARK_ARCHIVE**
- Alias: Montgomery–Dyson as Q6 identity

1. Open https://doi.org/10.5281/zenodo.20405593
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `The Montgomery–Dyson Coincidence as a Q6 Prime Lattice Eigenvalue Identity`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Montgomery–Dyson coincidence resolved via Q6</li><li>RH progress claim</li></ul>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20405591 — `10.5281/zenodo.20405591`

- Disposition: **PARK_ARCHIVE**
- Alias: Q_N operator RH spectral route

1. Open https://doi.org/10.5281/zenodo.20405591
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `The Q_N Operator: Self-Adjointness, Spectral Floor, and a Route to the Riemann Hypothesis via Renormalized GCD Eigenvalues`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Riemann Hypothesis proved via Q_N</li><li>Full-spectrum spectral floor as RH proof</li></ul>
<p><strong>Corrected public note:</strong> <a href="https://doi.org/10.5281/zenodo.22050962">10.5281/zenodo.22050962</a></p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20405589 — `10.5281/zenodo.20405589`

- Disposition: **PARK_ARCHIVE**
- Alias: Q6 Goldbach dark-state packaging

1. Open https://doi.org/10.5281/zenodo.20405589
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `A Q6 Spectral Route to the Strong Goldbach Conjecture: Spectral Non-Concentration and the Inverse-GCD Operator`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Goldbach via dark states</li><li>Full-spectrum λ_min floor</li><li>Bridge conjecture as load-bearing</li></ul>
<p><strong>Corrected public note:</strong> <a href="https://doi.org/10.5281/zenodo.22050962">10.5281/zenodo.22050962</a></p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20405585 — `10.5281/zenodo.20405585`

- Disposition: **PARK_ARCHIVE**
- Alias: Ring Lemma Borromean (May conditional toolkit)

1. Open https://doi.org/10.5281/zenodo.20405585
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `Borromean Triads, the Ring Lemma, and Spectral Non-Dispersal: A Conditional Regularity Framework for 3D Navier-Stokes`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Unconditional global regularity</li></ul>
<p><strong>Corrected public note:</strong> <a href="https://doi.org/10.5281/zenodo.22050976">10.5281/zenodo.22050976</a></p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20405526 — `10.5281/zenodo.20405526`

- Disposition: **PARK_ARCHIVE**
- Alias: Global Regularity / Clay Statement (B) packaging

1. Open https://doi.org/10.5281/zenodo.20405526
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `Global Regularity of the Navier-Stokes Equations on T3: Spectral Non-Dispersal, the Ring Lemma, Phi-Renormalization, and the Shell-Conditioned Commutator Estimate`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Clay Statement (B) proved</li><li>Unconditional global regularity for classical 3D NS on T³</li></ul>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20405405 — `10.5281/zenodo.20405405`

- Disposition: **PARK_ARCHIVE**
- Alias: Phi-renorm + global regularity (old Track B)

1. Open https://doi.org/10.5281/zenodo.20405405
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `Phi-Renormalization and Global Regularity for Axisymmetric-with-Swirl Navier–Stokes: Algebraic Cancellation of the Axis Singularity, Gronwall-Free Convergence, and the Prime Index Connection`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Unconditional global regularity for axisymmetric-with-swirl NS</li><li>Gronwall-free convergence as Clay closure</li><li>Prime index connection as Millennium glue</li></ul>
<p><strong>Corrected public note:</strong> <a href="https://doi.org/10.5281/zenodo.22050974">10.5281/zenodo.22050974</a></p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20272545 — `10.5281/zenodo.20272545`

- Disposition: **PARK_ARCHIVE**
- Alias: SND implies global NS regularity (May packaging)

1. Open https://doi.org/10.5281/zenodo.20272545
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `Spectral Non-Concentration Implies Global Regularity for 3D Navier–Stokes on T³`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Unconditional global regularity for 3D NS</li><li>SND as proved closure</li></ul>
<p><strong>Corrected public note:</strong> <a href="https://doi.org/10.5281/zenodo.22050976">10.5281/zenodo.22050976</a></p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20269843 — `10.5281/zenodo.20269843`

- Disposition: **PARK_ARCHIVE**
- Alias: Quantum Lens Millennium connector

1. Open https://doi.org/10.5281/zenodo.20269843
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `The Quantum Lens: A Spectral Framework Connecting the Millennium Prize Problems`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Millennium-from-SFE glue</li><li>Six Millennium problems connected via Q6 hub</li></ul>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 19842060 — `10.5281/zenodo.19842060`

- Disposition: **PARK_ARCHIVE**
- Alias: Early Ring Lemma / Borromean note

1. Open https://doi.org/10.5281/zenodo.19842060
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `Borromean Triads, the Ring Lemma, and Spectral Non-Dispersal`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is kept as <strong>dated archive</strong>. The title above is the original scholarly title without editorial banners.</p>
<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Unconditional regularity implied by early SND packaging</li></ul>
<p><strong>Corrected public note:</strong> <a href="https://doi.org/10.5281/zenodo.22050976">10.5281/zenodo.22050976</a></p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20552682 — `10.5281/zenodo.20552682`

- Disposition: **REVIEW**
- Alias: BSD Hamiltonian / prime lattice prototype

1. Open https://doi.org/10.5281/zenodo.20552682
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `The Prime Lattice as a Prototype for the BSD Hamiltonian: Rank as Spectral Multiplicity and the Zeta-Function Case of the Birch and Swinnerton-Dyer Conjecture`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is <strong>not</strong> in the current KEEP set. Treat it as exploratory / under review. The title has no editorial banners.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>BSD conjecture resolved via prime-lattice Hamiltonian</li></ul>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20271879 — `10.5281/zenodo.20271879`

- Disposition: **REVIEW**
- Alias: GCD operators and Ramanujan quadratic forms

1. Open https://doi.org/10.5281/zenodo.20271879
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `Spectral Properties of GCD Operators and Ramanujan Quadratic Forms`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is <strong>not</strong> in the current KEEP set. Treat it as exploratory / under review. The title has no editorial banners.</p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20271457 — `10.5281/zenodo.20271457`

- Disposition: **REVIEW**
- Alias: Ramanujan–Möbius / prime lattice spectral theory

1. Open https://doi.org/10.5281/zenodo.20271457
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `The Ramanujan–Möbius Identity and Prime Lattice Spectral Theory: GCD Operators, Spectral Floors, and the Arithmetic Casimir Constant`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is <strong>not</strong> in the current KEEP set. Treat it as exploratory / under review. The title has no editorial banners.</p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20269536 — `10.5281/zenodo.20269536`

- Disposition: **REVIEW**
- Alias: SND criteria Paper2 draft

1. Open https://doi.org/10.5281/zenodo.20269536
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `Spectral Non-Concentration Criteria for Navier–Stokes Regularity on T³`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is <strong>not</strong> in the current KEEP set. Treat it as exploratory / under review. The title has no editorial banners.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Unconditional NS regularity from early SND packaging</li></ul>
<p><strong>Corrected public note:</strong> <a href="https://doi.org/10.5281/zenodo.22050976">10.5281/zenodo.22050976</a></p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20184148 — `10.5281/zenodo.20184148`

- Disposition: **REVIEW**
- Alias: Montgomery–Dyson 'resolved' packaging

1. Open https://doi.org/10.5281/zenodo.20184148
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `The Montgomery–Dyson Coincidence Resolved by the Q6 Prime Lattice Operator`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is <strong>not</strong> in the current KEEP set. Treat it as exploratory / under review. The title has no editorial banners.</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Montgomery–Dyson coincidence resolved via Q6</li></ul>
<p><strong>Corrected public note:</strong> <a href="https://doi.org/10.5281/zenodo.22050962">10.5281/zenodo.22050962</a></p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---

## Record 20183673 — `10.5281/zenodo.20183673`

- Disposition: **REVIEW**
- Alias: Diffuse cascade / triad equidistribution numerics

1. Open https://doi.org/10.5281/zenodo.20183673
2. Click **New version**.
3. **Title** — paste exactly (no banners):

   `Diffuse Cascade in 3D Navier–Stokes: Time-Resolved Evidence for Triad Equidistribution`

4. **Description** — keep any honest original abstract at the top, then append:

```html
<h3>Correction notice (August 2026)</h3>
<p>This deposit is <strong>not</strong> in the current KEEP set. Treat it as exploratory / under review. The title has no editorial banners.</p>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>
```

5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.
6. Publish version.

---
