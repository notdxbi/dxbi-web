# dx.bi web

dx.bi on the web, and the page the dx.bi apps run on: [Stremio's web app](https://github.com/Stremio/stremio-web)
built from a pinned, tested release, dressed as dx.bi (name, icons) with dx.bi built in, and published at
https://notdxbi.github.io/dxbi-web/. Open it in any browser to use dx.bi; the apps load it instead of
web.stremio.com, so a change on Stremio's site can't break them before it has been tested.

In a browser, debrid and direct streams play; torrents need the dx.bi app (Stremio's streaming server
only answers Stremio's own sites).

- Stremio's code is unchanged: Stremio/stremio-web at the tag in `.github/workflows/build.yml` (`STREMIO_WEB_REF`).
- Licence: GPL-2.0, the same as stremio-web (see LICENSE.md). dx.bi itself: https://github.com/notdxbi/dxbi-stremio
- Not affiliated with Stremio.
- dx.bi part: `dxbi/web.js` (loads the latest released dx.bi in browsers) and `tools/brand.py` (name, icons, install details).
