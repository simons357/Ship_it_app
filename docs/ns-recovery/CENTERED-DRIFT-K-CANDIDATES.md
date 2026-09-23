# Centered drift: \(K\)-candidate score sheet

**23 September 2026.** Next calculation after
[`CENTERED-DRIFT-TRIAD-SPLIT.md`](CENTERED-DRIFT-TRIAD-SPLIT.md).
Internal checkpoint. **Not a closure theorem.** Ordinary NS is not solved.

Machine: `scripts/centered_drift_k_candidates.py`.
JSON: `results/centered_drift_k_candidates.json`.
The centered equation stays [`CENTERED-EQUATION.md`](CENTERED-EQUATION.md).
Soft X silent. Do not put \(K(t)\) in the PDE.
Do not redo K=0, the §4 triad, or the \(\varepsilon\)-scan as if they
were this page.

Sheet parameters: \(\theta=1/2\), \(\nu=1\). Those are the Young split
used to *score* remainders. They are not a new estimate.

---

## I. Named formulas (explicit)

Target remainder, already on the inventory:

\[
T_c^+\le\theta\nu D_s+K\,X
\qquad\text{or}\qquad
T_c^+\le\theta\nu D_s+K_Y\,Y,
\qquad\theta\in[0,1).
\]

If either sits, then \(\Lambda'\le 2K\) or \((\log\Lambda)'\le 2K_Y\).
One direction only. The formulas below are the candidates.

### 1. Tautological coefficient (not content)

\[
K=\frac{(T_c-\theta\nu D_s)_+}{X},
\qquad
K_Y=\frac{(T_c-\theta\nu D_s)_+}{Y}.
\]

The estimate becomes an identity. Content collapses to
\(\int K<\infty\) from admissible data.

### 2. Uniform energy-class slots (standalone \(C\))

A uniform \(C\) such that \(T_c^+\le C\cdot S\) for one of

\[
S\in\bigl\{E,\,\sqrt{X},\,X,\,Y,\,E\Lambda,\,EY,\,\sqrt{D_s EY}\bigr\}
\]

would give \(K=C\,S/X\) or \(K_Y=C\,S/Y\). Right degree for a cubic
is the \(\sqrt{X}\) / \(X^{3/2}\) line. The last slot is CS/Young of
\(\mathcal R_\star\): \(T_c^+/\sqrt{D_s EY}=\sqrt{\mathcal R_\star}\)
when \(T_c>0\).

### 3. Instantaneous Young packaging (identity, not a bound)

From the definition \(\mathcal R_\star=(T_c_+)^2/(D_s E Y)\) and AM-GM,

\[
T_c^+\le\theta\nu D_s+\frac{\mathcal R_\star}{4\theta\nu}\,EY.
\]

The matching coefficients are

\[
K_{\mathrm{inst}}
=\frac{\mathcal R_\star\,E\Lambda}{4\theta\nu},
\qquad
K_Y^{\mathrm{inst}}
=\frac{\mathcal R_\star\,E}{4\theta\nu}.
\]

This always covers. Integrability is
\(\int\mathcal R_\star E\Lambda\,dt\). That is packaging of the
snapshot ratio, not a remainder derived from data.

### 4. Claimed exact-shell ceiling (restricted class)

Replace \(\mathcal R_\star\) by \(16/9\):

\[
K_{\mathrm{shell}}^{\mathrm{claimed}}
=\frac{(16/9)\,E\Lambda}{4\theta\nu},
\qquad
K_Y^{\mathrm{shell}}
=\frac{(16/9)\,E}{4\theta\nu}.
\]

This is the 9D occupancy-gone majorant. It is **CLAIMED** on an
exact-shell class, not stamped here, and is **not** a regularity
close. \(v_n\) is comparable (aspect exactly 6) and is **not**
exact-shell. The formula is not justified on that field. It also
fails as soon as \(\mathcal R_\star>16/9\)
(\(n\gtrsim 165888\cdot 16/9\)).

No \(H^1\), \(L^\infty\), or BKM candidate is written.

---

## II. Numbers

**§4 note triad** (comparable; \(T_c=16/5\), \(D_s=12/5\), \(X=10\)).
\(K_{\mathrm{taut}}=1/5\). \(K_{\mathrm{inst}}\approx 0.213\).
Young covers. Shell covers (the sample \(\mathcal R_\star\approx 0.038<16/9\)).

**Separated \(L=8\).** \(T_c<\theta\nu D_s\), so
\(K_{\mathrm{taut}}=0\). Weaker face. Not the obstruction.

**Growing layer \(v_n\)** (aspect 6: comparable; in the class).

