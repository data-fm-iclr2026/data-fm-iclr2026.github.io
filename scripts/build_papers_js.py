"""
Convert assets/data/papers.json to assets/data/papers.js as a JS data file
so the page works over file:// (direct preview) as well as http(s)://.

Produces:
    window.PAPERS = [...];
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "data" / "papers.json"
DST = ROOT / "assets" / "data" / "papers.js"

with open(SRC, "r", encoding="utf-8") as f:
    papers = json.load(f)

with open(DST, "w", encoding="utf-8") as f:
    f.write("window.PAPERS = ")
    json.dump(papers, f, indent=2, ensure_ascii=False)
    f.write(";\n")

print(f"Wrote {DST} with {len(papers)} papers")
