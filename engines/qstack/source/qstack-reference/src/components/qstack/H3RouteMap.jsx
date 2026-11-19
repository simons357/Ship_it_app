import React from "react";
import { ML, MB } from "./MathBlock";

const Arrow = () => (
  <div className="flex items-center justify-center text-gray-600 text-xl my-2 md:my-0 md:mx-2">
    <span className="hidden md:block">⟹</span>
    <span className="md:hidden">⬇</span>
  </div>
);

const RouteStep = ({ label, formula, color = "gray", note }) => {
  const colors = {
    gray: "border-gray-700 bg-[#12151e]",
    cyan: "border-cyan-700/60 bg-cyan-950/10",
    amber: "border-amber-700/60 bg-amber-950/10",
    red: "border-red-800/60 bg-red-950/10",
    emerald: "border-emerald-700/60 bg-emerald-950/10",
  };
  const textColors = {
    gray: "text-gray-300",
    cyan: "text-cyan-300",
    amber: "text-amber-300",
    red: "text-red-400",
    emerald: "text-emerald-300",
  };
  return (
    <div className={`rounded-lg border p-4 ${colors[color]}`}>
      <div className={`text-xs font-bold uppercase tracking-widest mb-2 ${textColors[color]}`}>
        {label}
      </div>
      <div className="overflow-x-auto text-sm">
        <ML>{formula}</ML>
      </div>
      {note && <div className="text-[11px] text-gray-500 mt-2">{note}</div>}
    </div>
  );
};

export default function H3RouteMap() {
  return (
    <div className="space-y-8 max-w-3xl mx-auto">
      <div className="mb-8">
        <h2 className="text-lg font-bold text-white">H3 Energy-Observable Route</h2>
        <p className="text-xs text-gray-400 mt-1">
          The correct non-circular path from Leray energy to spectral gap persistence.
        </p>
      </div>

      {/* Wrong route */}
      <div className="rounded-lg border border-red-900/50 bg-red-950/10 p-5">
        <div className="text-xs text-red-400 uppercase tracking-widest mb-3 font-bold">❌ Dangerous Route (Circular)</div>
        <div className="flex flex-col md:flex-row items-center gap-2">
          <RouteStep label="Leray Energy" formula="\\|u\\|_{L^2}^2 + 2\\nu\\int_0^t \\|\\nabla u\\|_2^2" color="gray" />
          <Arrow />
          <RouteStep label="H^{2.3} Control" formula="\\|u(t)\\|_{H^{2.3}} \\le R_\\varepsilon" color="red"
            note="This regularity is not available for Leray-Hopf — it is the open problem." />
          <Arrow />
          <RouteStep label="H3 Goal" formula="\\|R_N(t)\\|_{\\mathrm{op}} < 0.20" color="red" />
        </div>
      </div>

      {/* Correct route */}
      <div className="rounded-lg border border-emerald-800/50 bg-emerald-950/10 p-5">
        <div className="text-xs text-emerald-400 uppercase tracking-widest mb-3 font-bold">✓ Correct Route (Non-Circular)</div>
        <div className="flex flex-col md:flex-row items-center gap-2 flex-wrap">
          <RouteStep
            label="Leray Energy"
            formula="\\|u\\|_{L_t^\\infty L_x^2} \\cap L_t^2 \\dot H_x^1"
            color="gray"
          />
          <Arrow />
          <RouteStep
            label="Shell Simplex"
            formula="a(t) \\in \\Delta_N"
            color="amber"
            note="Normalized shell weights live in a compact simplex — no regularity required."
          />
          <Arrow />
          <RouteStep
            label="SND + Coefficient Cage"
            formula="\\|a(t) - \\mu\\|_{\\ell^1} \\le \\eta_N"
            color="cyan"
            note="SND enforced by Q6."
          />
          <Arrow />
          <RouteStep
            label="H3 Goal"
            formula="\\|R_N(t)\\|_{\\mathrm{op}} < 0.20"
            color="emerald"
          />
        </div>
      </div>

      {/* Hierarchy box */}
      <div className="rounded-lg border border-gray-700 bg-[#12151e] p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-4">Refined Proof Hierarchy</div>
        <MB>
          {"\\mathrm{SND} \\Rightarrow \\|a(t)-\\mu\\|_{\\ell^1}\\le\\eta_N \\Rightarrow C_N\\eta_N<0.20 \\Rightarrow \\inf_{t\\ge0}\\lambda_{\\min}(H_N(t))>-\\tfrac{1}{2}"}
        </MB>
        <div className="text-xs text-gray-500 mt-3">
          The middle implication is complete by the Simplex Lipschitz Lemma.
          The remaining debt is proving SND implies the ℓ¹-tube condition.
        </div>
      </div>

      {/* Non-circular data */}
      <div className="rounded-lg border border-gray-700 bg-[#12151e] p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-4">Energy-Class Quantities (Non-Circular)</div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
          {[
            { label: "Global energy", formula: "\\|u(t)\\|_{L^2}" },
            { label: "Dissipation integral", formula: "\\int_0^t \\|\\nabla u\\|_2^2\\,d\\tau" },
            { label: "Shell projection", formula: "\\|P_j u(t)\\|_{L^2}" },
            { label: "Normalized weights", formula: "a_j[u] \\in \\Delta_N" },
          ].map((item) => (
            <div key={item.label} className="bg-[#0a0c12] border border-gray-800 rounded p-3">
              <div className="text-gray-500 mb-2">{item.label}</div>
              <ML>{item.formula}</ML>
            </div>
          ))}
        </div>
      </div>

      {/* H3 Boxed */}
      <div className="rounded-lg border border-cyan-700/50 bg-cyan-950/10 p-5">
        <div className="text-xs text-cyan-600 uppercase tracking-widest mb-3">Restated H3 Target (H3′)</div>
        <div className="text-sm text-cyan-200 leading-relaxed">
          <ML>{"\\gamma[u(t)]"}</ML> remains inside an explicitly certified coefficient cage whose operator radius is{" "}
          <ML>{"< 0.20"}</ML>.
        </div>
        <div className="text-xs text-gray-500 mt-3">
          Stronger than a vague stability assumption. Weaker than full regularity.
          The correct non-circular target.
        </div>
      </div>
    </div>
  );
}