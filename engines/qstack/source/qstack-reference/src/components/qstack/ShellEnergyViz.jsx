import React, { useState, useEffect, useCallback } from "react";
import { ML } from "./MathBlock";

const N_SHELLS = 10;
const BAND_HALF = 2; // m

function randomProfile(dominant = null) {
  const weights = Array.from({ length: N_SHELLS }, (_, i) => {
    const center = dominant ?? Math.floor(N_SHELLS / 2);
    const dist = Math.abs(i - center);
    return Math.max(0.01, Math.random() * Math.exp(-0.4 * dist));
  });
  const total = weights.reduce((a, b) => a + b, 0);
  return weights.map((w) => w / total);
}

function getJStar(weights) {
  return weights.indexOf(Math.max(...weights));
}

const SHELL_LABELS = Array.from({ length: N_SHELLS }, (_, i) => `j=${i + 1}`);
const COLORS = {
  normal: "#334155",
  active: "#22d3ee",
  danger: "#f59e0b",
  band: "rgba(34,211,238,0.15)",
};

export default function ShellEnergyViz() {
  const [weights, setWeights] = useState(() => randomProfile(4));
  const [q6On, setQ6On] = useState(true);
  const [animating, setAnimating] = useState(false);
  const [step, setStep] = useState(0);
  const [log, setLog] = useState([]);

  const jStar = getJStar(weights);
  const acCrit = 1 / N_SHELLS; // critical shell weight

  const isDangerous = weights[jStar] > acCrit * 2.5;

  const appendLog = useCallback((msg) => {
    setLog((prev) => [...prev.slice(-5), msg]);
  }, []);

  const tick = useCallback(() => {
    setWeights((prev) => {
      const js = getJStar(prev);
      let next = [...prev];

      // Cascade: energy flows toward dominant shell (simulated concentration)
      for (let i = 0; i < N_SHELLS; i++) {
        const dist = Math.abs(i - js);
        if (dist > 0) {
          const flow = 0.005 * prev[i] * Math.exp(-0.6 * dist);
          next[i] -= flow;
          next[js] += flow;
        }
      }

      // Add noise
      next = next.map((w) => Math.max(0.002, w + (Math.random() - 0.5) * 0.008));

      // Q6 damping
      if (q6On && prev[js] > acCrit * 2.0) {
        const excess = prev[js] - acCrit * 2.0;
        const damp = 0.12 * excess;
        for (let i = 0; i < N_SHELLS; i++) {
          if (Math.abs(i - js) <= BAND_HALF) {
            next[i] *= (1 - damp * Math.exp(-0.5 * Math.abs(i - js)));
          }
        }
        appendLog(`t=${step}: Q6 active on shell j=${js + 1}, damping ${(damp * 100).toFixed(1)}%`);
      }

      // Normalize
      const tot = next.reduce((a, b) => a + b, 0);
      return next.map((w) => w / tot);
    });
    setStep((s) => s + 1);
  }, [q6On, step, appendLog]);

  useEffect(() => {
    if (!animating) return;
    const id = setInterval(tick, 300);
    return () => clearInterval(id);
  }, [animating, tick]);

  const maxH = Math.max(...weights);

  return (
    <div className="space-y-6">
      <div className="mb-6">
        <h2 className="text-lg font-bold text-white">Shell Energy Visualizer</h2>
        <p className="text-xs text-gray-400 mt-1">
          Watch how Q6 damps the dominant shell when energy concentrates.{" "}
          <ML>{"a_j[u] = \\frac{2^{2j}\\|\\Delta_j u\\|_2^2}{\\sum_k 2^{2k}\\|\\Delta_k u\\|_2^2}"}</ML>
        </p>
      </div>

      {/* Controls */}
      <div className="flex flex-wrap items-center gap-3 mb-4">
        <button
          onClick={() => setAnimating((a) => !a)}
          className={`px-4 py-2 rounded text-xs font-bold tracking-wider uppercase border transition-colors ${
            animating
              ? "border-cyan-600 bg-cyan-900/30 text-cyan-300"
              : "border-gray-600 bg-gray-800/50 text-gray-300 hover:border-gray-400"
          }`}
        >
          {animating ? "⏸ Pause" : "▶ Simulate"}
        </button>
        <button
          onClick={() => {
            setWeights(randomProfile());
            setStep(0);
            setLog([]);
          }}
          className="px-4 py-2 rounded text-xs tracking-wider uppercase border border-gray-700 text-gray-400 hover:text-gray-200 transition-colors"
        >
          ↺ Reset
        </button>
        <button
          onClick={() => setWeights(randomProfile(4))}
          className="px-4 py-2 rounded text-xs tracking-wider uppercase border border-amber-800 text-amber-400 hover:bg-amber-900/20 transition-colors"
        >
          ⚡ Force Concentration
        </button>
        <label className="flex items-center gap-2 text-xs text-gray-400 cursor-pointer select-none ml-2">
          <div
            onClick={() => setQ6On((v) => !v)}
            className={`w-10 h-5 rounded-full relative transition-colors ${
              q6On ? "bg-cyan-700" : "bg-gray-700"
            }`}
          >
            <div
              className={`absolute top-0.5 w-4 h-4 rounded-full bg-white transition-all ${
                q6On ? "left-5" : "left-0.5"
              }`}
            />
          </div>
          Q6 Active
        </label>
      </div>

      {/* Bar Chart */}
      <div className="bg-[#0a0c12] border border-gray-800 rounded-lg p-5">
        <div className="flex items-end gap-1 h-48 mb-3">
          {weights.map((w, i) => {
            const inBand = Math.abs(i - jStar) <= BAND_HALF;
            const isDom = i === jStar;
            const height = `${Math.round((w / maxH) * 100)}%`;
            const danger = isDom && isDangerous;

            return (
              <div key={i} className="flex-1 flex flex-col items-center justify-end gap-1 h-full relative">
                {inBand && q6On && isDangerous && (
                  <div
                    className="absolute inset-0 rounded"
                    style={{ background: COLORS.band }}
                  />
                )}
                <div
                  className="w-full rounded-t transition-all duration-300 relative z-10"
                  style={{
                    height,
                    backgroundColor: danger
                      ? COLORS.danger
                      : isDom
                      ? COLORS.active
                      : inBand && q6On && isDangerous
                      ? "rgba(34,211,238,0.5)"
                      : COLORS.normal,
                    boxShadow: isDom ? `0 0 12px ${danger ? "#f59e0b88" : "#22d3ee88"}` : "none",
                  }}
                />
              </div>
            );
          })}
        </div>
        <div className="flex gap-1">
          {SHELL_LABELS.map((l, i) => (
            <div key={i} className="flex-1 text-center text-[9px] text-gray-600">
              {l}
            </div>
          ))}
        </div>

        {/* Legend */}
        <div className="flex flex-wrap gap-4 mt-4 text-[10px] text-gray-500">
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-cyan-400 inline-block" /> Dominant j*(t)</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-amber-400 inline-block" /> Danger zone</span>
          <span className="flex items-center gap-1"><span className="w-3 h-2 rounded inline-block" style={{ background: COLORS.band }} /> Q6 band</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-slate-700 inline-block" /> Normal</span>
        </div>
      </div>

      {/* Status Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
        <div className="bg-[#12151e] border border-gray-800 rounded p-3">
          <div className="text-gray-500 mb-1">Dominant shell</div>
          <div className="text-cyan-400 font-bold text-lg">j* = {jStar + 1}</div>
        </div>
        <div className="bg-[#12151e] border border-gray-800 rounded p-3">
          <div className="text-gray-500 mb-1">a_{jStar + 1}[u]</div>
          <div className={`font-bold text-lg ${isDangerous ? "text-amber-400" : "text-gray-200"}`}>
            {(weights[jStar] * 100).toFixed(1)}%
          </div>
        </div>
        <div className="bg-[#12151e] border border-gray-800 rounded p-3">
          <div className="text-gray-500 mb-1">Critical a_c</div>
          <div className="text-gray-300 font-bold text-lg">{(acCrit * 100).toFixed(1)}%</div>
        </div>
        <div className={`rounded p-3 border ${isDangerous && q6On ? "border-cyan-700 bg-cyan-950/30" : isDangerous ? "border-amber-700 bg-amber-950/30" : "bg-[#12151e] border-gray-800"}`}>
          <div className="text-gray-500 mb-1">Q6 status</div>
          <div className={`font-bold text-lg ${isDangerous && q6On ? "text-cyan-400" : isDangerous ? "text-amber-400" : "text-gray-600"}`}>
            {isDangerous && q6On ? "🔵 Active" : isDangerous ? "⚠️ Needed" : "● Dormant"}
          </div>
        </div>
      </div>

      {/* Log */}
      {log.length > 0 && (
        <div className="bg-[#0a0c12] border border-gray-800 rounded p-3 text-[10px] text-gray-500 font-mono space-y-1">
          {log.map((l, i) => (
            <div key={i} className="text-cyan-700">{l}</div>
          ))}
        </div>
      )}
    </div>
  );
}