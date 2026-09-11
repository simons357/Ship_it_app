# SuperGrok family check — scored against the lock

10 September 2026. Two sentences, then the check
they named. **★ OPEN. NS not solved.
Do not start H1. Do not stamp a kill.**

Statement: [`LEMMA-STAR-STATEMENT.md`](LEMMA-STAR-STATEMENT.md).
Identities: [`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
Core: [`LEMMA-STAR-CORE.md`](LEMMA-STAR-CORE.md).
Explore score: [`LEMMA-STAR-EXPLORE.md`](LEMMA-STAR-EXPLORE.md).

Probe: `python3 scripts/lemma_star_family_check.py`

No new family arrived with the paste.
The check ran on the locked families, with
the locked \(\mathcal D_s\), \(T_c\), \(\mathcal R_\star\).

---

## The two sentences

**1.** “Read the proof files first and check
the family against the locked \(D_s\), \(T_c\),
and \(\mathcal R_\star\) before saying whether
the unrestricted lemma is actually killed.”

**Keep.** That is the desk rule. A kill is
\(\mathcal R_\star(v_n)\to\infty\), or
\(\mathcal D_s=0\) with \(T_c>0\). One
finite lattice number is not that.
There is no Lemma★ proof to walk through.
The identities are the lock.

**2.** “The family is well-posed on paper.
Next: divergence-free / reality, then
\(\mathcal R_\star(v_n)\) on small lattices
against the locked shape form.”

**Keep the next step.** Div-free and
\(v_{-k}=\overline{v_k}\) are the setup.
The shape form is the boxed claim.

**Correct “well-posed on paper.”**
Admissible (mean-zero, \(k\cdot v_k=0\),
reality) is not Hadamard well-posedness
of NSE, and it is not
\(\sup_v\mathcal R_\star<\infty\).
A family can be well-defined and still
fail to kill, or fail to prove.
Do not mix those three.

**Correct \(v_n\).** If \(v_n=v(n\cdot)\)
(Fourier dilation on \(\mathbb{T}^3\)),
\(\mathcal R_\star\) is exactly invariant.
Already on disk. Not a kill.
A genuine indexed family still has to
diverge. Small \(n\) that stays finite
only raises \(C_{\mathrm{geom}}\).

Unrestricted lemma = the boxed claim
on every divergence-free field, not a
subclass. 9B \(K_{\alpha,\beta}\) is
restricted. Do not cash a subclass
bound as the unrestricted lemma, and
do not cash a subclass sample as a kill
of the unrestricted lemma.

---

## Locked objects (do not reconstruct)

\[
\mathcal D_s=Z-\Lambda Y,\qquad
T_c=M-\Lambda N,\qquad
\mathcal R_\star=\frac{(T_c)_+^2}{\mathcal D_s\,E\,Y}.
\]

Two \(\mathcal D_s\) formulas must agree.
\(T_c\) is a signed triad sum. Reverse
the field: \(T_c\) is odd.
This \(\mathcal R_\star\) is
`ratio_box` / `R_star` in the core.
It is not Attack-2 \(C_*\).

---

## What the probe did

On the locked two-shell aligned closer
\((\alpha,\beta)=(1,2)\) and \((4,8)\):

- every mode is divergence-free
- every mode has \(v_{-k}=\overline{v_k}\)
- \(\mathcal D_s\) moment form matches the
  spectral sum
- \(\mathcal R_\star(av)=\mathcal R_\star(v)\)
- \(\mathcal R_\star(v(n\cdot))=\mathcal R_\star(v)\)
  for \(n=2,3\)
- \(T_c(-v)=-T_c(v)\)

Those numbers stay finite. They match
the book (N-shell peak on \((1,2)\);
9B family on \((4,8)\)). Not
\(\mathcal R_\star\to\infty\).

No unnamed SuperGrok family was sent
with that paste. The later screenshot
dump named a growing cube. Score:
[`LEMMA-STAR-CUBE.md`](LEMMA-STAR-CUBE.md).
Run the lock on that mode list.
Do not invent a second family.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| LSfam_lock_first | **pass** | check locked \(\mathcal D_s,T_c,\mathcal R_\star\) before a kill stamp |
| LSfam_div_real | **pass** | setup sits on the locked families |
| LSfam_dilation_flat | **pass** | \(v(n\cdot)\) does not move \(\mathcal R_\star\) |
| LSfam_wellposed_kills | **fail** | “well-posed on paper” is not a kill |
| LSfam_small_lattice_kills | **fail** | finite \(\mathcal R_\star\) on small \(n\) is not \(\to\infty\) |
| LSfam_unrestricted_killed | **fail** | unrestricted ★ is OPEN |

★ stays OPEN. Kill lane stays LIVE.
Do not start H1. Do not stop patching.

NS not solved.