| \(n\) | \(T_c/D_s\) | \(T_c/E\) | \(T_c/X\) | \(T_c/EY\) | \(\sqrt{\mathcal R_\star}\) | \(K_{\mathrm{taut}}\) | \(K_{\mathrm{inst}}\) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | \(0.215\) | \(1.75\) | \(0.396\) | \(0.00651\) | \(0.0374\) | \(0\) | \(0.0426\) |
| 2 | \(0.189\) | \(91.2\) | \(5.36\) | \(0.0136\) | \(0.0507\) | \(0\) | \(0.507\) |
| 4 | \(0.178\) | \(5.21\cdot 10^3\) | \(78.1\) | \(0.0280\) | \(0.0705\) | \(0\) | \(6.94\) |
| 8 | \(0.172\) | \(3.14\cdot 10^5\) | \(1.19\cdot 10^3\) | \(0.0568\) | \(0.0989\) | \(0\) | \(102\) |

Every uniform slot ratio grows from \(n=1\) to \(n=8\)
(\(T_c/EY\) by \(\approx 8.7\); \(\sqrt{\mathcal R_\star}\) by
\(\approx 2.65\); \(T_c/E\) by \(\approx 1.8\cdot 10^5\)).
At this \(\theta=1/2\), \(T_c<\theta\nu D_s\) on the sample, so
absorption already holds and \(K_{\mathrm{taut}}=0\). \(v_n\) is the
unrestricted-\(\star\) kill, not an absorption kill at \(\theta=1/2\).
\(K_{\mathrm{inst}}\) still grows because it packages a growing
\(\mathcal R_\star\). That waste is the packaging, not a new bound.

**Near-shell annular \((\alpha,\beta)=(5,4)\).**

| \(\varepsilon\) | \(T_c\) | \(T_c/D_s\) | \(T_c/X\) | \(\mathcal R_\star\) | \(K_{\mathrm{inst}}\) |
|---:|---:|---:|---:|---:|---:|
| \(0.20\) | \(0.195\) | \(1.26\) | \(0.0379\) | \(0.00923\) | \(0.0238\) |
| \(0.10\) | \(0.0971\) | \(2.45\) | \(0.0193\) | \(0.00935\) | \(0.0236\) |
| \(0.05\) | \(0.0485\) | \(4.86\) | \(0.00968\) | \(0.00938\) | \(0.0235\) |
| \(0.025\) | \(0.0242\) | \(9.70\) | \(0.00484\) | \(0.00939\) | \(0.0235\) |

\(T_c/D_s=\Theta(\varepsilon^{-1})\) blows. \(K_{\mathrm{inst}}\)
stays, because \(\mathcal R_\star\to K_{5,4}\). A working \(K\) on
this family is at least \(\Theta(\varepsilon)=\Theta(T_c/X)\). That
scaling is a diagnostic. It is not a proved formula.

Young covers every row on the sheet. That is the identity, not
evidence.

---

## III. What this does to the remainder

- A uniform \(C\) in front of \(E\), \(\sqrt{X}\), \(X\), \(Y\),
  \(E\Lambda\), \(EY\), or \(\sqrt{D_s EY}\) is **dead** on \(v_n\).
  The comparable class contains \(v_n\). Those slots cannot be the
  comparable / near-shell \(K\).
- \(K_{\mathrm{inst}}\) / \(K_Y^{\mathrm{inst}}\) are explicit and
  true on every field, including \(v_n\). They are tautological
  Young packaging of snapshot \(\mathcal R_\star\). Not the missing
  implication.
- \(K_{\mathrm{shell}}^{\mathrm{claimed}}\) is explicit. It is not
  true as a derived remainder on the comparable class: \(v_n\) is in
  that class and leaves the exact-shell hypothesis. Numerically it
  still covers \(n=1,2,4,8\) because \(\mathcal R_\star\ll 16/9\).
  That is not justification.
- Constant \(K\) (right-hand side \(KX\) with \(K\) independent of
  amplitude) is already dead by the K=0 amplitude scaling. Do not
  rebuild it. The note-triad value \(K_{\mathrm{taut}}=1/5\) is a
  snapshot, not a law.
- Extra-factor diagnostics
  \(\mathcal R_\star\big/\sqrt{X/E}\) on \(v_n\) only remain
  diagnostics. They are not this \(K\). See
  [`REPLACEMENT-CLOSURE.md`](REPLACEMENT-CLOSURE.md).

No non-tautological \(K\) or \(K_Y\) from admissible data is written.

---

## IV. First missing implication (unchanged)

The algebra \(T_c\le\theta\nu D_s+KX\Rightarrow\Lambda'\le 2K\) sits.
The missing implication is still

\[
T_{\mathrm{comp}}+T_{\mathrm{HH}\to\mathrm{L}}
\;\Longrightarrow\;
K\in L^1_{\mathrm{loc}}
\text{ from admissible data, no }H^1/L^\infty/\mathrm{BKM}.
\]

The comparable / near-shell signed piece is still the face.
Need★ is still unwritten and is not this \(K(t)\).

No new estimate is claimed. No continuation criterion.
**NS not solved.**
