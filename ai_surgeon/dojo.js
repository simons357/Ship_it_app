/* Kuroto Dojo — budget Speed Racer cartoon. Loads engine/storyboard.json.
   Camera is optional frame-diff — not pose AI, not a medical device, not Carradine IP. */
(function (w) {
  const $ = (id) => document.getElementById(id);
  const RED = '#e31c23';
  const PAPER = '#f4ead6';
  const GOLD = '#d4af37';
  const TEAL = '#2a6f7a';
  const INK = '#111111';

  const Dojo = {
    board: null,
    skill: null,
    motion: 0,
    prevFrame: null,
    camStream: null,
    holdMs: 0,
    lastT: 0,
    waveCounts: 0,
    waveMs: 0,
    lastTwistAt: 0,
    palms: 0,
    bowedIn: false,
    bowedOut: false,
    chosen: null,
    spaceHeld: false,
    squeezeHeld: false,
    palmFlash: 0
  };

  function log(t) { $('log').textContent = t; }

  function skills() {
    return (Dojo.board && Dojo.board.dojo && Dojo.board.dojo.skills) || [];
  }

  function paintBeats() {
    const el = $('beats');
    if (!el || !Dojo.board) return;
    const ch = Dojo.board.chapters || [];
    el.textContent = 'Storyboard ' + ch.map((c) => c.title).join(' · ');
  }

  function paintSkills() {
    const box = $('skills');
    box.innerHTML = '';
    skills().forEach((s, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.id = 'skill-' + s.id;
      b.textContent = s.name + ' · ' + s.name_en;
      b.addEventListener('click', () => pick(i));
      box.appendChild(b);
    });
  }

  function paintProps() {
    const box = $('props');
    box.innerHTML = '';
    const s = Dojo.skill;
    if (!s || s.kind !== 'choose') return;
    (s.options || []).forEach((opt) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.id = 'prop-' + opt;
      b.textContent = opt;
      if (Dojo.chosen === opt) b.classList.add('on');
      b.addEventListener('click', () => choose(opt));
      box.appendChild(b);
    });
  }

  function choose(opt) {
    Dojo.chosen = opt;
    paintProps();
    log('Around you: ' + opt + '. No mall sword.');
    if (w.AISS && AISS.Pen) AISS.Pen.fire('twist', { source: 'dojo', around: opt });
  }

  function pick(i) {
    const list = skills();
    Dojo.skill = list[i];
    Dojo.holdMs = 0;
    Dojo.waveCounts = 0;
    Dojo.waveMs = 0;
    Dojo.palms = 0;
    Dojo.bowedIn = false;
    Dojo.bowedOut = false;
    Dojo.chosen = null;
    Dojo.palmFlash = 0;
    ;[...$('skills').children].forEach((b, n) => b.classList.toggle('on', n === i));
    $('coach').textContent = Dojo.skill.coach + '  (Pen: ' + Dojo.skill.maps_to_pen + ')';
    paintProps();
    log(Dojo.skill.name_en + ' — begin.');
  }

  function limb(ctx, x1, y1, x2, y2, w, color) {
    ctx.strokeStyle = color;
    ctx.lineWidth = w;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  function disc(ctx, x, y, r, fill, stroke) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = fill;
    ctx.fill();
    if (stroke) {
      ctx.strokeStyle = stroke;
      ctx.lineWidth = 2;
      ctx.stroke();
    }
  }

  function drawCape(ctx, x, y, t, pose) {
    const sway = Math.sin(t / 400) * 8;
    ctx.fillStyle = RED;
    ctx.beginPath();
    ctx.moveTo(x, y - 8);
    ctx.quadraticCurveTo(x - 40 + sway, y + 20, x - 28 + sway, y + 70);
    ctx.lineTo(x + 6, y + 18);
    ctx.closePath();
    ctx.fill();
    if (pose === 'leopard') {
      ctx.fillStyle = 'rgba(227,28,35,0.45)';
      ctx.beginPath();
      ctx.moveTo(x - 6, y);
      ctx.quadraticCurveTo(x - 70, y + 10, x - 50, y + 54);
      ctx.lineTo(x, y + 16);
      ctx.fill();
    }
  }

  function drawJun(ctx, x, y, pose, t) {
    const squat = pose === 'leopard' ? 22 : pose === 'bow' ? 26 : 6;
    const hipY = y - 64 + squat;
    const headY = hipY - 64;
    drawCape(ctx, x + 8, hipY - 20, t, pose);

    let lFootX = x - 28;
    let rFootX = x + 34;
    let lHand = { x: x - 42, y: hipY - 10 };
    let rHand = { x: x + 46, y: hipY - 18 };
    if (pose === 'leopard') {
      lFootX = x - 48;
      rFootX = x + 50;
      lHand = { x: x - 70, y: hipY - 6 };
      rHand = { x: x + 38, y: hipY + 8 };
    } else if (pose === 'wave') {
      const a = (Dojo.waveCounts + (Dojo.waveMs / 3000)) * 0.7;
      lHand = { x: x - 36 + Math.cos(a) * 28, y: hipY - 36 + Math.sin(a) * 18 };
      rHand = { x: x + 40 + Math.cos(a + 1.2) * 26, y: hipY - 28 + Math.sin(a + 1.2) * 16 };
    } else if (pose === 'bow') {
      lHand = { x: x - 10, y: hipY + 28 };
      rHand = { x: x + 12, y: hipY + 28 };
    } else if (pose === 'palm') {
      rHand = { x: x + 78, y: hipY - 36 };
      lHand = { x: x - 20, y: hipY + 4 };
    } else if (pose === 'broom' || pose === 'ribbon') {
      rHand = { x: x + 54, y: hipY - 48 };
      lHand = { x: x + 28, y: hipY - 8 };
    } else if (pose === 'sand') {
      rHand = { x: x + 22, y: hipY + 18 };
      lHand = { x: x - 8, y: hipY + 18 };
    }

    limb(ctx, x - 8, hipY + 8, lFootX, y, 7, INK);
    limb(ctx, x + 8, hipY + 8, rFootX, y, 7, INK);
    disc(ctx, lFootX, y, 6, INK);
    disc(ctx, rFootX, y, 6, INK);

    ctx.fillStyle = PAPER;
    ctx.strokeStyle = INK;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(x - 16, hipY - 28, 32, 42, 6);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = GOLD;
    ctx.font = '700 16px sans-serif';
    ctx.fillText('5', x - 5, hipY - 2);

    limb(ctx, x - 12, hipY - 18, lHand.x, lHand.y, 6, PAPER);
    limb(ctx, x + 12, hipY - 18, rHand.x, rHand.y, 6, PAPER);
    disc(ctx, lHand.x, lHand.y, 7, GOLD, INK);
    disc(ctx, rHand.x, rHand.y, 7, GOLD, INK);

    disc(ctx, x, headY, 18, PAPER, INK);
    ctx.fillStyle = PAPER;
    ctx.fillRect(x - 18, headY - 20, 36, 16);
    ctx.strokeRect(x - 18, headY - 20, 36, 16);
    ctx.fillStyle = RED;
    ctx.font = '700 16px sans-serif';
    ctx.fillText('J', x - 6, headY - 6);

    if (pose === 'broom') drawBroom(ctx, rHand.x, rHand.y);
    if (pose === 'ribbon') drawRibbon(ctx, rHand.x, rHand.y, t);
    if (pose === 'sand') drawSand(ctx, x + 8, y);
  }

  function drawBroom(ctx, hx, hy) {
    limb(ctx, hx, hy, hx + 12, hy - 90, 4, '#6b4a2a');
    ctx.fillStyle = TEAL;
    ctx.beginPath();
    ctx.moveTo(hx + 4, hy - 88);
    ctx.lineTo(hx + 28, hy - 108);
    ctx.lineTo(hx + 32, hy - 78);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = RED;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(hx + 8, hy - 40);
    ctx.quadraticCurveTo(hx + 36, hy - 48, hx + 22, hy - 18);
    ctx.stroke();
  }

  function drawRibbon(ctx, hx, hy, t) {
    const sway = Math.sin(t / 280) * 16;
    ctx.strokeStyle = RED;
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(hx, hy);
    ctx.quadraticCurveTo(hx + 20 + sway, hy - 40, hx + 8, hy - 88);
    ctx.stroke();
    ctx.fillStyle = RED;
    ctx.beginPath();
    ctx.moveTo(hx + 8, hy - 88);
    ctx.lineTo(hx + 28 + sway, hy - 70);
    ctx.lineTo(hx - 4, hy - 64);
    ctx.closePath();
    ctx.fill();
  }

  function drawSand(ctx, x, y) {
    ctx.fillStyle = GOLD;
    ctx.beginPath();
    ctx.moveTo(x - 28, y);
    ctx.lineTo(x, y - 22);
    ctx.lineTo(x + 28, y);
    ctx.closePath();
    ctx.fill();
  }

  function drawPartner(ctx, x, y, pose) {
    const bow = pose === 'bow' ? 1 : 0;
    const hipY = y - 48 + bow * 10;
    const headY = hipY - 50 + bow * 18;
    limb(ctx, x - 10, hipY, x - 22, y, 7, INK);
    limb(ctx, x + 10, hipY, x + 24, y, 7, INK);
    ctx.fillStyle = INK;
    ctx.fillRect(x - 18, hipY - 4, 36, 28);
    ctx.fillStyle = PAPER;
    ctx.fillRect(x - 16, hipY - 36, 32, 34);
    ctx.strokeStyle = INK;
    ctx.strokeRect(x - 16, hipY - 36, 32, 34);
    disc(ctx, x, headY, 14, PAPER, INK);
    ctx.fillStyle = INK;
    ctx.beginPath();
    ctx.arc(x, headY - 12, 10, Math.PI, 0);
    ctx.fill();
    if (pose === 'palm') {
      limb(ctx, x - 12, hipY - 24, x - 54, hipY - 40, 6, PAPER);
    } else if (pose === 'bow') {
      limb(ctx, x - 8, hipY - 20, x - 6, hipY + 20, 5, PAPER);
      limb(ctx, x + 8, hipY - 20, x + 8, hipY + 20, 5, PAPER);
    } else {
      limb(ctx, x - 14, hipY - 24, x - 36, hipY - 8, 5, PAPER);
      limb(ctx, x + 14, hipY - 24, x + 38, hipY - 12, 5, PAPER);
    }
  }

  function junPose() {
    const s = Dojo.skill;
    if (!s) return 'leopard';
    if (s.id === 'leopard') return 'leopard';
    if (s.id === 'tai_chi') return 'wave';
    if (s.id === 'surroundings') return Dojo.chosen || 'empty';
    if (s.id === 'spar') {
      if (!Dojo.bowedIn || (Dojo.palms >= 3 && !Dojo.bowedOut)) return 'bow';
      if (Dojo.palmFlash > 0) return 'palm';
      return 'empty';
    }
    return 'empty';
  }

  function partnerPose() {
    const s = Dojo.skill;
    if (s && s.id === 'spar') {
      if (!Dojo.bowedIn || (Dojo.palms >= 3 && !Dojo.bowedOut)) return 'bow';
      if (Dojo.palmFlash > 0) return 'palm';
      return 'ready';
    }
    return 'bow';
  }

  function paintCel(ctx, t) {
    const wdt = ctx.canvas.width;
    const h = ctx.canvas.height;
    ctx.fillStyle = '#120808';
    ctx.fillRect(0, 0, wdt, h);
    ctx.strokeStyle = 'rgba(227,28,35,0.28)';
    ctx.lineWidth = 2;
    for (let i = 0; i < 16; i++) {
      const y = (i * 18 + (t / 10) % 18);
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(wdt, y + 10);
      ctx.stroke();
    }
    ctx.fillStyle = '#1a1010';
    ctx.fillRect(0, h - 36, wdt, 36);
    ctx.strokeStyle = GOLD;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, h - 36);
    ctx.lineTo(wdt, h - 36);
    ctx.stroke();

    const floor = h - 38;
    drawJun(ctx, 210, floor, junPose(), t);
    drawPartner(ctx, 500, floor, partnerPose());
    if (!Dojo.chosen && Dojo.skill && Dojo.skill.id === 'surroundings') {
      drawBroom(ctx, 620, floor - 10);
      drawRibbon(ctx, 660, floor - 4, t);
      drawSand(ctx, 700, floor);
    }

    ctx.fillStyle = RED;
    ctx.font = '700 22px sans-serif';
    ctx.fillText(Dojo.skill ? Dojo.skill.name : '道場', 18, 32);
    ctx.fillStyle = GOLD;
    ctx.font = '13px sans-serif';
    ctx.fillText('SPEED RACER CEL · no sword tray · bow first', 18, 52);
    const m = Math.min(1, Dojo.motion * 8);
    ctx.fillStyle = m > 0.55 ? RED : TEAL;
    ctx.fillRect(18, 64, Math.max(4, m * 220), 8);
    ctx.fillStyle = PAPER;
    ctx.font = '12px sans-serif';
    ctx.fillText(m > 0.55 ? 'too fast for tai chi' : (m < 0.08 ? 'still / leopard' : 'slow wave'), 18, 88);
  }

  function rooted() {
    if (Dojo.spaceHeld || Dojo.squeezeHeld) return true;
    if (Dojo.camStream && Dojo.motion < 0.12) return true;
    return false;
  }

  function tick(t) {
    const c = $('fx');
    const ctx = c.getContext('2d');
    if (typeof ctx.roundRect !== 'function') {
      ctx.roundRect = function (x, y, w, h, r) {
        this.beginPath();
        this.rect(x, y, w, h);
      };
    }
    if (!Dojo.camStream) {
      Dojo.motion = Dojo.spaceHeld ? 0.02 : Dojo.motion * 0.82;
      if (Dojo.motion < 0.005) Dojo.motion = 0;
    }
    paintCel(ctx, t);
    const dt = Dojo.lastT ? t - Dojo.lastT : 16;
    Dojo.lastT = t;
    if (Dojo.palmFlash > 0) Dojo.palmFlash = Math.max(0, Dojo.palmFlash - dt);
    const s = Dojo.skill;
    if (s && s.kind === 'hold') {
      if (rooted()) Dojo.holdMs += dt;
      else Dojo.holdMs = Math.max(0, Dojo.holdMs - dt * 2);
      const need = (s.seconds || 20) * 1000;
      $('mot-n').textContent = Math.min(100, Math.round(Dojo.holdMs / need * 100)) + '% hold';
      if (Dojo.holdMs >= need) log('Leopard rooted. That was exercise. Bow.');
    }
    if (s && s.kind === 'slow_sequence') {
      const per = (s.seconds_per_count || 3) * 1000;
      const need = s.counts || 8;
      if (Dojo.camStream && Dojo.motion > 0.08 && Dojo.motion < 0.45) {
        Dojo.waveMs += dt;
        if (Dojo.waveMs >= per) {
          Dojo.waveMs = 0;
          Dojo.waveCounts = Math.min(need, Dojo.waveCounts + 1);
        }
      }
      $('mot-n').textContent = Dojo.waveCounts + ' / ' + need;
      if (Dojo.waveCounts >= need) log('Tai chi wave complete. Slow on purpose.');
      if (Dojo.motion > 0.6) log('Too fast. Tai chi is not a punch. Reset your breath.');
    }
    if (s && s.kind === 'choose') {
      $('mot-n').textContent = Dojo.chosen ? Dojo.chosen : 'pick the room';
    }
    if (s && s.kind === 'spar') {
      const n = s.exchanges || 3;
      if (!Dojo.bowedIn) $('mot-n').textContent = 'bow first';
      else if (Dojo.palms < n) $('mot-n').textContent = 'palm ' + Dojo.palms + ' / ' + n;
      else if (!Dojo.bowedOut) $('mot-n').textContent = 'bow after';
      else $('mot-n').textContent = 'spar done';
    }
    if (!s) $('mot-n').textContent = 'still';
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
      if (!opts.length) return;
      const cur = opts.indexOf(Dojo.chosen);
      const i = cur < 0 ? 0 : (cur + 1) % opts.length;
      choose(opts[i]);
      return;
    }
    if (s.kind === 'spar') {
      const n = s.exchanges || 3;
      if (g === 'squeeze') {
        if (!Dojo.bowedIn) {
          Dojo.bowedIn = true;
          log('Bow. Now three palms — click, not a flurry.');
        } else if (Dojo.palms >= n && !Dojo.bowedOut) {
          Dojo.bowedOut = true;
          log('Bow after. Cartoon. Nobody is wasted.');
        } else {
          log('Palms are click. Squeeze is the bow.');
        }
        return;
      }
      if (g === 'click') {
        if (!Dojo.bowedIn) {
          log('Bow first. Squeeze is the bow.');
          return;
        }
        if (Dojo.palms >= n) {
          log('Three already. Squeeze to bow after.');
          return;
        }
        Dojo.palms += 1;
        Dojo.palmFlash = 280;
        log('Palm ' + Dojo.palms + ' / ' + n + '. Cartoon.');
        return;
      }
    }
    if (s.kind === 'hold' && g === 'squeeze') {
      Dojo.squeezeHeld = true;
      Dojo.holdMs += 2000;
      log('Rooted a little more. Squeeze is the stance.');
      setTimeout(() => { Dojo.squeezeHeld = false; }, 400);
    }
    if (s.kind === 'slow_sequence' && g === 'twist') {
      const now = performance.now();
      if (Dojo.lastTwistAt && now - Dojo.lastTwistAt < 500) {
        log('Too fast. Tai chi is not a punch. Reset your breath.');
        Dojo.lastTwistAt = now;
        return;
      }
      Dojo.lastTwistAt = now;
      const need = s.counts || 8;
      if (Dojo.waveCounts < need) Dojo.waveCounts += 1;
      log('Wave count from the hand. Slow. ' + Dojo.waveCounts + ' / ' + need);
      if (Dojo.waveCounts >= need) log('Tai chi wave complete. Slow on purpose.');
    }
  }

  fetch('engine/storyboard.json')
    .then((r) => r.json())
    .then((board) => {
      Dojo.board = board;
      paintBeats();
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
    if (ev.repeat && ev.key !== ' ') return;
    if (ev.key === '1' || ev.key === '2' || ev.key === '3' || ev.key === '4') {
      pick(Number(ev.key) - 1);
      return;
    }
    if (ev.key === 'q' || ev.key === 'Q' || ev.key === 'e' || ev.key === 'E') onPen('twist');
    if (ev.key === 'Enter') { ev.preventDefault(); onPen('click'); }
    if (ev.key === 'f' || ev.key === 'F') onPen('squeeze');
    if (ev.key === ' ') {
      ev.preventDefault();
      Dojo.spaceHeld = true;
      Dojo.motion = 0.02;
      if (!ev.repeat) onPen('squeeze');
    }
  });
  window.addEventListener('keyup', (ev) => {
    if (ev.key === ' ') Dojo.spaceHeld = false;
  });

  w.KurotoDojo = Dojo;
})(window);
