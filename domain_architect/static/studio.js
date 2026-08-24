const PRESETS = {
  gold: {
    corner: 0.20, frame: 0.055, bg: "#161616", grain: 0.42,
    light_angle: -38, light: 0.88, bevel: 0.55,
    a_scale: 0.36, a_thick: 0.11, a_metal: "#d8d8d8",
    swirl_scale: 0.155, swirl_rot: -18, swirl_spread: 1,
    arm_width: 0.048, hue: 0, sat: 1, glow: 0.65,
    sphere: 0.028, sphere_metal: "#e6c35a",
    domain_metal: "#e6c35a", architect_metal: "#e8e8e8", tagline_metal: "#d4b45a",
    tracking: 0.34, show_wordmark: true, show_tagline: true, show_frame: true,
  },
  silver: {
    corner: 0.20, frame: 0.055, bg: "#161616", grain: 0.42,
    light_angle: -38, light: 0.9, bevel: 0.55,
    a_scale: 0.36, a_thick: 0.11, a_metal: "#dcdcdc",
    swirl_scale: 0.155, swirl_rot: -18, swirl_spread: 1,
    arm_width: 0.048, hue: 8, sat: 0.92, glow: 0.6,
    sphere: 0.028, sphere_metal: "#e8e8e8",
    domain_metal: "#e8e8e8", architect_metal: "#f0f0f0", tagline_metal: "#d0d0d0",
    tracking: 0.34, show_wordmark: true, show_tagline: true, show_frame: true,
  },
};

const SLIDERS = [
  ["corner", "Corner roundness", 0.08, 0.36, 0.005],
  ["frame", "Chrome frame", 0.02, 0.12, 0.002],
  ["grain", "Background grain", 0, 1, 0.01],
  ["light_angle", "Light angle", -90, 90, 1],
  ["light", "Metal shine", 0.2, 1, 0.01],
  ["bevel", "Bevel highlight", 0, 1, 0.01],
  ["a_scale", "A size", 0.2, 0.55, 0.005],
  ["a_thick", "A thickness", 0.05, 0.2, 0.002],
  ["swirl_scale", "Swirl size", 0.08, 0.3, 0.005],
  ["swirl_rot", "Swirl rotation", -180, 180, 1],
  ["swirl_spread", "Arm spread", 0.6, 1.5, 0.01],
  ["arm_width", "Arm width", 0.02, 0.1, 0.002],
  ["hue", "Rainbow hue", 0, 360, 1],
  ["sat", "Rainbow saturation", 0, 1, 0.01],
  ["glow", "Rainbow glow", 0, 1, 0.01],
  ["sphere", "Center sphere", 0.01, 0.06, 0.001],
  ["tracking", "Letter spacing", 0, 0.7, 0.01],
];

const COLORS = [
  ["bg", "Field"],
  ["a_metal", "A metal"],
  ["sphere_metal", "Sphere"],
  ["domain_metal", "DOMAIN"],
  ["architect_metal", "ARCHITECT"],
  ["tagline_metal", "Tagline"],
];

let params = { ...PRESETS.gold };
let studioBound = false;

function mix(a, b, t) {
  const pa = parseInt(a.slice(1), 16);
  const pb = parseInt(b.slice(1), 16);
  const ch = (shift) => {
    const va = (pa >> shift) & 255;
    const vb = (pb >> shift) & 255;
    return Math.round(va + (vb - va) * t);
  };
  return `rgb(${ch(16)},${ch(8)},${ch(0)})`;
}

function hsl(h, s, l) {
  return `hsl(${((h % 360) + 360) % 360} ${s * 100}% ${l * 100}%)`;
}

function metalGrad(ctx, x0, y0, x1, y1, hex, light) {
  const g = ctx.createLinearGradient(x0, y0, x1, y1);
  g.addColorStop(0, mix(hex, "#ffffff", 0.45 + 0.3 * light));
  g.addColorStop(0.45, hex);
  g.addColorStop(1, mix(hex, "#000000", 0.38));
  return g;
}

