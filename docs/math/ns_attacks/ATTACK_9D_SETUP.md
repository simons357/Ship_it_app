# Attack 9D — precise setup (do not guess)

**Locked:** 12 September 2026  
**This wording answers the setup questions.** Spec: [`ATTACK_9D_THETA_M2_LOCKED_PHASE.md`](./ATTACK_9D_THETA_M2_LOCKED_PHASE.md). Exclusion: [`ATTACK_9B_COUNTING_CS_EXCLUSION.md`](./ATTACK_9B_COUNTING_CS_EXCLUSION.md).

**NS not solved. Lemma★ OPEN.**

---

## What \(B\) is

The same bilinear as the rest of this book, not a new 9D object, not Attack 3’s HH→L split.

\[
B(w,w)=P[(w\cdot\nabla)w],
\qquad
\widehat B_k=i\,P_k\sum_{p+q=k}(q\cdot w_p)w_q.
\]

\(\Pi_\beta\) is the exact-shell projector onto \(\{|k|^2=\beta\}\). The 9D target is the **9B** uniform bound

\[
\|\Pi_\beta B(w,w)\|_2
\le C\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2,
\]

equivalent to \(\sup K_{\alpha,\beta}<\infty\) on exact-shell \(w\), where

\[
K_{\alpha,\beta}(w)
=\frac{\beta\,\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}.
\]

Observed constant:

\[
C_{\mathrm{obs}}(w)
=\frac{\|\Pi_\beta B(w,w)\|_2\,\sqrt{\beta}}{\alpha\|w\|_2^2}.
\]

Do **not** drop \(|k|\) from \(B\). Do **not** replace \(\|\Pi_\beta B\|_2\) by an HH→L-only piece of \(T_c\).

Attack 3 (Bony HH→L) is a **diagnostic partition of complete signed \(T_c\)**. It did not close. The discarded product \(|T_c|\le C\|u\|_2 X^{3/2}\) is false. There is **no** locked law \(\mathcal R_\star\sim\beta/\alpha\) in these files. 9B’s locked limit is, for aligned \(z_\beta\parallel\Pi_\beta B(w,w)\),

\[
\lim_{\varepsilon\to0}\mathcal R_\star(w+\varepsilon z_\beta)=K_{\alpha,\beta}(w).
\]

Finite 9B sample: \(\max K\approx 0.641\) at \((4,8)\). Not a kill.

---

## Growth law — no exponent is fixed

“Growing input and output supports” is **not** a prescribed \(m\sim\alpha^p\), \(s\sim\beta^q\). Finding a scaling that diverges is the **search**, not a locked setup parameter.

**Fixed (admissible family):**

- Input: \(w\) supported on exact shell \(\alpha\) (\(Aw=\alpha w\)), **full complex polarizations**, frequency factors retained. Support size \(m=\#\{k:|k|^2=\alpha\}\) grows with the lattice (or a growing subset of that shell). Conjugate-closed, divergence-free.
- Output: shell \(\beta\neq\alpha\) with \(\beta\le 4\alpha\) (two inputs on \(\alpha\) cannot produce larger \(\beta\)). Occupied count \(s=\#\mathrm{supp}(\Pi_\beta B(w,w))\). \(s\) is **observed**, not held fixed.
- Fixed \(s\) is **excluded** (\(K\le 16s\)). \(\Theta(m^2)\) onto one or finitely many outputs is **impossible**.

**Open:** whether \(K\) or \(C_{\mathrm{obs}}\) stays bounded as \(m\) and \(s\) grow. Unbounded \(\Rightarrow\) ★ dead on the 9B family. A bounded sample \(\Rightarrow\) those shapes did not kill ★; not a proof.

The checked-in probe `scripts/ns_attacks/attack9d_growing_io.py` implements the **natural** version: full shells up to `--kmax`, random complex polarizations, report best \(K\) / \(C_{\mathrm{obs}}\) per \((\alpha,\beta)\). It does **not** fix an exponent. A designed growing subset with growing \(s\) is also allowed by the spec; it is not a different \(B\).

---

## Order (this book’s call)

Do **not** start the ★ sentence from an HH→L kill-list or from a guessed \(\mathcal R_\star\sim\beta/\alpha\). That uses the wrong object and extrapolates past what is proved.

1. Use this setup if you run 9D.
2. If you write the ★ reason instead, write it from **complete signed** \(T_c\) and \(D_s\), and flag every step that is not already an identity in [`LEMMA_STAR_EXACT_FORMULAS.md`](./LEMMA_STAR_EXACT_FORMULAS.md).

Board: [`docs/ns-recovery/WHAT-ELSE.md`](../../ns-recovery/WHAT-ELSE.md).
