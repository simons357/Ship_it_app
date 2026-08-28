/* Page-turn for the ~90 min kids episode. Scroll still works. */
(function () {
  const stage = document.querySelector(".stage");
  if (!stage) return;

  const pages = Array.from(
    stage.querySelectorAll("[data-page]")
  );
  if (pages.length < 2) return;

  const bar = document.createElement("div");
  bar.className = "readerbar";
  bar.innerHTML =
    '<button type="button" data-go="-1" aria-label="Previous page">←</button>' +
    '<span class="readerpos"></span>' +
    '<button type="button" data-go="1" aria-label="Next page">→</button>' +
    '<button type="button" class="readermode" type="button">Scroll all</button>' +
    '<span class="readerlove">You are loved. あなたは、愛されている。</span>';
  document.body.appendChild(bar);

  let i = 0;
  let paged = true;

  function clamp(n) {
    return Math.max(0, Math.min(pages.length - 1, n));
  }

  function paint() {
    const modeBtn = bar.querySelector(".readermode");
    const pos = bar.querySelector(".readerpos");
    if (!paged) {
      pages.forEach(function (p) {
        p.classList.remove("is-hidden-page");
      });
      modeBtn.textContent = "Page turn";
      pos.textContent = "all " + pages.length + " pages · ~90 min script";
      bar.querySelectorAll("[data-go]").forEach(function (b) {
        b.disabled = true;
      });
      return;
    }
    pages.forEach(function (p, idx) {
      p.classList.toggle("is-hidden-page", idx !== i);
    });
    modeBtn.textContent = "Scroll all";
    const label = pages[i].getAttribute("data-page") || String(i + 1);
    const clock = pages[i].getAttribute("data-t") || "";
    pos.textContent =
      i + 1 + " / " + pages.length + " · " + label + (clock ? " · " + clock : "");
    bar.querySelectorAll("[data-go]").forEach(function (b) {
      const d = Number(b.getAttribute("data-go"));
      b.disabled = (d < 0 && i === 0) || (d > 0 && i === pages.length - 1);
    });
    pages[i].scrollIntoView({ block: "start" });
  }

  function go(d) {
    if (!paged) return;
    i = clamp(i + d);
    paint();
  }

  bar.addEventListener("click", function (ev) {
    const btn = ev.target.closest("button");
    if (!btn) return;
    if (btn.classList.contains("readermode")) {
      paged = !paged;
      if (paged) {
        const vis = pages.findIndex(function (p) {
          const r = p.getBoundingClientRect();
          return r.bottom > 80 && r.top < window.innerHeight;
        });
        if (vis >= 0) i = vis;
      }
      document.body.classList.toggle("scroll-all", !paged);
      paint();
      return;
    }
    const d = btn.getAttribute("data-go");
    if (d) go(Number(d));
  });

  document.addEventListener("keydown", function (ev) {
    if (ev.defaultPrevented) return;
    const tag = (ev.target && ev.target.tagName) || "";
    if (tag === "INPUT" || tag === "TEXTAREA" || tag === "A") return;
    if (ev.key === "ArrowRight" || ev.key === "PageDown") {
      go(1);
      ev.preventDefault();
    } else if (ev.key === "ArrowLeft" || ev.key === "PageUp") {
      go(-1);
      ev.preventDefault();
    }
  });

  paint();
})();
