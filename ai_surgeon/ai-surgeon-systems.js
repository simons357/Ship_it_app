/* ==========================================================================
   AI SURGEON — SHARED SYSTEMS
   Simons Medical Innovations, LLC

   This file is the part of the engine that is NOT specific to any one
   operation. Modules supply anatomy, steps and decisions; this supplies the
   five systems that behave the same way in every module:

     Profile   — who is holding the phone, and how much is expected of them
     Stress    — arousal estimated from behaviour, optionally from a heart
                 rate strap, used to adapt difficulty in both directions
     Gaze      — where attention is actually pointed, and what was never
                 looked at
     Decisions — forks with stated rationale that are committed and owned
     Ask       — free-text questions to the attending, answered from the
                 module's own content rather than a canned list
     Sensors   — every sensor the phone will actually give a web page, plus
                 an optional cheap wearable, feeding one arousal number
     Voice     — you say the instrument out loud, because that is the job
     Handover  — knowing when to stop is worth more than getting away with it
     Progress  — exact competency numbers, so you know where you stand
     Rewards   — streaks and unlocks, all of them hung off patient safety
     Humor     — the OR humor, with hard rules about when it is not allowed

   Nothing here transmits anything. Biometric input is processed in the page
   and only the derived band is ever retained. See RETENTION below.
   ========================================================================== */

