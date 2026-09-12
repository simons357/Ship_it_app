# ATTACK 9D — remaining packet falsifier

**Date:** 2026-09-12  
**Status:** **LIVE.** Growing input and output supports.
Full complex polarizations. Frequency factors kept.
Lemma★ **OPEN**. **NS not solved.**

Desk: [`../../LEMMA-STAR-LIVE.md`](../../LEMMA-STAR-LIVE.md).
Probe: `scripts/ns_attacks/attack9d_growing.py`

---

## Live write (this page)

Target
\[
\|\Pi_\beta B(w,w)\|_2
\le
C\alpha\beta^{-1/2}\|w\|_2^2
\qquad\Longleftrightarrow\qquad
\sup K_{\alpha,\beta}<\infty.
\]

- \(B=B(w,w)=P[(w\cdot\nabla)w]\) is the same
  exact-shell bilinear. \(w=w_\alpha\),
  \(Aw=\alpha w\). \(\Pi_\beta\) onto shell \(\beta\).
  **Not** a new field.
- Polarizations are **full complex** (elliptical:
  three real angles in \(k^\perp\)). Linear
  pol (one plane angle + phase) is a slice.
  Finite 9B \(K\approx 0.641\) used that slice.
  Do not redo it and call it 9D.
- Frequency factors stay. Dropping \(|k|\) /
  writing \(\|\Pi_\beta B\|_2\le C\alpha\|w\|_2^2\)
  is the wrong packaging (\(K\lesssim\beta\)).
- Input support \(m\) and occupied output
  support \(s\) **grow**. No seated exponent
  ties \((m,s)\) to \((\alpha,\beta)\).

Fixed-output \(\Theta(m^2)\) is **excluded**.
Per output, \(p+q=k\) gives at most \(m\) pairs.
\(K\le 16s\). [`../../LEMMA-STAR-9B-COUNTING.md`](../../LEMMA-STAR-9B-COUNTING.md).

Freiman-AP designed \(\Theta(m^2)\) locked-phase
subset is **dead** (\(\mathcal D_s\) wins).
Do not rebuild. [`../../LEMMA-STAR-PACKET.md`](../../LEMMA-STAR-PACKET.md).

Attack 12 \(\mathcal R_\star\sim\beta/\alpha\) is a
different quotient on a different family.
Do not merge \(\sqrt{K}\) with that number.

---

## Kill criterion

| Outcome | Meaning |
|---|---|
| Family with \(K\to\infty\) (or \(\mathcal R_\star\to\infty\)) | **★ dead** |
| Bounded \(K\) on the samples that were run | those shapes did not kill ★ — **not a proof**; kill lane **LIVE** |

A larger finite number only raises \(C_{\mathrm{geom}}\).

---

## Dead writings (do not merge into the live write)

1. Designed \(\Theta(m^2)\) locked-phase **subset** (Freiman-AP).
   Already scored. Already dead.
2. Screenshot: \(\Theta(m^2)\) pairs onto **one** / **fixed**
   outputs. Analytically excluded.

---

## ★ reason (other live write)

Why signed stretching cannot outrun spectral
spread. HH→L is the dangerous channel.
**That sentence is not written.**
[`../../LEMMA-STAR-REASON.md`](../../LEMMA-STAR-REASON.md).

---

## Reproduce

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/attack9d_growing.py \
  --out results/attack9d_growing/attack9d_growing.json
```

**NS not solved.** Lemma★ OPEN. Kill lane LIVE.
