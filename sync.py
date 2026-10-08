#!/usr/bin/env python3
"""Copy posts and diagrams from the blog source folders into site/src, adding site front matter
and rewriting relative links. The Markdown posts stay the source of truth and are never edited here."""
import re, json, shutil, pathlib, sys
ROOT = pathlib.Path("/home/claude/blog")
SRC = pathlib.Path(__file__).resolve().parent / "src"
POSTS = ROOT / "posts"
out_posts = SRC / "posts"; out_diag = SRC / "diagrams"
for d in (out_posts, out_diag):
    if d.exists(): shutil.rmtree(d)
    d.mkdir(parents=True)
for f in (ROOT / "diagrams").glob("*.svg"): shutil.copy(f, out_diag / f.name)

files = sorted(POSTS.glob("*.md"))
slug_of = {}
meta = {}
for f in files:
    t = f.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    fm, body = m.group(1), m.group(2)
    slug = re.search(r'^slug:\s*"?([^"\n]+)"?', fm, re.M).group(1).strip()
    num = int(re.search(r"^post_number:\s*(\d+)", fm, re.M).group(1))
    title = re.search(r'^title:\s*"(.*)"\s*$', fm, re.M).group(1)
    slug_of[f.name] = ("start-here" if num == 0 else slug, num)
    meta[f.name] = (fm, body, num, title, slug)

def plain(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    return re.sub(r"[*_`]", "", s).strip()

for fname, (fm, body, num, title, slug) in meta.items():
    # drop H1, take the one-sentence line as the deck
    body = re.sub(r"^\s*# .*\n", "", body, count=1)
    deck = ""
    dm = re.search(r"^\*\*In one sentence:\*\*\s*(.+)$", body, re.M)
    if dm:
        deck = plain(dm.group(1)); body = body.replace(dm.group(0), "", 1)
    # next-in-series section -> front matter
    nxt = re.search(r"\n## Next in the series\s*\n+Post (\d+): (.+?)\.\s*$", body)
    next_num = next_title = ""
    if nxt:
        next_num, next_title = nxt.group(1), nxt.group(2); body = body[:nxt.start()] + "\n"
    # links and images
    body = body.replace("](../diagrams/", "](/diagrams/")
    def link(m):
        name = m.group(1)
        if name in slug_of:
            s, n = slug_of[name]
            return "](/start-here/)" if n == 0 else f"](/azure-landing-zone/{s}/)"
        return m.group(0)
    body = re.sub(r"\]\(([^)/#]+\.md)\)", link, body)
    add = []
    s, n = slug_of[fname]
    add.append("layout: post.njk")
    add.append(f'permalink: "/start-here/"' if n == 0 else f'permalink: "/azure-landing-zone/{s}/"')
    add.append(f"order: {n}")
    add.append(f"deck: {json.dumps(deck)}")
    add.append(f"next_num: {json.dumps(next_num)}")
    add.append(f"next_title: {json.dumps(next_title)}")
    if n != 0: add.append("tags: [alz]")
    (out_posts / fname).write_text("---\n" + fm + "\n" + "\n".join(add) + "\n---\n" + body, encoding="utf-8")
print("synced", len(meta), "posts,", len(list(out_diag.glob('*.svg'))), "diagrams")
