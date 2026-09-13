# ATTACK 9D — Growing input and output supports (retarget)

**Date:** 10 September 2026  
**Status:** **LIVE test** of the uniform 9B target. Lemma★ **OPEN**. **NS not solved.**  
**Prior:** Fixed-output \(\Theta(m^2)\) 9D is **analytically excluded** — [`ATTACK_9B_COUNTING_CS_EXCLUSION.md`](./ATTACK_9B_COUNTING_CS_EXCLUSION.md). Natural same-shell (9C) is **not** a kill.  
**Setup (do not guess \(B\) or an exponent):** [`ATTACK_9D_SETUP.md`](./ATTACK_9D_SETUP.md).

## Exclusion (do not revive)

The screenshot’s \(\Theta(m^2)\) pairs onto **one**, or a **fixed number** of, output modes **cannot** happen:

- \(p+q=k\Rightarrow q=k-p\): at most \(m\) ordered pairs per output.
- Incompressibility + CS: \(|\widehat B_k|\le |k|\,\|w\|_2^2\) for every phase/polarization.
- Occupied output count \(s\) on shell \(\beta\): \(K_{\alpha,\beta}(w)\le s(\beta/\alpha)^2\le 16s\).

Fixed \(s\) \(\Rightarrow\) bounded \(K\). That mechanism is **dead**. Growing **output** support remains legitimate.

## Uniform target (what a 9B proof would need)

\[
\|\Pi_\beta B(w,w)\|_2
\le C\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2.
\]
The screenshot bound \(\|\Pi_\beta B\|_2\le C\alpha\|w\|_2^2\) is **insufficient** (\(K\le C^2\beta\) may grow with the output shell).

## Live family

Full **complex polarizations** on a growing exact-shell input support, with **growing** output support on admissible \(\beta\le 4\alpha\), **frequency factors retained**. Report complete \(K_{\alpha,\beta}\) and
\[
C_{\mathrm{obs}}(w)=\frac{\|\Pi_\beta B(w,w)\|_2\,\sqrt{\beta}}{\alpha\|w\|_2^2}.
\]
If \(C_{\mathrm{obs}}\) (or \(K\)) is unbounded on this family, the 9B route kills ★. A bounded sample is **not** a proof.

Do **not** drop \(|k|\) from \(B\). Do **not** restrict to HH→L-only \(T_c\).

## Kill criterion

| Outcome | Meaning |
|---|---|
| Smooth family with \(K_{\alpha,\beta}\to\infty\) or \(C_{\mathrm{obs}}\to\infty\) as input/output supports grow | **★ dead** on the 9B family |
| Bounded sample | those shapes did not kill ★ — **not a proof**; kill lane **LIVE** |
| Implementation that forces fixed \(s\) and claims \(\Theta(m^2)\) | counting bug — excluded |

## Script

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/attack9d_growing_io.py \
  --outdir /opt/cursor/artifacts/attack9d_growing_io
```

**NS not solved.**
