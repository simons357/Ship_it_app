# Pólya probe — dump and run

**Status:** exploratory classification, 2026-09-14  
**Riemann hypothesis status:** not claimed  
**Canonical SFE status:** unresolved  
**Run:** `python -m domain_architect --polya-probe`

Dump Pólya’s record into Domain Architect. Do not pre-filter what belongs.
DA chooses how many independently specifiable components to record — 7, 8,
15, or whatever the subject needs. Core roles are an interface, not a cap.
Quantum Hilbert–Pólya fitted by expansion (\(ℋ\), inner product, \(ℬ\),
\(D\), \(\Xi=0\), time-reversal), not by squeezing into five.

This is classification, not a proof of the Riemann hypothesis and not a
unification of Millennium problems.

---

## What was dumped

Theorems and candidates already in the Hilbert–Pólya briefing, plus a
further unfiltered Pólya ingest:

- Pólya 1915 integer-valued entire functions
- Pólya 1918 / 1923 zeros of entire functions
- Pólya 1921 random-walk recurrence / transience
- Pólya 1926 Acta integral representation of \(\xi\) (kept distinct from
  the cosine-zero criterion)
- Pólya frequency / variation-diminishing kernels
- Turán inequalities
- Pólya 1937 enumeration theorem
- Pólya–Szegő 1951 isoperimetric inequalities in mathematical physics
- Pólya 1954 membrane eigenvalues

Registry: `HP-H001`–`HP-H025`, `HP-H027`, plus `NS-H001`–`NS-H003`.

Run the CLI for the live component count, filter pops, and DA’s request list.

---

## What to read as DA’s output

```bash
python -m domain_architect --polya-probe
python -m domain_architect --pair
python -m domain_architect --breakdown-children
```

The narrative leads with **who survived the filter**, then **what popped**,
then the full component list, then **Domain Architect still needs**. Those needs
are not optional commentary. They are the missing independent objects DA
cannot invent:

- an independent self-adjoint \(H\), or
- an RH-free LP / 1926 / PF / Turán check on Riemann’s \(\Phi\) or \(\xi\), or
- \(\Lambda\le 0\) without assuming RH, or
- an explicit checked map if a Navier–Stokes (or other prize) bridge is claimed.

The narrative also records a **Millennium look**: parts of Pólya versus
NS / Yang–Mills / BSD / Hodge / P vs NP. Closest NS rhyme is Pólya 1921
\(d\ge 3\) transience with the 3D Biot–Savart kernel. That is not regularity.
Riemann kernel \(\Phi\) collides in notation with swirl \(\Phi=u_\theta/r\).
No Pólya object unifies the Clay prizes.

Refusals and blocked children are **path guidance** for the NS/RH chase:
`python -m domain_architect --breakdown-children`.
