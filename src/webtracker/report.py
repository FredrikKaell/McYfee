import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator
import seaborn as sns
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import json

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import database as db
from performance import timed_operation, performance_report_job

OUTPUT_DIR = Path('data/reports')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style='darkgrid')


def create_chart(monitor_id: int = None, days: int = 30):
    # Creating charts reflecting prices over time
    # Fetch snapshots
    snapshots = db.fetch_snapshots(monitor_id)
    if not snapshots:
        print('No data')
        return
    
    # Fetch data
    data = []
    for snap in snapshots:
        extracted = json.loads(snap['extracted_value']) if isinstance(snap['extracted_value'], str) else snap['extracted_value']
        if extracted.get('current'):
            data.append({
                'datetime': pd.to_datetime(snap['created_at']),
                'price': extracted['current'],
                'monitor': snap['name']
            })
    
    df = pd.DataFrame(data)
    
    # Filter by days
    df['date'] = df['datetime'].dt.date
    cutoff = datetime.now() - timedelta(days=days)
    df = df[df['datetime'] >= cutoff]
    
    if df.empty:
        print(f'No data for last {days} days')
        return

    # Create date-only column for grouping
    df['date_only'] = df['datetime'].dt.date
    
    # Group by date and monitor, calculate daily average
    df_daily = df.groupby(['date_only', 'monitor'])['price'].mean().reset_index()
    
    # Convert date_only to datetime for plotting
    df_daily['date'] = pd.to_datetime(df_daily['date_only'])
    
    if days <= 7:
        figsize = (14, 6)
        interval = 1  # Show every day
    elif days <= 30:
        figsize = (18, 6)
        interval = 2  # Show every 2nd day
    elif days <= 90:
        figsize = (24, 6)
        interval = 5  # Show every 5th day
    else:  # 365 days
        figsize = (30, 6)
        interval = 15  # Show every 15th day

    # Plot
    plt.figure(figsize=(figsize))

    date_range_start = datetime.now() - timedelta(days=days)
    date_range_end = datetime.now()


    
    if monitor_id:
        # Single monitor
        plt.plot(df_daily['date'], df_daily['price'], marker='o', linewidth=2)
        title = f"{df['monitor'].iloc[0]} - Last {days} Days"
        filename = f"{df['monitor'].iloc[0].replace(' ', '_')}_{days}days.png"
    else:
        # All monitors
        for monitor in df['monitor'].unique():
            monitor_df = df[df['monitor'] == monitor]
            plt.plot(monitor_df['date'], monitor_df['price'], marker='o', linewidth=2, label=monitor)
        plt.legend()
        title = f"All Monitors - Last {days} Days"
        filename = f"all_monitors_{days}days.png"

    # Set x-axis limits to show all days
    plt.xlim(date_range_start, date_range_end)
    
    # Format x-axis
    ax = plt.gca()
    ax.xaxis.set_major_locator(DayLocator(interval=interval))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    
    plt.xlabel('Date', fontsize=11)
    plt.ylabel('Price (SEK)', fontsize=11)
    plt.title(title, fontweight='bold', fontsize=13)
    plt.grid(alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save
    filepath = OUTPUT_DIR / filename
    plt.savefig(filepath, dpi=300)
    plt.close()
    
    print(f'Saved: {filepath}')


if __name__ == '__main__':
    timed_operation(create_chart,days=3)
    timed_operation(create_chart,monitor_id=20,days=3)