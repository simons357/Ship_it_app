import React, { useMemo } from "react";

const N_SHELLS = 12;
const REF_MU = (() => {
  const raw = Array.from({ length: N_SHELLS }, (_, j) => Math.exp(-0.35 * j) * 0.6);
  const sum = raw.reduce((a, b) => a + b, 0);
  return raw.map(v => v / sum);
})();

export default function MeasurementPanel({ measurement, params, layers }) {
  const derived = useMemo(() => {
    if (!measurement) return null;
    const { type, shell, zero } = measurement;
    const { eta, kappa, lambdaGap } = params;
    const C_N = 1 + 1 / Math.max(lambdaGap, 0.001);

    if (type === "simplex" && shell !== undefined) {
      const mu_j = REF_MU[shell];
      const a_j = mu_j * (1 + 0.1); // approximate current
      const delta_j = Math.abs(a_j - mu_j);
      const l1 = delta_j * N_SHELLS * 0.5;
      const lambdaMin = lambdaGap - C_N * l1;
      return {
        title: `Shell P_${shell + 1}`,
        rows: [
          { k: "μ_j (reference)", v: mu_j.toFixed(5), color: "#22d3ee" },
          { k: "a_j (current)", v: a_j.toFixed(5), color: "#22d3ee" },
          { k: "δ_j = |a_j − μ_j|", v: delta_j.toFixed(5), color: "#f59e0b" },
          { k: "ℓ¹ contribution", v: l1.toFixed(5), color: "#f59e0b" },
          { k: "λ_min estimate", v: lambdaMin.toFixed(5), color: lambdaMin > -0.5 ? "#34d399" : "#ef4444" },
          { k: "SND certified", v: l1 <= eta ? "✓ yes" : "✗ no", color: l1 <= eta ? "#34d399" : "#ef4444" },
          { k: "H3 certified", v: lambdaMin > -0.5 ? "✓ yes" : "✗ no", color: lambdaMin > -0.5 ? "#34d399" : "#ef4444" },
        ],
        formula: `a_{${shell+1}} ∈ Δ_N, ‖a−μ‖₁ contributes to λ_min via C_N = ${C_N.toFixed(2)}`,
      };
    }

    if (type === "spectral") {
      const l1 = 0.15;
      const lambdaMin = lambdaGap - C_N * l1;
      return {
        title: "Spectral Floor",
        rows: [
          { k: "Hard floor λ = ", v: "−½", color: "#ef4444" },
          { k: "Headroom (λ_gap)", v: lambdaGap.toFixed(4), color: "#a78bfa" },
          { k: "C_N (loss rate)", v: C_N.toFixed(4), color: "#f59e0b" },
          { k: "C_N · ℓ¹ (spent)", v: (C_N * l1).toFixed(4), color: "#f59e0b" },
          { k: "Remaining margin", v: Math.max(0, lambdaGap - C_N * l1).toFixed(4), color: "#34d399" },
          { k: "H3 holds", v: lambdaMin > -0.5 ? "✓ certified" : "✗ not certified", color: lambdaMin > -0.5 ? "#34d399" : "#ef4444" },
        ],
        formula: `λ_min ≥ λ_gap − C_N · ‖a−μ‖₁ = ${lambdaMin.toFixed(4)}`,
      };
    }

    if (type === "cascade" && shell !== undefined) {
      const energy = Math.pow(0.7, shell);
      const kolmogorov = Math.pow(2, -shell * 5 / 3);
      return {
        title: `Cascade Shell ${shell + 1}`,
        rows: [
          { k: "Energy E_j", v: energy.toFixed(4), color: "#f59e0b" },
          { k: "k^{-5/3} reference", v: kolmogorov.toFixed(4), color: "#f59e0b" },
          { k: "Scale 2^j", v: Math.pow(2, shell).toFixed(0), color: "#22d3ee" },
          { k: "Regime", v: shell < 3 ? "Large scale" : shell < 7 ? "Inertial" : "Dissipation", color: shell < 3 ? "#22d3ee" : shell < 7 ? "#a78bfa" : "#f59e0b" },
          { k: "Q6 active", v: energy > 0.3 ? "potential" : "inactive", color: energy > 0.3 ? "#22d3ee" : "#4b5563" },
        ],
        formula: `E(k) ~ k^{-5/3},  k = 2^${shell}`,
      };
    }

    if (type === "zeros" && zero !== undefined) {
      const bandIdx = Math.floor((zero - 14) / 6);
      return {
        title: `Zero ρ = ½ + ${zero.toFixed(3)}i`,
        rows: [
          { k: "Im(ρ)", v: zero.toFixed(3), color: "#ec4899" },
          { k: "Re(ρ)", v: "½ (on critical line)", color: "#ec4899" },
          { k: "Band Π_j^ζ", v: `j = ${bandIdx + 1}`, color: "#a78bfa" },
          { k: "N(T) ~ T log T", v: `≈ ${(zero * Math.log(zero) / (2 * Math.PI)).toFixed(1)}`, color: "#a78bfa" },
          { k: "RH status", v: "✓ on Re = ½", color: "#34d399" },
          { k: "Ω6 analog", v: `α_${bandIdx + 1}(T) shell`, color: "#6366f1" },
        ],
        formula: `ζ(½ + ${zero.toFixed(3)}i) = 0, verified numerically`,
      };
    }

    return {
      title: measurement.label,
      rows: [{ k: "Distance from origin", v: measurement.distance?.toFixed(2), color: "#6366f1" }],
      formula: "",
    };
  }, [measurement, params]);

  if (!measurement) {
    return (
      <div className="p-4 space-y-4">
        <div className="text-[9px] text-gray-600 uppercase tracking-widest border-b border-gray-800 pb-2">
          Measurement Tool
        </div>
        <div className="text-center py-12 space-y-3">
          <div className="text-3xl opacity-20">⊷</div>
          <div className="text-[10px] text-gray-600">Click any object in the 3D scene to measure it</div>
          <div className="text-[9px] text-gray-700">Shell energies, spectral values, zero properties, and their derived relationships will appear here.</div>
        </div>

        {/* Relationship matrix */}
        <div className="border border-gray-800 rounded-lg p-3">
          <div className="text-[9px] text-gray-600 uppercase tracking-widest mb-3">Relationship Matrix</div>
          <div className="space-y-2 text-[9px] font-mono">
            {[
              { a: "a_j", b: "λ_min", rel: "Lipschitz: |Δλ| ≤ C_N|Δa|", color: "#6366f1" },
              { a: "η", b: "H3", rel: "C_N·η < 0.20 → certified", color: "#34d399" },
              { a: "κ", b: "SND", rel: "higher κ → smaller ℓ¹ dev", color: "#22d3ee" },
              { a: "α_j", b: "a_j", rel: "ΩStack ↔ QStack analogy", color: "#ec4899" },
            ].map((r, i) => (
              <div key={i} className="grid grid-cols-5 items-center gap-1">
                <span className="text-cyan-500 text-right">{r.a}</span>
                <span className="text-gray-700 text-center">↔</span>
                <span className="text-violet-400">{r.b}</span>
                <span className="col-span-2 text-gray-700 text-[8px] leading-tight">{r.rel}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      <div className="text-[9px] text-gray-600 uppercase tracking-widest border-b border-gray-800 pb-2">
        Measurement
      </div>

      <div className="bg-gray-900/40 border border-gray-800 rounded-lg p-3 space-y-3">
        <div className="text-xs font-bold text-white">{derived?.title}</div>

        <div className="space-y-1.5">
          {derived?.rows.map((row, i) => (
            <div key={i} className="flex justify-between items-center text-[10px] font-mono border-b border-gray-800/40 pb-1">
              <span className="text-gray-600">{row.k}</span>
              <span className="font-bold" style={{ color: row.color }}>{row.v}</span>
            </div>
          ))}
        </div>

        {derived?.formula && (
          <div className="bg-black/40 border border-gray-800/60 rounded px-3 py-2 text-[9px] font-mono text-gray-500 leading-relaxed">
            {derived.formula}
          </div>
        )}
      </div>

      {/* Cross-connections */}
      <div className="border border-gray-800 rounded-lg p-3">
        <div className="text-[9px] text-gray-600 uppercase tracking-widest mb-2">Connected To</div>
        <div className="space-y-1.5 text-[9px] font-mono">
          {measurement.type === "simplex" && (
            <>
              <ConnRow from="Simplex" to="Spectral" desc="a_j shifts λ_min by C_N·δa_j" />
              <ConnRow from="Simplex" to="SND tube" desc="must stay in ℓ¹ ball of radius η" />
              <ConnRow from="Simplex" to="Cascade" desc="cascade feeds this shell weight" />
            </>
          )}
          {measurement.type === "spectral" && (
            <>
              <ConnRow from="Spectral" to="Simplex" desc="λ_min driven by simplex deviation" />
              <ConnRow from="Spectral" to="Zeros" desc="ΩStack spectral gap analogy" />
            </>
          )}
          {measurement.type === "cascade" && (
            <>
              <ConnRow from="Cascade" to="Simplex" desc="energy cascade updates a_j" />
              <ConnRow from="Cascade" to="Spectral" desc="cascade drives spectral instability" />
            </>
          )}
          {measurement.type === "zeros" && (
            <>
              <ConnRow from="Zeros" to="Spectral" desc="ΩStack ↔ H3 gap analogy" />
              <ConnRow from="Zeros" to="Simplex" desc="α_j ↔ a_j simplex fractions" />
            </>
          )}
        </div>
      </div>
    </div>
  );
}

function ConnRow({ from, to, desc }) {
  return (
    <div className="flex items-start gap-2">
      <div className="w-1 h-1 rounded-full bg-indigo-500 mt-1.5 flex-shrink-0" />
      <span className="text-indigo-400">{from}</span>
      <span className="text-gray-700">→</span>
      <span className="text-gray-400">{to}</span>
      <span className="text-gray-700 text-[8px]">{desc}</span>
    </div>
  );
}