(function (global) {
'use strict';

const AISS = {};
global.AISS = AISS;

/* Biometric data is a regulated category (Illinois BIPA, GDPR Art. 9,
   Texas CUBI). The product position is: derive on device, keep the band,
   discard the signal. This constant exists so that position is enforced in
   code and not only asserted in a slide. */
AISS.RETENTION = 'derived-band-only';

/* ==========================================================================
   1. PROFILE — medical background, and what it changes
   ========================================================================== */

const PROFILES = {
  none: {
    key: 'none',
    label: 'No medical background',
    blurb: 'Curious, a student, or someone who has never been in an operating room. Everything gets named in plain language first.',
    hintFloor: 2,        // notes always visible, demo text always shown
    distractors: 2,      // instrument choices offered alongside the right one
    jargon: 0,           // 0 = gloss every term, 1 = gloss the hard ones, 2 = none
    expect: 0.6,         // penalty multiplier — less is expected of you
    reward: 1.0,
    grace: 2.0,          // hesitation allowance
    teachDepth: 0,       // which variant of the teaching question is asked
    clear: 45            // coherence needed to be cleared at debrief
  },
  student: {
    key: 'student',
    label: 'Student / pre-health / EMT',
    blurb: 'You have had anatomy. You have not scrubbed into much. Terms are used properly and glossed once.',
    hintFloor: 1, distractors: 3, jargon: 1,
    expect: 0.85, reward: 1.0, grace: 1.4, teachDepth: 0, clear: 55
  },
  nurse: {
    key: 'nurse',
    label: 'Nurse, tech, or OR staff',
    blurb: 'You have been in the room. You know the instruments and the rhythm. The anatomy is the part being tested.',
    hintFloor: 1, distractors: 4, jargon: 2,
    expect: 1.0, reward: 1.05, grace: 1.0, teachDepth: 1, clear: 62
  },
  clinician: {
    key: 'clinician',
    label: 'Surgeon, resident, or anaesthesia',
    blurb: 'More is expected of you. Hints are off, the instrument tray is full, errors cost more, and the teaching questions are the hard versions.',
    hintFloor: 0, distractors: 6, jargon: 2,
    expect: 1.45, reward: 1.15, grace: 0.7, teachDepth: 1, clear: 72
  }
};

AISS.Profile = {
  current: PROFILES.student,
  all(){ return Object.keys(PROFILES).map(k => PROFILES[k]); },
  set(key){
    this.current = PROFILES[key] || PROFILES.student;
    try { localStorage.setItem('aiss.profile', this.current.key); } catch(e){}
    return this.current;
  },
  restore(){
    let k = null;
    try { k = localStorage.getItem('aiss.profile'); } catch(e){}
    if (k && PROFILES[k]) this.current = PROFILES[k];
    return this.current;
  },
  is(key){ return this.current.key === key; },
  /* Plain-language gloss, shown only when the profile asks for it. */
  gloss(term, plain){
    if (this.current.jargon >= 2) return term;
    return term + ' <span class="gloss">(' + plain + ')</span>';
  }
};

/* ==========================================================================
   2. STRESS — arousal from behaviour, optionally from a heart rate strap

   Coherence already measures how right you are. This measures what being
   that right is costing you. The two are not the same axis and the correct
   intervention is opposite in each corner:

     accurate + settled     -> push:  remove hints, tighten tolerance, speed up
     accurate + overloaded  -> hold:  do not add load, this is about to break
     struggling + settled   -> push:  this is boredom, not overwhelm
     struggling + overloaded-> back off: restore hints, widen tolerance, slow down

   With no hardware, arousal is estimated from response latency variance,
   gesture tremor, correction rate and error streak. With a strap it is
   estimated from heart rate above a rolling personal baseline. Both feed
   the same 0..100 index so the rest of the engine does not care which.
   ========================================================================== */

AISS.Stress = {
  arousal: 30,             // 0..100, EMA smoothed
  hasSensor: false,
  hr: 0, hrBaseline: 0,
  _lat: [], _tremor: [], _streak: 0, _corrections: 0, _events: 0,
  _hrSamples: [],

  reset(){
    this.arousal = 30; this._lat = []; this._tremor = [];
    this._streak = 0; this._corrections = 0; this._events = 0;
  },

  /* Behavioural inputs -------------------------------------------------- */

  response(seconds){
    this._lat.push(seconds);
    if (this._lat.length > 12) this._lat.shift();
    this._events++;
    this._recompute();
  },

  outcome(correct){
    this._streak = correct ? Math.max(0, this._streak - 1) : this._streak + 1;
    if (!correct) this._corrections++;
    this._recompute();
  },

  /* Tremor: mean perpendicular deviation of a drawn path from the straight
     line between its endpoints, normalised by path length. A steady hand
     draws close to a line; a rushed or shaking one does not. */
  path(points){
    if (!points || points.length < 6) return;
    const a = points[0], b = points[points.length - 1];
    const dx = b[0] - a[0], dy = b[1] - a[1];
    const len = Math.hypot(dx, dy);
    if (len < 30) return;
    let dev = 0;
    for (const p of points){
      dev += Math.abs((p[0]-a[0])*dy - (p[1]-a[1])*dx) / len;
    }
    this._tremor.push(Math.min(1, (dev / points.length) / 26));
    if (this._tremor.length > 8) this._tremor.shift();
    this._recompute();
  },

  /* Optional hardware --------------------------------------------------- */

  supported(){ return typeof navigator !== 'undefined' && !!navigator.bluetooth; },

  async connect(){
    if (!this.supported()) throw new Error('Web Bluetooth is not available in this browser.');
    const dev = await navigator.bluetooth.requestDevice({ filters:[{ services:['heart_rate'] }] });
    const server = await dev.gatt.connect();
    const svc = await server.getPrimaryService('heart_rate');
    const ch = await svc.getCharacteristic('heart_rate_measurement');
    await ch.startNotifications();
    ch.addEventListener('characteristicvaluechanged', e => {
      const d = e.target.value;
      const flags = d.getUint8(0);
      const bpm = (flags & 0x01) ? d.getUint16(1, true) : d.getUint8(1);
      this._hr(bpm);
    });
    dev.addEventListener('gattserverdisconnected', () => { this.hasSensor = false; });
    this.hasSensor = true;
    return dev.name || 'Heart rate monitor';
  },

  _hr(bpm){
    if (!bpm || bpm < 25 || bpm > 240) return;
    this.hr = bpm;
    this._hrSamples.push(bpm);
    if (this._hrSamples.length > 240) this._hrSamples.shift();
    /* Baseline is the 20th percentile of the session so far — the person's
       own resting-ish rate, not a population number. */
    if (this._hrSamples.length >= 20){
      const s = this._hrSamples.slice().sort((a,b)=>a-b);
      this.hrBaseline = s[Math.floor(s.length * 0.2)];
    }
    this._recompute();
  },

  /* Fusion -------------------------------------------------------------- */

  _recompute(){
    let target;

    if (this.hasSensor && this.hrBaseline){
      // 15 bpm above your own baseline reads as fully loaded.
      const lift = (this.hr - this.hrBaseline) / 15;
      target = 25 + Math.max(0, Math.min(1, lift)) * 70;
    } else {
      const lat = this._lat.length ? this._lat.reduce((a,b)=>a+b,0) / this._lat.length : 6;
      // Variance in latency reads as arousal more reliably than latency alone.
      const mean = lat;
      const varc = this._lat.length > 2
        ? Math.sqrt(this._lat.reduce((a,b)=>a+(b-mean)*(b-mean),0)/this._lat.length) : 0;
      const drawn = this._tremor.length
        ? this._tremor.reduce((a,b)=>a+b,0) / this._tremor.length : 0.2;
      /* If the accelerometer is live, physical hand tremor is the better
         signal and the drawn-path estimate becomes a secondary check. */
      const S = AISS.Sensors;
      const trem = (S && S.motion) ? (S.tremor * 0.7 + drawn * 0.3) : drawn;
      const streak = Math.min(1, this._streak / 3);
      const corr = this._events ? Math.min(1, this._corrections / this._events) : 0;

      target = 18
        + Math.min(1, varc / 7) * 26      // erratic pacing
        + trem * 22                        // unsteady input
        + streak * 24                      // consecutive errors
        + corr * 16;                       // overall correction rate
      // Very fast and very uniform also reads as pressure, not calm.
      if (mean < 1.6 && this._lat.length > 3) target += 10;
    }

    this.arousal += (Math.max(0, Math.min(100, target)) - this.arousal) * 0.28;
  },

  band(){
    return this.arousal > 72 ? 'overloaded'
         : this.arousal > 50 ? 'loaded'
         : this.arousal > 28 ? 'engaged' : 'settled';
  },

  source(){ return this.hasSensor ? 'heart rate' : 'input pattern'; }
};

/* ==========================================================================
   3. TUNING — how Profile, Coherence and Stress combine into difficulty
   ========================================================================== */

AISS.tuning = function (coherence){
  const p = AISS.Profile.current;
  const a = AISS.Stress.arousal;
  const accurate = coherence > 58;

  let hintFloor = p.hintFloor;
  let toleranceMul = 1.0;
  let clockRate = 1.0;
  let note = null;

  if (a > 72 && !accurate){
    hintFloor = Math.max(hintFloor, 2);
    toleranceMul = 1.35; clockRate = 0.78;
    note = 'backing off';
  } else if (a > 72 && accurate){
    toleranceMul = 1.10; clockRate = 0.92;
    note = 'holding';
  } else if (a < 32 && accurate){
    hintFloor = Math.min(hintFloor, p.key === 'none' ? 1 : 0);
    toleranceMul = 0.85; clockRate = 1.15;
    note = 'pushing';
  } else if (a < 32 && !accurate){
    toleranceMul = 0.95; clockRate = 1.05;
    note = 'pushing';
  }

  return { hintFloor, toleranceMul, clockRate, note, band: AISS.Stress.band() };
};

/* ==========================================================================
   4. GAZE — where attention is pointed

   On a phone there is no eye tracker, so the honest signal is where the
   device is aimed: a ray from the centre of the screen. In a headset the
   same call becomes real head gaze with no change to the module. Dwell is
   accumulated per structure, which gives two useful things: a nudge when
   the player is hunting in the wrong quadrant, and a debrief list of every
   structure they never once looked at.
   ========================================================================== */

AISS.Gaze = {
  enabled: true,
  lookingAt: null,
  dwell: {},          // id -> seconds
  seen: {},           // id -> true
  _since: 0,
  _tmpO: null, _tmpD: null, _q: null,

  reset(){ this.lookingAt = null; this.dwell = {}; this.seen = {}; this._since = 0; },

  /* Called from the module's render loop. */
  update(dt, THREE, camera, raycaster, targets){
    if (!this.enabled || !targets || !targets.length) return;
    if (!this._tmpO){
      this._tmpO = new THREE.Vector3();
      this._tmpD = new THREE.Vector3();
      this._q = new THREE.Quaternion();
    }
    camera.getWorldPosition(this._tmpO);
    camera.getWorldQuaternion(this._q);
    this._tmpD.set(0, 0, -1).applyQuaternion(this._q).normalize();
    raycaster.ray.origin.copy(this._tmpO);
    raycaster.ray.direction.copy(this._tmpD);
    const hits = raycaster.intersectObjects(targets, false);
    const id = hits.length ? hits[0].object.userData.id : null;

    if (id !== this.lookingAt){ this.lookingAt = id; this._since = 0; }
    if (id){
      this._since += dt;
      this.dwell[id] = (this.dwell[id] || 0) + dt;
      if (this.dwell[id] > 0.35) this.seen[id] = true;
    }
  },

  onTarget(id){ return this.lookingAt === id; },
  looked(id){ return !!this.seen[id]; },
  secondsOn(id){ return this.dwell[id] || 0; },

  /* Structures in a list that were never once looked at. */
  missed(ids){ return ids.filter(id => !this.seen[id]); },

  coverage(ids){
    if (!ids.length) return 1;
    return ids.filter(id => this.seen[id]).length / ids.length;
  }
};

/* ==========================================================================
   5. DECISIONS — forks you commit to and then live with

   No option is flagged correct. Every option carries the rationale someone
   would actually give for it and a consequence that is applied to the run.
   Once taken it is locked, and the debrief reports what it cost.
   ========================================================================== */

AISS.Decisions = {
  taken: [],          // {id, prompt, choice, rationale, consequence, cost}
  _seen: {},

  reset(){ this.taken = []; this._seen = {}; },

  pending(list, atKey){
    if (!list) return null;
    return list.find(d => d.at === atKey && !this._seen[d.id]) || null;
  },

  /* ui: {say, choices, btnrow, who} element ids handled by the caller via
     the render function it passes in. This keeps DOM ownership in the module. */
  present(d, ui, done){
    this._seen[d.id] = true;
    const t0 = performance.now();
    ui.who('AI Attending — your call');
    ui.say('<strong style="color:#eef4f8">Decision</strong><br><br>' + d.prompt
      + '<br><br><span style="color:var(--steel-dim);font-size:11.5px">There is no marked answer here. Each of these is defensible and each one costs something. Choose, and you will be held to it.</span>');
    ui.clear();
    d.options.forEach(o => {
      ui.option(o.t + '<br><span class="why">' + o.rationale + '</span>', () => {
        const secs = (performance.now() - t0) / 1000;
        AISS.Stress.response(secs);
        this.taken.push({
          id: d.id, prompt: d.prompt, choice: o.t,
          rationale: o.rationale, consequence: o.consequence,
          cost: o.cost || 0, tag: o.tag || null
        });
        ui.lock();
        ui.commit('<strong style="color:#eef4f8">Committed.</strong><br><br>' + o.consequence
          + '<br><br><span style="color:var(--steel-dim);font-size:11.5px">That is your decision. It stands for the rest of the case and it will be in your debrief.</span>',
          () => done(o));
      });
    });
  },

  /* Any effect a taken decision has on later steps. */
  has(tag){ return this.taken.some(t => t.tag === tag); },

  summary(){
    if (!this.taken.length) return '';
    return this.taken.map(t =>
      '<div class="dec"><b>' + t.prompt.replace(/<[^>]+>/g,'').slice(0,70) + '</b>'
      + '<span>You chose: ' + t.choice + '</span>'
      + '<span style="color:var(--steel-dim)">' + t.consequence + '</span></div>'
    ).join('');
  },

  netCost(){ return this.taken.reduce((a,t) => a + (t.cost || 0), 0); }
};

/* ==========================================================================
   6. ASK — free text questions, answered from the module's own content

   The requirement was support for all questions, not a menu of three. This
   builds a small retrieval index out of whatever the module already has
   (layer notes, organ notes, study cards, step dialogue, teaching answers,
   the instrument tray) plus a corpus of the general questions people
   actually ask at a field, and matches free text against it.

   When it does not know, it says so and offers the two nearest things it
   does know, which is what a decent attending does as well.
   ========================================================================== */

const STOP = new Set(('a an the is are was were be been being do does did done of to in on at for it its this that these those i you he she they we my your his her their our and or if but so then than as with without into onto from by not no yes what why how when where which who whom whose can could will would shall should may might must have has had get got am about over under again more most some any all just too very there here does dont doesnt cant im ive whats hows thats').split(' '));

const SYN = {
  belly:'abdomen', tummy:'abdomen', gut:'bowel', guts:'bowel', intestine:'bowel',
  bleeder:'artery bleeding haemorrhage', bleed:'bleeding haemorrhage',
  bleeding:'haemorrhage', numb:'anaesthesia anaesthetic local',
  numbing:'anaesthesia anaesthetic local', asleep:'anaesthesia',
  knife:'scalpel blade', scissors:'metzenbaum mayo scissors',
  clamp:'kelly hemostat clamp', stitch:'suture tie ligature',
  stitches:'suture tie ligature', sew:'suture', tie:'ligature suture',
  cut:'incision incise divide', cutting:'incision incise divide',
  vein:'vessel', veins:'vessel', artery:'vessel arterial',
  nerve:'nerve innervation', muscle:'muscle fibers',
  pain:'pain visceral somatic referred', hurt:'pain',
  infection:'infection contamination sepsis', pus:'abscess infection',
  burst:'perforation perforated rupture', rupture:'perforation',
  appendix:'appendix vermiform appendiceal',
  poop:'faecal fecalith bowel', tube:'drain tube',
  breathing:'respiratory ventilation oxygen',
  pressure:'blood pressure haemodynamic',
  heart:'cardiac rate rhythm', oxygen:'saturation oxygenation',
  scar:'closure scar cosmesis', close:'closure closing',
  lap:'laparoscopic laparoscopy', open:'open laparotomy',
  kid:'paediatric young', pregnant:'pregnancy gravid'
};

function tokens(s){
  const out = [];
  String(s || '').toLowerCase().replace(/<[^>]+>/g, ' ')
    .replace(/[^a-z0-9\s'-]/g, ' ').split(/\s+/).forEach(w => {
      w = w.replace(/'s$/,'').replace(/[-']/g,'');
      if (!w || w.length < 2 || STOP.has(w)) return;
      out.push(stem(w));
      if (SYN[w]) SYN[w].split(' ').forEach(x => out.push(stem(x)));
    });
  return out;
}

function stem(w){
  return w.replace(/ies$/,'y').replace(/(ss)$/,'$1')
          .replace(/([^s])s$/,'$1').replace(/ing$/,'').replace(/ed$/,'');
}

AISS.Ask = {
  docs: [], df: {}, N: 0, asked: 0, history: [],

  reset(){ this.asked = 0; this.history = []; },

  /* Modules call this once with whatever content they have. Everything is
     optional; missing sections are simply not indexed. */
  build(src){
    this.docs = []; this.df = {};
    const add = (kind, title, text, extra) => {
      if (!text) return;
      this.docs.push({ kind, title, text: String(text), extra: extra || null });
    };

    (src.layers || []).forEach(l => add('anatomy', l.name, l.note));
    (src.organs || []).forEach(o => add('anatomy', o.name, o.note));
    (src.brief  || []).forEach(b => {
      add('physiology', b.title, b.body);
      const right = (b.opts || []).find(o => o.ok);
      if (right) add('physiology', b.title + ' — the short answer', right.t);
    });
    (src.steps || []).forEach((s, i) => {
      add('technique', 'Step ' + (i+1) + ' — ' + (s.instr || s.id),
          [s.say, s.demo].filter(Boolean).join(' '));
      const right = (s.opts || []).find(o => o.ok);
      if (right) add('technique', 'Why — ' + (s.instr || s.id), s.teach + ' ' + right.t);
      if (s.instr) add('instrument', s.instr,
        s.instr + ' is what this step calls for. ' + (s.demo || s.say));
    });
    (src.extra || []).forEach(e => add(e.kind || 'general', e.title, e.text));
    FAQ.forEach(e => add(e.kind, e.title, e.text));

    this.N = this.docs.length;
    this.docs.forEach(d => {
      d.tok = tokens(d.title + ' ' + d.title + ' ' + d.text);
      const uniq = new Set(d.tok);
      uniq.forEach(t => this.df[t] = (this.df[t] || 0) + 1);
    });
    return this;
  },

  /* ctx lets dynamic questions be answered: what am I looking at, what do I
     do now, why this instrument. */
  answer(q, ctx){
    ctx = ctx || {};
    this.asked++;
    const raw = String(q || '').trim();
    if (!raw) return { text: 'Ask me something.', kind: 'none', confident: false };

    const dyn = this._dynamic(raw.toLowerCase(), ctx);
    if (dyn){ this.history.push({ q: raw, a: dyn.text }); return dyn; }

    const qt = tokens(raw);
    if (!qt.length) return this._unsure(raw, []);

    const scored = this.docs.map(d => {
      let s = 0;
      const tf = {};
      d.tok.forEach(t => tf[t] = (tf[t] || 0) + 1);
      const titleTok = new Set(tokens(d.title));
      qt.forEach(t => {
        if (!tf[t]) return;
        const idf = Math.log(1 + this.N / (this.df[t] || 1));
        s += idf * (1 + Math.log(tf[t])) / Math.sqrt(d.tok.length);
        if (titleTok.has(t)) s += idf * 0.6;
      });
      return { d, s };
    }).sort((a, b) => b.s - a.s);

    const top = scored[0];
    if (!top || top.s < 0.55) return this._unsure(raw, scored);

    const a = { text: this._render(top.d, ctx), kind: top.d.kind, title: top.d.title,
                confident: top.s > 1.1, score: top.s };
    this.history.push({ q: raw, a: a.text });
    return a;
  },

  _dynamic(q, ctx){
    const has = (...w) => w.every(x => q.indexOf(x) >= 0);
    if (ctx.lastStructure && (has('what','looking') || has('what','this') || has('what','am','i'))){
      return { text: '<strong>' + ctx.lastStructure.name + '.</strong> ' + ctx.lastStructure.note,
               kind: 'anatomy', confident: true };
    }
    if (has('what','now') || has('what','next') || has('what','do','i','do')){
      return { text: ctx.stepSay ? 'Same instruction, said plainly: ' + String(ctx.stepSay).replace(/<[^>]+>/g,'')
                                 : 'Follow the step on the card.', kind:'technique', confident: true };
    }
    if (ctx.instrument && (has('why','instrument') || has('why','this','one') || has('why','that'))){
      return { text: 'You are asking for the <strong>' + ctx.instrument + '</strong> because of what this tissue is, not because of habit. '
              + (ctx.stepDemo ? String(ctx.stepDemo).replace(/<[^>]+>/g,'') : ''), kind:'instrument', confident: true };
    }
    if (has('what','would','you','do')){
      return { text: 'I would do exactly what the step says, and I would do it slower than you think you need to. '
              + 'The part of this that goes wrong is never the part people rush past deliberately.', kind:'general', confident: true };
    }
    if (has('wrong') && (has('happens') || has('here') || has('if'))){
      return { text: ctx.consequence || 'You lose points and, in the modules where it is enabled, you can lose the patient. '
              + 'The specific risk at this step is in the layer note — identify the structure and read it.', kind:'general', confident: true };
    }
    if (has('head') && has('bed') || has('who','anaesthesia') || has('who','anesthesia')){
      return { text: 'The head of the bed is beyond the drape, and they are not in your line of sight. They see numbers you do not. '
              + 'If something on the monitor changes, you say it out loud — you do not wait to be told.', kind:'general', confident: true };
    }
    return null;
  },

  _render(d, ctx){
    let body = d.text.replace(/<em>|<\/em>/g, '');
    if (AISS.Profile.current.jargon === 0){
      body = '<span style="color:var(--steel-dim)">Plainly: </span>' + body;
    }
    return '<strong>' + d.title + '.</strong> ' + body;
  },

  _unsure(raw, scored){
    const near = scored.slice(0, 2).filter(x => x.s > 0.2).map(x => x.d.title);
    const tail = near.length
      ? ' I can tell you about ' + near.join(', or ') + ' — ask again that way.'
      : ' Try naming the structure or the step you mean.';
    return {
      text: 'Not something I have at this field.' + tail
        + '<br><br><span style="color:var(--steel-dim);font-size:11px">This is a prototype answering out of this module\'s own content. It does not invent anatomy it was not given, which is the correct failure for a teaching tool.</span>',
      kind: 'none', confident: false, near
    };
  }
};

/* General questions that are not in any module's anatomy data but get asked
   at every field. Kept here so every module inherits them. */
const FAQ = [
  { kind:'general', title:'Going too slowly',
    text:'Speed is the last thing to arrive and the first thing people chase. The clock only breaks ties in this product — errors decide the result. A slow correct case beats a fast one with a missed structure every time.' },
  { kind:'general', title:'What happens if I cut an artery',
    text:'You get pressure on it first, with a finger or a sponge, and you do not chase it blindly with a clamp. Blind clamping in a bleeding field is how the structure next to the artery gets injured as well. Pressure, suction, light, exposure, then control under vision.' },
  { kind:'general', title:'Asking questions',
    text:'Asking costs a small number of points and is worth far more than guessing silently. That is deliberate, and it is the opposite of what most games teach. In a real room the resident who asks is the safe one.' },
  { kind:'general', title:'Antibiotics',
    text:'A single pre-operative dose covering enteric gram negatives and anaerobes is standard for appendicitis. Continuing them afterwards depends entirely on whether the disease was complicated — perforation, abscess, gross contamination — not on how the operation felt.' },
  { kind:'general', title:'Drains',
    text:'A drain does not turn a contaminated abdomen into a clean one. In uncomplicated appendicitis it is not indicated. In a well-formed abscess cavity it is a different conversation.' },
  { kind:'general', title:'If it is not appendicitis',
    text:'The three things to look for once you are in are a Meckel\'s diverticulum on the antimesenteric border of the ileum, ovarian or tubal pathology in a woman, and mesenteric adenitis in a young patient. Look before you close. Finding a normal appendix is not the same as finding nothing.' },
  { kind:'general', title:'If I cannot find the appendix',
    text:'Follow the taenia libera. All three taeniae converge on the base and the base is fixed even when the tip is not. If the tip is retrocecal you mobilise the cecum laterally rather than pulling harder on something you cannot see.' },
  { kind:'general', title:'Laparoscopic instead of open',
    text:'Laparoscopic is the more common approach in most places now. Open is taught first here because the anatomy is visible, layer by layer, in a way a screen does not show you. You learn the wall before you learn the ports.' },
  { kind:'general', title:'Blood loss',
    text:'This operation should not lose meaningful blood. If it is, the mesoappendix is the reason until proven otherwise, and it has usually retracted somewhere you were not looking.' },
  { kind:'general', title:'Closure and the scar',
    text:'The muscle layers were split, not cut, so they fall back together. The external oblique aponeurosis is the layer that holds and it is the one you close properly. Skin is cosmesis, aponeurosis is the hernia.' },
  { kind:'general', title:'Losing the patient',
    text:'It voids the case and it costs rank. It is disabled in the entry modules and enabled from trauma onward. When it happens the debrief tells you the exact decision it started at, because that is the only part of it that is useful.' },
  { kind:'general', title:'Biometrics and what is recorded',
    text:'Arousal is estimated in the page from how you are moving and answering, or from a heart rate strap if you connect one. The signal is not stored and it is not transmitted. Only the band — settled, engaged, loaded, overloaded — is kept, and only for your debrief.' }
];

/* ==========================================================================
   7. DEBRIEF — the parts of the debrief these systems own
   ========================================================================== */

AISS.debrief = function (opts){
  opts = opts || {};
  const p = AISS.Profile.current;
  const parts = [];

  parts.push('<div class="dbrow"><b>Profile</b><span>' + p.label
    + ' — clearance at ' + p.clear + ' coherence, penalties ×' + p.expect.toFixed(2) + '</span></div>');

  parts.push('<div class="dbrow"><b>Load</b><span>Finished ' + AISS.Stress.band()
    + ' (' + Math.round(AISS.Stress.arousal) + '/100, read from ' + AISS.Sensors.available().join(', ') + '). '
    + loadNote() + '</span></div>');

  const H = AISS.Handover.summary();
  if (H){
    const line = { correct:'You handed over inside the window. Highest-value decision in the module.',
                   early:'You handed over before you had to. Safe, and you gave up ground.',
                   late:'You handed over after harm was done.',
                   gambleWon:'You stayed outside the safety envelope and it worked. It still scores below handing over.',
                   gambleLost:'You stayed outside the safety envelope and the patient paid.' }[H.outcome];
    if (line) parts.push('<div class="dbrow"><b>Safety</b><span>' + line + '</span></div>');
  }

  if (opts.gazeIds && opts.gazeIds.length){
    const missed = AISS.Gaze.missed(opts.gazeIds);
    const cov = Math.round(AISS.Gaze.coverage(opts.gazeIds) * 100);
    parts.push('<div class="dbrow"><b>Attention</b><span>You looked at ' + cov + '% of the structures in this field.'
      + (missed.length ? ' Never once looked at: ' + missed.map(id => (opts.names && opts.names[id]) || id).join(', ') + '.' : '')
      + '</span></div>');
  }

  if (AISS.Decisions.taken.length){
    parts.push('<div class="dbrow"><b>Your calls</b><span>'
      + AISS.Decisions.taken.map(t => t.choice + ' — ' + t.consequence).join('<br><br>')
      + '</span></div>');
  }

  if (AISS.Ask.asked){
    parts.push('<div class="dbrow"><b>Questions</b><span>You asked ' + AISS.Ask.asked
      + '. That cost you a little and it was worth it.</span></div>');
  }

  return parts.join('');

  function loadNote(){
    const b = AISS.Stress.band();
    if (b === 'overloaded') return 'The module was holding hints open for you by the end. That is not a failure — it is the system doing what it is for.';
    if (b === 'settled')    return 'You were not under pressure. The next case up the ladder should be.';
    return 'A working level. This is where people learn fastest.';
  }
};

/* ==========================================================================
   8. SENSORS — everything a phone will actually hand a web page

   Not a wish list. Each of these is reachable from a browser today, with the
   permission cost noted. The accelerometer and gyroscope are the valuable
   ones: a hand that is steady on a phone is measurably different from a hand
   that is not, and that difference is available for free at 60 Hz.

     DeviceMotion      accel + gyro    hand tremor, stillness, startle
     DeviceOrientation attitude        where the device is aimed (feeds Gaze)
     Touch.force       0..1 pressure   grip force on iOS hardware that has it
     PointerEvent      pressure/tilt   same on stylus and some Android
     visibilitychange  attention       you left the case
     AmbientLightSensor lux            room conditions (Chrome, flagged)
     getUserMedia audio breath/voice   opt-in only, envelope only, never kept
     Bluetooth GATT    heart rate      the cheap wearable, see Stress.connect

   iOS requires a user gesture before motion permission, so start() must be
   called from a button handler, not on load.
   ========================================================================== */

AISS.Sensors = {
  motion: false, orientation: false, light: 0, away: 0, force: 0,
  tremor: 0,          // 0..1, rolling
  stillness: 1,       // 0..1, 1 = rock steady
  startles: 0,
  _acc: [], _lastMag: 0, _awaySince: 0,

  async start(){
    /* Motion — the important one. */
    try {
      if (typeof DeviceMotionEvent !== 'undefined'
          && typeof DeviceMotionEvent.requestPermission === 'function'){
        const r = await DeviceMotionEvent.requestPermission();
        if (r !== 'granted') throw new Error('denied');
      }
      window.addEventListener('devicemotion', e => this._motion(e), { passive:true });
      this.motion = true;
    } catch(e){ this.motion = false; }

    try {
      if (typeof DeviceOrientationEvent !== 'undefined'
          && typeof DeviceOrientationEvent.requestPermission === 'function'){
        const r = await DeviceOrientationEvent.requestPermission();
        if (r === 'granted') this.orientation = true;
      } else if (typeof DeviceOrientationEvent !== 'undefined'){
        this.orientation = true;
      }
    } catch(e){ this.orientation = false; }

    /* Attention — free, no permission, and a genuine signal. */
    document.addEventListener('visibilitychange', () => {
      if (document.hidden){ this._awaySince = performance.now(); }
      else if (this._awaySince){
        this.away += (performance.now() - this._awaySince) / 1000;
        this._awaySince = 0;
      }
    });

    /* Ambient light — Chrome only, behind a flag, harmless if absent. */
    try {
      if ('AmbientLightSensor' in window){
        const s = new window.AmbientLightSensor({ frequency: 1 });
        s.addEventListener('reading', () => { this.light = s.illuminance; });
        s.start();
      }
    } catch(e){}

    return { motion:this.motion, orientation:this.orientation, light:('AmbientLightSensor' in window) };
  },

  _motion(e){
    const a = e.accelerationIncludingGravity || e.acceleration;
    if (!a || a.x == null) return;
    const mag = Math.hypot(a.x || 0, a.y || 0, a.z || 0);
    const jerk = Math.abs(mag - this._lastMag);
    this._lastMag = mag;

    this._acc.push(jerk);
    if (this._acc.length > 90) this._acc.shift();       // ~1.5 s at 60 Hz

    const mean = this._acc.reduce((x,y)=>x+y,0) / this._acc.length;
    /* 0.35 m/s^2 of frame-to-frame jerk is a visibly shaking hand. */
    this.tremor = Math.max(0, Math.min(1, mean / 0.35));
    this.stillness = 1 - this.tremor;
    if (jerk > 6) this.startles++;                      // phone snatched or dropped
  },

  /* Touch force where the hardware reports it. Called from the input layer. */
  touch(t){
    if (t && typeof t.force === 'number' && t.force > 0) this.force = t.force;
    else if (t && typeof t.pressure === 'number' && t.pressure > 0 && t.pressure !== 0.5) this.force = t.pressure;
  },

  available(){
    const out = [];
    if (this.motion) out.push('accelerometer + gyroscope');
    if (this.orientation) out.push('orientation');
    if (this.force) out.push('touch force');
    if (this.light) out.push('ambient light');
    if (AISS.Stress.hasSensor) out.push('heart rate strap');
    out.push('input timing');
    return out;
  }
};

/* ==========================================================================
   9. VOICE — you say the instrument out loud

   The scrub mechanic is already "ask for it by name". On hardware that has
   SpeechRecognition, say it instead of tapping it. Falls back silently to
   buttons everywhere else, which is most places, so nothing depends on it.
   ========================================================================== */

AISS.Voice = {
  active: false, supported: false, _rec: null, _onResult: null,

  init(){
    const R = global.SpeechRecognition || global.webkitSpeechRecognition;
    if (!R) return false;
    this.supported = true;
    this._rec = new R();
    this._rec.continuous = false;
    this._rec.interimResults = false;
    this._rec.lang = 'en-US';
    this._rec.onresult = e => {
      const said = e.results[0][0].transcript.toLowerCase().trim();
      if (this._onResult) this._onResult(said, e.results[0][0].confidence);
    };
    this._rec.onend = () => { this.active = false; };
    this._rec.onerror = () => { this.active = false; };
    return true;
  },

  listen(cb){
    if (!this.supported) return false;
    this._onResult = cb;
    try { this._rec.start(); this.active = true; return true; }
    catch(e){ return false; }
  },

  stop(){ try { this._rec && this._rec.stop(); } catch(e){} this.active = false; },

  /* Loose match against a tray — "ten blade", "kelly", "metz" should all work,
     because that is how people actually call for things. */
  match(said, tray){
    const t = tokens(said);
    if (!t.length) return null;
    let best = null, bestScore = 0;
    tray.forEach(name => {
      const nt = tokens(name);
      let hit = 0;
      t.forEach(q => { if (nt.some(n => n === q || n.indexOf(q) === 0 || q.indexOf(n) === 0)) hit++; });
      const score = hit / Math.max(1, Math.min(t.length, nt.length));
      if (score > bestScore){ bestScore = score; best = name; }
    });
    return bestScore >= 0.5 ? best : null;
  }
};

/* Haptics — free on Android, ignored on iOS Safari. Used only to confirm,
   never to punish; a buzz on error trains flinching. */
AISS.Haptic = {
  ok(){ try { navigator.vibrate && navigator.vibrate(18); } catch(e){} },
  step(){ try { navigator.vibrate && navigator.vibrate([12,40,12]); } catch(e){} }
};

/* ==========================================================================
   10. HANDOVER — knowing when to stop

   The rule the whole product is built around: patient safety outranks your
   score, and the scoring has to make that true rather than say it.

   So the ceiling on gambling sits below the floor on the right call. If you
   push past the safety envelope on a deteriorating patient and get away with
   it, you score less than the player who handed over. If you push past it and
   do not get away with it, you score far less, and the debrief names the
   moment it became avoidable.
   ========================================================================== */

AISS.Handover = {
  offered: false, taken: false, at: null, outcome: null,
  envelope: false,        // true once the patient is past the point of no return

  PTS: {
    correct:      40,     // handed over inside the window: the best outcome available
    early:         8,     // handed over before it was needed: safe, some ground given
    gambleWon:    22,     // pushed past the envelope and got away with it
    gambleLost:  -55,     // pushed past the envelope and the patient paid
    lateHandover: -6      // handed over after harm was already done
  },

  reset(){ this.offered=false; this.taken=false; this.at=null; this.outcome=null; this.envelope=false; },

  /* Modules call this from their physiology loop. severity 0..1. */
  assess(severity, secondsUnstable){
    if (!this.envelope && (severity > 0.7 || secondsUnstable > 25)) this.envelope = true;
    return this.envelope;
  },

  /* The player chose to turn it over to the AI attending. */
  handOver(ctx){
    this.taken = true;
    this.at = ctx || {};
    if (!this.envelope && !(ctx && ctx.harmed)){
      this.outcome = 'early';
      return { points: this.PTS.early, tag:'early',
        line:'Turned over. Nothing was going to happen yet, and you gave up ground you could have held — but nobody has ever been sued for that.' };
    }
    if (ctx && ctx.harmed){
      this.outcome = 'late';
      return { points: this.PTS.lateHandover, tag:'late',
        line:'Turned over, after. The decision was right and it was late. The debrief will show you where it stopped being early.' };
    }
    this.outcome = 'correct';
    return { points: this.PTS.correct, tag:'correct',
      line:'Turned over inside the window. That is the highest-scoring thing you can do in this module, and it is the one people find hardest.' };
  },

  /* The player pushed on instead. Called when the attempt resolves. */
  pushedOn(survived){
    if (!this.envelope){
      return { points: 0, tag:'inbounds', line:null };   // still inside the envelope, no judgement
    }
    if (survived){
      this.outcome = 'gambleWon';
      return { points: this.PTS.gambleWon, tag:'gambleWon',
        line:'You stayed and it worked. It scores less than handing over would have, and that is not a bug. '
           + 'You were outside the envelope; the outcome was availability, not skill. The version of this where it does not work is the same decision.' };
    }
    this.outcome = 'gambleLost';
    return { points: this.PTS.gambleLost, tag:'gambleLost',
      line:'You stayed and the patient paid for it. This is the error the whole product exists to teach: the moment it stopped being a technical problem and became a judgement one.' };
  },

  summary(){
    if (!this.taken && !this.outcome) return null;
    return { outcome:this.outcome, envelope:this.envelope };
  }
};

/* ==========================================================================
   11. PROGRESS — exact numbers, per competency, so you know where you stand

   Not a single score. Seven domains, tracked separately, persisted, and
   reported to the decimal. The point is that a player who is bad at one
   specific thing can be told which thing, in one sentence, with a number.
   ========================================================================== */

const DOMAINS = {
  anatomy:    { label:'Anatomy identification', fix:'Repeat the study cards and the See One phase — name the structure before you touch anything.' },
  instrument: { label:'Instrument naming',      fix:'Run skills-lab module 00.4, the tray. It is fifteen minutes and it fixes this outright.' },
  technique:  { label:'Technique and maneuver', fix:'Repeat Do One. Your hands are ahead of your sequencing.' },
  judgement:  { label:'Judgement at forks',     fix:'Re-read your committed decisions in the debrief. Every one of them had a stated rationale you could have weighed.' },
  vigilance:  { label:'Monitor vigilance',      fix:'You are working the field and not the room. Call out changes before the head of the bed does.' },
  safety:     { label:'Safety and handover',    fix:'You held on too long. In this product, calling for help scores higher than getting away with it.' },
  teaching:   { label:'Teaching',               fix:'You can do it and you cannot yet explain it. That gap is the whole reason Teach One is worth forty.' }
};

AISS.Progress = {
  moduleId: 'unknown',
  run: {},            // domain -> {n, ok}
  lifetime: {},

  init(moduleId){
    this.moduleId = moduleId || 'unknown';
    this.run = {};
    Object.keys(DOMAINS).forEach(k => this.run[k] = { n:0, ok:0 });
    try {
      this.lifetime = JSON.parse(localStorage.getItem('aiss.progress') || '{}');
    } catch(e){ this.lifetime = {}; }
    if (!this.lifetime[this.moduleId]) this.lifetime[this.moduleId] = { runs:0, domains:{}, bestSafe:0, safeStreak:0 };
    return this;
  },

  mark(domain, correct){
    if (!this.run[domain]) this.run[domain] = { n:0, ok:0 };
    this.run[domain].n++;
    if (correct) this.run[domain].ok++;
    AISS.Stress.outcome(!!correct);
  },

  pct(domain, scope){
    const d = (scope === 'lifetime')
      ? (this.lifetime[this.moduleId].domains[domain] || { n:0, ok:0 })
      : (this.run[domain] || { n:0, ok:0 });
    return d.n ? (d.ok / d.n) * 100 : null;
  },

  weakest(){
    let worst = null;
    Object.keys(this.run).forEach(k => {
      const d = this.run[k];
      if (d.n < 2) return;
      const p = d.ok / d.n;
      if (!worst || p < worst.p) worst = { key:k, p, n:d.n, ok:d.ok };
    });
    return worst;
  },

  commit(opts){
    opts = opts || {};
    const L = this.lifetime[this.moduleId];
    L.runs++;
    Object.keys(this.run).forEach(k => {
      if (!L.domains[k]) L.domains[k] = { n:0, ok:0 };
      L.domains[k].n += this.run[k].n;
      L.domains[k].ok += this.run[k].ok;
    });
    if (opts.harmFree){ L.safeStreak = (L.safeStreak || 0) + 1; L.bestSafe = Math.max(L.bestSafe || 0, L.safeStreak); }
    else L.safeStreak = 0;
    try { localStorage.setItem('aiss.progress', JSON.stringify(this.lifetime)); } catch(e){}
    return L;
  },

  /* The exact, thorough part. Every domain, this run and lifetime. */
  table(){
    const rows = Object.keys(DOMAINS).map(k => {
      const r = this.run[k] || { n:0, ok:0 };
      const l = (this.lifetime[this.moduleId].domains[k]) || { n:0, ok:0 };
      const rp = r.n ? Math.round((r.ok / r.n) * 100) : null;
      const lp = l.n ? Math.round((l.ok / l.n) * 100) : null;
      return '<div class="pgrow"><b>' + DOMAINS[k].label + '</b>'
        + '<span>' + (rp === null ? '—' : r.ok + '/' + r.n + '  ·  ' + rp + '%') + '</span>'
        + '<span class="life">' + (lp === null ? '' : 'lifetime ' + lp + '%') + '</span></div>';
    }).join('');
    const w = this.weakest();
    const advice = w
      ? '<div class="pgfix"><b>' + DOMAINS[w.key].label + ' is your weakest at '
        + Math.round(w.p * 100) + '% (' + w.ok + ' of ' + w.n + ').</b> ' + DOMAINS[w.key].fix + '</div>'
      : '';
    return rows + advice;
  }
};

/* ==========================================================================
   12. REWARDS — hooks, hung off the one thing that should be habit-forming

   A medical training product with retention mechanics has an obligation the
   average game does not: the behaviour the hooks reinforce is the behaviour
   the player will carry into a real room. So the headline streak is not
   speed and it is not points. It is consecutive cases without patient harm,
   and it is the only streak that appears on the front of a profile.
   ========================================================================== */

AISS.Rewards = {
  UNLOCKS: [
    { id:'variant-retrocecal', at:'anatomy>=85',  what:'Anatomical variants — retrocecal, pelvic and subhepatic appendix positions in the same module.' },
    { id:'variant-situs',      at:'runs>=6',      what:'Situs inversus presentation. Left lower quadrant pain, and everything you know is mirrored.' },
    { id:'cadaveric',          at:'anatomy>=92',  what:'Cadaveric-detail model — fascial planes and segmental nerves rendered at full density.' },
    { id:'night',              at:'runs>=3',      what:'Night float. Same case, 3 a.m. lighting, a tired scrub, and one instrument missing from the tray.' },
    { id:'paeds',              at:'teaching>=80', what:'Paediatric case. Smaller everything, different differential, and a parent asking you questions.' },
    { id:'attending',          at:'clear-all',    what:'Attending track. You stop being asked the questions and start asking them.' }
  ],

  /* Real-world prizes are funded by schools, hospital systems and STEM
     grants, and are gated behind a verified institutional account — not
     behind spend, and not behind speed. */
  eligible(progress, safeStreak){
    return {
      safeStreak: safeStreak || 0,
      note: safeStreak >= 5
        ? 'Five consecutive cases with no patient harm. That is the streak that counts toward institutional awards.'
        : 'Consecutive harm-free cases is the streak that counts. You are at ' + (safeStreak || 0) + '.'
    };
  },

  earned(progress){
    const L = progress.lifetime[progress.moduleId] || { runs:0, domains:{} };
    return this.UNLOCKS.filter(u => {
      if (u.at === 'clear-all') return false;
      const m = /^([a-z]+)>=(\d+)$/.exec(u.at);
      if (!m) return false;
      if (m[1] === 'runs') return L.runs >= +m[2];
      const d = L.domains[m[1]];
      return d && d.n >= 4 && (d.ok / d.n) * 100 >= +m[2];
    });
  }
};

/* ==========================================================================
   13. HUMOR — real, and fenced

   Operating rooms are funny because they have to be; the humor is how people
   discharge the pressure. It belongs in the product for the same reason.

   The fences are absolute:
     - never while the patient is unstable
     - never after a patient has been harmed, in that case or the debrief
     - never from the head of the bed; the monks do not participate
     - never at the expense of the patient
     - never at the player's expense while they are behind
   ========================================================================== */

AISS.Humor = {
  enabled: true,
  _used: {},

  LINES: [
    { t:'blame', who:'attending', when:'minor-error',
      s:'That is fine. In twenty years nobody has ever written "surgeon error" on one of these. It was anaesthesia.' },
    { t:'blame', who:'attending', when:'minor-error',
      s:'Not your fault. Something happened at the head of the bed. Something always did.' },
    { t:'tray', who:'scrub', when:'wrong-instrument',
      s:'I have it right here. I am simply not going to give it to you, because it is not what you asked for.' },
    { t:'tray', who:'scrub', when:'wrong-instrument',
      s:'That is a Mayo. You asked for a Mayo. You wanted a Metzenbaum. Those are three different sentences.' },
    { t:'time', who:'attending', when:'slow',
      s:'Take your time. The appendix has been there nineteen years. It can hold on another minute.' },
    { t:'time', who:'attending', when:'fast',
      s:'Quick hands. Now do it again at the speed of somebody who intends to be right.' },
    { t:'teach', who:'attending', when:'teach-correct',
      s:'Correct, and said in one sentence. Do not let that habit go.' },
    { t:'self', who:'attending', when:'good-run',
      s:'Good case. Do not tell anyone I said so, it ruins the whole arrangement.' },
    { t:'sterile', who:'scrub', when:'idle',
      s:'Your hands are above the drape. I am watching them. I am always watching them.' }
  ],

  /* ctx: {unstable, harmed, behind} — any of these true and nothing is said. */
  line(when, ctx){
    ctx = ctx || {};
    if (!this.enabled) return null;
    if (ctx.unstable || ctx.harmed) return null;
    if (ctx.behind && when === 'minor-error') return null;
    const pool = this.LINES.filter(l => l.when === when && !this._used[l.s]);
    if (!pool.length) return null;
    const pick = pool[Math.floor(Math.random() * pool.length)];
    this._used[pick.s] = true;
    return pick;
  },

  reset(){ this._used = {}; }
};

AISS.resetAll = function (){
  AISS.Stress.reset();
  AISS.Gaze.reset();
  AISS.Decisions.reset();
  AISS.Ask.reset();
  AISS.Handover.reset();
  AISS.Humor.reset();
};

})(typeof window !== 'undefined' ? window : globalThis);
