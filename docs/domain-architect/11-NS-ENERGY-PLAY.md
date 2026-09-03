# Energy as a visual object — see the outside, guess the shape

**Not a regularity proof.** A filled enstrophy ladder is not a bound on
\(X\). CosmoEvolution is not this lab.

```bash
python -m domain_architect --energy-play B
```

## Put energy in a shape you can see

Three representative objects:

| Object | What you see (outside) | What you might fill | Status |
|---|---|---|---|
| Shell ladder \(E_j\) | kinetic energy per dyadic shell | \(X_j=2^{2j}E_j\) | **identity** (Bernstein) |
| Energy blob \(e(r)\) | \(e(r)\) for \(r\ge\delta\) | tube interior by even reflect | **play** (extra \(E\)) |
| Spectral tail | high-\(j\) shells | the packet \(j_*\), \(\sigma\) | **cannot fill** |
| Energy tank | bounded Leray \(E\), sometimes the leak | \(X\in L^\infty\) | **cannot fill** (B6) |

## The honest fill

If you see the energy pile, Bernstein fills the enstrophy pile:

\[
X_j=2^{2j}E_j,\qquad E_j=\|\Delta_j u\|_2^2.
\]

The weight warps the shape: the peak of \(X_j\) can sit to the right of
the peak of \(E_j\). Same object, different texture. This does **not**
fill occupation time or \(I_{\mathrm{tube}}\).

```
E_j  ▁▁▂▃█▂▁   energy you see
X_j  ▁▂▅█▆▂▁   enstrophy filled by 2^{2j}
```

## Guessing the inside from the outside

The eye wants: “I see the outside of the energy blob, so I can fill the
tube.” That is the same play as even reflection on the cylinder.

- If the blob **really is even** across \(r=\delta\), the guess measures
  and looks right.
- If the energy **sits in the tube** (the live Navier–Stokes cut), the
  outside is the cheap part and the guessed interior is wrong.

Track B lives in the second case. Off-axis energy is T1 (Sobolev). The
live shape is \(I_{\mathrm{tube}}\), which is not a radial energy density.

Two packets can share a high-\(j\) tail and disagree in the core. Seeing
the outside of the spectrum does not name \(j_*\).

## The tank

You can see kinetic energy. A spike \(X\sim(T_*-t)^{-1/2}\) can have
finite area and infinite height. Seeing the tank does not bound the
height. That is `CLIP-B6-SPIKE`.

Related: [`10-NS-SHAPE-PLAY.md`](10-NS-SHAPE-PLAY.md), [`09-NS-GAP.md`](09-NS-GAP.md).
