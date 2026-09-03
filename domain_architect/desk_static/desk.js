function show(el, data) {
  el.textContent = typeof data === "string" ? data : JSON.stringify(data, null, 2);
}

async function post(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res.json();
}

async function get(url) {
  const res = await fetch(url);
  return res.json();
}

document.getElementById("inquire").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const out = document.getElementById("inquire-out");
  out.textContent = "Working…";
  try {
    const data = await post("/api/audit", {
      expression: document.getElementById("expr").value,
    });
    show(out, data.narrative || data);
  } catch (err) {
    show(out, String(err));
  }
});

document.getElementById("run-jigsaw").addEventListener("click", async () => {
  const out = document.getElementById("compute-out");
  out.textContent = "Working…";
  try {
    const data = await get("/api/jigsaw?book=B");
    show(out, {
      goal: data.goal,
      building: data.building,
      energy_path: data.energy_path,
      reconstruct: {
        outside: data.reconstruct.outside,
        floor: data.reconstruct.floor,
        kinds: data.reconstruct.kinds,
      },
      smooth: data.smooth,
    });
  } catch (err) {
    show(out, String(err));
  }
});

document.getElementById("run-tube").addEventListener("click", async () => {
  const out = document.getElementById("compute-out");
  out.textContent = "Working…";
  try {
    const data = await get("/api/tube");
    show(out, {
      hardy: data.hardy_probe,
      wall_trace: data.wall_trace_probe,
      next: data.next,
      not_a_proof: true,
    });
  } catch (err) {
    show(out, String(err));
  }
});

document.getElementById("run-q").addEventListener("click", async () => {
  const out = document.getElementById("compute-out");
  out.textContent = "Working…";
  try {
    const data = await get("/api/jigsaw?book=Q");
    show(out, {
      book: data.book,
      building: data.building,
      reconstruct: data.reconstruct,
      note: "Arithmetic face. No operator→ζ lemma. Not a Zeta-zero prover.",
    });
  } catch (err) {
    show(out, String(err));
  }
});
