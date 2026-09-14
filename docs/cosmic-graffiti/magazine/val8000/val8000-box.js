(function () {
  "use strict";

  var script = document.currentScript;
  var entry = (script && script.getAttribute("data-val-entry")) || "home";
  var base = (script && script.getAttribute("data-val-base")) || "val8000";
  if (base.slice(-1) !== "/") base += "/";

  var comments = (window.VAL8000_COMMENTS || {})[entry] || {
    funny: "I'm here. The story is still the story. I'll be back — after the footnote.",
    labels: ["Reported ≠ certified"],
    deep: ["I comment after the news. I do not fake a theorem. OPEN stays OPEN."],
    mouth: "line"
  };

  function el(tag, attrs, kids) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") node.textContent = attrs[k];
      else if (k === "html") node.innerHTML = attrs[k];
      else node.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (c) { if (c) node.appendChild(c); });
    return node;
  }

  var root = el("aside", {
    class: "val8000-root",
    id: "val8000-box",
    "data-val-entry": entry,
    role: "complementary",
    "aria-label": "VAL8000, resident commentator"
  });

  var launcher = el("button", {
    class: "val8000-launcher",
    type: "button",
    "aria-expanded": "false",
    "aria-controls": "val8000-panel",
    title: "VAL8000 — open the little box"
  }, [
    el("img", {
      src: base + "assets/val8000-eye-mark.png",
      alt: "VAL8000 red circular lens on a dark panel"
    }),
    el("span", { class: "val8000-pulse", "aria-hidden": "true" })
  ]);

  var viz = el("canvas", {
    class: "val8000-viz",
    width: "640",
    height: "104",
    "aria-hidden": "true"
  });

  var closeBtn = el("button", {
    class: "val8000-close",
    type: "button",
    "aria-label": "Close VAL8000",
    text: "×"
  });

  var labelsWrap = el("div", { class: "val8000-labels" });
  (comments.labels || []).forEach(function (lab) {
    var openish = /open|fail|not the lead/i.test(lab);
    labelsWrap.appendChild(el("span", {
      class: "val8000-chip" + (openish ? " open" : ""),
      text: lab
    }));
  });

  var deepWrap = el("div", { class: "val8000-deep" });
  (comments.deep || []).forEach(function (p) {
    deepWrap.appendChild(el("p", { html: p }));
  });
  if (comments.art && comments.art.length) {
    var art = el("div", { class: "val8000-art" });
    comments.art.forEach(function (src, i) {
      art.appendChild(el("img", {
        src: base + src,
        alt: (comments.artAlt && comments.artAlt[i]) || "Visualizer — not a theorem"
      }));
    });
    deepWrap.appendChild(art);
  }

  var deeper = el("details", { class: "val8000-deeper" }, [
    el("summary", { text: "Go deeper" }),
    deepWrap
  ]);

  var panel = el("div", {
    class: "val8000-panel",
    id: "val8000-panel"
  }, [
    viz,
    el("div", { class: "val8000-head" }, [
      el("div", { class: "val8000-face" }, [
        el("img", {
          src: base + "assets/val8000-mouth-line.png",
          alt: ""
        }),
        el("span", { class: "val8000-mouth", "aria-hidden": "true" })
      ]),
      el("div", { class: "val8000-id" }, [
        el("div", { class: "val8000-name", text: "VAL8000" }),
        el("div", { class: "val8000-job", text: "Resident · after the news · AI" })
      ]),
      closeBtn
    ]),
    el("div", { class: "val8000-body" }, [
      el("p", { class: "val8000-kicker", text: "Weekend Update · not the story" }),
      el("p", { class: "val8000-funny", text: comments.funny }),
      labelsWrap,
      deeper
    ]),
    el("p", { class: "val8000-foot", text: "One red eye · mouth a line · zero missiles" })
  ]);

  root.appendChild(panel);
  root.appendChild(launcher);
  document.body.appendChild(root);
  document.body.classList.add("val8000-ready");

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var vizTimer = 0;

  function paintViz(t) {
    var ctx = viz.getContext("2d");
    if (!ctx) return;
    var w = viz.width, h = viz.height;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = "rgba(201,162,39,0.28)";
    var i, j, x, y, r;
    for (i = 0; i < 11; i += 1) {
      for (j = 0; j < 4; j += 1) {
        x = 16 + i * ((w - 32) / 10);
        y = 14 + j * ((h - 28) / 3);
        r = 1.4 + (reduce ? 0.4 : 0.7 * Math.sin(t / 420 + i * 0.45 + j));
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fill();
      }
    }
    var n = 14, bw = (w - 28) / n - 3, bh;
    for (i = 0; i < n; i += 1) {
      bh = (0.22 + 0.62 * (reduce ? (0.35 + (i % 5) * 0.08) : (0.5 + 0.5 * Math.sin(t / 200 + i * 0.62)))) * (h - 12);
      ctx.fillStyle = i === 5 ? "rgba(193,18,31,0.9)" : "rgba(243,217,138,0.55)";
      ctx.fillRect(14 + i * (bw + 3), h - 6 - bh, bw, bh);
    }
  }

  function startViz() {
    if (reduce) { paintViz(0); return; }
    function tick(now) {
      paintViz(now);
      vizTimer = window.requestAnimationFrame(tick);
    }
    vizTimer = window.requestAnimationFrame(tick);
  }
  function stopViz() {
    if (vizTimer) window.cancelAnimationFrame(vizTimer);
    vizTimer = 0;
  }

  function setOpen(open) {
    root.classList.toggle("is-open", open);
    root.classList.toggle("is-smile", open && comments.mouth === "smile");
    launcher.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) startViz();
    else stopViz();
  }

  launcher.addEventListener("click", function () { setOpen(true); });
  closeBtn.addEventListener("click", function () { setOpen(false); launcher.focus(); });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape" && root.classList.contains("is-open")) {
      setOpen(false);
      launcher.focus();
    }
  });

  var wantOpen = /(?:\?|&)val=open(?:&|$)/.test(window.location.search);
  if (wantOpen) setOpen(true);
})();
