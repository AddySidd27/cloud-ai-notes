#!/usr/bin/env python3
"""Make 1200x630 social preview images (default + one per article) from the built site. Run after `npm run build`.
Usage: python3 tools/make-og.py   (needs playwright + chromium). Output goes to src/img/og/."""
import re, json, pathlib, html
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "_site"; out = root / "src/img/og"; out.mkdir(parents=True, exist_ok=True)
idx = json.loads((site / "search.json").read_text())
cover = re.search(r'<svg class="cv cv-azure".*?</svg>', (site / "azure/index.html").read_text(), re.S).group(0)
cover = re.sub(r'<text class="cv-n".*?</text>', '', cover, flags=re.S)
mark = re.search(r'<svg class="mark".*?</svg>', (site / "index.html").read_text(), re.S).group(0).replace('width="34" height="31"', 'width="64" height="58"')
def page(kicker, title, sub):
    return f'''<html><body style="margin:0;width:1200px;height:630px;background:#0A1B33;color:#EAF1F9;font-family:Archivo,'Segoe UI',Arial,sans-serif;position:relative;overflow:hidden">
<style>.m-a{{stroke:#EAF1F9}}.m-s{{stroke:#5AA9FF}}.m-n{{fill:#5AA9FF}}.cv-bg{{fill:transparent}}.cv-grid{{stroke:#8ED0FF;stroke-opacity:.12}}.cv-ln{{stroke:#8ED0FF;stroke-opacity:.8}}</style>
<div style="position:absolute;right:-40px;top:0;width:640px;height:630px;opacity:.55;-webkit-mask-image:linear-gradient(90deg,transparent,#000 50%)">{cover.replace('<svg ','<svg style="width:100%;height:100%" ',1)}</div>
<div style="position:absolute;left:72px;top:64px;display:flex;align-items:center;gap:16px">{mark}<span style="font-size:34px;font-weight:700">Adnan<b style="color:#8ED0FF">Siddiqui</b>.com</span></div>
<div style="position:absolute;left:72px;top:210px;width:900px">
<div style="font-size:26px;color:#8ED0FF;font-weight:600;margin-bottom:22px">{html.escape(kicker)}</div>
<div style="font-size:{58 if len(title)<60 else 48}px;line-height:1.08;font-weight:750;letter-spacing:-.02em">{html.escape(title)}</div></div>
<div style="position:absolute;left:72px;bottom:58px;font-size:24px;color:#A9BCD3">{html.escape(sub)}</div></body></html>'''
jobs = [("default", "Cloud architecture and engineering", "Cloud Architecture. Engineering. Real-World Technology.", "Azure · AVD · Windows 365 · Citrix · AWS · AI")]
for a in idx:
    slug = a["u"].strip("/").split("/")[-1]
    jobs.append((slug, a["s"] + " series", a["t"], "Technical article by Adnan Ahmed"))
jobs.append(("start-here", "Start here", "How this site is organized", "Technical article by Adnan Ahmed"))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 630})
    css = '@font-face{font-family:Archivo;src:url(file://%s);font-weight:100 900}' % (root / "src/fonts/archivo-latin-wdth-normal.woff2")
    for slug, k, t, s in jobs:
        pg.set_content(page(k, t, s).replace("<style>", "<style>" + css, 1)); pg.wait_for_timeout(150)
        pg.screenshot(path=str(out / f"{slug}.png"))
    # apple touch icon from the favicon
    pg.set_viewport_size({"width": 180, "height": 180})
    pg.set_content(f'<body style="margin:0"><img src="file://{root}/src/img/favicon.svg" width="180" height="180">'); pg.wait_for_timeout(150)
    pg.screenshot(path=str(root / "src/img/apple-touch-icon.png")); b.close()
print(len(jobs), "images")
