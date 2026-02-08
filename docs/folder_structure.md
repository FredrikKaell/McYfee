mcyfee/
├── .env
├── .gitignore
├── .flake8
├── pyproject.toml
├── README.md
├── requirements.txt│
│    
├── logs/
│   └── loggfiler
│
├── reports/
│   └── rapportfiler
│
├── src/
│   └── webtracker/        # webtracker
│       ├── __init__.py
│       ├──  config.py          
│       │
│       ├── core/            # Core
│       │   ├── __init__.py
│       │   ├── tracker.py       # Main tracker
│       │   └── worker.py        # Worker function
│       │
│       ├── scraper/         # Scraper module
│       │   ├── __init__.py
│       │   ├── parser.
│       │   └── scraper.py   
│       │
│       ├── database/        # DB actions
│       │   ├── __init__.py
│       │   └── database.py       
│       │
│       ├── notifications/   # Notifications
│       │   ├── __init__.py
│       │   ├── discord.py      # Discord notifier
│       │   ├── telegram.py     # Telegram notifier
│       │   └── email.py        # Email notifier
│       │
│       ├── reports/        # Report gen.
│       │   ├── __init__.py
│       │   └── generator.py
│       │
│       ├── ui/              # UI module
│       │   ├── __init__.py
│       │   ├── cli.py          # CLI commands
│       │   └──        # Color definitions
│       │
│       └── utils/           # Utilities
│           ├── __init__.py
│           ├── logger.py       # Logging setup
│           ├── inputvalidation.py # Validation for all user input to db
│           └── performance.py      # Performance measure
│
├── tests/                   # Tests
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_database.py
│   └── test_notifications.py
│
├── scripts/                 # Utility scripts
│   ├── setup_db.sql        # Database schema
│   └── deploy.sh           # Deployment script
│
├── docs/                    # Documentation
│   ├── architecture.md
│   └── user_guide.md
