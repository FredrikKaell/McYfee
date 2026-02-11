import time
import datetime
from datetime import timedelta
import re
import json

from webtracker.database import database as db
from webtracker.scraper import parser
from webtracker.notifications import discord_notifier
from webtracker.utils.performance import timed_operation, performance_report_job
from webtracker.config import colors, DEBUG_MODE, POLL_RATE, REFRESH_PERFORMANCE_REPORT, DAEMON

from webtracker.utils.logger import AppLogger

log = AppLogger().get_logger()

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)


def worker_function(row):
    # Worker is performing tasks when tracker finds trigger.
    date_time = datetime.datetime.now()
    was_triggered = False
    fetched_price = None

    row_id = row["id"]
    row_name = row["name"]
    url = row["url"]
    css_selector = row["css_selector"]
    xpath = row["xpath"]
    threshold = row["threshold_value"]
    interval = row["check_interval"]

    print(f"Worker started: {row_name}")

    current_db_value = row[
        "last_extracted_value"
    ]  # Fecthing current value which will later turn into previous
    if current_db_value and isinstance(current_db_value, str):
        try:
            current_db_value = json.loads(current_db_value)
        except json.JSONDecodeError:
            current_db_value = None

    try:
        # Performing scraping task
        selector = {
            "css_selector": css_selector,
            "xpath": xpath,
        }
        fetched_value = timed_operation(parser.parse, url, selector)
        log.info(
            f'Fetched value for "{row_name}" with id {row_id}: {fetched_value}. Threshold: {threshold}'
        )

        fetched_value_regex = re.search(r"(\d[\d\s.,]*\d|\d+)", fetched_value)

        if fetched_value_regex:
            num_str = fetched_value_regex.group(0)
            num_str = re.sub(r"[\s.,]+", "", num_str)
            fetched_price = float(num_str)

            if fetched_price <= threshold:
                log.info(
                    "Monitored value is under the threshold value, trigger Notifier!!"
                )
                was_triggered = True
                previous_price = None
                change_percent = None

                if current_db_value and current_db_value.get("current"):
                    previous_price = current_db_value["current"]
                    change_percent = (
                        (fetched_price - previous_price) / previous_price * 100
                    )

                timed_operation(
                    send_notification,
                    notification_type=row.get("notification_type"),
                    notification_config=row.get("notification_config"),
                    monitor_name=row_name,
                    threshold=threshold,
                    current_price=fetched_price,
                    previous_price=previous_price,
                    change_percent=change_percent,
                    url=url,
                    interval=interval,
                    monitor_id=row_id,
                    timestamp=date_time,
                )

                deactivate_monitor = db.set_monitor_status(row_id, 0)
                print(
                    f"{deactivate_monitor} monitor has been deactivated with id {row_id}."
                )

        else:
            log.error(f"Could not extract value from {fetched_value}")
            return None

        extract = {
            "monitor_name": row_name,
            "threshold": float(threshold),
            "current": float(fetched_price),
            "url": url,
            "interval": interval,
            "checked_time": date_time.isoformat(),
        }

        db.update_monitor_values(
            monitor_id=row_id,
            last_extracted_value=extract,
            previous_extracted_value=current_db_value,
            last_changed_at=date_time if was_triggered else None,
        )

        create_snap = db.create_snapshot(row_id, extract, was_triggered)
        print(f"Snapshot record with id {create_snap} was created.")

        return row["id"]

    except Exception as err:
        log.error(f"Error: {err}")

    finally:
        update_last_check = db.update_monitor_last_check(row_id)
        print(f"{update_last_check} row for last_check for {row_name} updated in db")
        print(f"Worker done: {row_name}")


