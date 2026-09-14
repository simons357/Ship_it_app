# Hilbert–Pólya program — Functional Role Analysis

**Status:** organizational completeness audit, not a proof  
**Riemann hypothesis status:** not claimed  
**Canonical SFE status:** unresolved  
**Informal nickname “five fingers”:** not used. The five core roles are \(P,H,\psi,\lambda,\Phi\).

This note answers two requests:

1. Break Hilbert–Pólya into pieces that can be specified or blocked separately.
2. Write those pieces as a Domain Architect instance, including the hoped-for
   identity that a physical quantum system has energy levels equal to the
   nontrivial zeros.

It does **not** construct that system. Assigning the zeros to the realized
output \(\Phi\) is the *target identity* of the program. It is not a fill of
\(H\).

Run:

```bash
python -m domain_architect --hilbert-polya
python -m domain_architect --hilbert-polya --candidate berry-keating
python -m domain_architect --hilbert-polya --candidate montgomery-gue
python -m domain_architect --polya-probe
python -m domain_architect --millennium-look
python -m unittest tests.test_hilbert_polya tests.test_polya_probe tests.test_millennium_overlap
```

---

## 1. What can be organized, and what cannot be set

Hilbert–Pólya is the implication

\[
H=H^\ast,\qquad \operatorname{spec}(H)=\{\gamma_n\}
\quad\Longrightarrow\quad
\text{every nontrivial zero of }\zeta\text{ has real part }1/2.
\]

The implication is valid. The missing object is an independently specified
self-adjoint \(H\) together with a proof of the spectral identity.

Functional Role Analysis may record the *claimed* realization

\[
\Phi_{\mathrm{target}}=\operatorname{spec}(H)\stackrel{?}{=}\{\gamma_n\}
\]

as a **target identity**. It may not copy \(\{\gamma_n\}\) into the \(H\),
\(\lambda\), or \(\Phi\) slots as a definition. That move is circular:

- \(H:=\operatorname{diag}(\gamma_n)\) on \(\ell^2\) is self-adjoint for any
  real sequence. Using the *computed* zeros gives those zeros only. Using
  *all* nontrivial zeros as a real sequence assumes RH.
- Setting \(\Phi:=\) “the zeros” without a formula for \(H\) is a label, not
  a quantum system.
- GUE / random-matrix agreement is a universality class for *spacings*.
  Many operators share it. It is not the identity \(\operatorname{spec}(H)=\{\gamma_n\}\).

Evidence for this document: **Level 0** (coherent classification), except the
negative GUE laboratory, which is **Level 1** (a random GUE matrix is not
the sequence \(\gamma_n\)). Nothing here is Levels 2–6, and nothing is Clay.

---

## 2. Core-role interface (not a cap of five)

\[
\Phi=\mathcal F(P,H,\psi,\lambda;E).
\]

\(P,H,\psi,\lambda,\Phi\) are interface letters. Domain Architect decides
how many independently specifiable components the subject needs — 7, 8, 15,
or more. Quantum Hilbert–Pólya does not fit in five. The extras below are
how it fitted.

| Role | Target occupant | Independent of zeros? | Status |
|---|---|---|---|
| \(P\) | Domain of \(H\): subspace, boundary conditions, self-adjoint extension, or cutoff projector | must be | must be declared; circular if \(P\) is “project onto the zeta-zero eigenspace” |
| \(H\) | An operator **formula** that does not mention the zeros | must be | **missing** — load-bearing gap |
| \(\psi\) | Eigenfunctions of that \(H\) | yes, once \(H\) exists | downstream of \(H\) |
| \(\lambda\) | Eigenvalue parameter \(E_n\) in \(H\psi=E_n\psi\) (subtype: **eigenvalue**, not a transfer function) | the *parameter* is; the *claim* \(E_n=\gamma_n\) is not a fill | target identity |
| \(\Phi\) | Spectral data of \(H\) (point spectrum, spectral measure, or \(\det\)) | the *kind* of output is; \(\Phi:=\{\gamma_n\}\) is not a fill | target identity |

Independently necessary structure that must sit in \(E\). Do not hide it
to fake a five-letter count:

