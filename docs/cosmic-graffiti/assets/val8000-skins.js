/* Clip-on VAL8000 skins. Accessories on the same square. He still types. No audio. */
(function (root) {
  "use strict";

  var DEFAULT_SKIN = "naked";
  var SKINS = {
    naked: { overlay: null, title: "Naked square" },
    frequency: { overlay: "overlay-frequency.png", title: "Frequency ribbon" },
    "weekend-update": {
      overlay: "overlay-weekend-update.png",
      title: "Weekend Update glasses",
    },
    issue1: { overlay: "overlay-issue1.png", title: "Issue 1 two-red-pill pin" },
    scientist: { overlay: "overlay-scientist.png", title: "Scientist visor" },
    "music-art": { overlay: "overlay-music-art.png", title: "Music and art room pin" },
    "glasses-ordinary": {
      overlay: "glasses-ordinary.png",
      title: "Ordinary glasses",
    },
    "glasses-camera": {
      overlay: "glasses-camera.png",
      title: "Camera-frame glasses",
    },
    monocle: {
      overlay: "monocle.png",
      title: "Monocle",
    },
    "tessellation-tray": { overlay: null, title: "Tessellation tray" },
  };

  function overlayDir(square) {
    var src = "";
    var face = square.querySelector(".val8000-square-face");
    if (face && face.getAttribute("src")) src = face.getAttribute("src");
    if (src.indexOf("/") === -1) return "skins/";
    return src.replace(/[^/]+$/, "") + "skins/";
  }

  function accessoryNode(square) {
    var node = square.querySelector(".val8000-accessory");
    if (node) return node;
    node = document.createElement("img");
    node.className = "val8000-accessory";
    node.alt = "";
    node.setAttribute("aria-hidden", "true");
    square.appendChild(node);
    return node;
  }

  function applySkin(square, id) {
    if (!square) return DEFAULT_SKIN;
    var skin = SKINS[id] ? id : DEFAULT_SKIN;
    square.setAttribute("data-skin", skin);
    var acc = accessoryNode(square);
    var spec = SKINS[skin];
    if (!spec.overlay) {
      acc.removeAttribute("src");
      acc.hidden = true;
      return skin;
    }
    acc.src = overlayDir(square) + spec.overlay;
    acc.hidden = false;
    return skin;
  }

  root.VAL8000_DEFAULT_SKIN = DEFAULT_SKIN;
  root.VAL8000_SKINS = SKINS;
  root.VAL8000_applySkin = applySkin;
})(typeof window !== "undefined" ? window : this);
