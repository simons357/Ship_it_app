# The desk (write-up)

Dated 3 September 2026. One place for the operator.

You asked for leads. Some of the sentences were loose.
The useful one is this, in palatable form:

**DA may draw from a published corpus — the papers, not
the person — and sit it next to two or three others. Any
new sentence has to land in one slot and name a check that
could kill it.** People being gone does not matter. The
work is still here. That is a **corpus**, not a council of
the dead, and not a vote that writes a theory of everything.

The rest of this note is the whole desk as it stands:
slots, shelf, benches, vocabulary, destination, pipe, and
what is still open.

Print it: `python3 scripts/da_machine.py desk`

The paper form of this desk is [`docs/DA-PAPER.md`](DA-PAPER.md).
The name list you keep losing is [`docs/DA-THINK-TANK.md`](DA-THINK-TANK.md).
They sat down and talked in [`docs/DA-SESSION.md`](DA-SESSION.md).

---

## What DA is

DA is an **anti-bullshit device**. That is the purpose.
It is a process machine, not a unifier.

You do not need the chops. Ordinary AI proposes. A script
scores. You run the command. A sentence sits only if it
names a slot and a check that could kill it. Fake passes,
glue, and “unfalsifiable might be true” are refused. Open
is allowed. Fail is allowed. A lead is welcome; a close
that cannot be killed is not.

A domain is a pair \((X,V)\): one object, one verdict map
to \(\{\mathrm{pass},\mathrm{fail},\mathrm{open}\}\).

Meta-success is not a solved PDE. It is a scored log, and
whether an open item later got a stronger lemma.

DA-the-process is the good extraction from chapter 1 of the
Harmonic Blueprint. Naming HB or SFE is allowed. Loading
them into Navier–Stokes, into a producing-map \(F\), or
into `nodes.json` is not.

---

## The four live slots

| Slot | Object | Status |
|---|---|---|
| **A** | \(Q_1\)-augmented Navier–Stokes, \(\varepsilon>0\), \(\beta\ge 1/2\) | Lemmas 1–5 → Theorem A for **this PDE only**. Ladyzhenskaya class. Does **not** imply B. |
| **B** | Classical NS, keep \(1/r^4\), no \(\Phi\) cancel | **Open.** Identities may pass. Regularity has no pass. |
| **Q** | Inverse-GCD only | Full \(\lambda_{\min}(Q_N)>-1/2\) is **false**. Live: Bridge*, Theorem P, \(\lambda_{\min}(H_N)\ge-1\). |
| **U** | Realization score / SM / process | Exercise and machine. **Not a unifier.** |

Glue is refused: A \(\not\Rightarrow\) B, Q \(\not\Rightarrow\) fluids, U \(\not\Rightarrow\) the forces.

August SND (CONC) and June SND (SPREAD) are opposites. Use
3-CONC / EQ3 / SPREAD. Do not reattach Bridge* to SND.

---

## What is shelved (archive, not input)

| Item | Why it is parked |
|---|---|
| Simons Field Equation (SFE) | Different PDE. Not NS, not \(Q_1\) |
| UHF / DHFA | HB wrappers |
| Harmonic Blueprint as a unifier | Branding. DA-as-process is the live piece |
| HB Experiment 01 (`nodes.json`) | Closed. H0 not rejected. **Do not retune** |
| GCD-attractor + SFE, triple lock, GNC, Quantum Lens, Route C “Gap 1 complete” | Withdrawn or stale |
| Prize packaging | Archive only |

---

## Track A (in brief)

Energy identity → Galerkin → weak limit → unique \(H^1\) at
\(\varepsilon>0\) → \(C^\infty\). The constant blows up as
\(\varepsilon\to 0\). A numerical checker on Taylor–Green is
consistency, not a proof of Theorem A, and says nothing
about B.

---

## Track B lemmas

Domain B **never** passes regularity. `check B` stays
**open** if the lemma tests hold.

