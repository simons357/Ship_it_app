# Zenodo remediation — `phirenorm-june30-conditional`

| Field | Value |
| --- | --- |
| Record ID | `21071991` |
| DOI | `10.5281/zenodo.21071991` |
| Disposition | **KEEP** |
| Alias | PhiRenorm June 30 conditional (open ||u^r/r||_∞) |
| Needs description errata | `True` |
| Needs title fix | `False` |
| Needs file fix | `True` |

## Clean title (use this — no banners)

Phi-Renormalization for Axisymmetric-with-Swirl Navier–Stokes: A Conditional Reduction of Global Regularity

## Current live title

Phi-Renormalization for Axisymmetric-with-Swirl Navier–Stokes: A Conditional Reduction of Global Regularity

## Errata banner in live title?

`False`

## Withdrawn / not claimed

- Unconditional classical 3D Navier–Stokes global regularity
- Clay / Millennium Statement (B) via this deposit alone

## File fix

```json
{
  "needed": true,
  "reason": "Live TeX/PDF still label energy norms as \\dot H^{2.6}; correct is \\dot H^{1.3}",
  "upload_pack": "data/zenodo/upload_packs/21071991",
  "replace_files": [
    "Simons_PhiRenorm_Swirl_2026-06-30.tex",
    "Simons_PhiRenorm_Swirl_2026-06-30.pdf"
  ]
}
```

## Description block (paste under original abstract)

<h3>File correction notice (September 2026)</h3>
<p>This deposit remains in the <strong>KEEP</strong> set. The title is a scholarly title without editorial banners.</p>
<p><strong>File correction:</strong> energy / dual norms previously labeled <code>\dot H^{2.6}</code> are relabeled <code>\dot H^{1.3}</code> (22 Aug 2026 audit). The open barrier <code>||u^r/r||_∞</code> / <code>op:gronwall</code> is unchanged. This is a <em>conditional</em> reduction — not a global regularity proof, not Clay Statement (B).</p>
<p><strong>Withdrawn / not claimed:</strong></p><ul><li>Unconditional classical 3D Navier–Stokes global regularity</li><li>Clay / Millennium Statement (B) via this deposit alone</li></ul>
<p>See the author status index: <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a></p>
<p><em>Credit for this DOI:</em> timestamp / history of work. Not current submit text unless listed in the KEEP set on the status index.</p>

## Notes

KEEP conditional. Open: ||u^r/r||_∞ / op:gronwall. File fix: replace Zenodo TeX+PDF — energy norms \dot H^{2.6} → \dot H^{1.3} (Aug 22 audit). Upload pack: data/zenodo/upload_packs/21071991/.
