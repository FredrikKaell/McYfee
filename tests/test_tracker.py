import pytest
from unittest.mock import patch, MagicMock
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
@patch('webtracker.notifications.discord_notifier.DiscordNotifier')   # Do not send real notification
@patch('webtracker.scraper.parser.parse')               # Don't fetch real webpage
@patch('webtracker.database.database')                  # Do not not create db record
def test_full_flow_price_below_threshold(mock_db, mock_parse, mock_discord, mock_perf):
    # Test flow. Parse > Extract price > Compare > Trigger
    mock_parse.return_value = "34995 kr"
    mock_db.update_monitor_last_check.return_value = True
    mock_db.create_snapshot.return_value = 1
    mock_db.update_monitor_values.return_value = True
    mock_db.set_monitor_status.return_value = 1

    mock_discord_instance = MagicMock()
    mock_discord.return_value = mock_discord_instance

    worker_function(MOCK_MONITOR_ROW)

    # Notification should trigger. Under 40000
    mock_discord.assert_called_once()
    mock_discord_instance.send.assert_called_once()

@patch('webtracker.utils.performance.db.save_performance_record')
@patch('webtracker.notifications.discord_notifier.DiscordNotifier')
@patch('webtracker.scraper.parser.parse')
@patch('webtracker.database.database')
def test_full_flow_price_above_threshold(mock_db, mock_parse, mock_discord, mock_perf):
    # Simulate return value above threshold
    mock_parse.return_value = "44995 kr"
    mock_db.update_monitor_last_check.return_value = True
    mock_db.create_snapshot.return_value = 1
    mock_db.update_monitor_values.return_value = True

    worker_function(MOCK_MONITOR_ROW)

    # Notification should not send, over 40000
    mock_discord.assert_not_called()

