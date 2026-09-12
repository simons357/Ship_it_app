# Axisymmetric swirl probe of \(T_{j\leftarrow j}\)

11 September 2026.
**Not a close. NS not solved.
Remainder is open.**

Axisymmetric-with-swirl Navier–Stokes,
unaugmented, compact swirl on
\(\mathbb{R}^3\) with support in a ball
of radius \(R=2.4<\pi\); quantity
\(Z_j\) of the 2/3-dealiased Leray
interpolant; remainder
\(T_{j\leftarrow j}\); [no extra field];
pairing closed on these samples;
[ρ] not assumed for the class.

Estimate: [`AXISYM-SHELL.md`](AXISYM-SHELL.md).
Filter: [`ESTIMATE-AUDIT.md`](ESTIMATE-AUDIT.md).
Wall / dictionary
(occupation from the detector withdrawn):
[`SWIRL-WALL-CORRECTION.md`](SWIRL-WALL-CORRECTION.md).
Probe: `python3 scripts/axisym_swirl_probe.py`

This is a measurement of named fields.
It is not a bound. It is not H1. It is
not Lemma★. Occupancy is not scored.
\(\alpha\) is printed separately.
The sign of \(\Lambda'\) is not quoted
(no closed time series).

---

## Fields

Continuum, on the ball
\(q^2=X^2+Y^2+Z^2<R^2\),
\(B=\exp\bigl(-1/(R^2-q^2)\bigr)\),
and \(B=0\) outside. Images do not
overlap on the torus.

- **pure swirl.**
  \(u=B\,(1+\sin Z)\,(-Y,X,0)\).
  Divergence-free. Smooth on the axis.
- **swirl + meridional, \(m=1\) and \(m=3\).**
  Same swirl plus \(m\) times the
  Stokes stream field of
  \(\chi=r^2 B(1+\sin Z)\).

The scored object is the
energy-normalized Leray projection of
the Fourier interpolant, 2/3-dealiased,
so the pairing diagnostic matches
[`AXISYM-SHELL.md`](AXISYM-SHELL.md).
A 90° residual about the axis checks
that SO(2) survived the interpolant.

---

## Printed ratios

Pairing residual \(\le 3\times 10^{-18}\)
relative. Split error at roundoff.
Rotation residual \(\le 4\times 10^{-15}\).
Identity closed on these samples.
Still no \(\Lambda'\) sign: there is no
time series.

| field | \(n\) | \(\max\lvert T_{j\leftarrow j}/X_j\rvert\) | \(\max\lvert T_{j\leftarrow j}^{Z}/Z_j\rvert\) | \(\overline{\alpha}\) |
|---|---|---|---|---|
| pure swirl | 32 | \(3.2\times 10^{-19}\) | \(6.9\times 10^{-20}\) | \(0\) |
| swirl+meridional \(m=1\) | 32 | \(0.00112\) | \(0.00125\) | \(-1.3\times 10^{-4}\) |
| swirl+meridional \(m=3\) | 32 | \(0.00141\) | \(0.00140\) | \(-1.0\times 10^{-4}\) |
| pure swirl | 48 | \(6.7\times 10^{-20}\) | \(4.1\times 10^{-20}\) | \(0\) |
| swirl+meridional \(m=1\) | 48 | \(0.000583\) | \(0.000569\) | \(-9.2\times 10^{-5}\) |
| swirl+meridional \(m=3\) | 48 | \(0.000726\) | \(0.000617\) | \(-4.5\times 10^{-5}\) |

The meridional ratio moved with \(n\)
and with \(m\). A number can come out
the other way. Both resolutions are
allowed in. The continuum value of
these blobs is not locked.

Pure swirl on this family printed as
zero to residual. That is a fact about
these two grids, not a class bound.

2-D \(\rho\sim 0.017\) is not used here.
Occupancy 1 is not imported.

---

## What is not claimed

- [ρ] for the class.
- \(T_{j\leftarrow j}\) small in
  axisymmetric-with-swirl NS.
- A close of the shell estimate.
- A bound by \(\Lambda'\) or
  \(\dot Z_j\).
- Occupation decay from the swirl-wall
  detector. That claim is withdrawn.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| ASW_class_field | **pass** | compact swirl; rotation residual \(10^{-15}\) |
| ASW_pairing | **pass** | residual \(10^{-18}\) |
| ASW_split | **pass** | Door 1 on the interpolant |
| ASW_rho_printed | **pass** | ratios in the table |
| ASW_alpha_separate | **pass** | \(\alpha\) printed; occupancy not scored |
| ASW_remainder | **fail** | \(T_{j\leftarrow j}\) open |
| ASW_rho_class | **fail** | [ρ] is not a class fact |
| ASW_ns_solved | **fail** | class and \(\rho_j\) stay in the sentence |

NS not solved.
