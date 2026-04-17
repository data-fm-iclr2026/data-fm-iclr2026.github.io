"""
Build assets/data/papers.json from the submission status CSV + OpenReview API.

- Reads "ICLR 2026 Workshop DATA-FM Submission Status.csv"
- Filters to Accept + Accept (Oral)
- Sorts by submission number (ascending)
- For each accepted paper, fetches authors from the public OpenReview API
- Writes assets/data/papers.json
"""
import csv
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "ICLR 2026 Workshop DATA-FM Submission Status.csv"
OUT_PATH = ROOT / "assets" / "data" / "papers.json"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"


def fetch_authors(forum_id):
    url = f"https://api2.openreview.net/notes?forum={forum_id}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    for note in data.get("notes", []):
        if note.get("id") == forum_id:
            content = note.get("content", {})
            authors = content.get("authors", {}).get("value", [])
            return authors
    return []


def main():
    rows = []
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for r in reader:
            decision = (r.get("decision") or "").strip()
            if decision in ("Accept", "Accept (Oral)"):
                rows.append({
                    "number": int(r["number"]),
                    "title": r["title"].strip(),
                    "forum_url": r["forum"].strip(),
                    "decision": decision,
                })
    rows.sort(key=lambda x: x["number"])
    print(f"Accepted papers: {len(rows)}")

    out = []
    for i, p in enumerate(rows, 1):
        forum_id = p["forum_url"].rsplit("id=", 1)[-1]
        try:
            authors = fetch_authors(forum_id)
        except Exception as e:
            print(f"[{i}/{len(rows)}] FAILED #{p['number']} ({forum_id}): {e}")
            authors = []
        out.append({
            "number": p["number"],
            "title": p["title"],
            "authors": authors,
            "forum_url": p["forum_url"],
            "decision": p["decision"],
        })
        print(f"[{i}/{len(rows)}] #{p['number']} {len(authors)} authors -- {p['title'][:70]}")
        time.sleep(0.25)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {OUT_PATH}")


if __name__ == "__main__":
    main()
