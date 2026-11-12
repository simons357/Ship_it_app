# DA-NS-2 — Y-cousin occupation bound

**12 November 2026.** Portable Domain Architect lock of leftover 4 / G4
on `main`. Identities sit. **The integral is OPEN.** Ordinary unaugmented
3-D Navier–Stokes is not solved. Lemma★ is not proved. Soft X silent.

Do not put \(K(t)\) in the PDE. Do not glue this page to Φ-renorm or
Clay Statement B.

Machine: `scripts/ns_attacks/da_ns_2.py`.
JSON: `results/da_ns_2.json`.
Evaluator: `scripts/ns_lemma_star_core.py`.
DA card: `python3 -m domain_architect --da-ns-2`.

DA-NS-1 is the X-remainder \(T_c\le\theta\nu D_s+K(t)X\). This page is
the Y-cousin. They are the same leftover, two writings.

---

## 1. The named hole

On mean-zero divergence-free Galerkin fields on \(\mathbb T^3\),
\(A=-P\Delta\), \(\lambda_k=|k|^2\):

\[
X=\|A^{1/2}u\|_2^2,\quad
Y=\|Au\|_2^2,\quad
Z=\|A^{3/2}u\|_2^2,\quad
\Lambda=Y/X,
\]
\[
T_c=M-\Lambda N,\qquad
D_s=Z-\Lambda Y\ge 0.
\]

The centered equation is exact:

\[
(\log\Lambda)'=\frac{2}{Y}(T_c-\nu D_s).
\]

For fixed \(\theta\in[0,1)\),

\[
K_{\min,\theta}^{(n)}
=\frac{\bigl[T_c^{(n)}-\theta\nu D_s^{(n)}\bigr]_+}{Y^{(n)}}.
\]

**DA-NS-2.**

\[
\sup_n\int_0^T K_{\min,\theta}^{(n)}(t)\,dt
\le F(\nu,T,u_0)<\infty
\]

without a continuation norm. Phase variables count only if they prove
this bound rather than rename it.

If it sits, \(\Lambda\) stays bounded, then \(X\le\|u_0\|_2^2\Lambda\),
then continuation. The implication is the usual skeleton. **The integral is the hole.**

---

## 2. Exact algebra that is not the bound

Rewrite

\[
(\log\Lambda)'
=
\frac{2}{Y}(T_c-\theta\nu D_s)
-
2(1-\theta)\nu\frac{D_s}{Y}.
\]

Always \((\log\Lambda)'\le 2K_{\min,\theta}\), because the first term is
at most twice the positive part and the second term is non-positive.
On the note triad the machine residual of that inequality is zero after
accounting for the leftover.

The tautological Y-estimate

\[
T_c\le\theta\nu D_s+K_{\min,\theta}\,Y
\]

is an **identity**, not a theorem: \(K_{\min,\theta}\) is defined as that
ratio. Content collapses to \(\int K_{\min,\theta}<\infty\).

Cousin relation: the tautological X-coefficient is
\(K_X=\Lambda K_{\min,\theta}\). DA-NS-1 and DA-NS-2 are two writings of
the same leftover. Lemma★ writes it a third time as an energy-budget
Clay packaging and is also **not proved**.

Frozen \(\theta=1\) leftover:

\[
\frac{T_c-\theta\nu D_s}{Y}
=
\frac{T_c-\nu D_s}{Y}
+(1-\theta)\nu\frac{D_s}{Y}.
\]

The needed endpoint is \(\theta<1\). The term \((1-\theta)\nu D_s/Y\)
survives. Standalone frozen log-charge does not close DA-NS-2.

---

## 3. Locked finite-triad checkpoint

Section-4 near-scale triad \(p=(1,0,0)\), \(q=(0,1,0)\), \(r=(1,1,0)\):

\[
X=10,\quad Y=14,\quad Z=22,\quad\Lambda=\frac75,\quad
D_s=\frac{12}{5},\quad N=2,\quad M=6,\quad
T_c=\frac{16}{5},\quad \frac{T_c}{D_s}=\frac43.
\]

At \(\nu=1\):

\[
K_{\min,0}=\frac{16}{70}=\frac{8}{35},\qquad
K_{\min,1/2}=\frac{1}{7}.
\]

Sign is phase: \(u\mapsto -u\) flips \(T_c\) and \(K_{\min}\) (at
\(\theta=0\)) and leaves \(Y,D_s\) fixed. Quadratic moments do not see
the dangerous sign.

---

## 4. What is killed

| Attempt | Status |
|---|---|
| \(T_c\le\theta\nu D_s\) (pure absorption) | **KILLED.** \(T_c/D_s\) scales with amplitude. The note triad already has \(T_c/D_s=4/3\). |
| Tautological \(K_Y\) as a theorem | **KILLED.** An identity is not DA-NS-2. |
| Charge-only net coercivity | **KILLED** (Sprint 01 / PR #142). Two-triad witness: \(Q_{a,\Gamma}=0\) and \(\mathfrak T_c^{\mathrm{het}}>0\). |
| Frozen log-charge at \(\theta=1\) | **KILLED** as a \(\theta<1\) budget. \((1-\theta)\nu D_s/Y\) survives. |
| Automatic dephasing | **KILLED.** 2D3C half-turn lock is separately regular geometry. |
| One-channel ODE as vector NS | **KILLED.** Not an invariant subsystem. |
| Near-shell \(T_c/D_s\) bounded | **KILLED.** \(T_c=\Theta(\varepsilon)\), \(D_s=\Theta(\varepsilon^2)\). Snapshot \(K_{\min}\) on this family is \(O(\varepsilon)\) because \(Y\) stays \(O(1)\); that is not the integral bound. |
| Serrin / BKM last line | **STOP.** Continuation norm. |
| \(\int D_s/Y\), \(\sup\Lambda\), \(\int Y\) | **STOP.** Renamed hole. |

---

## 5. What stays OPEN

The Galerkin-uniform integral. A **useful** (non-tautological) \(K_Y\)
controlled by energy-inequality data, or by a named dynamical bound that
does not assume the desired \(H^1\) ceiling, \(L^\infty\), or BKM.

**Next write (not sitting).** Joint Gap–Charge Epoch Budget: charge,
radial covariance, moving-barycenter error, homochiral drift, cross-band
flux, phase/far terms, one-use dissipation, summable resets. All
together, cutoff-uniform, \(\theta<1\) directly. If the last line is
\(\int D_s/Y\), \(\sup\Lambda\), \(\int Y\), or a continuation norm,
stop.

Need★ (signed dual on HH→L after two-shell gap-cancel) remains
**MISSING**. It is related, not a substitute for the integral.

Smooth-split (PR #149) is an instantaneous estimate. It does not close
\(\int g^2\,dt\), DA-NS-2, Lemma★, or NS.

---

## 6. What this is not

- Not Φ-renorm (wrong-variable story near the swirl axis).
- Not DA-NS-1 proved. That X-remainder is the same leftover.
- Not Lemma★ proved. PRODUCT-BLOCK still blocks the energy-budget writing.
- Not a Clay path.
- Not Q1 / de-augmentation. That is a different PDE.

`ns_solved` is false. `lemma_star_proved` is false. `da_ns_2` is OPEN.
