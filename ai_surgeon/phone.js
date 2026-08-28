/* Phone-first screens for the August 2026 stills. Twist to choose, touch to commit. */
(function () {
  "use strict";

  const $ = (sel, root) => (root || document).querySelector(sel);
  const view = () => $("#view");

  const state = {
    points: 40,
    coherence: 61,
    tool: null,
    studyCorrect: 0,
    studyCard: 3,
    studyChoice: null,
    identified: false,
    identifyState: "ASK",
    grabbed: null,
    lastTouch: null,
    layers: new Set(["peritoneum", "bowel_wall", "mesoappendix"]),
    trayOpen: false,
    trayIndex: 0,
    step: "ligate_the_base",
    airway: 2,
    propofolTwist: 0,
    drillIndex: 1,
    verseSeat: "surgeon",
    verseCase: 0,
    seeNamed: {},
    anatomyShot: "b",
    trauma: {
      coherence: 44,
      acuity: 2.5,
      elapsed: 37,
      needle: false,
      tube: false,
      fluid: false,
      dead: false,
      points: 590,
    },
  };

  const STILLS = [
    ["01", "stills/01-anesthesia-pen.png", "Anesthesia / The Pen", "playable", "anesthesia"],
    ["02", "stills/02-art-fidelity.png", "Art fidelity", "pitch", "art"],
    ["03", "stills/03-hardware-ladder.png", "Hardware ladder", "pitch", "hardware"],
    ["04", "stills/04-identify-before-you-cut.png", "Identify before you cut", "playable", "identify"],
    ["05", "stills/05-cecum-appendix-a.png", "Cecum / appendix A", "playable", "anatomy"],
    ["06", "stills/06-cecum-appendix-b.png", "Cecum / appendix B", "playable", "anatomy"],
    ["07", "stills/07-surgery-verse.png", "Surgery Verse", "playable", "verse"],
    ["08", "stills/08-tablet-pencil-mat.png", "Tablet + pencil + mat", "pitch", "tablet"],
    ["09", "stills/09-the-lab.png", "The Lab", "playable", "lab"],
    ["10", "stills/10-twist-stylus.png", "Twist stylus", "pitch", "stylus"],
    ["11", "stills/11-the-nib.png", "The Nib", "playable", "nib"],
    ["12", "stills/12-study-one.png", "Study One", "playable", "study"],
    ["13", "stills/13-see-one.png", "See One", "playable", "see"],
    ["14", "stills/14-do-one.png", "Do One", "playable", "do"],
    ["15", "stills/15-call-for-instrument.png", "Call for the instrument", "playable", "call"],
    ["16", "stills/16-trauma-pneumo.png", "Trauma case 07", "playable", "trauma"],
  ];

  const REGIONS = [
    { id: "appendix", cx: 0.64, cy: 0.74, rx: 0.2, ry: 0.18 },
    { id: "mesoappendix", cx: 0.48, cy: 0.6, rx: 0.15, ry: 0.13 },
    { id: "ileum", cx: 0.22, cy: 0.36, rx: 0.18, ry: 0.16 },
    { id: "cecum", cx: 0.5, cy: 0.36, rx: 0.32, ry: 0.3 },
  ];
  const COPY = {
    appendix: { label: "Appendix", sub: "CONFIRMED", footer: "Appendix. Base at the taenia. Scalpel unlocked." },
    cecum: { label: "Cecum", sub: "NOT THE TARGET", footer: "That is the cecum. Follow the taenia down: -5" },
    mesoappendix: { label: "Mesoappendix", sub: "NOT THE TARGET", footer: "That is the mesoappendix. The appendix is the tube: -5" },
    ileum: { label: "Terminal ileum", sub: "NOT THE TARGET", footer: "That is the ileum. The appendix hangs off the cecum: -5" },
    field: { label: "Field", sub: "NOT A STRUCTURE", footer: "Touch the organ, not the drape: -5" },
  };
  const TRAY = ["SCALPEL", "FORCEPS", "CLAMP", "DRIVER", "SPONGE"];
  const LEGAL = { ligate_the_base: ["SCALPEL", "CLAMP", "DRIVER"] };
  const AIRWAY = ["MASK", "LMA", "ETT"];
  const DRILL = [
    ["Macintosh 3", "Curved blade. Tip in the vallecula."],
    ["LMA", "Sits over the larynx, no cords needed."],
    ["Bougie", "Hold-up tells you you are in trachea."],
    ["Stylet", "Shapes the tube. Not a weapon."],
  ];
  const CASES = ["Appendectomy", "Lap chole", "Bowel obstruction", "Tension pneumo", "C-section", "Trauma lap", "CABG", "Ruptured AAA"];
  const TABLE = [
    ["hemostat", "Hemostat", "Kelly / mosquito", "open_peritoneum"],
    ["metz", "Metzenbaum scissors", "sharp dissection", "aponeurosis"],
    ["babcock", "Babcock clamp", "delivers the cecum", "deliver_cecum"],
    ["retractor", "Army-Navy retractor", "wound edge", "retract"],
    ["vicryl", "0-Vicryl on driver", "fascial closure", "close"],
    ["bovie", "Bovie", "electrocautery", "hemostasis"],
  ];
  const SEE = [
    ["external_oblique", "External oblique", "Outermost flat. Split with the fibres."],
    ["internal_oblique", "Internal oblique", "Middle layer. Fibres run opposite. Still split."],
    ["transversalis", "Transversalis fascia", "Under it, preperitoneal fat, then peritoneum."],
  ];
  const STUDY = [
    null,
    { title: "Anatomy", prompt: "Where do the three taeniae of the cecum converge?",
      opts: [["A", "At the ileocecal valve", false], ["B", "At the base of the appendix", true], ["C", "At the hepatic flexure", false]],
      explain: "All three taeniae meet at the appendiceal base." },
    { title: "McBurney", prompt: "A gridiron incision splits which layers?",
      opts: [["A", "External, internal, transversus — split, not cut", true], ["B", "Rectus sheath, then midline peritoneum", false], ["C", "Skin, then a muscle-cutting Kocher", false]],
      explain: "McBurney is split, not cut." },
    { title: "Pathophysiology", prompt: "So which comes first?",
      body: "The lumen obstructs. Mucus keeps being secreted, so intraluminal pressure rises — past venous pressure before it passes arterial.",
      opts: [["A", "Arterial ischaemia, then venous congestion", false], ["B", "Venous congestion, then arterial ischaemia", true], ["C", "Simultaneous — the wall fails all at once", false]],
      explain: "Correct. Congestion precedes ischaemia. +10" },
    { title: "Referred pain", prompt: "Why periumbilical first, then right lower quadrant?",
      opts: [["A", "The appendix migrates during the attack", false], ["B", "Visceral afferents first (midgut / T10), then parietal peritoneum", true], ["C", "The ileocolic artery spasms", false]],
      explain: "Visceral midgut pain is periumbilical. Parietal localises to the RLQ." },
  ];

  function route() {
    return (location.hash.replace(/^#\/?/, "") || "hub").split("/")[0];
  }
  function go(name) {
    location.hash = "#" + name;
  }
  function hitStructure(nx, ny) {
    for (const r of REGIONS) {
      const dx = (nx - r.cx) / r.rx;
      const dy = (ny - r.cy) / r.ry;
      if (dx * dx + dy * dy <= 1) return r.id;
    }
    return "field";
  }
  function chrome(phase, title, pts, coh) {
    const fill = coh >= 72 ? "var(--teal)" : coh >= 34 ? "var(--amber)" : "var(--red)";
    const tool = state.tool
      ? `<div class="chip on" style="margin:0">${state.tool}</div>`
      : "";
    return `<header class="chrome">
      <div class="row">
        <button class="back" data-go="hub" aria-label="Back">←</button>
        <div>
          <div class="kicker">${phase}</div>
          <div class="title">${title}</div>
        </div>
        <div class="pts">${pts}<span>POINTS</span></div>
      </div>
      <div class="coh">COHERENCE <div class="bar"><i style="width:${coh}%;background:${fill}"></i></div>
        <span class="n" style="color:${fill}">${coh}</span> ${tool}</div>
    </header>`;
  }

  function hub() {
    const cards = STILLS.map(([id, src, title, kind, r]) => {
      const tag = kind === "playable" ? "Playable" : "Pitch still";
      return `<a class="hub-card ${kind}" href="#${r}">
        <img src="${src}" alt="">
        <div class="b"><div class="k">Still ${id} · ${tag}</div>
        <div class="n">${title}</div></div></a>`;
    }).join("");
    return `${chrome("AI SURGEON · ONE APP", "Phone screens", state.points, state.coherence)}
      <div class="pad">
        <p class="meta">Twist to choose, touch to commit. Surgery and anaesthesia are two seats of the same case.
        Module 12 appendectomy and Module 21 trauma stay on the hub — this page does not replace them.</p>
        <a class="cta" href="index.html">← Residency hub</a>
      </div>
      <div class="hub-grid">${cards}
        <a class="hub-card" href="generators/AI-Surgeon-Brochure.pdf">
          <img src="generators/screen-01-study-one.png" alt="">
          <div class="b"><div class="k">Brochure</div><div class="n">Concept PDF</div>
          <div class="d">Generated from brochure.py + mockups.py</div></div></a>
        <a class="hub-card" href="ai-surgeon-prototype.html">
          <img src="art/hero-surgical-table.jpg" alt="">
          <div class="b"><div class="k">Sibling module</div><div class="n">Open appendectomy</div>
          <div class="d">Playable prototype. Not replaced.</div></div></a>
        <a class="hub-card" href="ai-surgeon-module02-trauma.html">
          <img src="art/key-art-x.jpg" alt="">
          <div class="b"><div class="k">Sibling module</div><div class="n">Tube thoracostomy</div>
          <div class="d">Full trauma module. Case 07 is the phone still.</div></div></a>
      </div>
      <p class="disclaimer">Training simulation. Not a medical device. Not a clinical reference.</p>`;
  }

  function identify() {
    const shot = "stills/06-cecum-appendix-b.png";
    const st = state.identifyState;
    const copy = COPY[state.grabbed] || null;
    let overlay = "";
    if (st === "MISS" && state.lastTouch) {
      overlay = `<div class="ring" style="left:${state.lastTouch.x * 100}%;top:${state.lastTouch.y * 100}%"></div>
        <div class="callout miss" style="left:${Math.min(72, state.lastTouch.x * 100 + 8)}%;top:${state.lastTouch.y * 100 - 8}%">
          ${copy.label} / ${copy.sub}</div>`;
    }
    if (st === "HIT") {
      overlay = `<div class="glow-appendix" style="left:44%;top:56%;width:40%;height:36%"></div>
        <div class="callout hit" style="left:58%;top:52%">Appendix / CONFIRMED</div>`;
    }
    const footer = st === "ASK"
      ? `<div class="card"><div class="who">ONE TAP</div>Touch the appendix.</div>`
      : `<div class="card ${st === "HIT" ? "teal" : "amber"}">${copy ? copy.footer : ""}</div>`;
    const pts = st === "HIT" ? "+ 15" : st === "MISS" ? "− 5" : "0:12";
    return `${chrome("STUDY ONE · DRILL 4", "Right lower quadrant", pts, 66)}
      <div class="field" id="id-field">
        <img class="anat" src="${shot}" alt="Cecum and appendix, wet-shader mesh">
        ${overlay}
      </div>
      <div class="pad">${footer}
        <p class="fine">The case will not advance until you put a finger on the right thing. Highlight is the same mesh, lit differently.</p>
        ${st === "HIT" ? `<button class="cta" data-go="do">Scalpel unlocked →</button>` : ""}
      </div>`;
  }

  function bindIdentify() {
    const field = $("#id-field");
    if (!field) return;
    field.addEventListener("pointerdown", (ev) => {
      if (state.identifyState === "HIT") return;
      const img = field.querySelector("img");
      const r = img.getBoundingClientRect();
      const nx = (ev.clientX - r.left) / r.width;
      const ny = (ev.clientY - r.top) / r.height;
      const grabbed = hitStructure(nx, ny);
      state.grabbed = grabbed;
      state.lastTouch = { x: nx, y: ny };
      if (grabbed === "appendix") {
        state.identifyState = "HIT";
        state.identified = true;
        state.tool = "SCALPEL";
        state.points += 15;
      } else {
        state.identifyState = "MISS";
        state.points -= 5;
      }
      render();
    }, { once: false });
  }

  function lab() {
    const layers = ["peritoneum", "bowel_wall", "mesoappendix", "arteries", "lymphatics", "nerves"];
    const chips = layers.map((l) => {
      const on = state.layers.has(l);
      return `<button class="chip ${on ? "on" : ""}" data-layer="${l}">${l.replace("_", " ")}</button>`;
    }).join("");
    const kind = classifyLab();
    const src = kind === "SUBTRACT" ? "stills/06-cecum-appendix-b.png" : "stills/05-cecum-appendix-a.png";
    const art = state.layers.has("arteries")
      ? `<svg class="still-full" viewBox="0 0 100 100" style="position:absolute;inset:0;pointer-events:none">
           <path d="M42 48 Q50 60 62 72" stroke="#c0392b" fill="none" stroke-width="1.6"/>
           <path d="M50 58 Q58 64 70 68" stroke="#c0392b" fill="none" stroke-width="1.1"/>
           <text x="68" y="42" fill="#31b9a4" font-size="4">Appendicular a.</text>
         </svg>` : "";
    const veil = state.layers.has("peritoneum")
      ? `<div style="position:absolute;inset:0;background:rgba(180,140,90,.12);pointer-events:none"></div>` : "";
    return `${chrome("MODULE 01 · THE LAB", kind, state.points, 70)}
      <div class="field" style="min-height:280px">
        <img class="anat" src="${src}" alt="Lab anatomy" style="filter:${state.layers.has("bowel_wall") ? "none" : "grayscale(.4) brightness(.7)"}">
        ${veil}${art}
      </div>
      <div class="pad">
        <div class="chips">
          <button class="chip ${kind === "FIELD" ? "on" : ""}" data-preset="FIELD">FIELD</button>
          <button class="chip ${kind === "ADD" ? "on" : ""}" data-preset="ADD">ADD</button>
          <button class="chip ${kind === "SUBTRACT" ? "on" : ""}" data-preset="SUBTRACT">SUBTRACT</button>
        </div>
        <div class="chips" id="layer-chips">${chips}</div>
        <p class="fine">${kind === "FIELD" ? "The artery is in there, unseen." :
          kind === "ADD" ? "Now you know what you will tie." :
          kind === "SUBTRACT" ? "Appendix, alone. Back to the case when ready." :
          `${state.layers.size} on. Same meshes as the case.`}</p>
      </div>`;
  }
  function classifyLab() {
    const s = [...state.layers].sort().join(",");
    if (s === "bowel_wall,mesoappendix,peritoneum") return "FIELD";
    if (s === "arteries,bowel_wall,mesoappendix,peritoneum") return "ADD";
    if (s === "arteries,bowel_wall") return "SUBTRACT";
    return "CUSTOM";
  }
  function bindLab() {
    view().querySelectorAll("[data-preset]").forEach((b) => {
      b.addEventListener("click", () => {
        const p = b.getAttribute("data-preset");
        if (p === "FIELD") state.layers = new Set(["peritoneum", "bowel_wall", "mesoappendix"]);
        if (p === "ADD") state.layers = new Set(["peritoneum", "bowel_wall", "mesoappendix", "arteries"]);
        if (p === "SUBTRACT") state.layers = new Set(["bowel_wall", "arteries"]);
        render();
      });
    });
    view().querySelectorAll("[data-layer]").forEach((b) => {
      b.addEventListener("click", () => {
        const l = b.getAttribute("data-layer");
        if (state.layers.has(l)) state.layers.delete(l);
        else state.layers.add(l);
        render();
      });
    });
  }

  function study() {
    const card = STUDY[state.studyCard];
    const locked = state.studyCorrect < 4;
    const opts = card.opts.map(([id, text, ok]) => {
      const chosen = state.studyChoice === id;
      const cls = chosen ? (ok ? "on" : "bad") : "";
      const note = chosen && ok ? `<span class="sub">${card.explain}</span>` : "";
      return `<button class="opt ${cls}" data-choice="${id}" ${state.studyChoice ? "disabled" : ""}><b>${id}</b> ${text}${note}</button>`;
    }).join("");
    return `${chrome("PHASE 1 OF 4 · STUDY ONE", "Acute appendicitis", state.points, state.coherence)}
      <div class="pad">
        <div class="banner">${locked ? "LOCKED · You cannot scrub in until 4 of 4 cards are complete." : "SCRUB UNLOCKED · 4 of 4 cards complete."}</div>
        <div class="card">
          <div class="who">CARD ${state.studyCard} OF 4 · ${card.title.toUpperCase()}</div>
          ${card.body ? `<p class="meta">${card.body}</p>` : ""}
          <p style="margin-top:8px;font-weight:700">${card.prompt}</p>
          <p class="fine">Points ride on the answer. The attending asks this again mid-case.</p>
        </div>
        ${opts}
        ${state.studyChoice ? `<button class="cta" data-next-card>CONTINUE →</button>` : ""}
        ${!locked ? "" : `<div class="card"><div class="who">REMAINING</div>Card ${Math.min(4, state.studyCard + (state.studyChoice ? 1 : 0))} — keep going.</div>`}
        <p class="fine">Studying: 10 pts/card · Observing: 5/step · Operating: 25/step · Teaching: 40/step</p>
      </div>`;
  }
  function bindStudy() {
    view().querySelectorAll("[data-choice]").forEach((b) => {
      b.addEventListener("click", () => {
        if (state.studyChoice) return;
        const id = b.getAttribute("data-choice");
        const card = STUDY[state.studyCard];
        const opt = card.opts.find((o) => o[0] === id);
        state.studyChoice = id;
        if (opt[2]) {
          state.points += 10;
          state.studyCorrect += 1;
        }
        render();
      });
    });
    const next = $("[data-next-card]");
    if (next) next.addEventListener("click", () => {
      if (state.studyCard < 4) {
        state.studyCard += 1;
        state.studyChoice = null;
        render();
      } else {
        go("see");
      }
    });
  }

  function see() {
    const named = Object.keys(state.seeNamed).length;
    const opts = SEE.map(([id, name, why]) => {
      const on = state.seeNamed[id];
      return `<button class="opt ${on ? "on" : ""}" data-see="${id}">${name}${on ? `<span class="sub">${why} +5</span>` : ""}</button>`;
    }).join("");
    return `${chrome("PHASE 2 OF 4 · SEE ONE", "The attending operates", state.points, 66)}
      <div class="field" style="min-height:220px">
        <img class="cover" src="stills/13-see-one.png" alt="See One attending operates">
      </div>
      <div class="pad">
        <div class="card teal">
          <div class="who">AI ATTENDING</div>
          Transversalis fascia. Under it, preperitoneal fat, then peritoneum. I am splitting muscle, not cutting it.
        </div>
        <p class="fine">Tap any structure to be told what it is and why it matters. Nothing here is skippable. Nothing is graded as a fail.</p>
        ${opts}
        <div class="chips" style="margin-top:12px">
          <button class="chip" data-go="hub">PAUSE · ASK</button>
          <button class="cta" data-go="do" ${named ? "" : ""}>SCRUB IN →</button>
        </div>
      </div>`;
  }
  function bindSee() {
    view().querySelectorAll("[data-see]").forEach((b) => {
      b.addEventListener("click", () => {
        const id = b.getAttribute("data-see");
        if (!state.seeNamed[id]) {
          state.seeNamed[id] = true;
          state.points += 5;
        }
        render();
      });
    });
  }

  function doOne() {
    const opts = [
      ["mesoappendix", "Mesoappendix, carrying the appendicular artery", "+25", true],
      ["taenia", "Taenia libera", "−10", false],
      ["ileocolic", "Ileocolic artery", "−25 wrong structure", false],
      ["peritoneum", "Peritoneal reflection", "−10", false],
    ].map(([id, t, pts, ok]) => {
      const chosen = state.doChoice === id;
      return `<button class="opt ${chosen ? (ok ? "on" : "bad") : ""}" data-do="${id}">${t}<span class="sub">${pts}</span></button>`;
    }).join("");
    return `${chrome("PHASE 3 OF 4 · DO ONE", "You are operating", state.points, 78)}
      <div class="field" style="min-height:200px">
        <img class="cover" src="stills/06-cecum-appendix-b.png" alt="Field">
      </div>
      <div class="pad">
        <div class="card teal">
          <div class="who">AI ATTENDING ASKS</div>
          “What are you about to divide?”
          <div class="fine">Answer before the instrument unlocks. <span class="timer">0:14</span></div>
        </div>
        ${opts}
        <div class="who" style="margin-top:12px">THEN THE GESTURE</div>
        <div class="gestures">
          <button data-g="swipe"><b>swipe</b><span>incise</span></button>
          <button data-g="two-finger"><b>2-finger</b><span>split / retract</span></button>
          <button data-g="pinch"><b>pinch</b><span>clamp</span></button>
          <button data-g="hold"><b>hold</b><span>ligate</span></button>
        </div>
        <p class="fine" id="g-note">${state.identified || state.doChoice === "mesoappendix" ? "Hold until the knot seats." : "Name it before you cut."}</p>
      </div>`;
  }
  function bindDo() {
    view().querySelectorAll("[data-do]").forEach((b) => {
      b.addEventListener("click", () => {
        const id = b.getAttribute("data-do");
        state.doChoice = id;
        if (id === "mesoappendix") {
          state.points += 25;
          state.identified = true;
        } else if (id === "ileocolic") state.points -= 25;
        else state.points -= 10;
        render();
      });
    });
    view().querySelectorAll("[data-g]").forEach((b) => {
      b.addEventListener("click", () => {
        const g = b.getAttribute("data-g");
        const note = $("#g-note");
        if (state.doChoice !== "mesoappendix") {
          note.textContent = "Name it before the instrument unlocks.";
          return;
        }
        if (g !== "hold") {
          note.textContent = "Wrong maneuver. This step is ligate (hold).";
          return;
        }
        note.textContent = "Knot seated. +25";
        state.points += 25;
      });
    });
  }

  function callView() {
    const rows = TABLE.map(([id, name, note, step]) => {
      const on = state.callPick === id;
      return `<button class="opt ${on ? "on" : ""}" data-call="${id}">${name}<span class="sub">${note}</span></button>`;
    }).join("");
    const picked = TABLE.find((t) => t[0] === state.callPick);
    const ok = picked && picked[3] === "open_peritoneum";
    return `${chrome("PHASE 3 OF 4 · DO ONE", "Call for the instrument", state.points, 81)}
      <div class="pad">
        <div class="card teal">
          <div class="who">AI ATTENDING</div>
          “Open the peritoneum between two of these. Ask the scrub. By name.”
        </div>
        <div class="who" style="margin-top:12px">STERILE BACK TABLE · you have no instruments until you ask</div>
        ${rows}
        ${picked ? `<div class="card ${ok ? "teal" : "amber"}"><div class="who">SCRUB TECH</div>${ok ? "Two hemostats. Careful, they're loaded." : picked[1] + ". That is not what was asked."}</div>` : ""}
        <div class="card amber"><div class="who">WRONG INSTRUMENT COSTS POINTS</div>And the scrub says so. Nobody hands you the wrong thing silently.</div>
        <button class="cta" data-call-go ${state.callPick ? "" : "disabled"}>CALL FOR IT</button>
        <p class="fine">Voice or tap. Spoken aloud scores higher. This screen is tap-only in the phone still.</p>
      </div>`;
  }
  function bindCall() {
    view().querySelectorAll("[data-call]").forEach((b) => {
      b.addEventListener("click", () => {
        state.callPick = b.getAttribute("data-call");
        render();
      });
    });
    const goBtn = $("[data-call-go]");
    if (goBtn) goBtn.addEventListener("click", () => {
      const picked = TABLE.find((t) => t[0] === state.callPick);
      if (!picked) return;
      if (picked[3] === "open_peritoneum") state.points += 25;
      else state.points -= 10;
      render();
    });
  }

  function anesthesia() {
    const rate = Math.max(0.2, Math.min(4, +(2 + state.propofolTwist).toFixed(1)));
    const tooFast = rate >= 3.2;
    const air = AIRWAY[state.airway % 3];
    const drill = DRILL[state.drillIndex % DRILL.length];
    return `${chrome("MODULE 04 · TWO SEATS, ONE CASE", "The Pen", state.points, 70)}
      <div class="pad">
        <p class="meta">The pen pushes. The pen seats. The pen threads. Twist to choose, touch to commit.</p>
        <div class="card teal">
          <div class="who">01 · INDUCTION · TWIST IS THE PLUNGER</div>
          <div class="knob-row">
            <div class="knob" id="prop-knob" style="--rot:${state.propofolTwist * 40}deg"></div>
            <div>
              <div class="dose">PROPOFOL ${rate.toFixed(1)} mg/kg</div>
              <div class="fine">twist = push</div>
              <div class="fine">${tooFast ? "Push it too fast and the pressure answers you." : "Speed is a user decision, not an animation."}</div>
            </div>
          </div>
          <button class="cta" data-commit-prop>Touch to commit the push</button>
        </div>
        <div class="card">
          <div class="who">02 · AIRWAY · TWIST TO TOGGLE</div>
          <div class="chips" id="airway-chips">
            ${AIRWAY.map((t, i) => `<button class="chip ${i === state.airway ? "on" : ""}" data-air="${i}">${t}</button>`).join("")}
          </div>
          <p class="fine">Name the cords before you pass the tube. ${air === "ETT" ? "DEPTH 22 cm" : air}</p>
          <button class="cta" data-commit-air>Touch to commit ${air}</button>
        </div>
        <div class="card">
          <div class="who">03 · DRILL · NAME THE TOOL</div>
          <p><b>${drill[0]}</b> — ${drill[1]}</p>
          <div class="chips">
            <button class="chip" data-drill="-1">twist ←</button>
            <button class="chip" data-drill="1">twist →</button>
          </div>
          <button class="cta" data-commit-drill>Touch to commit</button>
        </div>
      </div>`;
  }
  function bindAnesthesia() {
    const knob = $("#prop-knob");
    if (knob) bindKnob(knob, (d) => {
      state.propofolTwist = Math.max(-1.8, Math.min(2, state.propofolTwist + d / 40));
      render();
    });
    view().querySelectorAll("[data-air]").forEach((b) => {
      b.addEventListener("click", () => { state.airway = +b.getAttribute("data-air"); render(); });
    });
    view().querySelectorAll("[data-drill]").forEach((b) => {
      b.addEventListener("click", () => {
        state.drillIndex = (state.drillIndex + +b.getAttribute("data-drill") + DRILL.length) % DRILL.length;
        render();
      });
    });
    const cp = $("[data-commit-prop]");
    if (cp) cp.addEventListener("click", () => { state.points += 10; render(); });
    const ca = $("[data-commit-air]");
    if (ca) ca.addEventListener("click", () => { state.points += 10; render(); });
    const cd = $("[data-commit-drill]");
    if (cd) cd.addEventListener("click", () => {
      state.points += drillCorrect() ? 10 : -5;
      render();
    });
  }
  function drillCorrect() {
    return DRILL[state.drillIndex % DRILL.length][0] === "LMA";
  }
  function bindKnob(el, onDelta) {
    let last = null;
    el.addEventListener("pointerdown", (ev) => {
      last = ev.clientX;
      el.setPointerCapture(ev.pointerId);
    });
    el.addEventListener("pointermove", (ev) => {
      if (last == null) return;
      const dx = ev.clientX - last;
      last = ev.clientX;
      if (dx) onDelta(dx);
    });
    el.addEventListener("pointerup", () => { last = null; });
  }

  function nib() {
    const legal = LEGAL[state.step] || TRAY;
    const tools = TRAY.filter((t) => legal.includes(t) || !legal.length);
    const shown = state.trayOpen ? tools : [];
    return `${chrome("MODULE 01 · STEP 3", "Ligate the base", state.points, 79)}
      <div class="field" style="min-height:240px">
        <img class="cover" src="stills/06-cecum-appendix-b.png" alt="Field">
      </div>
      <div class="pad">
        <p class="meta">Twist raises the tray. Touch takes the instrument. Eyes stay on the field.</p>
        <div class="chips">
          <button class="chip" id="twist-btn">twist the grip</button>
          <span class="chip on">${state.tool || "—"}</span>
        </div>
        ${state.trayOpen ? `<div class="who">TRAY · touch to take · legal for this step only</div>
          <div class="tray">${shown.map((t, i) => `<button class="tool ${state.trayIndex === i ? "on" : ""}" data-take="${t}">${t}</button>`).join("")}</div>` : ""}
        <p class="fine">No menu. No tap-to-open. The tray turns because your hand turned. Then you cut.</p>
      </div>`;
  }
  function bindNib() {
    const twist = $("#twist-btn");
    if (twist) twist.addEventListener("click", () => {
      state.trayOpen = true;
      state.trayIndex = (state.trayIndex + 1) % ((LEGAL[state.step] || TRAY).length);
      render();
    });
    view().querySelectorAll("[data-take]").forEach((b) => {
      b.addEventListener("click", () => {
        state.tool = b.getAttribute("data-take");
        state.trayOpen = false;
        render();
      });
    });
  }

  function verse() {
    const seat = state.verseSeat;
    const kase = CASES[state.verseCase % CASES.length];
    const body = {
      surgeon: `<img class="cover" src="stills/06-cecum-appendix-b.png" alt="Field">
        <div class="pad"><div class="card">You cannot see the pressure.</div>
        <button class="cta">Call for the 2-0 tie.</button></div>`,
      anaesthesia: `<div class="pad">
        <div class="monitor">
          <div class="who">ECG II</div>
          <svg class="ecg" viewBox="0 0 300 54"><path d="M0 28 L20 28 L24 20 L28 40 L32 8 L38 32 L48 28 L68 28 L72 20 L76 40 L80 8 L86 32 L96 28 L300 28" stroke="#31b9a4" fill="none" stroke-width="1.6"/></svg>
          <div class="vitals"><div><span>HR</span><b>128</b></div><div><span>ART</span><b>78/44</b></div><div><span>SpO2</span><b>94</b></div></div>
        </div>
        <div class="card">You cannot see the bleeder.</div>
        <button class="cta">Tell him. Do not just treat it.</button>
      </div>`,
      scrub: `<div class="pad">
        <p class="meta">HE WILL ASK FOR 2-0 silk tie because the artery is clamped and the next thing is the knot, not the knife.</p>
        <div class="chips"><span class="chip on">2-0 silk tie</span><span class="chip">#10 blade</span><span class="chip">Kelly</span></div>
        <div class="card">You can see both of them.</div>
        <button class="cta" id="slap">Slap it in his hand. +10</button>
      </div>`,
    }[seat];
    return `${chrome("SURGERY VERSE · " + kase.toUpperCase(), seat.toUpperCase(), state.points, 72)}
      <div class="pad">
        <p class="meta">Three people, one patient, and only one of them can see the bleeding.</p>
        <div class="seat-grid">
          ${["surgeon", "anaesthesia", "scrub"].map((s) => `<button class="chip ${seat === s ? "on" : ""}" data-seat="${s}">${s}</button>`).join("")}
        </div>
        <div class="chips" style="margin-top:8px">
          <button class="chip" data-spin="-1">spin ←</button>
          <span class="chip on">${kase}</span>
          <button class="chip" data-spin="1">spin →</button>
        </div>
      </div>
      ${body}
      <div class="pad"><p class="fine">Same seed, both teams. Faster and wronger still loses. Errors first. Time only breaks ties.</p></div>`;
  }
  function bindVerse() {
    view().querySelectorAll("[data-seat]").forEach((b) => {
      b.addEventListener("click", () => { state.verseSeat = b.getAttribute("data-seat"); render(); });
    });
    view().querySelectorAll("[data-spin]").forEach((b) => {
      b.addEventListener("click", () => {
        state.verseCase = (state.verseCase + +b.getAttribute("data-spin") + CASES.length) % CASES.length;
        render();
      });
    });
    const slap = $("#slap");
    if (slap) slap.addEventListener("click", () => { state.points += 10; render(); });
  }

  function traumaRemain(t) {
    if (t.dead) return 0;
    const c = Math.max(0, Math.min(100, t.coherence));
    const arrest = 78 - 22 * (c / 100);
    const buy = 110 - 43 * (c / 100);
    if (t.tube) return buy;
    let base = arrest;
    if (t.needle) base += buy;
    return Math.max(0, base - t.elapsed);
  }
  function traumaVitals(t) {
    if (t.tube) return { hr: 92, sbp: 118, dbp: 72, spo2: 97 };
    const deadline = 78 - 22 * (t.coherence / 100);
    let frac = 1 - traumaRemain(t) / Math.max(deadline, 0.01);
    if (t.fluid) frac += 0.15;
    let hr = 118 + 40 * frac, sbp = 92 - 38 * frac, dbp = 58 - 22 * frac, spo2 = 94 - 22 * frac;
    if (t.needle && !t.tube) { sbp += 8; spo2 += 4; hr -= 8; }
    return { hr: Math.round(hr), sbp: Math.round(sbp), dbp: Math.round(dbp), spo2: Math.max(40, Math.round(spo2)) };
  }
  function mmss(s) {
    const n = Math.max(0, Math.floor(s));
    return String(Math.floor(n / 60)).padStart(2, "0") + ":" + String(n % 60).padStart(2, "0");
  }
  function traumaView() {
    const t = state.trauma;
    const v = traumaVitals(t);
    const rem = traumaRemain(t);
    return `${chrome("TRAUMA MODE · CASE 07", "Tension pneumothorax", t.points, t.coherence)}
      <div class="pad">
        <div class="chips">
          <span class="chip" style="color:var(--red);border-color:var(--red)">ACUITY ×2.5</span>
          <span class="chip" style="color:var(--amber);border-color:var(--amber)">PATIENT DEATH ENABLED</span>
        </div>
        <div class="monitor" style="margin-top:10px">
          <div class="who">ECG II</div>
          <svg class="ecg" viewBox="0 0 300 54"><path d="M0 28 L18 28 L22 22 L26 40 L30 10 L36 34 L46 28 L64 28 L68 22 L72 40 L76 10 L82 34 L92 28 L300 28" stroke="#31b9a4" fill="none" stroke-width="1.7"/></svg>
          <div class="vitals">
            <div><span>HR</span><b>${v.hr}</b></div>
            <div><span>BP</span><b>${v.sbp}/${v.dbp}</b></div>
            <div><span>SpO2</span><b>${v.spo2}</b></div>
          </div>
        </div>
        <div class="card teal" style="margin-top:10px">
          <div class="who">ANAESTHESIA</div>
          Pressure is falling and I cannot ventilate him. This is obstructive, not hypovolaemic. Move.
        </div>
        <div class="card red">
          TIME TO DECOMPRESSION · Arrest at current trajectory
          <span class="timer" style="float:right">${t.dead ? "ARREST" : t.tube ? "HOLDING" : mmss(rem)}</span>
        </div>
        <button class="opt" data-t="needle">Needle decompression, 2nd ICS<span class="sub">buys time, does not fix it</span></button>
        <button class="opt" data-t="tube">Tube thoracostomy, 5th ICS<span class="sub">definitive</span></button>
        <button class="opt" data-t="fluid">Fluid bolus<span class="sub">wrong physiology</span></button>
        <div class="card amber"><div class="who">COHERENCE IS RUNNING THE CLOCK</div>
          You are ahead of this module, so the deterioration model is running faster than baseline.</div>
        <p class="fine">${t.dead ? "Death voids the case score." : t.tube ? "Tube in. Field holding." : "Errors first. Time only breaks ties."}
          Full 10-step Module 21 is unchanged at <a href="ai-surgeon-module02-trauma.html">ai-surgeon-module02-trauma.html</a>.</p>
      </div>`;
  }
  let traumaTimer = null;
  function bindTrauma() {
    if (traumaTimer) clearInterval(traumaTimer);
    traumaTimer = setInterval(() => {
      const t = state.trauma;
      if (t.dead || t.tube) return;
      t.elapsed += 1;
      if (traumaRemain(t) <= 0) {
        t.dead = true;
        t.points = 0;
      }
      if (route() === "trauma") render();
    }, 1000);
    view().querySelectorAll("[data-t]").forEach((b) => {
      b.addEventListener("click", () => {
        const a = b.getAttribute("data-t");
        const t = state.trauma;
        if (t.dead) return;
        if (a === "needle") { t.needle = true; t.points += 10; }
        if (a === "tube") { t.tube = true; t.points += Math.round(25 * t.acuity); }
        if (a === "fluid") { t.fluid = true; t.points += Math.round(-25 * t.acuity); }
        render();
      });
    });
  }

  function anatomy() {
    const src = state.anatomyShot === "a" ? "stills/05-cecum-appendix-a.png" : "stills/06-cecum-appendix-b.png";
    return `${chrome("ANATOMY · SCANNED MESH", "Cecum and appendix", state.points, 70)}
      <div class="field" style="min-height:360px">
        <img class="anat" src="${src}" alt="Raw cecum/appendix 3D asset">
      </div>
      <div class="pad">
        <div class="chips">
          <button class="chip ${state.anatomyShot === "a" ? "on" : ""}" data-shot="a">Mesh A</button>
          <button class="chip ${state.anatomyShot === "b" ? "on" : ""}" data-shot="b">Mesh B</button>
          <button class="chip" data-go="identify">Identify on this</button>
          <button class="chip" data-go="lab">Open in The Lab</button>
        </div>
        <p class="fine">BodyParts3D / Z-Anatomy / Visible Human is the production path. These stills are the visual spec for identify, lab, verse, and anatomy views. Shader-driven wet look; Figma is chrome only.</p>
      </div>`;
  }
  function bindAnatomy() {
    view().querySelectorAll("[data-shot]").forEach((b) => {
      b.addEventListener("click", () => { state.anatomyShot = b.getAttribute("data-shot"); render(); });
    });
  }

  function pitch(still, title, note) {
    return `${chrome("PITCH STILL", title, state.points, 70)}
      <img class="still-full" src="${still}" alt="${title}">
      <div class="pad"><p class="fine">${note}</p>
        <button class="cta" data-go="hub">Back to screens</button></div>`;
  }

  const PITCH = {
    hardware: ["stills/03-hardware-ladder.png", "Hardware ladder",
      "Phone ships first. iPad is the desk tier. VR is king. One codebase, three tiers. The tier changes what your hands are doing, never what you have to know."],
    art: ["stills/02-art-fidelity.png", "Art fidelity",
      "Placeholder vs scanned mesh. Wet shader, not outlines. Figma is chrome only."],
    tablet: ["stills/08-tablet-pencil-mat.png", "Tablet + pencil + mat",
      "Desk tier. Hands on the mat, eyes on the field. Conductive pads, no battery in the cheap version."],
    stylus: ["stills/10-twist-stylus.png", "Twist stylus",
      "A barrel, a detent ring, a nib. No radio, no battery, no firmware. Out of the box it is a scalpel."],
    stills: ["stills/04-identify-before-you-cut.png", "Stills", "All sixteen stills are on the hub."],
  };

  function render() {
    const r = route();
    const root = view();
    const map = {
      hub, identify, lab, study, see, do: doOne, call: callView,
      anesthesia, nib, verse, trauma: traumaView, anatomy,
    };
    if (map[r]) root.innerHTML = map[r]();
    else if (PITCH[r]) root.innerHTML = pitch(...PITCH[r]);
    else root.innerHTML = hub();

    root.querySelectorAll("[data-go]").forEach((b) => {
      b.addEventListener("click", () => go(b.getAttribute("data-go")));
    });
    if (r === "identify") bindIdentify();
    if (r === "lab") bindLab();
    if (r === "study") bindStudy();
    if (r === "see") bindSee();
    if (r === "do") bindDo();
    if (r === "call") bindCall();
    if (r === "anesthesia") bindAnesthesia();
    if (r === "nib") bindNib();
    if (r === "verse") bindVerse();
    if (r === "trauma") bindTrauma();
    if (r === "anatomy") bindAnatomy();
  }

  window.addEventListener("hashchange", render);
  window.addEventListener("keydown", (ev) => {
    if (ev.key === "ArrowLeft" || ev.key === "q") {
      if (route() === "nib") { state.trayOpen = true; state.trayIndex = (state.trayIndex + TRAY.length - 1) % TRAY.length; render(); }
      if (route() === "anesthesia") { state.airway = (state.airway + 2) % 3; render(); }
    }
    if (ev.key === "ArrowRight" || ev.key === "e") {
      if (route() === "nib") { state.trayOpen = true; state.trayIndex = (state.trayIndex + 1) % TRAY.length; render(); }
      if (route() === "anesthesia") { state.airway = (state.airway + 1) % 3; render(); }
    }
    if (ev.key === "Enter" && route() === "nib" && state.trayOpen) {
      const legal = LEGAL[state.step] || TRAY;
      state.tool = legal[state.trayIndex % legal.length];
      state.trayOpen = false;
      render();
    }
  });
  document.addEventListener("DOMContentLoaded", render);
})();
