# Issues sheet — every leftover that still needs an estimate

12 September 2026.
**One page. Send this.**
https://github.com/simons357/Ship_it_app/blob/cursor/unaugmented-r4-vorticity-f80e/docs/ISSUES-SHEET.md

Math for 1–5: [`HELP-OFF-DESK.md`](HELP-OFF-DESK.md).
Filter: [`ESTIMATE-AUDIT.md`](ESTIMATE-AUDIT.md).
Yes / no / open (the tape):
[`YES-NO-OPEN.md`](YES-NO-OPEN.md).
Borrowed systems (maps only; not a close):
[`FRAMEWORK-MAP.md`](FRAMEWORK-MAP.md).
B-hand five-finger map (not a leftover):
[`DA-NS-FIVE-FINGER.md`](DA-NS-FIVE-FINGER.md).
Cosmo / SM fingers stay the other book.
Living line: GitHub PR 24,
branch `cursor/unaugmented-r4-vorticity-f80e`.
Operator: Jonathan Robert Simons
(Prime Field Technologies).

Ordinary Navier–Stokes is not solved.
The Riemann hypothesis is not solved.
Do not retitle any row below as a close.

Catalog B open count is 1 (`B_regularity`).
That is ordinary NS. It is row 1 or 4 or 5,
not a thirteenth NS leftover.

---

## A. Open — need an estimate or a named kill

One person, one row. Do not glue 1, 4, and 5.

| # | Issue | Object | What would close it | File |
|---|---|---|---|---|
| 1 | H1 = WRITE (6) | Bad-pair stretching \(A_{\mathrm{bad}}\) on the cylinder \(Q_r\) | Prove thinness, or \(J\) on folds, or dynamics on \(r^2/\nu\); or write a named kill of those shapes. Not another *if*. | `docs/H1-WRITE.md`, `docs/WRITE_6.md`, `docs/H1-OBJECT.md` |
| 2 | H2 from energy | Flux \(r^{-1}\iint|u||\omega|^2\) on the same cylinder | A priori from energy, or keep CKN-smallness and say so. CKN-small already sits. | `docs/H-SYSTEM.md` |
| 3 | H3 | Exterior Biot–Savart on the same cylinder | Absorb as \(r\to 0\). Written, not absorbed. | `docs/H-SYSTEM.md` |
| 4 | Replacement energy-budget closure (Lemma★ box killed) | A different estimate that the growing-layer family \(v_n\) does not kill | Write that estimate, or drop the energy-budget path. Unrestricted \(\sup\mathcal R_\star<\infty\) is **KILLED**. Need★ cannot repair that box. | `docs/LEMMA-STAR-GROWING-LAYER.md`, `docs/LEMMA-STAR-STATEMENT.md`, `docs/NEED-STAR-HH-L-DUAL.md` |
| 4a | Hyp-Lat★ | Lattice transfer X1–X4/X6 of the continuum incidence \(I\ll m^{4/3}\) | Write the transfer, or drop the incidence route. Continuum \(m^{4/3}\) is not a lattice theorem. | `docs/LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md` |
| 5 | Axisymmetric remainder | \(\int\rho_j=\int(T_{j\leftarrow j})_+/Z_j\) on unaugmented axisymmetric-with-swirl \(\mathbb{R}^3\) | A class bound, or a field in the class with \(\int\rho_j=\infty\). Occupancy \(55/56\) already printed; it did not decay. | `docs/AXISYM-SHELL.md`, `docs/AXISYM-SWIRL-PROBE.md` |
| 6 | RH WRITE (6) | Every non-trivial zero of \(\zeta\) on \(\operatorname{Re}s=1/2\) | One estimate that forces the line. Q is not it. | `docs/RH-CHAIN.md` |
| 7 | Uniform \(H^1\) as \(\varepsilon\to 0\) | Track A extra-stress NS | A bound independent of \(\varepsilon\). **Not required** for Theorem A to stay finished. A is not B. | `docs/A-CHAIN.md` |
| 8 | Goldbach’s conjecture | Every even integer \(\ge 4\) is a sum of two primes | That statement. The matrix corollary \(R\ge -2/9\) already sits and is not this. | `docs/GOLDBACH-CHAIN.md` |
| 9 | Yang–Mills mass gap | Spectrum of 4-D quantum YM on the vacuum-orthogonal subspace bounded below by a positive constant | That gap. The SM kinetic term is not it. | `docs/YM-PROOF-CHAIN.md` |
| 10 | BSD | For every \(E/\mathbb{Q}\): algebraic rank = analytic rank, \(\Sha\) finite, leading term | That identity for every curve. Zenodo 20552682 is Q as a prototype, not BSD. | `docs/BSD-PROOF-CHAIN.md` |
| 11 | Hodge | Every rational Hodge class on a smooth complex projective variety is algebraic | That for every such \(X\). No Hodge paper sits here. | `docs/HODGE-PROOF-CHAIN.md` |
| 12 | P vs NP | A Turing-machine proof that \(\mathrm{P}=\mathrm{NP}\) or \(\mathrm{P}\neq\mathrm{NP}\) | That proof in the TM model. SFE is not the model. | `docs/PNP-PROOF-CHAIN.md` |

