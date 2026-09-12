# Correction index — Harmonic Blueprint / spectral preprint stack

**Author:** Jonathan Robert Simons  
**Date:** August 2026 (metadata remediation freeze: 2026-08-23)  
**Status index DOI:** [10.5281/zenodo.22050978](https://doi.org/10.5281/zenodo.22050978)

This page is the single dignified public index for what stands, what is archived, and how corrections are presented on Zenodo.

---

## Presentation rule (non-negotiable)

| Layer | What belongs there |
| --- | --- |
| **Title** | Clean scholarly title only — no `ERRATA`, `WITHDRAWN`, `SUPERSEDED`, or `see errata` banners |
| **Abstract / PDF** | Corrected content for KEEP records; original dated files for archive records |
| **Description (underneath)** | Correction notice: what changed, what is withdrawn, link to this index |

Banners in titles were a presentation mistake. They are being removed; the correction text moves to the description.

---

## What stands (KEEP — cite these)

| Work | DOI | Notes |
| --- | --- | --- |
| **Möbius–GCD Q6 v2.1** (inverse-GCD operator) | [10.5281/zenodo.22050962](https://doi.org/10.5281/zenodo.22050962) | Definitions, Bridge\* single-pair bound, floor withdrawals. **No RH claim. No NS claim. No Goldbach claim.** |
| **Φ-renorm swirl algebra** (long) | [10.5281/zenodo.22050974](https://doi.org/10.5281/zenodo.22050974) | Algebraic cancel for axisymmetric swirl; Q₁-augmented framing |
| **Φ-renorm swirl algebra** (short concept) | [10.5281/zenodo.22050975](https://doi.org/10.5281/zenodo.22050975) | Companion to 22050974 |
| **Ring Lemma + SND conditional** | [10.5281/zenodo.22050976](https://doi.org/10.5281/zenodo.22050976) | Unaugmented NS + SND **hypothesis** framing; conditional only |
| **T2 under SND** | [10.5281/zenodo.22050965](https://doi.org/10.5281/zenodo.22050965) | Shell-flux Gronwall conditional on SND |
| **Route C exploratory** | [10.5281/zenodo.22050963](https://doi.org/10.5281/zenodo.22050963) | Conditional on two analytic gaps; **RH not proved** |
| **Domain Architect / FRA** | *(repo only)* | `domain_architect/` + `docs/domain-architect/` — model auditing; canonical SFE **unresolved** |
| **This index** | [10.5281/zenodo.22050978](https://doi.org/10.5281/zenodo.22050978) | What stands vs withdrawn |

---

## Parked / archive (history only — do not cite as proof)

Keep files for timestamp history. Titles restored to original scholarly form; withdrawal explained in description.

| Topic | DOI | Why archived |
| --- | --- | --- |
| Clay Statement (B) / global regularity packaging | [10.5281/zenodo.20405526](https://doi.org/10.5281/zenodo.20405526) | Unconditional NS not proved |
| Quantum Lens Millennium connector | [10.5281/zenodo.20269843](https://doi.org/10.5281/zenodo.20269843) | Millennium-from-SFE glue retired |
| Q6 Goldbach dark-state packaging | [10.5281/zenodo.20405589](https://doi.org/10.5281/zenodo.20405589) | Superseded by [22050962](https://doi.org/10.5281/zenodo.22050962) |
| Montgomery–Dyson “resolved via Q6” | [10.5281/zenodo.20405593](https://doi.org/10.5281/zenodo.20405593) | Exploratory only |
| Three-in-one / Prime Manifold Hamiltonian | [10.5281/zenodo.20552171](https://doi.org/10.5281/zenodo.20552171) | Millennium-from-SFE retired |
| **Triple Lock** SND ≡ GNC ≡ Bridge | [10.5281/zenodo.20552400](https://doi.org/10.5281/zenodo.20552400) | Identity / floor claims withdrawn |
| SND ⇒ global NS (May packaging) | [10.5281/zenodo.20272545](https://doi.org/10.5281/zenodo.20272545) | See [22050976](https://doi.org/10.5281/zenodo.22050976) |
| Early Ring Lemma deposits | [19842060](https://doi.org/10.5281/zenodo.19842060), [20405585](https://doi.org/10.5281/zenodo.20405585) | See [22050976](https://doi.org/10.5281/zenodo.22050976) |
| Older SND framework | [10.5281/zenodo.20518057](https://doi.org/10.5281/zenodo.20518057) | See [22050976](https://doi.org/10.5281/zenodo.22050976) |

### Explicitly withdrawn claim families

- **RH:** not proved (Route C remains conditional; Q6 has no RH claim).
- **Bridge / Triple Lock** as unconditional equivalence.
- **ARCHON RH proved** packaging.
- **SFE → NS / RH** glue and Millennium-from-SFE narratives.
- **Full-spectrum λ_min(Q_N) > −1/2** on named inverse-GCD matrices.

---

## Urgent title fixes (errata banner → description)

These records currently have **banners in the title** on Zenodo. Remediation:

1. Remove `[Claim withdrawn - see errata]` or `[Superseded - see errata]` from the title.
2. Restore the clean title from the table above.
3. Append the correction block from `docs/zenodo/deposits/<slug>.md` to the description.

| Record ID | Clean title starts with… |
| --- | --- |
| 20405526 | Global Regularity of the Navier-Stokes Equations on T3… |
| 20269843 | The Quantum Lens: A Spectral Framework… |
| 20405593 | The Montgomery–Dyson Coincidence… |
| 20552171 | A Quantum Field Theory on the Prime Manifold… |
| 20552400 | A Universal Non-Concentration Principle: SND ≡ GNC ≡ Bridge |
| 20272545 | Spectral Non-Concentration Implies Global Regularity… |
| 19842060 | Borromean Triads, the Ring Lemma, and Spectral Non-Dispersal |
| 20405585 | Borromean Triads, the Ring Lemma, and Spectral Non-Dispersal: A Conditional… |

Run `python3 scripts/zenodo_metadata_remediation.py manual-instructions` for paste-ready blocks.

---

## Contact

Jonathan Robert Simons — simonsmedicalinnovations@gmail.com
