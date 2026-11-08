"""Dresses the built web app as dx.bi: name, icons and colours, and dx.bi itself built in.

Run after `pnpm build`, from the stremio-web checkout:  python3 brand.py <build dir> <dxbi-stremio checkout> <dxbi-web checkout>
Stremio's code is left as it is; only the page's name, icons and install details change, and dx.bi
(the released plugin, with its built-in look) is added for browsers.
"""
import hashlib, json, re, shutil, sys, pathlib

build, dxbi, web = (pathlib.Path(p) for p in sys.argv[1:4])
out = build / "dxbi"
out.mkdir(exist_ok=True)

# dx.bi itself, and its icons
shutil.copy(dxbi / "dxbi.plugin.js", out / "dxbi.plugin.js")
shutil.copy(web / "dxbi" / "web.js", out / "web.js")
images = dxbi / "app" / "images"
shutil.copy(images / "icon.ico", out / "favicon.ico")
shutil.copy(images / "icon-256.png", out / "icon-256.png")
shutil.copy(images / "icon-512.png", out / "icon-512.png")

# The page: dx.bi's name, icon and colour; Stremio's branded splash screens go
page = build / "index.html"
html = page.read_text()
html = re.sub(r"<title>.*?</title>", "<title>dx.bi</title>", html, flags=re.S)
html = html.replace('content="Stremio"', 'content="dx.bi"')
html = re.sub(r'<meta name="theme-color" content="[^"]*">', '<meta name="theme-color" content="#0b0b0d">', html)
html = re.sub(r'<link rel="icon"[^>]*>', '<link rel="icon" type="image/x-icon" href="dxbi/favicon.ico">', html)
html = re.sub(r'<link rel="apple-touch-icon"[^>]*>', '<link rel="apple-touch-icon" href="dxbi/icon-256.png">', html)
html = re.sub(r'\s*<link rel="apple-touch-startup-image"[^>]*>', "", html)
html = html.replace("</head>", '    <script src="dxbi/web.js"></script>\n</head>', 1)
# dx.bi's own loading screen, painted from the very first frame (part of the page, so nothing of
# Stremio's shows while its scripts start). It hands over to dx.bi's intro when that plays, or fades
# into the app once dx.bi's look is on and there's something to show.
boot = (web / "dxbi" / "boot.html").read_text()
html = html.replace("</head>", boot.split("<!--body-->")[0] + "</head>", 1)
html, n = re.subn(r"<body([^>]*)>", lambda mm: "<body" + mm.group(1) + ">" + boot.split("<!--body-->")[1], html, count=1)
assert n == 1, "no <body> in index.html"
page.write_text(html)

# Installing it as an app (Add to Home Screen): dx.bi's name and icons
manifest = build / "manifest.json"
m = json.loads(manifest.read_text())
m.update({
    "name": "dx.bi",
    "short_name": "dx.bi",
    "description": "Netflix-style Stremio",
    "background_color": "#0b0b0d",
    "theme_color": "#0b0b0d",
    "icons": [
        {"src": "dxbi/icon-256.png", "sizes": "256x256", "type": "image/png"},
        {"src": "dxbi/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "dxbi/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
})
manifest.write_text(json.dumps(m, indent=2))
# The offline cache knows index.html by a revision code made before the changes above: a new one,
# so browsers that already have the page take the dx.bi one
sw = build / "service-worker.js"
if sw.exists():
    rev = hashlib.md5(page.read_bytes()).hexdigest()
    code = sw.read_text()
    # (either order, keys quoted or not: {url:"index.html",revision:"…"} / {"revision":"…","url":"index.html"})
    code, n1 = re.subn(r'(\{"?url"?:"index\.html","?revision"?:")[0-9a-f]+(")', lambda mm: mm.group(1) + rev + mm.group(2), code)
    code, n2 = re.subn(r'(\{"?revision"?:")[0-9a-f]+(","?url"?:"index\.html")', lambda mm: mm.group(1) + rev + mm.group(2), code)
    n = n1 + n2
    sw.write_text(code)
    print("service worker index.html revision updated:", n)

print("branded:", page, manifest, "plugin", (out / "dxbi.plugin.js").stat().st_size, "bytes")
