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
scores. You run the command. The living roster and the live
feed sit inside that loop. The shape is an agent. It is
not a closer. A sentence sits only if it
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
\(\varepsilon>0\) → \(C^\infty\). Theorem A **pass** for this
PDE. The constant blows up as \(\varepsilon\to 0\); that row
stays **open**. A\(\Rightarrow\)B **fail**. Catalog:
[`TRACK-A-LEMMAS.md`](TRACK-A-LEMMAS.md).
Gap: [`TRACK-A-GAP.md`](TRACK-A-GAP.md).
`python3 scripts/da_machine.py tracka`

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
| B5f | angular piece closes \(X\) | **fail** |
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
| B14d | geometry closes \(X\) | **fail** |
| B14e | this retunes the PDE | **fail** |
| B15 / B15a / B15b | stretching budget; CF weights it; majority from aligned cap | **pass** |
| B15c / B15d | run depletes median; run empties aligned share | **fail** |
| B15e | budget closes \(X\) | **fail** |
| B15f | this retunes the PDE | **fail** |
| B16 / B16a | enstrophy identity; visc owns the net | **pass** |
| B16b / B16c / B16d | \(P_+\) is a net cubic; \(L^2\) is BKM; random-phase \(\Rightarrow\) all CONC | **fail** |
| B16e | balance closes \(X\) | **fail** |
| B16f | this retunes the PDE | **fail** |
| B17 / B17a | signed-strain blob readable; net \(\approx P_+\) | **pass** |
| B17b / B17c / B17d | cubic owns \(\dot X\); tube also nets; \(L^2\) blob is BKM | **fail** |
| B17e | blob closes \(X\) | **fail** |
| B17f | this retunes the PDE | **fail** |
| B18 / B18a | field clock on a path; paths stay CONC | **pass** |
| B18b / B18c / B18d | clock saved \(X\); CONC short; cubic-live time | **fail** |
| B18e | field occupation closes \(X\) | **fail** |
| B18f | this retunes the PDE | **fail** |
| B19 | both \(\dot X\) readable | **pass** |
| B19a / B19b / B19c / B19d | sign match; NS is B9b; \(\alpha_c\) is cubic; \(\gamma\) is visc | **fail** |
| B19e | matching the sketch closes \(X\) | **fail** |
| B19f | this retunes the PDE | **fail** |
| B20 | \(c\) readable on blob and paths | **pass** |
| B20a / B20b / B20c / B20d | blob \(t=0\) \(c\ge 8\); path mean \(c\ge 8\); visc ladder; offset is a climb | **fail** |
| B20e | field climb closes \(X\) | **fail** |
| B20f | this retunes the PDE | **fail** |
| B21 | ODE and NS readable on the window | **pass** |
| B21a / B21b / B21c / B21d | room on this window; sitting path is NS; \(\Delta j=cT\); sketch sits here | **fail** |
| B21e | matching the sketch closes \(X\) | **fail** |
| B21f | this retunes the PDE | **fail** |
| B22 | longer paths readable past room time | **pass** |
| B22a / B22b / B22c / B22d | longer \(c\ge 8\); ladder; high fill; clock saved \(X\) | **fail** |
| B22e | finer (\(n>32\)) produces a saving climb | **fail** |
| B22f | this retunes the PDE | **fail** |
| B23 | short and longer DNS readable | **pass** |
| B23a / B23b / B23c / B23d | DNS a priori; room-time continuation; packet is all data; no-blow \(\Rightarrow L^\infty\) | **fail** |
| B23e | finer makes DNS an a priori | **fail** |
| B23f | this retunes the PDE | **fail** |
| B24 | B4c and B5b readable together | **pass** |
| B24a / B24b / B24c / B24d | angular closes \(X\); B4c is an a priori; \(R_D\ll 1\Rightarrow L^\infty\); revive Hardy/\(\Phi\) | **fail** |
| B24e | packet geometry closes \(X\) | **fail** |
| B24f | this retunes the PDE | **fail** |
| B25 | identity, undepleted CONC, CF readable | **pass** |
| B25a / B25b / B25c / B25d | depletion closes \(X\); Lipschitz+CF is an a priori; median is a class; CF is BKM | **fail** |
| B25e | aligned budget closes \(X\) | **fail** |
| B25f | this retunes the PDE | **fail** |
| B26 | budget, CF weight, majority readable | **pass** |
| B26a / B26b / B26c / B26d | share closes \(X\); time emptying is continuation; share is a class; aligned budget is \(\int\|\omega\|_\infty\) | **fail** |
| B26e | enstrophy balance closes \(X\) | **fail** |
| B26f | this retunes the PDE | **fail** |
| B27 | identity, visc-owned net, cancelled \(P_+\) readable | **pass** |
| B27a / B27b / B27c / B27d | visc ensemble closes \(X\); cancel is all-data; decay is continuation; identity is \(\int\|\omega\|_\infty\) | **fail** |
| B27e | signed-strain blob closes \(X\) | **fail** |
| B27f | this retunes the PDE | **fail** |
| B28 | blob, one-sided net, visc-owned cubic readable | **pass** |
| B28a / B28b / B28c / B28d | one-sided leftover closes \(X\); sign is a class; peaked \(L^2\) is \(\int\|\omega\|_\infty\); \(\nu\) knob is continuation | **fail** |
| B28e | field occupation closes \(X\) | **fail** |
| B28f | this retunes the PDE | **fail** |
| B29 | clock, full CONC, visc-owned \(X\) readable | **pass** |
| B29a / B29b / B29c / B29d | stay closes \(X\); \(\tau_{\mathrm{C}}=T\) is a short visit; CONC is a live cubic; clock is \(\int\|\omega\|_\infty\) | **fail** |
| B29e | matching the sketch closes \(X\) | **fail** |
| B29f | this retunes the PDE | **fail** |
| B30 | rates, sign mismatch, model-grows / field-falls readable | **pass** |
| B30a / B30b / B30c / B30d | match closes \(X\); shrinking \(\alpha_c\) is continuation; wrong-sign ODE is NS; match is \(\int\|\omega\|_\infty\) | **fail** |
| B30e | a field climb law closes \(X\) | **fail** |
| B30f | this retunes the PDE | **fail** |
| B31 | field \(c\), blob miss, path-mean miss readable | **pass** |
| B31a / B31b / B31c / B31d | field climb closes \(X\); offset is continuation; visc fall is a class; reading \(c\) is \(\int\|\omega\|_\infty\) | **fail** |
| B31e | matching the prescribed-\(c\) sketch closes \(X\) | **fail** |
| B31f | this retunes the PDE | **fail** |
| B32 | window rates, missed room, sketch-grows / field-falls readable | **pass** |
| B32a / B32b / B32c / B32d | match closes \(X\); cashing B11c is continuation; growing sketch is NS; window is \(\int\|\omega\|_\infty\) | **fail** |
| B32e | a finer box closes \(X\) | **fail** |
| B32f | this retunes the PDE | **fail** |
| B33 | longer miss, empty high shells, short window readable | **pass** |
| B33a / B33b / B33c / B33d | finer closes \(X\); cashing \(n=64\) is continuation; unrun \(n=64\) is NS; finer is \(\int\|\omega\|_\infty\) | **fail** |
| B33e | finer makes DNS an a priori | **fail** |
| B33f | this retunes the PDE | **fail** |
| B34 | DNS miss, refused no-blow, finer-box miss readable | **pass** |
| B34a / B34b / B34c / B34d | finer DNS closes \(X\); cashing \(n=64\) DNS is continuation; unrun finer DNS is NS; finer DNS is \(\int\|\omega\|_\infty\) | **fail** |
| B34e | a leftover close writes regularity | **fail** |
| B34f | this retunes the PDE | **fail** |
| B35 | finer-box miss, finer-DNS miss, leftover catalog readable | **pass** |
| B35a / B35b / B35c / B35d | leftover close writes \(X\); scoring leftovers is continuation; stack of fails is NS; leftover closes are \(\int\|\omega\|_\infty\) | **fail** |
| B35e | classical regularity is decided by leftover closes | **fail** |
| B35f | this retunes the PDE | **fail** |
| B36 | leftover catalog miss, leftover-close miss readable | **pass** |
| B36a / B36b / B36c / B36d / B36e | leftover knobs decide regularity; catalog is continuation; naming the object is NS; leftover catalog is \(\int\|\omega\|_\infty\); this write decides regularity | **fail** |
| B36f | this retunes the PDE | **fail** |
| B37 | three holes of \(\mathcal{R}\) readable on \(n=32\) | **pass** |
| B37a / B37b / B37c / B37d / B37e | naming holes is a closed estimate; readable is integrable; synthetic \(\mathcal{R}\) is NS; residual is \(\int\|\omega\|_\infty\); residual decides regularity | **fail** |
| B37f | this retunes the PDE | **fail** |
| B38 | Miller \(\lambda_2^+\) is a different cut from hole 2 | **pass** |
| B38a / B38b / B38c / B38d / B38e | the cut is a closed estimate; a gap is integrable \(\mathcal{R}\); reading \(\lambda_2^+\) is NS; Miller cut is \(\int\|\omega\|_\infty\); this write decides regularity | **fail** |
| B38f | this retunes the PDE | **fail** |
| B39 | identity holds; \(\det_+\) is the same cut as \(\lambda_2^+\) | **pass** |
| B39a / B39b / B39c / B39d / B39e | empty rename is a closed estimate; empty is integrable \(\mathcal{R}\); reading \(\det S\) is NS; empty rename is \(\int\|\omega\|_\infty\); sitting down decides regularity | **fail** |
| B39f | this retunes the PDE | **fail** |
| B40 | A1 off, A2 live on the box | **pass** |
| B40a / B40b / B40c / B40d / B40e | blanks are a closed estimate; blanks are integrable \(\mathcal{R}\); naming blanks is NS; blanks are \(\int\|\omega\|_\infty\); this write decides regularity | **fail** |
| B40f | this retunes the PDE | **fail** |
| B41 | A2 ratio stays on the B15 path | **pass** |
| B41a / B41b / B41c / B41d / B41e | a flat path is a closed estimate; a flat path is integrable \(\mathcal{R}\); reading A2 along the path is NS; a flat ratio is \(\int\|\omega\|_\infty\); this write decides regularity | **fail** |
| B41f | this retunes the PDE | **fail** |
| classical regularity | — | **open** |

