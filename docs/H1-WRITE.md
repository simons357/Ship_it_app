# H1 write — the estimate, not the theorem

12 September 2026.
Unaugmented Navier–Stokes, one cylinder
\(Q_r\); quantity is Bad-pair stretching
\(A_{\mathrm{bad}}\); remainder is
\(A_{\mathrm{bad}}\) versus
\(\nu/8\iint|\nabla\omega|^2\phi
+C r^{-2}\iint|\omega|^2\);
no extra field; no extra hypothesis;
**OPEN.**

**This is the write. It is not proved.
H1 is not a theorem. WRITE (6) is not
a theorem. Ordinary Navier–Stokes is
not solved.**

Do not start this write from ABC_λ.
Do not glue this integral to
\(\mathcal R_\star\). Do not quote the
Ring Lemma as proved. Do not add
\(K(t)\) to the PDE.

Machine that obeys this objective:
`python3 scripts/h1_machine.py`

Object: [`H1-OBJECT.md`](H1-OBJECT.md).
One-line write: [`WRITE_6.md`](WRITE_6.md).
Data behind the write:
[`WRITE_6_SUPPORTED.md`](WRITE_6_SUPPORTED.md).
Shapes: [`H1-SHAPES.md`](H1-SHAPES.md).
Locator: [`WHERE-H1.md`](WHERE-H1.md).

---

## 0. The word this math obeys

The objective is one of two sentences.

**Bound.** On \(Q_r\), Bad pairs only
(\(|\omega|\ge\Lambda\) and
\(|\sin\varphi|>C_*|x-y|^{1/2}\)),
both ends in the ball,

\[
A_{\mathrm{bad}}(Q_r)
\le
\frac\nu8\iint_{Q_r}|\nabla\omega|^2\phi
+C r^{-2}\iint_{Q_r}|\omega|^2.
\]

**Kill.** A named sequence of admissible
cylinders (or fields) on which the
locked ratio \(\mathcal G\) below
diverges.

Nothing else is a close of leftover 1.
A cousin that sits is not this write.
An *if* is not this write. A tube
number is not this write. A Dream-team
vote is not this write. Evolution is
not this write.

The machine in
`scripts/h1_machine.py` refuses any
paragraph that retitles a cousin as
(6), drops the class, or claims the
write sits. That is the obedience.
It is not a solver.

---

## 1. Locked ratio

\[
\mathcal G(Q_r)
=
\frac{A_{\mathrm{bad}}(Q_r)}
{\iint_{Q_r}|\nabla\omega|^2\phi
+r^{-2}\iint_{Q_r}|\omega|^2}.
\]

H1 as a bound is
\(\sup\mathcal G<\infty\)
(the conventional slice \(\nu/8\)
is a packaging of that supremum,
not a sharp constant).

A kill of H1 is a sequence with
\(\mathcal G\to\infty\).

A finite sample of \(\mathcal G\)
raises the implied constant. It does
not prove the bound. It does not
kill the bound.

This ratio is the cylinder writing of
leftover 1. It is **not**
\(\mathcal R_\star=(T_c)_+^2/(\mathcal D_s E Y)\).
Different integral. Different class
of test objects. Do not merge the
two letters.

Near-Bad (\(|x-y|<\rho\)) is the core
of the numerator. Mid-Bad
(\(|x-y|\ge\rho\)) is a named
remainder of H3 class,
\[
A_{\mathrm{bad}}^{\ge\rho}
\le
C\rho^{-3/2}\int E_{\mathrm{loc}}^{3/2}\,dt.
\]
That bound sits. It is not H1.

---

## 2. Local identity (sits; does not bound \(A_{\mathrm{bad}}\))

Cutoff \(\phi\equiv 1\) on \(B_{r/2}\),
supported in \(B_r\). Vorticity form,
pressure free:

\[
\tfrac12\frac{d}{dt}\int|\omega|^2\phi
+\nu\int|\nabla\omega|^2\phi
=
\int\alpha|\omega|^2\phi
+\tfrac12\int|\omega|^2(\partial_t\phi+u\cdot\nabla\phi)
+\tfrac\nu2\int|\omega|^2\Delta\phi.
\]

On \(\{\omega\neq 0\}\),
\(\xi=\omega/|\omega|\),
\(\varphi(x,y)\) the angle between
\(\xi(x)\) and \(\xi(y)\),

\[
\alpha(x)=\mathrm{P.V.}\int
D(\hat z,\xi(x),\xi(y))
\frac{|\omega(y)|}{|x-y|^3}\,dy,
\qquad
|D|\le C|\sin\varphi|.
\]

Direction energy (identity):

\[
|\nabla\omega|^2
=
|\nabla|\omega||^2
+|\omega|^2|\nabla\xi|^2.
\]

