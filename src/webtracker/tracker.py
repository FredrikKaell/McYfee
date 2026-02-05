import time
import datetime
from datetime import timedelta
import re
from venv import create

# Emil only
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import database as db
from parser import parse
from notifier import DiscordNotifier

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)


DEBUG_MODE = False

POLL_RATE = 10


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def worker_function(row):
    date_time = datetime.datetime.now()
    was_triggered = False
    fetched_price = None 

    row_id = row['id']
    row_name = row['name']
    url = row['url']
    css_selector = row['css_selector']
    xpath = row['xpath']
    threshold = row['threshold_value']
    interval = row['check_interval']

    print(f'Worker started: {row_name}')

    # Performing task
    selector = {
        "css_selector": css_selector,
        "xpath": xpath,
    }

    try:
        fetched_value = parse(url, selector)
        print(f'Fetched price for {row_name}: {fetched_value}')

        fetched_value_regex = re.search(r'(\d[\d\s.,]*\d|\d+)', fetched_value)

        if fetched_value_regex:  
            num_str = fetched_value_regex.group(0)
            num_str = re.sub(r'[\s.,]+', '', num_str)
            fetched_price = float(num_str)
            
            if fetched_price <= threshold:
                print('Monitored value is under the threshold value!!')
                print('Trigger Notifier!!')
                was_triggered = True

                WEBHOOK_URL = "https://discord.com/api/webhooks/1466515978497036380/F8JwMrt75R1uCE5iXbsx74PW9lVYFu6pNlh7AAtdR7JEYGQKERdbAC4T3DmTRRe8fs6g"
    
                message = f'''
**{date_time}**.
The monitored price for **"{row_name}"** has went under the threshold price __{threshold}__.
Current price is: __{fetched_price}__.
Url is: {url}.
Check interval is every {interval} minutes. 
_Monitor with id {row_id} will deactivate after this alert_.
                '''

                print(message)
                notifier = DiscordNotifier(WEBHOOK_URL)
                notifier.send(message)

                deactivate_monitor = db.set_monitor_status(row_id,0)
                print(f'{deactivate_monitor} monitor has been deactivated with id {row_id}.')

        else:
            print(f'Could not extract value from {fetched_value}')
            return None

        # Creating a snapshot record 
        to_snapshots = {
        'monitor_name':row_name,
        'threshold':float(threshold),
        'current':float(fetched_price),
        'url':url,
        'interval':interval,
        'checked_time':date_time.isoformat()
        }
        create_snap = db.create_snapshot(row_id,to_snapshots,was_triggered)
        print(f'Snapshot record with id {create_snap} was created.')

        print(f'Worker done: {row_name}')
        return row['id']

    except Exception as err:
        print(f'Error: {err}')

    finally:
        update_last_check = db.update_monitor_last_check(row_id)
        print(f'{update_last_check} row for last_check for {row_name} updated in db')



def tracker(daemon: bool = True):
    while True:
        date_time = datetime.datetime.now()

        rows = db.fetch_monitors_poller('all_due') or []
        for row in rows: 

            if (row.get('is_active')) == 1:
                monitor_id = row.get('id')
                monitor_name = row.get('name')
                monitor_url = row.get('url')
                monitor_type = row.get('type')
                monitor_threshold = row.get('threshold_value')

                selector_id = row.get('selector_id')
                selector_name = row.get('selector_name')
                selector_description = row.get('description')
                selector_css = row.get('css_selector')
                xpath = row.get('xpath')

                notification_type = row.get('notification_type')
                notification_config = row.get('notification_config')

                check_interval = row.get('check_interval')
                last_checked = row.get('last_check_at')

                created_at = row.get('created_at')

                if last_checked:
                    next_check = last_checked + timedelta(minutes=check_interval)
                else:
                    next_check = created_at + timedelta(minutes=check_interval)

                if DEBUG_MODE:
                    print('='*60)
                    print(f'Monitor id: {monitor_id}')
                    print(f'Monitor name: {monitor_name}')
                    print(f'Monitor url: {monitor_url}')
                    print(f'Monitor threshold: {monitor_threshold}')
                    print()
                    print(f'Selector name: {selector_name}')
                    print(f'Selector description: {selector_description}')
                    print(f'Selector css: {selector_css[:150]}...')
                    print(f'Notification via: {notification_type}')
                    print()
                    print(f'Check interval: {check_interval} minutes')
                    print(f'Created at: {created_at}')
                    print(f'Last check at: {last_checked}')
                    print(f'Next check at: {next_check}')
                    print(f'Now time: {date_time}')
                    print('='*60)
                    print('\n')

                
                if next_check <= date_time:
                    print(colors.OKCYAN)
                    print('Trigger hit!!')
                    print(colors.ENDC)

                    executor.submit(worker_function, row)

        if daemon is True:        
            print(colors.OKBLUE)
            print(f'Chillar i {POLL_RATE} sekunder.')
            print(colors.ENDC)
            time.sleep(POLL_RATE)
        else:
            break




if __name__ == '__main__':
    tracker(daemon=True)