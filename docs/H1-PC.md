# H1 / PC — path-cost of one Bad pair

10 September 2026. **This estimate sits. It is not H1.
WRITE (6) is not proved. NS is not solved.**

Same leftover class. Not a new name.
Locator: [`WHERE-H1.md`](WHERE-H1.md).
Object: [`H1-OBJECT.md`](H1-OBJECT.md).
P1 (frequency, different integral): [`H1-P1.md`](H1-P1.md).
P1-loc (cutoff, \(\nabla u\) kept): [`H1-P1-LOC.md`](H1-P1-LOC.md).
Shapes: [`H1-SHAPES.md`](H1-SHAPES.md).
Do not merge with Lemma★, \(H_N\), or Lemma C.

Probe: `python3 scripts/h1_pc_pathcost.py`

This is what DA can write here: a sitting 1-D bound.
DA cannot convert it into WRITE (6).

---

## What sits

Let \(\xi:U\to S^2\) be \(C^1\) on an open set \(U\subset\mathbb{R}^3\).
Let \(x,y\in U\), \(\rho=|x-y|>0\), and let \(\gamma\subset U\) be a
\(C^1\) path from \(x\) to \(y\). Write \(\varphi\in[0,\pi]\) for the
angle between \(\xi(x)\) and \(\xi(y)\).

**Lemma PC (path-cost of one pair).**

\[
\int_\gamma|\nabla\xi|\,|ds|
\ge
\varphi
\ge
|\sin\varphi|.
\]

If also \((x,y)\) is Bad in the WRITE (6) cut,
\(|\sin\varphi|>C_*\rho^{1/2}\), then

\[
\int_\gamma|\nabla\xi|\,|ds|
>
C_*\rho^{1/2}.
\]

Proof. \(|(\xi\circ\gamma)'|\le|\nabla\xi|\,|\gamma'|\), so the
length of \(\xi\circ\gamma\) on \(S^2\) is at most the path
integral. That length is at least the geodesic \(\varphi\).
On \([0,\pi]\), \(\varphi\ge\sin\varphi=|\sin\varphi|\).
The Bad cut is the last line.

No NSE. No energy. Sphere geometry and the chain rule.

---

## What does not sit

**A path in \(\{|\omega|\ge\Lambda\}\).** The lemma needs
\(\gamma\subset U\) with \(\xi\) defined. A gap
(\(\omega\approx 0\) between two blobs) removes the path.
The pair can still be Bad. Biot–Savart does not need a path.
Packet §6: reconnection / two-blobs.

**Volume dissipation / fold.** Cauchy–Schwarz on the segment
gives a 1-D bound, still not
\(\int_{B_{2\rho}}|\nabla\omega|^2\gtrsim\Lambda^2\rho^2\).
A thin tube of rotation keeps the path-cost and sends the
volume integral to \(0\) with the radius. That is why
path-cost dies as H1. Shape 2 (Vitali on folds) is not this
lemma. Lemma J on generic fields stays false.

**H1 / WRITE (6).** The leftover is a triple integral of
\(|z|^{-3}\) on the Bad set versus
\(\nu/8\iint|\nabla\omega|^2\phi+C r^{-2}\iint|\omega|^2\).
A lower bound on one curve does not absorb that.

Do not cash PC as shape 1, 2, or 3. Do not cash it as P1.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| H1pc_geodesic_sits | **pass** | \(\varphi\ge|\sin\varphi|\) on \(S^2\) |
| H1pc_path_sits | **pass** | rotating field: \(\int_\gamma|\nabla\xi|\ge\varphi\) |
| H1pc_bad_cut | **pass** | Bad \(\Rightarrow\) path-cost \(>C_*\rho^{1/2}\) on that field |
| H1pc_gap | **pass** | two blobs: no path in \(\{|\omega|\ge\Lambda\}\) |
| H1pc_not_fold | **pass** | thin tube: path-cost stays, volume fold dies |
| H1pc_is_h1 | **fail** | a segment bound is not \(A_{\mathrm{bad}}\) versus dissipation |

H1 remains the leftover. Shapes 1–3 remain unproved.
P1-lowpass is a different sitting cousin.

NS not solved.
