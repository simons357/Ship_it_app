# Axisymmetric shell estimate

11 September 2026.
**Not a close. NS not solved.
Remainder is open.**

Axisymmetric-with-swirl Navier–Stokes,
unaugmented, on \(\mathbb{R}^3\); quantity
\(Z_j=\|\Delta_j\omega\|_{L^2(\mathbb{R}^3)}^2\);
remainder \(T_{j\leftarrow j}\); [no extra
field]; Young only on the far shells, with
named constants \(C_{\mathrm{IR}}[\varphi]\)
and \(C_{\mathrm{UV}}[\varphi]\).

Filter: [`ESTIMATE-AUDIT.md`](ESTIMATE-AUDIT.md).
Probe: `python3 scripts/axisym_shell.py`

This is not Lemma★. This is not H1 /
WRITE (6). This is not unrestricted
three-dimensional regularity. Do not glue
those three. Do not add a field.

---

## 1. Class and equation

Let \(u\) be smooth, divergence-free,
rapidly decreasing, and invariant under
rotations about \(e_3\), with swirl:
\[
u=u^r(r,z,t)\,e_r+u^\theta(r,z,t)\,e_\theta+u^z(r,z,t)\,e_z.
\]
Keep the \(1/r^4\) Biot–Savart kernel.
The equation is
\[
\partial_t u+(u\cdot\nabla)u=-\nabla p+\nu\Delta u,
\qquad\nabla\cdot u=0,
\]
\(\nu>0\), no force, no extra stress.
\(\omega=\nabla\times u\).

Littlewood–Paley: a fixed radial bump
\(\varphi\), projectors \(\Delta_j\),
\(S_m=\sum_{k\le m}\Delta_k\), \(j\in\mathbb{Z}\).
Write
\[
u_{\mathrm{IR}}=S_{j-2}u,\qquad
u_{\mathrm{loc}}=(\Delta_{j-1}+\Delta_j+\Delta_{j+1})u,\qquad
u_{\mathrm{UV}}=u-u_{\mathrm{IR}}-u_{\mathrm{loc}},
\]
and the same split of \(\omega\).

Swirl is the class that removes *free*
helical HHH: a field with
\(\widehat u(R_\theta\xi)=R_\theta\widehat u(\xi)\)
cannot carry three independent helical
amplitudes on a generic triad. That is a
restriction on the allowed set. It is not
a bound on \(T_{j\leftarrow j}\).

---

## 2. Identity

