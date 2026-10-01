# Gate 83 — specimen-1 8×8 minor

**27 September 2026.** Data. Not a regularity proof.
Ordinary NS is not solved. Soft X silent.

Machine: `scripts/da_gate_83_minor_factor.py`.
JSON: `results/da_gate_83_minor_factor.json`.

Does **not** alter locked SBP / \(\phi/d\) / low-tail / sign /
\(S_{pq}\) / local exact-shell ★ / 71E packets.

---

## Generators and Jacobian

\(G_1,\dots,G_6\): the six pairwise space-diagonal collinearities
of the four pairs
\((000,111),\ (100,011),\ (010,101),\ (001,110)\).

\(G_7,\dots,G_{12}\): the six face-diagonal collinearities.

Gauge: \(a=(1,0,0)\), \(p_0=(r_1,r_2,r_3)\), \(b=(b_1,b_2,0)\),
\(d=(d_1,d_2,\lambda)\). Polarization chart
\(U_p=(p\times e_1)+z\,(p\times(p\times e_1))\).

\[
J_{\mathcal L}
=
D_{(z_0,\ldots,z_7,\lambda)}
(G_1,\ldots,G_{12})
\Big|_{\lambda=0,\;z_0=\cdots=z_7=t}.
\]

---

## Specimen 1

\[
t=1,\quad
r=(1,2,3),\quad
b=(0,1),\quad
d=(2,3).
\]

Exact rank of \(J_{\mathcal L}\) at this point: \(9\).

First exact-nonzero \(8\times 8\) pivot:

- rows \((0,1,2,3,4,6,7,8)\)
  i.e. \(G\in\{C_{01},C_{02},C_{03},C_{12},C_{13},F_{ab0},F_{ab1},F_{ad0}\}\)
- columns \((1,2,3,4,5,6,7,8)\) — drop \(\partial/\partial z_0\)

Exact determinant:

\[
M
=
-1800283866071764628484124381981399482114048
\neq 0.
\]

Of the \(220\) full \(9\times 9\) minors, \(200\) are nonzero.

---

## Verdict

\[
\boxed{M\not\equiv 0}
\]

Generic rank is at least \(8\) (and is \(9\) at specimen 1).
That is a Zariski-open local-trap result on this minor.

The same minor was **not** factored over
\(\mathbb Q[t,r_1,r_2,r_3,b_1,b_2,d_1,d_2]\) — the factorization
did not land.
No exceptional locus \(\mathcal E_{83}=\{Q=0\}\) is named.
This is not \(M=H_{\mathrm{known}}Q\) and not \(M\equiv 0\).

**NS not solved.**
