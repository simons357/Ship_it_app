# Lemma★ — canonical shape form

**Date:** 2026-09-10  
**Branch:** `cursor/ns-five-lane-lemma-star-1390`  
**Lock:** Truth only. **NS is NOT solved.** Lemma★ is **OPEN**. This note reframes ★; it does not prove it.

## Reframe (lock)

**Lemma★ is no longer a viscosity statement. It is a shape statement.**

### What ★ was claiming (viscosity packaging)

Stretching \(\mathfrak T_c\) is cubic in the field. Spectral spread \(\mathcal D_s\) is quadratic. Viscosity multiplies the spread and sits in the remainder as \(1/\nu\). The original line mixed three scalings — hard to see what kills it:

\[
\mathfrak T_c\le\theta\nu\mathcal D_s+C_0\nu^{-1}\|u\|_2^2 X\Lambda
=\theta\nu\mathcal D_s+C_0\nu^{-1} E\,Y,
\]
since \(X\Lambda=Y\).

### What \(u=av\) does

Change only the size of a fixed shape \(v\). Optimize over size. Worst size cancels \(\nu\). What remains is pure geometry on the shape.

## Notation (matches `scripts/ns_attacks/stokes_moments.py`)

On divergence-free Fourier–Galerkin fields on \(\mathbb{T}^3\), Stokes operator \(A\):

| Symbol | Definition |
|--------|------------|
| \(E\) | \(\|u\|_2^2\) |
| \(X\) | \(\|A^{1/2}u\|_2^2=\sum\|k\|^2|\hat u(k)|^2\) |
| \(Y\) | \(\|Au\|_2^2=\sum\|k\|^4|\hat u(k)|^2\) |
| \(Z\) | \(\|A^{3/2}u\|_2^2=\sum\|k\|^6|\hat u(k)|^2\) |
| \(\Lambda\) | \(Y/X\) |
| \(\mathcal D_s\) | \(Z-\Lambda Y=X\cdot\mathrm{Var}_\mu(\|k\|^2)\ge0\) |
| \(\mathcal N\) | \(-\langle B(u,u),Au\rangle\) |
| \(\mathcal M\) | \(-\langle B(u,u),A^2u\rangle\) |
| \(\mathfrak T_c\) | \(\mathcal M-\Lambda\mathcal N\) (scripts: `Tc`) |

Homogeneity under \(u=av\) (fixed shape \(v\), amplitude \(a>0\)):

\[
\mathfrak T_c(av)=a^3\mathfrak T_c(v),\quad
\mathcal D_s(av)=a^2\mathcal D_s(v),\quad
E(av)=a^2 E(v),\quad
Y(av)=a^2 Y(v),\quad
\Lambda(av)=\Lambda(v).
\]

## Boxed shape inequality (canonical ★)

\[
\boxed{
\bigl(\mathfrak T_c(v)\bigr)^2
\le
C_{\mathrm{geom}}\,
\mathcal D_s(v)\,
E(v)\,
Y(v)
}
\]

for every divergence-free \(v\) on \(\mathbb{T}^3\), with one geometric constant \(C_{\mathrm{geom}}\) independent of amplitude and of \(\nu\).

In words:

\[
(\text{stretching of the shape})^2
\le
(\text{one geometric constant})
\times
(\text{how spread the spectrum is})
\times
(\text{energy})
\times Y.
\]

### Equivalence to the viscosity packaging

Young / AM–GM on the amplitude line recovers the old form with
\[
C_0(\theta)=\frac{C_{\mathrm{geom}}}{4\theta}
\]
(up to the conventional \(\theta\in(0,1)\) bookkeeping). Conversely, if viscosity-★ holds with some \(C_0(\theta)\), then the boxed shape inequality holds with \(C_{\mathrm{geom}}=4\theta\,C_0(\theta)\).

**Therefore:** if the boxed line holds for every divergence-free \(v\) with one \(C_{\mathrm{geom}}\) (equivalently one \(C_0(\theta)\)), then original ★ holds for every amplitude and every \(\nu\). If it fails for even one shape, ★ is false.

## Shape ratio \(\mathcal R_\star(v)\)

When \(\mathcal D_s(v)>0\), \(E(v)>0\), \(Y(v)>0\):

\[
\mathcal R_\star(v)
:=
\frac{\bigl(\mathfrak T_c(v)\bigr)^2}{\mathcal D_s(v)\,E(v)\,Y(v)}.
\]

Scripts expose this as `ratio_R_star_shape` on `ProbeResult`.

**Meaning:** stretching that shape gets per unit of spread, energy, and \(Y\). Pure geometry. Same for \(av\) as for \(v\). Independent of viscosity.

| Outcome | Verdict |
|---------|---------|
| Some shapes make \(\mathcal R_\star\) arbitrarily large | no finite \(C_{\mathrm{geom}}\) / \(C_0\) → **★ dead** |
| \(\mathcal D_s=0\) (one Fourier shell) and \(\mathfrak T_c>0\) | **★ dead** on that field |
| Pure single shell, both sides vanish (\(\mathfrak T_c=0=\mathcal D_s\)) | vacuous — not a kill |
| Live kill attempt | **almost-single-shell** that still stretches (\(\mathcal D_s\to0^+\) with \(\mathfrak T_c\not\to0\) fast enough that \(\mathcal R_\star\to\infty\)) |
| Every shape has \(\mathcal R_\star\) below one number \(K\) | that number is ★ (up to \(4\theta\)): \(C_{\mathrm{geom}}=K\), \(C_0=K/(4\theta)\) |
| A list of fields with small \(\mathcal R_\star\) | **NOT** that number — only those shapes did not kill it |

**Do not confuse** with the older post-Young scalar \(R_{\mathrm{post}}=\mathfrak T_c/(E\,X\Lambda)=\mathfrak T_c/(EY)\) (scripts: `ratio_star`), which falls as \(1/a\) on a fixed shape, nor with the pre-Young \(R_{\mathrm{pre}}=\mathfrak T_c/(\sqrt{E}\,X\Lambda)\) (scripts: `ratio_preyoung`).

## What a proof would have to be

Reason from how triads add that stretching cannot get large unless spectrum also spreads or phases cancel. **HH→L** is the channel that could refuse that. That reason is **NOT written**.

**NS not solved.**

## Related

- Status board: [`PROOF_LemmaStar_STATUS.md`](./PROOF_LemmaStar_STATUS.md)
- Synthesis: [`ATTACK_SYNTHESIS_SIMULTANEOUS.md`](./ATTACK_SYNTHESIS_SIMULTANEOUS.md)
- DA metaphor map: [`DA-SHAPE-TEXTURE-LINK.md`](./DA-SHAPE-TEXTURE-LINK.md)
- Probe: `scripts/ns_attacks/stokes_moments.py`, `attack5_route2_kill.py` (`almost_single_shell` family)
