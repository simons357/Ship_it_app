# PR 24 — SuperGrok review scored

13 September 2026.
Screenshots of SuperGrok’s seven questions
and the PR bottom-line table.
**This page scores that review against
the tape. It does not close a leftover.**

Exact-shell \(4/3\) stays **CLAIMED**.
SuperGrok’s “keep it as a theorem”
is **NO**. Specialist pending.
The write-up example is three-shear
\(K=2/3\), not a sweep table.
Unrestricted ★ stays **KILLED** by \(v_n\).
NS is not solved. Soft X silent.

Tape: [`YES-NO-OPEN.md`](YES-NO-OPEN.md).
9D bound: [`ATTACK-9D-FULL-SUPPORT-BOUND.md`](ATTACK-9D-FULL-SUPPORT-BOUND.md).
Floor: [`ATTACK-9D-TWO-THIRDS.md`](ATTACK-9D-TWO-THIRDS.md).
Kill: [`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md).

---

## Bottom line (SuperGrok’s table)

| Claim | SuperGrok | Tape |
|---|---|---|
| Exact-shell 9D, \(C=4/3\) | Believable hand proof; keep as a theorem of exact-shell theory, not multi-shell | Scope restriction **YES**. Theorem stamp **NO**. Status **CLAIMED**. |
| Unrestricted ★, one geometry constant | Family admissible; matches the evaluator; treat the unrestricted claim as false | **YES.** Killed by \(v_n\). |
| Signed-dual repair of that box | Not available without changing the statement | **YES.** Need★ cannot repair. |
| Unaugmented regularity | Needs a new closure; this patch does not provide one | **YES.** Replacement **OPEN**. |
| Finite grow-\(s\) / 9B maxima | Historical only; do not promote | **YES.** |

The two analytic conclusions stay distinct.
A specialist can accept or break each
by pointing at one equation.
That is the right status for PR 24.
It is not a close of ordinary NS.

---

## SuperGrok’s \(K=2/3\) field

Agreed. Already seated.
\(w=(\sin y,\sin z,\sin x)\),
\(K_{1,2}=2/3\) by hand.
That is the write-up example.
It clears \(0.641\). It sits under
\(16/9\). Floor, not ceiling.

SuperGrok also said the \(4/3\) bound
would be the focus of a report.
The claimed bound is \(4/3\).
The example a reader can check
without a seed is \(2/3\).
Do not swap those roles.

---

## The seven questions

### 1. Derivation

Closed-form **claim**, not a fit to
samples. The coefficient \(4/3\) enters
from the claimed polarization form

\[
K_{\alpha,\beta}
\le
\frac{3}{4}\Bigl(\frac{\beta}{\alpha}\Bigr)^2
\Bigl(1-\frac{\beta}{4\alpha}\Bigr)
\le
\frac{16}{9},
\]

then
\(\|\Pi_\beta B\|_2
\le (4/3)\,(\alpha/\sqrt{\beta})\,\|w\|_2^2\)
because
\(K=\beta\|\Pi_\beta B\|_2^2/(\alpha^2\|w\|_2^4)\).
\(16/9\) is the max of that cubic
factor on \(0<\beta\le 4\alpha\),
attained at \(x=\beta/\alpha=8/3\).
The derivative and the endpoints
now sit on the bound page.
That calculus does not prove the
envelope. Optimality is **not** claimed.
Conventions (normalized torus,
\(\alpha>0\), \(w\neq 0\)) and the
constraint set sit with the bound.
Hermitian Cauchy–Schwarz covers
independent complex polarizations
on the one-mode factor
\(\lvert k\cdot w_p\rvert\le\lvert k_\perp\rvert\,\lvert w_p\rvert\).
Live \(B\) is the ordered sum with
no extra \(1/2\). A reconstructed
\(3/4=(1/2)^2\cdot 3\) is **NO**.
The kernel geometry
(\(k\cdot p=\beta/2\),
\(\lvert k_\perp\rvert^2=\beta(1-\beta/(4\alpha))\))
sits. The verifier is an internal
check: live family, live sample \(K\),
live count ratios, saved grow-\(s\).
It does not certify \(16/9\).
The factor \(3\) is derived on the
bound page from claimed two-plane
plus AM-GM. Not the Ring Lemma.
Hermitian CS is written as
\(\lvert\langle k_\perp,\overline{w_p}\rangle\rvert\).
\(2/3<16/9\) is a sanity check.
As \(\beta\to 4\alpha\) nothing divides
by \(\lvert k_\perp\rvert\).
Independent review: no name, no date.
Soft X silent. Not a letter.
Specialist review of the weighted
count, the factor \(3/4\), the
kernel step, and the
two-plane incidence is still pending.

### 2. Evidence

Full aligned 9B table
(`K_by_pair`, seed 1390, \(k_{\max}=6\),
24 pairs):

| \((\alpha,\beta)\) | \(K\) |
|---|---:|
| \((4,8)\) | \(0.641\) |
| \((1,2)\) | \(0.578\) |
| \((5,10)\) | \(0.298\) |
| \((2,4)\) | \(0.296\) |
| \((13,26)\) | \(0.234\) |
| \((9,18)\) | \(0.179\) |
| \((5,6)\) | \(0.101\) |
| \((9,10)\) | \(0.061\) |
| \((6,8)\) | \(0.053\) |
| \((5,2)\) | \(0.012\) |
| others in the 24 | \(0\) |

JSON: `results/ns_five_lane_2026-09-10/attack9b_exact_shell/attack9b.json`.
Plot: `K_by_ab_pair.png` in that folder.
Counting lock (288 fields): max
\(K\approx 0.506\).
Grow-\(s\) (\(k_{\max}=8\), 2084 fields):
max \(K\approx 0.456\) at \((16,32)\).
Three-shear: \(K=2/3\approx 0.667\).
None of those approach
\(16/9\approx 1.778\).
That is not a near-ceiling sweep.

### 3. Independence

Nobody outside this project has
checked the algebra. No date. No name.
Minimal reproduction, under an hour:

```bash
python3 scripts/ns_attacks/attack9d_two_thirds.py
python3 scripts/ns_attacks/verify_pr24_closure_review.py \
  --out results/pr24_closure_review/audit.json
python3 -m unittest tests.test_attack9d_two_thirds \
  tests.test_pr24_closure_review \
  tests.test_pr24_supergrok_review
```

That checks the floor and the \(v_n\)
table. It does not certify \(16/9\).

### 4. Role in regularity

If \(4/3\) holds, you have an
exact-shell bound on \(K\).
It does not close leftover 4.
Unrestricted ★ is already dead
by the multi-shell family \(v_n\).
There is no path from this
coefficient to a continuation
criterion. Unused as a regularity
close. A true \(4/3\) does not
restore ★ \(\Rightarrow\) GR.

### 5. Priority

Original to this project as a write.
Not published. No literature search
against shell-interaction or
packet-exhaustion sits on this
branch. Do not invent one.

### 6. Open end

A single exact-shell field with
\(K>16/9\) falsifies the claimed
constant. A sequence with
\(K\to\infty\) falsifies
\(\sup K<\infty\). Those are
different statements.
If \(16/9\) is false, the \(v_n\)
kill of unrestricted ★ still stands,
H1 stays open, ordinary NS stays
open. Designed 9D stays dead.

### 7. What SuperGrok covered

Derivation, evidence, independence,
role, priority, falsifiability.
The seventh object is the explicit
field \(K=2/3\). Seated.

---

## Four items SuperGrok wanted before review

Now on the live pages. Isolation
is not certification.

1. One-line killed inequality, every
   symbol defined:
   [`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md).
2. \(v_n\) against every kill-relevant
   side-condition written on
   [`LEMMA-STAR-REASON.md`](LEMMA-STAR-REASON.md):
   same page, checklist.
3. \(\langle D_n^3\rangle=3n^2+3n+1\)
   as a three-line sum:
   [`math/ns_attacks/LEMMA_STAR_GROWING_LAYER_COUNTEREXAMPLE.md`](math/ns_attacks/LEMMA_STAR_GROWING_LAYER_COUNTEREXAMPLE.md).
4. Two-plane incidence isolated as
   its own claimed proposition:
   [`math/ns_attacks/ATTACK_9D_FULL_SUPPORT_BOUND.md`](math/ns_attacks/ATTACK_9D_FULL_SUPPORT_BOUND.md).

---

## Status

| Item | Verdict |
|---|---|
| SuperGrok ★ / Need★ / leftover / historical | **YES.** Matches the tape. |
| SuperGrok “4/3 is a theorem” | **NO.** CLAIMED. |
| Three-shear as write-up example | **YES.** Floor. |
| Outside algebra check | **NO.** |
| Near-ceiling sweep | **NO.** |
| Ordinary NS | **OPEN.** |
