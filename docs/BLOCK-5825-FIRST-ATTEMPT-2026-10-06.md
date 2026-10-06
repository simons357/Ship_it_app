# One regenerated block first: \((5,8,25)\)

6 October 2026.
**Concrete proof attempt. Not a bound on (17). NS not solved.**

Start with one complete regenerated scalene block from the
PR #165 / \(K=2\) all-high jet. Second target
\((5,10,25)\) is not treated here.

Parents:
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md) (7), (14), (15)–(17);
[`ALL-HIGH-T6-K2-DATUM-2026-10-06.md`](ALL-HIGH-T6-K2-DATUM-2026-10-06.md);
[`DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md`](DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md);
[`SIGNED-SCALENE-NEXT-ATTACK.md`](SIGNED-SCALENE-NEXT-ATTACK.md).

Census:
`scripts/ns_attacks/block_5825_census.py`
→ `BLOCK-5825-CENSUS.json`.

---

## RESULT (attempt, not a close)

1. The signed evolution of the complete \((5,8,25)\) block
   is written exactly from (7) and (14), with every
   receiver and with forcing split by source.
2. Viscosity **does** match the linear slots. It does
   **not**, by energy and the three shell \(L^2\)
   quantities alone, absorb the **external** quartic
   forcing without a frequency-growing or high-norm
   factor. Intra-block forcing on this **finite**
   triangle set is the part that can be estimated
   without occupancy and that **survives** frequency
   dilation at fixed energy.
3. A crude energy bound on the external forcing
   reintroduces a factor that grows with frequency.
   That is the named next obstruction — before
   summing blocks or repeated episodes.

(17) remains **OPEN**. This page does not claim a
positive \([\mathcal T_{\mathrm{sc}}-\nu Y/4]_+\)
episode.

---

## 1. Exact signed evolution of the block

Let \(a=5\), \(b=8\), \(c=25\). Lattice census
(integer modes, \(p+q+r=0\)):

| Shell \(|k|^2\) | Mode count |
|---|---:|
| \(5\) | \(24\) |
| \(8\) | \(12\) |
| \(25\) | \(30\) |
| Oriented triples \((p,q,r)\) | \(24\) |

Sample triangle: \(p=(-2,-1,0)\), \(q=(-2,-2,0)\),
\(r=(4,3,0)\). All such triples lie in coordinate
planes (one vanishing Cartesian component).

On the same indexed set as vault (7),

\[
I_p
=\sum_{\substack{p+q+r=0\\ \lvert p\rvert^2=a,\,\lvert q\rvert^2=b,\,\lvert r\rvert^2=c}}
\operatorname{Im}\bigl[(q\cdot u_p)(u_q\cdot u_r)\bigr],
\]

and cyclically \(I_q\), \(I_r\). The complete signed
block (every receiver, both Fourier signs, negative
triples included in the index set) is

\[
\boxed{
\mathcal T_{5,8,25}
=(c-b)I_p+(a-c)I_q+(b-a)I_r
=17\,I_p-20\,I_q+3\,I_r.
}
\tag{B7}
\]

Galerkin NSE on each mode,
\(\partial_t u_k=-\nu\lvert k\rvert^2 u_k-\widehat B(u,u)(k)\).
Differentiating the trilinear form (B7) puts
\(-\nu\lvert k\rvert^2 u_k\) in each slot and
reproduces the viscous identity in (14):

\[
\boxed{
\dot{\mathcal T}_{5,8,25}+\nu(a+b+c)\mathcal T_{5,8,25}
=\mathcal Q_{5,8,25,N},
}
\qquad
a+b+c=38.
\tag{B14}
\]

The quartic \(\mathcal Q\) is the same trilinear
form with **one slot replaced by \(-\widehat B(u,u)\)**
in each of the three positions, summed. Inputs of
\(\widehat B\) are **not** confined to the three
shells. A Duhamel factor \(1/(38\nu)\) does not by
itself bound the integrated budget (15).

On the \(K=2\) witness, \(\mathcal T_{5,8,25}(0)=0\)
(those shells are empty). The block is forced.

---

