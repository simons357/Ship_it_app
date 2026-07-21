(() => {
  const year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());

  const header = document.querySelector("[data-header]");
  const onScroll = () => {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 18);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  document
    .querySelectorAll(
      ".section-intro, .work-item, .research-grid article, .about-panel, .contact-block, .also-list, .ip-note"
    )
    .forEach((el) => {
      el.classList.add("reveal");
    });

  if (!reduceMotion && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.16, rootMargin: "0px 0px -8% 0px" }
    );
    document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
  } else {
    document.querySelectorAll(".reveal").forEach((el) => el.classList.add("is-visible"));
  }

  const filterButtons = Array.from(document.querySelectorAll(".filter-btn"));
  const workItems = Array.from(document.querySelectorAll("[data-work-list] > li"));
  const emptyState = document.querySelector("[data-filter-empty]");

  const applyFilter = (filter) => {
    let visible = 0;
    workItems.forEach((item) => {
      const category = item.getAttribute("data-category");
      const show = filter === "all" || category === filter;
      item.classList.toggle("is-hidden", !show);
      if (show) visible += 1;
    });
    if (emptyState) emptyState.hidden = visible > 0;

    filterButtons.forEach((btn) => {
      const active = btn.getAttribute("data-filter") === filter;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-selected", active ? "true" : "false");
    });
  };

  filterButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      applyFilter(btn.getAttribute("data-filter") || "all");
    });
  });

  const canvas = document.getElementById("field");
  if (!canvas || !(canvas instanceof HTMLCanvasElement)) return;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  let width = 0;
  let height = 0;
  let dpr = 1;
  let raf = 0;
  let t0 = performance.now();

  const resize = () => {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = canvas.clientWidth;
    height = canvas.clientHeight;
    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };

  const draw = (now) => {
    const t = (now - t0) / 1000;
    ctx.clearRect(0, 0, width, height);

    const cx = width * 0.62;
    const cy = height * 0.42;
    const rings = 9;

    for (let i = 0; i < rings; i += 1) {
      const progress = i / (rings - 1);
      const radius = Math.min(width, height) * (0.12 + progress * 0.55);
      const pulse = Math.sin(t * 0.55 + progress * 2.4) * 0.5 + 0.5;
      const alpha = 0.045 + pulse * 0.05;

      ctx.beginPath();
      ctx.ellipse(cx, cy, radius * 1.25, radius * 0.72, -0.35 + Math.sin(t * 0.15) * 0.05, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(47, 143, 123, ${alpha})`;
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    for (let i = 0; i < 5; i += 1) {
      const y = height * (0.2 + i * 0.14);
      ctx.beginPath();
      for (let x = 0; x <= width; x += 8) {
        const wave =
          Math.sin((x / width) * Math.PI * (2.2 + i * 0.35) + t * (0.4 + i * 0.08)) * (10 + i * 3) +
          Math.sin((x / width) * Math.PI * 5.5 - t * 0.25 + i) * 4;
        const yy = y + wave;
        if (x === 0) ctx.moveTo(x, yy);
        else ctx.lineTo(x, yy);
      }
      ctx.strokeStyle = `rgba(201, 164, 92, ${0.05 + i * 0.015})`;
      ctx.lineWidth = 1.25;
      ctx.stroke();
    }

    const nodes = 18;
    for (let i = 0; i < nodes; i += 1) {
      const a = (i / nodes) * Math.PI * 2 + t * 0.08;
      const r = Math.min(width, height) * 0.28;
      const x = cx + Math.cos(a) * r * 1.15;
      const y = cy + Math.sin(a) * r * 0.68;
      const glow = 0.35 + Math.sin(t + i) * 0.15;
      ctx.beginPath();
      ctx.arc(x, y, 1.6, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(231, 235, 230, ${glow})`;
      ctx.fill();
    }

    if (!reduceMotion) raf = requestAnimationFrame(draw);
  };

  resize();
  draw(performance.now());
  window.addEventListener("resize", () => {
    resize();
    if (reduceMotion) draw(performance.now());
  });

  if (reduceMotion) {
    cancelAnimationFrame(raf);
  }
})();
