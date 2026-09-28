# DA gate — 83D √113 spec for Heavy

**28 September 2026.** Spec only. Not a new witness.

Heavy’s 83D derivation is **PROVED** (internal, no factors
removed) and is **REPORTED** on this tree, not recomputed as a
Gröbner run. DA gates that reading:

- three radius conditions plus \(\mathcal G\)
- hinge-mode column identically zero in all 12 equations
- factorization \(-r_3^3 L^2(R_{111}-R_i)\)
- saturation removes only \(r_3=0\) and six activity factors
- fifth radius \(=\) three radius differences \(+\,2\mathcal G\)

The fifth-radius identity is **proved on this tree** as a
generic polynomial. The √113 cube is the specimen Heavy did
not have. JSON:
[`../results/da_gate_83d_sqrt113_spec.json`](../results/da_gate_83d_sqrt113_spec.json).
Page: [`../docs/ns-recovery/GATE-83D-HINGE.md`](../docs/ns-recovery/GATE-83D-HINGE.md).

## Lattice (exact)

\[
\begin{aligned}
a&=(1,0,0),\\
r&=p_0=\bigl(-\tfrac12,\;\tfrac65,\;\tfrac65\bigr),\\
b&=\bigl(\tfrac12,\;\tfrac1{10},\;0\bigr),\\
d&=\Bigl(-\tfrac14-\frac{3\sqrt{113}}{452},\;
-\tfrac54+\frac{45\sqrt{113}}{452},\;
-\tfrac{12}{5}\Bigr),\\
\lambda&=-\tfrac{12}{5},\qquad
\Delta=-\tfrac6{25},\qquad
\mathcal G=0,\\
R_{000}=R_{100}=R_{010}=R_{001}=R_{111}&=\tfrac{169}{100}.
\end{aligned}
\]

Companion root: \(u=(13+15\sqrt{113})/82\) on the 10-scaled
circle \(X^2+Y^2=169\), chord \(A=(-5,12)\), \(C=(0,13)\).

Seated \(z\)-order: \(000,010,001,011,100,110,101,111\).
On \(I_{\mathrm{act}}\) the vanishing column is seated
\(z_4=p_{100}\). Heavy’s hinge label \(z_7\) should be matched
against that dictionary, not assumed to be \(p_{111}\).

Polarization: \(U_p=(p\times e_1)+z(p\times(p\times e_1))\).
Raw \(W\), twelve generators as in the Gate 83 minor script.

Do not search for another cube. (83.34) stays **OPEN**.
**NS not solved.**
