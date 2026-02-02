from pathlib import Path
import logging

from webtracker.scraper import fetch_html

logging.basicConfig(level=logging.INFO)

URL = URL = "https://www.elgiganten.se/datorer-kontor/datorer"
OUT = Path("data/raw/elgiganten_page.html")


html = fetch_html(URL)

if not html:
    print("Failed to fetch HTML")
    raise SystemExit(1)

print("OK - fetched HTML")
print("Snippet:", html[:200].replace("\n", " "))

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print(f"Saved to {OUT}")
