# Review target: the bound on \(\mathcal Q\) (not the damping)

6 October 2026.
**Author qualification of the Cursor truth-run. Packet not yet on GitHub.
Not (17). NS not solved.**

Parents:
[`TRUTH-RUN-CAVEATS-2026-10-06.md`](TRUTH-RUN-CAVEATS-2026-10-06.md),
[`BLOCK-5825-PARTIAL-BOUNDS-2026-10-06.md`](BLOCK-5825-PARTIAL-BOUNDS-2026-10-06.md).

Author packet (local / handoff — **not** uploaded to PR #165
until explicitly authorized):
`Block-5825-Review.pdf`, `Block-5825-Review-Package.zip`.

---

## RESULT

The right review target for (P1) is the bound on
\(\mathcal Q\) (transfer from other modes). The viscous
damping / Duhamel algebra is straightforward.

Packet proposal:

\[
\boxed{
\lvert\mathcal Q\rvert
\le
D\beta\,E\,X_{\mathrm{block}}.
}
\tag{Q⋆}
\]

If (Q⋆) holds, the energy identity
\(E'+2\nu X=0\) and \(X_{\mathrm{block}}\le X\) give

\[
\int_0^T\lvert\mathcal Q\rvert\,dt
\le
D\beta\,E_0\int_0^T X_{\mathrm{block}}\,dt
\le
\frac{D\beta\,E_0^2}{2\nu}.
\]

The second step (integration against the established
energy budget) is STANDARD once (Q⋆) is granted.
**The first inequality — (Q⋆) itself — needs the
scrutiny:** geometric factors, all differentiated terms
in the quartic forcing, and correct counting of shared
modes.

---

## 1. What to check in the packet

| Check | Question |
|---|---|
| Geometry | Are the exact-sphere / triangle factors in \(D\beta\) correct for this block? |
| Differentiated slots | Does \(\mathcal Q\) include every nonlinear derivative term required by (14), including outside-mode feed? |
| Shared modes | When a mode sits in more than one contributing pair, is it counted once in \(X_{\mathrm{block}}\) / the majorant, not duplicated? |
| Scope | Does (Q⋆) cover the complete signed block including outside inputs, as claimed for (P1)? |

Damping rate \(38\nu=(5+8+25)\nu\) is not the dispute.

---

## 2. Qualifications to the Cursor truth-run

### 2.1 Factor of four — by definition, not float probe

Cursor reported \(\beta/\alpha\approx 4\) from decimal faces
\(0.375329\) and \(1.501315\). That floating-point
agreement is **not** the verification.

Author definition: the threshold constant is
**four times** the transfer-bound constant (the budget
share \(\nu Y/4\)). Exact expressions in the packet
must be checked; do not treat float coincidence as a
proof of the factor four.

### 2.2 Overlap counts — diagnostic, not a universal kill

Reported shape/shell overlap counts (e.g. shell \(5\) in
many shapes) show why **naïvely adding** per-shape
bounds repeatedly charges the same frequency-shell
energies (SCHEME A).

They do **not** alone prove that every weighted
summation over shapes must fail. A convergent weight,
a once-per-shell pot (SCHEME B), or another structured
assembly remains possible. Overlaps motivate the pot;
they do not close the negative survey of all assemblies.

### 2.3 Jet below threshold — not a positive budget episode

Agree with the truth-run separation: on the regenerated
\(K=2\) datum, \(\mathcal T_{\mathrm{sc}}(h_2)=O(t^6)\)
starts below \(\nu Y/4\). Appearance of that jet is
**not** evidence of a positive high-pass budget episode
near \(t=0\).

---

## 3. Upload / handoff status

| Item | Status |
|---|---|
| `Block-5825-Review.pdf` | Ready on author side; **not** in the repo / PR #165 |
| `Block-5825-Review-Package.zip` | Same |
| Upload to `simons357/Ship_it_app` PR #165 | **BLOCKED** pending explicit authorization |

Cursor must **not** upload these binaries until the
author authorizes that handoff. Filing this page does
not constitute authorization.

---

## STATUS

REVIEW TARGET: (Q⋆) \(\lvert Q\rvert\le D\beta\,E\,X_{\mathrm{block}}\) — UNCHECKED UNTIL PACKET AUDIT.
∫\|Q\| VIA ENERGY BUDGET AFTER (Q⋆): STANDARD.
β = 4α: BY AUTHOR DEFINITION — VERIFY FROM EXACT PACKET EXPRESSIONS, NOT FLOATS.
OVERLAP COUNTS: DIAGNOSE NAIVE DOUBLE-CHARGE; DO NOT KILL ALL WEIGHTED SUMS.
JET BELOW νY/4 INITIALLY: NOT A POSITIVE BUDGET EPISODE.
PDF/ZIP UPLOAD TO PR #165: AWAITING EXPLICIT AUTHORIZATION.
NS NOT SOLVED.
