"""
Fill in missing authors in assets/data/papers.json by re-fetching from the
OpenReview API. Uses longer delays and exponential backoff on 429.
"""
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "assets" / "data" / "papers.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"


def fetch_authors(forum_id):
    url = f"https://api2.openreview.net/notes?forum={forum_id}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    for note in data.get("notes", []):
        if note.get("id") == forum_id:
            return note.get("content", {}).get("authors", {}).get("value", [])
    return []


def fetch_with_retry(forum_id, max_attempts=5):
    delay = 2.0
    for attempt in range(max_attempts):
        try:
            return fetch_authors(forum_id)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_attempts - 1:
                print(f"    429, sleeping {delay}s (attempt {attempt + 1})")
                time.sleep(delay)
                delay *= 2
            else:
                raise
    return []


def main():
    with open(PATH, "r", encoding="utf-8") as f:
        papers = json.load(f)

    missing = [p for p in papers if not p.get("authors")]
    print(f"Missing: {len(missing)} of {len(papers)}")

    for i, p in enumerate(missing, 1):
        forum_id = p["forum_url"].rsplit("id=", 1)[-1]
        try:
            authors = fetch_with_retry(forum_id)
            p["authors"] = authors
            print(f"[{i}/{len(missing)}] #{p['number']} {len(authors)} authors -- {p['title'][:60]}")
        except Exception as e:
            print(f"[{i}/{len(missing)}] FAILED #{p['number']}: {e}")
        time.sleep(1.0)

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)

    still = [p for p in papers if not p.get("authors")]
    print(f"\nStill missing: {len(still)}")
    for p in still:
        print(f"  #{p['number']} {p['forum_url']}")


if __name__ == "__main__":
    main()