The one term that can grow \(Z_j\) is the
full shell pairing \(T_j\) below. It is
not bounded by \(\dot Z_j\), by
\(\Lambda'\), or by a new symbol of the
same size.

**Proposition AS-Id.** On this class,
\[
\tfrac12\dot Z_j+\nu D_j=T_j,
\qquad
D_j=\|\nabla\Delta_j\omega\|_2^2,
\]
\[
T_j=\langle\Delta_j(\omega\cdot\nabla u-u\cdot\nabla\omega),\Delta_j\omega\rangle.
\]

Bookkeeping that already sits, and is
*not* this left-hand side:
\[
\Lambda'=\frac{2}{X}(T_c-\nu\mathcal D_s).
\]
No time series of that identity is closed
on this page. The sign of \(\Lambda'\) is
not quoted.

---

## 3. Door 1 — shell split

Let \(B(a,b)=a\cdot\nabla b-b\cdot\nabla a\)
on the vorticity–velocity pair, and write
\(B(u):=B(\omega,u)\). Partition

\[
\begin{aligned}
T_{j\leftarrow\mathrm{IR}}
&=\langle\Delta_j\bigl(B(u)-B(u-u_{\mathrm{IR}})\bigr),\Delta_j\omega\rangle,\\
T_{j\leftarrow j}
&=\langle\Delta_j B(u_{\mathrm{loc}}),\Delta_j\omega\rangle,\\
T_{j\leftarrow\mathrm{UV}}
&=\langle\Delta_j\bigl(B(u-u_{\mathrm{IR}})-B(u_{\mathrm{loc}})\bigr),\Delta_j\omega\rangle.
\end{aligned}
\]

**Proposition AS-Split.** These three
lines are disjoint and exhaust \(T_j\):
\[
T_j=T_{j\leftarrow\mathrm{IR}}+T_{j\leftarrow j}+T_{j\leftarrow\mathrm{UV}}.
\]
The only remainder after the next two
lemmas is \(T_{j\leftarrow j}\).

This is Audit Door 1. It is not
Attack-6 Door 1 (uniform pre-Young \(C\)),
which is off.

---

## 4. Young on the far shells

Constants depend only on \(\varphi\).

**Lemma AS-IR.** There exists
\(C_{\mathrm{IR}}=C_{\mathrm{IR}}[\varphi]<\infty\)
such that
\[
\lvert T_{j\leftarrow\mathrm{IR}}\rvert
\le
C_{\mathrm{IR}}
\Bigl(\sum_{k\le j-2}2^{3k/2}Z_k^{1/2}\Bigr)Z_j
+
C_{\mathrm{IR}}
\Bigl(\sum_{k\le j-2}2^{k/2}Z_k^{1/2}\Bigr)D_j^{1/2}Z_j^{1/2}.
\]
Hölder on stretching and transport;
Bernstein on the infrared pieces;
commutator \([\Delta_j,u_{\mathrm{IR}}\cdot\nabla]\)
absorbed into the same \(C_{\mathrm{IR}}\).

Young on the infrared *transport* piece
only:
\[
C_{\mathrm{IR}}\|u_{\mathrm{IR}}\|_\infty D_j^{1/2}Z_j^{1/2}
\le
\frac\nu4 D_j
+\frac{C_{\mathrm{IR}}^2}{\nu}\|u_{\mathrm{IR}}\|_\infty^2 Z_j.
\]
That absorption is not an estimate of
\(T_{j\leftarrow j}\).

**Lemma AS-UV.** There exists
\(C_{\mathrm{UV}}=C_{\mathrm{UV}}[\varphi]<\infty\)
such that
\[
\lvert T_{j\leftarrow\mathrm{UV}}\rvert
\le
C_{\mathrm{UV}}
\sum_{\ell\ge j+2}
2^{j-\ell/2}
Z_\ell\,Z_j^{1/2}.
\]
Bernstein gain on a high–high product
read at frequency \(2^j\). If a later
check moves the exponent by a fixed
shift, enlarge \(C_{\mathrm{UV}}\). Do
not move that shift onto the local block.

---

## 5. Local block — identities, not bounds

On a closed triad of frequencies
\(\xi+\eta+\zeta=0\), write the scalar
coupling of the local pairing as
\[
\tau=(\omega(\xi)-\omega(\zeta))J_\xi+(\omega(\eta)-\omega(\zeta))J_\eta.
\]
Here \(\omega(\,\cdot\,)\) is a frequency
weight on that triad and \(J_\xi,J_\eta\)
are the couplings from the other two legs.

**Proposition AS-τ.** This is an algebraic
rewrite of one triad’s contribution. It
does not bound \(\tau\).

**Proposition AS-ω\*.** For any constant
\(\omega_*\in\mathbb{R}\),
\[
\tau(\omega-\omega_*)=\tau(\omega).
\]
Shift by a fixed frequency, not by
\(\Lambda\). The identity does not
smallen \(T_{j\leftarrow j}\).

---

## 6. Door 3 is a criterion

Alignment
\(\alpha=\xi\cdot S_{\mathrm{strain}}\xi\)
is a number one may print. It is kept
separate from triad-phase occupancy.
Neither is Constantin–Fefferman. A
printed \(\alpha\) is not a bound on
\(T_{j\leftarrow j}\).

---

## 7. Extra hypothesis, in the open

**[ρ]** Assume that on \(\{Z_j>0\}\),
\[
\rho_j(t)=\frac{(T_{j\leftarrow j})_+(t)}{Z_j(t)}
\]
satisfies \(\int_0^T\rho_j(t)\,dt<\infty\),
for each \(j\), and that the infrared sum
in Lemma AS-IR is finite on \([0,T]\).

**Theorem AS-ρ (conditional).** Under
[ρ], after Lemma AS-IR, the transport
Young, and Lemma AS-UV, \(Z_j\) stays
finite on \([0,T]\).

A conditional theorem is a theorem.
[ρ] is not a smallness that was
measured for the class. Visibility of
cancellation is not uniform smallness.

---

## 8. Galerkin truncation

**Theorem AS-Gal.** Let \(u^N\) be a
smooth solution of the spectral Galerkin
truncation of this equation with
frequencies \(|\xi|\le 2^N\), still
axisymmetric with swirl, unaugmented,
on \(\mathbb{R}^3\). Let
\(Z_j^N=\|\Delta_j\omega^N\|_2^2\) for
\(j\le N-2\). Then Proposition AS-Id,
Proposition AS-Split, Lemma AS-IR, and
Lemma AS-UV hold for \(u^N\), with the
same \(C_{\mathrm{IR}}[\varphi]\) and
\(C_{\mathrm{UV}}[\varphi]\) — independent
of \(N\), of \(\nu\), and of \(u^N\).
The remainder is still \(T_{j\leftarrow j}^N\).
Scope: this truncation, this class, this
remainder. Constants named above.

---

## 9. What was measured

The probe checks the pairing algebra on
the integer lattice \(\mathbb{Z}^3\)
(normalized \(\mathbb{T}^3\)). That is
not the manifold of §§1–8. It is the
energy-conservation check: if the
diagnostic residual is larger than
\(10^{-16}\) relative to the pairing
scale, the identity is not closed and
no sign of \(\Lambda'\) is quoted.

Printed on the samples that were run
(not a class bound; a number may come
out the other way). Lattice, \(n=16\),
seed \(1390\). Pairing residual
\(\le 3\times 10^{-19}\) relative.
Split error \(0\). Not \(\rho_j\) for
the \(\mathbb{R}^3\) class.

- energy pairing residual, and
  \(\sum_j T_j\) residual;
- shell block
  \(T_{j\leftarrow j}/X_j\) on energy
  shells, and
  \(T_{j\leftarrow j}^{Z}/Z_j\) on
  enstrophy shells;
- mean alignment \(\alpha\) on the set
  where \(|\omega|\) exceeds a threshold.

| sample | \(\max\lvert T_{j\leftarrow j}/X_j\rvert\) | \(\max\lvert T_{j\leftarrow j}^{Z}/Z_j\rvert\) | \(\overline{\alpha}\) |
|---|---|---|---|
| random div-free | \(0.090\) | \(0.084\) | \(0.013\) |
| 4-fold about \(z\) | \(0.014\) | \(0.017\) | \(-0.0085\) |
| Taylor–Green-like | \(6\times 10^{-20}\) | \(3\times 10^{-19}\) | \(0\) |

The random field can come out larger
than the 4-fold field. Both are allowed
in as printed measurements. Neither
closes [ρ].

Named in the audit and **not
regenerated** here:

- 2-D adversary
  \(\lvert T_c\rvert/\mathcal D_s\sim 0.017\),
  occupancy \(\sim 0.15\). 2-D stays 2-D.
- 3-D random-phase ratio \(O(10^{-2})\),
  HHH occupancy 1 on the orbits that
  were run, \(\alpha\approx 0.5\).
  Those orbits stay those orbits.
  Occupancy 1 is not imported into
  Constantin–Fefferman.

---

## 10. What is not claimed

- \(T_{j\leftarrow j}\) is small.
- [ρ] holds for the class.
- Unrestricted three-dimensional
  regularity.
- A close of Lemma★ or of H1.
- A bound of the local block by
  \(\Lambda'\) or by \(\dot Z_j\).

If a paragraph needs an object from the
discard list of
[`ESTIMATE-AUDIT.md`](ESTIMATE-AUDIT.md)
to move — including as motivation —
that paragraph is out.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| AS_identity | **pass** | Proposition AS-Id |
| AS_split | **pass** | Door 1 partition |
| AS_young_IR | **pass** | \(C_{\mathrm{IR}}[\varphi]\) named |
| AS_young_UV | **pass** | \(C_{\mathrm{UV}}[\varphi]\) named |
| AS_tau | **pass** | rewrite, not a bound |
| AS_omega_star | **pass** | shift by a constant, not by \(\Lambda\) |
| AS_pairing_check | **pass** | residual printed; lattice, not \(\mathbb{R}^3\) |
| AS_remainder | **fail** | \(T_{j\leftarrow j}\) open |
| AS_rho | **fail** | [ρ] is assumed, not measured for the class |
| AS_door3 | **fail** | \(\alpha\) is a criterion |
| AS_ns_solved | **fail** | class and \(\rho_j\) stay in the sentence |

NS not solved.
