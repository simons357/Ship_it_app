# Truth run on the three caveats

6 October 2026.
**Run to the truth. Not (17). NS not solved.**

Parents:
[`BLOCK-5825-PARTIAL-BOUNDS-2026-10-06.md`](BLOCK-5825-PARTIAL-BOUNDS-2026-10-06.md),
[`ALL-HIGH-T6-K2-DATUM-2026-10-06.md`](ALL-HIGH-T6-K2-DATUM-2026-10-06.md),
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md) (14)–(17).

Checks:
`scripts/ns_attacks/truth_run_caveats.py`
→ `TRUTH-RUN-CAVEATS.json`.

Complementary to the author fixed-pair bounds: keep the
shell-feed breakdown; use this page to mark what is
STANDARD, what is CLAIMED-unchecked, and what is FAILED
as a path to (17).

---

## RESULT

| Caveat | Truth found |
|---|---|
| (1) Verify (P1)–(P3) | Duhamel reduction to \(\int\lvert Q\rvert\) is **STANDARD**. The first unchecked step is the energy-only bound on \(\int\lvert Q_{5825}\rvert\,dt\). Constants not verified (packet absent). (P2)–(P3) faces satisfy \(\beta/\alpha=4\) to float precision — consistent with comparing to \(\nu Y/4\). |
| (2) \(\int\lvert T_{5825}\rvert\) vs budget | **Distinct objects.** On the \(K=2\) jet, \(\mathcal T_{\mathrm{sc}}(h_2)=O(t^6)\) while \(\nu Y/4\to 8\nu>0\), so the budget integrand stays off near \(t=0\). (P1) does not turn it on. |
| (3) All-shape assembly | **SCHEME A FAILED:** summing per-shape (P1)-style bounds over all scalene multisets has no uniform constant (#shapes \(\to\infty\); shared shells overcounted). Need a once-per-shell (or convergent) pot. |

(17) remains **OPEN**. Author fixed-pair claims are not discarded; their reach is delimited.

---

## 1. Caveat (1) — where a proof of (P1) must be checked

From (14) with rate \(38\nu\),

\[
\mathcal T(t)
=\mathcal T(0)\,e^{-38\nu t}
+\int_0^t e^{-38\nu(t-s)}\mathcal Q(s)\,ds.
\]

Integrating absolute values (STANDARD),

\[
\int_0^T\lvert\mathcal T\rvert\,dt
\le
\frac{\lvert\mathcal T(0)\rvert}{38\nu}
+\frac1{38\nu}\int_0^T\lvert\mathcal Q(s)\rvert\,ds.
\]

Matching the author face \(0.275533\,E_0^2/\nu^2\) forces, if
\(\int\lvert Q\rvert\le K E_0^2/\nu\),

\[
K=0.275533\times 38\approx 10.470.
\]

**First unjustified step without the packet:** the bound on
\(\int\lvert\mathcal Q_{5825}\rvert\,dt\) by an energy-only
multiple of \(E_0^2/\nu\), **including outside inputs**, with
no future \(X\). That is exactly what to audit in
`Block-5825-Review.pdf` — not the Duhamel algebra.

(P2)–(P3): with faces \(\alpha=0.375329\),
\(\beta=1.501315\),

\[
\frac\beta\alpha=4.00000\quad\text{(float)}.
\]

If \(\lvert T_{5825,n}\rvert+\lvert T_{51025,n}\rvert
\le\alpha\sqrt{E_0}\,Y_{S_4,n}/n\) is compared to the
budget share \(\nu Y_{S_4}/4\), the threshold is
\(n\ge 4\alpha\sqrt{E_0}/\nu=\beta\sqrt{E_0}/\nu\).
This is a **consistency probe**, not a verification of
the inequality (P2).

Shell-feed breakdown ([`Q-OTHER-51025`](Q-OTHER-51025.md))
stays on file as the diagnostic map if the \(Q\)-bound
fails.

---

## 2. Caveat (2) — two integrands, one jet

| Object | Formula | Controlled by (P1)? |
|---|---|---|
| Fixed-block \(L^1\) transfer | \(\displaystyle\int\lvert\mathcal T_{5825}\rvert\,dt\) | **Yes** if (P1) holds |
| High-pass budget (15) | \(\displaystyle\int\frac{[\mathcal T_{\mathrm{sc}}(h_K)-\nu Y/4]_+}{X}\,dt\) | **No** |

On the filed \(K=2\) witness,
\(\mathcal T_{\mathrm{sc}}(h_2)=(15084/1625)\,t^6+O(t^7)\),
\(Y(0)=32\), so \(\nu Y(0)/4=8\nu\). Because the left
side is \(O(t^6)\) and the threshold is positive at
\(t=0+\), there exists \(t_*(\nu)>0\) with

\[
\bigl[\mathcal T_{\mathrm{sc}}(h_2(t))-\nu Y(t)/4\bigr]_+=0
\quad\text{for all }0\le t\le t_*
\]

along any continuous trajectory with those jets
(qualitative **EXACT** given the filed leading term and
\(Y(0)>0\)).

So: agreeing to (P1) is not agreeing that the budget
integrand lights up. Cursor’s earlier caveat stands as
a separation of objects, not as hostility to (P1).

---

## 3. Caveat (3) — naive all-shape summation dies

Census of scalene squared-radius multisets \(a<b<c\le 30\)
that admit an integer triangle: **631** shapes. Shell
\(5\) alone participates in **92** of them; the busiest
shells exceed **100** shapes each.

**SCHEME A (FAILED path to (17)).** Assign each shape a
(P1)-style bound
\(\int\lvert T_{abc}\rvert\le C_{abc}E_0^2/\nu^2\) and
sum on shapes. Then either

- \(\sum C_{abc}\) diverges as the radius cutoff
  \(\to\infty\), or
- shared shell energies are charged once per shape and
  massively overcounted.

Either way, SCHEME A does not produce a uniform
\(\sup_N\mathcal S_{K,N}(T)<\infty\).

**What would be needed.** A pot that charges each
**frequency shell** (exact \(\lvert k\rvert^2\) set — not
a physical shell or hole in the fluid) or each unit of
\(Y\) / \(X\) **at most once**, or a convergent weight
over shapes — the author’s “normalized budget for the
fixed pair” is a step for **two** shapes; lifting it to
all shapes without repeated charging is exactly the open
blank toward (17).

Locked one-pager:
[`ALL-SHAPE-SHELL-POT-BLANK.md`](ALL-SHAPE-SHELL-POT-BLANK.md).

Attack design replacing the blank’s “need a pot”:
[`SCHEME-B-SHELL-POT.md`](SCHEME-B-SHELL-POT.md)
— target (B1) \(\lvert\mathcal T_{\mathrm{sc}}\rvert\le C_\star X\sqrt Y\);
SCHEME A′ (Young after shapes) killed by probe.

---

## 4. How the two approaches stay complementary

| Tool | Role after this truth run |
|---|---|
| Author (P1)–(P3) + normalized fixed-pair budget | Stronger starting estimate for complete blocks with outside inputs — **check the \(Q\)-step in the packet** |
| Cursor shell-feed / \(S_4\) / \(\mathcal Q^{\infty}\) breakdown | Diagnostic if that \(Q\)-step fails; shows which outside shells enter |
| This truth run | Delimits reach: Duhamel OK; budget integrand separate; SCHEME A dead |

Failure modes (as agreed):

- Constant wrong → maybe fixable.
- Frequency argument fails → fixed-block (P1) might still hold.
- Combining many blocks fails → individual bounds may survive; SCHEME A already shows naive combining dies.

---

## STATUS

(P1) DUAMEL SKELETON: STANDARD.
(P1) \(\int\lvert Q\rvert\) ENERGY BOUND: UNCHECKED — FIRST PACKET TARGET.
(P2)–(P3): \(\beta/\alpha=4\) CONSISTENT WITH \(\nu Y/4\); PROOF UNCHECKED.
BUDGET INTEGRAND VS \(\int\lvert T_{5825}\rvert\): SEPARATED; JET STAYS BELOW THRESHOLD INITIALLY.
SCHEME A (SUM PER SHAPE): FAILED.
ALL-SHAPE ONCE-PER-SHELL POT: OPEN → (17).
NS NOT SOLVED.
