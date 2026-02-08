import mysql.connector
import time
from datetime import datetime
from typing import List, Dict, Optional

DB_CONFIG = {
    'host': '192.168.8.116',
    'port': '3306',
    'user': 'emil_local',
    'password': '0popcorn0',
    'database': 'mcyfee',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}


POLL_INTERVAL = 10


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def get_due_monitors(conn) -> List[Dict]:
    """
    Fetch all monitors that are due to be checked.
    Uses the logic from v_due_monitors view.
    """
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            m.id,
            m.name,
            m.url,
            m.check_interval,
            m.last_check_at,
            TIMESTAMPDIFF(SECOND, m.last_check_at, NOW()) AS seconds_since_check,
            s.name AS selector_name,
            s.css_selector,
            s.xpath
        FROM monitors m
        JOIN selectors s ON m.selector_id = s.id
        WHERE m.is_active = TRUE
          AND (
              m.last_check_at IS NULL 
              OR TIMESTAMPDIFF(SECOND, m.last_check_at, NOW()) >= m.check_interval
          )
    """
    
    cursor.execute(query)
    monitors = cursor.fetchall()
    cursor.close()
    
    return monitors


def update_last_check(conn, monitor_id: int):
    """Update the last_check_at timestamp for a monitor."""
    cursor = conn.cursor()
    
    query = """
        UPDATE monitors 
        SET last_check_at = NOW() 
        WHERE id = %s
    """
    
    cursor.execute(query, (monitor_id,))
    conn.commit()
    cursor.close()


def process_monitor(conn, monitor: Dict):

    print(f"\n{'='*60}")
    print(f"Processing Monitor: {monitor['name']}")
    print(f"{'='*60}")
    print(f"ID:              {monitor['id']}")
    print(f"URL:             {monitor['url']}")
    print(f"Selector:        {monitor['selector_name']}")
    print(f"CSS Selector:    {monitor['css_selector'] or 'N/A'}")
    print(f"XPath Selector:  {monitor['xpath'] or 'N/A'}")
    print(f"Check Interval:  {monitor['check_interval']}minutes")
    
    if monitor['last_check_at']:
        print(f"Last Check:      {monitor['last_check_at']} ({monitor['seconds_since_check']}s ago)")
    else:
        print(f"Last Check:      Never")
    
    print(f"Status: DUE FOR CHECK")
    print(f"{'='*60}")
    
    # Update the last_check_at timestamp
    update_last_check(conn, monitor['id'])
    print(f"✅ Updated last_check_at for monitor {monitor['id']}")


def main():
    """Main tracker loop."""
    print("McYfee Tracker POC Starting...")
    print(f"Polling database every {POLL_INTERVAL} seconds")
    print(f"Database: {DB_CONFIG['database']} @ {DB_CONFIG['host']}")
    print("-" * 60)
    
    iteration = 0
    
    try:
        while True:
            iteration += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n[{timestamp}] Poll #{iteration}")
            
            # Connect to database
            try:
                conn = get_db_connection()
                
                # Get monitors that are due
                due_monitors = get_due_monitors(conn)
                
                if due_monitors:
                    print(f"Found {len(due_monitors)} monitor(s) due for checking:")
                    
                    for monitor in due_monitors:
                        process_monitor(conn, monitor)
                        
                else:
                    print("No monitors due for checking")
                
                conn.close()
                
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
            
            # Wait before next poll
            time.sleep(POLL_INTERVAL)
            
    except KeyboardInterrupt:
        print("Tracker stopped by user input")


if __name__ == "__main__":
    main()