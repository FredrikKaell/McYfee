"""
parser.py
Takes a URL + selector dict, fetches HTML via scraper, and extracts a value.

Expected selector format:
selector = {
    "css_selector": "...",
    "xpath": None
}
"""

from __future__ import annotations

import logging
from typing import Optional, Dict, Any

from bs4 import BeautifulSoup

from .scraper import fetch_html  # important: relative import for package structure

logger = logging.getLogger(__name__)


def parse_with_css(html: str, css_selector: str) -> Optional[str]:
    """Extract text from the first element matching the CSS selector."""
    soup = BeautifulSoup(html, "lxml")
    el = soup.select_one(css_selector)
    if el is None:
        return None
    return el.get_text(strip=True)


def parse_with_xpath(html: str, xpath: str) -> Optional[str]:
    """
    Placeholder for XPath support.
    (You can implement later with lxml.html / etree)
    """
    raise NotImplementedError("XPath parsing not implemented yet.")


def parse(url: str, selector: Dict[str, Any]) -> Optional[str]:
    """
    Main parser function. 
    Fetches HTML from URL, then extracts value using xpath or css_selector.
    Returns extracted value as raw text, or None if not found / fetch failed.
    """
    html = fetch_html(url)
    if not html:
        logger.warning("No HTML returned for url=%s", url)
        return None

    xpath = selector.get("xpath") or selector.get("XPath")
    css = selector.get("css_selector") or selector.get("CSS_Selector")

    try:
        if xpath:
            return parse_with_xpath(html, xpath)
        if css:
            return parse_with_css(html, css)

        logger.warning("No selector provided (xpath/css missing). url=%s", url)
        return None

    except Exception as exc:
        logger.warning("Parse failed for url=%s: %s", url, exc)
        return None


def _quick_test() -> None:
    """
    Quick local test:
      cd src
      py -m webtracker.parser
    """
    logging.basicConfig(level=logging.INFO)

    url = "https://www.elgiganten.se/product/datorer-kontor/datorer/laptop/hp-laptop-14-ep0807no-i3-n3058128-14-barbar-dator/911981"
    selector = {
        "css_selector": "span.-mt-\\[6px\\].font-headline.text-\\[3\\.5rem\\].leading-\\[3\\.5rem\\].inc-vat",
        "xpath": None,
    }

    value = parse(url, selector)
    print("Parsed value:", value)


if __name__ == "__main__":
    _quick_test()
