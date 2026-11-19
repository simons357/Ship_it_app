import React, { useState, useEffect, useCallback } from "react";
import { ML, MB } from "../qstack/MathBlock";

// Known RH zeros (imaginary parts of first zeros of ζ)
const KNOWN_ZEROS = [14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327, 48.005, 49.774,
  52.970, 56.446, 59.347, 60.832, 65.113, 67.080, 69.546, 72.067, 75.705, 77.145];

const N_SHELLS = 10;
const SHELL_HEIGHT = 8; // imaginary part units per shell
const DELTA0 = 0.20;

function initZeros() {
  // Place known zeros on critical line + small perturbation for visualization
  return KNOWN_ZEROS.slice(0, N_SHELLS * 2).map((t, i) => ({
    id: i,
    t,
    re: 0.5 + (Math.random() - 0.5) * 0.04, // near 1/2
    shell: Math.floor(t / SHELL_HEIGHT),
    active: true,
  }));
}

export default function ZeroShellViz() {
  const [zeros, setZeros] = useState(initZeros);
  const [omega6On, setOmega6On] = useState(true);
  const [running, setRunning] = useState(false);
  const [kappa, setKappa] = useState(0.15);
  const [tick, setTick] = useState(0);
  const [events, setEvents] = useState([]);

  // Compute alpha_j (normalized zero density per shell)
  const shellCounts = Array.from({ length: N_SHELLS }, (_, j) =>
    zeros.filter((z) => z.active && z.shell === j).length
  );
  const totalZeros = shellCounts.reduce((a, b) => a + b, 0) || 1;
  const alpha = shellCounts.map((c) => c / totalZeros);
  const alphaCrit = 1 / N_SHELLS;
  const maxAlpha = Math.max(...alpha);
  const dominantShell = alpha.indexOf(maxAlpha);
  const maxDev = Math.max(...zeros.filter((z) => z.active).map((z) => Math.abs(z.re - 0.5)));
  const rhBound = maxDev * 5; // scaled to [0,1] range for comparison with delta0

  const isDanger = maxDev > 0.08;
  const rhMet = maxDev < 0.04;

  const step = useCallback(() => {
    setZeros((prev) => {
      let next = prev.map((z) => {
        if (!z.active) return z;
        // Brownian drift toward or away from critical line
        let newRe = z.re + (Math.random() - 0.49) * 0.012;

        // Omega6 repulsion: push zeros back toward Re=1/2 when off-axis
        if (omega6On && Math.abs(z.re - 0.5) > 0.06) {
          const force = kappa * (0.5 - z.re);
          newRe += force;
        }

        // Clamp to strip
        newRe = Math.max(0.3, Math.min(0.7, newRe));
        return { ...z, re: newRe };
      });
      return next;
    });
    setTick((t) => t + 1);
  }, [omega6On, kappa]);

  useEffect(() => {
    if (!running) return;
    const id = setInterval(step, 180);
    return () => clearInterval(id);
  }, [running, step]);

  useEffect(() => {
    if (isDanger && omega6On) {
      setEvents((prev) => [
        { msg: `t=${tick} · Ω6 fired · max|Re(ρ)−½|=${maxDev.toFixed(4)} · κ=${kappa}` },
        ...prev,
      ].slice(0, 8));
    }
  }, [tick]);

  const reset = () => {
    setZeros(initZeros());
    setTick(0);
    setEvents([]);
  };

  const perturb = () => {
    setZeros((prev) =>
      prev.map((z) => ({ ...z, re: z.re + (Math.random() - 0.5) * 0.25 }))
    );
  };

  // Scatter plot: x = Re(ρ), y = Im(ρ) (imaginary part)
  const W = 320, H = 220;
  const reToX = (re) => ((re - 0.25) / 0.5) * W;
  const imToY = (im) => H - ((im - 10) / 70) * H;

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div className="mb-4">
        <div className="flex items-center gap-3 mb-2">
          <div className={`w-2 h-2 rounded-full ${isDanger && omega6On ? "bg-violet-400 animate-pulse" : isDanger ? "bg-amber-400 animate-pulse" : "bg-gray-600"}`} />
          <span className={`text-xs tracking-widest uppercase font-mono ${isDanger && omega6On ? "text-violet-400" : isDanger ? "text-amber-400" : "text-gray-500"}`}>
            {isDanger && omega6On ? "Ω6 Active — Zero Repulsion" : isDanger ? "Off-Axis Drift Detected" : "Zeros On Critical Line"}
          </span>
        </div>
        <h2 className="text-lg font-bold text-white">Zero-Shell Visualizer</h2>
        <p className="text-xs text-gray-400 mt-1">
          Critical strip: Re(s) ∈ [¼, ¾]. Zeros drift toward/away from Re(s) = ½. Ω6 repels them back.
        </p>
      </div>

      {/* Controls */}
      <div className="flex flex-wrap items-center gap-3">
        <button onClick={() => setRunning((r) => !r)}
          className={`px-4 py-2 rounded text-xs font-bold tracking-wider uppercase border transition-colors ${running ? "border-violet-600 bg-violet-900/30 text-violet-300" : "border-gray-600 bg-gray-800/50 text-gray-300 hover:border-gray-400"}`}>
          {running ? "⏸ Pause" : "▶ Run"}
        </button>
        <button onClick={reset} className="px-4 py-2 rounded text-xs tracking-wider uppercase border border-gray-700 text-gray-400 hover:text-gray-200 transition-colors">
          ↺ Reset
        </button>
        <button onClick={perturb} className="px-4 py-2 rounded text-xs tracking-wider uppercase border border-amber-800 text-amber-400 hover:bg-amber-900/20 transition-colors">
          ⚡ Perturb
        </button>
        <label className="flex items-center gap-2 text-xs text-gray-400 cursor-pointer select-none ml-auto">
          <div onClick={() => setOmega6On((v) => !v)} className={`w-10 h-5 rounded-full relative transition-colors ${omega6On ? "bg-violet-700" : "bg-gray-700"}`}>
            <div className={`absolute top-0.5 w-4 h-4 rounded-full bg-white transition-all ${omega6On ? "left-5" : "left-0.5"}`} />
          </div>
          Ω6
        </label>
      </div>

      {/* κ slider */}
      <div className="bg-[#0a0c12] border border-gray-800 rounded-lg p-4">
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span><ML>{"\\kappa_\\Omega"}</ML> (repulsion strength)</span>
          <span className="text-violet-400 font-mono">{kappa.toFixed(2)}</span>
        </div>
        <input type="range" min={0.01} max={0.5} step={0.01} value={kappa} onChange={(e) => setKappa(parseFloat(e.target.value))} className="w-full accent-violet-400" />
      </div>

      {/* Critical strip scatter */}
      <div className="bg-[#0a0c12] border border-gray-800 rounded-lg p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">Critical Strip — Zero Positions</div>
        <div className="relative overflow-hidden rounded" style={{ width: "100%", paddingBottom: "60%" }}>
          <svg
            viewBox={`0 0 ${W} ${H}`}
            className="absolute inset-0 w-full h-full"
            style={{ background: "#080a10" }}
          >
            {/* Critical line Re=1/2 */}
            <line x1={reToX(0.5)} y1={0} x2={reToX(0.5)} y2={H} stroke="#22d3ee" strokeWidth={1} strokeDasharray="4,4" opacity={0.5} />
            {/* Danger zone markers */}
            <line x1={reToX(0.42)} y1={0} x2={reToX(0.42)} y2={H} stroke="#f59e0b" strokeWidth={0.5} strokeDasharray="2,4" opacity={0.3} />
            <line x1={reToX(0.58)} y1={0} x2={reToX(0.58)} y2={H} stroke="#f59e0b" strokeWidth={0.5} strokeDasharray="2,4" opacity={0.3} />
            {/* Shell band lines */}
            {Array.from({ length: N_SHELLS }).map((_, j) => {
              const im = j * SHELL_HEIGHT + 14;
              const y = imToY(im);
              return <line key={j} x1={0} y1={y} x2={W} y2={y} stroke="#1e293b" strokeWidth={0.5} />;
            })}
            {/* Labels */}
            <text x={reToX(0.5)} y={H - 5} textAnchor="middle" fill="#22d3ee" fontSize={8} opacity={0.6}>Re=½</text>
            <text x={reToX(0.25) + 4} y={12} fill="#374151" fontSize={7}>Re=¼</text>
            <text x={reToX(0.75) - 28} y={12} fill="#374151" fontSize={7}>Re=¾</text>
            {/* Zeros */}
            {zeros.filter((z) => z.active && z.t > 12 && z.t < 82).map((z) => {
              const x = reToX(z.re);
              const y = imToY(z.t);
              const offAxis = Math.abs(z.re - 0.5);
              const color = offAxis > 0.08 ? "#f59e0b" : offAxis > 0.04 ? "#a78bfa" : "#22d3ee";
              return (
                <g key={z.id}>
                  {offAxis > 0.04 && omega6On && (
                    <line x1={x} y1={y} x2={reToX(0.5)} y2={y} stroke={color} strokeWidth={0.5} opacity={0.3} strokeDasharray="2,2" />
                  )}
                  <circle cx={x} cy={y} r={3.5} fill={color} opacity={0.85} />
                  <circle cx={x} cy={y} r={offAxis > 0.06 ? 6 : 3.5} fill="none" stroke={color} strokeWidth={0.5} opacity={0.3} />
                </g>
              );
            })}
          </svg>
        </div>
        <div className="flex gap-4 mt-3 text-[10px] text-gray-500">
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-cyan-400 inline-block" /> On-axis (RH OK)</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-violet-400 inline-block" /> Near off-axis</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-amber-400 inline-block" /> Off-axis (danger)</span>
        </div>
      </div>

      {/* Shell density bars */}
      <div className="bg-[#0a0c12] border border-gray-800 rounded-lg p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-4">
          α_j — Zero Density Per Shell <span className="text-violet-600 ml-3">α_c = 1/N = {alphaCrit.toFixed(2)}</span>
        </div>
        <div className="flex items-end gap-1 h-24">
          {alpha.map((a, j) => {
            const isDom = j === dominantShell;
            const danger = isDom && a > alphaCrit * 2;
            const pct = Math.round((a / (maxAlpha || 0.001)) * 100);
            return (
              <div key={j} className="flex-1 flex flex-col items-center justify-end h-full">
                <div
                  className="w-full rounded-t transition-all duration-300"
                  style={{
                    height: `${pct}%`,
                    backgroundColor: danger ? "#f59e0b" : isDom ? "#a78bfa" : "#334155",
                    boxShadow: isDom ? `0 0 8px ${danger ? "#f59e0b88" : "#a78bfa88"}` : "none",
                  }}
                />
              </div>
            );
          })}
        </div>
        <div className="flex gap-1 mt-1">
          {alpha.map((_, j) => (
            <div key={j} className="flex-1 text-center text-[9px] text-gray-600 font-mono">{j + 1}</div>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
        <div className="bg-[#12151e] border border-gray-800 rounded p-3">
          <div className="text-gray-500 mb-1">max|Re(ρ)−½|</div>
          <div className={`font-bold text-lg font-mono ${rhMet ? "text-emerald-400" : isDanger ? "text-amber-400" : "text-gray-200"}`}>
            {maxDev.toFixed(4)}
          </div>
        </div>
        <div className="bg-[#12151e] border border-gray-800 rounded p-3">
          <div className="text-gray-500 mb-1">RH status</div>
          <div className={`font-bold text-sm font-mono ${rhMet ? "text-emerald-400" : isDanger ? "text-rose-400" : "text-amber-400"}`}>
            {rhMet ? "✓ HOLDING" : isDanger ? "✗ VIOLATED" : "⚠ MARGINAL"}
          </div>
        </div>
        <div className="bg-[#12151e] border border-gray-800 rounded p-3">
          <div className="text-gray-500 mb-1">Dom. shell j*</div>
          <div className="text-violet-400 font-bold text-lg font-mono">{dominantShell + 1}</div>
        </div>
        <div className={`rounded p-3 border ${isDanger && omega6On ? "border-violet-700 bg-violet-950/30" : "bg-[#12151e] border-gray-800"}`}>
          <div className="text-gray-500 mb-1">Ω6</div>
          <div className={`font-bold text-lg font-mono ${isDanger && omega6On ? "text-violet-400" : "text-gray-600"}`}>
            {isDanger && omega6On ? "🟣 Active" : "● Dormant"}
          </div>
        </div>
      </div>

      {/* Omega6 formula */}
      <div className="rounded-lg border border-gray-700 bg-[#12151e] p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">Ω6 Repulsion Formula</div>
        <MB>{"\\lambda_j^\\zeta[\\alpha] = \\kappa_\\Omega\\;\\chi_{\\{|j-j_*|\\le m\\}}\\left(\\frac{\\alpha_j}{\\alpha_c}\\right)^\\theta \\cdot \\mathrm{sgn}\\bigl(\\operatorname{Re}(\\rho_j)-\\tfrac{1}{2}\\bigr)"}</MB>
        <div className="mt-3 text-xs text-gray-600">
          κ_Ω = {kappa.toFixed(2)} · forces zeros toward Re(s) = ½ when off-axis concentration detected
        </div>
      </div>

      {/* Event log */}
      {events.length > 0 && (
        <div className="bg-[#0a0c12] border border-gray-800 rounded p-3 space-y-1">
          <div className="text-[10px] text-gray-600 uppercase tracking-widest mb-2">Ω6 Event Log</div>
          {events.map((e, i) => (
            <div key={i} className="text-[10px] font-mono text-violet-700">{e.msg}</div>
          ))}
        </div>
      )}
    </div>
  );
}