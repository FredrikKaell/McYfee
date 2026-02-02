"""
scraper.py
Fetch raw HTML from a URL.
"""

from __future__ import annotations

import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)


def fetch_html(url: str, timeout: int = 10) -> Optional[str]:
    """Return HTML as text, or None if request fails."""
    headers = {
        "User-Agent": "McYfee/0.1 (student project)",
        "Accept-Language": "sv-SE,sv;q=0.9,en;q=0.8",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        logger.info("Fetched %s (%d chars)", url, len(resp.text))
        return resp.text
    except requests.RequestException as exc:
        logger.warning("Failed to fetch %s: %s", url, exc)
        return None
