#!/usr/bin/env python3
"""Inline the data files and logotype into the template and write index.html (one self-contained file).

Also refreshes the logotype in the tools home page (../index.html) so both footers match.
"""
import json, pathlib, re, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
data = ROOT / "data"
safe = lambda s: s.replace("</", "<\\/")

# The logo ships as a CSS mask (colored by the theme), inlined as a data URI so the page still makes zero requests.
svg = (ROOT / "images" / "SVG" / "doc-rock-logotype-white.svg").read_text(encoding="utf-8")
svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
svg = re.sub(r"\s+", " ", svg).replace("> <", "><").strip()
logo_uri = "data:image/svg+xml," + urllib.parse.quote(svg, safe=" =:/,.-")

payload = "\n".join([
    "const RATES = " + safe(json.dumps(json.loads((data / "rates.json").read_text()), separators=(",", ":"))) + ";",
    "const LAND = " + (data / "land.json").read_text() + ";",
    "const AIRPORTS_RAW = " + safe(json.dumps((data / "airports.txt").read_text(encoding="utf-8"), ensure_ascii=False)) + ";",
])
html = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
html = html.replace("/*@DATA@*/", payload, 1).replace("@LOGOTYPE_URI@", logo_uri)
out = ROOT / "index.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out.relative_to(ROOT.parent)} ({out.stat().st_size / 1024:.0f} KB)")

home = ROOT.parent / "index.html"
page = home.read_text(encoding="utf-8")
page = re.sub(r'--logotype: url\("[^"]*"\)', lambda m: f'--logotype: url("{logo_uri}")', page)
home.write_text(page, encoding="utf-8")
print(f"refreshed logotype in {home.name}")
