# Requested Young line — not written

11 September 2026.
**Not a close. NS not solved.
The chain stays a chain.**

Axisymmetric-with-swirl Navier–Stokes,
unaugmented, on \(\mathbb{R}^3\); quantity
\(Z_j=\|\Delta_j\omega\|_{L^2(\mathbb{R}^3)}^2\);
remainder \(T_{j\leftarrow j}\); [no extra
field]. This page answers one request:

\[
\lvert T_{j\leftarrow j}\rvert
\le
\varepsilon\nu P_j+R,
\]
where \(R\) uses only energy, \(Z\), and
maybe a direction factor — not
\(\dot Z_j\), not \(\Lambda'\).

That line is **not seated**. Emitting it
as a theorem is the discarded WRITE.
Identity and far-shell Young already sit
in [`AXISYM-SHELL.md`](AXISYM-SHELL.md).
Filter: [`ESTIMATE-AUDIT.md`](ESTIMATE-AUDIT.md).

This is not Lemma★. This is not H1 /
WRITE (6). Do not glue those three.

---

## 1. What the symbols would have to mean

\(P_j\) is not a seated symbol on this
door. The only dissipative slot in
Proposition AS-Id is
\(D_j=\|\nabla\Delta_j\omega\|_2^2\).
Read the request as leftover form (3)
on the local block:

\[
\lvert T_{j\leftarrow j}\rvert
\le
\varepsilon\nu D_j+R.
\]

Older \(P_{j_*}=X_{j_*-1}+X_{j_*}+X_{j_*+1}\)
and hole-1 \(P_+\) are different objects.
They do not enter.

Allowed in an \(R\), if one existed:

- energy \(\mathcal E=\tfrac12\|u\|_2^2\),
  or a three-shell energy
  \(\mathcal E_{\mathrm{loc}}\);
- the family \(\{Z_k\}\), used as a
  *lower-order* term, not as
  \(\dot Z_j\);
- maybe a direction factor
  \(\alpha=\xi\cdot S_{\mathrm{strain}}\xi\).

Forbidden in \(R\) (audit DISCARD):

- \(\dot Z_j\) (the user’s \(\dot e_j\);
  no seated \(e_j\));
- \(\Lambda'=2(T_c-\nu\mathcal D_s)/X\);
- a new symbol of the same size as
  \(T_{j\leftarrow j}\).

Leftover form (3) already sits globally
as a *shape* in
[`NS-PROOF-CHAIN.md`](NS-PROOF-CHAIN.md):
\[
\frac{d}{dt}X+\nu\|\nabla\omega\|_2^2
\le\varepsilon\nu\|\nabla\omega\|_2^2
+C_\varepsilon X\cdot\mathcal R(t).
\]
HAVE (3) is not WRITE of the local
block. The request is exactly that
missing Young.

---

## 2. Verdict

**The estimate cannot be written.**

No identity, Young step, or measurement
on disk produces
\(\lvert T_{j\leftarrow j}\rvert\le\varepsilon\nu D_j+R\)
with \(R\) built only from energy,
\(\{Z_k\}\), and maybe \(\alpha\),
independent of \(\dot Z_j\) and
\(\Lambda'\).

AS_remainder stays **fail**.
EAud_door1_closed stays **fail**.
The chain stays a chain.

---

## 3. Why the natural writings fail the \(R\)-constraint

### 3.1 Bernstein + Young — valid inequality, wrong \(R\)

On the local block the standard Hölder /
Bernstein bound sits as an inequality
(constants depend only on \(\varphi\)):

\[
\lvert T_{j\leftarrow j}\rvert
\le
C[\varphi]\,\|u_{\mathrm{loc}}\|_\infty\,D_j^{1/2}Z_j^{1/2}
+
C[\varphi]\,\|\nabla u_{\mathrm{loc}}\|_\infty\,Z_j.
\]

Young on the transport piece:

\[
C\|u_{\mathrm{loc}}\|_\infty D_j^{1/2}Z_j^{1/2}
\le
\varepsilon\nu D_j
+
C_\varepsilon\nu^{-1}\|u_{\mathrm{loc}}\|_\infty^2 Z_j.
\]

The stretching piece remains. Bernstein
on three neighboring shells gives
\(\|\nabla u_{\mathrm{loc}}\|_\infty\lesssim 2^{j/2}Z_{\mathrm{loc}}^{1/2}\),
hence a remainder of size
\[
C\,2^{j/2}Z_{\mathrm{loc}}^{1/2}Z_j.
\]
That is the cubic wall at one shell.
It uses a frequency weight \(2^{j/2}\),
not energy, and it is quadratic in the
\(Z\)-scale after one more Young against
\(D_j\sim 2^{2j}Z_j\). Leftover form (3)
needs a coefficient that is integrable
from the energy inequality. Shell-cubic
is not that coefficient.

\(\|u_{\mathrm{loc}}\|_\infty\) is not
energy. Bernstein
\(\|u_{\mathrm{loc}}\|_\infty\lesssim 2^{3j/2}\mathcal E_{\mathrm{loc}}^{1/2}\)
puts \(2^{3j}\) into \(R\). Frequency
weights are not on the allowed list.

This inequality may be printed as a
*template*. It is not the requested
line.

### 3.2 Direction rewrite — identity, not a bound

Door 3:
\[
\alpha=\xi\cdot S_{\mathrm{strain}}\xi.
\]
The stretching pairing may be rewritten
\[
T_{j\leftarrow j}^{\mathrm{stretch}}
=
\int\alpha_{\mathrm{loc}}\,\lvert\Delta_j\omega\rvert^2
+
\text{commutators}.
\]
Then
\(\lvert\int\alpha_{\mathrm{loc}}\,\lvert\Delta_j\omega\rvert^2\rvert
\le\|\alpha_{\mathrm{loc}}\|_\infty Z_j\).
Young against \(D_j\) only moves
\(\|\alpha_{\mathrm{loc}}\|_\infty\) into
\(R\). That factor is not controlled by
energy or by \(\{Z_k\}\)
(\(W^{1,2}\not\subset L^\infty\) on the
strain). The commutators are not
estimated. A printed \(\alpha\) is a
criterion, not a bound
([`AXISYM-SHELL.md`](AXISYM-SHELL.md) §6).
Putting \(\alpha\) into \(R\) restates
Door 3. The chain stays a chain.

### 3.3 Energy-linear remainder — would close, not proved

The line that would finish the shell
budget, given AS-IR / transport Young /
AS-UV and a finite infrared sum, is
\[
\lvert T_{j\leftarrow j}\rvert
\le
\varepsilon\nu D_j
+
C_\varepsilon\,\mathcal E\,Z_j
\]
or the same with an integrable
\(\|\omega\|_\infty\) in place of
\(\mathcal E\). Then Gronwall and
\(\int\mathcal E<\infty\) (actually
\(\int E<\infty\) from the energy
equality) keep \(Z_j\) finite, which is
Theorem AS-ρ without assuming [ρ].

That is the estimate the request asked
for. It is not on disk. Writing it here
as a theorem is the discarded move:
an LLM emits the WRITE line.

[ρ] remains an extra hypothesis, in
the open.

### 3.4 Forbidden closings

From AS-Id,
\(T_j=\tfrac12\dot Z_j+\nu D_j\).
Bounding \(T_{j\leftarrow j}\) by
\(\dot Z_j\) restates the identity.
Audit KEEP: never bound the growing
term by a copy of the time derivative
you are estimating.

\(\Lambda'=2(T_c-\nu\mathcal D_s)/X\)
already contains the leftover \(T_c\).
It is bookkeeping, not this LHS, and
not a bound. No time series of that
identity is closed on this door. The
sign of \(\Lambda'\) is not quoted.

---

## 4. What sits, and what does not

| Item | Status |
|---|---|
| AS-Id, AS-Split | sit |
| AS-IR, IR-transport Young, AS-UV | sit |
| AS-τ, AS-ω\* | sit as identities, not bounds |
| Requested line \(\lvert T_{j\leftarrow j}\rvert\le\varepsilon\nu D_j+R\) with allowed \(R\) | **not written** |
| [ρ] for the class | not measured |
| Door 3 \(\alpha\) as a bound | fail |
| Lemma★ / H1 / unrestricted 3-D | other doors; not this page |

Samples of \(T_{j\leftarrow j}/Z_j\) may
come out either way. Visibility of
cancellation is not uniform smallness.
Those numbers are in
[`AXISYM-SHELL.md`](AXISYM-SHELL.md) §9
and
[`AXISYM-SWIRL-PROBE.md`](AXISYM-SWIRL-PROBE.md).
They are not this estimate.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| TJJ_requested_line | **fail** | \(\lvert T_{j\leftarrow j}\rvert\le\varepsilon\nu D_j+R\) with allowed \(R\) is not seated |
| TJJ_forbidden_slots | **pass** | \(\dot Z_j\) and \(\Lambda'\) were not used as a bound |
| TJJ_bernstein_template | **pass** | §3.1 is an inequality with the wrong \(R\); not cashed as the line |
| TJJ_direction | **fail** | \(\alpha\) in \(R\) is Door 3, still a criterion |
| TJJ_energy_linear | **fail** | the closing shape is named, not proved |
| TJJ_chain | **pass** | HAVE / WRITE / THEN stay a chain |
| TJJ_ns_solved | **fail** | class and \(\rho_j\) stay in the sentence |

NS not solved.
The chain stays a chain.