function noise(ctx, w, h, amount) {
  if (amount <= 0) return;
  const off = document.createElement("canvas");
  off.width = w;
  off.height = h;
  const octx = off.getContext("2d");
  const img = octx.createImageData(w, h);
  const d = img.data;
  for (let i = 0; i < d.length; i += 4) {
    const n = (Math.random() * 255) | 0;
    d[i] = d[i + 1] = d[i + 2] = n;
    d[i + 3] = Math.floor(amount * 55);
  }
  octx.putImageData(img, 0, 0);
  ctx.drawImage(off, 0, 0);
}

function roundRect(ctx, x, y, w, h, r) {
  const radius = Math.max(0, Math.min(r, w / 2, h / 2));
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.arcTo(x + w, y, x + w, y + h, radius);
  ctx.arcTo(x + w, y + h, x, y + h, radius);
  ctx.arcTo(x, y + h, x, y, radius);
  ctx.arcTo(x, y, x + w, y, radius);
  ctx.closePath();
}

function armPath(ctx, swirlR) {
  ctx.beginPath();
  ctx.moveTo(0, -swirlR * 0.16);
  ctx.bezierCurveTo(
    swirlR * 0.62, -swirlR * 0.02,
    swirlR * 1.02, swirlR * 0.38,
    swirlR * 0.08, swirlR * 0.98
  );
}