**Next B write:** A1 is off. A2 is live. A2 does not
blow on the B15 path. Beirão da Veiga–Berselli sit as
an A1 wall: a weaker geometric if is still an if.
Grujić arXiv 2607.08866 sits as a log-bmo if: still
an if, not all-data A1. Giga–Miura sit as Type I plus
continuous direction: two ifs, not all-data A1.
Constantin–Fefferman–Majda 1996 sits as Euler: a
different equation, not NS A1. Šverák doors: ruled-out
self-similar is not an a priori; Liouville and ancient
remain doors, not a bound. Jia–Šverák forward
self-similar large-data existence is not an a priori.
Guillod–Šverák numerical pitchfork is not an a priori
and not a singularity. Hou–Wang–Yang arXiv 2509.25116
announced unforced Leray–Hopf non-uniqueness is not an
a priori and not regularity. Lei–Ren–Tian arXiv 2501.08976
double-cone if is still an if, not all-data A1.
Chen–Strain–Tsai–Yau axisymmetric Type I exclusion is
not an a priori. Kozono–Taniuchi BMO continuation is
still an if, not an a priori. Neustupa–Penel
one-component if is still an if, not all-data
regularity. Escauriaza–Seregin–Šverák \(L^3\)
endpoint is a criterion, not an a priori.
KNSS ancient Liouville is a door, not an a priori.
Gabriel Koch is not Herbert Koch. Chae Triebel–Lizorkin
geometric if is still an if, not all-data A1. Scheffer
stays out of the living room. Chemin–Gallagher large
Besov data is still a nonlinear smallness condition,
not all-data regularity. Cannone–Planchon critical
Besov mild is small-data self-similar, not Jia and
not a bound on \(X\). Lin's new proof of CKN is still
\(\varepsilon\)-regularity, not no blowup. Vasseur's
De Giorgi proof of CKN is the same theorem, not no
blowup. Farwig very weak solutions are a different
class, not Leray–Hopf and not a bound on classical
\(X\). Sohr stays out. Cheskidov energy equality in an
Onsager class is a condition, not a bound on \(X\).
Masmoudi uniqueness of mild solutions in \(L^N\) is
uniqueness, not a bound on \(X\).
Wolf local pressure is the same \(\varepsilon\)-regularity
without a global pressure, not no blowup.
Galdi physically reasonable solutions are steady
exterior flow, not evolutionary \(X\).
Temam's 3D attractor assumes the solution stays
smooth. That if is not a bound on \(X\). Foias stays
out. Isett Onsager is Euler Hölder \(1/3\), not a bound
on NS \(X\). Tsai local-energy self-similar exclusion
is not an a priori on \(X\).
Lemarié-Rieusset local Leray solutions are a different
class, not a bound on global \(X\).
Danchin density-dependent NS is a different equation,
not a bound on homogeneous \(X\). Heywood stays out.
Kukavica unique continuation is vanishing order, not a
bound on \(X\). Not the one-component chair.
Barker Type I iff ancient is an equivalence, not a
bound on \(X\). Forced Leray stays Albritton.
Barker sequential \(L^3\) Liouville is not ESS.
Robinson a posteriori regularity is a numerical
certificate, still an if, not a bound on \(X\).
Pavlović critical ill-posedness is norm inflation in
\(\dot B^{-1}_{\infty,\infty}\), not a bound on \(X\).
Small critical stays Koch–Tataru. Bourgain stays out.
Rusin minimal \(\dot H^{1/2}\) singularity data is
compactness of a hypothetical set, not a bound on
\(X\). It does not prove a singularity. Šverák stays
doors. Jia stays existence.
Germain weak-strong uniqueness (JDE 2006) is
uniqueness, not a bound on \(X\). Mild uniqueness
stays Masmoudi. Water waves stay off this chair.
Cao primitive equations (*Ann. of Math.* 2007) are
hydrostatic. A different equation is not a bound on
NS \(X\). Titi stays off. Robinson stays a posteriori.
Sit down on leftover-close B42. Stretching budget is not an a priori
(B15e). Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). Leftover close is not an a priori (B34e). Regularity leftover is not an a priori (B35e). Regularity stays open. Finer
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
python3 scripts/da_machine.py status      # slots + last feed age; no network
python3 scripts/da_machine.py check       # check B stays open
python3 scripts/da_machine.py tracka      # Q1-augmented NS; this PDE only
python3 scripts/da_machine.py trackb
python3 scripts/da_machine.py team        # past bench
python3 scripts/da_machine.py session     # they talk; not a close
python3 scripts/da_machine.py living      # living papers; where now / can X close
python3 scripts/da_machine.py leads       # every chair, one lead; glue refused
python3 scripts/da_machine.py ground      # destination + program review
python3 scripts/da_machine.py pipe        # now-bench
python3 scripts/da_machine.py now         # living roster; not a genius census
python3 scripts/da_machine.py feed        # latest LIGO / LHC / PDG / arXiv
python3 scripts/da_machine.py agent       # tick: roster + feed; not a closer
python3 scripts/da_machine.py harmonic    # vocabulary
python3 scripts/da_machine.py sm
python3 scripts/da_machine.py smbreak
python3 scripts/da_machine.py lineage
python3 scripts/da_machine.py cosmos
python3 scripts/da_machine.py classify --claim "…"
```

Longer notes: `docs/DOMAIN-ARCHITECT-MACHINE.md`,
`docs/SHELF.md`, `docs/TRACK-A-LEMMAS.md`,
`docs/TRACK-A-GAP.md`,
`docs/TRACK-B-LEMMAS.md`,
`docs/DA-GROUND.md`, `docs/DA-PIPE.md`,
`docs/DA-NOW.md`, `docs/DA-FEED.md`, `docs/DA-AGENT.md`,
`docs/DA-HARMONIC-VOCAB.md`, `docs/DA-DREAM-TEAM.md`,
`docs/DA-SM-LAGRANGIAN.md`, `docs/DA-SM-LINEAGE.md`,
`docs/DA-COMPUTE.md`, `docs/DA-ALERT.md`,
`docs/DA-PAPER.md`, `docs/DA-THINK-TANK.md`,
`docs/DA-SESSION.md`,
`docs/DA-LIVING.md`,
`docs/DA-LEADS.md`, `docs/TRACK-B-HARDY-TUBE.md`,
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
`docs/TRACK-B-FIELD-GLUE.md`,
`docs/TRACK-B-RESIDUAL.md`.

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
