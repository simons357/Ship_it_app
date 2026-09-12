# ATTACK 9D — Designed \(\Theta(m^2)\)-closure subset with locked phases (stub / spec)

**Date:** 2026-09-10  
**Branch:** `cursor/ns-five-lane-lemma-star-1390`  
**Status:** **SPEC / STUB** on the five-lane branch — remaining packet falsifier there. Kill lane **LIVE**. Lemma★ **OPEN**. **NS not solved.**  
**Prior non-kill:** Attack 9C (fixed-gap spheres) — natural same-shell ensemble **NOT** a kill; \(\mathcal{R}_\star\) fell \(0.11\to 0.031\) — [`ATTACK_9C_FIXED_GAP_SPHERES.md`](./ATTACK_9C_FIXED_GAP_SPHERES.md).

**On this branch.** Two writings of “9D,” do not merge:

1. Designed \(\Theta(m^2)\) locked-phase **subset** (Freiman-AP).
   Already scored. Already dead (\(\mathcal D_s\) wins).
   Do not rebuild. [`../../LEMMA-STAR-PACKET.md`](../../LEMMA-STAR-PACKET.md).
2. Screenshot: \(\Theta(m^2)\) pairs onto **one** output, or a
   **fixed** number of outputs. **Analytically excluded.**
   Per output, \(p+q=k\) gives at most \(m\) pairs.
   \(K_{\alpha,\beta}\le 16s\). Fixed \(s\) cannot unbound \(K\).
   File: [`../../LEMMA-STAR-9B-COUNTING.md`](../../LEMMA-STAR-9B-COUNTING.md).

Growing the **number of output modes** stays a 9B test
(complex polarizations, keep \(|k|\)). That is not (1) and
not (2).

## Setup lock — do not guess this as 9D

The uniform target
\[
\|\Pi_\beta B(w,w)\|_2
\le
C\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2
\]
is **Attack 9B**, not 9D.
[`../../LEMMA-STAR-9B-COUNTING.md`](../../LEMMA-STAR-9B-COUNTING.md).

- \(B=B(w,w)=P[(w\cdot\nabla)w]\) is the same bilinear
  as the exact-shell / HH→L fan work. \(w=w_\alpha\)
  lives on one Stokes eigen-shell \(Aw=\alpha w\).
  \(\Pi_\beta\) is the projector onto shell \(\beta\).
  This is **not** a new 9D field.
- Equivalent form:
  \(\sup K_{\alpha,\beta}<\infty\), with
  \(K_{\alpha,\beta}=\beta\|\Pi_\beta B(w,w)\|_2^2/(\alpha^2\|w\|_2^4)\).
- Attack 12’s \(\mathcal R_\star\sim\beta/\alpha\) is a
  **different quotient** on a **different family**
  (partners of a low key on a high sphere). Do **not**
  merge \(\sqrt{K}\approx 0.711\) with Attack 12’s
  \(\mathcal R_\star\approx 0.71\).

**Growth law.** There is no seated exponent that ties
input/output support sizes to \(\alpha,\beta\).
\(\alpha,\beta\) are eigenvalues. \(m\) is the number of
input keys on shell \(\alpha\). \(s\) is the number of
occupied keys of \(\Pi_\beta B(w,w)\) on shell \(\beta\).
The crude phase-free bound is \(K\le 16s\). Fixed \(s\)
is closed. Whether \(K\) stays bounded as \(m\) and \(s\)
**grow** is the open 9B test
(`attack9b_growing_s.py`, also
`attack9b_output_counting.py`). Finding that scaling
is **not** a 9D lemma.

9D’s \(\Theta(m^2)\) is a *design size for a closure
subset*, not a proven law for \(\|\Pi_\beta B\|_2\).
Writing (1) already died. Writing (2) is excluded.
Do not start a 9D pass by inventing a support
\(\leftrightarrow(\alpha,\beta)\) exponent.

## Motivation (why 9C failed → what 9D must change)

Attack 9C locked:
- \(\mathcal{D}_s\) from the **gap**, not packet width;
- natural closures only \(O(m)\);
- \(\mathcal{R}_\star\) **falls** with \(n\) and does **not** track \(m^{1/2}\).

So the remaining packet falsifier is **not** another natural same-shell random/ensemble probe. It must **design** a closure subset of size \(\Theta(m^2)\) and **lock phases** so that coherent stretching can accumulate in \((T_c)_+\) without the cancellations that keep natural ensembles bounded/decaying.

## Target family (spec)

1. **Mode set:** Choose a primary packet of cardinality \(m\) (exact shell or controlled near-shell) plus a **designed** closing / interaction subset whose cardinality (or number of active triad closures) scales as \(\Theta(m^2)\), not \(O(m)\).
2. **Phases:** Lock relative phases (and polarizations) so the signed triad Im-sum adds constructively in total \(T_c\) — no free random-phase averaging.
3. **Spectral control:** Keep \(\mathcal{D}_s\) under explicit control (fixed gap, exact-shell + \(\varepsilon\) closing, or other documented spectral support). Do **not** accidentally reintroduce 9A-style \(\mathcal{D}_s\) blowup from uncontrolled packet widening.
4. **Quotient:** Report complete
   \[
   \mathcal{R}_\star(v)=\frac{(T_c(v)_+)^2}{\mathcal{D}_s(v)\,\|v\|_2^2\,Y(v)}
   \]
   with **total** signed \(T_c\) (not HH→L-only).

## Kill criterion

| Outcome | Meaning |
|---------|---------|
| Smooth family with \(\mathcal{R}_\star\to\infty\) (e.g. \(\sim m^{\gamma}\), \(\gamma>0\), or unbounded in designed scale) | **★ dead** |
| Bounded / decaying \(\mathcal{R}_\star\) on the designed locked-phase family | Those shapes did not kill ★ — **not a proof**; kill lane still **LIVE** |
| Uncontrolled \(\mathcal{D}_s\) growth that invalidates the design | Implementation / design bug — fix before claiming |

## Required controls (when implemented)

| Control | Expectation |
|---------|-------------|
| Amplitude: \(\mathcal{R}_\star(av)=\mathcal{R}_\star(v)\) | Exact |
| Uniform Fourier dilation invariance (when applicable) | Exact |
| Closure count / designed subset size | Document \(\Theta(m^2)\) scaling explicitly |
| Phase lock | Reproducible; no silent random re-phase |
| Report **total** signed \(T_c\) | Not HH→L-only |

## Script status

**Not implemented.** Planned name (TBD): `scripts/ns_attacks/attack9d_theta_m2_locked_phase.py`.  
Until then this note is **spec-only** in the Source of Truth.

## Reproduce (placeholder)

```bash
# Not yet available — SoT stub only
# PYTHONPATH=scripts python3 scripts/ns_attacks/attack9d_theta_m2_locked_phase.py \
#   --outdir /opt/cursor/artifacts/attack9d_theta_m2_locked_phase
```

## Related

- [`ATTACK_9C_FIXED_GAP_SPHERES.md`](./ATTACK_9C_FIXED_GAP_SPHERES.md) — natural ensemble non-kill
- [`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md) — \(K_{\alpha,\beta}\)
- [`ATTACK_9A_AP_PACKET_FAILURE.md`](./ATTACK_9A_AP_PACKET_FAILURE.md) — AP fan non-kill
- [`ATTACK_SYNTHESIS_SIMULTANEOUS.md`](./ATTACK_SYNTHESIS_SIMULTANEOUS.md)
- [`PROOF_LemmaStar_STATUS.md`](./PROOF_LemmaStar_STATUS.md)

**NS not solved.**
