import React, { useState, useEffect, useRef, useCallback } from "react";
import { ML, MB } from "./MathBlock";

const N = 12;
const BAND = 2;
const CRIT = 1 / N;

function initWeights(dominant = 5) {
  const w = Array.from({ length: N }, (_, i) => {
    const d = Math.abs(i - dominant);
    return Math.max(0.005, Math.exp(-0.5 * d) * (0.5 + Math.random() * 0.5));
  });
  const s = w.reduce((a, b) => a + b, 0);
  return w.map((v) => v / s);
}

function jStar(w) { return w.indexOf(Math.max(...w)); }

export default function Q6DampingViz() {
  const [weights, setWeights] = useState(() => initWeights());
  const [q6On, setQ6On] = useState(true);
  const [running, setRunning] = useState(false);
  const [kappa, setKappa] = useState(0.18);
  const [theta, setTheta] = useState(1.5);
  const [events, setEvents] = useState([]);
  const [tick, setTick] = useState(0);
  const rafRef = useRef(null);
  const lastRef = useRef(0);

  const js = jStar(weights);
  const dominant = weights[js];
  const isDanger = dominant > CRIT * 2.2;
  const acNorm = (dominant / CRIT).toFixed(2);

  const appendEvent = useCallback((msg) => {
    setEvents((prev) => [{ t: Date.now(), msg }, ...prev].slice(0, 8));
  }, []);

  const step = useCallback(() => {
    setWeights((prev) => {
      const js = jStar(prev);
      let next = [...prev];

      // Nonlinear cascade: energy flows toward dominant shell
      for (let i = 0; i < N; i++) {
        if (i === js) continue;
        const d = Math.abs(i - js);
        const flow = 0.006 * prev[i] * Math.exp(-0.5 * d);
        next[i] -= flow;
        next[js] += flow;
      }

      // Stochastic perturbation
      next = next.map((v) => Math.max(0.003, v + (Math.random() - 0.49) * 0.006));

      // Q6 damping
      if (q6On && prev[js] > CRIT * 2.0) {
        const excess = (prev[js] / CRIT - 2.0) / 2.0;
        for (let i = 0; i < N; i++) {
          const d = Math.abs(i - js);
          if (d <= BAND) {
            const aj = prev[i] / CRIT;
            const lam = kappa * Math.pow(Math.max(0, aj - 1.0), theta);
            const decay = Math.exp(-0.5 * d);
            next[i] *= Math.max(0.01, 1 - lam * decay);
          }
        }
      }

      // Normalize
      const s = next.reduce((a, b) => a + b, 0);
      return next.map((v) => v / s);
    });
    setTick((t) => t + 1);
  }, [q6On, kappa, theta]);

  useEffect(() => {
    if (!running) return;
    const id = setInterval(step, 220);
    return () => clearInterval(id);
  }, [running, step]);

  // Log Q6 events
  useEffect(() => {
    if (isDanger && q6On) {
      appendEvent(`t=${tick} · Q6 fired on j=${js + 1} · a_j=${(dominant * 100).toFixed(1)}% · κ=${kappa}`);
    }
  }, [tick]);

  const reset = () => {
    setWeights(initWeights());
    setTick(0);
    setEvents([]);
  };

  const forceConcentration = () => {
    const w = Array.from({ length: N }, (_, i) => i === 5 ? 0.7 : 0.03 / (N - 1));
    const s = w.reduce((a, b) => a + b, 0);
    setWeights(w.map((v) => v / s));
  };

  const maxW = Math.max(...weights);

  // Per-shell λ_j computation (for display)
  const lambdas = weights.map((w, i) => {
    const d = Math.abs(i - js);
    if (d > BAND || !q6On) return 0;
    const aj = w / CRIT;
    return kappa * Math.pow(Math.max(0, aj - 1.0), theta);
  });
  const maxLam = Math.max(...lambdas, 0.001);

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <div className={`w-2 h-2 rounded-full ${isDanger && q6On ? "bg-cyan-400 animate-pulse" : isDanger ? "bg-amber-400 animate-pulse" : "bg-gray-600"}`} />
          <span className={`text-xs tracking-widest uppercase font-mono ${isDanger && q6On ? "text-cyan-400" : isDanger ? "text-amber-400" : "text-gray-500"}`}>
            {isDanger && q6On ? "Q6 Active — Damping" : isDanger ? "Concentration Detected — Q6 Off" : "Q6 Dormant"}
          </span>
        </div>
        <h2 className="text-lg font-bold text-white">Q6 Damping Visualizer</h2>
        <p className="text-xs text-gray-400 mt-1">
          Real-time per-shell damping coefficients <ML>{"\\lambda_j[u]"}</ML> with adaptive Q6.
        </p>
      </div>

      {/* Controls */}
      <div className="flex flex-wrap items-center gap-3">
        <button
          onClick={() => setRunning((r) => !r)}
          className={`px-4 py-2 rounded text-xs font-bold tracking-wider uppercase border transition-colors ${running ? "border-cyan-600 bg-cyan-900/30 text-cyan-300" : "border-gray-600 bg-gray-800/50 text-gray-300 hover:border-gray-400"}`}
        >
          {running ? "⏸ Pause" : "▶ Run"}
        </button>
        <button onClick={reset} className="px-4 py-2 rounded text-xs tracking-wider uppercase border border-gray-700 text-gray-400 hover:text-gray-200 transition-colors">
          ↺ Reset
        </button>
        <button onClick={forceConcentration} className="px-4 py-2 rounded text-xs tracking-wider uppercase border border-amber-800 text-amber-400 hover:bg-amber-900/20 transition-colors">
          ⚡ Concentrate
        </button>

        {/* Q6 Toggle */}
        <label className="flex items-center gap-2 text-xs text-gray-400 cursor-pointer select-none ml-auto">
          <div onClick={() => setQ6On((v) => !v)} className={`w-10 h-5 rounded-full relative transition-colors ${q6On ? "bg-cyan-700" : "bg-gray-700"}`}>
            <div className={`absolute top-0.5 w-4 h-4 rounded-full bg-white transition-all ${q6On ? "left-5" : "left-0.5"}`} />
          </div>
          Q6
        </label>
      </div>

      {/* Tuning */}
      <div className="grid grid-cols-2 gap-4 bg-[#0a0c12] border border-gray-800 rounded-lg p-4">
        <div>
          <div className="flex justify-between text-xs text-gray-500 mb-1">
            <span><ML>{"\\kappa_6"}</ML> (strength)</span>
            <span className="text-cyan-400 font-mono">{kappa.toFixed(2)}</span>
          </div>
          <input type="range" min={0.01} max={0.5} step={0.01} value={kappa} onChange={(e) => setKappa(parseFloat(e.target.value))} className="w-full accent-cyan-400" />
        </div>
        <div>
          <div className="flex justify-between text-xs text-gray-500 mb-1">
            <span><ML>{"\\theta"}</ML> (exponent)</span>
            <span className="text-amber-400 font-mono">{theta.toFixed(1)}</span>
          </div>
          <input type="range" min={0.5} max={4} step={0.1} value={theta} onChange={(e) => setTheta(parseFloat(e.target.value))} className="w-full accent-amber-400" />
        </div>
      </div>

      {/* Dual chart: energy + damping */}
      <div className="bg-[#0a0c12] border border-gray-800 rounded-lg p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-4">Shell Energy  <span className="text-cyan-600 ml-4">Q6 Damping λ_j</span></div>

        <div className="flex items-end gap-1 h-40 mb-1">
          {weights.map((w, i) => {
            const inBand = Math.abs(i - js) <= BAND;
            const isDom = i === js;
            const danger = isDom && isDanger;
            const hPct = Math.round((w / maxW) * 100);
            const lPct = Math.round((lambdas[i] / maxLam) * 100);

            return (
              <div key={i} className="flex-1 flex flex-col items-center justify-end h-full gap-0.5 relative">
                {/* Band highlight */}
                {inBand && q6On && isDanger && (
                  <div className="absolute inset-0 rounded" style={{ background: "rgba(34,211,238,0.07)" }} />
                )}
                {/* Damping overlay bar (behind) */}
                {lambdas[i] > 0 && (
                  <div
                    className="w-full rounded-t absolute bottom-0 opacity-40"
                    style={{ height: `${lPct}%`, backgroundColor: "#22d3ee", zIndex: 1 }}
                  />
                )}
                {/* Energy bar */}
                <div
                  className="w-full rounded-t transition-all duration-200 relative"
                  style={{
                    height: `${hPct}%`,
                    backgroundColor: danger ? "#f59e0b" : isDom ? "#22d3ee" : inBand && isDanger ? "rgba(34,211,238,0.5)" : "#334155",
                    boxShadow: isDom ? `0 0 10px ${danger ? "#f59e0b88" : "#22d3ee88"}` : "none",
                    zIndex: 2,
                  }}
                />
              </div>
            );
          })}
        </div>

        <div className="flex gap-1 mb-4">
          {Array.from({ length: N }, (_, i) => (
            <div key={i} className="flex-1 text-center text-[9px] text-gray-600 font-mono">
              {i + 1}
            </div>
          ))}
        </div>

        {/* Lambda row */}
        <div className="border-t border-gray-800 pt-3">
          <div className="text-[10px] text-gray-600 mb-2 font-mono">λ_j[u] per shell:</div>
          <div className="flex gap-1">
            {lambdas.map((l, i) => (
              <div key={i} className="flex-1 text-center">
                <div
                  className="text-[9px] font-mono transition-all"
                  style={{ color: l > 0.05 ? "#22d3ee" : l > 0 ? "#164e63" : "#1e293b" }}
                >
                  {l > 0.001 ? l.toFixed(2) : "·"}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap gap-4 mt-4 text-[10px] text-gray-500">
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-cyan-400 inline-block" /> Dominant j*</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-amber-400 inline-block" /> Danger</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-cyan-400/40 inline-block" /> Q6 damping overlay</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-slate-700 inline-block" /> Normal</span>
        </div>
      </div>

      {/* Status grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
        <div className="bg-[#12151e] border border-gray-800 rounded p-3">
          <div className="text-gray-500 mb-1">Dominant shell</div>
          <div className="text-cyan-400 font-bold text-lg font-mono">j* = {js + 1}</div>
        </div>
        <div className="bg-[#12151e] border border-gray-800 rounded p-3">
          <div className="text-gray-500 mb-1">a_{js+1} / a_c</div>
          <div className={`font-bold text-lg font-mono ${isDanger ? "text-amber-400" : "text-gray-200"}`}>
            {acNorm}×
          </div>
        </div>
        <div className="bg-[#12151e] border border-gray-800 rounded p-3">
          <div className="text-gray-500 mb-1">Max λ_j</div>
          <div className={`font-bold text-lg font-mono ${maxLam > 0.05 ? "text-cyan-400" : "text-gray-600"}`}>
            {maxLam.toFixed(3)}
          </div>
        </div>
        <div className={`rounded p-3 border ${isDanger && q6On ? "border-cyan-700 bg-cyan-950/30" : isDanger ? "border-amber-700 bg-amber-950/20" : "bg-[#12151e] border-gray-800"}`}>
          <div className="text-gray-500 mb-1">Q6 status</div>
          <div className={`font-bold text-lg font-mono ${isDanger && q6On ? "text-cyan-400" : isDanger ? "text-amber-400" : "text-gray-600"}`}>
            {isDanger && q6On ? "🔵 Active" : isDanger ? "⚠️ Needed" : "● Dormant"}
          </div>
        </div>
      </div>

      {/* Q6 formula */}
      <div className="rounded-lg border border-gray-700 bg-[#12151e] p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">Active Formula</div>
        <MB>{"Q_6(u) = -\\sum_j \\lambda_j[u]\\,\\Delta_j u"}</MB>
        <div className="mt-3">
          <MB>{"\\lambda_j[u] = \\kappa_6\\;\\chi_{\\{|j-j_*|\\le m\\}}\\left(\\frac{a_j[u]}{a_c}\\right)^\\theta"}</MB>
        </div>
        <div className="mt-3 text-xs text-gray-600">
          κ₆ = {kappa.toFixed(2)} &nbsp;·&nbsp; θ = {theta.toFixed(1)} &nbsp;·&nbsp; m = {BAND} &nbsp;·&nbsp; a_c = 1/N = {(CRIT).toFixed(3)}
        </div>
      </div>

      {/* Event log */}
      {events.length > 0 && (
        <div className="bg-[#0a0c12] border border-gray-800 rounded p-3 space-y-1">
          <div className="text-[10px] text-gray-600 uppercase tracking-widest mb-2">Q6 Event Log</div>
          {events.map((e, i) => (
            <div key={i} className="text-[10px] font-mono text-cyan-700">{e.msg}</div>
          ))}
        </div>
      )}
    </div>
  );
}