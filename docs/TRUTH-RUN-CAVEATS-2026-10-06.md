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
| (1) Verify (P1)–(P3) | Damping / Duhamel is **STANDARD**. Substantive claim is (Q⋆) \(\lvert Q\rvert\le D\beta\,E\,X_{\mathrm{block}}\) (packet); then \(\int\lvert Q\rvert\le D\beta E_0^2/(2\nu)\) by the energy budget. (Q⋆) unchecked until packet audit. Factor four in (P2)–(P3) is **by author definition** (threshold = \(4\times\) transfer-bound constant) — verify from exact expressions, not float faces. |
| (2) \(\int\lvert T_{5825}\rvert\) vs budget | **Distinct objects.** On the \(K=2\) jet, \(\mathcal T_{\mathrm{sc}}(h_2)=O(t^6)\) stays below \(\nu Y/4\) near \(t=0\). Jet appearance is **not** a positive budget episode. |
| (3) All-shape assembly | **SCHEME A FAILED** as a path: naïve per-shape sum repeatedly charges shared shells. Overlap counts **diagnose** that failure; they do **not** alone prove every weighted summation must fail. Once-per-shell / convergent pot still OPEN (SCHEME B). |

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

**Right review target** (author qualification): the packet
bound

\[
\lvert\mathcal Q\rvert\le D\beta\,E\,X_{\mathrm{block}},
\tag{Q⋆}
\]

not the damping calculation. If (Q⋆) holds, then
\(\int\lvert Q\rvert\,dt\le D\beta E_0\int X_{\mathrm{block}}
\le D\beta E_0^2/(2\nu)\) by the established energy
budget — STANDARD after (Q⋆). Scrutiny of (Q⋆):
geometric factors, all differentiated terms, shared-mode
counting. See
[`Q-BOUND-REVIEW-TARGET.md`](Q-BOUND-REVIEW-TARGET.md).

Matching the decimal face \(0.275533\,E_0^2/\nu^2\) with
rate \(38\nu\) forces an implied
\(\int\lvert Q\rvert\le K E_0^2/\nu\) with
\(K\approx 0.275533\times 38\); prefer exact packet
constants over this float back-solve.

(P2)–(P3): author defines the threshold constant as
**four times** the transfer-bound constant (budget share
\(\nu Y/4\)). Cursor’s \(\beta/\alpha\approx 4\) from
decimal faces was only a float check — **withdrawn as
verification**. Confirm the factor four from the exact
packet expressions.

Shell-feed breakdown ([`Q-OTHER-51025`](Q-OTHER-51025.md))
stays on file as the diagnostic map if (Q⋆) fails.

`Block-5825-Review.pdf` / `.zip`: **not uploaded** to
PR #165 pending explicit authorization.

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
integrand lights up. The jet’s appearance is **not**
evidence of a positive high-pass budget episode near
\(t=0\) (author + Cursor agree).

---

## 3. Caveat (3) — naive all-shape summation dies

Census of scalene squared-radius multisets \(a<b<c\le 30\)
that admit an integer triangle: **631** shapes. Shell
\(5\) alone participates in **92** of them; the busiest
shells exceed **100** shapes each.

**SCHEME A (FAILED path to (17)).** Assign each shape a
(P1)-style bound
\(\int\lvert T_{abc}\rvert\le C_{abc}E_0^2/\nu^2\) and
**naïvely sum** on shapes. Then either

- \(\sum C_{abc}\) diverges as the radius cutoff
  \(\to\infty\), or
- shared shell energies are charged once per shape and
  massively overcounted.

Overlap / incidence counts **show why** that naïve sum
double-charges frequency shells. Per author
qualification, they do **not** alone prove that every
weighted summation must fail — convergent weights or a
once-per-shell pot remain open routes.

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

Attack design:
[`SCHEME-B-SHELL-POT.md`](SCHEME-B-SHELL-POT.md)
— target (B1); absolute donor-pair shortcuts killed;
signed assembly still OPEN.

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

DAMPING / DUAMEL: STANDARD.
(Q⋆) \(\lvert Q\rvert\le D\beta\,E\,X_{\mathrm{block}}\): UNCHECKED — FIRST PACKET TARGET
([`Q-BOUND-REVIEW-TARGET.md`](Q-BOUND-REVIEW-TARGET.md)).
∫\|Q\| AFTER (Q⋆) VIA ENERGY BUDGET: STANDARD.
(P2)–(P3) FACTOR FOUR: BY AUTHOR DEFINITION — VERIFY EXACT EXPRESSIONS (FLOAT PROBE WITHDRAWN AS VERIFICATION).
BUDGET INTEGRAND VS \(\int\lvert T_{5825}\rvert\): SEPARATED; JET BELOW THRESHOLD ≠ POSITIVE EPISODE.
SCHEME A (NAÏVE SUM PER SHAPE): FAILED.
OVERLAP COUNTS: DIAGNOSE DOUBLE-CHARGE; DO NOT KILL ALL WEIGHTED SUMS.
ALL-SHAPE ONCE-PER-SHELL POT: OPEN → (17).
PDF/ZIP ON PR #165: AWAITING EXPLICIT AUTHORIZATION.
NS NOT SOLVED.
