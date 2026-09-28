# -*- coding: utf-8 -*-
"""校验 README.md 与 docs/*.md 中的相对链接/图片是否可达。"""
import os, re, urllib.parse

ROOT = r"E:/study_book/AIGC-Interview-Book"
FILES = ["README.md", "CONTRIBUTING.md"] + ["docs/" + f for f in os.listdir(os.path.join(ROOT, "docs")) if f.endswith(".md")]

pat = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
bad, ok = [], 0
for rel in FILES:
    p = os.path.join(ROOT, rel.replace("/", os.sep))
    if not os.path.exists(p):
        bad.append((rel, "(文件本身缺失)")); continue
    txt = open(p, encoding="utf-8").read()
    base = os.path.dirname(p)
    for m in pat.finditer(txt):
        url = m.group(1)
        if url.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = url.split("#")[0]
        if not target:
            continue
        target = urllib.parse.unquote(target)
        full = os.path.normpath(os.path.join(base, target.replace("/", os.sep)))
        if os.path.exists(full):
            ok += 1
        else:
            bad.append((rel, url))

print("可解析的相对链接/图片: %d" % ok)
if bad:
    print("!! 失效链接 (%d):" % len(bad))
    for f, u in bad:
        print("   %-34s -> %s" % (f, u))
else:
    print("全部相对链接可达")
