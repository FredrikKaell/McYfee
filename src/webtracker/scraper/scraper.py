"""
scraper.py
Fetches raw HTML from a URL and returns it as a string.
No parsing, no file saving, no database logic.
"""

from __future__ import annotations

import logging
import time
from typing import Optional

import requests

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10
DEFAULT_RETRIES = 2


def fetch_html(url: str, timeout: int = DEFAULT_TIMEOUT, retries: int = DEFAULT_RETRIES) -> Optional[str]:
    """
    Fetch HTML from the given URL.
    Returns the HTML string, or None if it fails.
    """
    headers = {
        "User-Agent": "McYfee/0.1 (student project)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "sv-SE,sv;q=0.9,en;q=0.8",
        "Connection": "close",
    }

    last_exc: Exception | None = None

    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            html = resp.text

            logger.info("Fetched %s (status=%s, chars=%d)", url, resp.status_code, len(html))
            return html

        except requests.RequestException as exc:
            last_exc = exc
            logger.warning("Fetch failed (attempt %d/%d) for %s: %s", attempt + 1, retries + 1, url, exc)

            # small backoff before retrying
            if attempt < retries:
                time.sleep(0.5 * (attempt + 1))

    logger.error("Giving up fetching %s. Last error: %s", url, last_exc)
    return None


def _quick_test() -> None:
    """
    Simple local test. Run this file directly:
      python -m webtracker.scraper
    or (depending on your setup):
      python src/webtracker/scraper.py
    """
    logging.basicConfig(level=logging.INFO)

    url = "https://www.elgiganten.se/product/datorer-kontor/datorer/laptop/hp-laptop-14-ep0807no-i3-n3058128-14-barbar-dator/911981"
    html = fetch_html(url)

    if html is None:
        print("Scraper test failed")
        raise SystemExit(1)

    print("Scraper test OK")
    print("Snippet:", html[:200].replace("\n", " "))


if __name__ == "__main__":
    _quick_test()