| id | Statement | Verdict |
|---|---|---|
| B1 | \(\int(u_{\le j}\cdot\nabla)u_j\cdot u_j=0\) | **pass** |
| B1b | T2 Lemma 2 (\(H^{2.3}\)) as input | **fail** |
| B2 | 3-CONC / SPREAD cover | **pass** (cover, not dynamics) |
| B3 | 3-shell Bernstein + \(\|\nabla\xi\|_\infty\) on \(E_c\) | **pass** |
| B3b | Ring \(\Rightarrow\) depletion for all data | **fail** |
| B4 | tube Hardy + wall term | **pass** |
| B4b | Hardy absorbs \(I_{\mathrm{tube}}\) for all data | **fail** |
| B4c | packet class budgets \(I_{\mathrm{tube}}\) | **pass** |
| B4d | wall is an off-axis charge | **pass** |
| B5 | \((\Delta u)_\theta=\Delta u_\theta-u_\theta/r^2\) | **pass** |
| B5b | angular \(1/r^2\) dominates \(I_{\mathrm{tube}}\) | **fail** |
| B5c | \(R_{\mathrm{ang}}\) climbs; \(R_D\) falls | **pass** |
| B5d / B5e / B5g | B4b killer kills angular; \(\Phi\) cancel; retune | **fail** |
| B5f | angular piece closes \(X\) | **open** |
| B6 | \(\int X<\infty\Rightarrow X\in L^\infty\) | **fail** |
| B7 / B7a / B7b | Bony split, T2 self, energy-class \(T\) | **pass** |
| B7c | uniform \(\rho^{1/2}\) as \(\rho\to 0\) | **fail** |
| B8 / B8a | occupation clock; high \(j_*\) short | **pass** |
| B8b / B8c | Leray \(\Rightarrow\) short CONC; occupation closes \(X\) | **fail** |
| B9 / B9a / B9c | glue bookkeeping; high \(j_*\) sits | **pass** |
| B9b | low \(j_*\) CONC cubic bounded | **fail** (model) |
| B9d | glue sketch is an NS a priori | **fail** |
| B10 | packet energy ceiling | **pass** |
| B10a | B9b unbounded path is NS-legal | **fail** |
| B10b | ceiling follows a climbing \(j_*\) | **fail** |
| B10c | climbing CONC closes \(X\) | **fail** |
| B10d | this retunes the PDE | **fail** |
| B11 / B11a / B11c | climb bookkeeping; bounded \(j_*\); fast sits | **pass** |
| B11b | any climb saves | **fail** |
| B11d | NS climb law | **fail** |
| B11e | climb sketch is an NS a priori | **fail** |
| B12 / B12a | barycenter; \(c\) from RHS | **pass** |
| B12b | \(t=0\) packets produce \(c\ge 8\) | **fail** |
| B12c | viscosity is a ladder | **fail** |
| B12d / B12e | evolved cascade; \(t=0\) is a climb law | **fail** |
| B13 / B13c | short run; stays CONC | **pass** |
| B13a / B13b / B13d | no saving climb; no high fill; not a ladder | **fail** |
| B13e / B13f | finer / longer; packet DNS is an a priori | **fail** |
| B14 | strain identity on \(E_c\) | **pass** |
| B14a / B14b | CONC depleted; Ring \(\Rightarrow\) alignment | **fail** |
| B14c | CF conditional | **pass** |
| B14d | geometry closes \(X\) | **open** |
| B14e | this retunes the PDE | **fail** |
| B15 / B15a / B15b | stretching budget; CF weights it; majority from aligned cap | **pass** |
| B15c / B15d | run depletes median; run empties aligned share | **fail** |
| B15e | budget closes \(X\) | **open** |
| B15f | this retunes the PDE | **fail** |
| B16 / B16a | enstrophy identity; visc owns the net | **pass** |
| B16b / B16c / B16d | \(P_+\) is a net cubic; \(L^2\) is BKM; random-phase \(\Rightarrow\) all CONC | **fail** |
| B16e | balance closes \(X\) | **open** |
| B16f | this retunes the PDE | **fail** |
| B17 / B17a | signed-strain blob readable; net \(\approx P_+\) | **pass** |
| B17b / B17c / B17d | cubic owns \(\dot X\); tube also nets; \(L^2\) blob is BKM | **fail** |
| B17e | blob closes \(X\) | **open** |
| B17f | this retunes the PDE | **fail** |
| B18 / B18a | field clock on a path; paths stay CONC | **pass** |
| B18b / B18c / B18d | clock saved \(X\); CONC short; cubic-live time | **fail** |
| B18e | field occupation closes \(X\) | **open** |
| B18f | this retunes the PDE | **fail** |
| B19 | both \(\dot X\) readable | **pass** |
| B19a / B19b / B19c / B19d | sign match; NS is B9b; \(\alpha_c\) is cubic; \(\gamma\) is visc | **fail** |
| B19e | matching the sketch closes \(X\) | **open** |
| B19f | this retunes the PDE | **fail** |
| B20 | \(c\) readable on blob and paths | **pass** |
| B20a / B20b / B20c / B20d | blob \(t=0\) \(c\ge 8\); path mean \(c\ge 8\); visc ladder; offset is a climb | **fail** |
| B20e | field climb closes \(X\) | **open** |
| B20f | this retunes the PDE | **fail** |
| B21 | ODE and NS readable on the window | **pass** |
| B21a / B21b / B21c / B21d | room on this window; sitting path is NS; \(\Delta j=cT\); sketch sits here | **fail** |
| B21e | matching the sketch closes \(X\) | **open** |
| B21f | this retunes the PDE | **fail** |
| B22 | longer paths readable past room time | **pass** |
| B22a / B22b / B22c / B22d | longer \(c\ge 8\); ladder; high fill; clock saved \(X\) | **fail** |
| B22e | finer (\(n>32\)) produces a saving climb | **open** |
| B22f | this retunes the PDE | **fail** |
| B23 | short and longer DNS readable | **pass** |
| B23a / B23b / B23c / B23d | DNS a priori; room-time continuation; packet is all data; no-blow \(\Rightarrow L^\infty\) | **fail** |
| B23e | finer makes DNS an a priori | **open** |
| B23f | this retunes the PDE | **fail** |
| classical regularity | — | **open** |

