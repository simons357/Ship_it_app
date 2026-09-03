# Tube estimate — live geometric write

**Not a regularity proof.** Keep \(1/r^4\). Keep \(\Gamma=ru_\theta\).
Do not switch the unknown to \(\Phi_\theta\).

```bash
python -m domain_architect --tube B
```

## The split

\[
I=\int\frac1{r^4}\partial_z(\Gamma^2)\,\omega^r\,r\,dr\,dz
=I_{\mathrm{off}}(\delta)+I_{\mathrm{tube}}(\delta).
\]

Set \(h=\Gamma/r\). Axisymmetric smoothness wants \(h(0)=0\).

| Piece | Geometry | Status |
|---|---|---|
| \(I_{\mathrm{off}}\) | \(r\ge\delta\), weight \(\le\delta^{-4}\) | **pass** as a bound (T1) |
| Hardy+wall, from **inside** | \(h(0)=0\Rightarrow\int_0^\delta h^2/r\le 4\int(h')^2 r+2h(\delta)^2\) | **pass** (B4 / T2) |
| Young trace, from **outside** | \(h(R)=0\Rightarrow h(\delta)^2\le\varepsilon\int_\delta^R r(h')^2+\varepsilon^{-1}\int_\delta^R h^2/r\) | **pass** as a cylinder identity (T3a) |
| Outer vanishing on \(\mathbb{T}^3\) | the box is not a half-line | **clipped** (`CLIP-T3-OUTER`) |
| Wall \(\to I_{\mathrm{off}}\) | same \(r^{-3}\) weight, different fields | **open** (T3b, `CLIP-T3-WELD`) |
| \(\delta\sim 2^{-j_*}\) | tube = viscous scale of the CONC packet | architecture (T4); spread uses Bony |
| \(I_{\mathrm{tube}}\) vs \(\nu\|\nabla\omega\|_2^2\) | danger and dissipation in the same tube | **open** (T5, T6) |
| Gronwall \(R\in L^1\) | would close \(X\in L^\infty\) | **open** (T7) |

Target form, still unearned:

\[
\frac{d}{dt}X+\nu\|\nabla\omega\|_2^2
\le\varepsilon\nu\|\nabla\omega\|_2^2
+C_\varepsilon X\,\mathcal R(t).
\]

\(\mathcal R\) would have to come from tube Hardy and/or Ring on \(E_c\)
and/or spread Poincaré. Integrable enstrophy alone is not \(\mathcal R\)
(B6 failed that close).

## The wall is a two-sided cylinder

Hardy integration by parts lives **inside** the tube and dumps a remainder
on the lateral surface \(r=\delta\):

\[
2h(\delta)^2.
\]

If swirl vanishes at some outer radius \(R>\delta\), the **same number**
is a Young trace from the complement:

\[
h(\delta)^2=-2\int_\delta^R h\,h'\,dr
\le\varepsilon\int_\delta^R r(h')^2\,dr
+\varepsilon^{-1}\int_\delta^R\frac{h^2}{r}\,dr.
\]

That is T3a. It is a cylinder identity. Numeric probe holds on manufactured
profiles that vanish at \(R\).

Two clips stay attached:

- **`CLIP-T3-OUTER`.** Periodic \(\mathbb{T}^3\) does not give an \(R\) with
  \(\Gamma(R)=0\). T3a used extra environment.
- **`CLIP-T3-WELD`.** Off-axis Hardy sees \(\Gamma^2/r^3\). The swirl source
  \(I_{\mathrm{off}}\) sees \((\Gamma\partial_z\Gamma)\,\omega^r/r^3\). Same
  radial weight, different fields. Do not silent-merge them.

## Monomials (do not glue)

| ID | Expression | Lives |
|---|---|---|
| HARDY-WEIGHT | \(h^2/r=\Gamma^2/r^3\) | radial line, either side of the wall |
| WALL | \(2(\Gamma/\delta)^2\) | cylinder \(r=\delta\) |
| I-OFF | \((\Gamma\partial_z\Gamma)\,\omega^r/r^3\) | volume \(r\ge\delta\) |
| I-TUBE | \(2\Gamma\partial_z\Gamma/r^4\) | volume \(r<\delta\) |
| ANGULAR-VISC | \((u_\theta/r)^2=(\Gamma/r^2)^2\) | same tube as I-TUBE |

## Scaling ledger (architecture, not a proof)

Under \(\delta\sim 2^{-j_*}\), two naive charts disagree:

- **\(L^2\) packet:** \(\|\Delta_j u\|_2\sim 2^{-j}\sqrt{X_j}\), so wall
  \(\sim\delta^2 X\) looks small.
- **\(L^\infty\) Bernstein:** \(\|\Delta_j u\|_\infty\lesssim 2^{j/2}\sqrt{X_j}\),
  so wall \(\sim X/\delta\) looks large.

Pick neither as a close. That disagreement **is** the open weld.

## What “continue” means next

1. **T5** — bound \(|I_{\mathrm{tube}}|\) with T2 + T3a, carrying
   `CLIP-T3-WELD` and `CLIP-T3-OUTER`. This is the estimate we refused to
   escape by canceling to \(\Phi_\theta\).
2. Then energy-class low Bony \(T\) on the **spread** chart (Cartesian
   \(\mathbb{T}^3\), no \(\Gamma\)). Do not glue H onto the tube.

Regularity stays open until T7 has a constructed \(\mathcal R\).