def tracker(daemon: bool = True):
    # Tracker is polling the db for tasks to execute
    counter = 0
    while True:
        date_time = datetime.datetime.now()

        rows = db.fetch_monitors_poller("all_due") or []
        for row in rows:

            if (row.get("is_active")) == 1:
                monitor_id = row.get("id")
                monitor_name = row.get("name")
                monitor_url = row.get("url")
                monitor_type = row.get("type")
                monitor_threshold = row.get("threshold_value")

                selector_id = row.get("selector_id")
                selector_name = row.get("selector_name")
                selector_description = row.get("description")
                selector_css = row.get("css_selector")
                xpath = row.get("xpath")

                notification_type = row.get("notification_type")
                notification_config = row.get("notification_config")

                check_interval = row.get("check_interval")
                last_checked = row.get("last_check_at")

                created_at = row.get("created_at")

                if last_checked:
                    next_check = last_checked + timedelta(minutes=check_interval)
                else:
                    next_check = created_at + timedelta(minutes=check_interval)

                if DEBUG_MODE:
                    print("=" * 60)
                    print(f"Monitor id: {monitor_id}")
                    print(f"Monitor name: {monitor_name}")
                    print(f"Monitor url: {monitor_url}")
                    print(f"Monitor threshold: {monitor_threshold}")
                    print()
                    print(f"Selector name: {selector_name}")
                    print(f"Selector description: {selector_description}")
                    print(f"Selector css: {selector_css[:150]}...")
                    print(f"Notification via: {notification_type}")
                    print()
                    print(f"Check interval: {check_interval} minutes")
                    print(f"Created at: {created_at}")
                    print(f"Last check at: {last_checked}")
                    print(f"Next check at: {next_check}")
                    print(f"Now time: {date_time}")
                    print("=" * 60)
                    print("\n")

                if next_check <= date_time:
                    print(colors.OKCYAN)
                    print("Detected trigger to execute worker!!")
                    print(colors.ENDC)

                    executor.submit(lambda r=row: timed_operation(worker_function, r))

        if daemon is True:
            print(colors.OKBLUE)
            print("-" * 60)
            print(
                f"Running as daemon. Refreshing in {POLL_RATE} seconds. Iteration counter: {counter}"
            )
            print("-" * 60)
            print(colors.ENDC)
            if counter % REFRESH_PERFORMANCE_REPORT == 0:
                timed_operation(performance_report_job)
                print(
                    f"*** Performance report refreshed (refreshing every {REFRESH_PERFORMANCE_REPORT} iteration.) ***"
                )
            counter += 1
            time.sleep(POLL_RATE)
        else:
            timed_operation(performance_report_job)
            break


def send_notification(
    notification_type: str,
    notification_config: str,
    monitor_name: str,
    threshold: float,
    current_price: float,
    url: str,
    interval: int,
    monitor_id: int,
    timestamp: datetime.datetime,
    previous_price: float = None,
    change_percent: float = None,
):
    # Notification gets sent to predetermined destination.
    try:
        config = json.loads(notification_config)

        message_parts = [
            f"**{timestamp.strftime('%Y-%m-%d %H:%M:%S')}**",
            f'The monitored price for **"{monitor_name}"** has dropped below threshold!',
            f"Threshold: __{threshold}__ SEK",
        ]

        if previous_price is not None:
            message_parts.append(f"Previous: __{previous_price}__ SEK")
            message_parts.append(f"Current: __{current_price}__ SEK")
            if change_percent is not None:
                message_parts.append(f"Change: __{change_percent:.1f}%__")
        else:
            message_parts.append(f"Current price: __{current_price}__ SEK")

        message_parts.extend(
            [
                f"URL: {url}",
                f"Check interval: {interval} minutes",
                f"_Monitor {monitor_id} will be deactivated._",
            ]
        )

        message = "\n".join(message_parts)

        # Send based on type
        if notification_type == "discord":
            webhook_url = config.get("webhook")

            if not webhook_url:
                print(f"No webhook URL in Discord config")
                return False

            print(f"Sending Discord notification")
            notifier = discord_notifier.DiscordNotifier(webhook_url)
            notifier.send(message)
            print(f"Discord notification sent!")
            return True

        # Telegram functionality not implemented in mvp version
        elif notification_type == "telegram":
            bot_token = config.get("bot_token")
            chat_id = config.get("chat_id")

            if not bot_token or not chat_id:
                print(f"Missing Telegram credentials")
                return False

            print(f"Telegram notification not implemented yet.")
            return False

        # Email function not implemented in mvp version
        elif notification_type == "email":
            to_email = config.get("to")
            from_email = config.get("from")

            if not to_email or not from_email:
                print(f"Missing email config")
                return False

            print(f"Email notification not implemented yet.")
            return False

        else:
            print(f"Unknown notification type: {notification_type}")
            return False

    except json.JSONDecodeError as err:
        print(f"Invalid JSON config: {err}")
        return False

    except Exception as err:
        print(f"Error sending notification: {err}")
        return False


if __name__ == "__main__":
    try:
        tracker(daemon=DAEMON)

    except KeyboardInterrupt:
        print(f"Tracker was stopped with keyboard interrupt.")

    except Exception as err:
        log.error(f"Tracker stopped with following: {err}")
