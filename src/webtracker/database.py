import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime

from config import DB_CONFIG




''' Create connection '''

def db_connection():
    # Connect to DB
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as err:
        print(f"Error connecting to database: {err}")
        raise



''' DB Read actions '''

def fetch_monitors(active: bool = True):
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = 'SELECT * FROM monitors WHERE is_active = %s'

        cursor.execute(query, (1 if active else 0,))
        result = cursor.fetchall()
        return result

    except Exception as err:
        print(f'Error: {err}')   
        return None 

    finally:
        cursor.close()
        conn.close()  


def fetch_monitor_by_id(id: int = None):
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = 'SELECT * FROM monitors WHERE id = %s'

        cursor.execute(query, (id, ))
        result = cursor.fetchall()
        return result

    except Exception as err:
        print(f'Error: {err}')   
        return None 

    finally:
        cursor.close()
        conn.close()  


def fetch_all_monitors():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = 'SELECT * FROM monitors'

        cursor.execute(query)
        result = cursor.fetchall()
        return result

    except Exception as err:
        print(f'Error: {err}') 
        return None    

    finally:
        cursor.close()
        conn.close()      


def fetch_selectors(url_pattern: str = None):
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if url_pattern:
            query = 'SELECT * FROM selectors WHERE url_pattern LIKE %s'
            cursor.execute(query, (f'%{url_pattern}%',))
        else:
            query = 'SELECT * FROM selectors'
            cursor.execute(query)
        
        result = cursor.fetchall()
        return result

    except Exception as err:
        print(f'Error: {err}')  
        return None  

    finally:
        cursor.close()
        conn.close()  


def fetch_notifications(active: bool = True):
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = 'SELECT * FROM notifications WHERE active = %s'

        cursor.execute(query, (1 if active else 0,))
        result = cursor.fetchall()
        return result

    except Exception as err:
        print(f'Error: {err}') 
        return None   

    finally:
        cursor.close()
        conn.close()  


def fetch_monitors_poller(type: str = 'all_active'):
    # Fetching all monitors in active state that has connected selector and notification
    # With option 'all_due' we're only showing monitors that are ready to be triggered!
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try: 
        query = '''
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
                s.name as selector_name,
                s.css_selector,
                s.description,
                m.notification_id,
                n.type as notification_type,
                n.config as notification_config
                FROM monitors AS m
                INNER JOIN selectors as s on s.id = m.selector_id
                INNER JOIN notifications as n on n.id = m.notification_id
                WHERE is_active = 1
        '''

        if type == 'all_due':  
            query += '''
                    AND (
                    m.last_check_at IS NULL 
                    OR TIMESTAMPDIFF(MINUTE , m.last_check_at, NOW()) >= m.check_interval
                    )
            '''
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    except Exception as err:
        print(f'Error: {err}')   
        return None 

    finally:
        cursor.close()
        conn.close()



''' Insert, update, delete actions '''

def create_selector(name: str, css_selector: str, xpath: str, url_pattern: str, description: str):
    # Create a new selector
    conn = db_connection()
    cursor = conn.cursor()
    
    try: 
        query = '''
            INSERT INTO 
            selectors (name, css_selector, xpath, url_pattern, description) 
            VALUES (%s, %s, %s, %s, %s)
        '''
        cursor.execute(query, (name, css_selector, xpath, url_pattern, description))
        conn.commit()
        return cursor.lastrowid

    except Exception as err:
        print(f'Error: {err}') 
        conn.rollback()  
        return None 

    finally:
        cursor.close()
        conn.close()

def create_monitor(name: str, url: str, selector_id: int, monitor_type: str, threshold: int, check_interval: int, is_active: int):
    # Create a new monitor
    conn = db_connection()
    cursor = conn.cursor()
    
    try: 
        query = '''
            INSERT INTO 
            monitors (name, url, selector_id, type, threshold_value, check_interval, is_active) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(query, (name, url, selector_id, monitor_type, threshold, check_interval, is_active))
        conn.commit()
        return cursor.rowcount

    except Exception as err:
        print(f'Error: {err}') 
        conn.rollback()  
        return None 

    finally:
        cursor.close()
        conn.close()


def create_notification(type: str, config: json, active: str = 1):
    # Create a new notification
    conn = db_connection()
    cursor = conn.cursor()
    
    try: 
        query = '''
            INSERT INTO 
            monitors (type, config, active) 
            VALUES (%s, %s, %s)
        '''
        cursor.execute(query, (type, config, active))
        conn.commit()
        return cursor.lastrowid

    except Exception as err:
        print(f'Error: {err}') 
        conn.rollback()  
        return None 

    finally:
        cursor.close()
        conn.close()


def set_monitor_status(id: int= None, status: int = 0):
    # Upate status on monitor
    conn = db_connection()
    cursor = conn.cursor()

    try:
        query = 'UPDATE monitors SET is_active = %s where id = %s'
        cursor.execute(query, (status, id))
        conn.commit()
        return cursor.rowcount

    except Exception as err:
        print(f'Error: {err}') 
        conn.rollback()  
        return None 

    finally:
        cursor.close()
        conn.close()


def set_notification_status(id: int= None, status: int = 0):
    # Upate status on notification
    conn = db_connection()
    cursor = conn.cursor()

    try:
        query = 'UPDATE notifications SET is_active = %s where id = %s'
        cursor.execute(query, (status, id))
        conn.commit()
        return cursor.rowcount

    except Exception as err:
        print(f'Error: {err}')   
        conn.rollback()
        return None 

    finally:
        cursor.close()
        conn.close()


def delete_monitor(id: int = None):
    # Delete a monitor
    conn = db_connection()
    cursor = conn.cursor()

    try:
        query = 'DELETE FROM monitors where id = %s'
        cursor.execute(query, (id,))
        conn.commit()
        return cursor.rowcount

    except Exception as err:
        print(f'Error: {err}')  
        conn.rollback()  
        return None

    finally:
        cursor.close()
        conn.close()



''' DB audit field updates '''

def update_monitor_last_check(id: int = None, timestamp: datetime = None):
    # Upate monitor set last checked
    conn = db_connection()
    cursor = conn.cursor()

    try:
        if timestamp is None:
            timestamp = datetime.now()
        query = 'UPDATE monitors SET last_check_at = %s where id = %s'
        cursor.execute(query, (timestamp, id))
        conn.commit()
        return cursor.rowcount

    except Exception as err:
        print(f'Error: {err}')   
        conn.rollback() 
        return None

    finally:
        cursor.close()
        conn.close()



if __name__ == '__main__':
    #Tester
    db_connection()

    print('fetch_all_monitors():')
    for row in fetch_monitors():
        print(f'{row}\n')
    
    print('fetch_monitors():')
    for row in fetch_monitors():
        print(f'{row}\n')

    print('fetch_monitor_by_id(id=2):')
    for row in fetch_monitor_by_id(id=2):
        print(f'{row}\n')

    print('fetch_selectors():')
    for row in fetch_selectors():
        print(f'{row}\n')

    print('fetch_notifications():')
    for row in fetch_notifications():
        print(f'{row}\n')

    print('fetch_selectors(url_pattern=elgiganten):')
    for row in fetch_selectors(url_pattern='elgiganten'):
        print(f'{row}\n')