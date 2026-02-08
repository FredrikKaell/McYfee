mcyfee/
├── README.md
├── pyproject.toml
├── requirements.txt
├── setup.py
├── .gitignore
│
├── config/
│   ├── config.py          # Settings (poll_rate, workers, etc)
│   └── .env.example         # Template för secrets
│    
├── logs/
│
├── reports/
│
├── src/
│   └── webtracker/        # webtracker eller mcyfee
│       ├── __init__.py
│       │
│       ├── core/            # Core/Orchestrator
│       │   ├── __init__.py
│       │   ├── tracker.py       # Main tracker/orchestrator
│       │   └── worker.py        # Worker function
│       │
│       ├── scraper/         # Scraper module
│       │   ├── __init__.py
│       │   ├── parser.py        # HTML parsing logic
│       │   └── extractors.py   # Price/text/image extractors
│       │
│       ├── database/        # Database module
│       │   ├── __init__.py
│       │   └── database.py       
│       │
│       ├── notifications/   # Notifications module
│       │   ├── __init__.py
│       │   ├── discord.py      # Discord notifier
│       │   ├── telegram.py     # Telegram notifier
│       │   └── email.py        # Email notifier
│       │
│       ├── ui/              # UI module (CLI för nu)
│       │   ├── __init__.py
│       │   ├── cli.py          # CLI commands
│       │   └── colors.py       # Color definitions
│       │
│       └── utils/           # Utilities
│           ├── __init__.py
│           ├── logger.py       # Logging setup
│           └── helpers.py      # Helper functions
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
│
└── 
