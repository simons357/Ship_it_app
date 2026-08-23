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
  el.textContent = JSON.stringify(payload, null, 2);
}

document.querySelectorAll(".tab").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".pane").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(btn.dataset.pane).classList.add("active");
  });
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

$("syRun").addEventListener("click", async () => {
  $("syOut").textContent = "Synthesizing…";
  const constraints = $("syConstraints").value.split(",").map((s) => s.trim()).filter(Boolean);
  show($("syOut"), await api("/api/synthesize", {
    target: $("syTarget").value,
    constraints,
  }));
});

$("cyRun").addEventListener("click", async () => {
  $("cyOut").textContent = "Running cycle…";
  show($("cyOut"), await api("/api/cycle", { name: $("cyName").value }));
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