## 2. Split the forcing (every source named)

Write \(u=u_{\mathrm{block}}+u_{\mathrm{rest}}\) with
\(u_{\mathrm{block}}\) the projection onto squared
radii \(\{5,8,25\}\). Then

\[
\widehat B(u,u)
=B(\mathrm{block},\mathrm{block})
+B(\mathrm{block},\mathrm{rest})
+B(\mathrm{rest},\mathrm{block})
+B(\mathrm{rest},\mathrm{rest}).
\]

Correspondingly

\[
\mathcal Q
=\mathcal Q^{\mathrm{in}}+\mathcal Q^{\mathrm{low}}+\mathcal Q^{\mathrm{other}}.
\]

| Piece | Source of the inserted \(B\) | Status on this attempt |
|---|---|---|
| \(\mathcal Q^{\mathrm{in}}\) | both \(B\)-inputs on \(\{5,8,25\}\) | Finite \(24\) triangles. Occupancy does not grow under dilation of this support. |
| \(\mathcal Q^{\mathrm{low}}\) | at least one \(B\)-input with \(\lvert k\rvert\le K=2\) | Frozen-\(K\) low modes. Same shape as the seated fixed-low complement, but here feeding this block’s currents. |
| \(\mathcal Q^{\mathrm{other}}\) | other **high** shells (e.g. \(10\), and later radii) | Summing blocks / repeated episodes. Not absorbed on this page. |

Every receiver in (B7) is already assembled before
this split. Do not take \(\lvert\widehat B_k\rvert\)
before summing the three currents.

---

## 3. Viscosity vs energy and shell quantities

**Allowed:** \(E\), \(X\), \(Y\) of the full field;
shell energies \(e_5,e_8,e_{25}\); frozen \(K=2\);
exact geometry of this block. **Forbidden as
hypotheses:** a future bound on \(X(t)\),
\(\lVert u\rVert_\infty\), BKM, ESS, or (16).

### 3.1 Linear (viscous) slots — absorbed

By construction of (B14), the \(-\nu Au\) insertions
are exactly \(38\nu\,\mathcal T_{5,8,25}\). No
remainder. This is not the difficulty.

### 3.2 Intra-block quartic — finite, occupancy-free

On this named lattice block there are \(24\) oriented
triples, independent of a later dilation
\(k\mapsto\lambda k\) of the **same** support.

Hölder on that finite index set gives

\[
\lvert I_p\rvert
\le
\sqrt{b}\,C_\triangle (e_5 e_8 e_{25})^{1/2},
\]

with \(C_\triangle\) depending only on the finite
incidence of this block (not on a growing circle
fiber). Hence

\[
\lvert\mathcal T_{5,8,25}\rvert
\le
C_T\,c\,\sqrt{c}\,(e_5 e_8 e_{25})^{1/2}
\]

up to an absolute factor from \(\lvert c-b\rvert\)
etc. (\(c\) is the large squared radius). Likewise
\(\mathcal Q^{\mathrm{in}}\) is a finite sum of
products of four coefficients on these shells,
with **one** extra wavevector from \(B\).

**Frequency dilation at fixed energy.** Embed the
same \(24\) triangles at \(\lambda p,\lambda q,\lambda r\)
and keep the Fourier amplitudes (hence \(E_{\mathrm{block}}\))
fixed. Then

\[
a,b,c\sim\lambda^2,
\qquad
\mathcal T\sim\lambda^3\,\mathrm{amp}^3,
\qquad
\mathcal Q^{\mathrm{in}}\sim\lambda^4\,\mathrm{amp}^4,
\qquad
\nu(a+b+c)\lvert\mathcal T\rvert\sim\nu\lambda^5\,\mathrm{amp}^3.
\]

The ratio
\(\lvert\mathcal Q^{\mathrm{in}}\rvert\big/\bigl(\nu(a+b+c)\lvert\mathcal T\rvert\bigr)\)
is \(\sim\mathrm{amp}/(\nu\lambda)\) and **does not
grow** with \(\lambda\) at fixed amplitudes. Intra-block
forcing is **not** the frequency-growing obstruction.

