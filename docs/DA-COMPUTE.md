# Computing techniques we can borrow

`python3 scripts/da_machine.py compute`

Yes. Some are already running. Some can sit on a slot.
A library is a tool. It does not write \(F\) and it does
not close Track B.

---

## Already wired

| Tool | Slot | What it does | What it cannot |
|---|---|---|---|
| `numpy` FFT + Leray + 2/3 dealias | A | energy residual of \(Q_1\) NS (`augmented_ns_verify.py`) | prove Theorem A; speak B |
| `numpy.linalg` on GCD matrices | Q | Rayleigh / \(\lambda_{\min}\) of \(Q,\widetilde Q,H\) | map onto \((u\cdot\nabla)u\) |
| FFT probes of identities | B | fail B1 if a named field breaks it | regularity |
| arXiv Atom sample | U | refresh now-bench titles | ingest all of science |
| `unittest` | meta | the anti-bullshit device | replace a missing estimate |

`pandas` is only on the **shelved** ringdown script. Do not
grow that.

---

## Legal to borrow (not yet wired)

| Tool | Slot | Job | Killer |
|---|---|---|---|
| `scipy.fft` / pyFFTW | A | same Galerkin, larger \(n\) | energy residual gets worse |
| Dedalus | A (probes on B) | spectral PDE, Fourier / Chebyshev | a smooth run is not a close |
| SymPy | B, U | B1 / B5 / tube Hardy algebra; SM index contractions | identity is not \(I_{\mathrm{tube}}\) |
| LP / Bony from the desk FFT | B | dyadic \(T\) / occupation; a wall-wins field for B4b | domain B stays open |
| LMFDB API, Sage / Pari | Q | L-functions, characters, gcd tables | not QNMs, not NS |
| GWOSC, PDG, DESI public tables | U | refresh catalogs and tensions | not \(F\), not the tube |
| JAX autodiff | A | catch an energy-law coding bug | not Theorem A |

**If you wire one next:** SymPy on B1/B5, or LP/Bony FFT
probes aimed at B4b (a tube family where the wall wins).
That is a check. It is not the estimate.

---

## Do not wire as a close

| Thing | Why |
|---|---|
| “DNS never blew up” | not a bound on \(X\) |
| Kerr QNM solver → B or Q | observation language on U only; do not retune `nodes.json` |
| Cosmo private core | no public equation, no SDK |
| “the model proved it” | generator proposes; checker scores |

---

## Techniques, not brands

These are the methods the desk already speaks, with or
without a new package:

- Fourier–Galerkin + dealias + Leray (A)
- energy-law residual (A)
- Littlewood–Paley dyadic projectors (B)
- Bony paraproduct split (B)
- localized Hardy on a tube (B)
- Rayleigh quotient / Hermitian floor (Q)
- holdout \(\chi^2\) (U; affine \(F\) already lost)
- one sentence, one slot, one killer (meta)

Borrow a package if it computes one of those faster or on
a bigger grid. Do not borrow a story.
