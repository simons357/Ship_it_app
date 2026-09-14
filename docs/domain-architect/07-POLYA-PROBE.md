# Pólya probe — what Domain Architect did with the full briefing

**Status:** exploratory classification, 2026-09-14  
**Riemann hypothesis status:** not claimed  
**Canonical SFE status:** unresolved  
**Run:** `python -m domain_architect --polya-probe`

This is the probe asked for after the five-role Hilbert–Pólya map: put every
relevant object in, let Domain Architect decide how many independently
specifiable components it needs (not a cap of five), include proven Pólya
entire-function facts, and see whether anything pops out.

Core roles remain an *interface*. Informal nicknames (“N-fingers”, “slots”)
are not product vocabulary. The method name is Functional Role Analysis.

---

## What was ingested

Theorems: Euler product, \(\xi(s)=\xi(1-s)\), Weil explicit formula,
\(N(T)\), Laguerre–Pólya class, Jensen polynomials (GORZ Hermite limit).

Candidates: Berry–Keating \(xp\), Connes absorption spectrum, Montgomery GUE,
circular \(\operatorname{diag}(\gamma_n)\).

Other books, classified not absorbed: retired SFE-HAM, Navier–Stokes.

Quantum extras DA promoted out of a five-role map: Hilbert space \(\mathcal H\),
inner product, domain/\(\mathcal B\), evolution \(D\), implicit \(\Xi=0\),
time-reversal breaking.

Registry: `HP-H001`–`HP-H010`.

---

## What DA returned

**25 independently specifiable components** (5 core + 20 extension / \(E\)).
Program complete: **false**. Evidence: Level 0 classification plus Level 1
laboratories (GUE is not \(\{\gamma_n\}\); the oscillator is rejected by \(N(T)\)).

The result that is actually a finding, not a Hamiltonian:

1. Quantum Hilbert–Pólya does not fit in five roles. That is how quantum
   “fits”: extra components, not a tighter five-letter formula.
2. There are **two parallel Pólya routes**, and they must not be merged:
   - Hilbert–Pólya: a self-adjoint \(H\) with \(\operatorname{spec}(H)=\{\gamma_n\}\);
   - Laguerre–Pólya: \(\xi(1/2+iz)\) in the LP class (all zeros real).
   Completing either would imply RH. Stating either does not. Feeding Pólya’s
   proven LP / Jensen calculus **does not fill \(H\)**; it restates reality of
   zeros in entire-function language.
3. **Usable surprise — a filter, not a Hamiltonian.** \(N(T)\) rejects the
   harmonic oscillator and any equally spaced spectrum: Riemann mean gaps
   shrink like \(1/\log T\), oscillator gaps do not. Hermite polynomials show
   up in the oscillator, in GUE, and as the GORZ limit of Jensen(\(\xi\)).
   That is a special-function collision, not identity of \(H\). Classical
   \(xp\) matches the leading von Mangoldt term (compatibility, not identity).
4. Berry–Keating \(xp\) is the only supplied *emission* Hamiltonian with an
   independent classical symbol that survives this Weyl screen. Connes is a
   different object. GUE is statistics. \(\operatorname{diag}(\gamma_n)\) is circular.
5. No checked transformation to Navier–Stokes or to a canonical SFE.

**Can proven Pólya fill \(H\)?** No. Pólya 1926 is the real attempt: a
sufficient condition for \(\int\Phi\cos(zt)\,dt\) to have only real zeros.
Riemann’s \(\Xi\) has that shape. The hypotheses are not a checked theorem
for that \(\Phi\). DA’s classification: this **relocates** the gap from
“find \(H\)” to “verify a kernel condition.” It does not occupy the \(H\)
role. Pólya’s Liouville-sum conjecture is **false**, so Pólya is not an
oracle for other Millennium problems.

---

## What DA still needs (it cannot invent these)

- One independent operator formula for \(H\), with \(\mathcal H\), inner
  product, and domain — not a merge of \(xp\), adeles, GUE, and \(\operatorname{diag}(\gamma_n)\).
- Essential self-adjointness.
- Whether an \(xp\) cutoff is \(P\), \(\mathcal B\), or extra regularization in \(E\).
- Weil from \(\operatorname{Tr} f(H)\), or \(\xi(s)\) as a proven determinant.
- If the LP route is chosen instead: an RH-free proof that \(\xi(1/2+iz)\) lies
  in the Laguerre–Pólya class.
- If a Navier–Stokes bridge is claimed: an explicit checked transformation.

There was no surprise Hamiltonian. The surprise is a **Weyl-law filter**:
DA can throw out the wrong \(H\) now, without proving RH.