Hence
\(\int_{\{|\omega|\ge\Lambda\}}|\nabla\xi|^2
\le\Lambda^{-2}\int|\nabla\omega|^2\).
Identity. Not Hölder \(1/2\).
Morrey: \(W^{1,2}\not\subset C^{0,1/2}\)
in three dimensions.

Time-integrate on \(Q_r\). Stretching
splits. This identity does **not**
bound the Bad piece.

---

## 3. Split (dictionary; not a close)

| Piece | Cut | Status |
|---|---|---|
| Good | \(\lvert\sin\varphi\rvert\le C_*\lvert x-y\rvert^{1/2}\) whenever both \(\lvert\omega\rvert\ge\Lambda\) | Lemma C. Their theorem as an *if*. Localization leaves \(R_\phi\). Not free. Not an H. |
| Bad | \(\lvert\omega\rvert\ge\Lambda\) and \(\lvert\sin\varphi\rvert>C_*\lvert x-y\rvert^{1/2}\) | **This write. Open.** |
| Low | one or both ends below \(\Lambda\) | Labeled. Not H1. |
| Exterior / H3 | one end outside the ball | Written: \(A_{\mathrm{ext}}\le C r^{-3/2}\int E^{1/2}E_{\mathrm{loc}}\,dt\). Not absorbed as \(r\to 0\). |
| Flux / H2 | skin term \(r^{-1}\iint\lvert u\rvert\lvert\omega\rvert^2\) | CKN-smallness sits. From energy alone: open. |
| Parent **H** | all stretching on \(\mathbb{R}^3\) | Open. A cylinder is not this parent. |

A cylinder closes only if
\(\mathrm{C}+R_\phi\), **this write**,
H2-a priori (or CKN-small), and H3
all sit. Then local Serrin on
\(Q_{\theta r}\), not CKN.
If this write sits and H2-from-energy
does not, the cylinder is still open.

---

## 4. Hölder cut, spent once

On Good pairs the cut is an
*upper* bound on \(\lvert\sin\varphi\rvert\).
The kernel drops:

\[
\frac{|D|}{|z|^3}
\le
C\frac{|z|^{1/2}}{|z|^3}
=
C|z|^{-5/2}.
\]

That is Lemma C. It absorbs.
It is an *if*.

On Bad pairs the same cut is a
*lower* bound on \(\lvert\sin\varphi\rvert\).
The majorant still uses
\(\lvert D\rvert\le C\lvert\sin\varphi\rvert\le C\),
so the kernel stays \(\lvert z\rvert^{-3}\).
HLS returns local \(E^3\).

The cut changes the set. It does not
change the exponent on what remains.
You cannot spend the cut a second
time on Bad and call that thinness.
That sentence is the destroyer of
the usual fake close.

Signed \(D\) already failed for an
isolated pair. Absolute value on
\(A_{\mathrm{bad}}\) is sufficient,
not necessary. The triple-integral
majorant
\[
\iint\!\!\int_{\mathrm{Bad}}
\frac{|\omega(x)|^2|\omega(y)|}{|x-y|^3}\,\phi
\]
is the same leftover. Constants in
\(\lvert D\rvert\) go into \(\nu/8\).

Parabolic scaling of
\(A_{\mathrm{bad}}\),
\(\iint|\nabla\omega|^2\phi\), and
\(r^{-2}\iint|\omega|^2\) agrees
(\(r^{-1}\)). There is no dimensional
obstruction. There is also no proof.

---

## 5. Cousins that sit — not this write

**P1 (low-pass).** If
\(\widehat{\omega}(k)=0\) for
\(\lvert k\rvert>K\), then
\(\int|\omega|^2\le K^2\int|u|^2\).
If also \(K\le C/\rho\),
\(\rho^2\int|\omega|^2\le C^2\int|u|^2\).
Plancherel. NSE membership open.
High-pass at the same \(\rho\)
breaks the \(O(1)\) claim.
[`H1-P1.md`](H1-P1.md).

**P1-loc (cutoff).**
\[
\int_{B_\rho}|\omega|^2
\le
4\int_{B_{2\rho}}|\nabla u|^2
+C\rho^{-2}\int_{B_{2\rho}}|u|^2.
\]
\(\nabla u\) stays. Dropping it
fails on high-pass.
[`H1-P1-LOC.md`](H1-P1-LOC.md).

**PC (path-cost).** On a \(C^1\)
path \(\gamma\) from \(x\) to \(y\),
\[
\int_\gamma|\nabla\xi|\,|ds|
\ge
\varphi
\ge
|\sin\varphi|.
\]
Bad cut: path-cost \(>C_*\rho^{1/2}\).
A gap removes the path. A thin tube
keeps the path-cost and kills the
volume fold. One curve is not
\(A_{\mathrm{bad}}\).
[`H1-PC.md`](H1-PC.md).

