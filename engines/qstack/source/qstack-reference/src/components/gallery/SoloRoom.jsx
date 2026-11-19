import React, { useEffect, useRef, useState } from "react";

export default function SoloRoom({ room, entanglementState, onExit }) {
  const canvasRef = useRef(null);
  const [mousePos, setMousePos] = useState({ x: 0.5, y: 0.5 });
  const { phase, pulse, drift } = entanglementState;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    if (room.id === "cascade") paintCascade(canvas, phase, pulse, mousePos);
    if (room.id === "zeros")   paintZeros(canvas, phase, pulse, mousePos);
  }, [phase, pulse, drift, mousePos, room.id]);

  function handleMouse(e) {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    setMousePos({
      x: (e.clientX - rect.left) / rect.width,
      y: (e.clientY - rect.top) / rect.height,
    });
  }

  const insight = room.id === "cascade"
    ? [
        { label: "Kolmogorov scaling", val: "E(k) ~ k^{−5/3}", color: "#f59e0b" },
        { label: "Inertial range", val: "shells 4–7", color: "#a78bfa" },
        { label: "Dissipation scale", val: "k ~ Re^{3/4}", color: "#22d3ee" },
        { label: "Q6 monitors", val: "j* (dominant shell)", color: "#22d3ee" },
      ]
    : [
        { label: "First zero", val: "Im = 14.134...", color: "#ec4899" },
        { label: "All known zeros", val: "on Re = ½", color: "#ec4899" },
        { label: "GUE spacing", val: "random matrix analogy", color: "#a78bfa" },
        { label: "Ω6 monitors", val: "zero density per shell", color: "#a78bfa" },
      ];

  return (
    <div className="min-h-screen bg-[#04050a] font-mono flex flex-col">
      <div className="flex items-center justify-between px-8 py-5 border-b border-gray-900">
        <button onClick={onExit}
          className="text-[10px] text-gray-600 hover:text-gray-300 tracking-widest uppercase transition-colors">
          ← Gallery
        </button>
        <div className="text-center">
          <div className="text-[9px] tracking-[0.4em] uppercase mb-0.5" style={{ color: room.color }}>
            {room.subtitle}
          </div>
          <div className="text-white text-sm font-bold">{room.name}</div>
        </div>
        <div className="w-24" />
      </div>

      <div className="flex-1 relative"
        onMouseMove={handleMouse}>
        <canvas
          ref={canvasRef}
          width={1200} height={600}
          className="w-full"
          style={{ display: "block", minHeight: 500, cursor: "crosshair" }}
        />
        {/* Insight overlay */}
        <div className="absolute bottom-6 left-6 space-y-2">
          {insight.map(m => (
            <div key={m.label}
              className="bg-black/70 backdrop-blur-sm rounded-lg px-3 py-2 border border-gray-800 flex items-center gap-3">
              <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ backgroundColor: m.color }} />
              <span className="text-[9px] text-gray-500">{m.label}</span>
              <span className="text-[9px] font-bold" style={{ color: m.color }}>{m.val}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="px-8 py-5 border-t border-gray-900 bg-[#06080e]">
        <p className="text-[11px] text-gray-500 max-w-3xl mx-auto text-center leading-relaxed">
          {room.id === "cascade"
            ? "Energy enters at large scales (left). It cascades rightward through the inertial range — no energy lost, just redistributed — until it hits the dissipation scale and becomes heat. Hover to disturb the cascade."
            : "Each glowing point is a confirmed zero of the Riemann zeta function ζ(s). They all appear to lie on the vertical line Re(s) = ½. Nobody has proven they all must. That is the Riemann Hypothesis. Hover to illuminate individual zeros."}
        </p>
      </div>
    </div>
  );
}

