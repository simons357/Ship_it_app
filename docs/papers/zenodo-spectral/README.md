# Zenodo spectral stack — local mirror + glossary

**Pulled:** 2026-08-15  
**Path:** `docs/papers/zenodo-spectral/`  
**Machine index:** `INDEX.json`, per-record folders `/{record_id}/`

This is every Jonathan R. Simons spectral / SND / Ring / Q6 / Bridge record we could resolve on Zenodo by DOI + title search. Concept duplicates (e.g. `20518056`→`20518057`) collapse to the latest version file.

---

## Catalog (unique DOIs, chronological)

| Date | DOI | Title (short) | Local files |
| --- | ---: | --- | --- |
| 2026-04-28 | [19842060](https://doi.org/10.5281/zenodo.19842060) | Borromean Triads, Ring Lemma, SND | `19842060/*.pdf,png` |
| 2026-05-18 | [20269843](https://doi.org/10.5281/zenodo.20269843) | Quantum Lens (Millennium spectral framework) | `20269842/*.tex` |
| 2026-05-18 | [20272545](https://doi.org/10.5281/zenodo.20272545) | Spectral Non-Concentration ⇒ NS regularity (Paper 2) | `20272545/*.pdf` |
| 2026-05-27 | [20405405](https://doi.org/10.5281/zenodo.20405405) | Phi-Renormalization Track B | `20405404/*.pdf` |
| 2026-05-27 | [20405526](https://doi.org/10.5281/zenodo.20405526) | Global Regularity on T³ (claims Statement B) | `20405526/*.{tex,html}` |
| 2026-05-27 | [20405585](https://doi.org/10.5281/zenodo.20405585) | Ring Lemma + Borromean conditional framework | `20405585/*.{tex,html}` |
| 2026-05-27 | [20405589](https://doi.org/10.5281/zenodo.20405589) | Q6 spectral route to Strong Goldbach | `20405589/*.tex` |
| 2026-05-27 | [20405593](https://doi.org/10.5281/zenodo.20405593) | Montgomery–Dyson as Q6 eigenvalue identity | `20405593/*.tex` |
| 2026-05-27 | [20405597](https://doi.org/10.5281/zenodo.20405597) | Phi-Renorm axisymmetric short note | `20405597/*.tex` |
| 2026-06-03 | [20518057](https://doi.org/10.5281/zenodo.20518057) | SND + Ring Lemma **conditional** NS framework | `20518057/*.tex` |
| 2026-06-03 | [20518388](https://doi.org/10.5281/zenodo.20518388) | Route C (RH; equidistribution / two gaps) | `20518388/*.tex` |
| 2026-06-05 | [20552080](https://doi.org/10.5281/zenodo.20552080) | T2 Gronwall / SND conditional + GNC bridge | `20552080/*.{tex,pdf}` |
| 2026-06-05 | [20552171](https://doi.org/10.5281/zenodo.20552171) | Three-in-one Quantum Millennium | `20552171/*.{tex,pdf}` |
| 2026-06-05 | [20552400](https://doi.org/10.5281/zenodo.20552400) | SND ≡ GNC ≡ Bridge Triple Lock | `20552400/*.pdf` |

**Not found on Zenodo under these names:** `NS_FINAL_MERGED_UNCONDITIONAL.tex`, `NS_PROOF_CHAIN.html` (June 10 merge). Still Drive-only if it exists.

---

## Glossary — your question: is “dominant shell” Q6?

**No. Different objects.**

| Term | What it is | Where it lives |
| --- | --- | --- |
| **Dominant shell** \(j^*\) | The Littlewood–Paley shell that currently holds the most enstrophy: \(j^*=\arg\max_j X_j\), \(J=\max_j X_j\) | Fluids / NS papers (`20518057`, Ring Lemma, Global Regularity) |
| **SND** | Spectral Non-Dispersal: \(\inf_t J(t)/X(t)\ge c_*>0\) — a **positive fraction** of enstrophy stays in some dominant shell (does not fully disperse across all scales) | Same NS stack; also “Non-Concentration” wording in Paper 2 / Goldbach isomorphism |
| **\(\mathcal{Q}_6\) / Q6** | **Prime spectral damper** — a coupling / damping operator built from \(1/\gcd(i,j)\) (or related inverse-GCD weights) that preferentially damps modes according to coprimality on the prime lattice | NS papers as an *extra* damping term in concentrated regime; Goldbach/RH papers as arithmetic Hamiltonian |
| **Equidistribution** | Mostly **Möbius / arithmetic equidistribution** (Bombieri–Vinogradov, Anderson delocalization of coprime subspace) used as a *strategy* toward Bridge / Route C — **not** the same as “dominant shell” | Route C (`20518388`), Quantum Lens (`20269843`), three-in-one |
| **GNC** | Goldbach Non-Concentration — arithmetic twin of SND on Goldbach test vectors | `20405589`, Triple Lock, T2 |
| **Bridge** | Shared spectral-floor slogan \(\lambda_{\min}>-1/2\) (full-spectrum version later audited as false for named matrices) | Triple Lock / three-in-one |

### One-sentence map

- **Dominant shell** = *which frequency band is loudest right now* (LP geometry).  
- **SND** = *that loudest band never becomes negligible as a fraction of total enstrophy*.  
- **Q6** = *an operator that tries to damp / couple shells using gcd weights* — a proposed *mechanism*, not the definition of the dominant shell.  
- **Equidistribution** = *arithmetic delocalization strategy* (μ / coprime subspace), mainly on the RH/Bridge side.

So: if you “have SND and equidistribution,” that does **not** automatically answer Tao’s dominant-shell propagation question unless a paper proves that \(j^*(t)\) and \(J/X\) stay controlled for all time under the true NS flow (without circular \(X\le M\)). Q6 is the tool some drafts use to *argue* concentration cannot persist — it is not itself the dominant-shell condition.

---

## Reproduce / extend the mirror

```bash
# already downloaded under docs/papers/zenodo-spectral/
python3 -c "import json; print(len(json.load(open('docs/papers/zenodo-spectral/INDEX.json'))))"
```

If you have newer Zenodo DOIs (post–June 5) or the June 10 merge, drop them here and this index will be extended.
