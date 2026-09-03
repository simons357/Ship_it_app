# Geometric analysis of Track B (classical NS)

**Not a regularity proof.** This is a geometric analysis of the
architecture: torus, tube, shells, strain frame, swirl source. Domain
Architect maps which geometry each lemma uses and which remainder is
still clipped.

```bash
python -m domain_architect --geometry B
python -m domain_architect --chain B
```

## The four geometries (one object)

The PDE shape does not change. Four charts sit on it.

### 1. Physical space

A periodic box \(\mathbb{T}^3\), divergence-free. For swirl, split at a
tube radius \(\delta(t)\):

\[
I = I_{\mathrm{off}}(\delta)+I_{\mathrm{tube}}(\delta).
\]

Off-axis (\(r\ge\delta\)) the weight \(1/r^4\) is bounded. The live
geometry is the tube \(r<\delta\) around the axis, with a **wall** at
\(r=\delta\). Under concentration, \(\delta\sim 2^{-j_*}\).

### 2. Frequency space

Dyadic shells \(X_j\), total enstrophy \(X=\|\omega\|_2^2\), peak
\(J=\max X_j\). A **3-shell packet** around \(j_*\). Mass fraction
\(\sigma=P_{j_*}/X\) is either concentrated (\(\sigma\ge 1/2\)) or
spread (\(\sigma\le 1/2\)). That cover is B2. Occupation time is still
a clip.

### 3. Vorticity geometry

Strain eigenframe \(\lambda_1+\lambda_2+\lambda_3=0\), stretching
\(|\omega|^2\sum\lambda_i\cos^2\alpha_i\), direction \(\xi=\omega/|\omega|\),
superlevel \(E_c\). Ring bounds \(|\nabla\xi|\) on \(E_c\) for a
3-shell field (B3). All-data alignment is **not** geometry we have.
That slogan is `CLIP-B3b-ALIGN`.

### 4. Swirl tube

Keep \(\Gamma=ru_\theta\). The source \(r^{-4}\partial_z(\Gamma^2)\)
and the extra angular viscosity \(u_\theta/r^2\) live in the **same
tube**. That is the geometric reason not to cancel to \(\Phi_\theta\).
Canceling moves the work onto \(\|\Phi_\theta\|_\infty\)
(`CLIP-PHI-LINFTY`).

## What is closed vs open, geometrically

| Closed | Open |
|---|---|
| Low flux vanishes because the field is div-free (B1) | Occupation time of CONC vs SPREAD |
| Regime cover (B2) | Depletion / alignment for all data |
| 3-shell Bernstein / Ring on \(E_c\) (B3) | \(I_{\mathrm{tube}}\) at \(\delta\sim 2^{-j_*}\) |
| Tube Hardy + wall identity (B4) | Angular viscosity dominates \(I_{\mathrm{tube}}\) |
| Cylindrical Laplacian identity (B5) | Closed bound on \(X\) |
| Energy \(\Rightarrow L^\infty\) is false (B6) | Regularity |

## Next geometric write

Estimate \(I_{\mathrm{tube}}\) with Hardy plus the wall, match the wall
to \(I_{\mathrm{off}}\), set \(\delta\) from \(j_*\), keep \(1/r^4\).
Then the energy-class low Bony term \(T\). Do not pass regularity.
