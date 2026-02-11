import pytest
from unittest.mock import patch
from webtracker.core.tracker import worker_function


# Simulating DB record
MOCK_MONITOR_ROW = {
    'id': 1,
    'name': 'Test Monitor',
    'url': 'https://www.aftonbladet.se',
    'css_selector': '.price',
    'xpath':None,
    'threshold_value': 40000,
    'check_interval': 60,
    'last_extracted_value': None,
    'notification_type': 'discord',
    'notification_config': '{"webhook": "https://discord.com/api/webhooks/12345"}'
}



@patch('webtracker.utils.performance.db.save_performance_record') # Don't save real performance record
@patch('webtracker.core.tracker.send_notification')   # Do not send real notification
@patch('webtracker.scraper.parser.parse')               # Don't fetch real webpage
@patch('webtracker.core.tracker.db')                  # Do not not create db record
def test_full_flow_price_below_threshold(mock_db, mock_parse, mock_notification, mock_perf):
    # Test flow. Parse > Extract price > Compare > Trigger
    mock_parse.return_value = "34995 kr"
    mock_db.update_monitor_last_check.return_value = True
    mock_db.create_snapshot.return_value = 1
    mock_db.update_monitor_values.return_value = True

    worker_function(MOCK_MONITOR_ROW)

    # Notification should trigger. Under 40000
    mock_notification.assert_called_once()

@patch('webtracker.utils.performance.db.save_performance_record')
@patch('webtracker.core.tracker.send_notification')
@patch('webtracker.scraper.parser.parse')
@patch('webtracker.core.tracker.db')
def test_full_flow_price_above_threshold(mock_db, mock_parse, mock_notification, mock_perf):
    """
    Test full flow:
    parse → extract price → compare → no notification
    """
    # Simulera att sidan returnerar ett pris över threshold
    mock_parse.return_value = "44995 kr"
    mock_db.update_monitor_last_check.return_value = True
    mock_db.create_snapshot.return_value = 1
    mock_db.update_monitor_values.return_value = True

    worker_function(MOCK_MONITOR_ROW)

    # Notification should not send, over 40000
    mock_notification.assert_not_called()

