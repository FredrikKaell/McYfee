import time
import mysql.connector
import datetime
from datetime import timedelta

DB_CONFIG = {
    'host': '136.0.141.240',
    'port': '37628',
    'user': 'mcyfee_db_user',
    'password': '',
    'database': 'mcyfee',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}



POLL_RATE = 15


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



def tracker():
    while True:

        date_time = datetime.datetime.now()

        DBConn = mysql.connector.connect(**DB_CONFIG);
        cursor = DBConn.cursor(dictionary=True)
        cursor.execute('''
            SELECT
            m.id,
            m.name,
            m.url,
            m.selector_id,
            m.check_interval,
            m.type,
            m.threshold_value,
            m.is_active,
            m.last_check_at,
            m.created_at,
            s.name as Selector_namn,
            s.css_selector,
            s.description,
            m.notification_id,
            n.type as Notification_type,
            n.config as Notification_config
            FROM monitors AS m
            LEFT JOIN selectors as s on s.id = m.selector_id
            INNER JOIN notifications as n on n.id = m.notification_id;
            ''')

        row = cursor.fetchall()   

        for row in row:

            def scraper_function():
                print(colors.OKGREEN)
                print('Scraper function triggered!!')
                print(colors.ENDC)

            def messageout():
                print('Messageout function tiggered!!')


            if (row.get('is_active')) == 1:
                monitor_id = row.get('id')
                monitor_name = row.get('name')
                monitor_url = row.get('url')
                monitor_type = row.get('type')
                monitor_threshold = row.get('threshold_value')

                selector_id = row.get('selector_id')
                selector_name = row.get('Selector_namn')
                selector_description = row.get('description')
                selector_css = row.get('css_selector')

                notification_type = row.get('Notification_type')
                notification_config = row.get('Notification_config')

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

                    scraper_function()

                    cursor.execute(f'UPDATE monitors SET last_check_at = %s where id = %s', (date_time, monitor_id))
                    DBConn.commit()

                print('='*60)
                print('\n')
        print(colors.OKBLUE)
        print(f'Chillar i {POLL_RATE} sekunder.')
        print(colors.ENDC)
        time.sleep(POLL_RATE)




if __name__ == '__main__':
    tracker()