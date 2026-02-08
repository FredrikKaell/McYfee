from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import os





# === PATH CONFIGURATION ===
# Using __file__ makes paths work regardless of where the script is run from
PACKAGE_DIR = Path(__file__).parent  # Directory where this file lives
PROJECT_ROOT = PACKAGE_DIR.parent.parent  # McYfee root
DATA_DIR = PROJECT_ROOT / 'data'  # Data directory in project root

# .env finder
env_path = find_dotenv(usecwd=True)
if not env_path:
    #Fallback:
    env_path = PROJECT_ROOT / ".env"
    

load_dotenv(dotenv_path=env_path, override=False)

DB_CONFIG = {
'host': os.getenv('DB_HOST'),
'port': int(os.getenv('DB_PORT')),
'user': os.getenv('DB_USER'),
'password': os.getenv('DB_PASS'),
'database': os.getenv('DB_NAME')
}

# Tracker settings
# Debug mode prints lots of more information which can help troubleshooting
DEBUG_MODE = False

# Poll rate determines the refresh rate to poll records from databas to check for monitors to trigger
POLL_RATE = 60

# This determines how many iterations before the performance report gets refreshed
REFRESH_PERFORMANCE_REPORT = 10

# === TEXT COLORS ===
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