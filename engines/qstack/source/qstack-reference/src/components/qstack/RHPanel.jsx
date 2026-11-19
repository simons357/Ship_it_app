import React, { useState } from "react";
import { ML, MB } from "./MathBlock";

const Section = ({ title, color = "gray", children }) => {
  const borders = {
    gray: "border-gray-700",
    cyan: "border-cyan-700/50",
    violet: "border-violet-700/50",
    amber: "border-amber-700/50",
    rose: "border-rose-700/50",
    emerald: "border-emerald-700/50",
  };
  const labels = {
    gray: "text-gray-500",
    cyan: "text-cyan-500",
    violet: "text-violet-400",
    amber: "text-amber-400",
    rose: "text-rose-400",
    emerald: "text-emerald-400",
  };
  return (
    <div className="mb-8">
      <div className={`text-xs uppercase tracking-widest mb-3 border-b pb-2 ${borders[color]} ${labels[color]}`}>
        {title}
      </div>
      {children}
    </div>
  );
};

const Callout = ({ color = "cyan", title, children }) => {
  const styles = {
    cyan: "border-cyan-800/50 bg-cyan-950/20 text-cyan-200",
    violet: "border-violet-800/50 bg-violet-950/20 text-violet-200",
    amber: "border-amber-800/50 bg-amber-950/20 text-amber-200",
    rose: "border-rose-800/50 bg-rose-950/20 text-rose-200",
    emerald: "border-emerald-800/50 bg-emerald-950/20 text-emerald-200",
    red: "border-red-800/50 bg-red-950/10 text-red-300",
  };
  return (
    <div className={`rounded-lg border p-4 text-xs leading-relaxed ${styles[color]}`}>
      {title && <div className="font-bold mb-1">{title}</div>}
      {children}
    </div>
  );
};

const ANALOGY_ROWS = [
  { ns: "Shell energy weight a_j[u]", rh: "Zero density near Re(s) = 1/2" },
  { ns: "Dominant shell j*(t)", rh: "Most-populated zero cluster" },
  { ns: "SND: energy stays spread", rh: "Zeros stay on the critical line" },
  { ns: "Q6 prevents concentration", rh: "No zero-free region collapse" },
  { ns: "Coefficient cage ‖Δγ_j‖ < 0.20", rh: "Uniform zero-spacing lower bound" },
  { ns: "Leray energy class", rh: "L² Mellin-transform class" },
];

const OPEN_ITEMS = [
  {
    id: "RH1",
    tag: "Core Conjecture",
    color: "rose",
    title: "Riemann Hypothesis",
    formula: "\\zeta(s) = 0,\\; \\operatorname{Re}(s)\\in(0,1) \\implies \\operatorname{Re}(s)=\\tfrac{1}{2}",
    note: "All non-trivial zeros of the Riemann zeta function lie on the critical line.",
  },
  {
    id: "RH2",
    tag: "Spectral Interpretation",
    color: "violet",
    title: "Hilbert–Pólya Operator",
    formula: "\\exists\\, T = T^*\\text{ self-adjoint on }L^2 :\\; \\sigma(T) = \\left\\{\\operatorname{Im}(\\rho):\\zeta(\\rho)=0\\right\\}",
    note: "If such a self-adjoint operator exists, RH follows immediately from spectral reality.",
  },
  {
    id: "RH3",
    tag: "Explicit Formula",
    color: "amber",
    title: "Prime Counting via Zeros",
    formula: "\\psi(x) = x - \\sum_{\\rho}\\frac{x^\\rho}{\\rho} - \\frac{\\zeta'(0)}{\\zeta(0)} - \\frac{1}{2}\\ln(1-x^{-2})",
    note: "Each zero ρ contributes an oscillatory term. RH bounds the error in prime distribution.",
  },
  {
    id: "RH4",
    tag: "Zero-Free Region",
    color: "emerald",
    title: "Classical Zero-Free Region",
    formula: "\\zeta(\\sigma+it) \\ne 0 \\text{ for } \\sigma > 1 - \\frac{c}{\\ln|t|},\\; |t|\\ge 2",
    note: "Best known classical bound. RH would replace the log factor with the sharp boundary Re(s) = 1/2.",
  },
  {
    id: "RH5",
    tag: "GUE Conjecture",
    color: "cyan",
    title: "Random Matrix / Correlation",
    formula: "\\lim_{T\\to\\infty}\\frac{1}{N(T)}\\#\\left\\{\\rho:\\operatorname{Im}(\\rho)\\in[T,T+L]\\right\\} \\sim \\text{GUE}_\\beta",
    note: "Zero spacings match eigenvalue statistics of random unitary matrices — a deep spectral analogy.",
  },
];

