const $ = (id) => document.getElementById(id);

async function api(path, body) {
  const options = body === undefined
    ? {}
    : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  const res = await fetch(path, options);
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    return { error: text || res.statusText };
  }
}

function show(el, payload) {
  const board =
    payload && payload.board && payload.board.text
      ? payload.board.text
      : payload && payload.prediction && payload.prediction.board && payload.prediction.board.text
        ? payload.prediction.board.text
        : "";
  const json = JSON.stringify(payload, null, 2);
  el.textContent = board ? board + "\n\n" + json : json;
}

document.querySelectorAll(".tab").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".pane").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(btn.dataset.pane).classList.add("active");
    document.body.classList.toggle("mark-open", btn.dataset.pane === "mark");
    if (btn.dataset.pane === "mark") {
      const silverOn = $("viewSilver") && !$("viewSilver").classList.contains("ghost");
      const labOn = $("viewLab") && !$("viewLab").classList.contains("ghost");
      showMarkView(labOn ? "lab" : silverOn ? "silver" : "gold");
    }
  });
});

function showMarkView(which) {
  const lab = document.getElementById("lambdaFrame");
  const renders = document.getElementById("rendersStudio");
  const buttons = {
    gold: document.getElementById("viewGold"),
    silver: document.getElementById("viewSilver"),
    lab: document.getElementById("viewLab"),
  };
  const labOn = which === "lab";
  if (lab) lab.hidden = !labOn;
  if (renders) renders.hidden = labOn;
  Object.entries(buttons).forEach(([key, el]) => {
    if (!el) return;
    el.classList.toggle("ghost", key !== which);
  });
  if (labOn) return;
  if (window.bindStudio) window.bindStudio();
  const innerId = which === "silver" ? "presetSilver" : "presetGold";
  const inner = document.getElementById(innerId);
  if (inner) inner.click();
  else if (window.applyStudioPreset) window.applyStudioPreset(which === "silver" ? "silver" : "gold");
}

["viewGold", "viewSilver", "viewLab"].forEach((id) => {
  const el = $(id);
  if (!el) return;
  el.addEventListener("click", () => showMarkView(id.replace("view", "").toLowerCase()));
});

document.querySelectorAll(".example").forEach((btn) => {
  btn.addEventListener("click", () => {
    $(btn.dataset.fill).value = btn.dataset.value;
  });
});

$("decRun").addEventListener("click", async () => {
  $("decOut").textContent = "Decomposing…";
  show($("decOut"), await api("/api/decompose", { expression: $("decExpr").value }));
});

$("trRun").addEventListener("click", async () => {
  $("trOut").textContent = "Translating…";
  show($("trOut"), await api("/api/translate", {
    left: $("trLeft").value,
    right: $("trRight").value,
  }));
});

$("trExample").addEventListener("click", async () => {
  $("trLeft").value = "m*xdd + c*xd + k*x = f";
  $("trRight").value = "L*qdd + R*qd + kC*q = v";
  $("trOut").textContent = "Translating mechanical ↔ electrical…";
  show($("trOut"), await api("/api/translate", { example: "mechanical-electrical" }));
});

$("trSndVsH").addEventListener("click", async () => {
  $("trLeft").value = "J/X >= cstar";
  $("trRight").value = "HN = D^((-1)/2)*Qtilde*D^((-1)/2)";
  $("trOut").textContent = "Translating Ring SND vs Q6 H_N (lab, not glue)…";
  show($("trOut"), await api("/api/translate", {
    left: $("trLeft").value,
    right: $("trRight").value,
  }));
});

$("syRun").addEventListener("click", async () => {
  $("syOut").textContent = "Synthesizing…";
  const constraints = $("syConstraints").value.split(",").map((s) => s.trim()).filter(Boolean);
  show($("syOut"), await api("/api/synthesize", {
    target: $("syTarget").value,
    constraints,
  }));
});

$("syAvailable").addEventListener("click", async () => {
  $("syTarget").value = "x → 0.85";
  $("syConstraints").value = "|u| ≤ 6, manufacturable, hardware already available";
  $("syOut").textContent = "Assembling available-tech 15% stack…";
  show($("syOut"), await api("/api/synthesize", {
    target: "x → 0.85",
    constraints: ["|u| ≤ 6", "manufacturable", "hardware already available"],
  }));
});

$("cyRun").addEventListener("click", async () => {
  $("cyOut").textContent = "Running cycle…";
  show($("cyOut"), await api("/api/cycle", { name: $("cyName").value }));
});

$("cyLeftover").addEventListener("click", async () => {
  $("cyName").value = "leftover-repair";
  $("cyOut").textContent = "Running leftover repair…";
  show($("cyOut"), await api("/api/cycle", { name: "leftover-repair" }));
});

$("cySurgery").addEventListener("click", async () => {
  $("cyName").value = "localized-repair";
  $("cyOut").textContent = "Running classical unaugmented surgery (default cut 7–8)…";
  show($("cyOut"), await api("/api/cycle", { name: "localized-repair" }));
});

$("cyOpenBoard").addEventListener("click", async () => {
  $("cyName").value = "open-board";
  $("cyOut").textContent = "Classifying the OPEN pile…";
  show($("cyOut"), await api("/api/cycle", { name: "open-board" }));
});

$("cyIntensity").addEventListener("click", async () => {
  $("cyName").value = "turbulence-intensity";
  $("cyOut").textContent = "Running intensity vs no-actuation control…";
  show($("cyOut"), await api("/api/cycle", { name: "turbulence-intensity" }));
});

$("cyAvailable").addEventListener("click", async () => {
  $("cyName").value = "available-turbulence";
  $("cyOut").textContent = "Assembling available-tech 15% stack…";
  show($("cyOut"), await api("/api/cycle", { name: "available-turbulence" }));
});

$("cyExciseStep").addEventListener("click", async () => {
  const raw = ($("cyExciseK").value || "").trim();
  const k = Number.parseInt(raw, 10);
  if (!Number.isInteger(k) || k < 1) {
    $("cyOut").textContent = "Enter a step number k to excise on the n-step chain.";
    return;
  }
  $("cyName").value = "localized-repair";
  $("cyOut").textContent = `Excising step ${k} and re-inserting the graft…`;
  show($("cyOut"), await api("/api/localized-repair", { excise: k }));
});

$("arRun").addEventListener("click", async () => {
  $("arOut").textContent = "Loading archive…";
  show($("arOut"), await api("/api/archive"));
});

$("shortcutBtn").addEventListener("click", async () => {
  const res = await fetch("/api/status");
  const status = await res.json();
  alert(
    "From a terminal in this repository:\n\n" +
    "python -m domain_architect app --install-shortcut\n\n" +
    "That writes Domain Architect to your Desktop.\n\n" +
    status.operations
  );
});

api("/api/status").then((status) => {
  $("decOut").textContent = status.description + "\n\n" + status.historical_note;
});
