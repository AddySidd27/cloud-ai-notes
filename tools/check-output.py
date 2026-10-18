#!/usr/bin/env python3
"""Post-build checks for a built site directory (default _site). Read-only; does not change the build.
Usage: python3 tools/check-output.py [OUTPUT_DIR] [--purge FILE]
Checks: (1) every internal href/src resolves, (2) every og:image file exists, (3) screenshot files in
img/avd for the privacy-reviewed sets (Post-03/04/05 *.png|*.jpg that are photos of the portal) are all in
tools/approved-screenshots.txt, (4) optional: none of the file names listed in --purge is present."""
import re, sys, glob, os, pathlib
args = [a for a in sys.argv[1:]]
purge = None
if "--purge" in args:
    i = args.index("--purge"); purge = args[i + 1]; del args[i:i + 2]
out = pathlib.Path(args[0] if args else "_site").resolve()
root = pathlib.Path(__file__).resolve().parent
approved = set(l.strip() for l in (root / "approved-screenshots.txt").read_text().splitlines() if l.strip())
bad = []
for f in glob.glob(str(out / "**/*.html"), recursive=True):
    t = open(f, errors="ignore").read()
    for m in re.finditer(r'(?:href|src)="(/[^"#?]*)', t):
        p = m.group(1)
        if p.startswith("//"): continue
        if not ((out / p.lstrip("/")).exists() or (out / p.lstrip("/") / "index.html").exists()):
            bad.append(f"broken ref {p} in {os.path.relpath(f, out)}")
    m = re.search(r'property="og:image" content="https?://[^/]+(/[^"]+)"', t)
    if m and not (out / m.group(1).lstrip("/")).exists():
        bad.append(f"missing og image {m.group(1)}")
shots = re.compile(r"AVD-Post-0[345]-(?!.*(Scope|Models|Kerberos|Hub|Connections|Identity)).*\.(png|jpg)$", re.I)
for f in (out / "img" / "avd").glob("*"):
    if shots.search(f.name) and f.name not in approved:
        bad.append(f"screenshot not in approved list: {f.name}")
if purge:
    for n in pathlib.Path(purge).read_text().split():
        n = n.split("/")[-1]
        if (out / "img" / "avd" / n).exists(): bad.append(f"purged file present: {n}")
print("\n".join(bad) if bad else "OK: all checks passed")
sys.exit(1 if bad else 0)
