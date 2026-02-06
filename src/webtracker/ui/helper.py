"""
Module for helperfunctions used in ui
"""
import tldextract
from webtracker.database import fetch_selectors
from typing import Optional

def check_existing_selectors(url):
    """
    Function for checking if there exists a selector for chosen URL.
    """
    print(url)
    domain = tldextract.extract(url)
    print(domain)
    selectors = fetch_selectors(domain.domain)
    if not selectors:
        return False
    return selectors

def get_selector_by_id(selectors : list[dict], id : int):
    for selector in selectors:
        if selector['id'] == id:
            return selector

