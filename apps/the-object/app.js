(function () {
  const data = window.OBJECT_DATA;
  const canvas = document.getElementById("space");
  const ctx = canvas.getContext("2d");

  function fmt(x, n) {
    if (x == null || !isFinite(x)) return "—";
    return Number(x).toFixed(n);
  }

  function nearestRow(list, idx) {
    return list[Math.max(0, Math.min(list.length - 1, idx))];
  }

  const state = {
    rotY: 0.7,
    rotX: 0.35,
    dragging: false,
    lastX: 0,
    lastY: 0,
  };

  function project(p, w, h) {
    const cy = Math.cos(state.rotY);
    const sy = Math.sin(state.rotY);
    const cx = Math.cos(state.rotX);
    const sx = Math.sin(state.rotX);
    let x = p[0];
    let y = p[1];
    let z = p[2];
    let x1 = x * cy + z * sy;
    let z1 = -x * sy + z * cy;
    let y1 = y * cx - z1 * sx;
    z1 = y * sx + z1 * cx;
    const scale = 78;
    const depth = 8 / (8 + z1);
    return {
      x: w / 2 + x1 * scale * depth,
      y: h / 2 - y1 * scale * depth,
      z: z1,
      r: 5.5 * depth,
    };
  }

  function drawSphere(radius, color, w, h) {
    ctx.strokeStyle = color;
    ctx.globalAlpha = 0.18;
    ctx.lineWidth = 1;
    for (let t = 0; t < 12; t += 1) {
      ctx.beginPath();
      for (let i = 0; i <= 48; i += 1) {
        const a = (i / 48) * Math.PI * 2;
        const p = project(
          [
            radius * Math.cos(a) * Math.cos(t),
            radius * Math.sin(t * 0.26),
            radius * Math.sin(a) * Math.cos(t),
          ],
          w,
          h
        );
        if (i === 0) ctx.moveTo(p.x, p.y);
        else ctx.lineTo(p.x, p.y);
      }
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }

  function draw() {
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);
    drawSphere(2, "#e2a35a", w, h);
    drawSphere(Math.sqrt(8), "#7eb8c9", w, h);

    const pts = [];
    for (const k of data.shells.alpha) pts.push({ k, c: "#e2a35a", s: 1.25 });
    for (const k of data.shells.beta) pts.push({ k, c: "#7eb8c9", s: 0.95 });
    const projected = pts
      .map((item) => ({ ...item, p: project(item.k, w, h) }))
      .sort((a, b) => a.p.z - b.p.z);

    if (data.shells.alpha.length >= 2 && data.shells.beta.length) {
      const a0 = project(data.shells.alpha[0], w, h);
      const a1 = project(data.shells.alpha[1], w, h);
      const sum = [
        data.shells.alpha[0][0] + data.shells.alpha[1][0],
        data.shells.alpha[0][1] + data.shells.alpha[1][1],
        data.shells.alpha[0][2] + data.shells.alpha[1][2],
      ];
      const b = project(sum, w, h);
      ctx.strokeStyle = "#c45c26";
      ctx.globalAlpha = 0.8;
      ctx.beginPath();
      ctx.moveTo(a0.x, a0.y);
      ctx.lineTo(b.x, b.y);
      ctx.moveTo(a1.x, a1.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
      ctx.globalAlpha = 1;
    }

    for (const item of projected) {
      ctx.beginPath();
      ctx.fillStyle = item.c;
      ctx.arc(item.p.x, item.p.y, item.p.r * item.s, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function syncReadout() {
    const idx = Number(document.getElementById("eps").value);
    const aligned = document.getElementById("aligned").checked;
    const row = nearestRow(aligned ? data.aligned : data.misaligned, idx);
    document.getElementById("eps-out").textContent = String(row.eps);
    document.getElementById("k-val").textContent = fmt(data.featured.K, 4);
    document.getElementById("r-val").textContent = fmt(row.R_star, 4);
    document.getElementById("tc-val").textContent = fmt(row.T_c, 4);
    document.getElementById("ds-val").textContent = fmt(row.D_s, 5);
    document.getElementById("ab").textContent =
      data.featured.alpha + ", " + data.featured.beta;
  }

  canvas.addEventListener("pointerdown", (ev) => {
    state.dragging = true;
    state.lastX = ev.clientX;
    state.lastY = ev.clientY;
    canvas.setPointerCapture(ev.pointerId);
  });
  canvas.addEventListener("pointerup", () => {
    state.dragging = false;
  });
  canvas.addEventListener("pointermove", (ev) => {
    if (!state.dragging) return;
    state.rotY += (ev.clientX - state.lastX) * 0.01;
    state.rotX += (ev.clientY - state.lastY) * 0.01;
    state.lastX = ev.clientX;
    state.lastY = ev.clientY;
    draw();
  });

  document.getElementById("eps").addEventListener("input", syncReadout);
  document.getElementById("aligned").addEventListener("change", syncReadout);

  if (!data) {
    document.querySelector(".status").textContent = "data.js missing";
    return;
  }
  syncReadout();
  draw();
})();
