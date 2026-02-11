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


@patch('webtracker.database.database.update_monitor_last_check')
@patch('webtracker.database.database.set_monitor_status')
@patch('webtracker.database.database.create_snapshot')
@patch('webtracker.database.database.update_monitor_values')
@patch('webtracker.utils.performance.db.save_performance_record')
@patch('webtracker.notifications.discord_notifier.DiscordNotifier')
@patch('webtracker.scraper.parser.parse')
def test_full_flow_price_below_threshold(
    mock_parse,
    mock_discord,
    mock_perf,
    mock_update_values,
    mock_create_snap,
    mock_set_status,
    mock_last_check
):
    # Test flow. Parse > Extract price > Compare > Trigger
    mock_parse.return_value = "34995 kr"
    mock_update_values.return_value = True
    mock_create_snap.return_value = 1
    mock_set_status.return_value = 1
    mock_last_check.return_value = 1

    worker_function(MOCK_MONITOR_ROW)

    # Notification should trigger. Under 40000
    mock_discord.assert_called_once()
    mock_discord.return_value.send.assert_called_once()


@patch('webtracker.database.database.update_monitor_last_check')
@patch('webtracker.database.database.create_snapshot')
@patch('webtracker.database.database.update_monitor_values')
@patch('webtracker.utils.performance.db.save_performance_record')
@patch('webtracker.notifications.discord_notifier.DiscordNotifier')
@patch('webtracker.scraper.parser.parse')
def test_full_flow_price_above_threshold(
    mock_parse,
    mock_discord,
    mock_perf,
    mock_update_values,
    mock_create_snap,
    mock_last_check
):
    # Simulate return value above threshold
    mock_parse.return_value = "44995 kr"
    mock_update_values.return_value = True
    mock_create_snap.return_value = 1
    mock_last_check.return_value = 1

    worker_function(MOCK_MONITOR_ROW)

    # Notification should not send, over 40000
    mock_discord.assert_not_called()