"""
Module for helperfunctions used in ui
"""
import tldextract
from typing import Optional
from webtracker.database import database as db

def check_existing_selectors(url):
    """
    Function for checking if there exists a selector for chosen URL.
    """
    domain = tldextract.extract(url)
    selectors = db.fetch_selectors(domain.domain)
    if not selectors:
        return False
    return selectors

def get_selector_by_id(selectors : list[dict], id : int):
    for selector in selectors:
        if selector['id'] == id:
            return selector