function drawMark(canvas, p) {
  const s = canvas.width;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, s, s);
  const cx = s / 2;
  const word = p.show_wordmark;
  const ay = s * (word ? 0.30 : 0.50);
  const corner = p.corner * s;
  const frame = p.frame * s;
  const innerR = Math.max(2, corner - frame * 0.6);

  roundRect(ctx, 0, 0, s, s, corner);
  if (p.show_frame) {
    ctx.fillStyle = metalGrad(ctx, 0, 0, s, s, "#cfd3d8", p.light);
    ctx.fill();
    roundRect(ctx, frame, frame, s - 2 * frame, s - 2 * frame, innerR);
    ctx.fillStyle = p.bg;
    ctx.fill();
    ctx.strokeStyle = "rgba(255,255,255,0.22)";
    ctx.lineWidth = Math.max(1.2, s * 0.004);
    ctx.stroke();
  } else {
    ctx.fillStyle = p.bg;
    ctx.fill();
  }

  ctx.save();
  roundRect(ctx, frame, frame, s - 2 * frame, s - 2 * frame, innerR);
  ctx.clip();
  noise(ctx, s, s, p.grain);
  ctx.restore();

  const aH = p.a_scale * s;
  const aW = aH * 0.92;
  const thick = p.a_thick * s;
  const apexX = cx;
  const apexY = ay - aH * 0.52;
  const leftX = cx - aW * 0.52;
  const leftY = ay + aH * 0.48;
  const rightX = cx + aW * 0.52;
  const rightY = ay + aH * 0.48;
  const ang = (p.light_angle * Math.PI) / 180;

  ctx.lineJoin = "miter";
  ctx.miterLimit = 2.4;
  ctx.lineCap = "butt";
  ctx.lineWidth = thick + 6;
  ctx.strokeStyle = "rgba(0,0,0,0.45)";
  ctx.beginPath();
  ctx.moveTo(leftX + 4, leftY + 6);
  ctx.lineTo(apexX + 4, apexY + 6);
  ctx.lineTo(rightX + 4, rightY + 6);
  ctx.stroke();

  ctx.lineWidth = thick;
  ctx.strokeStyle = metalGrad(
    ctx,
    cx + Math.cos(ang) * -aW,
    ay + Math.sin(ang) * -aH,
    cx + Math.cos(ang) * aW,
    ay + Math.sin(ang) * aH,
    p.a_metal,
    p.light
  );
  ctx.beginPath();
  ctx.moveTo(leftX, leftY);
  ctx.lineTo(apexX, apexY);
  ctx.lineTo(rightX, rightY);
  ctx.stroke();

  ctx.lineWidth = Math.max(1.5, thick * (0.22 + 0.28 * p.bevel));
  ctx.strokeStyle = metalGrad(
    ctx,
    cx + Math.cos(ang) * -aW,
    ay + Math.sin(ang) * -aH,
    cx + Math.cos(ang) * aW,
    ay + Math.sin(ang) * aH,
    "#ffffff",
    1
  );
  ctx.globalAlpha = 0.45;
  ctx.beginPath();
  ctx.moveTo(leftX, leftY);
  ctx.lineTo(apexX, apexY);
  ctx.lineTo(rightX, rightY);
  ctx.stroke();
  ctx.globalAlpha = 1;

  const swirlR = p.swirl_scale * s * p.swirl_spread;
  const armW = p.arm_width * s;
  for (let i = 0; i < 3; i += 1) {
    const rot = ((p.swirl_rot + i * 120) * Math.PI) / 180;
    const hue = p.hue + i * 120;
    ctx.save();
    ctx.translate(cx, ay);
    ctx.rotate(rot);
    ctx.shadowColor = hsl(hue, p.sat, 0.55);
    ctx.shadowBlur = 8 + p.glow * 18;
    ctx.lineCap = "round";
    ctx.strokeStyle = "#d8d8d8";
    ctx.lineWidth = armW * 1.28;
    armPath(ctx, swirlR);
    ctx.stroke();
    const g = ctx.createLinearGradient(0, -swirlR * 0.2, swirlR, swirlR);
    g.addColorStop(0, hsl(hue, p.sat, 0.62));
    g.addColorStop(0.55, hsl(hue + 50, p.sat, 0.42));
    g.addColorStop(1, hsl(hue + 90, p.sat, 0.48));
    ctx.strokeStyle = g;
    ctx.lineWidth = armW;
    armPath(ctx, swirlR);
    ctx.stroke();
    ctx.restore();
  }

  const sr = p.sphere * s;
  const sg = ctx.createRadialGradient(cx - sr * 0.35, ay - sr * 0.4, sr * 0.1, cx, ay, sr);
  sg.addColorStop(0, "#fff");
  sg.addColorStop(0.35, mix(p.sphere_metal, "#ffffff", 0.25));
  sg.addColorStop(1, mix(p.sphere_metal, "#000000", 0.35));
  ctx.fillStyle = sg;
  ctx.beginPath();
  ctx.arc(cx, ay, sr, 0, Math.PI * 2);
  ctx.fill();

  if (word) {
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.font = `700 ${s * 0.055}px ui-sans-serif, system-ui, sans-serif`;
    ctx.letterSpacing = `${p.tracking * 8}px`;
    ctx.fillStyle = metalGrad(ctx, 0, s * 0.68, 0, s * 0.76, p.domain_metal, p.light);
    ctx.fillText("DOMAIN", cx, s * 0.72);
    ctx.font = `700 ${s * 0.072}px ui-sans-serif, system-ui, sans-serif`;
    ctx.fillStyle = metalGrad(ctx, 0, s * 0.78, 0, s * 0.86, p.architect_metal, p.light);
    ctx.fillText("ARCHITECT", cx, s * 0.82);
  }
  if (p.show_tagline) {
    ctx.letterSpacing = `${s * 0.006}px`;
    ctx.font = `600 ${s * 0.028}px ui-sans-serif, system-ui, sans-serif`;
    ctx.fillStyle = p.tagline_metal;
    ctx.fillText("DECOMPOSE  ·  TRANSLATE  ·  SYNTHESIZE", cx, s * 0.90);
  }
}

function currentPayload() {
  return { ...params, size: 1024 };
}