- Hilbert space \(\mathcal H\) and inner product;
- operator domain \(D(H)\) and deficiency indices;
- archimedean / Gamma factor of \(\xi\);
- Weil explicit formula (primes on the geometric side);
- multiplicity;
- continuous versus point spectrum;
- time-reversal breaking if GUE rather than GOE is expected;
- regularization / cutoff if the classical symbol is \(xp\).

A completed interface *map* is still only classification. Completeness of the
**program** requires the pieces in §3.

---

## 3. Piece-by-piece work breakdown

Each parent piece has **children** (sub-pieces). Refusals are path guidance.
Run: `python -m domain_architect --breakdown-children`.

### Configuration layer (UHF) — can be started now

| ID | Piece | Tackle now? | Depends on | Status |
|---|---|---|---|---|
| HP-U1 | Declare \(\mathcal H\) without referring to zeros | yes | — | open; many spaces, none canonical |
| HP-U2 | Inner product, units, normalization | yes | HP-U1 | open |
| HP-U3 | Domain \(D(H)\subset\mathcal H\) and boundary data \(\mathcal B\) | yes, once a formula exists | HP-U1, HP-S0 | open |

These are ordinary functional-analysis declarations. They do not use RH.

### Realization layer — the blocked core

| ID | Piece | Tackle now? | Depends on | Status |
|---|---|---|---|---|
| **HP-S0** | Independent formula for \(H\) | yes as a search; currently empty | — | **missing** |
| HP-S1 | Essential self-adjointness | no | HP-S0, HP-U3 | blocked |
| HP-S2 | Control discrete / continuous spectrum and multiplicities | no | HP-S1 | blocked |
| HP-S3 | Weyl law matching \(N(T)=(T/2\pi)\log(T/2\pi e)+S(T)+O(1)\) | no | HP-S2 | blocked; necessary, not sufficient |
| **HP-S5** | Spectral identity: \(E\in\operatorname{spec}(H)\) iff \(\zeta(1/2+iE)=0\), or \(\xi(s)\) equals a proven entire factor times \(\det\bigl((s-1/2)/i-H\bigr)\) | no | HP-S1, HP-T2 | blocked; **this step is RH given self-adjointness** |

### Trace layer — one theorem, one missing derivation

| ID | Piece | Tackle now? | Status |
|---|---|---|---|
| HP-T1 | Weil explicit formula (zeros \(\leftrightarrow\) primes) | yes: it is already a theorem | **theorem**. Record in \(E\). Do not rename it \(H\). |
| HP-T2 | Derive that formula from \(\operatorname{Tr} f(H)\) for an independent dynamical system whose periodic orbits are primes | no | blocked on HP-S0 and HP-S1 |

### Statistics layer — corollary, not an ingredient

| ID | Piece | Tackle now? | Status |
|---|---|---|---|
| HP-G1 | Montgomery pair correlation / Odlyzko / Keating–Snaith GUE dictionary | yes as numerics and conjectures | cannot replace HP-S5 |

A frozen GUE matrix can have Wigner–GUE spacings and still fail to equal
\(\{\gamma_n\}\) after any affine rescaling. The software laboratory
`gue_is_not_riemann_spectrum` records that negative fact. It does not
estimate a probability for RH.

### Evolution layer (DHFA) — not a shortcut

| ID | Piece | Status |
|---|---|---|
| HP-D1 | \(e^{-iHt}\) exists once HP-S1 holds | blocked on HP-S1; dynamics do not construct \(H\) |

### Forbidden fills (enforced)

| ID | Refusal |
|---|---|
| HP-F1 | \(\Phi:=\) zeros, \(\lambda:=\{\gamma_n\}\), or \(H:=\operatorname{diag}(\gamma_n)\) as a *definition* of the instance |

---

## 4. What “set \(\Phi\) to the zeros” actually does

The honest FRA move is:

\[
\Phi_{\mathrm{target}}:=\operatorname{spec}(H),\qquad
\text{claim: }\operatorname{spec}(H)=\{\gamma_n\}.
\]

That records a **claim** at evidence Level 0. Completeness still fails
because \(H\) is unspecified.

The dishonest move is to treat that claim as an instance:

\[
H:=\operatorname{diag}(\gamma_n)\quad\text{or}\quad
\Phi:=\{\gamma_n\}\text{ with }H\text{ blank}.
\]

Software: `is_circular_fill` returns true; CLI candidate `target-identity`
and `diagonal-zeros` are flagged circular; both remain incomplete.

There is no third move in which the five-role grammar *produces* \(H\).
The grammar classifies an instance after \(H\) is given.

---

## 5. Historical candidates (do not merge)

These are distinct formulas. Shared motivation is not a transformation.

| ID | Formula | Independent \(H\)? | What it actually supplies | Missing |
|---|---|---|---|---|
| HP-H001 | Hilbert–Pólya statement | no (a strategy) | program statement | all construction pieces |
| HP-H002 | Weil explicit formula | no | HP-T1 (theorem in \(E\)) | Hamiltonian |
| HP-H003 | Berry–Keating \(H=xp\) (or \((xp+px)/2\)) with cutoff | **yes**, as a classical symbol | a candidate formula, heuristic periodic orbits | unique self-adjoint quantization, cutoff as extra structure, spectral identity |
| HP-H004 | Connes absorption / adelic construction | yes, as a different object | a different spectral picture (missing lines) | compact self-adjoint \(H\) with point spectrum \(\{\gamma_n\}\) |
| HP-H005 | Montgomery–Odlyzko GUE pair correlation | no | HP-G1 | all of HP-S0–S5 |
| HP-H006 | \(\xi(s)=\xi(1-s)\) | no | analytic input to a determinant identity | the determinant |
| HP-H007 | \(\Phi:=\{\gamma_n\}\) or \(H=\operatorname{diag}(\gamma_n)\) | no | a circular fill | everything that would count as a construction |

Berry–Keating and Connes are **incompatible as Hamiltonians**: emission
eigenvalues versus absorption holes. They may be discussed as related
heuristics. They must not be averaged into one operator.

The retired Fock model `SFE-HAM` (inverse-GCD occupation Hamiltonian) is a
different book. It is not a Hilbert–Pólya operator and is not revived here.

---

## 6. Order of attack (what is actually piece-by-piece)

Work that does not wait on RH:

1. Keep the checklist and circular-fill refusal (this repository).
2. For each published candidate, score it against HP-U\* / HP-S\* / HP-T\*
   without promoting heuristics to identities (CLI `--candidate`).
3. Functional analysis of a *named* operator: deficiency indices of a
   chosen quantization of \(xp\), effect of a declared cutoff \(P\),
   Weyl term of that regularized operator.
4. Numerical diagonalization of a *frozen* truncation versus Odlyzko zeros,
   with the Hamiltonian formula hashed before the zero table is opened
   (`protocol.freeze_protocol`). Agreement is evidence of approximation,
   not HP-S5.
5. Keep GUE tests in the statistics book. Never retune \(H\) on the zeros
   and then score the same zeros as confirmation.

Work that *is* RH, and should be named as such:

- HP-S1 + HP-S5 (self-adjoint \(H\) whose spectrum is exactly the zeros);
- HP-T2 at theorem strength (Weil formula derived from that \(H\)).

There is no remaining “small piece” that turns GUE matching into HP-S5.

---

## 7. Registry and nulls

Machine-readable records:

- equations `HP-H001`–`HP-H007` in `data/domain_architect/historical_equations.json`
- conflicts among those IDs and against `SFE-H003`
- `NULL-HP-CIRCULAR` — assigning \(\Phi\) to the zeros does not specify \(H\)
- `NULL-HP-GUE` — GUE matching is not spectral identity
- `NULL-HP-COMPLETE` — no candidate completes the checklist

Disposition: theorems and the program statement are retained as such;
incomplete Hamiltonians stay `UNRESOLVED`; circular fills are `RETIRE` as
constructions and kept as historical records.

---

## 8. What this freeze refuses

- Treating a five-role map as a derived Hamiltonian.
- Treating representation of the Weil explicit formula as derivation of a
  quantum system.
- Merging Berry–Keating, Connes, GUE statistics, and \(\operatorname{diag}(\gamma_n)\).
- Claiming the Riemann hypothesis, a Millennium result, or a canonical SFE.
- Reintroducing the informal nickname “five fingers” as product language.
