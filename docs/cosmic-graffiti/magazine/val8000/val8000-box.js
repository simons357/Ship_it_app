(function () {
  "use strict";

  var script = document.currentScript;
  var entry = (script && script.getAttribute("data-val-entry")) || "home";
  var base = (script && script.getAttribute("data-val-base")) || "val8000";
  if (base.slice(-1) !== "/") base += "/";

  var LINE = base + "assets/val8000-mouth-line.png";
  var SMILE = base + "assets/val8000-mouth-smile.png";
  var EYE_MARK = base + "assets/val8000-eye-mark.png";
  var HELP = window.VAL8000_HELP;
  var replyFn = window.VAL8000_reply;
  if (typeof HELP !== "string" || typeof replyFn !== "function") {
    throw new Error("VAL8000 reply catalog missing — load val8000-comments.js first");
  }

  function el(tag, attrs, kids) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") node.textContent = attrs[k];
      else node.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (c) {
      if (c) node.appendChild(c);
    });
    return node;
  }

  var reduce =
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var busy = false;
  var typeTimer = 0;

  var face = el("img", {
    class: "val8000-square-face",
    src: LINE,
    alt: "VAL8000, red circular lens and a straight mouth line on a dark panel",
    width: "72",
    height: "72",
  });

  var square = el(
    "button",
    {
      class: "val8000-square val8000-launcher",
      type: "button",
      title: "VAL8000 — always-visible square in the view. He types.",
      "aria-expanded": "true",
      "aria-controls": "val8000-panel",
    },
    [face]
  );

  var log = el("div", {
    class: "val8000-log",
    id: "val8000-log",
    role: "log",
    "aria-live": "polite",
    "aria-relevant": "additions",
  });
  log.appendChild(
    el("p", {
      class: "val8000-hint",
      text: "Type a question. He types back. No audio.",
    })
  );

  var input = el("input", {
    class: "val8000-input",
    id: "val8000-ask",
    type: "text",
    name: "val8000-question",
    maxlength: "280",
    autocomplete: "off",
    placeholder: "Type to VAL8000",
    "aria-label": "Type a question to VAL8000",
  });

  var send = el("button", {
    class: "val8000-send val8000-ask-btn",
    type: "submit",
    text: "Type",
  });

  var helpBtn = el("button", {
    class: "val8000-help",
    type: "button",
    text: "Help with unanswered",
  });

  var form = el(
    "form",
    {
      class: "val8000-form val8000-ask",
      action: "#",
      method: "get",
    },
    [
      el("label", { class: "val8000-ask-label", text: "Ask the Desk" }),
      input,
      send,
      helpBtn,
    ]
  );

  var hideBtn = el("button", {
    class: "val8000-hide val8000-close",
    type: "button",
    "aria-label": "Hide the type box. The square stays.",
    text: "–",
  });

  var panel = el(
    "div",
    {
      class: "val8000-panel",
      id: "val8000-panel",
    },
    [
      el("div", { class: "val8000-head" }, [
        el("div", { class: "val8000-id" }, [
          el("div", { class: "val8000-name", text: "VAL8000" }),
          el("div", { class: "val8000-job", text: "He types. Voice later." }),
        ]),
        hideBtn,
      ]),
      log,
      form,
      el("p", {
        class: "val8000-foot",
        text: "Typed transcript · no audio · clone voice later",
      }),
    ]
  );

  var root = el("aside", {
    class: "val8000-root is-open",
    id: "val8000-box",
    "data-val-entry": entry,
    "data-val-mode": "type",
    "data-val-audio": "off",
    "data-eye-mark": EYE_MARK,
    role: "complementary",
    "aria-label": "VAL8000 type box",
  });
  root.appendChild(square);
  root.appendChild(panel);
  document.body.appendChild(root);
  document.body.classList.add("val8000-ready");

  function setMouth(smile) {
    root.classList.toggle("is-smile", smile);
    root.classList.toggle("is-idle", !smile);
    face.src = smile ? SMILE : LINE;
    face.alt = smile
      ? "VAL8000, red circular lens and a smile after he typed"
      : "VAL8000, red circular lens and a straight mouth line on a dark panel";
  }

  function setOpen(open) {
    root.classList.toggle("is-open", open);
    root.classList.toggle("is-collapsed", !open);
    square.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) input.focus();
  }

  function addLine(role, text, typing, done) {
    var row = el("p", { class: "val8000-line val8000-line-" + role });
    row.appendChild(
      el("span", {
        class: "val8000-who",
        text: role === "val" ? "VAL8000" : "You",
      })
    );
    var body = el("span", { class: "val8000-typed" });
    row.appendChild(body);
    log.appendChild(row);
    log.scrollTop = log.scrollHeight;

    function finish() {
      body.textContent = text;
      log.scrollTop = log.scrollHeight;
      if (typeof done === "function") done();
    }

    if (!typing || reduce) {
      finish();
      return;
    }

    var i = 0;
    function tick() {
      i += 1;
      body.textContent = text.slice(0, i);
      log.scrollTop = log.scrollHeight;
      if (i < text.length) typeTimer = window.setTimeout(tick, 12);
      else if (typeof done === "function") done();
    }
    tick();
  }

  function ask(question) {
    var q = String(question || "").replace(/\s+/g, " ").trim();
    if (busy) return;
    if (!q) {
      helpBtn.click();
      return;
    }
    busy = true;
    input.value = "";
    input.disabled = true;
    send.disabled = true;
    helpBtn.disabled = true;
    setOpen(true);
    setMouth(false);
    addLine("you", q, false);
    var answer = replyFn(q, entry);
    addLine("val", answer, true, function () {
      setMouth(true);
      busy = false;
      input.disabled = false;
      send.disabled = false;
      helpBtn.disabled = false;
      input.focus();
    });
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    ask(input.value);
  });
  helpBtn.addEventListener("click", function () {
    var q = String(input.value || "").trim();
    if (q) {
      ask(q);
      return;
    }
    if (busy) return;
    busy = true;
    input.disabled = true;
    send.disabled = true;
    helpBtn.disabled = true;
    setOpen(true);
    setMouth(false);
    addLine("val", HELP, true, function () {
      setMouth(true);
      busy = false;
      input.disabled = false;
      send.disabled = false;
      helpBtn.disabled = false;
      input.focus();
    });
  });
  square.addEventListener("click", function () {
    setOpen(true);
    input.focus();
  });
  hideBtn.addEventListener("click", function () {
    setOpen(false);
    square.focus();
  });
  input.addEventListener("focus", function () {
    if (!busy) setMouth(false);
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape" && root.classList.contains("is-open")) {
      setOpen(false);
      square.focus();
    }
  });

  setMouth(false);
  if (/(?:\?|&)val=open(?:&|$)/.test(window.location.search)) setOpen(true);
})();