A cylinder (ordinary NS, geometric path) closes only if
C+\(R_\phi\), **1**, **2** (or CKN-small), and **3** all sit.
Then local Serrin, not CKN. Lemma C is an *if*, not an H.
Global parent stretching **H** is open and is not a
cylinder. \(R_\phi\) is not free.

Do not start 1 from ABC_λ. Do not cash \(0.641\),
\(0.610\), \(0.327\), or three-shear \(2/3\) as the
\(v_n\) kill or as \(16/9\).
The named kill of unrestricted ★ already sits. Do not
restore occupation decay from the wall detector
as a close of 5. Do not retitle Q as 6 or 10.
Evolution / biology / other systems are maps
onto a named row, or they stop. They do not
move a row. [`FRAMEWORK-MAP.md`](FRAMEWORK-MAP.md).

---

## B. Already sit — do not redo

| Item | What it is | Send as |
|---|---|---|
| Theorem A | Extra-stress / \(Q_1\)-NS, \(\varepsilon>0\), \(\beta\ge 1/2\) | This PDE only. Known class. Not ordinary NS. |
| Q / 22045478 | Inverse-GCD: Bridge*, Theorem P, \(H_N\ge -1\), nonnegative form | August GCD paper. Not RH. Not BSD. |
| Goldbach-shaped | \(R\ge -2/9\) if that prime-difference vector is nonzero | Matrix corollary. Not row 8. |
| Poincaré | Perelman | Literature reprint. Not ours as a proof. |
| Lemma C | Good-pair alignment *if* | Their theorem as an *if*. |
| P1 / P1-loc / PC | Low-pass, cutoff, one-path cost | Sit. None is H1. |
| Far-shell Young | Axisymmetric \(T_{j\leftarrow\mathrm{IR}}\), \(T_{j\leftarrow\mathrm{UV}}\) | Sit. Remainder is still row 5. |
| Good-set | supplied estimate | **Fixed.** Do not rewrite. |

---

## C. Dead or withdrawn — do not rebuild

| Item | Status |
|---|---|
| \(K=0\) | Dead. Amplitude kills it. |
| \(\lvert T_c\rvert\le C\|u\|_2 X^{3/2}\) | Dead. Scaling \(a^3\) vs \(a^4\). |
| Uniform pre-Young \(C\) | Dead. |
| Attack 9D designed \(\Theta(m^2)\) | Freiman-AP. **Dead.** Do not start 9D. Setup: `docs/ATTACK-9D-SETUP.md`. Same \(B\) as 9B. Grow-\(s\) samples are historical. |
| Unrestricted \(\sup\mathcal R_\star<\infty\) | **Killed** by the growing-layer family \(v_n\). `docs/LEMMA-STAR-GROWING-LAYER.md`. Not a singular NSE solution. |
| Fixed-output \(\Theta(m^2)\) | Counting error. \(K\le 16s\). |
| Detector occupation | 5-D occupation from the swirl wall. **Withdrawn.** |
| Full Q floor \(>-1/2\), \(H_N\ge -3/14\) | Taken back. Stay back. |
| \(\Phi\)-cancel as ordinary NS | Dropped. |
| HB as a unifier | Thrown out. |
| SFE / UHF / DHFA as constitutive NS | Shelved. |
| Ring Lemma \(\|\nabla\xi\|_{L^\infty(E_c)}\le C\,2^{j^*}\) | **REPAIR.** Do not quote as proved. |

---

## D. What Monday can close without closing A

Operator page (cover paste, file list):
[`MONDAY-PACKET.md`](MONDAY-PACKET.md).
These clear the *pile*. They do not close rows 1–12.

1. Zenodo the swirl paper as a **map**.
   Paste: [`SWIRL-DEPOSIT.md`](SWIRL-DEPOSIT.md).
   PDF: `docs/SWIRL-PAPER.pdf`.
2. Theorem A, honest title, class credited.
   `docs/THEOREM-A-Q1.pdf`.
3. Leave 22045478 as the GCD paper.
4. Send **this sheet** to everyone who worked
   the project. Attach [`HELP-OFF-DESK.md`](HELP-OFF-DESK.md)
   if they are taking a row in 1–5.
5. Tape: “ordinary NS solved” and
   “RH solved” stay false.

**Do not send.** A theft letter. WRITE (6) as a
theorem. Theorem A as unaugmented NS.
Axisymmetric-with-swirl as finished.
A cold letter as a close. Attack 9D as live.

---

## E. Attachments if they take a row

- This sheet.
- [`HELP-OFF-DESK.md`](HELP-OFF-DESK.md) (rows 1–5).
- [`WRITE_6.md`](WRITE_6.md).
- [`LEMMA-STAR-STATEMENT.md`](LEMMA-STAR-STATEMENT.md).
- [`AXISYM-SHELL.md`](AXISYM-SHELL.md),
  [`AXISYM-SWIRL-PROBE.md`](AXISYM-SWIRL-PROBE.md),
  [`SWIRL-WALL-CORRECTION.md`](SWIRL-WALL-CORRECTION.md).
- [`ESTIMATE-AUDIT.md`](ESTIMATE-AUDIT.md).
- `docs/SWIRL-PAPER.pdf`, `docs/THEOREM-A-Q1.pdf`.

Do not send the PR 48 SND/SFE pile as this leftover.
Do not overwrite `scripts/ns_attacks/stokes_moments.py`.

NS not solved. RH not solved.
The door is named. The last line is not written.
