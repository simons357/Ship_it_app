# Same-shell packet: \(D_s\) is the gap, not an AP width

**SoT:** [`SOT.md`](SOT.md) — **locked** 10 September 2026. This note does not override it.

**Date:** 10 September 2026  
**Source of the claim:** user note on cloud agent https://cursor.com/agents/bc-01a07930-4f88-7811-8d60-3383fff0b5c1  
**Probe:** `scripts/same_shell_packet_probe.py`  
**Status:** **numerical / combinatorial on the natural ensemble.** Not a theorem. Uniform triadic bound **open**. Navier–Stokes **not solved**.

This is **not** an arithmetic progression. It is a **packet**: the full integer lattice spheres of radii \(\sqrt{n}\) and \(\sqrt{n+d}\) for a **fixed gap** \(d\).

---

## Construction (exact)

Let \(S_n=\{k\in\mathbb{Z}^3:\lvert k\rvert^2=n\}\). The packet is \(S_n\cup S_{n+d}\). The number of keys is

\[
m=r_3(n)+r_3(n+d),\qquad r_3(n)=\#S_n,
\]

which grows with \(n\). There is **no AP width**.

**Landings / mixed closures:** unordered triples \(\{k,p,r\}\subset S_n\cup S_{n+d}\) with \(k+p+r=0\) and shell type \((n,n,n+d)\) — two vectors on the lower sphere, one on the upper. That uses the gap \(d\), not a long progression.

**Two-mass \(D_s\)** (equal \(L^2\) masses \(a=b=1\) on the two shells, Stokes eigenvalues \(\lambda=n\), \(\mu=n+d\)):

\[
X=\lambda a+\mu b,\quad
Y=\lambda^2 a+\mu^2 b,\quad
Z=\lambda^3 a+\mu^3 b,\quad
\mathcal D_s=\frac{XZ-Y^2}{X}=\frac{ab\,\lambda\mu\,d^2}{X}.
\]

For fixed \(d\) this is \(\Theta(n)\): gap fixed, \(\lambda\sim n\). The \(O(1)\) in the denominator of a gap (not a growing width) is available in this discrete model. This is the **two-point spectral remainder**, not a proved NS estimate.

---

## What grew (independently checked)

On the live gap \(d=1\), mixed closures **exist** and run from **48 to 288** on the shells below. They scale like \(O(m)\), not \(O(m^2)\). A full sphere is not an additive basis of that density.

| \(n\) | \(d\) | \(r_3(n)+r_3(n+d)\) | mixed closures \((n,n,n+d)\) | \(c/m\) | \(c/m^2\) |
|---:|---:|---:|---:|---:|---:|
| 9 | 1 | 30+24 = 54 | **48** | 0.889 | 0.0165 |
| 13 | 1 | 24+48 = 72 | 48 | 0.667 | 0.0093 |
| 17 | 1 | 48+36 = 84 | 36 | 0.429 | 0.0051 |
| 25 | 1 | 30+72 = 102 | 48 | 0.471 | 0.0046 |
| 41 | 1 | 96+48 = 144 | 96 | 0.667 | 0.0046 |
| 49 | 1 | 54+84 = 138 | 72 | 0.522 | 0.0038 |
| **89** | 1 | **144+120 = 264** | **288** | 1.091 | 0.0041 |

Verified by `tests/test_same_shell_packet.py`. The 10 Sep note’s “144+120 keys, 288 closures” matches \(S_{89}\cup S_{90}\).

**\(d=2\):** no mixed \((n,n,n+2)\) landings on the same list \(\{9,17,25,41,49,89\}\).  
**\(d=3\):** sporadic mixed landings on that list (24 at \(n=9\), 0 at \(n=17,25,89\), 96 at \(n=41\)).

Unrestricted \(k+p+r=0\) on *other* \(n\) can be nonempty for \(d=2\). The user statement is about the **range tested** (the growing-\(m\) \(d=1\) shells), and that is what the tests lock.

---

## What \(\mathcal R_\star\) did (user-reported; not recomputed here)

Quoted from the 10 Sep 2026 note, **not recomputed on this branch**:

> Largest at the smallest shell: \(n=9\), \(\mathcal R_\star\simeq 0.11\). At \(n=89\), 144+120 keys, 288 closures, \(\mathcal R_\star\simeq 0.031\). The ratio falls, it does not track \(m^{1/2}\).

Classification: **numerical evidence from an unrecovered script / session.** Key counts and closure counts above are independently reproduced. The ratio’s **definition** is now locked in `five-lane-pack/docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md`; the two numbers \(0.11\) and \(0.031\) have **not** been re-run against that formula here.

---

## What the heuristic assumed, and the verdict

**Assumed:** whole-sphere packets supply \(\Theta(m^2)\) aligned closures, so \(\mathfrak T_c\) would produce \(\mathcal R_\star\sim m\).

**On this ensemble:** closures are \(O(m)\); \(\mathcal R_\star\) as reported **falls**. The \(O(1)\) gap denominator is available, and \(\mathfrak T_c\) still does not produce \(\mathcal R_\star\sim m\).

**Verdict (construction, not Clay):** the heuristic is **false for the natural same-shell ensemble**.

---

## What would still be a packet kill

A **designed subset** of two fixed shells with \(\Theta(m^2)\) closures **and locked phases** — not the full sphere. Until that object is built and \(\mathcal R_\star\) tracks \(m\), the heuristic does not hold here.

Isolated triangles, wide APs, narrow APs, and full adjacent spheres: **no kill** (user statement; AP families were not re-run in this probe).

**Uniform triadic bound: open. Navier–Stokes: not solved.**

---

## Other live writing (not started here)

H1 on the cylinder remains the other live track if the packet line is shelved. This note does **not** switch to it.

---

## Separation of sources

| Kind | Content |
|---|---|
| User note 10 Sep 2026 | Packet vs AP; \(\mathcal R_\star\) values; heuristic false; kill criterion; NS not solved |
| This agent, independent | \(r_3\) counts; 48 and 288 mixed closures; \(O(m)\) vs \(O(m^2)\); \(d=2\) zeros on the listed shells; two-mass \(D_s=\Theta(n)\) |
| Not done | No invented \(\mathfrak T_c\) formula; no \(\mathcal R_\star\) recompute; no NS claim; no H1-cylinder write |
