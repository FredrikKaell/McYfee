import time
import datetime
from datetime import timedelta

import database as db

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)




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
    print(colors.OKGREEN)
    print('Scraper function triggered!!')
    print(colors.ENDC)


    # Performing task
    time.sleep(5)

    row_id = row['id']
    update_last_check = db.update_monitor_last_check(row_id)
    print(f'{update_last_check} row for last_check updated in db')

    print('Worker klar')
    return row['id']

def tracker():
    while True:

        date_time = datetime.datetime.now()

        rows = db.fetch_monitors_poller('all_due') or []
        for row in rows: 



            def messageout():
                print('Messageout function tiggered!!')


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

                notification_type = row.get('notification_type')
                notification_config = row.get('notification_config')

                check_interval = row.get('check_interval')
                last_checked = row.get('last_check_at')

                created_at = row.get('created_at')

                if last_checked:
                    next_check = last_checked + timedelta(minutes=check_interval)
                else:
                    next_check = created_at + timedelta(minutes=check_interval)

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
                

                if next_check <= date_time:
                    print(colors.OKCYAN)
                    print('Trigger hit!!')
                    print(colors.ENDC)

                    executor.submit(worker_function, row)



                print('='*60)
                print('\n')
        print(colors.OKBLUE)
        print(f'Chillar i {POLL_RATE} sekunder.')
        print(colors.ENDC)
        time.sleep(POLL_RATE)




if __name__ == '__main__':
    tracker()