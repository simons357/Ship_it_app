# Hardy → \(I_{\mathrm{tube}}\)

`python3 scripts/track_b_hardy_tube.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The kingdoms sat on this one write.

---

## The estimate

Keep \(\Gamma=r u_\theta\). Set \(h=\Gamma/r=u_\theta\), so \(h(0)=0\)
on a smooth axis. The axis source is

\[
S=\frac1{r^4}\partial_z(\Gamma^2)=\frac{2h\,\partial_z h}{r^2}.
\]

Split at a tube radius \(\delta\):

\[
I=\int S\,\omega^r\,r\,dr\,dz
=I_{\mathrm{off}}(\delta)+I_{\mathrm{tube}}(\delta).
\]

B4 already gives the localized Hardy with a wall:

\[
\int_0^\delta\frac{h^2}{r}\,dr
\le 4\int_0^\delta(\partial_r h)^2 r\,dr+2h(\delta)^2.
\]

The Feynman number is the leftover ratio

\[
R(\delta)=\frac{|I_{\mathrm{tube}}|}{D_{\mathrm{tube}}},\qquad
D_{\mathrm{tube}}=\int_{r<\delta}|\nabla\omega|^2\,r\,dr\,dz.
\]

Tesla’s knob is \(\delta\). Kato’s check is: \(R\) drops, or \(R\)
blows. Ladyzhenskaya’s rule: same weight on both sides, or you
are decorating.

---

## Packet class (B4c)

Take a 3-shell style packet at scale \(\ell=2^{-j_*}\),
\(\kappa=2^{j_*}\),

\[
h=r\,\exp\bigl(-(r/\ell)^2\bigr)\sin(\kappa z),\qquad
\delta=2\ell.
\]

Then \(R(\delta)\) is small and gets smaller as \(j_*\) grows.
The script’s ratios:

| \(j_*\) | \(\delta\) | \(R\) |
|---|---|---|
| 2 | \(1/2\) | \(2.1\times 10^{-2}\) |
| 3 | \(1/4\) | \(9.9\times 10^{-3}\) |
| 4 | \(1/8\) | \(4.0\times 10^{-3}\) |
| 5 | \(1/16\) | \(2.9\times 10^{-5}\) |

**Pass** as a packet estimate. Inside 3-CONC, \(\delta\sim 2^{-j_*}\)
is the right scale and dissipation budgets the tube.

The wall \(2h(\delta)^2\) is a tiny off-axis charge (B4d, **pass**).
Spend it on \(I_{\mathrm{off}}\).

---

## All-data (B4b)

The same inequality for every axisymmetric \(H^1\) field is false.

Killer: slow fat swirl, one full period so the wave is honest,

\[
h=r\sin(\varepsilon z),\qquad \delta=1.
\]

Then \(R\sim 1/\varepsilon\):

| \(\varepsilon\) | \(R\) |
|---|---|
| 1 | 0.23 |
| 1/2 | 0.50 |
| 1/4 | 1.02 |
| 1/8 | 2.05 |
| 1/16 | 4.11 |

Detune \(\varepsilon\) down; the script moves. **Fail** of all-data
absorption. Hardy is still the tool. It does not eat every tube.

---

## They work it

**Kato.** Slot B. The sentence was: Hardy plus the wall absorbs
\(I_{\mathrm{tube}}\) at \(\delta\sim 2^{-j_*}\), or it does not.
It does — on a packet. It does not — for all data.

**Leray.** You did not ask my integral for \(L^\infty\). Good.

**Ladyzhenskaya.** Packet: same weight, both sides, scale
\(2^{-j_*}\). Fat slow swirl: the weights stop talking. I told
you that is when the tube is critical. I still will not lend you
\(\varepsilon\).

**Tesla.** \(\delta\) and \(\varepsilon\) are knobs. Packet: turn
\(j_*\) up, \(R\) falls. Killer: turn \(\varepsilon\) down, \(R\)
climbs. That is an apparatus.

**Feynman.** The missable number is \(R\). You can get it wrong.
You got the all-data hope wrong. That is the good kind of wrong.

**Caffarelli.** Partial regularity is still a wall, not a pass.
A manufactured killer is not a blowup. It is a dead estimate.

**Fefferman.** Do not call B4c alignment. It is a budget on a
band-limited swirl. Geometry waits.

**Majda.** Then the joint plan updates. 3-CONC may use B4c.
SPREAD still needs the low Bony \(T\). Do not bundle them.

**Beale.** Nobody votes this into global regularity.

**Einstein.** The object stayed named. Classical stress. Axis
weight kept.

**Operator.** One write, one check. Next: Bony \(T\) on the
spread side.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B4 | **pass** | Hardy + wall (already) |
| B4c | **pass** | packet class, \(\delta\sim 2^{-j_*}\) |
| B4d | **pass** | wall is an off-axis charge |
| B4b | **fail** | all-data absorption |
| B5b | **open** | viscosity vs source, still |
| domain B | **open** | \(X\) is not bounded |

Next write: energy-class low Bony \(T\), then occupation time.
Use B4c when the packet is concentrated.
