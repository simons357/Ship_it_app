# Attack 9D — grow \(s\) on the 9B family

12 September 2026.
**Historical packet sweep. Not a close.
Designed \(\Theta(m^2)\) 9D is still dead.
Unrestricted ★ is killed by a different
family. NS is not solved.**

This is live write 1. Same \(B\) as 9B.
Fixed-output \(\Theta(m^2)\) is excluded
(\(K\le 16s\)). Do **not** implement
`attack9d_theta_m2_locked_phase.py`.

Probe:
`python3 scripts/ns_attacks/attack9b_grow_s.py`
JSON: `results/attack9b_grow_s/grow_s.json`
Setup: [`ATTACK-9D-SETUP.md`](ATTACK-9D-SETUP.md).
Counting: [`LEMMA-STAR-9B-COUNTING.md`](LEMMA-STAR-9B-COUNTING.md).
Tape: [`YES-NO-OPEN.md`](YES-NO-OPEN.md).

---

## Target (frequency factors kept)

\[
B(w,w)=P\bigl[(w\cdot\nabla)w\bigr],
\qquad
K_{\alpha,\beta}(w)
=
\frac{\beta\,\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}.
\]

\[
\|\Pi_\beta B(w,w)\|_2
\le
C\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2
\quad\Longleftrightarrow\quad
\sup K_{\alpha,\beta}<\infty.
\]

Wrong packaging:
\(\|\Pi_\beta B\|_2\le C\alpha\|w\|_2^2\).

9B family: \(v_\varepsilon=w_\alpha+\varepsilon z_\beta\),
\(z_\beta\parallel\Pi_\beta B(w_\alpha,w_\alpha)\).
On aligned, sign-selected \(z_\beta\),
\(\mathcal R_\star\to K\). Arbitrary \(z_\beta\)
sees the projection against \(B(w,w)\).

Input support \(m\) = number of keys in
\(w_\alpha\). Output occupancy \(s\) =
number of keys in \(\Pi_\beta B(w,w)\).
Both grow. Full complex polarizations.

---

## What this run is not

- Designed locked-phase \(\Theta(m^2)\)
  subset (Freiman-AP). Dead.
- \(\Theta(m^2)\) onto one output, or a
  fixed number of outputs. Counting
  error. \(K\le 16s\).
- Attack 12 HH→L. Different family.
  Do not merge a finite \(\sqrt{K}\)
  with that table’s \(0.71\).
- Five lanes 1–5, 9A, natural 9C,
  finite 9B \(K\approx 0.641\).
  Already scored. Do not redo.

---

## Sweep (this branch)

Seed 1390. Exact shells through
\(k_{\max}=8\) (\(|k_i|\le 8\)).
Random subsets of the positive half,
then the full shell. One \(B(w,w)\)
per input field. Every occupied
output shell with \(\beta\le 4\alpha\),
\(\beta\neq\alpha\). Four trials per
\((m,\alpha)\).

Inequalities sit (pairs on one \(k\le m\);
\(\lvert\widehat B_k\rvert\le\lvert k\rvert\|w\|_2^2\);
\(K\le 16s\)). A finite max is not
\(C_0\). A larger finite number only
raises \(C_{\mathrm{geom}}\).
\(\mathcal R_\star\to\infty\) would kill ★.

Printed samples on that draw
(seed 1390, \(k_{\max}=8\), four trials):
2084 input fields, 39853 occupied
\((\alpha,\beta)\) rows. Max
\(K\approx 0.456\) at
\((\alpha,\beta)=(16,32)\), \(s=4\),
\(m=4\). Max \(\sqrt{K}\approx 0.675\).
Max \(s=192\). Max \(m=120\).
Pairs / CS / \(K\le 16s\): no fails.
On the \(K\) vs \(s\) curve, max \(K\)
for \(s\le 8\) is \(0.456\); for
\(s\ge 24\) it is \(0.239\). Larger
occupancy did not raise \(K\) here.

This is random polarizations on
growing supports. It is not the
aligned 9B search that printed
\(K\approx 0.641\) at \((4,8)\).
Do not merge those two numbers.
The write-up example is the
three-shear field
\(w=(\sin y,\sin z,\sin x)\),
\(K_{1,2}=2/3\) by hand
([`ATTACK-9D-TWO-THIRDS.md`](ATTACK-9D-TWO-THIRDS.md)).
A table of random maxima is not
that example. A finite max is not
\(C_0\).
A larger finite number only raises
\(C_{\mathrm{geom}}\).
\(\mathcal R_\star\to\infty\) would
kill ★. This draw did not. It is
not a kill.

JSON: `results/attack9b_grow_s/grow_s.json`
(summary; per-row dump not committed).

---

## Status

| Item | Verdict |
|---|---|
| Designed 9D \(\Theta(m^2)\) | **NO.** Dead. |
| Fixed \(s\) | **NO** as a kill. \(K\le 16s\). |
| Grow \(m\) and \(s\) as a ★ kill | **NO.** Historical. |
| Exact-shell \(\sup K<\infty\) | **CLAIMED** on the other page |
| Unrestricted Lemma★ | **NO.** Killed by \(v_n\). |

This draw did not kill ★. The named
kill is [`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md).
Exact-shell \(K\le 16/9\) is claimed on
[`ATTACK-9D-FULL-SUPPORT-BOUND.md`](ATTACK-9D-FULL-SUPPORT-BOUND.md).
Bounded samples are not a proof.
NS not solved.
