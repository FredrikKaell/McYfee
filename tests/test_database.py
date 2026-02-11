import pytest
from webtracker.database import database as db

# Tests for database module, uses real database connection.


def test_fetch_monitors_returns_list():
    #Test that fetch_monitors returns a list.
    result = db.fetch_monitors()
    
    assert isinstance(result, list)


def test_fetch_all_monitors_returns_list():
    #Test that fetch_all_monitors returns a list.
    result = db.fetch_all_monitors()
    
    assert isinstance(result, list)


def test_fetch_performance_records_returns_list():
    #Test that fetch_performance_records returns a list.
    result = db.fetch_performance_records()
    
    assert isinstance(result, list)