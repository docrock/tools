#!/usr/bin/env python3
"""Inline the data files into the template and write dist/index.html (one self-contained file)."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
data = ROOT / "data"
safe = lambda s: s.replace("</", "<\\/")

payload = "\n".join([
    "const RATES = " + safe(json.dumps(json.loads((data / "rates.json").read_text()), separators=(",", ":"))) + ";",
    "const LAND = " + (data / "land.json").read_text() + ";",
    "const AIRPORTS_RAW = " + safe(json.dumps((data / "airports.txt").read_text(encoding="utf-8"), ensure_ascii=False)) + ";",
])
html = (ROOT / "src" / "template.html").read_text(encoding="utf-8").replace("/*@DATA@*/", payload, 1)
out = ROOT / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding="utf-8")
print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size / 1024:.0f} KB)")
