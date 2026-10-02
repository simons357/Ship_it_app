# Square-root estimate — small-case board (sharpness)

**Estimate (finite \(C\) proved, 2 Oct 2026):**

\[
|T_c|
\le
C\,\|\nabla u\|_3\sqrt{Y\,D_s},
\qquad
C=(7+6M_{\mathrm{mult}})C_s.
\]

Derivation: [`SMOOTH-SPLIT-CENTERED-CONSTANT.md`](./SMOOTH-SPLIT-CENTERED-CONSTANT.md).

**Honesty lock.** This board verifies Fourier identities and records certified quotient intervals. It does **not** evaluate \(C_s\) or \(M_{\mathrm{mult}}\), does **not** pay the cutoff-uniform time budget, and does **not** prove Navier–Stokes regularity. A prior exact witness \(C>0.4\) remains a necessary lower bound; no optimized decimal \(C\) is claimed here.

Code: `scripts/ns_attacks/exact_fourier.py`, `scripts/ns_attacks/sqrt_estimate_attack.py`, `scripts/ns_attacks/six_mode_family.py`.  
Tests: `tests/test_sqrt_estimate_attack.py`, `tests/test_smooth_split_constant.py`.

---

## What a green run certifies

| Object | How | Status |
| --- | --- | --- |
| \(Y,D_s,T_c=M-\Lambda N,\sum T_k=0\) | exact \(Q(i)\) Fourier arithmetic | **identity** |
| \(\widehat{|\nabla u|^2}(0)=X\) | exact convolution | **identity** |
| \(\|\nabla u\|_3\) interval | \(L^2\) lower / Riesz–Thorin \(L^4\) upper | **bounds** |
| Quotient interval for sharpness | \(Q_{\mathrm{lb}}\) uses the \(L^3\) upper bound | **interval** |
| Existence of finite \(C\) | smooth-split theorem | **proved** (not by this board) |
| Time budget / \(\int g^2\) | — | **OPEN** |
| Global NSE regularity | — | **NOT established** |

Sampled physical-space quadrature is not used for \(\|\nabla u\|_3\).

---

## Near-shell obstruction (why \(\sqrt{D_s}\))

On a main shell plus satellite amplitude \(\varepsilon\),

\[
T_c\sim\varepsilon,\qquad D_s\sim\varepsilon^2,
\]

so \(T_c/D_s\) blows up while \(T_c/\sqrt{D_s}\) stays ordered. That kills a linear-in-\(D_s\) same-time bound. The smooth split is what upgrades the motivation into a finite-\(C\) estimate.

---

## Families (sharpness, not existence)

1. Nearly single-shell states with several interacting triads (shell 5 → 10).
2. Widely separated frequencies with varied amplitudes (shells 1–2 vs 36–72).
3. Dense packets with coordinated phases (common-phase box; P/Q affine packet).
4. DA six-mode family \(p=(1,0,0)\), \(q=(j,j,0)\), \(k=p+q\): \(N=-2(2j+1)\), \(D_s/(\Lambda Y)\sim 1/(4j)\), normalized \(\Lambda N\) quotient decreases with \(j\).

Finite certified \(Q_{\mathrm{lb}}\) on this board is compatible with the theorem. It is not a kill and not an optimized \(C\).

---

## Runtime

```bash
python3 scripts/ns_attacks/sqrt_estimate_attack.py
python3 scripts/ns_attacks/smooth_split_board.py
python3 -m unittest tests.test_sqrt_estimate_attack tests.test_smooth_split_constant -v
```

---

## Do not glue

- Φ-renorm swirl algebra is a different book.
- Lemma★ shape form \(\mathcal{R}_\star=(T_c)_+^2/(D_s\,E\,Y)\) is a different quotient.
- Clay Statement B remains open.
