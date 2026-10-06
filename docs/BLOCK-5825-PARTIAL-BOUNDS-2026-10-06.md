# Stronger partial bounds for the fixed blocks \((5,8,25)\) and \((5,10,25)\)

6 October 2026.
**Author correction to the Cursor one-block / \(\mathcal Q^{\mathrm{other}}\) write-ups.
Partial result. Not (17). NS not solved.**

Author packet (ready on author side; **not** on PR #165
until explicitly authorized):
`Block-5825-Review.pdf`, `Block-5825-Review-Package.zip`.
First audit target inside the packet: (Q⋆)
\(\lvert\mathcal Q\rvert\le D\beta\,E\,X_{\mathrm{block}}\) —
[`Q-BOUND-REVIEW-TARGET.md`](Q-BOUND-REVIEW-TARGET.md).

Parents corrected:
[`BLOCK-5825-FIRST-ATTEMPT-2026-10-06.md`](BLOCK-5825-FIRST-ATTEMPT-2026-10-06.md),
[`Q-OTHER-51025-2026-10-06.md`](Q-OTHER-51025-2026-10-06.md).

---

## RESULT

The claim that outside forcing defeats an energy-only estimate
is **too strong for this fixed block**. Including every outside
input, the complete signed transfer of \((5,8,25)\) obeys

\[
\boxed{
\int_0^T\lvert\mathcal T_{5825}(t)\rvert\,dt
\le
\frac{\lvert\mathcal T_{5825}(0)\rvert}{38\nu}
+0.275533\,\frac{E_0^2}{\nu^2}.
}
\tag{P1}
\]

Here \(E_0=\lVert u_0\rVert_2^2\). The initial-transfer term
vanishes for the regenerated \(K=2\) witness
(\(\mathcal T_{5825}(0)=0\)). The bound uses the existing
energy budget — **no future smoothness** assumption.

Frequency test on complete shells scaled by \(n\), including
their additional lattice directions: the two jet blocks satisfy

\[
\boxed{
\lvert\mathcal T_{5825,n}\rvert+\lvert\mathcal T_{51025,n}\rvert
\le
0.375329\,\frac{\sqrt{E_0}}{n}\,Y_{S_4,n}.
}
\tag{P2}
\]

Both fit below the viscous allowance once

\[
\boxed{
n\ge 1.501315\,\frac{\sqrt{E_0}}{\nu}.
}
\tag{P3}
\]

In plain English: these two particular interaction shapes
become **easier** for viscosity to control at higher frequency.
Outside feeding does **not** invalidate that estimate.

A normalized time-budget bound for the fixed pair that covers
**repeated episodes** is also derived in the author review
packet.

**Remaining obstacle toward (17):** assembling **all** scalene
triangle shapes in frequency space without repeatedly
spending the same Fourier-shell energy allowance
(exact \(\lvert k\rvert^2\) sets — not physical shells).
That remains **OPEN**.
See [`ALL-SHAPE-SHELL-POT-BLANK.md`](ALL-SHAPE-SHELL-POT-BLANK.md).

Exact checks passed for the signed receiver sum and full-forcing
evolution (author packet).

---

## 1. What was overclaimed

Prior Cursor notes said external / outside-high forcing
(\(\mathcal Q^{\mathrm{other}}\), \(\mathcal Q^{\infty}\))
fails energy-only absorption on this block. That overstates
the obstruction for the **fixed** shapes \((5,8,25)\) and
\((5,10,25)\).

What remains true from those notes:

- Intra-block / joint \(S_4\) forcing is finite and
  dilation-compatible.
- A **crude** \(\lvert\widehat B_k\rvert\le\lvert k\rvert E\)
  majorant before signed assembly is still the wrong tool.
- Closing (17) still requires controlling **all** scalene
  shapes, not just these two.

What is corrected:

- For this fixed block, integrating
  \(\lvert\mathcal T_{5825}\rvert\) against the viscous
  rate \(38\nu\) yields an \(E_0,\nu\)-bound **including
  outside inputs**.
- Frequency scaling improves the viscous margin for these
  two shapes (P2)–(P3).

---

## 2. Scope and tags

| Statement | Tag |
|---|---|
| (P1) for fixed \((5,8,25)\), all outside inputs | **CLAIMED** (author analytic; exact checks for receiver sum / full-forcing evolution) |
| (P2)–(P3) for \(n\)-scaled complete shells of the two blocks | **CLAIMED** (author analytic) |
| Normalized time budget for the fixed pair, repeated episodes | **CLAIMED** in author PDF (file into vault with the ZIP) |
| Constants \(0.275533\), \(0.375329\), \(1.501315\) | Numerical faces of exact constants in the review proofs — prefer exact forms from the PDF when filing the full write |
| Threshold factor four in (P2)–(P3) | **By author definition** (threshold = \(4\times\) transfer-bound constant / \(\nu Y/4\) share) — verify from exact packet expressions, not float \(\beta/\alpha\) |
| (Q⋆) \(\lvert Q\rvert\le D\beta\,E\,X_{\mathrm{block}}\) | **CLAIMED** in packet; first independent audit target |
| (17) for all scalene shapes | **OPEN** |
| Global regularity / Clay | **NOT CLAIMED** |
| PDF/ZIP on PR #165 | **AWAITING EXPLICIT AUTHORIZATION** |

Independent review of the analytic proofs in
`Block-5825-Review.pdf` remains appropriate. This page
records the correction and the boxed partial results for
the PR #165 chain.

Truth-run delimitation (Duhamel vs \(Q\)-step; budget
integrand; SCHEME A failure):
[`TRUTH-RUN-CAVEATS.md`](TRUTH-RUN-CAVEATS.md).

---

## 3. Consequence for the next attack

1. Do not restart “outside feeding kills energy-only” for
   these two fixed shapes — (P1)–(P3) contradict that.
2. Plow **assembly of all scalene shapes** with a bookkeeping
   scheme that does not charge the same shell energies once
   per shape (double-counting / repeated charging is the
   named blank).
3. Keep the shear filter and the all-high \(t^6\) jet as
   witnesses; they are compatible with (P1) on the
   regenerated datum (\(\mathcal T_{5825}(0)=0\)).

---

## STATUS

FIXED-BLOCK OUTSIDE FEEDING: ENERGY-ONLY TIME BOUND (P1) CLAIMED.
FREQUENCY TEST (P2)–(P3): SURVIVES; HIGHER \(n\) HELPS VISCOSITY.
REPEATED EPISODES ON THE FIXED PAIR: COVERED IN AUTHOR PACKET.
ALL-SHAPE ASSEMBLY WITHOUT REPEATED SHELL CHARGING: OPEN → (17).
PRIOR “OUTSIDE DEFEATS ENERGY-ONLY” FOR THIS BLOCK: WITHDRAWN AS TOO STRONG.
NS NOT SOLVED.