function paintCascade(canvas, phase, pulse, mouse) {
  const ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height;
  ctx.clearRect(0, 0, W, H);

  // Background
  const bg = ctx.createLinearGradient(0, 0, W, 0);
  bg.addColorStop(0, "#050a18");
  bg.addColorStop(0.5, "#08050f");
  bg.addColorStop(1, "#0a0502");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, W, H);

  const N = 14;
  const mx = mouse.x;

  for (let j = 0; j < N; j++) {
    const t = j / N;
    const x0 = t * W * 0.85 + W * 0.05;
    const x1 = (t + 1 / N) * W * 0.85 + W * 0.05;
    const cx = (x0 + x1) / 2;

    const scale = Math.pow(0.72, j);
    const turbulence = 0.15 * Math.sin(phase * (1.2 + j * 0.2) + j * 1.4);
    const mouseEffect = 0.3 * Math.exp(-8 * Math.pow(t - mx, 2)) * (1 - mouse.y);
    const energy = scale * (0.85 + turbulence) + mouseEffect;
    const barH = energy * H * 0.55;
    const barW = (x1 - x0) * 0.75;

    // Color: large scale = cyan, inertial = violet, dissipation = amber, cutoff = red
    let r, g, b;
    if (j < 3)       { r = 34;  g = 211; b = 238; }
    else if (j < 8)  { r = 167; g = 139; b = 250; }
    else if (j < 12) { r = 245; g = 158; b = 11; }
    else             { r = 239; g = 68;  b = 68; }

    const alpha = 0.5 + energy * 0.4;

    // Glow bar
    ctx.shadowBlur = 20 + energy * 15;
    ctx.shadowColor = `rgba(${r},${g},${b},0.4)`;
    const grd = ctx.createLinearGradient(cx, H * 0.85 - barH, cx, H * 0.85);
    grd.addColorStop(0, `rgba(${r},${g},${b},${alpha})`);
    grd.addColorStop(1, `rgba(${r},${g},${b},${alpha * 0.15})`);
    ctx.fillStyle = grd;
    ctx.beginPath();
    ctx.roundRect(cx - barW / 2, H * 0.85 - barH, barW, barH, 4);
    ctx.fill();
    ctx.shadowBlur = 0;

    // Flow arrow between shells
    if (j < N - 1) {
      const nx = ((j + 1) / N) * W * 0.85 + W * 0.05 + (W * 0.85 / N) * 0.12;
      const ay = H * 0.85 - barH * 0.5;
      const flowAlpha = 0.15 + energy * 0.2;
      ctx.strokeStyle = `rgba(${r},${g},${b},${flowAlpha})`;
      ctx.lineWidth = 1 + energy;
      ctx.beginPath();
      ctx.moveTo(cx + barW / 2 + 4, ay);
      ctx.lineTo(nx - 4, ay);
      ctx.stroke();
    }

    // Shell label
    ctx.fillStyle = `rgba(${r},${g},${b},0.4)`;
    ctx.font = "8px monospace";
    ctx.textAlign = "center";
    ctx.fillText(`P_${j + 1}`, cx, H * 0.85 + 14);

    // Mouse probe dot
    if (Math.abs(t - mx) < 0.04) {
      ctx.beginPath();
      ctx.arc(cx, H * 0.85 - barH, 5, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${r},${g},${b},0.9)`;
      ctx.fill();
      // Value label
      ctx.fillStyle = `rgba(${r},${g},${b},0.8)`;
      ctx.font = "9px monospace";
      ctx.fillText(`E=${energy.toFixed(3)}`, cx, H * 0.85 - barH - 10);
    }
  }

  // Kolmogorov -5/3 reference line
  const kPts = [];
  for (let i = 0; i < N; i++) {
    const t = i / N;
    const x = t * W * 0.85 + W * 0.05 + (W * 0.85 / N) * 0.5;
    const e = Math.pow(0.72, i) * 0.85;
    const y = H * 0.85 - e * H * 0.55;
    kPts.push([x, y]);
  }
  ctx.strokeStyle = "rgba(255,255,255,0.07)";
  ctx.lineWidth = 1;
  ctx.setLineDash([6, 4]);
  ctx.beginPath();
  kPts.forEach(([x, y], i) => i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y));
  ctx.stroke();
  ctx.setLineDash([]);

  ctx.textAlign = "left";
  ctx.fillStyle = "rgba(255,255,255,0.15)";
  ctx.font = "10px monospace";
  ctx.fillText("← large scale (IR)", W * 0.06, H - 10);
  ctx.textAlign = "right";
  ctx.fillText("UV cutoff →", W * 0.94, H - 10);
  ctx.textAlign = "left";
}

function paintZeros(canvas, phase, pulse, mouse) {
  const ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height;
  ctx.clearRect(0, 0, W, H);

  const bg = ctx.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, W * 0.6);
  bg.addColorStop(0, "#0d0510");
  bg.addColorStop(1, "#04050a");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, W, H);

  const zeros = [
    14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327,
    48.005, 49.774, 52.970, 56.446, 59.347, 60.832, 65.113, 67.080,
    69.546, 72.067, 75.705, 77.145, 79.337, 82.910, 84.735, 87.425,
  ];
  const maxT = 92;
  const cx = W / 2;

  // Strip boundaries
  ctx.fillStyle = "rgba(55, 65, 81, 0.05)";
  ctx.fillRect(cx - 150, 0, 300, H);

  // Critical line
  ctx.shadowBlur = 15;
  ctx.shadowColor = "rgba(34, 211, 238, 0.3)";
  ctx.strokeStyle = "rgba(34, 211, 238, 0.25)";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(cx, 0); ctx.lineTo(cx, H);
  ctx.stroke();
  ctx.shadowBlur = 0;

  // Re = 0 and 1
  ctx.strokeStyle = "rgba(55, 65, 81, 0.3)";
  ctx.lineWidth = 1;
  ctx.setLineDash([4, 4]);
  [cx - 150, cx + 150].forEach(x => {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
  });
  ctx.setLineDash([]);

  // Zeros
  zeros.forEach((t, i) => {
    const y = (t / maxT) * (H - 60) + 30;
    const dist = Math.abs(mouse.y - y / H);
    const nearness = Math.exp(-dist * 8);
    const glow = 0.4 + 0.4 * Math.sin(phase * 0.6 + i * 1.7) + nearness * 0.5;

    // Horizontal guide
    ctx.strokeStyle = `rgba(236, 72, 153, ${0.06 + nearness * 0.15})`;
    ctx.lineWidth = 0.8;
    ctx.beginPath();
    ctx.moveTo(cx - 200, y); ctx.lineTo(cx + 200, y);
    ctx.stroke();

    // Zero dot
    const radius = 5 + nearness * 8;
    ctx.shadowBlur = 15 + nearness * 20;
    ctx.shadowColor = `rgba(236, 72, 153, ${glow})`;
    ctx.beginPath();
    ctx.arc(cx, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(236, 72, 153, ${0.5 + glow * 0.4})`;
    ctx.fill();
    ctx.shadowBlur = 0;

    // Label on hover
    if (nearness > 0.3) {
      ctx.fillStyle = `rgba(236, 72, 153, ${nearness})`;
      ctx.font = `${9 + nearness * 4}px monospace`;
      ctx.textAlign = "left";
      ctx.fillText(`ζ(½ + ${t.toFixed(3)}i) = 0`, cx + radius + 10, y + 4);
    } else {
      ctx.fillStyle = "rgba(100, 60, 80, 0.5)";
      ctx.font = "8px monospace";
      ctx.textAlign = "right";
      ctx.fillText(t.toFixed(3), cx - radius - 5, y + 3);
    }
  });

  ctx.textAlign = "center";
  ctx.fillStyle = "rgba(34, 211, 238, 0.3)";
  ctx.font = "10px monospace";
  ctx.fillText("Re(s) = ½", cx, H - 10);
  ctx.fillStyle = "rgba(55, 65, 81, 0.5)";
  ctx.fillText("Re=0", cx - 150, H - 10);
  ctx.fillText("Re=1", cx + 150, H - 10);
}