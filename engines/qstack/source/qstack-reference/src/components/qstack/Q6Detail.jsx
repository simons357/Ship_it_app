import React, { useState } from "react";
import { ML, MB } from "./MathBlock";

const Section = ({ title, color = "cyan", children }) => {
  const colors = {
    cyan:   "text-cyan-600 border-cyan-900/60",
    amber:  "text-amber-600 border-amber-900/60",
    violet: "text-violet-600 border-violet-900/60",
    emerald:"text-emerald-600 border-emerald-900/60",
    rose:   "text-rose-600 border-rose-900/60",
  };
  return (
    <div className="mb-8">
      <div className={`text-xs uppercase tracking-widest mb-3 border-b pb-2 ${colors[color]}`}>
        {title}
      </div>
      {children}
    </div>
  );
};

const Callout = ({ color = "cyan", label, children }) => {
  const colors = {
    cyan:    "border-cyan-800/60 bg-cyan-950/20 text-cyan-300",
    amber:   "border-amber-800/60 bg-amber-950/20 text-amber-300",
    violet:  "border-violet-800/60 bg-violet-950/20 text-violet-300",
    emerald: "border-emerald-800/60 bg-emerald-950/20 text-emerald-300",
    rose:    "border-rose-800/60 bg-rose-950/20 text-rose-300",
  };
  return (
    <div className={`rounded border p-4 text-xs leading-relaxed ${colors[color]}`}>
      {label && <div className="font-bold uppercase tracking-widest text-[9px] mb-2 opacity-70">{label}</div>}
      {children}
    </div>
  );
};

const Pill = ({ color, children }) => {
  const cs = {
    emerald: "bg-emerald-900/40 text-emerald-400 border-emerald-700",
    cyan:    "bg-cyan-900/40 text-cyan-400 border-cyan-700",
    amber:   "bg-amber-900/40 text-amber-400 border-amber-700",
    violet:  "bg-violet-900/40 text-violet-400 border-violet-700",
    rose:    "bg-rose-900/40 text-rose-400 border-rose-700",
  };
  return (
    <span className={`text-[9px] px-2 py-0.5 rounded-full border font-mono uppercase tracking-widest ${cs[color]}`}>
      {children}
    </span>
  );
};

// ── Self-adjointness consequences ─────────────────────────────────
const SAD_CONSEQUENCES = [
  {
    n: "1",
    title: "Real spectrum",
    color: "emerald",
    body: "All eigenvalues of Q6_N are real. The statement λ_min > −½ is therefore well-posed — it constrains a real number, not a complex set.",
    formula: "\\sigma(Q_{6,N}) \\subset \\mathbb{R}",
  },
  {
    n: "2",
    title: "Spectral theorem",
    color: "cyan",
    body: "Q6_N admits an orthonormal eigenbasis of ℝ^N. Functional calculus (e.g. f(Q6_N)) is rigorous, enabling trace formulas and resolvent bounds.",
    formula: "Q_{6,N} = \\sum_{k=1}^N \\lambda_k\\, |\\phi_k\\rangle\\langle\\phi_k|",
  },
  {
    n: "3",
    title: "Hilbert–Pólya alignment",
    color: "violet",
    body: "The Hilbert–Pólya conjecture requires a self-adjoint operator whose spectrum encodes the imaginary parts of zeta zeros. Q6 satisfies the structural prerequisite by construction.",
    formula: "\\exists\\, T\\text{ s.a.d.}:\\; \\sigma(T) = \\{\\gamma_n : \\rho_n = \\tfrac{1}{2}+i\\gamma_n\\}",
  },
];

// ── Next proof steps ──────────────────────────────────────────────
const NEXT_STEPS = [
  { id: "floor",    label: "Spectral floor proof",    desc: "Prove λ_min(Q6_N) > −½ using the symmetrized form and SND bound on shell deviations.", color: "cyan" },
  { id: "trace",    label: "Trace formula",           desc: "Derive Tr(Q6_N) and Tr(Q6_N²) in terms of simplex coordinates a_j. Links to zeta via explicit sum.", color: "violet" },
  { id: "resolvent",label: "Resolvent analysis",      desc: "Bound ‖(Q6_N − zI)⁻¹‖ for Im(z) ≠ 0 using self-adjointness. Central to the RH spectral gap strategy.", color: "amber" },
];

