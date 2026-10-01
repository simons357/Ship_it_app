# Exact matrix-to-Mertens identities

**Proved.** No Riemann or Mertens estimate is used.

## Objects

Keep precisely

\[
Q_N(i,j)=\frac{\mu(\gcd(i,j))}{\gcd(i,j)},
\qquad
D_N=\operatorname{diag}(1,2,\ldots,N).
\]

\(Q_N\) is real and symmetric. It is **not** \(\widetilde Q_N(i,j)=1/\gcd(i,j)\). The diagonal matrix \(D_N\) is the arithmetic index matrix, not the graph-degree matrix that appears in \(H_N\).

The Mertens function is the partial sum of the Möbius function,

\[
M(N)=\sum_{n=1}^N\mu(n).
\]

## Diagonal identity

The diagonal of \(Q_N\) is \(Q_N(n,n)=\mu(n)/n\). Therefore

\[
(D_NQ_N)_{nn}=n\cdot\frac{\mu(n)}{n}=\mu(n),
\]

and

\[
\boxed{M(N)=\operatorname{Tr}(D_NQ_N).}
\]

The identity is the sum of the diagonal entries. Off-diagonal entries of \(Q_N\) do not enter.

## Spectral form

Let \(Q_Nv_j=\lambda_jv_j\) be an orthonormal eigenbasis. Then
\(Q_N=\sum_j\lambda_jv_jv_j^T\) and

\[
\operatorname{Tr}(D_NQ_N)
=\sum_{j=1}^N\lambda_j\,v_j^TD_Nv_j.
\]

Writing \(w_j=v_j^TD_Nv_j=\sum_{i=1}^N i\,(v_j)_i^2\),

\[
\boxed{
M(N)=\sum_{j=1}^N\lambda_j\,w_j.
}
\]

Because \(\|v_j\|_2=1\) and the index weights run from \(1\) to \(N\),

\[
1\le w_j\le N,
\qquad
\sum_{j=1}^N w_j=\operatorname{Tr}(D_N)=\frac{N(N+1)}{2}.
\]

The second identity is basis-independent: \(\sum_j v_jv_j^T=I\).

## Repeated eigenvalues

If \(\lambda\) has multiplicity greater than one, the individual \(w_j\) depend on the chosen orthonormal frame of the eigenspace. The invariant weight is the spectral projector \(P_\lambda\):

\[
w_\lambda=\operatorname{Tr}(D_NP_\lambda),
\qquad
M(N)=\sum_{\lambda\in\sigma(Q_N)}\lambda\,\operatorname{Tr}(D_NP_\lambda).
\]

## Alternative packagings (still the same identity)

1. **Congruence matrix.** Let \(A_N=D_N^{1/2}Q_ND_N^{1/2}\). Then \(\operatorname{Tr}(A_N)=M(N)\), so \(M(N)\) is the sum of the eigenvalues of \(A_N\). This removes the weights by folding \(D_N\) into the operator. It does not create an independent cancellation proof.

2. **Divisor-poset factorization.** Write \(f(n)=\mu(n)/n\) and \(g=f*\mu\), so
   \(g(n)=\sum_{d\mid n}(\mu(d)/d)\,\mu(n/d)\). On squarefree \(n\) this equals
   \(\mu(n)\prod_{p\mid n}(1+1/p)\); it need not vanish when \(n\) has a square
   factor. Then

   \[
   Q_N=B\operatorname{diag}(g)B^T,
   \qquad
   B_{ik}=\mathbf 1_{k\mid i}.
   \]

   The columns of \(B\) are not orthonormal, so this is not the eigen-decomposition. It does give the independent expansion

   \[
   \operatorname{Tr}(D_NQ_N)
   =\sum_{k=1}^N g(k)\,k\,\frac{m(m+1)}{2},
   \qquad
   m=\bigl\lfloor N/k\bigr\rfloor,
   \]

   which the software checks against \(M(N)\). The right-hand side is still a Möbius-oscillatory sum.

## Worked matrix \(Q_6\)

\(\mu(1),\ldots,\mu(6)=1,-1,-1,0,-1,1\), so \(M(6)=-1\). The stated kernel is

\[
Q_6=
\begin{pmatrix}
1 & 1 & 1 & 1 & 1 & 1 \\
1 & -1/2 & 1 & -1/2 & 1 & -1/2 \\
1 & 1 & -1/3 & 1 & 1 & -1/3 \\
1 & -1/2 & 1 & 0 & 1 & -1/2 \\
1 & 1 & 1 & 1 & -1/5 & 1 \\
1 & -1/2 & -1/3 & -1/2 & 1 & 1/6
\end{pmatrix}.
\]

The diagonal test is

\[
\operatorname{Tr}(D_6Q_6)
=1\cdot 1+2\cdot(-1/2)+3\cdot(-1/3)+4\cdot 0+5\cdot(-1/5)+6\cdot(1/6)
=-1.
\]

Locked numerically in `arith_qn.identity.q6_explicit` and `results/mertens_spectral/q6.json`.

## What this does not prove

The identities rewrite \(M(N)\). They do not bound \(M(N)\). Eigenvalue information without control of the index weights \(w_j\) (or of \(\operatorname{Tr}(D_NP_\lambda)\)) does not automatically give

\[
|M(N)|\le C_\varepsilon N^{1/2+\varepsilon}.
\]

That estimate is recorded as **OPEN** in [03 — Bounds](03-BOUNDS.md).