This is **not** yet a time-integrated bound: \(e_5(t)\)
etc. are unknown. It only shows that a snapshot
majorant of \(\mathcal Q^{\mathrm{in}}\) in the three
shell energies has a constant compatible with
dilation.

### 3.3 External forcing — precise failure of energy-only absorption

\(\mathcal Q^{\mathrm{low}}+\mathcal Q^{\mathrm{other}}\)
inserts \(\widehat B\) with at least one input off
\(\{5,8,25\}\).

A crude bound \(\lvert\widehat B_k\rvert\le\lvert k\rvert E\)
(sum all pairs, discard signs) produces a factor
that **grows with frequency** in \(\mathcal Q\), and
reintroduces occupancy if one restores shells as
thick annuli. That majorant is rejected (Loss A /
Attack 8 counting, already mapped).

Using only \(E\) and \(X\) of the **full** field:
three-dimensional NSE does not give
\(\lVert u\rVert_\infty\) from \((E,X)\). Gagliardo–
Nirenberg \(\lVert u\rVert_3^4\le C\,EX\) returns
Foias–Temam-type powers of \(X\), which is circular
for the program that uses (17) to get (16).

**Low piece at frozen \(K=2\).** Inputs with
\(\lvert k\rvert\le 2\) have a bounded
\(C_K^2=\sum_{0<\lvert k\rvert\le 2}\lvert k\rvert^2\).
This is the same structure as the seated fixed-low
complement, now feeding \((5,8,25)\) rather than the
global \(C\). A Young allocation against
\(\nu Y\) **global** is possible in shape, but it
charges the **full** dissipation budget and does not
close a single-block remainder without controlling
the other high shells that share that \(\nu Y\).

**Verdict on step 2.** Viscosity absorbs the linear
slots exactly. Energy + \(\{e_5,e_8,e_{25}\}\) absorb
a dilation-stable majorant of \(\mathcal Q^{\mathrm{in}}\)
at the snapshot level. They do **not** absorb
\(\mathcal Q^{\mathrm{other}}\) (and do not honestly
absorb \(\mathcal Q^{\mathrm{low}}\) as a
**single-block** budget) without either (i) a
frequency-growing crude factor or (ii) a smoothness
/ future-\(X\) hypothesis. That is a **precise
failure** of an energy-only one-block close, not a
failure of the signed identities.

---

## 4. What would have to survive to continue

If a later write bounds \(\mathcal Q^{\mathrm{low}}\)
by frozen-\(K\) constants times global \(E,X\) **without**
eating the \(\nu Y/4\) already allocated to the
complement, and bounds \(\mathcal Q^{\mathrm{in}}\)
as in §3.2, the leftover is exactly
\(\mathcal Q^{\mathrm{other}}\): coupling to
\((5,10,25)\) and further regenerated shells.

That leftover is “summing blocks and repeated
episodes” — the missing work toward (17). Do not
pretend a Duhamel \(1/(38\nu)\) on this one block
sums those episodes.

---

## 5. Relation to the \(t^6\) jet

On the \(K=2\) witness the first all-high signed
transfer is
\(\mathcal T_{\mathrm{sc}}(h_2)=(15084/1625)t^6+O(t^7)\),
from **both** \((5,8,25)\) and \((5,10,25)\). A bound
on one block’s \(\mathcal T_{5,8,25}\) is necessary
but not sufficient even for that jet’s budget
integrand. The jet remains below \(\nu Y/4\)
initially; this attempt does not change that.

---

## STATUS

\((5,8,25)\) SIGNED EVOLUTION: WRITTEN (B7), (B14).
\(\mathcal Q\) SPLIT: IN / LOW / OTHER.
INTRA-BLOCK: FINITE; DILATION DOES NOT GROW THE CONSTANT.
EXTERNAL / OTHER-HIGH: ENERGY-ONLY ABSORPTION FAILS
(FREQUENCY-GROWING CRUDE FACTOR OR CIRCULAR \(X\)).
SUMMING BLOCKS + REPEATED EPISODES: STILL THE BLANK
TOWARD (17).
NS NOT SOLVED.
