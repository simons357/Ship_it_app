(function bootChatVaultSkin() {
  var KEY = "chatvault.skin.v1";
  var ALLOWED = { steel: 1, ink: 1, signal: 1, day: 1 };
  var skin = "steel";
  try {
    var saved = localStorage.getItem(KEY);
    if (saved && ALLOWED[saved]) skin = saved;
    else if (saved) localStorage.setItem(KEY, "steel");
  } catch (err) {
    /* private mode */
  }
  document.documentElement.setAttribute("data-skin", skin);
})();
