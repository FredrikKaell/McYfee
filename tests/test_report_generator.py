import pytest
import json
from pathlib import Path
from unittest.mock import patch
from webtracker.database import database as db
from webtracker.reports.report_generator import create_chart

# Tests for report generator module.

MOCK_SNAPSHOTS = [
    {
        'monitor_id': 1,
        'id': 15,
        'extracted_value': '{"url": "https://www.example.com", "current": 34995.0, "interval": 60, "threshold": 32000.0, "checked_time": "2026-02-11T11:14:30.038832", "monitor_name": "Stationär dator på Alina.se"}',
        'was_triggered': 0,
        'created_at': '2026-02-11 11:14:36',
        'name': 'Stationär dator på Alina.se'
    },
    {
        'monitor_id': 1,
        'id': 16,
        'extracted_value': '{"url": "https://www.example.com", "current": 34995.0, "interval": 60, "threshold": 32000.0, "checked_time": "2026-02-11T11:14:30.038832", "monitor_name": "Stationär dator på Alina.se"}',
        'was_triggered': 0,
        'created_at': '2026-02-11 11:14:36',
        'name': 'Stationär dator på Alina.se'
    },
    {
        'monitor_id': 1,
        'id': 17,
        'extracted_value': '{"url": "https://www.example.com", "current": 34995.0, "interval": 60, "threshold": 32000.0, "checked_time": "2026-02-11T11:14:30.038832", "monitor_name": "Stationär dator på Alina.se"}',
        'was_triggered': 0,
        'created_at': '2026-02-11 11:14:36',
        'name': 'Stationär dator på Alina.se'
    },
]

@patch('webtracker.reports.report_generator.db.fetch_snapshots')
def test_create_chart_with_data(mock_fetch, tmp_path):
    # Test tha create_chart generates a file
    mock_fetch.return_value = MOCK_SNAPSHOTS
    
    with patch('webtracker.reports.report_generator.OUTPUT_DIR', tmp_path):
        result = create_chart(days=7)
    
    assert result is not None
    assert Path(result).exists()


@patch('webtracker.reports.report_generator.db.fetch_snapshots')
def test_create_chart_no_data(mock_fetch):
    # Testing that create_chart returns None when no data
    mock_fetch.return_value = []
    
    result = create_chart(days=7)
    
    assert result is None