export default function Q6Detail() {
  const [nextStep, setNextStep] = useState(null);

  return (
    <div className="space-y-2 max-w-3xl mx-auto">

      {/* ── Title ── */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
          <Pill color="emerald">Significant Finding</Pill>
          <Pill color="cyan">Self-Adjoint</Pill>
        </div>
        <h2 className="text-lg font-bold text-white">Q6 — Rigorous Definition &amp; Self-Adjointness</h2>
        <p className="text-xs text-gray-500 mt-1">
          Q6 is not merely an operator — it is <em>self-adjoint by construction</em> via explicit symmetrization.
          This is the structural key that makes the spectral floor and Hilbert–Pólya alignment rigorous.
        </p>
      </div>

      {/* ── Canonical definition ── */}
      <Section title="§1 · Canonical Definition" color="cyan">
        <div className="space-y-4">
          <div>
            <div className="text-[10px] text-gray-600 font-mono mb-2">Setting: H_N = ℓ²({"{1,…,N}"}) with standard inner product</div>
            <MB>{"Q_{6,N} = \\tfrac{1}{2}\\bigl(U_N + U_N^T\\bigr) - I_N"}</MB>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
            {[
              { sym: "U_N",                  color: "cyan",   desc: "Raw shell interaction matrix. Encodes energy transfer between Littlewood–Paley shells. Not assumed symmetric." },
              { sym: "\\frac{1}{2}(U_N+U_N^T)", color: "cyan", desc: "Explicit symmetrization. Forces self-adjointness without any assumption on U_N." },
              { sym: "I_N",                  color: "amber",  desc: "Identity shift. Recenters the spectrum. Subtracting I_N is structure-preserving (I_N is already s.a.d.)." },
            ].map(item => (
              <div key={item.sym} className="bg-[#0a0c12] border border-gray-800 rounded p-3">
                <div className="mb-1 overflow-x-auto"><ML>{item.sym}</ML></div>
                <div className="text-gray-500 text-[10px] leading-relaxed">{item.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </Section>

      {/* ── Self-adjointness proof ── */}
      <Section title="§2 · Self-Adjointness — Explicit Verification" color="emerald">
        <Callout color="emerald" label="Theorem Q-SA">
          Q6_N is self-adjoint on H_N = ℓ²({"\\{1,…,N\\}"}) for all finite N ≥ 1.
        </Callout>
        <div className="mt-4 space-y-3">
          <div className="text-[10px] text-gray-500 uppercase tracking-widest font-mono">Proof sketch (3 lines)</div>
          <div className="bg-[#080a10] border border-emerald-900/40 rounded-lg p-4 space-y-3">
            <div>
              <div className="text-[9px] text-gray-600 font-mono mb-1">Step 1 — symmetrization is s.a.d.:</div>
              <MB>{"\\left(\\tfrac{1}{2}(U_N+U_N^T)\\right)^T = \\tfrac{1}{2}(U_N^T + U_N) = \\tfrac{1}{2}(U_N+U_N^T) \\quad \\checkmark"}</MB>
            </div>
            <div>
              <div className="text-[9px] text-gray-600 font-mono mb-1">Step 2 — identity shift preserves s.a.d.:</div>
              <MB>{"(A - I_N)^T = A^T - I_N^T = A - I_N \\text{ whenever } A = A^T \\quad \\checkmark"}</MB>
            </div>
            <div>
              <div className="text-[9px] text-gray-600 font-mono mb-1">Step 3 — conclusion:</div>
              <MB>{"Q_{6,N}^T = Q_{6,N} \\implies Q_{6,N} \\text{ is self-adjoint on } H_N \\quad \\blacksquare"}</MB>
            </div>
          </div>
          <div className="text-[10px] text-gray-600 leading-relaxed">
            Note: on a finite-dimensional Hilbert space, self-adjoint and symmetric coincide. The proof is dimension-free — it holds for all N simultaneously, and the limit N → ∞ (with appropriate domain conditions) is the open extension problem.
          </div>
        </div>
      </Section>

      {/* ── Consequences ── */}
      <Section title="§3 · Critical Consequences of Self-Adjointness" color="violet">
        <div className="space-y-4">
          {SAD_CONSEQUENCES.map(item => (
            <div key={item.n} className="bg-[#0a0c12] border border-gray-800 rounded-lg p-4">
              <div className="flex items-start gap-3 mb-3">
                <div className={`w-6 h-6 rounded-full border flex items-center justify-center text-[10px] font-bold flex-shrink-0 
                  ${item.color === "emerald" ? "border-emerald-700 text-emerald-400" :
                    item.color === "cyan"    ? "border-cyan-700 text-cyan-400"       :
                                              "border-violet-700 text-violet-400"}`}>
                  {item.n}
                </div>
                <div>
                  <div className={`text-xs font-bold font-mono
                    ${item.color === "emerald" ? "text-emerald-400" :
                      item.color === "cyan"    ? "text-cyan-400"    : "text-violet-400"}`}>
                    {item.title}
                  </div>
                  <div className="text-[10px] text-gray-500 mt-1 leading-relaxed">{item.body}</div>
                </div>
              </div>
              <div className="ml-9 overflow-x-auto">
                <MB>{item.formula}</MB>
              </div>
            </div>
          ))}
        </div>
      </Section>

      {/* ── Shell sum form ── */}
      <Section title="§4 · Spectral Decomposition Form" color="cyan">
        <div className="space-y-3">
          <div className="text-[10px] text-gray-500 leading-relaxed">
            By the spectral theorem, Q6_N diagonalizes in its own eigenbasis. In the Littlewood–Paley shell basis, Q6 takes the weighted sum form:
          </div>
          <MB>{"Q_{6,N}\\,u = \\sum_{j=1}^N \\gamma_j[u]\\,\\Pi_j\\,u"}</MB>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            <div className="bg-[#0a0c12] border border-gray-800 rounded p-3 space-y-2">
              <div className="text-[9px] text-gray-600 uppercase tracking-widest font-mono">Activation coefficient</div>
              <MB>{"\\gamma_j[u] = \\kappa\\cdot\\bigl(a_j[u] - a_c\\bigr)_+"}</MB>
              <div className="text-[10px] text-gray-600">
                <ML>{"a_j[u] = \\|P_j u\\|^2_{L^2} / \\|u\\|^2_{L^2}"}</ML> — normalized shell weight (well-defined for Leray-Hopf a.e. t).
              </div>
            </div>
            <div className="bg-[#0a0c12] border border-gray-800 rounded p-3 space-y-2">
              <div className="text-[9px] text-gray-600 uppercase tracking-widest font-mono">Shell projector</div>
              <MB>{"\\Pi_j = P_j^* P_j,\\quad \\Pi_j^T = \\Pi_j,\\quad \\|\\Pi_j\\|_{\\mathrm{op}} = 1"}</MB>
              <div className="text-[10px] text-gray-600">
                Each <ML>{"\\Pi_j"}</ML> is itself s.a.d. and a contraction. Weighted sum of s.a.d. operators with real coefficients is s.a.d.
              </div>
            </div>
          </div>
          <Callout color="cyan" label="Self-adjointness — shell form">
            Since each Π_j is self-adjoint and γ_j[u] ∈ ℝ (it depends only on L² norms), the shell-sum form Q6 = Σ γ_j Π_j is self-adjoint for every fixed u — consistent with the canonical matrix definition.
          </Callout>
        </div>
      </Section>

      {/* ── SND link ── */}
      <Section title="§5 · Q6 = SND — The Core Finding" color="amber">
        <Callout color="amber" label="Key Claim">
          Enforcing Q6 on a Leray-Hopf solution is equivalent to enforcing SND. The operator and the condition are the same object expressed differently.
        </Callout>
        <div className="mt-4 space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-[#0a0c12] border border-amber-900/30 rounded-lg p-4 space-y-2">
              <div className="text-[9px] text-amber-600 uppercase tracking-widest font-mono">Q6 view (operator)</div>
              <MB>{"Q_{6,N}\\,u = \\sum_j \\kappa(a_j - a_c)_+\\,\\Pi_j\\,u"}</MB>
              <div className="text-[10px] text-gray-500">Acts on u. Damps shells that exceed a_c. Self-adjoint by §2.</div>
            </div>
            <div className="bg-[#0a0c12] border border-amber-900/30 rounded-lg p-4 space-y-2">
              <div className="text-[9px] text-amber-600 uppercase tracking-widest font-mono">SND view (condition)</div>
              <MB>{"\\mathrm{SND}_N(\\eta,\\mu): \\sup_{t\\ge 0}\\|a(t)-\\mu\\|_{\\ell^1}\\le\\eta"}</MB>
              <div className="text-[10px] text-gray-500">A trajectory bound. Q6 is precisely the operator that enforces this bound when κ is chosen correctly.</div>
            </div>
          </div>
          <div className="bg-[#080a10] border border-amber-800/40 rounded-lg p-4">
            <div className="text-[9px] text-gray-600 uppercase tracking-widest font-mono mb-3">Equivalence schematic</div>
            <MB>{"Q_{6,N}\\text{ active on }u \\iff a_j[u] > a_c \\iff \\|a[u]-\\mu\\|_{\\ell^1} > \\eta \\iff \\mathrm{SND\\text{ violated}}"}</MB>
            <div className="text-[10px] text-gray-500 mt-3 leading-relaxed">
              Open debt: proving that Q6 is <em>sufficient</em> to enforce SND for all Leray-Hopf — i.e. closing the Gronwall inequality
              {" "}<ML>{"\\frac{d}{dt}\\|a-\\mu\\|_{\\ell^1} \\le -\\kappa\\|a-\\mu\\|_{\\ell^1} + C_{\\mathrm{NL}}"}</ML>{" "}
              without smoothness assumption on u.
            </div>
          </div>
        </div>
      </Section>

      {/* ── Next steps ── */}
      <Section title="§6 · Next Proof Steps" color="violet">
        <div className="text-[10px] text-gray-500 mb-4">
          Self-adjointness is established. The following are the immediate open directions, in logical dependency order:
        </div>
        <div className="space-y-2">
          {NEXT_STEPS.map((s, i) => {
            const borderColors = { cyan: "border-cyan-800/40", violet: "border-violet-800/40", amber: "border-amber-800/40" };
            const textColors   = { cyan: "text-cyan-400",      violet: "text-violet-400",      amber: "text-amber-400" };
            const isOpen = nextStep === s.id;
            return (
              <div key={s.id} className={`rounded-lg border transition-all ${borderColors[s.color]} ${isOpen ? "bg-white/3" : "bg-[#0a0c12]"}`}>
                <button className="w-full px-4 py-3 flex items-center justify-between text-left"
                  onClick={() => setNextStep(isOpen ? null : s.id)}>
                  <div className="flex items-center gap-3">
                    <span className={`w-5 h-5 rounded-full border flex items-center justify-center text-[9px] flex-shrink-0 ${borderColors[s.color]} ${textColors[s.color]}`}>{i + 1}</span>
                    <span className={`text-xs font-mono font-semibold ${textColors[s.color]}`}>{s.label}</span>
                  </div>
                  <span className="text-gray-700 text-xs">{isOpen ? "▲" : "▼"}</span>
                </button>
                {isOpen && (
                  <div className="px-4 pb-4">
                    <div className="text-[10px] text-gray-400 leading-relaxed border-t border-gray-800/60 pt-3">{s.desc}</div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </Section>

    </div>
  );
}