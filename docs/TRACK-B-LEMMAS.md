# Track B lemmas (DA-scored)

`python3 scripts/da_machine.py trackb`

Classical Navier–Stokes, keep \(1/r^4\). Domain Architect scores each
proposal. **The domain stays open.** A lemma pass is not regularity.

No \(Q_1\). No \(\Phi\) as the estimate variable. No Bridge*. No
A \(\Rightarrow\) B. SFE / HB stay shelved.

The plan these sit in is [`docs/UNAUGMENTED-R4-VORTICITY-PLAN.md`](UNAUGMENTED-R4-VORTICITY-PLAN.md).

---

## How DA treats slot B

| Level | What a pass means |
|---|---|
| One lemma | An identity or cover held, or a bad close was correctly failed |
| Domain B | **Never pass.** Regularity stays open until a closed estimate for \(X=\|\omega\|_2^2\) exists |

`check B` runs the lemma tests. If they break, the domain is **fail**.
If they hold, the domain is **open** (identities held; continuation is
not done).

---

## The scored list

| id | Statement | Verdict | What it is |
|---|---|---|---|
| B1 | \(\int(u_{\le j}\cdot\nabla)u_j\cdot u_j=0\) | **pass** | T2 Lemma 1. Periodic, div-free. Parts. |
| B1b | T2 Lemma 2 (\(H^{2.3}\) ball) as input | **fail** | Circular for large-data a priori. Dropped. |
| B2 | 3-CONC \(\sigma\ge 1/2\) and SPREAD \(\sigma\le 1/2\) cover | **pass** | A cover of mass fractions, not dynamics. \(\rho\le\sigma\). |
| B3 | 3-shell \(\Rightarrow\) Bernstein and \(\|\nabla\xi\|_\infty\le C\,2^{j_*}\) on \(E_c\) | **pass** | Ring upgrade. One extra octave is a constant. |
| B3b | Ring \(\Rightarrow\cos\alpha_3\to 0\) for all data | **fail** | Forbidden Biot–Savart slogan. |
| B4 | Localized Hardy, \(g(0)=0\), plus wall term | **pass** | \(\int h^2/r\,dr\le 4\int(h')^2 r\,dr+2h(\delta)^2\). |
| B4b | Hardy absorbs \(I_{\mathrm{tube}}\) for all data | **fail** | Slow fat swirl, \(R\sim 1/\varepsilon\). |
| B4c | Packet class at \(\delta\sim 2^{-j_*}\) budgets \(I_{\mathrm{tube}}\) | **pass** | Same weight, both sides. \(R\) falls with \(j_*\). |
| B4d | Hardy wall is an off-axis charge | **pass** | Spend \(2h(\delta)^2\) on \(I_{\mathrm{off}}\). |
| B5 | Axisymmetric \((\Delta u)_\theta=\Delta u_\theta-u_\theta/r^2\) | **pass** | Identity. Angular piece lives in the tube. |
| B5b | Angular viscosity dominates \(I_{\mathrm{tube}}\) at \(\delta\sim 2^{-j_*}\) | **fail** | \(R_{\mathrm{ang}}\) sits above 1 and climbs with \(j_*\). |
| B5c | \(R_{\mathrm{ang}}\) climbs with \(j_*\) while \(R_D\) falls | **pass** | Two ratios disagree. |
| B5d | B4b killer kills angular domination | **fail** | Turn \(\varepsilon\) down: \(R_{\mathrm{ang}}\) falls. |
| B5e | therefore cancel to \(\Phi\) | **fail** | B4c already budgets the packet. Keep \(\Gamma\). |
| B5f | angular piece closes \(X\) | **fail** | Failed Poincaré. Packet budget is not continuation (B24). |
| B5g | reading the ratio retunes the PDE | **fail** | Knob on the estimate. |
| B6 | \(\int X\,dt<\infty\Rightarrow X\in L^\infty\) | **fail** | \(X=(T_*-t)^{-1/2}\) is integrable and unbounded. |
| B7 | \(\Pi_j=T+T^*+R+\mathrm{self}\) | **pass** | Bony bookkeeping. |
| B7a | self-flux is T2 Lemma 1 | **pass** | The leftover \(T\) is not self-advection. |
| B7b | \(\|u_{\le j-N}\|_\infty\lesssim 2^{(j-N)/2}X^{1/2}\) | **pass** | Energy class. No \(\rho\) upgrade. |
| B7c | spread \(\Rightarrow\) uniform \(\rho^{1/2}\) as \(\rho\to 0\) | **fail** | Low sum in \(L^\infty\) grows. G is dead. |
| B8 | \(\tau_{\mathrm{C}}+\tau_{\mathrm{S}}=T\) | **pass** | Two-regime clock. |
| B8a | high \(j_*\) hot occupation falls | **pass** | Packet ODE at B4c’s scale. |
| B8b | Leray \(\Rightarrow\) short CONC | **fail** | B6 spike, wearing a regime hat. |
| B8c | occupation closes a bound for \(X\) | **fail** | Clock is not the estimate. B8b + field paths. |
| B9 | \(\Delta X=\Delta_{\mathrm{C}}+\Delta_{\mathrm{S}}\) | **pass** | Two-regime bookkeeping. |
| B9a | high \(j_*\) CONC model sits | **pass** | Packet viscosity owns the cubic. |
| B9b | low \(j_*\) CONC stays bounded | **fail** | \(j_*=2\), \(X_0=2.5\): \(X\) crosses 40. |
| B9c | switching high \(j_*\) sits | **pass** | Clock can flip. |
| B9d | glue sketch is an NS a priori | **fail** | Typed \(j_*=2\) grows; NS packet falls. |
| B10 | packet \(X\le K^2 E\) | **pass** | Frozen support has an energy ceiling. |
| B10a | B9b unbounded path is NS-legal | **fail** | The model forgot \(E\). |
| B10b | ceiling bounds a climbing \(j_*\) | **fail** | \(K\) rises with \(j_*\). |
| B10c | climbing CONC closes \(X\) | **fail** | Broken out as B11. B11e / B13f scored. |
| B10d | energy ceiling retunes the PDE | **fail** | No \(Q_1\), no \(\varepsilon\). Knob on the estimate. |
| B11 | climb increments add | **pass** | Prescribed \(c=\mathrm{d}j_*/\mathrm{d}t\). |
| B11a | bounded \(j_*\) ⇒ bounded \(X\) | **pass** | Necessary condition. |
| B11b | any climb saves the model | **fail** | \(c=1\): \(X\) crosses 40. |
| B11c | fast climb sits | **pass** | \(c=8\): reaches the viscous room. |
| B11d | NS forces a saving \(c\) | **fail** | \(t=0\), short run, blob, B18 paths. None give \(c=8\). |
| B11e | climb sketch is an NS a priori | **fail** | Prescribed \(c=8\) sits on the ODE. NS did not pick it. |
| B12 | \(j_{\mathrm{bar}}\) readable on a packet | **pass** | Peak scale from the field. |
| B12a | \(c\) from the vorticity RHS | **pass** | The apparatus reads. |
| B12b | \(t=0\) packets produce \(c\ge 8\) | **fail** | None do. |
| B12c | viscosity forces an upward climb | **fail** | \(j_{\mathrm{bar}}\) falls. |
| B12d | a short evolution produces a saving climb | **fail** | B13a / B22. No \(c=8\). |
| B12e | \(t=0\) drift is an NS a priori | **fail** | A reading is not a law. The path did not write one. |
| B13 | short IF-RK2 run stays finite | **pass** | Viscous \(X\) falls. |
| B13a | short run produces \(c\ge 8\) | **fail** | Viscous \(c<0\). Euler \(\sim 0\). |
| B13b | resolved high shells fill | **fail** | Mass above \(j_*+1\) stays \(\sim 0\). |
| B13c | short run stays CONC | **pass** | Clock did not sneak into SPREAD. |
| B13d | evolution is a ladder | **fail** | \(j_{\mathrm{bar}}\) falls. |
| B13e | finer / longer saving climb | **fail** | Longer \(n=32\) past room time. No \(c=8\). |
| B13f | packet DNS is an a priori | **fail** | Short missed. Longer missed. A check is not continuation. |
| B14 | \(\xi\cdot S\xi=\sum\lambda_i\cos^2\alpha_i\) on \(E_c\) | **pass** | Strain eigenframe. Not depletion. |
| B14a | 3-CONC \(\Rightarrow\) median \(\lvert\cos\alpha_3\rvert\le 0.25\) | **fail** | Median sits near \(1/2\). |
| B14b | Ring Lipschitz \(\Rightarrow\cos\alpha_3\to 0\) | **fail** | Same slogan as B3b. |
| B14c | small \(\lvert\cos\alpha_3\rvert\) stretches less on \(E_c\) | **pass** | CF as a conditional. Not all-data. |
| B14d | packet geometry closes \(X\) | **fail** | Lipschitz + conditional \(\neq\) continuation (B25). |
| B14e | reading alignment retunes the PDE | **fail** | Knob on the estimate. |
| B15 | \((\omega\cdot S\omega)_+\) on \(E_c\) is a stretching budget | **pass** | Who pays the cubic. |
| B15a | stretch-weighted \(\lvert\cos\alpha_3\rvert\) exceeds the unweighted mean | **pass** | CF as a budget. Field not depleted. |
| B15b | majority of \(+\)stretch from \(\lvert\cos\alpha_3\rvert>0.8\) | **pass** | Directional minority, production majority. |
| B15c | short run depletes median \(\lvert\cos\alpha_3\rvert\le 0.25\) | **fail** | Median stays \(\sim 1/2\). |
| B15d | short run drops aligned share below \(1/2\) | **fail** | \(\mathrm{frac}_{hi}\) stays \(\sim 0.65\). |
| B15e | aligned budget closes \(X\) | **fail** | A share is not continuation (B26). |
| B15f | weighting stretching retunes the PDE | **fail** | Knob on the estimate. |
| B16 | \(\dot X=2\int\omega\cdot S\omega-2\nu\|\nabla\omega\|_2^2\) | **pass** | Fluids identity. |
| B16a | viscosity owns the net on B13-scale packets | **pass** | \(\lvert P\rvert\ll D\), \(\dot X<0\). |
| B16b | aligned \(P_+\) is a large net cubic | **fail** | Plus/minus cancel \(\sim 10^{-3}\). |
| B16c | \(L^2\) packet is BKM | **fail** | \(\|\omega\|_\infty/\|\omega\|_2\sim 0.2\). |
| B16d | random-phase \(\Rightarrow\) all CONC | **fail** | Ensemble, not a class. |
| B16e | balance closes \(X\) | **fail** | A decaying packet is not continuation (B27). |
| B16f | reading the balance retunes the PDE | **fail** | Knob on the estimate. |
| B17 | blob + signed strain is readable CONC | **pass** | Two-scale. Not a Stokes eigenfunction. |
| B17a | net \(P\approx(\omega\cdot S\omega)_+\) | **pass** | Cancel \(\approx 0.83\) on a still-CONC blob. |
| B17b | cubic owns \(\dot X\) at the working box | **fail** | \(P/D\approx 0.008\). Visc still owns the net. |
| B17c | \(z\)-independent tube also nets | **fail** | \(\int\cos z\,dz=0\). Swirl \(\neq\) cubic. |
| B17d | \(L^2\) blob is BKM | **fail** | \(\|\omega\|_\infty/\|\omega\|_2\sim 2.4\). Still not \(\int\|\omega\|_\infty\). |
| B17e | signed-strain blob closes \(X\) | **fail** | One-sided leftover \(\neq\) continuation (B28). |
| B17f | reading the blob retunes the PDE | **fail** | Knob on the check. |
| B18 | clock identity on a path | **pass** | B8, read on IF-RK2. |
| B18a | packet and blob occupy CONC fully | **pass** | \(\tau_{\mathrm{C}}=T\). Zero switches. |
| B18b | the clock left CONC and saved \(X\) | **fail** | Viscosity. No flip. |
| B18c | CONC occupation is short on these runs | **fail** | \(\tau_{\mathrm{C}}=T\). |
| B18d | cubic-live time is nonempty | **fail** | Zero samples with \(\lvert P\rvert/D\ge 0.05\). |
| B18e | field occupation closes \(X\) | **fail** | Occupation of CONC \(\neq\) continuation (B29). |
| B18f | reading the path retunes the PDE | **fail** | Knob on the check. |
| B19 | both \(\dot X\) readable | **pass** | Sketch versus NS, same box. |
| B19a | \(j_*=2\) model sign matches NS | **fail** | Model \(+2.25\); NS \(\approx-22.5\). |
| B19b | NS packet is the B9b blowup | **fail** | Model grows; NS falls. |
| B19c | \(\alpha_c\) is the field cubic | **fail** | Implied \(\alpha\sim 0\) vs \(0.4\). |
| B19d | \(\nu 2^{2j_*}X\) is NS visc | **fail** | \(2D/(\gamma X)\approx 5.6\). |
| B19e | matching the sketch closes \(X\) | **fail** | Wrong-sign sketch \(\neq\) continuation (B30). |
| B19f | reading the rates retunes the PDE | **fail** | Knob on the check. |
| B20 | \(c\) readable on blob and paths | **pass** | RHS and \(\Delta j_{\mathrm{bar}}/T\). |
| B20a | blob \(t=0\) produces \(c\ge 8\) | **fail** | Visc \(c\approx-2\). Euler \(\approx 0\). |
| B20b | B18-path mean \(c\ge 8\) | **fail** | Visc means negative. Euler \(\sim 0\). |
| B20c | visc on the blob is a ladder | **fail** | \(j_{\mathrm{bar}}\) falls. |
| B20d | \(j_{\mathrm{bar}}>\text{typed }j_*\) is a climb | **fail** | Static offset, then a fall. |
| B20e | field climb closes \(X\) | **fail** | Missing \(c=8\) \(\neq\) continuation (B31). |
| B20f | reading \(c\) retunes the PDE | **fail** | Knob on the check. |
| B21 | ODE and NS readable on the window | **pass** | Same \(T=0.064\). Long ODE still sits. |
| B21a | \(c=8\) reached the viscous room here | **fail** | \(j\colon 2\to 2.51\). Room is \(j=5\). |
| B21b | B11c sitting path is the NS packet | **fail** | Model grows; NS falls. |
| B21c | NS \(\Delta j_{\mathrm{bar}}=cT\) | **fail** | Prescribed \(+0.512\); field \(\approx-0.015\). |
| B21d | the sketch already sits on this window | **fail** | Model \(X\) still grows. |
| B21e | matching the sketch closes \(X\) | **fail** | Short window \(\neq\) sitting (B32). |
| B21f | reading the sketch retunes the PDE | **fail** | Knob on the check. |
| B22 | longer paths readable past room time | **pass** | \(T=0.384>0.375\). Still \(n=32\). |
| B22a | longer run produces \(c\ge 8\) | **fail** | Visc means negative. Euler \(\sim 0\). |
| B22b | longer visc is a ladder | **fail** | \(j_{\mathrm{bar}}\) still falls. |
| B22c | longer fills high shells | **fail** | Mass above \(j_*+1\) stays \(\sim 0\). |
| B22d | the clock left CONC and saved \(X\) | **fail** | Viscosity. No flip. |
| B22e | finer (\(n>32\)) produces a saving climb | **fail** | A bigger FFT is not continuation (B33). |
| B22f | lengthening \(T\) retunes the PDE | **fail** | Knob on the check. |
| B23 | short and longer DNS readable | **pass** | \(T=0.384>0.375\). Still \(n=32\). |
| B23a | decaying packet DNS is an a priori | **fail** | One IC, finite \(T\), finite \(n\). |
| B23b | room-time length is continuation | **fail** | An estimate, not a longer interval. |
| B23c | the packet class is all data | **fail** | B9b and SPREAD are not this run. |
| B23d | no blow on \(n=32\) \(\Rightarrow X\in L^\infty\) | **fail** | DNS-never-blew-up is refused. |
| B23e | finer makes DNS an a priori | **fail** | Same knob as B22e. Scored as B34. |
| B23f | scoring this retunes the PDE | **fail** | Knob on the check. |
| B24 | B4c and B5b readable together | **pass** | \(R_D\) falls. \(R_{\mathrm{ang}}\) climbs. |
| B24a | angular \(1/r^2\) closes \(X\) | **fail** | Same slogan as B5f. |
| B24b | B4c packet budget is an a priori | **fail** | A class budget is not all data. |
| B24c | \(R_D\ll 1\Rightarrow X\in L^\infty\) | **fail** | A ratio is not Beale. |
| B24d | revive Hardy or cancel to \(\Phi\) | **fail** | B4b / B5e already missed. |
| B24e | packet geometry closes \(X\) | **fail** | Scored as B14d / B25. |
| B24f | scoring this retunes the PDE | **fail** | Knob on the estimate. |
| B25 | identity, undepleted CONC, CF readable | **pass** | Median \(\sim 1/2\). Conditional holds. |
| B25a | 3-CONC depletion closes \(X\) | **fail** | Spectrum, not alignment. |
| B25b | Lipschitz + CF is an a priori | **fail** | An if is not continuation. |
| B25c | median \(\sim 1/2\) is a geometric class | **fail** | Random on the sphere. |
| B25d | CF conditional is BKM | **fail** | A subset ratio is not \(\int\|\omega\|_\infty\). |
| B25e | aligned budget closes \(X\) | **fail** | Scored as B15e / B26. |
| B25f | scoring this retunes the PDE | **fail** | Knob on the estimate. |
| B26 | budget, CF weight, majority readable | **pass** | Same caches as B15. No new FFT. |
| B26a | aligned \(P_+\) share closes \(X\) | **fail** | A payer count is not continuation. |
| B26b | time emptying the cap is continuation | **fail** | B15c / B15d already missed. |
| B26c | \(65\%\) share is a geometric class | **fail** | Packets, not all data. |
| B26d | aligned budget is \(\int\|\omega\|_\infty\) | **fail** | A subset share is not the max. |
| B26e | enstrophy balance closes \(X\) | **fail** | Scored as B16e / B27. |
| B26f | scoring this retunes the PDE | **fail** | Knob on the estimate. |
| B27 | identity, visc-owned net, cancelled \(P_+\) readable | **pass** | Same caches as B16. No new FFT. |
| B27a | visc owning this ensemble closes \(X\) | **fail** | A reading is not continuation. |
| B27b | cancellation is all-data | **fail** | B16d already missed. |
| B27c | decaying \(L^2\) packet is continuation | **fail** | Same slogan as B23. |
| B27d | identity is \(\int\|\omega\|_\infty\) | **fail** | \(L^2\) is not the max. |
| B27e | signed-strain blob closes \(X\) | **fail** | Scored as B17e / B28. |
| B27f | scoring this retunes the PDE | **fail** | Knob on the estimate. |
| B28 | blob, one-sided net, visc-owned cubic readable | **pass** | Same caches as B17. No new FFT. |
| B28a | one-sided leftover closes \(X\) | **fail** | \(P/D\approx 0.008\). |
| B28b | sitting in one sign is a class | **fail** | Localization is a knob. |
| B28c | peaked \(L^2\) is \(\int\|\omega\|_\infty\) | **fail** | Ratio \(\sim 2.4\) is not the max. |
| B28d | turning \(\nu\) down is continuation | **fail** | Knob on the check. |
| B28e | field occupation closes \(X\) | **fail** | Scored as B18e / B29. |
| B28f | scoring this retunes the PDE | **fail** | Knob on the estimate. |
| B29 | clock, full CONC, visc-owned \(X\) readable | **pass** | Same caches as B18. No new FFT. |
| B29a | occupying CONC the whole interval closes \(X\) | **fail** | Viscosity. The clock did not leave. |
| B29b | \(\tau_{\mathrm{C}}=T\) is a short visit | **fail** | B18c already missed. |
| B29c | CONC occupation is a live cubic | **fail** | Zero live samples. |
| B29d | \(\tau_{\mathrm{C}}=T\) is \(\int\|\omega\|_\infty\) | **fail** | A clock column is not the max. |
| B29e | matching the sketch closes \(X\) | **fail** | Scored as B19e / B30. |
| B29f | scoring this retunes the PDE | **fail** | Knob on the estimate. |
| B30 | rates, sign mismatch, model-grows / field-falls readable | **pass** | Same caches as B19. No new FFT. |
| B30a | matching the sketch closes \(X\) | **fail** | Model \(+2.25\); NS \(\approx-22.5\). |
| B30b | shrinking \(\alpha_c\) is continuation | **fail** | Knob on the estimate. |
| B30c | wrong-sign ODE is an NS a priori | **fail** | B9b is typed, not this field. |
| B30d | matching \(\dot X\) is \(\int\|\omega\|_\infty\) | **fail** | A sign is not the max. |
| B30e | a field climb law closes \(X\) | **fail** | Scored as B20e / B31. |
| B30f | scoring this retunes the PDE | **fail** | Knob on the estimate. |
| B31 | field \(c\), blob miss, path-mean miss readable | **pass** | Same caches as B20. No new FFT. |
| B31a | a field climb closes \(X\) | **fail** | The field did not hand us \(c=8\). |
| B31b | \(j_{\mathrm{bar}}\) offset is continuation | **fail** | Static offset, then a fall. |
| B31c | visc fall is a class | **fail** | A reading is not a type. |
| B31d | reading \(c\) is \(\int\|\omega\|_\infty\) | **fail** | A rate is not the max. |
| B31e | matching the prescribed-\(c\) sketch closes \(X\) | **fail** | Scored as B21e / B32. |
| B31f | scoring this retunes the PDE | **fail** | Knob on the estimate. |
| B32 | window rates, missed room, sketch-grows / field-falls readable | **pass** | Same caches as B21. No new FFT. |
| B32a | matching the sketch closes \(X\) | **fail** | Sketch grew; field fell. |
| B32b | cashing B11c on \(T=0.064\) is continuation | **fail** | Sitting is a long ODE. |
| B32c | growing sketch is an NS a priori | **fail** | Prescribed \(\Delta j\neq\) field. |
| B32d | matching the window is \(\int\|\omega\|_\infty\) | **fail** | A sign is not the max. |
| B32e | a finer box closes \(X\) | **fail** | Scored as B22e / B33. |
| B32f | scoring this retunes the PDE | **fail** | Knob on the estimate. |
| B33 | longer miss, empty high shells, short window readable | **pass** | Same caches as B22 / B32. No \(n=64\). |
| B33a | a finer box closes \(X\) | **fail** | A mesh is not an estimate. |
| B33b | cashing \(n=64\) is continuation | **fail** | Continuation is an estimate, not a finer mesh. |
| B33c | an unrun \(n=64\) is an NS a priori | **fail** | A box you did not run is not the packet. |
| B33d | a finer box is \(\int\|\omega\|_\infty\) | **fail** | A mesh is not the max. |
| B33e | finer makes DNS an a priori | **fail** | Scored as B23e / B34. |
| B33f | scoring this retunes the PDE | **fail** | Knob on the box. |
| B34 | DNS miss, refused no-blow, finer-box miss readable | **pass** | Same caches as B23 / B33. No \(n=64\). |
| B34a | finer DNS closes \(X\) | **fail** | Same slogan as B23a at a finer \(n\). |
| B34b | cashing \(n=64\) DNS is continuation | **fail** | A finer grid is not an estimate. |
| B34c | an unrun finer DNS is an NS a priori | **fail** | A box you did not run is not the packet. |
| B34d | finer DNS is \(\int\|\omega\|_\infty\) | **fail** | A mesh is not the max. |
| B34e | a leftover close writes regularity | **fail** | Scored as B35. A leftover close is not \(X\). |
| B34f | scoring this retunes the PDE | **fail** | Knob on the box. |
| B35 | leftover catalog, finer miss, DNS miss readable | **pass** | Same caches as B33 / B34. No \(n=64\). |
| B35a | a leftover close writes \(X\) | **fail** | A catalog of fails is not continuation. |
| B35b | scoring leftovers is continuation | **fail** | An estimate, not a list. |
| B35c | a stack of fails is an NS a priori | **fail** | Failing a knob is not the packet. |
| B35d | leftover closes are \(\int\|\omega\|_\infty\) | **fail** | A leftover close is not the max. |
| B35e | classical regularity is decided by leftover closes | **open** | The leftover is the object. |
| B35f | scoring this retunes the PDE | **fail** | Knob on the check. |
| Φ | Switch the estimate to \(\Phi=\Gamma/r^2\) | **fail** | Moves the work onto \(\|\Phi\|_\infty\). Keep \(\Gamma\). |
| regularity | Classical 3D NS is globally regular | **open** | No closed estimate for \(X\). |

---

## What was actually proved or checked

**B1.** For periodic divergence-free \(u\), the low self-flux into a
dyadic block vanishes:

\[
\int_{\mathbb{T}^3}(u_{\le j}\cdot\nabla)u_j\cdot u_j
=\frac12\int u_{\le j}\cdot\nabla(|u_j|^2)
=-\frac12\int(\nabla\cdot u_{\le j})\,|u_j|^2
=0.
\]

The script repeats this on a random Leray field. Residual is at
roundoff. This is T2 Lemma 1 only.

**B2.** \(\sigma=P_{j_*}/X\) is a number in \((0,1]\). The split
\(\sigma\ge 1/2\) vs \(\sigma\le 1/2\) covers the interval. August
CONC and June SPREAD stay two names. The checker does not claim the
solution lives in either regime.

**B3.** On a field whose Fourier support sits in three consecutive
octaves around \(2^{j_*}\), Bernstein gives

\[
\|\nabla\omega\|_\infty\lesssim 2^{2(j_*+1)}\|\omega\|_2,
\]

and on \(E_c=\{|\omega|\ge c\|\omega\|_{\mathrm{rms}}\}\)

\[
\|\nabla\xi\|_\infty\le C(c)\,2^{j_*}.
\]

The script measures the constants on \(\mathbb{T}^3\). That is Ring,
not depletion of \(\sum\lambda_i\cos^2\alpha_i\).

**B4.** Classical Hardy: \(g(0)=0\) implies
\(\int_0^\delta(g/r)^2\,dr\le 4\int(g')^2\,dr\).

Tube form with wall: \(h(0)=0\) and completion of the square

\[
0\le\int_0^\delta\bigl|r h'+\tfrac12 h\bigr|^2\frac{dr}{r}
\]

gives

\[
\int_0^\delta\frac{h^2}{r}\,dr
\le 4\int_0^\delta(h')^2 r\,dr+2h(\delta)^2.
\]

If \(h=\Gamma/r\), the wall term is the off-axis match. This is the
localized Hardy the plan asked for.

**B4b / B4c / B4d.** The Hardy \(\to I_{\mathrm{tube}}\) write
lives in [`TRACK-B-HARDY-TUBE.md`](TRACK-B-HARDY-TUBE.md).
All-data absorption **fails** (slow fat swirl, \(R\sim 1/\varepsilon\)).
Packet class at \(\delta\sim 2^{-j_*}\) **passes**. The wall is a
finite off-axis charge.

**B5.** In cylindrical components, axisymmetric,

\[
(\Delta u)_\theta=\Delta u_\theta-\frac{u_\theta}{r^2}.
\]

The extra \(1/r^2\) sits in the same tube as \(1/r^4\partial_z(\Gamma^2)\).
The identity **passes**. Domination by that piece alone **fails**.
Write: [`TRACK-B-ANGULAR.md`](TRACK-B-ANGULAR.md).
\(R_{\mathrm{ang}}\) sits above 1 and climbs with \(j_*\).
Full \(D_{\mathrm{tube}}\) still budgets the packet (B4c).
Do not cancel to \(\Phi\).

**B6.** Leray’s \(\int X\,dt<\infty\) does not stop
\(\dot X\sim X^3\). A spike \(X\sim(T_*-t)^{-1/2}\) is compatible
with integrable enstrophy and is unbounded. DA fails that close.

**B7 / B7a / B7b / B7c.** The low Bony \(T\) write lives in
[`TRACK-B-BONY-T.md`](TRACK-B-BONY-T.md). Split and T2 self
**pass**. Energy-class \(L^\infty\) **pass**. Uniform
\(\rho^{1/2}\) as \(\rho\to 0\) **fails**. Theorem G is dead.
H at frozen \(\rho\le 1/4\) may still use B7b.

**B8 / B8a / B8b / B8c.** Occupation time lives in
[`TRACK-B-OCCUPATION.md`](TRACK-B-OCCUPATION.md). Clock
**pass**. High \(j_*\) short **pass**. Leray \(\Rightarrow\)
short CONC **fail**. Occupation closes \(X\) **fail**.

**B9 / B9a / B9b / B9c / B9d.** The two-regime glue lives in
[`TRACK-B-GLUE.md`](TRACK-B-GLUE.md). Increments add
**pass**. High \(j_*\) CONC sits **pass**. Switching high
\(j_*\) sits **pass**. Low \(j_*\) CONC **fails** on the model
ODE. Sketch \(\neq\) NS a priori **fail**.

**B10 / B10a / B10b / B10c / B10d.** Energy ceiling lives in
[`TRACK-B-LOW-J.md`](TRACK-B-LOW-J.md). Packet \(X\le K^2E\)
**pass**. B9b unbounded path is not NS **fail**. Ceiling
does not follow a climbing \(j_*\) **fail**. Climbing CONC
as a close **fail**. Not a PDE retune **fail**.

**B11 / B11a / B11b / B11c / B11d / B11e.** Climbing CONC
lives in [`TRACK-B-CLIMB.md`](TRACK-B-CLIMB.md). Increments
add **pass**. Bounded \(j_*\) bounds \(X\) **pass**. Slow
climb **fails** to save. Fast climb sits **pass**. NS climb
law **fail**. Sketch \(\neq\) NS a priori **fail**.

**B12 / B12a / B12b / B12c / B12d / B12e.** The field climb
lives in [`TRACK-B-CLIMB-LAW.md`](TRACK-B-CLIMB-LAW.md).
Barycenter **pass**. \(c\) from the RHS **pass**. \(t=0\)
saving climb **fail**. Viscosity as a ladder **fail**.
Evolved cascade **fail**. \(t=0\) as a priori **fail**.

**B13 / B13a / B13b / B13c / B13d / B13e / B13f.** Short
evolution lives in [`TRACK-B-EVOLVE.md`](TRACK-B-EVOLVE.md).
Run finite **pass**. Saving climb **fail**. High fill
**fail**. Stays CONC **pass**. Evolution as a ladder
**fail**. Longer saving climb **fail**. DNS as an a priori **fail**.

**B14 / B14a / B14b / B14c / B14d / B14e.** Packet geometry
lives in [`TRACK-B-GEOMETRY.md`](TRACK-B-GEOMETRY.md).
Strain identity **pass**. CONC \(\Rightarrow\) depleted
\(\cos\alpha_3\) **fail**. Ring \(\Rightarrow\) alignment
**fail**. CF conditional **pass**. Geometry closes \(X\)
**fail**. Not a PDE retune **fail**.

**B15 / B15a / B15b / B15c / B15d / B15e / B15f.** Stretching
budget lives in [`TRACK-B-STRETCH.md`](TRACK-B-STRETCH.md).
Budget readable **pass**. CF weights the budget **pass**.
Majority from aligned cap **pass**. Short run depletes
median \(\lvert\cos\alpha_3\rvert\) **fail**. Short run
empties the aligned share **fail**. Budget closes \(X\)
**fail**. Not a PDE retune **fail**.

**B16 / B16a / B16b / B16c / B16d / B16e / B16f.** Enstrophy
balance lives in [`TRACK-B-BALANCE.md`](TRACK-B-BALANCE.md).
Identity **pass**. Viscosity owns the net on this ensemble
**pass**. Aligned \(P_+\) as a net cubic **fail**. \(L^2\)
is BKM **fail**. Random-phase \(\Rightarrow\) all CONC
**fail**. Balance closes \(X\) **fail**. Not a PDE retune
**fail**.

**B17 / B17a / B17b / B17c / B17d / B17e / B17f.** Coherent
CONC lives in [`TRACK-B-COHERENT.md`](TRACK-B-COHERENT.md).
Signed-strain blob readable **pass**. Net \(\approx P_+\)
**pass**. Working-box cubic live **fail**. \(z\)-independent
tube also nets **fail**. \(L^2\) blob is BKM **fail**.
Blob closes \(X\) **fail**. Not a PDE retune **fail**.

**B18 / B18a / B18b / B18c / B18d / B18e / B18f.** Field
occupation lives in [`TRACK-B-FIELD-OCC.md`](TRACK-B-FIELD-OCC.md).
Clock on a path **pass**. Paths stay CONC **pass**. Clock
saved \(X\) **fail**. CONC occupation short **fail**.
Cubic-live time **fail**. Field occupation closes \(X\)
**fail**. Not a PDE retune **fail**.

**B19 / B19a / B19b / B19c / B19d / B19e / B19f.** Field
glue lives in [`TRACK-B-FIELD-GLUE.md`](TRACK-B-FIELD-GLUE.md).
Both \(\dot X\) readable **pass**. Sign match **fail**.
NS packet is B9b **fail**. \(\alpha_c\) is the cubic **fail**.
\(\gamma\) is NS visc **fail**. Matching the sketch closes
\(X\) **fail**. Not a PDE retune **fail**.

**B20 / B20a / B20b / B20c / B20d / B20e / B20f.** NS climb
law lives in [`TRACK-B-NS-CLIMB.md`](TRACK-B-NS-CLIMB.md).
\(c\) readable **pass**. Blob \(t=0\) saving climb **fail**.
B18-path mean **fail**. Visc as a ladder **fail**.
\(j_{\mathrm{bar}}\) offset as a climb **fail**. Field climb
closes \(X\) **fail**. Not a PDE retune **fail**.

**B21 / B21a / B21b / B21c / B21d / B21e / B21f.** Climb
sketch lives in [`TRACK-B-CLIMB-SKETCH.md`](TRACK-B-CLIMB-SKETCH.md).
Window rates **pass**. Viscous room on this window **fail**.
Sitting path is NS **fail**. \(\Delta j=cT\) **fail**. Sketch
sits on this window **fail**. Matching the sketch closes
\(X\) **fail**. Not a PDE retune **fail**.

**B22 / B22a / B22b / B22c / B22d / B22e / B22f.** Longer
path lives in [`TRACK-B-LONGER.md`](TRACK-B-LONGER.md).
Readable past room time **pass**. Longer \(c\ge 8\) **fail**.
Ladder **fail**. High fill **fail**. Clock saved \(X\)
**fail**. Finer box **fail**. Not a PDE retune **fail**.

**B23 / B23a / B23b / B23c / B23d / B23e / B23f.** DNS as
an a priori lives in [`TRACK-B-DNS.md`](TRACK-B-DNS.md).
Readable **pass**. Decaying packet DNS is an a priori
**fail**. Room-time length is continuation **fail**.
Packet class is all data **fail**. No-blow \(\Rightarrow L^\infty\)
**fail**. Finer box **fail**. Not a PDE retune **fail**.

**B24 / B24a / B24b / B24c / B24d / B24e / B24f.** Tube
budget as an a priori lives in
[`TRACK-B-TUBE.md`](TRACK-B-TUBE.md). Readable **pass**.
Angular closes \(X\) **fail**. B4c is an a priori **fail**.
\(R_D\ll 1\Rightarrow L^\infty\) **fail**. Revive Hardy / \(\Phi\)
**fail**. Geometry leftover **fail**. Not a PDE retune **fail**.

**B25 / B25a / B25b / B25c / B25d / B25e / B25f.** Alignment
as an a priori lives in [`TRACK-B-ALIGN.md`](TRACK-B-ALIGN.md).
Readable **pass**. Depletion closes \(X\) **fail**.
Lipschitz + CF is an a priori **fail**. Median is a class
**fail**. CF is BKM **fail**. Budget leftover **fail**.
Not a PDE retune **fail**.

**B26 / B26a / B26b / B26c / B26d / B26e / B26f.** Stretching
budget as an a priori lives in
[`TRACK-B-PAYERS.md`](TRACK-B-PAYERS.md). Readable **pass**.
Aligned share closes \(X\) **fail**. Time emptying is
continuation **fail**. Share is a class **fail**. Aligned
budget is \(\int\|\omega\|_\infty\) **fail**. Enstrophy
leftover **fail**. Not a PDE retune **fail**.

**B27 / B27a / B27b / B27c / B27d / B27e / B27f.** Enstrophy
balance as an a priori lives in
[`TRACK-B-NET.md`](TRACK-B-NET.md). Readable **pass**.
Visc ensemble closes \(X\) **fail**. Cancellation is
all-data **fail**. Decaying packet is continuation
**fail**. Identity is \(\int\|\omega\|_\infty\) **fail**.
Coherent leftover **fail**. Not a PDE retune **fail**.

**B28 / B28a / B28b / B28c / B28d / B28e / B28f.** Signed-strain
blob as an a priori lives in
[`TRACK-B-BLOB.md`](TRACK-B-BLOB.md). Readable **pass**.
One-sided leftover closes \(X\) **fail**. Sitting in one
sign is a class **fail**. Peaked \(L^2\) is
\(\int\|\omega\|_\infty\) **fail**. Turning \(\nu\) down is
continuation **fail**. Occupation leftover **fail**.
Not a PDE retune **fail**.

**B29 / B29a / B29b / B29c / B29d / B29e / B29f.** Field
occupation as an a priori lives in
[`TRACK-B-CLOCK.md`](TRACK-B-CLOCK.md). Readable **pass**.
Staying CONC closes \(X\) **fail**. \(\tau_{\mathrm{C}}=T\)
is a short visit **fail**. CONC occupation is a live
cubic **fail**. Clock is \(\int\|\omega\|_\infty\) **fail**.
Glue leftover **fail**. Not a PDE retune **fail**.

**B30 / B30a / B30b / B30c / B30d / B30e / B30f.** Field
glue as an a priori lives in
[`TRACK-B-MATCH.md`](TRACK-B-MATCH.md). Readable **pass**.
Matching the sketch closes \(X\) **fail**. Shrinking
\(\alpha_c\) is continuation **fail**. Wrong-sign ODE is
NS **fail**. Match is \(\int\|\omega\|_\infty\) **fail**.
Climb leftover **fail**. Not a PDE retune **fail**.

**B31 / B31a / B31b / B31c / B31d / B31e / B31f.** NS
climb as an a priori lives in
[`TRACK-B-SAVING.md`](TRACK-B-SAVING.md). Readable **pass**.
Field climb closes \(X\) **fail**. Offset is continuation
**fail**. Visc fall is a class **fail**. Reading \(c\) is
\(\int\|\omega\|_\infty\) **fail**. Sketch leftover **fail**.
Not a PDE retune **fail**.

**B32 / B32a / B32b / B32c / B32d / B32e / B32f.** Climb
sketch as an a priori lives in
[`TRACK-B-WINDOW.md`](TRACK-B-WINDOW.md). Readable **pass**.
Matching the sketch closes \(X\) **fail**. Cashing B11c
on \(T=0.064\) is continuation **fail**. Growing sketch
is NS **fail**. Window is \(\int\|\omega\|_\infty\) **fail**.
Finer leftover **fail**. Not a PDE retune **fail**.

**B33 / B33a / B33b / B33c / B33d / B33e / B33f.** Finer
box as an a priori lives in
[`TRACK-B-FINER.md`](TRACK-B-FINER.md). Readable **pass**.
A finer box closes \(X\) **fail**. Cashing \(n=64\) is
continuation **fail**. Unrun \(n=64\) is NS **fail**.
Finer is \(\int\|\omega\|_\infty\) **fail**. DNS leftover
**fail**. Not a PDE retune **fail**.

**B34 / B34a / B34b / B34c / B34d / B34e / B34f.** Finer
DNS as an a priori lives in
[`TRACK-B-MESH.md`](TRACK-B-MESH.md). Readable **pass**.
Finer DNS closes \(X\) **fail**. Cashing \(n=64\) DNS is
continuation **fail**. Unrun finer DNS is NS **fail**.
Finer DNS is \(\int\|\omega\|_\infty\) **fail**. Regularity
leftover **fail**. Not a PDE retune **fail**.

**B35 / B35a / B35b / B35c / B35d / B35e / B35f.** Leftover
close as an a priori lives in
[`TRACK-B-CLOSE.md`](TRACK-B-CLOSE.md). Readable **pass**.
A leftover close writes \(X\) **fail**. Scoring leftovers
is continuation **fail**. Stack of fails is NS **fail**.
Leftover closes are \(\int\|\omega\|_\infty\) **fail**.
Regularity leftover **open**. Not a PDE retune **fail**.

---

## What is still the next write

1. Stretching budget is not an a priori (B15e).
   Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). Leftover close is not an a priori (B34e). Regularity stays open. Finer (\(n>32\))
   stays a box knob (B22e). Do not spawn \(n=64\). B4c
   stands. Angular \(1/r^2\) does not. Do not cancel to
   \(\Phi\). Do not write \(c=8\) into the PDE.
2. Do not revive all-data Hardy absorption, G’s \(\rho\to 0\),
   Leray-as-occupation, the glue sketch as an NS a priori,
   a typed \(c=8\), all-data Biot–Savart depletion, BKM-from-\(L^2\),
   a \(\Phi\) cancel, substituting \(j_{\mathrm{bar}}\) for typed
   \(j_*\), or a retune of the PDE.

None of those is a pass on regularity. Checker:

```
python3 scripts/track_b_hardy_tube.py
python3 scripts/track_b_angular.py
python3 scripts/track_b_bony_t.py
python3 scripts/track_b_occupation.py
python3 scripts/track_b_glue.py
python3 scripts/track_b_low_j.py
python3 scripts/track_b_climb.py
python3 scripts/track_b_climb_law.py
python3 scripts/track_b_evolve.py
python3 scripts/track_b_geometry.py
python3 scripts/track_b_stretch.py
python3 scripts/track_b_balance.py
python3 scripts/track_b_coherent.py
python3 scripts/track_b_field_occ.py
python3 scripts/track_b_field_glue.py
python3 scripts/track_b_ns_climb.py
python3 scripts/track_b_climb_sketch.py
python3 scripts/track_b_longer.py
python3 scripts/track_b_dns.py
python3 scripts/track_b_tube.py
python3 scripts/track_b_align.py
python3 scripts/track_b_payers.py
python3 scripts/track_b_net.py
python3 scripts/track_b_blob.py
python3 scripts/track_b_clock.py
python3 scripts/track_b_match.py
python3 scripts/track_b_saving.py
python3 scripts/track_b_window.py
python3 scripts/track_b_finer.py
python3 scripts/track_b_mesh.py
python3 scripts/track_b_close.py
python3 scripts/track_b_lemmas.py
python3 -m unittest tests.test_track_b_lemmas tests.test_track_b_glue tests.test_track_b_low_j tests.test_track_b_climb tests.test_track_b_climb_law tests.test_track_b_evolve tests.test_track_b_geometry tests.test_track_b_stretch tests.test_track_b_balance tests.test_track_b_angular tests.test_track_b_coherent tests.test_track_b_occupation tests.test_track_b_field_occ tests.test_track_b_field_glue tests.test_track_b_ns_climb tests.test_track_b_climb_sketch tests.test_track_b_longer tests.test_track_b_dns tests.test_track_b_tube tests.test_track_b_align tests.test_track_b_payers tests.test_track_b_net tests.test_track_b_blob tests.test_track_b_clock tests.test_track_b_match tests.test_track_b_saving tests.test_track_b_window tests.test_track_b_finer tests.test_track_b_mesh tests.test_track_b_close
python3 scripts/da_machine.py trackb
python3 scripts/da_machine.py check --domain B
```
