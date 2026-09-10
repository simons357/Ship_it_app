# Five-lane discussion (PR 48)

10 September 2026. Recovery. **NS not solved.
★ not proved.** Stay in this chat.

Source: https://github.com/simons357/Ship_it_app/pull/48
Branch: `cursor/ns-five-lane-lemma-star-1390`

Full lock:
[`five-lane-export/FIVE_LANES.md`](five-lane-export/FIVE_LANES.md).
JSON: [`five-lane-export/COMPUTE.md`](five-lane-export/COMPUTE.md).
Math: [`math/ns_attacks/LEMMA_STAR_CANONICAL.md`](math/ns_attacks/LEMMA_STAR_CANONICAL.md).

---

## Screenshot

“Finished Five-lane NS drill”
“Five-lane drill done; K=0 dead; Lemma★
survives numeric kill only (not proved);
HH→L still the gap.”

A later Grok screenshot calls “Lane two”
an analytic \(X^{3/2}\)-type bound.

Those excerpts do not name all five lanes.
The pack does.

---

## Original five (not 9A–9D)

1. Covariance — `attack1_covariance.py`
2. Triad / K=0 / \(C_*\) — `attack2_triad_k0_cstar.py`
   Remainder \(\lvert T_c\rvert\le C_* X^{3/2}\Lambda\)
   (amp-invariant). K=0 dead. Not \(C_{\star}\).
3. Bony HH→L — `attack3_bony_hh_l.py`
4. Stokes — `attack4_stokes.py`
5. Route 2 — `attack5_route2_kill.py`

Do **not** substitute 9A–9D for these.
9A AP, 9B exact-shell \(K\), 9C fixed-gap,
9D Freiman-AP / screenshot counting error
are later. Attack 12’s lattice fan is not
lane 3.

The other \(X^{3/2}\) line
\(\lvert T_c\rvert\le C\|u\|_2 X^{3/2}\)
is dead by scaling (\(a^3\) vs \(a^4\)).
That is not lane 2.

Canonical target still
\((T_{c+})^2\le C_{\mathrm{geom}}\,\mathcal D_s\,E\,Y\),
i.e. \(\sup\mathcal R_\star<\infty\).