function bindStudio() {
  const canvas = document.getElementById("markCanvas");
  if (!canvas) return;
  canvas.width = 1024;
  canvas.height = 1024;
  if (studioBound) {
    drawMark(canvas, params);
    return;
  }
  studioBound = true;
  const sliders = document.getElementById("sliders");
  const colors = document.getElementById("colors");
  sliders.innerHTML = "";
  colors.innerHTML = "";
  SLIDERS.forEach(([key, label, min, max, step]) => {
    const wrap = document.createElement("label");
    wrap.className = "ctrl";
    wrap.innerHTML = `<span>${label}</span><input type="range" min="${min}" max="${max}" step="${step}" data-key="${key}"><em data-val="${key}"></em>`;
    sliders.appendChild(wrap);
  });
  COLORS.forEach(([key, label]) => {
    const wrap = document.createElement("label");
    wrap.className = "ctrl color";
    wrap.innerHTML = `<span>${label}</span><input type="color" data-key="${key}">`;
    colors.appendChild(wrap);
  });

  function sync() {
    sliders.querySelectorAll("input").forEach((el) => {
      el.value = params[el.dataset.key];
    });
    sliders.querySelectorAll("em").forEach((el) => {
      const v = params[el.dataset.val];
      el.textContent = Number.isInteger(v) ? v : Number(v).toFixed(2);
    });
    colors.querySelectorAll("input").forEach((el) => {
      el.value = params[el.dataset.key];
    });
    document.getElementById("wordmarkOn").checked = params.show_wordmark;
    document.getElementById("taglineOn").checked = params.show_tagline;
    document.getElementById("frameOn").checked = params.show_frame;
    drawMark(canvas, params);
  }

  sliders.addEventListener("input", (ev) => {
    const el = ev.target;
    if (!el.dataset.key) return;
    params[el.dataset.key] = Number(el.value);
    sync();
  });
  colors.addEventListener("input", (ev) => {
    const el = ev.target;
    if (!el.dataset.key) return;
    params[el.dataset.key] = el.value;
    sync();
  });
  document.getElementById("wordmarkOn").addEventListener("change", (ev) => {
    params.show_wordmark = ev.target.checked;
    sync();
  });
  document.getElementById("taglineOn").addEventListener("change", (ev) => {
    params.show_tagline = ev.target.checked;
    sync();
  });
  document.getElementById("frameOn").addEventListener("change", (ev) => {
    params.show_frame = ev.target.checked;
    sync();
  });
  document.getElementById("presetGold").addEventListener("click", () => {
    params = { ...PRESETS.gold };
    sync();
  });
  document.getElementById("presetSilver").addEventListener("click", () => {
    params = { ...PRESETS.silver };
    sync();
  });
  document.getElementById("presetIcon").addEventListener("click", () => {
    params = {
      ...PRESETS.gold,
      show_wordmark: false,
      show_tagline: false,
      a_scale: 0.52,
      swirl_scale: 0.22,
      arm_width: 0.07,
      sphere: 0.04,
    };
    sync();
  });
  document.getElementById("downloadPng").addEventListener("click", () => {
    const a = document.createElement("a");
    a.download = params.show_wordmark
      ? "domain-architect-mark.png"
      : "domain-architect-icon.png";
    a.href = canvas.toDataURL("image/png");
    a.click();
  });
  document.getElementById("applyMark").addEventListener("click", async () => {
    const note = document.getElementById("markNote");
    note.textContent = "Writing app icon…";
    const res = await fetch("/api/brand/apply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(currentPayload()),
    });
    const payload = await res.json();
    if (payload.error) {
      note.textContent = payload.error;
      return;
    }
    const stamp = Date.now();
    note.textContent = "Applied as app icon + favicon.";
    const header = document.querySelector(".titlebar .mark");
    if (header) header.src = `/icon.svg?ts=${stamp}`;
    const fav = document.querySelector("link[rel='icon']");
    if (fav) fav.href = `/favicon.svg?ts=${stamp}`;
  });
  sync();
}

window.bindStudio = bindStudio;
