# Snapshot tests — \(A_{\mathrm{bad}}\) with \(\Lambda=\Lambda_0\) fixed

15 September 2026.
**Snapshot tests. Not leftover 1. H1 is not a theorem.
WRITE (6) is not a theorem. Ordinary NS is not solved.**

Do not start leftover 1 from this table.
Do not start leftover 1 from ABC_λ.
Do not glue this integral to \(\mathcal R_\star\).

Probe: `python3 scripts/h1_abad_snapshot.py`

Write: [`H1-WRITE.md`](H1-WRITE.md).
Object: [`H1-OBJECT.md`](H1-OBJECT.md).
Tube numbers (different integral): [`H1-TUBE.md`](H1-TUBE.md).

---

## What was asked

Keep \(\Lambda=\Lambda_0\) fixed during the
amplitude sweep. If the threshold tracks
\(\|\omega\|_\infty\), a fixed-shape field
has an amplitude-invariant high set and
the sweep does not test the cut.

\(\Lambda_0=0.35\|\omega\|_\infty\) at
amplitude \(1\), per field. Then only the
field is scaled.

`run_one()` computes
\(C_{\mathrm{needed,raw}}=A_{\mathrm{bad}}/(r^{-2}\iint|\omega|^2)\).
Dissipation \(\nu/8\iint|\nabla\omega|^2\phi\)
is not subtracted. That constant sits on
`FieldReport` and in the printed table.

The original bad-pair integral is the
majorant
\[
\iiint_{\mathrm{Bad}}
\frac{|\omega(x)|^2|\omega(y)|}{|x-y|^3}
\]
on \(\mathbb T^3\) at one time, \(\phi\equiv 1\),
\(r=\pi\), \(C_*=0.25\). Periodic min-image.
Self-pairs dropped. Not a space-time
cylinder. That is why these are snapshot
tests.

---

## Table

Numbers from `n=16`. A finite
\(C_{\mathrm{needed,raw}}\) is not \(C_0\).
A growing sample is not \(\mathcal G\to\infty\).

The filled rows are written after the
corrected sweep is run. Until then the
script is the record.

| field | amplitude | fixed threshold \(\Lambda_0\) | original bad-pair integral | \(C_{\mathrm{needed,raw}}\) |
|---|---:|---:|---:|---:|
| ABC | *(run)* | *(run)* | *(run)* | *(run)* |
| Taylor–Green | *(run)* | *(run)* | *(run)* | *(run)* |

---

## What this is not

- not leftover 1
- not WRITE (6) as a theorem
- not a start of H1 from ABC_λ
- not BKM
- not \(\sup\mathcal G<\infty\)
- not a kill of leftover 1

NS not solved. H1 not a theorem.
The door is named. The last line
is not written.
