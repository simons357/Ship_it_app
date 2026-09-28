# Gate 83B-2b — curvature of the cocircular kernel

**28 September 2026.** Data plus one structural identity.
Ordinary NS is not solved. DA-NS-2 stays **OPEN**.
Unrestricted \(\sup\mathcal R_\star<\infty\) stays **KILLED**.
Soft X silent.

Machine: `scripts/da_gate_83b2b_curvature.py`.
JSON: `results/da_gate_83b2b_curvature.json`.
Desk card:
[`../../packets/DA-GATE-83B2B-CURVATURE-2026-09-28.md`](../../packets/DA-GATE-83B2B-CURVATURE-2026-09-28.md).

Does **not** alter locked SBP / \(\phi/d\) / low-tail / sign /
\(S_{pq}\) / local exact-shell ★ / 71E packets.
Does **not** close (83.34). Gate 81 census is not recomputed.

---

## The cheap test

At an active point \(x_0\) with extra right kernel \(v\),

\[
x(s)=x_0+s\,v+s^2 w+O(s^3),
\qquad
A=\mathrm{D}F(x_0),\qquad
Av=0.
\]

The order-\(s^2\) solvability condition is

\[
A w=-\tfrac12\mathrm{D}^2F[v,v],
\qquad
\ell^T A=0
\;\Rightarrow\;
\ell^T\mathrm{D}^2F[v,v]=0.
\]

If that pairing is nonzero, a rank drop is not a branch.
If it vanishes, one solves for \(w\) and goes to cubic order.

---

## Structural fact (exact)

The nine raw cube triples \(F=(C_1,C_2,C_3,F_1,\dots,F_6)\) are
**affine in each single polarization coordinate** \(z_i\). On the
locked lattice every pure second derivative vanishes:

\[
\mathrm{D}^2F[e_{z_i},e_{z_i}]\equiv 0.
\]

So for \(v=e_{z_i}\) the Lyapunov–Schmidt pairing is automatic:

\[
\boxed{\ell^T\mathrm{D}^2F[v,v]=0}.
\]

Moreover, \(\partial F/\partial z_i\) is independent of \(z_i\).
If that whole column vanishes at \(x_0\), then \(F\) is independent
of \(z_i\) and the kernel integrates at once:

\[
F(x_0)=0,\;
\partial_{z_i}F(x_0)=0
\;\Rightarrow\;
F(x_0+s\,e_{z_i})=0
\quad\text{for all }s.
\]

There is no cubic obstruction in a pure \(z_i\) direction.
The circle is not a tangent illusion once a column vanishes.

---

## Locked lattice (exact)

Gauge \(a=(1,0,0)\), \(b=(b_1,b_2,0)\), \(d=(d_1,d_2,\lambda)\).
Seated node order \(000,010,001,011,100,110,101,111\).

\[
\begin{aligned}
r&=p_0=\bigl(-\tfrac12,\;\tfrac65,\;\tfrac65\bigr),\\
b&=\bigl(\tfrac12,\;\tfrac1{10}\bigr),\\
d&=\Bigl(-\tfrac14-\frac{3\sqrt{113}}{452},\;
-\tfrac54+\frac{45\sqrt{113}}{452}\Bigr),\\
\lambda&=-\tfrac{12}{5},
\qquad
\Delta=b_2\lambda=-\tfrac6{25}\neq 0.
\end{aligned}
\]

The five horizontal projections

\[
p_{000,h},\;p_{100,h},\;p_{010,h},\;p_{001,h},\;p_{111,h}
\]

lie on the circle of radius \(13/10\) centred at the origin
(\(X^2+Y^2=169/100\) identically over \(\mathbb Q(\sqrt{113})\)).
The other three vertices do **not** lie on that circle.

This is a detached cube, not a point of the 71E thickening.
The reduced \(\lambda\)-chart through \(\mathfrak p_{71E}\) stays
empty of volumetric hits, as previously recorded.

---

## Witness (numerical polarizations, exact line)

On that lattice there is a real active zero of the nine raw
triples with every one of the 16 cube pairs live
(\(\min|W|\approx 0.4508\)). The \(9\times 8\) \(z\)-Jacobian
has rank \(7\). The extra kernel is

\[
v=e_{z_4}=e_{p_{100}}.
\]

The entire \(z_4\) column vanishes. The \(z_7=p_{111}\) column
does **not**. In binary \(i\)-major order the free node is
\(z_1=p_{100}\) (the reflected locus). A \(p_{111}\) kernel was
not found on this lattice.

Because \(F\) is affine in \(z_4\) and the column is zero,

\[
\boxed{F(x_0+s\,e_{z_4})=0}
\]

for every real \(s\). Activity is constant along the line
(the four pairs that see node \(100\) keep \(\min|W|\) fixed).
Checked at \(s\in\{-3,-1,0,1,3\}\): raw residuals
\(\lesssim 10^{-13}\), all 16 live.

The complementary seven polarizations are locked numerically
(high-precision least squares, \(z_4=0\) slice). They have not
been written as elements of \(\mathbb Q(\sqrt{113})\). The
**line** is exact once any one point on it is a zero; the
column-vanishing plus affinity do that work.

---

## Board

```
GATE 83B-2b
──────────────────────────────────────────
λ-chart through 71E     EMPTY of volumetric ✓
Δ ≠ 0, 13/10 lattice    EXACT ✓
cocircular five         EXACT ✓
all 16 active           YES ✓
rank Dz F               7
extra kernel            e_{z4} = e_{p100}
reflected (i-major z1)  SAME NODE ✓
p111 = z7 kernel        NOT ON THIS LATTICE
F affine in each z_i    YES ✓
ℓ^T D²F[v,v]            0 (structural)
branch in v             EXACT LINE ✓
GLOBAL RANK-8 TRAP      DEAD
POLARIZATION ESCAPE     YES (detached cube)
LATTICE BRANCH AT 71E   OPEN (83.34)
z1 ... z6 other loci    INCOMPLETE
```

\[
\boxed{\text{GLOBAL RANK-8 TRAP: FALSIFIED}}
\]

\[
\boxed{\text{DETACHED VOLUMETRIC POLARIZATION LINE: ESTABLISHED}}
\]

\[
\boxed{\text{71E LATTICE ESCAPE: NOT YET ESTABLISHED}}
\]

A rank drop on this cube **does** give a branch, because the
equations are affine in the kernel coordinate. That branch
moves only the polarization of \(p_{100}\). It does not thicken
71E, and it does not by itself restore unrestricted \(\star\).

**NS not solved.**
