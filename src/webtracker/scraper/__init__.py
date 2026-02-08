"""
webtracker.scraper package

Exports the public API for scraping + parsing.
"""

from .scraper import fetch_html
from .parser import parse, parse_with_css

__all__ = ["fetch_html", "parse", "parse_with_css"]
