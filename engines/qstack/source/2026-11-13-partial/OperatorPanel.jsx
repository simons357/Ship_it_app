import React from "react";
import { ML, MB } from "./MathBlock";

const OPERATORS = [
  {
    id: "Q1",
    color: "border-violet-500 text-violet-400",
    dot: "bg-violet-500",
    role: "Nonlinear damping / cascade absorber",
    desc: "Absorbs energy cascading from large scales to small, acting as a nonlinear sink that prevents unbounded enstrophy growth.",
    status: "active",
  },
  {
    id: "Q3",
    color: "border-amber-500 text-amber-400",
    dot: "bg-amber-500",
    role: "Middle-shell enstrophy stabilizer",
    desc: "Controls the enstrophy in the mid-frequency shells, bridging the gap between large-scale forcing and fine-scale dissipation.",
    status: "active",
  },
  {
    id: "Q6",
    color: "border-cyan-400 text-cyan-300",
    dot: "bg-cyan-400",
    role: "Adaptive dominant-shell spectral stabilizer",
    desc: "Watches the flow's dominant spectral shell and adds targeted damping only where energy is trying to concentrate dangerously. The enforcement mechanism of SND.",
    status: "primary",
    formula: "Q_6(u) = -\\lambda_H[u]\\, P_{\\mathcal{B}_H[u]}\\,u",
  },
  {
    id: "Q-N",
    color: "border-emerald-500 text-emerald-400",
    dot: "bg-emerald-500",
    role: "Full normalized shell-control architecture",
    desc: "The complete shell-weight normalization system acting across all dyadic shells up to N. Encompasses Q1, Q3, Q6 into a unified framework.",
    status: "active",
  },
];

export default function OperatorPanel() {
  return (
    <div className="space-y-6">
      <div className="mb-8">
        <h2 className="text-lg font-bold text-white mb-1">QStack Operator Architecture</h2>
        <p className="text-sm text-gray-400">
          Each operator targets a distinct role in the spectral stabilization hierarchy.
          Q6 is the adaptive hub — the operator version of the Spectral Non-Dispersal (SND) condition.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {OPERATORS.map((op) => (
          <div
            key={op.id}
            className={`rounded-lg border bg-[#12151e] p-5 ${
              op.status === "primary"
                ? "border-cyan-400/60 shadow-[0_0_24px_rgba(34,211,238,0.08)]"
                : "border-gray-800"
            }`}
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${op.dot}`} />
                <span className={`text-lg font-bold font-mono ${op.color.split(" ")[1]}`}>
                  {op.id}
                </span>
                {op.status === "primary" && (
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-cyan-900/40 text-cyan-400 border border-cyan-800 tracking-widest uppercase">
                    Focus
                  </span>
                )}
              </div>
            </div>
            <div className="text-xs text-gray-300 font-semibold mb-2">{op.role}</div>
            <div className="text-xs text-gray-500 mb-3 leading-relaxed">{op.desc}</div>
            {op.formula && (
              <div className="bg-[#0a0c12] border border-gray-800 rounded px-3 py-2 overflow-x-auto">
                <ML>{op.formula}</ML>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* SND Bridge */}
      <div className="mt-8 rounded-lg border border-gray-700 bg-[#12151e] p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">Strategic Story</div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center text-xs">
          <div className="bg-[#0d0f14] rounded p-3 border border-gray-800">
            <div className="text-amber-400 font-bold mb-1">SND</div>
            <div className="text-gray-400">The Rule</div>
            <div className="text-gray-600 text-[11px] mt-1">Spectral Non-Dispersal condition</div>
          </div>
          <div className="flex items-center justify-center text-gray-600 text-lg">⟹</div>
          <div className="bg-[#0d0f14] rounded p-3 border border-cyan-800/40">
            <div className="text-cyan-400 font-bold mb-1">Q6</div>
            <div className="text-gray-400">The Enforcement</div>
            <div className="text-gray-600 text-[11px] mt-1">Adaptive spectral damping operator</div>
          </div>
        </div>
        <div className="mt-4 text-xs text-gray-500 text-center">
          Q6 is the operator version of SND. If SND is the rule, Q6 is the enforcement mechanism.
        </div>
      </div>

      {/* Big theorem target */}
      <div className="rounded-lg border border-gray-700 bg-[#12151e] p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">Big Theorem Target</div>
        <MB>{"\\frac{d}{dt}H_N[a(t)] \\ge -C"}</MB>
        <div className="text-center text-gray-500 text-xs my-2">or stronger:</div>
        <MB>{"j_*(t) \\le J_0 \\quad \\forall\\, t \\ge 0"}</MB>
        <div className="text-xs text-gray-500 text-center mt-2">This is the SND bridge.</div>
      </div>
    </div>
  );
}
