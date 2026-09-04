# Coherent CONC

`python3 scripts/track_b_coherent.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
Random-phase packets cancelled (B16d). This write
hands the cubic a named field.

---

## The knob on this write

For periodic incompressible \(u\),

\[
\int\omega\cdot S\omega=-\int u\cdot(\omega\times\Delta u).
\]

Any Stokes eigenfunction (\(\Delta u=-\lambda u\)),
including Beltrami / ABC and a single spherical shell,
has net production zero. A \(z\)-independent vortex tube
in a periodic axial strain also nets zero:
\(S_{zz}\propto\cos z\) and \(\int\cos z\,dz=0\).

Sit a Gaussian blob at \((\pi,\pi,0)\), where the same
strain

\[
u_{\mathrm{s}}=(\sin x\cos z,\,0,\,-\cos x\sin z)
\]

has \(S_{zz}=+1\). Weak strain (\(\mathrm{amp}_s=0.02\))
so the barycenter stays CONC. Scale the whole field to
the B13 box: \(n=32\), \(X=2.5\), \(\nu=0.1\).

Tesla: a Stokes eigenfunction is not a cubic. Localization
in \(z\) is a knob on the check. One-sided is a number.
Large versus \(D\) is a different number.

No \(Q_1\). No \(\varepsilon\). No BKM-from-\(L^2\).

---

## What the apparatus does

**B17, pass.** The blob is readable. Tiny IF-RK2 matches
\(\dot X=2P-2D\) at relative residual \(\sim 2\cdot 10^{-4}\).
\(\sigma\approx 0.85\), \(j_{\mathrm{bar}}\approx 2.57\),
\(j_*=3\). Still 3-CONC. Not one Stokes eigenvalue.

**B17a, pass.** Cancellation
\(\lvert P\rvert/(P_++P_-)\approx 0.83\). Net sits on the
plus pile. Random-phase packets sat at \(\sim 10^{-3}\).
B16d said a coherent field could do this. This one does.

**B17b, fail** of “the one-sided cubic owns \(\dot X\) at
the working box.” \(P/D\approx 0.008\), \(\dot X<0\).
Coherence killed cancellation. It did not make \(P\) large
versus dissipation. Viscosity still owns the net. Same
box as B13 / B16a.

**B17c, fail** of “a \(z\)-independent swirl in the same
strain also nets.” That tube has cancel \(\approx 0\).
Coherence of swirl is not the cubic. The blob had to sit
where \(S_{zz}\) keeps a sign. Do not promote “vortex”
to a class.

**B17d, fail** of “an \(L^2\) bound on this blob is BKM.”
\(\|\omega\|_\infty/\|\omega\|_2\sim 2.4\) (more peaked
than a fat packet’s \(0.2\)). The criterion still asks
for \(\int\|\omega\|_\infty\).

**B17e, fail** of “a signed-strain blob closes
\(X\).” Scored as B28. One-sided cubic at this
box is still a leftover versus \(D\). A leftover
that no longer cancels is not continuation.

**B17f, fail** of “this retunes the PDE.” Localization in
\(z\) is a knob. Turning \(\nu\) down until \(\dot X>0\)
is the same knob. The equation is untouched.

---

## They work it

**Leray.** You used my dissipation again. On this blob it
still owns the net at the working box. Jean, a signed
strain is not my theorem extended.

**Majda.** Random phase was not a vortex. A vortex tube
that sees oscillating stretch is not a vortex blob that
sits in one sign. Do not sit “coherent” as a class
either.

**Beale.** The ratio climbed from \(0.2\) to \(2.4\).
Nobody here turns \(\|\omega\|_2\) into our criterion.

**Ladyzhenskaya.** I still will not give you \(\varepsilon\).
Turn \(\nu\) down and the cubic can win. That is a knob
on the check.

**Tesla.** Two knobs after B16. Cancellation, then size
versus \(D\). First moved (\(10^{-3}\to 0.83\)). Second
sat (\(\sim 0.8\%\)). You can miss the second if you stop
at “we found a field.”

**Feynman.** Missable: \(\lvert P\rvert/(P_++P_-)\),
\(\lvert P\rvert/D\), and the tube control. All readable.
The cubic-owns-\(\dot X\) slogan missed. The tube slogan
missed.

**Einstein.** The object stayed the classical field. Two
scales, one sign of strain, same PDE.

**Operator.** The blob is scored. B17e is scored.
Next: field occupation (B18e). Finer stays B22e.
Do not spawn \(n=64\). B4c stands. Do not cancel
to \(\Phi\).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B17 | **pass** | blob + signed strain is readable CONC |
| B17a | **pass** | net \(P\approx(\omega\cdot S\omega)_+\) |
| B17b | **fail** | cubic owns \(\dot X\) at the working box |
| B17c | **fail** | \(z\)-independent tube also nets |
| B17d | **fail** | \(L^2\) blob is BKM |
| B17e | **fail** | signed-strain blob closes \(X\) |
| B17f | **fail** | this retunes the PDE |
| domain B | **open** | field-occupation leftover is B18e |

Tesla’s line: a Stokes eigenfunction is not a cubic.
Sit the blob where \(S_{zz}\) keeps a sign. One-sided is
not large versus \(D\).
