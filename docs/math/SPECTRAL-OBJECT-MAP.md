# Spectral object map (from Zenodo mirror)

Quick answers after pulling the Zenodo spectral stack into `docs/papers/zenodo-spectral/`.

## Notation hygiene (do not conflate)

| Symbol | Domain | What it is | Clay / NS impact alone |
|--------|--------|------------|------------------------|
| Raw \(Q_M\) | Arithmetic | \(Q_{ij}=1/\gcd(i,j)\) | None; full \(\lambda_{\min}>-1/2\) **false** |
| \(\widetilde Q_M\) | Arithmetic | \(1/(\gcd\sqrt{ij})\) | None; full floor **false**; shell blocks are Route N LEAD |
| \(H_N\) / \(H_M\) | Arithmetic | Degree-normalized \(\widetilde Q\) | None without a PDE map |
| \(B_{M,j}\) | Arithmetic (Route N) | Shell-blocked Hermitian (probe: principal submatrix of \(\widetilde Q\) or \(H\) on dyadic index shell) | Auxiliary only |
| \(H_M[a]\) | Arithmetic (Route N) | Convex combo \(\sum a_j B_{M,j}\) | **≠** fluids Theorem H |
| Theorem H | Fluids | SND-C / shell flux under \(X\le M\) | Conditional; **≠** unconditional SND |
| Ring Lemma | Fluids | Band-limited \(\|\nabla(\omega/|\omega|)\|_{L^\infty(E_c)}\le C\,2^{j^*}\) | Toolkit; Statement (B) not proved |

See `docs/math/NS-EXTRACTION-LEDGER.md` (Route N) and `docs/math/TAO-MATH-PANEL-SND-H.md` (H vs \(H_N\)).

## Dominant shell ≠ Q6

**Dominant shell** \(j^* = \arg\max_j X_j\), \(J = \max_j X_j\) — a Littlewood–Paley fact about where enstrophy sits.

**Q6** \(\mathcal{Q}_6\) — inverse-GCD / prime-lattice **damping operator** used in some drafts to argue the concentrated regime cannot persist.

They interact in the story (“Q6 damps the dominant shell”), but they are not the same definition.

## SND vs equidistribution

**SND** (fluids): \(\inf_t J/X \ge c_*>0\).

**Equidistribution** in this stack: mostly Möbius / coprime-subspace delocalization (Route C, Quantum Lens) — arithmetic tool toward Bridge/RH, not a rename of the dominant shell.

## Papers that define each

| Object | Best local source |
| --- | --- |
| Dominant shell + SND | `zenodo-spectral/20518057/98d1b1cc9_NS_UPLOAD_ZENODO.tex` |
| Q6 coercive / damper | same file §Q6; also `20405589`, `20405593` |
| Equidistribution (μ / Route C) | `20518388/d8fcfda3f_RouteC_fresh.tex`, `20269842/e39ad1642_QUANTUM_MILLENNIUM.tex` |
| SND ≡ GNC ≡ Bridge slogan | `20552400/SND_GNC_BRIDGE_UNIFIED.pdf` (audited elsewhere — full-spectrum floor false) |

Full catalog: `docs/papers/zenodo-spectral/README.md`.