Literature lookup: all miss.
H1 is not under another name.
[`LOOKUP-H1.md`](LOOKUP-H1.md).
Closest cousins (CF, BdVB, Grujić
2009 / 2010 / 2013) are still ifs.
[`LITERATURE-H.md`](LITERATURE-H.md).

---

## 6. Shapes that would be this write — none sits

Prove one. Then leftover 1 moves.
None sits.

**1. Thinness.** An exponent drop
on the Bad kernel
(\(\lvert z\rvert^{-3}\) to
\(\lvert z\rvert^{-3+\varepsilon}\)),
or an operator bound that pays
stretching by dissipation plus
\(r^{-2}\iint|\omega|^2\), from
\(\int E<\infty\).
CS-summable volume thinness
\(\theta_k\le C\,2^{-(3+\delta)k}\)
returns
\[
A_{\mathrm{bad}}^{<\rho}
\le
C_\delta\rho^{-3/2}\int E_{\mathrm{loc}}^{3/2}\,dt.
\]
That is the mid-Bad / H3 class.
**CS thinness is not H1.**
“Assume thin” is Lemma C (Good).
It is not shape 1.

**2. \(J\) on folds only.**
Every persistent-Bad pair at scale
\(\rho\) sits in a ball \(B\) of
radius \(2\rho\) with
\(\int_B|\nabla\omega|^2\gtrsim\Lambda^2\rho^2\).
Vitali plus
\(A_{\mathrm{bad}}^{<\rho}\le C\sum\Lambda^3\rho_j^3\)
gives a factor \(\sup\Lambda\rho_j\).
If \(\Lambda\rho\le c\nu\), the
\(\nu/8\) slice sits.
Three hypotheses, none free:
persistent Bad pairs are folds
(not sheets or gaps); stretching
is the Vitali sum; \(\Lambda\rho\)
is small enough to eat.
Lemma J on generic fields is false.
PC is not this shape.

**3. Dynamics.** NSE forbids the
sheet and the gap on the time
scale \(r^2/\nu\), so the fold
hypothesis in (2) holds.
An imposed waiting time is not
this shape. Pathwise enstrophy
does not produce
\(\int|\nabla\omega|^2\).

Outside-\(\mathcal{E}\) identity:
**blocked.** No candidate. Do not
invent one.

Tube writing of the same leftover
class is a different integral.
[`H1-SOT.md`](H1-SOT.md).
Plan: [`DOOR-B-H1-ESTIMATE-PLAN.md`](DOOR-B-H1-ESTIMATE-PLAN.md).
OPEN. Not a GR close. Not this
numerator.

---

## 7. What would kill this write

A sequence of admissible cylinders
with \(\mathcal G(Q_{r_n})\to\infty\).
Class: unaugmented NS (or a field
the leftover is tested on).
Quantity: \(A_{\mathrm{bad}}\).
Remainder: the same denominator
as \(\mathcal G\).

Not a kill:

- a large finite \(\mathcal G\)
- ABC_λ, or any screenshot of it
- a Beltrami tube number
- HH→L \(\mathcal R_\star\sim\beta/\alpha\)
- occupancy \(55/56\)
- Ring Lemma (REPAIR)
- selection / evolution language
- SFE, HB, \(Q_1\), or any other PDE

---

## 8. Automatic refuse

The machine refuses a paragraph that
needs any of:

- leftover 1 sold as a finished theorem
- P1, P1-loc, or PC cashed as the write
- CS \(E^{3/2}\) cashed as shape 1
- generic-field Lemma J cashed
  as shape 2
- an imposed wait cashed as shape 3
- Ring quoted as a sitting bound
- glue to \(\mathcal R_\star\) or
  to \(H_N\)
- \(K(t)\) in the PDE
- a start from the ABC_λ table
- drop the class and claim
  unrestricted regularity

KEEP may enter: the local identity,
the split, Lemma C as an *if*,
P1 / P1-loc / PC as cousins,
the three shapes as estimates,
\(\mathcal G\) as the locked ratio.

---

## 9. Status

| Item | Verdict |
|---|---|
| Write stated | **pass** (aimed leftover) |
| Write proved | **fail** |
| \(\mathcal G\) locked | **pass** (definition) |
| \(\sup\mathcal G<\infty\) | **open** |
| Hölder cut spent once | **pass** (arithmetic) |
| P1 / P1-loc / PC | **pass** as cousins; **fail** as H1 |
| Shapes 1–3 | **open** |
| Outside-\(\mathcal{E}\) | **blocked** |
| Cylinder | **open** (needs C+\(R_\phi\), this write, H2, H3) |

NS not solved. H1 not a theorem.
The door is named. The last line
is not written.