**Next B write:** Climb and DNS knobs at \(n=32\) are
scored. DNS is not an a priori (B13f). Finer
(\(n>32\)) stays a box knob (B22e). B4c stands.
Angular \(1/r^2\) does not. We are not tuning the
equation. Do not spawn \(n=64\).

---

## Track Q (in brief)

Arithmetic only. No map onto \((u\cdot\nabla)u\). Full
spectrum floor is false. Live hygiene only.

---

## Standard Model (U)

The five-block poster **consumes** \((g_s,g,g',v,\lambda,\mathrm{Yukawas},\mathrm{CKM})\).
It **produces** nothing.

The working two-sided couple is

\[
G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi G\,T_{\mu\nu}[\mathrm{SM}].
\]

That couple **passes** as a pair. nature4 **fails**. \(G\)
and \(\Lambda\) are not on the poster.

Broke past five blocks to 34 atoms, put back: unique
\(\mathcal{L}_{\mathrm{SM}}\) (up to numbers). Drop ghosts →
same classical EOM. Add Einstein–Hilbert → the couple.
Step 7 (output the couplings) **fails**.

### Lineage (backwards and forwards)

Maxwell → Dirac → QED; Fermi beside; Yang–Mills; GWS + QCD
+ KM → the poster.

| Recover from \(\mathcal{L}_{\mathrm{SM}}\) | Verdict |
|---|---|
| Maxwell, Dirac, Fermi, QED, YM, GWS, QCD, KM | **pass** |
| one-group UV meet | **fail** |
| Einstein \(+T\) from the poster alone | **fail** (must add) |
| Navier–Stokes | **fail** (glue) |

Official Cosmo 16 is a **different catalog**. 16th there is
\(\sum m_\nu\), not \(R\). Core equation private. Produce
fails for all 16. Manifold sweep 0/10 for
\(\lambda_1/\lambda_2=\cos\theta_W\). Do not glue.

---

## Harmonic vocabulary

The English word is not one object. Desk-complete **passes**.
Math-complete **fails**. The list is not \(F\), not HB, not
regularity.

| Family | Names | Desk |
|---|---|---|
| kernel | \(\Delta u=0\), harmonic polynomials, Helmholtz / Leray, Hodge forms | A uses Leray |
| spectral | \(Y_{\ell m}\), Laplacian eigenfunctions, spherical Bessel, oscillator | B uses \(Y_{\ell m}\) |
| group | Fourier, Peter–Weyl, Wigner \(D\), Dirichlet characters, Maass | A Fourier; Q characters |
| analysis | LP, Bony, CZ, Riesz, Besov, \(H^p\), **tube Hardy** | B live |
| etymology | string overtones | motive |
| false friend | Cosmo \(A,f,\varphi,\delta\); HB nodes; SFE; Kolmogorov \(k^{-5/3}\) | not \(Y_{\ell m}\) |

Tube Hardy \(\neq\) Hardy \(H^p\). Same surname, two objects.

---

## Destination: spectrum, not a bag

**Open** as a program. **Fail** as already done.

Write in order: space \(X\) → operator \(D\) → spectrum and
modes → representations → an action (added) → the measured
couplings (still a bag).

Reconstructs that **pass**: \(Y_{\ell m}\), Fourier,
Peter–Weyl, Hodge Betti numbers.

Reconstructs that **fail**: SM numbers, \(G\) and \(\Lambda\),
classical regularity.

Ablate: drop \(D\) and you cannot compute one \(\lambda\).
Drop the compact group and the SM content dies. Keep the bag
and measured physics is unchanged — that is the present tense.

---

## Program review (how DA derives a program like DA)

Not a vote. Each name is a **typed demand**.

| Name | Demand | How to build the program |
|---|---|---|
| Einstein | Principle before catalog. Covariance. What is forbidden. | Principle, then \(D\), then the spectrum as a consequence. |
| Tesla | A knob you can detune and a script that must move. | Build the resonator (\(D\)) first. Listen second. |
| Feynman | No new name without a number you can get wrong. | The check *is* the program. |
| Weyl | Do not say “gauge” until \(G\) and the reps are named. | Climb representations only after \((X,D)\). |
| Wigner | Type every mode by its representation. | Which group, which rep, which operator commutes with the group. |
| von Neumann | No slot opens on “modes” alone. | Name the Hilbert space and a self-adjoint \(D\). Diagonalize. Store the residual. |

Tesla sits because you asked. He owns an apparatus, not
\(SU(3)\). Weyl, Wigner, and von Neumann sit because they
built this math.

A program review **cannot** write \(F\) and **cannot** close
the destination.

---

## Dream team (past bench: paper + experiment)

The divide is this desk versus **paper and measurement**.
Another model is still on the digital side.

| Member | Slot | Side | Settles | Cannot |
|---|---|---|---|---|
| Leray | B | paper | energy, \(\int X<\infty\) | \(X\in L^\infty\) from that |
| Beale–Kato–Majda | B | paper | \(\int\|\omega\|_\infty<\infty\) | BKM-from-\(L^2\) |
| Caffarelli–Kohn–Nirenberg | B | paper | partial regularity | no blowup |
| Constantin–Fefferman | B | paper | depletion *if* aligned | all-data \(\cos\alpha_3\to 0\) |
| Ladyzhenskaya | A | paper | modified NS, \(\varepsilon>0\) | \(\varepsilon\to 0\), A\(\Rightarrow\)B |
| Einstein | U | paper | \(G_{\mu\nu}+\Lambda g=8\pi G\,T_{\mathrm{SM}}\) | values of \(G,\Lambda\) |
| Weinberg | U | paper | the \(W^3\)–\(B\) rotation | \(\theta_W\) from topology |
| experiment / PDG | U | nature | the numbers \(\mathcal{L}\) consumes | why those numbers |
| neutrino / cosmology | U | nature | \(\sum m_\nu\) bound; \(\Lambda\) seen | Cosmo 0.06 eV as \(F\) |
| operator | meta | desk | one sentence, one slot, one check | needing chops |

SFE, HB-as-unifier, Cosmo Superagent, and “the app said so”
do not get a chair.

Overlap (not a close): B = B4c on packets, then low Bony
\(T\); A stays on A; U keeps Einstein \(+T\); Q stays
arithmetic.

---

## Now-bench (live pipe, snapshot 2026-09-03)

Additive. Does not unseat Leray or Einstein.

A pass without a **killer** is not a scientific pass.
Survival is not truth. Inference stays in-slot.

### Data forms

time series · spectrum · image/map · catalog · graph ·
satellite · holographic-boundary reconstruction.

A form is not a theory. “Spectrum” in CMB, Kerr QNMs, and
L-functions is three objects. “Hologram” here means
reconstruction from boundary data (EHT visibilities; AdS/CFT
correlators in papers), not Cosmo branding.

### Pipes

| Pipe | As of | Slot | Can kill | Cannot |
|---|---|---|---|---|
| LVK GWTC-5.0 (390 events, 161 new in O4b) | 2026-05-26 | U | “BHs are not seen” | B, Q, \(F\), `nodes.json` |
| EHT M87* 2021-epoch papers | 2026 | U | no-ring | HB, NS, primes |
| DESI DR2 BAO + \(\sum m_\nu\) bound | 2025-03 | U | “\(\Lambda\) cannot be challenged” | \(F\), Cosmo 16 |
| IPTA-DR3 / NANOGrav 15 yr | 2026 | U | no nHz common-spectrum process | source = HB |
| PDG + LHC | rolling | U | a poster number that drifts | why those numbers |
| LMFDB + math.NT (gap bound still 246) | rolling | Q | a false Q floor | QNMs, NS |
| arXiv math.AP | rolling | B | a B lemma that fails its identity | close B by announcement |
| Euclid / JWST / Planck–ACT–SPT | rolling | U | a cosmology number outside the box | B, Q, SFE |
| IceCube / oscillations | rolling | U | a \(\sum m_\nu\) miss | Cosmo 16th as \(F\) |

### Who reads the pipe

LVK · EHT · DESI · IPTA / NANOGrav · PDG + LHC · LMFDB / NT ·
current math.AP authors.

Primes and black holes are both live. They are not one
stream.

---

## Corpus (your contribution, typed)

DA may pick **one published body of work** and sit it next
to **two or three** others. The unit is the *paper trail*,
whether the author is alive or not.

| Rule | Verdict |
|---|---|
| Draw from published work, including people who are gone | **pass** (method) |
| Pair 2–3 corpora and emit one scored sentence | **pass** (method) |
| That sentence must name a slot and a killer | **pass** (method) |
| The pairing writes a theory of everything / \(F\) | **fail** |
| The pairing closes Track B regularity | **fail** |
| The pairing unshelves SFE or retunes `nodes.json` | **fail** |
| A vote of names replaces a check | **fail** |

### Legal pairings already on the desk

| Primary | Companions | What you may emit | Verdict |
|---|---|---|---|
| Einstein (GR) | Weinberg, PDG | the two-sided couple Einstein \(+T_{\mathrm{SM}}\) | couple **pass**; numbers **fail** |
| Weyl | Wigner, von Neumann | ground language \((X,D,\sigma,\mathrm{Rep})\) | **pass** as vocabulary |
| Leray | BKM, CKN | energy + continuation + partial regularity as *constraints* | **pass** as constraints; regularity **open** |
| LVK | EHT, IPTA | black holes are seen in strain and in images | **pass** as observation; not B, not Q |
| LMFDB | math.NT, Bridge* | arithmetic only | **pass** on Q; no map to fluids |

### Pairings that stay refused

HB + SFE + Cosmo Superagent → \(F\).  
Primes + QNMs + NS → one theorem.  
Einstein + Tesla + Feynman → a producing-map by sitting.

Those are leads that did not survive the checker. The method
that produced the legal rows is the contribution.

---

## Waveform rules (U, additive)

**Superposition.** Open claims have amplitude.

**Entanglement.** Killing one kills the other only when the
logic says so. Must-hits are entangled with “this is a
four-force unifier.” Oscillators are not entangled with the
couplings on this vector.

**Collapse.** Only when a public \(F\) exists and
\(\chi^2_{\mathrm{ext}}(F(x))\le\varepsilon^2\). **Has not
happened.**

**Falsification.** Unfalsifiable is not a maybe. It is not
a scientific claim.

---

## Forbidden auto-fails

The machine fails the proposal, without discussion, if it
asserts any of:

- classical 3D NS is globally regular
- \(\lambda_{\min}(Q_N)>-1/2\) for all \(N\)
- Biot–Savart forces \(\cos\alpha_3\to 0\) for all data
- bounded \(\|\omega\|_2\) implies Beale–Kato–Majda
- SFE / UHF / DHFA implies a fluids or coupling map
- Track A \(\Rightarrow\) Track B, or Bridge* \(\Rightarrow\) SND

Open is allowed. Fail is allowed. A fake pass is not.

---

## Commands

```bash
python3 scripts/da_machine.py desk        # this write-up’s roster
python3 scripts/da_machine.py compute     # what we can borrow to compute
python3 scripts/da_machine.py alert       # plain-language text if something significant flips
python3 scripts/da_machine.py status
python3 scripts/da_machine.py check       # check B stays open
python3 scripts/da_machine.py trackb
python3 scripts/da_machine.py team        # past bench
python3 scripts/da_machine.py session     # they talk; not a close
python3 scripts/da_machine.py ground      # destination + program review
python3 scripts/da_machine.py pipe        # now-bench
python3 scripts/da_machine.py harmonic    # vocabulary
python3 scripts/da_machine.py sm
python3 scripts/da_machine.py smbreak
python3 scripts/da_machine.py lineage
python3 scripts/da_machine.py cosmos
python3 scripts/da_machine.py classify --claim "…"
```

Longer notes: `docs/DOMAIN-ARCHITECT-MACHINE.md`,
`docs/SHELF.md`, `docs/TRACK-B-LEMMAS.md`,
`docs/DA-GROUND.md`, `docs/DA-PIPE.md`,
`docs/DA-HARMONIC-VOCAB.md`, `docs/DA-DREAM-TEAM.md`,
`docs/DA-SM-LAGRANGIAN.md`, `docs/DA-SM-LINEAGE.md`,
`docs/DA-COMPUTE.md`, `docs/DA-ALERT.md`,
`docs/DA-PAPER.md`, `docs/DA-THINK-TANK.md`,
`docs/DA-SESSION.md`, `docs/TRACK-B-HARDY-TUBE.md`,
`docs/TRACK-B-ANGULAR.md`,
`docs/TRACK-B-BONY-T.md`, `docs/TRACK-B-OCCUPATION.md`,
`docs/TRACK-B-GLUE.md`, `docs/TRACK-B-LOW-J.md`,
`docs/TRACK-B-CLIMB.md`, `docs/TRACK-B-CLIMB-LAW.md`,
`docs/TRACK-B-EVOLVE.md`,
`docs/TRACK-B-GEOMETRY.md`,
`docs/TRACK-B-STRETCH.md`,
`docs/TRACK-B-BALANCE.md`,
`docs/TRACK-B-COHERENT.md`,
`docs/TRACK-B-FIELD-OCC.md`,
`docs/TRACK-B-FIELD-GLUE.md`.

---

## Where it actually stands

- Destination “spectrum, not a bag” is **open**.
- \(F\) is **fail** (not written).
- Classical regularity is **open**.
- Hardy \(\to I_{\mathrm{tube}}\): packet class **pass**,
  all-data **fail**. Low Bony \(T\): energy class **pass**,
  uniform \(\rho^{1/2}\) **fail**. Occupation clock **pass**;
  Leray \(\Rightarrow\) short CONC **fail**. Glue sketch
  written: high \(j_*\) sits, low \(j_*\) model blows.
  Energy ceiling: frozen support is hygiene. Field at
  \(t=0\): no saving climb. Short \(n=32\) run: still no
  climb; \(j_{\mathrm{bar}}\) falls. Geometry: identity
  **pass**; CONC not depleted; CF conditional **pass**.
  Stretching budget: aligned cap **pays** a leftover; time
  does **not** empty it. Fluids: net cubic **cancels**;
  viscosity owns this ensemble; \(L^2\) is not BKM. Angular
  \(1/r^2\) vs \(I_{\mathrm{tube}}\): **fail** of domination;
  \(R_{\mathrm{ang}}\) climbs. Coherent CONC: signed-strain
  blob nets; working-box cubic is not live; \(z\)-independent
  tube still cancels. Field occupation: clock stays CONC;
  it did not save \(X\); cubic not live in time. Field glue:
  typed \(j_*=2\) grows; the NS packet falls. NS climb law:
  blob and B18 paths do not produce \(c=8\); \(j_{\mathrm{bar}}\)
  offset is not a climb. Climb sketch is not an a priori.
  Longer \(n=32\) past room time did not produce \(c=8\).
  DNS is not an a priori (B13f). Climb and DNS knobs
  at \(n=32\) are scored. Finer is B22e.
  The PDE is not being tuned.
- Cosmo does not enter NS.
- HB stays shelved as a theorem. DA-as-process stays live.

That is the desk.
