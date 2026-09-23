# Centered drift: symmetrized coefficient and channel split

**23 September 2026.** Next calculation after
[`CENTERED-DRIFT-TRIAD-TEST.md`](CENTERED-DRIFT-TRIAD-TEST.md).
Internal checkpoint. **Not a closure theorem.** Ordinary NS is not solved.

Machine: `scripts/centered_drift_triad_split.py`.
JSON: `results/centered_drift_triad_split.json`.
The centered equation stays [`CENTERED-EQUATION.md`](CENTERED-EQUATION.md).
Soft X silent. Do not put \(K(t)\) in the PDE.

---

## I. Exact identities

### Coupling

For a real triad \(r=p+q\) with amplitudes \(A=\widehat u(p)\),
\(B=\widehat u(q)\), \(C=\widehat u(r)\),

\[
\Gamma(A,B,C;p,q)
=
\mathrm{Im}\Bigl(\overline C\cdot P_r\bigl((q\cdot A)B+(p\cdot B)A\bigr)\Bigr).
\]

On the six-mode real field this is \(\tau_r\) for the \(+r\) mode.
The note triad has \(\Gamma=1=\tau_r\). Reality gives \(\tau_{-k}=\tau_k\).
Energy on each conjugate pair: \(\tau_p+\tau_q+\tau_r=0\).

### Fully symmetrized coefficient

With \(f_\Lambda(s)=s(s-\Lambda)\),

\[
T_c
=
2\sum_{k\in\{p,q,r\}}f_\Lambda(\lambda_k)\,\tau_k
=
2\bigl(f_\Lambda(\lambda_p)-f_\Lambda(\lambda_r)\bigr)\tau_p
+
2\bigl(f_\Lambda(\lambda_q)-f_\Lambda(\lambda_r)\bigr)\tau_q.
\]

The factor \(f_\Lambda(a)-f_\Lambda(b)=(a-b)(a+b-\Lambda)\) is the
spectral-gap coefficient. It is not a sign and not a bound on
\((\tau_p,\tau_q)\). One comparable triad can put all the flux on a
single leg (§4: \(\tau_p=0\), \(\tau_q=-1\), \(\tau_r=1\)).

### Ordered-pair split of a general field

\[
T_c
=
\sum_{p+q=k}\lambda_k(\lambda_k-\Lambda)\,I_3(p,q;k),
\qquad
I_3=\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

Each ordered pair is labelled:

- **HH→L** if \(\lambda_k<\lambda_p\) and \(\lambda_k<\lambda_q\);
- **separated** if \(\max\lambda/\min\lambda\ge 8\) and not HH→L;
- **comparable** otherwise.

Then \(T_c=T_{\mathrm{comp}}+T_{\mathrm{sep}}+T_{\mathrm{HH}\to\mathrm{L}}\)
exactly. Residual on the note triad: \(0\). Back-reaction pairs on a
fat field can sit in a different bucket from the geometric closer
\((p,q)\to r\). That is bookkeeping, not a second \(T_c\).

---

## II. Numerical observations

**Phase-coherent §4 shape.** Twenty-four phases on the aligned closer.
\(\max T_c=16/5\), \(\min T_c=-16/5\), \(\max T_c/D_s=4/3\). The note
phase is already the maximizer. Sign is phase. All of \(T_c\) is
comparable.

**Separated \(L=8\).** \(T_c/D_s\approx 0.179\sim\sqrt{2}/8\). Split is
separated, with a small HH→L back-reaction. Not the obstruction.

**HH→L triad** \(p=(2,2,1)\), \(q=(-2,-2,1)\), \(r=(0,0,2)\)
(\(\alpha=9\), \(\beta=4\)), aligned closer. \(T_c=-55.54\), flip
\(T_c^+=55.54\), \(T_c^+/D_s\approx 0.339<4/3\). Weaker than the
comparable note triad on this example. Not a uniform HH→L law.

**Comparable neighbors** (aligned, same \(A\)):

| \(q\) | \(T_c/D_s\) |
|---|---:|
| \((0,1,0)\) | \(4/3\) |
| \((0,1,1)\) | \(0.168\) |
| \((1,1,0)\) | \(0.487\) |
| \((0,2,1)\) | \(0.421\) |

The note triad is the strongest of these four.

**Annular packets.** Exact shell \(\alpha\) plus aligned \(\varepsilon\)-closer
on \(\beta\). Adjacent \((\alpha,\beta)=(5,4)\):

| \(\varepsilon\) | \(T_c\) | \(D_s\) | \(T_c/D_s\) | \(\mathcal R_\star\) |
|---:|---:|---:|---:|---:|
| \(0.20\) | \(0.195\) | \(0.155\) | \(1.26\) | \(0.00923\) |
| \(0.10\) | \(0.097\) | \(0.0397\) | \(2.45\) | \(0.00935\) |
| \(0.05\) | \(0.0485\) | \(0.00998\) | \(4.86\) | \(0.00938\) |
| \(0.025\) | \(0.0242\) | \(0.00250\) | \(9.70\) | \(0.00939\) |

So \(T_c=\Theta(\varepsilon)\), \(D_s=\Theta(\varepsilon^2)\),
\(T_c/D_s=\Theta(\varepsilon^{-1})\to\infty\), while
\(\mathcal R_\star\to K_{5,4}\approx 0.00939\). This is the near-shell
linearization, not a new \(C_{\mathrm{geom}}\).

---

## III. What this does to the remainder

Pure absorption \(T_c^+\le\theta\nu D_s\) is already dead on §4
(\(T_c^+/D_s=(4/3)s\)). The annular scan kills it again, more sharply:
\(T_c^+/D_s\) is unbounded as \(\varepsilon\to 0\) along an aligned
closer, even though \(\mathcal R_\star\) stays finite.

Any remainder of the form \(T_c^+\le\theta\nu D_s+K(t)X\) must therefore
carry the \(\Theta(\varepsilon)\) piece. On that family \(X=\Theta(1)\)
and \(T_c=\Theta(\varepsilon)\), so a working \(K\) is at least
\(\Theta(\varepsilon)=\Theta(T_c/X)\). That scaling is a diagnostic.
It is not a proved formula for \(K(t)\), and it is not integrable
control.

Tautological \(K=(T_c-\theta\nu D_s)_+/X\) remains not content.

---

## IV. First missing implication (unchanged object, sharper face)

The algebra \(T_c\le\theta\nu D_s+KX\Rightarrow\Lambda'\le 2K\) sits.
The missing implication is still

\[
T_{\mathrm{comp}}+T_{\mathrm{HH}\to\mathrm{L}}
\;\Longrightarrow\;
K\in L^1_{\mathrm{loc}}
\text{ from admissible data, no }H^1/L^\infty/\mathrm{BKM}.
\]

The separated bucket is the weaker face on the tested families.
The comparable / near-shell signed piece is the obstruction.
Need★ is the two-shell signed dual on HH→L; it is still unwritten
and is not this \(K(t)\).

No new estimate is claimed. No continuation criterion.
