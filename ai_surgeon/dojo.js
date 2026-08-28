/* Kuroto Dojo — budget Speed Racer cartoon. Loads engine/storyboard.json. */
(function (w) {
  const $ = (id) => document.getElementById(id);

  const Dojo = {
    board: null,
    skill: null,
    motion: 0,
    prevFrame: null,
    camStream: null,
    holdMs: 0,
    lastT: 0,
    counts: 0
  };

  function log(t) { $('log').textContent = t; }

  function paintSkills() {
    const box = $('skills');
    box.innerHTML = '';
    const skills = (Dojo.board.dojo && Dojo.board.dojo.skills) || [];
    skills.forEach((s, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = s.name + ' · ' + s.name_en;
      b.addEventListener('click', () => pick(i));
      box.appendChild(b);
    });
  }

  function pick(i) {
    const skills = Dojo.board.dojo.skills;
    Dojo.skill = skills[i];
    Dojo.holdMs = 0;
    Dojo.counts = 0;
    ;[...$('skills').children].forEach((b, n) => b.classList.toggle('on', n === i));
    $('coach').textContent = Dojo.skill.coach + '  (Pen: ' + Dojo.skill.maps_to_pen + ')';
    log(Dojo.skill.name_en + ' — begin.');
  }

  function speedLines(ctx, t) {
    ctx.fillStyle = '#120808';
    ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.strokeStyle = 'rgba(227,28,35,0.35)';
    ctx.lineWidth = 2;
    for (let i = 0; i < 18; i++) {
      const y = (i * 14 + (t / 8) % 14);
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(ctx.canvas.width, y + 8);
      ctx.stroke();
    }
    ctx.fillStyle = '#e31c23';
    ctx.font = '700 22px sans-serif';
    const label = Dojo.skill ? Dojo.skill.name : '道場';
    ctx.fillText(label, 24, 48);
    ctx.fillStyle = '#d4af37';
    ctx.font = '14px sans-serif';
    ctx.fillText('SPEED RACER CEL · no sword tray · bow first', 24, 74);
    const m = Math.min(1, Dojo.motion * 8);
    ctx.fillStyle = m > 0.55 ? '#e31c23' : '#2a6f7a';
    ctx.fillRect(24, 160, Math.max(4, m * 300), 12);
    ctx.fillStyle = '#f4ead6';
    ctx.fillText(m > 0.55 ? 'too fast for tai chi' : (m < 0.08 ? 'still / leopard' : 'slow wave'), 24, 196);
  }

  function tick(t) {
    const c = $('fx');
    const ctx = c.getContext('2d');
    speedLines(ctx, t);
    const dt = Dojo.lastT ? t - Dojo.lastT : 16;
    Dojo.lastT = t;
    const s = Dojo.skill;
    if (s && s.kind === 'hold') {
      if (Dojo.motion < 0.12) Dojo.holdMs += dt;
      else Dojo.holdMs = Math.max(0, Dojo.holdMs - dt * 2);
      const need = (s.seconds || 20) * 1000;
      $('mot-n').textContent = Math.min(100, Math.round(Dojo.holdMs / need * 100)) + '% hold';
      if (Dojo.holdMs >= need) log('Leopard rooted. That was exercise. Bow.');
    }
    if (s && s.kind === 'slow_sequence') {
      if (Dojo.motion > 0.08 && Dojo.motion < 0.45) Dojo.counts += dt / 1000;
      const need = (s.counts || 8) * (s.seconds_per_count || 3);
      $('mot-n').textContent = Math.min(s.counts, Math.floor(Dojo.counts / (s.seconds_per_count || 3))) + ' / ' + s.counts;
      if (Dojo.counts >= need) log('Tai chi wave complete. Slow on purpose.');
      if (Dojo.motion > 0.6) log('Too fast. Tai chi is not a punch. Reset your breath.');
    }
    $('mot').style.width = Math.min(100, Dojo.motion * 400) + '%';
    requestAnimationFrame(tick);
  }

  function sampleCam() {
    const v = $('cam');
    if (!Dojo.camStream || v.readyState < 2) return;
    const tmp = document.createElement('canvas');
    tmp.width = 48; tmp.height = 36;
    const x = tmp.getContext('2d', { willReadFrequently: true });
    x.drawImage(v, 0, 0, 48, 36);
    const d = x.getImageData(0, 0, 48, 36).data;
    if (Dojo.prevFrame) {
      let acc = 0;
      for (let i = 0; i < d.length; i += 4) {
        acc += Math.abs(d[i] - Dojo.prevFrame[i]);
      }
      Dojo.motion = acc / (d.length * 255);
    }
    Dojo.prevFrame = d.slice();
  }

  async function camOn() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' }, audio: false });
      Dojo.camStream = stream;
      $('cam').srcObject = stream;
      await $('cam').play();
      $('cam').classList.add('on');
      log('Camera on. Frame-diff only. Not pose tracking. Not cleared.');
    } catch (e) {
      log('Camera denied. Keyboard and Pen still work.');
    }
  }

  function camOff() {
    if (Dojo.camStream) Dojo.camStream.getTracks().forEach((t) => t.stop());
    Dojo.camStream = null;
    $('cam').classList.remove('on');
    Dojo.motion = 0;
  }

  function onPen(g) {
    if (w.AISS && AISS.Pen) AISS.Pen.fire(g, { source: 'dojo' });
    const s = Dojo.skill;
    if (!s) { log(g); return; }
    if (s.kind === 'choose' && g === 'twist') {
      const opts = s.options || [];
      const i = Math.floor(Math.random() * opts.length);
      log('Around you: ' + opts[i] + '. No mall sword.');
    }
    if (s.kind === 'spar' && g === 'click') {
      Dojo.counts += 1;
      log('Palm ' + Dojo.counts + ' / 3. Cartoon. Bow if you are done.');
    }
    if (s.kind === 'hold' && g === 'squeeze') {
      Dojo.holdMs += 2000;
      log('Rooted a little more. Squeeze is the stance.');
    }
    if (s.kind === 'slow_sequence' && g === 'twist') {
      Dojo.counts += 1;
      log('Wave count from the hand. Slow.');
    }
  }

  fetch('engine/storyboard.json')
    .then((r) => r.json())
    .then((board) => {
      Dojo.board = board;
      paintSkills();
      pick(0);
      $('coach').textContent = board.dojo.why;
      requestAnimationFrame(tick);
      setInterval(sampleCam, 80);
    })
    .catch(() => { $('coach').textContent = 'Could not load engine/storyboard.json'; });

  $('btn-cam').addEventListener('click', camOn);
  $('btn-cam-off').addEventListener('click', camOff);
  document.querySelectorAll('[data-pen]').forEach((b) => {
    b.addEventListener('click', () => onPen(b.getAttribute('data-pen')));
  });
  window.addEventListener('keydown', (ev) => {
    if (ev.key === 'q' || ev.key === 'Q' || ev.key === 'e' || ev.key === 'E') onPen('twist');
    if (ev.key === 'Enter') { ev.preventDefault(); onPen('click'); }
    if (ev.key === 'f' || ev.key === 'F') onPen('squeeze');
    if (ev.key === ' ') {
      ev.preventDefault();
      Dojo.motion = 0.02;
      onPen('squeeze');
    }
  });
})(window);
