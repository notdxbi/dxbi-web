// dx.bi on the web: in a browser, this page is dx.bi, not plain Stremio. The dx.bi apps (desktop,
// TV, phones, iPhone) add dx.bi to the page themselves, so it steps aside there and isn't loaded twice.
(function () {
  var ua = navigator.userAgent;
  if (window.StremioEnhancedAPI || window.DxbiTV || /\bdxbi(-tv)?\//.test(ua)) return;
  function load() {
    var s = document.createElement("script");
    s.src = "dxbi/dxbi.plugin.js";
    s.id = "dxbi.plugin.js";
    document.head.appendChild(s);
  }
  // after Stremio's own scripts have started, as the apps load it
  if (document.readyState === "complete") load();
  else window.addEventListener("load", load, { once: true });
})();
