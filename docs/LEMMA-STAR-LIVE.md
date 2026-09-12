# Lemma★ — two live writes

12 September 2026. Desk lock.
**NS not solved. Lemma★ OPEN.**

Phone: stay in this chat.

Everything else is scored or refused.
Kill lane is still live.

---

## 1. Attack 9D — grow \(s\) on the 9B family

Same \(B=B(w,w)=P[(w\cdot\nabla)w]\).
Same 9B family
\(v_\varepsilon=w_\alpha+\varepsilon z_\beta\),
\(z_\beta\parallel\Pi_\beta B(w,w)\).

Target
\[
\|\Pi_\beta B\|_2
\le
C\alpha\beta^{-1/2}\|w\|_2^2
\qquad\Longleftrightarrow\qquad
\sup K_{\alpha,\beta}<\infty,
\]
\[
K
=
\frac{\beta\|\Pi_\beta B\|_2^2}{\alpha^2\|w\|_2^4}.
\]
Growing input and output. Full complex
polarizations. \(|k|\) kept.

Fixed-output \(\Theta(m^2)\) excluded
(\(K\le 16s\)). Designed \(\Theta(m^2)\)
stays dead. `attack9d_theta_m2_locked_phase.py`
was not written. Do not write it.

Seed 1390, \(k_{\max}=8\): 2084 input
fields, 39853 occupied \((\alpha,\beta)\)
rows. Max \(K\approx 0.456\) at
\((16,32)\), \(s=4\). Max \(\sqrt{K}\approx 0.675\).
Max \(s=192\). Pairs / CS / \(K\le 16s\):
no fails. On the \(K\) vs \(s\) curve,
max \(K\) for \(s\le 8\) is \(0.456\);
for \(s\ge 24\) it is \(0.239\). Larger
occupancy did not raise \(K\) on this draw.

That is not the aligned 9B search
(\(K\approx 0.641\) at \((4,8)\)).
Do not merge them. A finite max is not
\(C_0\). This draw did not kill ★.

Page: [`ATTACK-9D-GROW-S.md`](ATTACK-9D-GROW-S.md).
JSON: `results/attack9b_grow_s/grow_s.json`.
Probe: `python3 scripts/ns_attacks/attack9b_grow_s.py`.
Setup: [`ATTACK-9D-SETUP.md`](ATTACK-9D-SETUP.md).

This branch’s smaller sweeps stay scored
and separate. Do not merge them with
\(0.456\) or \(0.641\):

- linear-pol growing-\(s\): \(K\approx 0.631\)
  ([`LEMMA-STAR-9B-GROWING.md`](LEMMA-STAR-9B-GROWING.md));
- 225-field full-complex: \(K\approx 0.612\)
  (`scripts/ns_attacks/attack9d_growing.py`).

---

## 2. The ★ reason — map, not a theorem

Keep \(\mathrm{Im}\). Do not replace it
by an absolute value. HH→L is the
dangerous channel (weight \(\sim\beta\cdot\alpha\);
Attack 12 vertex carries \(\sqrt{\beta}\)).
Cheap CS returns occupancy — the same
hole as \(K\le 16s\).

Until that sentence is a theorem, or
\(\mathcal R_\star\to\infty\), leftover 4
stays OPEN.

Need★ (signed dual on HH→L after
gap-cancel) is still **MISSING**.

[`LEMMA-STAR-REASON.md`](LEMMA-STAR-REASON.md).
[`NEED-STAR-HH-L-DUAL.md`](NEED-STAR-HH-L-DUAL.md).
Tape: [`YES-NO-OPEN.md`](YES-NO-OPEN.md).

---

Kill lane LIVE. Bounded samples are
not a proof. A diverging family would
kill ★. A larger finite number only
raises \(C_{\mathrm{geom}}\).

---

## Optional, not next by default

- Locked-\(\mathcal R_\star\) 9C recompute
  (\(0.11\to 0.031\)). Never done here.
- Exact-core ABC at \(\lambda=8\) and \(16\)
  on one field definition. Clue only.
- H1 from ABC_λ. Do not start it.
  This branch started shape 3
  (predictive CF ODE). Alignment frozen.
  Not a theorem.
  [`H1-PREDICTIVE.md`](H1-PREDICTIVE.md).

---

## Do not redo

Five lanes 1–5, 9A, natural 9C, finite 9B
(\(K\approx 0.641\)), small-lattice truncated
ABC, SuperGrok falsifier stamp, Dream Team
vote.

---

## Out of this book

Q-stack, SND, Theorem H, five fingers,
augmented NSE.

NS not solved. Lemma★ OPEN.
