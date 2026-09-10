# Lemma★ — boxed ratio \(\mathcal R_\star\)

10 September 2026. Exact reduction. **Not a proof. NS not solved.**

Locked statement: [`LEMMA-STAR.md`](LEMMA-STAR.md).
Probe: `python3 scripts/ns_attacks/attack7_rstar.py`

---

## The reduction (sits as algebra)

Write \(u=av\), \(a>0\). Then \(T_c\sim a^3\), \(\mathcal D_s\sim a^2\),
\(\Lambda\) is amplitude-invariant, and \(X\Lambda=Y\).

Optimizing Lemma★ over \(a>0\) converts it into the viscosity-free
inequality
\[
\bigl(T_c(v)_+\bigr)^2
\le
4\theta C_0\,
\mathcal D_s(v)\,
\|v\|_2^2\,Y(v).
\]

The decisive dimensionless ratio is
\[
\mathcal R_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}
{\mathcal D_s(v)\,\|v\|_2^2\,Y(v)}.
\]

- If \(\sup_v\mathcal R_\star(v)=\infty\), Lemma★ is dead.
- If \(\mathcal D_s(v)=0\) while \(T_c(v)>0\), it is dead immediately.
- A proof requires a uniform bound on this ratio from triadic
  geometry or cancellation.
- Numerically bounded samples remain evidence only.

\(C_0\) may depend on \(\theta\in(0,1)\). Finite \(\sup\mathcal R_\star\)
gives \(C_0(\theta)\ge(\sup\mathcal R_\star)/(4\theta)\). Unbounded
\(\mathcal R_\star\) kills every finite \(C_0\).

---

## Immediate kill does not fire on a single shell

If the field lives on one eigenvalue of \(A\), then
\(\mathcal D_s=0\) and \(T_c=M-\Lambda N=0\) identically
(\(M=\Lambda N\)). Checked on a two-mode unishell: both zero.
The “\(\mathcal D_s=0\) and \(T_c>0\)” kill needs a field that
is *not* monochromatic.

---

## What Attack 6 did *not* kill

Uniform pre-Young \(|T_c|\le C\|u\|_2 X\Lambda\) dies like \(s\).
On the same scaled triad, \(\mathcal R_\star\) is **flat**:
about \(2.26\times 10^{-4}\) at default phase, about \(0.022\)
at the best of 24 phases, independent of \(s=1\ldots 64\).
Killing the pre-Young form is not killing Lemma★.

Amplitude: \(\mathcal R_\star(av)=\mathcal R_\star(v)\). Checked.

---

## Still open

\(\sup\mathcal R_\star<\infty\) is Lemma★. It is not proved.
HH→L is still the gap. A near-mono probe with one frozen
perturbation gave \(T_c=0\); that is not a bound. Do not cash
\(0.022\) on one triad as \(C_0\).

Do not merge with H1. Do not add \(K(t)\) to the PDE.
Do not write “almost proved.”