export default function RHPanel() {
  const [expanded, setExpanded] = useState("RH1");

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-2 h-2 rounded-full bg-violet-400 animate-pulse" />
          <span className="text-xs text-violet-400 tracking-widest uppercase">Millennium Problem</span>
        </div>
        <h2 className="text-lg font-bold text-white">Riemann Hypothesis</h2>
        <p className="text-xs text-gray-400 mt-1 leading-relaxed">
          Spectral operator-theoretic framing — with explicit analogies to the QStack / H3 approach.
        </p>
      </div>

      {/* Statement */}
      <Section title="The Statement" color="rose">
        <div className="bg-[#0a0c12] border border-rose-800/40 rounded-xl p-6 mb-4">
          <MB>{"\\zeta(s) = \\sum_{n=1}^{\\infty}\\frac{1}{n^s} = \\prod_{p\\text{ prime}}\\frac{1}{1-p^{-s}}"}</MB>
          <div className="text-xs text-gray-500 text-center mt-3">Euler product / Dirichlet series, valid for Re(s) &gt; 1</div>
        </div>
        <MB>{"\\text{RH: All non-trivial zeros }\\rho\\text{ satisfy }\\operatorname{Re}(\\rho)=\\tfrac{1}{2}"}</MB>
        <div className="mt-3 text-xs text-gray-500">
          Trivial zeros at s = −2, −4, −6, … are understood. The <em>non-trivial</em> zeros in the critical strip 0 &lt; Re(s) &lt; 1 are the open problem.
        </div>
      </Section>

      {/* Functional equation */}
      <Section title="Functional Equation (Symmetry)" color="violet">
        <MB>{"\\xi(s) := \\tfrac{1}{2}s(s-1)\\pi^{-s/2}\\Gamma(s/2)\\zeta(s) = \\xi(1-s)"}</MB>
        <div className="text-xs text-gray-400 mt-3 leading-relaxed">
          The completed zeta function ξ(s) is entire and symmetric about Re(s) = 1/2.
          This forces zeros to come in conjugate pairs: if ρ is a zero, so is 1−ρ̄.
          RH says all zeros sit exactly on the axis of symmetry.
        </div>
      </Section>

      {/* Expandable items */}
      <Section title="Key Formulas & Conjectures" color="cyan">
        <div className="space-y-3">
          {OPEN_ITEMS.map((item) => {
            const colorMap = {
              rose: { border: "border-rose-700/60", bg: "bg-rose-950/10", tag: "text-rose-400" },
              violet: { border: "border-violet-700/60", bg: "bg-violet-950/10", tag: "text-violet-400" },
              amber: { border: "border-amber-700/60", bg: "bg-amber-950/10", tag: "text-amber-400" },
              emerald: { border: "border-emerald-700/60", bg: "bg-emerald-950/10", tag: "text-emerald-400" },
              cyan: { border: "border-cyan-700/60", bg: "bg-cyan-950/10", tag: "text-cyan-400" },
            };
            const c = colorMap[item.color];
            const open = expanded === item.id;
            return (
              <div key={item.id} className={`rounded-lg border ${c.border} ${open ? c.bg : "bg-[#12151e]"}`}>
                <button
                  className="w-full px-5 py-4 flex items-center justify-between text-left"
                  onClick={() => setExpanded(open ? null : item.id)}
                >
                  <div className="flex items-center gap-3">
                    <span className={`text-xs font-bold uppercase tracking-widest ${c.tag}`}>{item.tag}</span>
                    <span className="text-sm text-gray-200">{item.title}</span>
                  </div>
                  <span className="text-gray-600 text-xs">{open ? "▲" : "▼"}</span>
                </button>
                {open && (
                  <div className="px-5 pb-5 space-y-3">
                    <MB>{item.formula}</MB>
                    <div className={`text-xs rounded border p-3 ${c.border} ${c.bg} ${c.tag}`}>{item.note}</div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </Section>

      {/* QStack Analogy Table */}
      <Section title="QStack / H3 Analogy" color="amber">
        <Callout color="amber" title="Structural Parallel">
          Both the H3 route and RH reduce to proving that a spectral distribution (shell weights vs. zeros)
          cannot concentrate — and that a quantitative gap prevents the dangerous clustering event.
        </Callout>
        <div className="mt-4 overflow-x-auto rounded-lg border border-gray-800">
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-gray-800">
                <th className="text-left px-4 py-3 text-gray-500 font-normal">Navier-Stokes / QStack</th>
                <th className="text-left px-4 py-3 text-gray-500 font-normal">Riemann Hypothesis</th>
              </tr>
            </thead>
            <tbody>
              {ANALOGY_ROWS.map((row, i) => (
                <tr key={i} className="border-b border-gray-800/50 hover:bg-[#12151e] transition-colors">
                  <td className="px-4 py-3 text-cyan-300/80 font-mono">{row.ns}</td>
                  <td className="px-4 py-3 text-violet-300/80 font-mono">{row.rh}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      {/* Operator-Theoretic Route */}
      <Section title="Operator-Theoretic Route to RH" color="violet">
        <div className="space-y-3">
          <Callout color="violet" title="Hilbert–Pólya Strategy">
            Find a self-adjoint operator T on a Hilbert space whose eigenvalues are exactly the imaginary parts
            of the non-trivial zeros. Self-adjoint ⟹ real eigenvalues ⟹ Re(ρ) = 1/2.
          </Callout>
          <MB>{"\\langle Tu,v\\rangle = \\langle u,Tv\\rangle \\implies \\sigma(T)\\subset\\mathbb{R}"}</MB>
          <Callout color="cyan" title="Berry–Keating Proposal">
            The operator H = xp + px (quantized classical Hamiltonian) on L²(ℝ⁺) has been proposed as a
            candidate. Its classical trajectories follow the flow x·ξ = E, with period matching prime counting.
          </Callout>
          <MB>{"H = xp + px = -i\\hbar\\left(x\\frac{d}{dx}+\\frac{1}{2}\\right)"}</MB>
          <div className="text-xs text-gray-500 mt-2">
            The spectrum of this operator matches the GUE distribution — but rigorously linking it to the
            actual zeros of ζ(s) remains open.
          </div>
        </div>
      </Section>

      {/* Consequence of RH */}
      <Section title="Consequences if True" color="emerald">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {[
            {
              title: "Prime Number Theorem sharpened",
              formula: "\\pi(x) = \\operatorname{Li}(x) + O(\\sqrt{x}\\ln x)",
              color: "emerald",
            },
            {
              title: "Cramér's conjecture (conditional)",
              formula: "p_{n+1}-p_n = O(\\ln^2 p_n)",
              color: "cyan",
            },
            {
              title: "Goldbach error bound",
              formula: "r(n) = \\frac{n}{2}C(n) + O(\\sqrt{n}\\ln n)",
              color: "violet",
            },
            {
              title: "L-function zero alignment",
              formula: "\\text{All Dirichlet L-functions: }\\operatorname{Re}(\\rho)=\\tfrac{1}{2}",
              color: "amber",
            },
          ].map((item) => {
            const bg = {
              emerald: "bg-emerald-950/15 border-emerald-800/40",
              cyan: "bg-cyan-950/15 border-cyan-800/40",
              violet: "bg-violet-950/15 border-violet-800/40",
              amber: "bg-amber-950/15 border-amber-800/40",
            };
            const tc = {
              emerald: "text-emerald-400",
              cyan: "text-cyan-400",
              violet: "text-violet-400",
              amber: "text-amber-400",
            };
            return (
              <div key={item.title} className={`rounded-lg border p-4 ${bg[item.color]}`}>
                <div className={`text-xs font-semibold mb-2 ${tc[item.color]}`}>{item.title}</div>
                <ML>{item.formula}</ML>
              </div>
            );
          })}
        </div>
      </Section>

      {/* Open debts */}
      <Section title="Open Debts (Parallel to H3)" color="rose">
        <div className="space-y-3">
          {[
            { n: "1", title: "Construct the Hilbert–Pólya operator explicitly", desc: "No candidate has been rigorously linked to ζ(s) zeros. Berry–Keating is heuristic only." },
            { n: "2", title: "Prove zero-spacing lower bound", desc: "A quantitative version of RH would give inf_n |γ_{n+1} − γ_n| > 0 — analogous to the coefficient cage in H3." },
            { n: "3", title: "Close the GUE / spectral gap connection", desc: "The Montgomery–Odlyzko law gives statistical evidence but no operator whose spectral measure equals the zero measure." },
            { n: "4", title: "Generalize to all L-functions", desc: "Grand Riemann Hypothesis: all automorphic L-functions have zeros only on Re(s) = 1/2." },
          ].map((s) => (
            <div key={s.n} className="flex gap-4 text-xs">
              <div className="w-6 h-6 rounded-full border border-rose-700/50 flex items-center justify-center text-rose-500 flex-shrink-0 mt-0.5">
                {s.n}
              </div>
              <div>
                <div className="text-gray-200 font-semibold mb-1">{s.title}</div>
                <div className="text-gray-500">{s.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );
}