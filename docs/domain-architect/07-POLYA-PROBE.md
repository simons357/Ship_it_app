# Pólya probe — dump and run

**Status:** exploratory classification, 2026-09-14  
**Riemann hypothesis status:** not claimed  
**Canonical SFE status:** unresolved  
**Run:** `python -m domain_architect --polya-probe`

Dump Pólya’s record into Domain Architect. Do not pre-filter what belongs.
DA chooses how many independently specifiable components to record (core
roles are an interface, not a cap). Then DA asks for whatever else it needs.

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

Registry: `HP-H001`–`HP-H024`.

Run the CLI for the live component count, filter pops, and DA’s request list.

---

## What to read as DA’s output

```bash
python -m domain_architect --polya-probe
```

The narrative leads with **what popped through the DA filter**, then the
full component list, then **Domain Architect still needs**. Those needs
are not optional commentary. They are the missing independent objects DA
cannot invent:

- an independent self-adjoint \(H\), or
- an RH-free LP / 1926 / PF / Turán check on Riemann’s \(\Phi\) or \(\xi\), or
- \(\Lambda\le 0\) without assuming RH, or
- an explicit checked map if a Navier–Stokes (or other prize) bridge is claimed.

Do not merge Berry–Keating, Connes, GUE, \(\operatorname{diag}(\gamma_n)\),
the LP class, \(\Lambda\), Pólya frequency kernels, membrane Weyl laws,
enumeration, or random walk into one object.
