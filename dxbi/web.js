// dx.bi on the web: in a browser, this page is dx.bi, not plain Stremio. The dx.bi apps (desktop,
// TV, phones, iPhone) add dx.bi to the page themselves, so it steps aside there and isn't loaded twice.
(function () {
  var ua = navigator.userAgent;
  if (window.StremioEnhancedAPI || window.DxbiTV || /\bdxbi(-tv)?\//.test(ua)) return;
  // In a browser there's no streaming server to install: Stremio's "install it" bar has nothing for
  // dx.bi's visitors (debrid and direct streams play here; torrents need the dx.bi app)
  var style = document.createElement("style");
  style.id = "dxbi-web-style";
  style.textContent = '#app [class*="board-warning-container"] { display: none !important; }';
  document.head.appendChild(style);
  function load() {
    var s = document.createElement("script");
    s.src = "dxbi/dxbi.plugin.js";
    s.id = "dxbi.plugin.js";
    document.head.appendChild(s);
  }
  // as soon as Stremio's own scripts have run (they're at the end of the page), not after every
  // third-party script (Chromecast, Apple sign-in) has loaded too
  if (document.readyState !== "loading") load();
  else document.addEventListener("DOMContentLoaded", load, { once: true });
})();
