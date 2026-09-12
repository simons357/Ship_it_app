# Issues sheet — what still has to be solved

12 September 2026.
**One page. Send this.** Math is in
[`HELP-OFF-DESK.md`](HELP-OFF-DESK.md).
Filter: [`ESTIMATE-AUDIT.md`](ESTIMATE-AUDIT.md).

Ordinary Navier–Stokes is not solved.
The Riemann hypothesis is not solved.
Do not retitle anything below as a close.

Living line: GitHub PR 24,
branch `cursor/unaugmented-r4-vorticity-f80e`.
Operator: Jonathan Robert Simons
(Prime Field Technologies).

---

## Open leftovers (one person, one integral)

| # | Issue | Object | What would close it | Who |
|---|---|---|---|---|
| 1 | H1 = WRITE (6) | Bad-pair stretching \(A_{\mathrm{bad}}\) on the cylinder \(Q_r\) | Prove one of the three shapes (thinness / \(J\) on folds / dynamics on \(r^2/\nu\)), or write a named kill of those shapes. Not another *if*. | Geometric NS / vorticity stretching |
| 2 | Lemma★ | \(\sup\mathcal R_\star<\infty\) on \(\mathbb{T}^3\), \(\mathcal R_\star=(T_c)_+^2/(\mathcal D_s E Y)\) | A geometry-only bound, or a sequence with \(\mathcal R_\star\to\infty\). Lattice transfer X1–X4/X6 still missing. | Fourier / triad NS |
| 3 | Axisymmetric remainder | \(\int\rho_j=\int(T_{j\leftarrow j})_+/Z_j\) on unaugmented axisymmetric-with-swirl \(\mathbb{R}^3\) | A class bound, or a field in the class with \(\int\rho_j=\infty\). Occupancy \(55/56\) already printed; it did not decay. | Axisymmetric NS with swirl |
| 4 | RH WRITE (6) | Every non-trivial zero of \(\zeta\) on \(\operatorname{Re}s=1/2\) | One estimate that forces the line. Q is not it. | Analytic number theory |

Do not glue 1–3. A number on one is not a
bound on the others. Do not start H1 from
ABC_λ. Do not cash \(0.641\), \(0.610\),
or \(0.327\). Do not restore occupation
decay from the wall detector.

---

## Same cylinder, not Job 1

A cylinder closes only if all of these sit.
H1 alone is not enough.

| Letter | Object | Status |
|---|---|---|
| C | Good pairs (alignment *if*) | Theorem as an *if*. Not an H. |
| H1 | Bad pairs | **Open. Job 1.** |
| H2 | Flux \(r^{-1}\iint\|u\|\|\omega\|^2\) | CKN-smallness sits. From energy alone: **open**. |
| H3 | Exterior Biot–Savart | Written. Not absorbed as \(r\to 0\). **Open.** |
| \(R_\phi\) | Cutoff error | Not free. |
| H | Global parent stretching | Open. A cylinder is not this parent. |

Ring Lemma \(\|\nabla\xi\|_{L^\infty(E_c)}\le C\,2^{j^*}\)
is **REPAIR**. Do not quote it as proved.

---

## Already off this desk (do not redo)

| Item | What it is | Send as |
|---|---|---|
| Theorem A | Extra-stress / \(Q_1\)-NS, \(\varepsilon>0\), \(\beta\ge 1/2\) | This PDE only. Known class. Not ordinary NS. Uniform \(H^1\) as \(\varepsilon\to 0\) is extra and still open. |
| Q / 22045478 | Inverse-GCD: Bridge*, Theorem P, \(H_N\ge -1\), nonnegative form | August GCD paper. Not RH. |
| Goldbach-shaped | \(R\ge -2/9\) if that prime-difference vector is nonzero | Matrix corollary. Not Goldbach’s conjecture. |
| Poincaré | Perelman | Literature reprint. Not ours as a proof. |
| Detector occupation | 5-D occupation from the swirl wall | **Withdrawn.** |
| Good-set | supplied estimate | **Fixed.** Do not rewrite. |
| Full Q floor, \(H_N\ge -3/14\), \(\Phi\)-cancel as ordinary NS, HB as unifier | taken back | Stay back. |

---

## Other maps (open; not this week’s four jobs)

YM mass gap, BSD, Hodge, P vs NP: reading
maps only. Missing step stays missing.
Files: `docs/YM-PROOF-CHAIN.md`,
`docs/BSD-PROOF-CHAIN.md`,
`docs/HODGE-PROOF-CHAIN.md`,
`docs/PNP-PROOF-CHAIN.md`.

---

## What Monday can close without a leftover close

These clear the *pile*. They do not close
Jobs 1–4.

1. Zenodo the swirl paper as a **map**.
   Paste: [`SWIRL-DEPOSIT.md`](SWIRL-DEPOSIT.md).
   PDF: `docs/SWIRL-PAPER.pdf`.
2. Theorem A, honest title, class credited.
   `docs/THEOREM-A-Q1.pdf`.
3. Leave 22045478 as the GCD paper.
4. Send this sheet plus
   [`HELP-OFF-DESK.md`](HELP-OFF-DESK.md)
   to everyone who worked the project.
5. Tape: “ordinary NS solved” and
   “RH solved” stay false.

**Do not send.** A theft letter. WRITE (6)
as a theorem. Theorem A as unaugmented NS.
Axisymmetric-with-swirl as finished.
A cold letter as a close.

---

## Attachments

- This sheet.
- [`HELP-OFF-DESK.md`](HELP-OFF-DESK.md)
  (the four integrals, stated).
- [`WRITE_6.md`](WRITE_6.md).
- [`LEMMA-STAR-STATEMENT.md`](LEMMA-STAR-STATEMENT.md).
- [`AXISYM-SHELL.md`](AXISYM-SHELL.md),
  [`AXISYM-SWIRL-PROBE.md`](AXISYM-SWIRL-PROBE.md),
  [`SWIRL-WALL-CORRECTION.md`](SWIRL-WALL-CORRECTION.md).
- [`ESTIMATE-AUDIT.md`](ESTIMATE-AUDIT.md).
- `docs/SWIRL-PAPER.pdf`,
  `docs/THEOREM-A-Q1.pdf`.

Do not send the PR 48 SND/SFE pile as
this leftover. Do not overwrite
`scripts/ns_attacks/stokes_moments.py`.

NS not solved. RH not solved.
The door is named. The last line is not
written.
