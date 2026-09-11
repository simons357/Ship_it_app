# Requested Young line — figured out, not written

11 September 2026.
**Not a close. NS not solved.
The chain stays a chain.**

Axisymmetric-with-swirl Navier–Stokes,
unaugmented, on \(\mathbb{R}^3\); quantity
\(Z_j=\|\Delta_j\omega\|_{L^2(\mathbb{R}^3)}^2\);
remainder \(T_{j\leftarrow j}\); [no extra
field]. Request:

\[
\lvert T_{j\leftarrow j}\rvert
\le
\varepsilon\nu P_j+R,
\]
with \(R\) from energy, \(Z\), and maybe
a direction factor — not \(\dot Z_j\),
not \(\Lambda'\). Read \(P_j\) as the
seated slot \(D_j=\|\nabla\Delta_j\omega\|_2^2\).

What was figured out: the local block
splits, the energy-only \(R\) is
**false**, and \(\alpha Z_j\) is sharp
for the main stretch. The allowed \(R\)
still cannot host the commutators.
The line is **not seated**.

Filter: [`ESTIMATE-AUDIT.md`](ESTIMATE-AUDIT.md).
Shell page: [`AXISYM-SHELL.md`](AXISYM-SHELL.md).
Probe: `python3 scripts/tjj_estimate.py`

This is not Lemma★. This is not H1 /
WRITE (6). Do not glue those three.

---

## 1. Split that sits

Write \(u_{\mathrm{loc}}=(\Delta_{j-1}+\Delta_j+\Delta_{j+1})u\).
Then \(\Delta_j\omega_{\mathrm{loc}}=\Delta_j\omega\),
and \(u_{\mathrm{loc}}\) stays
divergence-free.

**Proposition TJJ-Trans.**
\[
\int\bigl(u_{\mathrm{loc}}\cdot\nabla\bigr)\Delta_j\omega\cdot\Delta_j\omega=0.
\]
The main transport term vanishes.
Only the commutator
\([\Delta_j,u_{\mathrm{loc}}\cdot\nabla]\)
remains from transport.

**Proposition TJJ-α.**
\[
\int\bigl((\Delta_j\omega)\cdot\nabla u_{\mathrm{loc}}\bigr)\cdot\Delta_j\omega
=
\int\alpha_{\mathrm{loc},j}\,\lvert\Delta_j\omega\rvert^2,
\]
where
\(\alpha_{\mathrm{loc},j}=\xi_j\cdot S(u_{\mathrm{loc}})\,\xi_j\)
and \(\xi_j=\Delta_j\omega/\lvert\Delta_j\omega\rvert\)
on \(\{\Delta_j\omega\neq 0\}\).
The antisymmetric part of \(\nabla u\)
drops. This is an identity, not a bound.

Lattice check (`scripts/tjj_estimate.py`,
vortex blob, \(n=32\)): transport
residual \(10^{-23}\); stretch versus
\(\int\alpha\lvert\omega_j\rvert^2\)
residual \(0\).

So
\[
T_{j\leftarrow j}
=
\int\alpha_{\mathrm{loc},j}\,\lvert\Delta_j\omega\rvert^2
+
T_{j\leftarrow j}^{\mathrm{comm}}.
\]

---

## 2. What is true, and is not the request

Young on the transport commutator,
constants from \(\varphi\) only:

\[
\lvert T_{j\leftarrow j}^{\mathrm{comm,\,trans}}\rvert
\le
\varepsilon\nu D_j
+
C_\varepsilon[\varphi]\,\nu^{-1}\|u_{\mathrm{loc}}\|_\infty^2 Z_j.
\]

The main stretch is one-sided:
\[
\int\alpha_{\mathrm{loc},j}\,\lvert\Delta_j\omega\rvert^2
\le
\|(\alpha_{\mathrm{loc},j})_+\|_\infty Z_j.
\]
Neighbor-shell stretch commutators are
at most
\(C[\varphi]\,\|\nabla u_{\mathrm{loc}}\|_\infty\sum_{|k-j|\le 1}Z_k\).

**Proposition TJJ-template.**
\[
T_{j\leftarrow j}
\le
\varepsilon\nu D_j
+
\|(\alpha_{\mathrm{loc},j})_+\|_\infty Z_j
+
C_\varepsilon[\varphi]\,\nu^{-1}\|u_{\mathrm{loc}}\|_\infty^2 Z_j
+
C[\varphi]\,\|\nabla u_{\mathrm{loc}}\|_\infty\sum_{|k-j|\le 1}Z_k.
\]

This inequality sits. Its remainder is
**not** the allowed \(R\):
\(\|u_{\mathrm{loc}}\|_\infty\) and
\(\|\nabla u_{\mathrm{loc}}\|_\infty\)
are not energy, not \(Z\), and not a
direction factor. Bernstein puts
\(2^{3j}\) or \(2^{j/2}Z^{1/2}\) back
in. That is the cubic wall.

Door 3: a printed \(\alpha\) is a
criterion. \(\|(\alpha)_+\|_\infty\) is
not controlled by energy or by
\(\{Z_k\}\) (\(W^{1,2}\not\subset L^\infty\)).

---

## 3. Energy-linear \(R\) is false

The line that would have finished the
shell budget is
\[
\lvert T_{j\leftarrow j}\rvert
\le
\varepsilon\nu D_j+C\,\mathcal E\,Z_j.
\]
It is not open. It is **false** as a
uniform bound (\(C,\varepsilon\)
independent of the field and of \(j\)).

**Proposition TJJ-E-false.**
Let \(\varphi\) be smooth, compactly
supported, divergence-free, and not
identically zero. Set
\(u^\lambda(x)=\lambda^{3/2}\varphi(\lambda x)\).
Then \(\mathcal E\) is invariant,
the occupied shell is \(j\sim\log_2\lambda\),
and
\[
Z_{j(\lambda)}\sim\lambda^2,\qquad
D_{j(\lambda)}\sim\lambda^4,\qquad
T_{j(\lambda)\leftarrow j(\lambda)}\sim\lambda^{9/2}.
\]
Hence
\[
\frac{\lvert T_{j\leftarrow j}\rvert}{\varepsilon\nu D_j+C\,\mathcal E\,Z_j}
\sim\lambda^{1/2}\to\infty
\qquad(\lambda\to\infty).
\]

The same scaling shows
\(\|(\alpha)_+\|_\infty Z_j\sim\lambda^{9/2}\)
is sharp for the main stretch: strain
is \(\sim\lambda^{5/2}\). Direction
matches the leftover size and is not
an integrable coefficient from the
energy inequality.

\(1/r^4\) Hardy on the swirl source
does not repair this. Localized Hardy
fails on slow fat swirl
([`SWIRL-PAPER.md`](SWIRL-PAPER.md) §6;
[`UNAUGMENTED-R4-VORTICITY-PLAN.md`](UNAUGMENTED-R4-VORTICITY-PLAN.md)).

---

## 4. Forbidden slots stay out

AS-Id:
\(T_j=\tfrac12\dot Z_j+\nu D_j\).
Bounding \(T_{j\leftarrow j}\) by
\(\dot Z_j\) restates the identity.

\(\Lambda'=2(T_c-\nu\mathcal D_s)/X\)
already contains the leftover. Not this
LHS. No closed time series on this
door. The sign of \(\Lambda'\) is not
quoted.

---

## 5. Verdict

The request asked for one estimate
whose \(R\) is only energy, \(Z\), and
maybe \(\alpha\).

- Energy plus viscosity: **false**
  (Proposition TJJ-E-false).
- Direction \(\alpha Z_j\): true for
  the main stretch, uncontrolled, and
  does not eat the commutators.
- Commutators: need
  \(\|u_{\mathrm{loc}}\|_\infty\) or
  \(\|\nabla u_{\mathrm{loc}}\|_\infty\),
  which are not on the allowed list.
- \(\dot Z_j\), \(\Lambda'\): discarded.

**The estimate cannot be written.**
AS_remainder stays **fail**.
EAud_door1_closed stays **fail**.
The chain stays a chain.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| TJJ_transport_vanishes | **pass** | Proposition TJJ-Trans |
| TJJ_stretch_is_alpha | **pass** | Proposition TJJ-α |
| TJJ_template | **pass** | §2 inequality; remainder not allowed |
| TJJ_energy_visc_false | **pass** | energy-linear \(+\) viscosity is false |
| TJJ_requested_line | **fail** | allowed \(R\) is not seated |
| TJJ_forbidden_slots | **pass** | \(\dot Z_j\) and \(\Lambda'\) not used as a bound |
| TJJ_direction | **fail** | \(\alpha\) is Door 3, still a criterion |
| TJJ_chain | **pass** | HAVE / WRITE / THEN stay a chain |
| TJJ_ns_solved | **fail** | class and \(\rho_j\) stay in the sentence |

NS not solved.
The chain stays a chain.
