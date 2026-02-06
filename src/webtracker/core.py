"""
Module for defining core function for scraping
"""

from typing import Optional

# PLACEHOLDER FUNCTIONS SHOULD BE REPLACED WITH REAL FUNCTIONS
def add_endpoint(**kwargs):
    pass

def add_monitor(
    name : str,
    url : str,
    threshold : int,
    interval : int,
    xpath : Optional[str] = None,
    css_selector : Optional[str] = None
    ):
    """
    Function for adding endpoint to database.
    """
    
    add_endpoint(
        name = name,
        url = url,
        threshold = threshold,
        interval = interval,
        xpath = xpath,
        css_selector = css_selector,
        is_active = 1
    )

    return f"Monitor {name} has been added to the database."