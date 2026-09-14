(function () {
  "use strict";

  var LINE = "/val8000/val8000-mouth-line.png";
  var SMILE = "/val8000/val8000-mouth-smile.png";

  var FIELDS = [
    {
      id: "decExpr",
      pane: "decompose",
      label: "Decompose expression",
      fill: "xdd + k*x = 0",
      say: [
        "Empty decompose. I parked an incomplete oscillator — missing damping is a role hole, not a solved mountain.",
        "I do not invent theorems. Correspondence is a hypothesis, not physical equivalence.",
        "Unaugmented leftover stays OPEN. DA-VC-01 stays FAIL."
      ]
    },
    {
      id: "trLeft",
      pane: "translate",
      label: "System A",
      fill: "m*xdd + c*xd + k*x = f",
      say: [
        "System A was blank. Mechanical oscillator is a labeled example with an executable T on the electrical twin.",
        "I will not stamp TRANSFORMABLE without a real T. SND vs H_N still refuses a letter map."
      ]
    },
    {
      id: "trRight",
      pane: "translate",
      label: "System B",
      fill: "L*qdd + R*qd + kC*q = v",
      say: [
        "System B was blank. Series RLC is the twin that actually has a T, not a slogan.",
        "I will not stamp TRANSFORMABLE without a real T. Unaugmented leftover stays OPEN."
      ]
    },
    {
      id: "syTarget",
      pane: "synthesize",
      label: "Target state",
      fill: "x★ = 1",
      say: [
        "Empty target. x★ = 1 is a desired state for the analog loop — a hypothesis, not a tank certificate.",
        "I do not close OPEN leftovers. DA-VC-01 stays FAIL."
      ]
    },
    {
      id: "syConstraints",
      pane: "synthesize",
      label: "Constraints",
      fill: "|u| ≤ 6, manufacturable",
      say: [
        "Constraints were blank. I filled a bounded, manufacturable request. Hardware 15% is still not a 3D NS proof.",
        "DA-VC-01 stays FAIL."
      ]
    },
    {
      id: "cyExciseK",
      pane: "cycle",
      label: "Step k",
      fill: "7",
      say: [
        "Step k was blank. Default classical surgery cuts leftover 7–8. Step 2 is Ring Lemma and is already PROVED.",
        "I will not close the unaugmented leftover. DA-VC-01 stays FAIL."
      ]
    }
  ];

  var ASK_STARTERS = [
    {
      q: "Why does cream swirl in coffee?",
      known: "The cream is a tracer riding a viscous velocity. Navier–Stokes is the street map of that ride in a cup.",
      open: "Whether every smooth three-dimensional start stays smooth is still an analysis question. I will not close it.",
      picture: "Cream is a tourist. The cup mixed. The mountain did not move. Unaugmented leftover stays OPEN. DA-VC-01 stays FAIL."
    },
    {
      q: "Are swirl Φ, lab Φ, and slider φ the same object?",
      known: "Same glyph, several jobs. Swirl Φ = u_θ/r is not Domain Architect leftover Φ, not Newtonian Φ_g, not compact SFE Φ, not slider φ.",
      open: "Correspondence across pictures is a hypothesis, not physical equivalence. I will not stamp TRANSFORMABLE without a real T.",
      picture: "Sticky notes, not a wedding. Letters collide. I do not glue them."
    }
  ];

  function $(id) {
    return document.getElementById(id);
  }

  function activePane() {
    var pane = document.querySelector(".pane.active");
    return pane ? pane.id : "decompose";
  }

  function unanswered(paneId) {
    var pane = paneId || activePane();
    return FIELDS.filter(function (f) {
      if (f.pane !== pane) return false;
      var node = $(f.id);
      return node && !String(node.value || "").trim();
    });
  }

  function setMouth(which) {
    var img = $("val8000-face");
    var dock = $("val8000-dock");
    if (!img || !dock) return;
    img.src = which === "smile" ? SMILE : LINE;
    img.alt = which === "smile"
      ? "VAL8000 red circular lens and a smile on a dark square panel"
      : "VAL8000 red circular lens and a straight mouth line on a dark square panel";
    dock.classList.toggle("is-smile", which === "smile");
  }

  function showAnswer(lines, smile) {
    var dock = $("val8000-dock");
    var box = $("val8000-answer");
    var status = $("val8000-status");
    if (!dock || !box || !status) return;
    dock.classList.add("is-help");
    box.hidden = false;
    box.innerHTML = lines.map(function (p) {
      return "<p>" + p + "</p>";
    }).join("");
    status.textContent = smile
      ? "Answered. Mouth a smile. I still do not fly the ship."
      : "Idle. Mouth a line. If a field is empty, I can help with unanswered questions.";
    setMouth(smile ? "smile" : "line");
  }

  function helpUnanswered() {
    var pane = activePane();
    var miss = unanswered(pane);
    var lines;
    if (!miss.length) {
      var ask = $("val8000-ask");
      if (ask && !String(ask.value || "").trim()) {
        var starter = ASK_STARTERS[0];
        ask.value = starter.q;
        lines = [
          "Ask the Desk was blank. I parked a starter, not a theorem.",
          "<strong>Q.</strong> " + starter.q,
          "<strong>Known.</strong> " + starter.known,
          "<strong>Open.</strong> " + starter.open,
          "<strong>Picture.</strong> " + starter.picture
        ];
        showAnswer(lines, true);
        return;
      }
      lines = [
        "Every field on this pane already has an answer. I will not invent a theorem on top.",
        "Unaugmented leftover stays OPEN. I will not stamp TRANSFORMABLE without a real T. DA-VC-01 stays FAIL."
      ];
      showAnswer(lines, true);
      return;
    }
    var first = miss[0];
    var node = $(first.id);
    if (node) node.value = first.fill;
    lines = [
      "Unanswered: <strong>" + first.label + "</strong>. I filled a labeled example. I do not invent theorems."
    ].concat(first.say);
    showAnswer(lines, true);
    if (node) node.focus();
  }

  function idleIfEmptyHelp() {
    var miss = unanswered();
    if (miss.length) setMouth("line");
  }

  var helpBtn = $("val8000-help");
  if (helpBtn) helpBtn.addEventListener("click", helpUnanswered);

  ["decRun", "trRun", "syRun", "cyRun", "cyExciseStep"].forEach(function (id) {
    var btn = $(id);
    if (!btn) return;
    btn.addEventListener("click", function () {
      var miss = unanswered();
      if (id === "cyExciseStep") miss = unanswered("cycle");
      if (id === "decRun") miss = unanswered("decompose");
      if (id === "trRun") miss = unanswered("translate");
      if (id === "syRun") miss = unanswered("synthesize");
      if (miss.length) helpUnanswered();
    }, true);
  });

  document.querySelectorAll(".tab").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var miss = unanswered(btn.getAttribute("data-pane"));
      if (miss.length) {
        setMouth("line");
        var status = $("val8000-status");
        if (status) {
          status.textContent = "Idle. Mouth a line. This pane has an unanswered field. I can help.";
        }
      }
    });
  });

  FIELDS.forEach(function (f) {
    var node = $(f.id);
    if (!node) return;
    node.addEventListener("input", idleIfEmptyHelp);
  });

  window.VAL8000 = {
    helpUnanswered: helpUnanswered,
    unanswered: unanswered,
    setMouth: setMouth
  };

  setMouth("line");
})();
