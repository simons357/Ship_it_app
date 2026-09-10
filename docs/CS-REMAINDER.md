# Localized ABC — DISPUTED. DA REJECT. ★ still OPEN.

10 September 2026. **NS not solved.** Lemma★ is still open.
This is a table, not a stamp.

The prior Target A / “★ killed” language on this branch
is walked back. DA’s live lock keeps
\(\sup\mathcal R_\star<\infty\) **OPEN**
(`docs/ns-review/PROOF_LemmaStar_LIVE_LOCK.md` on PR 60).
The evaluator lock stands: exact triad sum is not a proof.

## Against DA REJECT

Exact ABC is Beltrami: \(B(\mathrm{ABC},\mathrm{ABC})=0\),
so \(T_c=0\). The field on this branch is a reconstruction

\[
v_\lambda
=
-
\frac{P(\gamma_\lambda\,\mathrm{ABC}_\lambda)}
{\|P(\gamma_\lambda\,\mathrm{ABC}_\lambda)\|_2},
\qquad
\widehat{\gamma}_\lambda(k)=\exp(-|k|^2/(2\lambda^2)).
\]

That is cutoff plus Leray, not ABC. DA rejects that recon
as a kill of the uniform bound.

`cs_remainder_exact_check.py` sits as a checker, not a close.

| Check | What this branch has | Against the reject |
|---|---|---|
| Requested frame \(\lambda=2,4,8,16\) | Not run | Missing \(\lambda=16\). Exact core never ran 8 or 16. |
| FFT Galerkin (all modes) | \(\lambda=2,3,4,5,6,8\) | Extra 3,5,6. Not the requested set. |
| Exact triad core | \(\lambda=2,3,4\) on a **99% energy cutoff** | Different field from the full FFT. \(T_c\) differs \(\sim 50\)–\(56\%\). |
| Same truncated field | FFT \(T_c\) = triad sum to \(10^{-13}\) | Convention sits. Does not make the cutoff into ABC. |
| Fourier dilation \(v(n\cdot)\) | \(\mathcal R_\star\) invariant (rel \(=0\)) | The boxed family is invariant. Spatial concentration is a different scaling. |
| Exact ABC | Not computed here | \(B=0\). A climb on \(P(\gamma_\lambda\mathrm{ABC}_\lambda)\) is the recon. |

N-shell samples still saturate. That table stands.
H1 is a different integral.

## Requested frame \(\lambda=2,4,8,16\)

Not on disk. Closest FFT rows (signed \(\mathcal R_\star\),
\(T_c<0\) then reverse):

| \(\lambda\) | \(\|A^{1/2}B\|_2/\sqrt{EY}\) | signed \(\mathcal R_\star\) |
|---|---|---|
| 2 | 2.492 | 0.00517 |
| 4 | 7.104 | 0.0409 |
| 8 | 20.114 | 0.327 |
| 16 | — | not run |

## Exact-core table (99% energy cutoff)

Direct pair sum on the exported modes. Reverse so \(T_c>0\).
These are **not** the full FFT fields.

| \(\lambda\) | modes | exact \(\mathcal R_\star\) | FFT \(\mathcal R_\star\) (same \(\lambda\), full field) | \(T_c\) rel. gap |
|---|---|---|---|---|
| 2 | 836 | 0.001748 | 0.00517 | 0.535 |
| 3 | 2820 | 0.005181 | 0.0173 | 0.565 |
| 4 | 6672 | 0.013669 | 0.0409 | 0.542 |
| 8 | — | not run | 0.327 | — |
| 16 | — | not run | — | — |

The first table compared a full FFT field to a 99% cutoff.
Those are different fields. \(T_c\) lives in the tail.
That gap is not a convention bug. It is why the recon
does not sit as a continuum family.

Checked against the exact triad core before any stamp.
Locks that sit (not a kill):

- Fast triad \(T_c\) matches `stokes_moments.probe` on a three-mode field.
- Same truncated export: FFT \(T_c\) equals the triad sum to \(10^{-13}\).
- Fourier dilation \(v(n\cdot)\) leaves that cutoff \(\mathcal R_\star\) invariant.

Do not cash 0.327, 0.0137, or a \(\lambda^3\) fit as \(C_0\).
Do not restamp Target A false from this family.

Script: `scripts/ns_attacks/cs_remainder_exact_check.py`
JSON: `results/cs_remainder_bump/exact_core_check.json`
FFT table: `results/cs_remainder_bump/cs_remainder.json`

Stay in this chat.
