# Periodic snapshot diagnostics — \(A_{\mathrm{bad}}\) with \(\Lambda=\Lambda_0\) fixed

15 September 2026.
**Periodic snapshot diagnostics. Not leftover 1.
H1 is not a theorem. WRITE (6) is not a
theorem. Ordinary NS is not solved.**

Do not start leftover 1 from this table.
Do not start leftover 1 from ABC_λ.
Do not glue this integral to \(\mathcal R_\star\).
Does not rescue unrestricted local (6).

ABC as an exact smooth Beltrami field
already defeats unrestricted local (6).
Stretch on that field grows like amplitude
([`H1-TUBE.md`](H1-TUBE.md)). These
snapshots neither establish nor undo that
result. Correcting the numerical record
does not rescue that estimate.

Probe: `python3 scripts/h1_abad_snapshot.py`

Write: [`H1-WRITE.md`](H1-WRITE.md).
Object: [`H1-OBJECT.md`](H1-OBJECT.md).
Tube numbers (different integral): [`H1-TUBE.md`](H1-TUBE.md).

---

## What was asked

Keep Lambda = Lambda0 fixed during the
amplitude sweep. \(\Lambda=\Lambda_0\).
If the threshold tracks
\(\|\omega\|_\infty\), a fixed-shape field
has an amplitude-invariant high set and
the sweep does not test the cut.

\(\Lambda_0=0.35\|\omega\|_\infty\) at
amplitude \(1\), per field. Then only the
field is scaled.

Two integrals, same grid, same Bad pairs.
The Bad cut does not replace the angle
factor in the integrand.
\[
\delta(x,y)=|\xi(x)\times\xi(y)|,
\qquad
0\le\delta\le 1.
\]
\[
A_{\mathrm{angle}}
=
\iiint_{\mathrm{Bad}}
\frac{\delta(x,y)\,|\omega(x)|^2|\omega(y)|}{|x-y|^3},
\qquad
A_{\mathrm{no\ angle}}
=
\iiint_{\mathrm{Bad}}
\frac{|\omega(x)|^2|\omega(y)|}{|x-y|^3}.
\]
\(A_{\mathrm{no\ angle}}\) is a larger
majorant. It is not the original quantity.
Do not call it the original bad-pair
integral.

`run_one()` writes both on `FieldReport`
as `A_angle` and `A_no_angle`.
The requested constant subtracts
dissipation, \(\nu=1\), \(\phi\equiv 1\):
\[
C_{\mathrm{needed,raw}}
=
\max\!\left(
0,
\frac{r^2}{E}
\left[
A_{\mathrm{angle}}
-
\frac{\nu}{8}D_\phi
\right]
\right),
\]
\[
E=\int|\omega|^2,
\qquad
D_\phi=\int|\nabla\omega|^2\phi.
\]
The ratio \(r^2 A_{\mathrm{no\ angle}}/E\)
is a legitimate diagnostic of the
angle-free majorant. It answers a
different question. It is not
`C_needed_raw`.

Periodic \(\mathbb T^3\), one time,
\(r=\pi\), \(C_*=0.25\). Min-image.
Self-pairs dropped. Not a space-time
cylinder. That is why these are
periodic snapshot diagnostics.

---

## Table

Corrected sweep, \(n=16\). A finite
\(C_{\mathrm{needed,raw}}\) is not \(C_0\).
A growing sample is not \(\mathcal G\to\infty\).
One grid does not establish a continuum
bound or a counterexample.

\(\Lambda_0\) is frozen at amplitude 1
for that field.

| field | amplitude | fixed threshold \(\Lambda_0\) | \(A_{\mathrm{angle}}\) | \(A_{\mathrm{no\ angle}}\) | \(C_{\mathrm{needed,raw}}\) |
|---|---:|---:|---:|---:|---:|
| ABC | *(run)* | *(run)* | *(run)* | *(run)* | *(run)* |
| Taylor–Green | *(run)* | *(run)* | *(run)* | *(run)* | *(run)* |

---

## What this is not

- not leftover 1
- not WRITE (6) as a theorem
- not a start of H1 from ABC_λ
- not BKM
- not \(\sup\mathcal G<\infty\)
- not a kill of leftover 1
- not a rescue of unrestricted local (6)

NS not solved. H1 not a theorem.
The door is named. The last line
is not written.
