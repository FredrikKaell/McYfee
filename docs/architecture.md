Proposal for project structure:

mcyfee/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # CI/CD pipeline
│       └── release.yml               # Release automation
│
├── docs/
│   └── architecture.md               # Denna fil
│
├── src/
│   └── mcyfee/
│       ├── __init__.py
│       ├── __main__.py               # Entry point: python -m mcyfee
│       │
│       ├── core/                     # Kärnlogik
│       │   ├── __init__.py
│       │   ├── fetcher.py            # Async HTTP-hämtning
│       │   ├── extractor.py          # Data-extraktion från HTML
│       │   ├── comparator.py         # Jämför nuvarande vs tidigare värden
│       │   └── scheduler.py          # Schemaläggning av bevakningar
│       │
│       ├── models/                   # Data models (SQLAlchemy/Pydantic)
│       │   ├── __init__.py
│       │   ├── monitor.py            # Monitor-konfiguration
│       │   ├── selector.py           # Återanvändbar selector
│       │   ├── snapshot.py           # Sparad data från tidigare körning
│       │   └── notification.py       # Notifikationskonfiguration
│       │
│       ├── extractors/               # Pluggbara extraktorer
│       │   ├── __init__.py
│       │   ├── base.py               # AbstractExtractor
│       │   ├── price.py              # PriceExtractor
│       │   ├── text.py               # TextExtractor
│       │   ├── image.py              # ImageExtractor
│       │   ├── element_count.py      # ElementCountExtractor
│       │   └── attribute.py          # AttributeExtractor
│       │
│       ├── conditions/               # Pluggbara villkor
│       │   ├── __init__.py
│       │   ├── base.py               # AbstractCondition
│       │   ├── numeric.py            # <, >, ==, != för numeriska värden
│       │   ├── text.py               # contains, matches, changed
│       │   └── list.py               # added, removed, count_changed
│       │
│       ├── notifiers/                # Pluggbara notifierare
│       │   ├── __init__.py
│       │   ├── base.py               # AbstractNotifier
│       │   ├── telegram.py           # TelegramNotifier
│       │   ├── discord.py            # DiscordNotifier
│       │   ├── email.py              # EmailNotifier
│       │   └── webhook.py            # WebhookNotifier
│       │
│       ├── database/                 # Databas-hantering
│       │   ├── __init__.py
│       │   ├── dbactions.py
│       │   └── connection.py         # Connection pooling
│       ├── cli/                      # Command-line interface
│       │   ├── __init__.py
│       │   ├── main.py               # Click/Typer CLI root
│       │   ├── monitor.py            # Monitor-hanteringskommandon
│       │   ├── selector.py           # Selector-hantering
│       │   └── run.py                # Kör bevakningar
│       │
│       ├── config/                   # Konfigurationshantering
│       │   ├── __init__.py
│       │   ├── settings.py           # Pydantic Settings
│       │   └── logging.py            # Logging-konfiguration
│       │
│       └── utils/                    # Hjälpfunktioner
│           ├── __init__.py
│           ├── retry.py              # Retry-logik
│           ├── cache.py              # Caching-hjälp
│           └── validators.py         # Custom validators
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # Pytest fixtures
│   ├── unit/                         # Unit tests
│   │   ├── test_extractors.py
│   │   ├── test_conditions.py
│   │   └── test_notifiers.py
│   ├── integration/                  # Integration tests
│   │   ├── test_monitor_flow.py
│   │   └── test_database.py
│   └── e2e/                          # End-to-end tests
│       └── test_full_workflow.py
├── .env.example                      # Exempel på miljövariabler
├── .gitignore
├── .pre-commit-config.yaml           # Pre-commit hooks
├── pyproject.toml                    # Projekt-metadata & dependencies
├── requirements.txt                  # (Genereras från pyproject.toml)
├── requirements-dev.txt              # Dev-dependencies
├── README.md
├── LICENSE
└── CHANGELOG.md





DB-design:

┌─────────────────┐
│   Selector      │
├─────────────────┤
│ id (PK)         │
│ name            │
│ css_selector    │
│ xpath_selector  │
│ site_pattern    │  Selector 
│ description     │
│ created_at      │
│ updated_at      │
└─────────────────┘
        │
        │ 1:N
        ▼
┌─────────────────┐         ┌──────────────────┐
│   Monitor       │────1:N──│  Snapshot        │
├─────────────────┤         ├──────────────────┤
│ id (PK)         │         │ id (PK)          │
│ name            │         │ monitor_id (FK)  │
│ url             │         │ extracted_value  │  # JSON
│ selector_id(FK) │         │ value_hash       │
│ extractor_type  │         │ created_at       │
│ condition_type  │         └──────────────────┘
│ condition_value │
│ check_interval  │
│ is_active       │
│ last_check      │
│ created_at      │
│ updated_at      │
└─────────────────┘
        │
        │ N:M
        ▼
┌─────────────────┐
│  Notification   │
├─────────────────┤
│ id (PK)         │
│ monitor_id (FK) │
│ type            │  # telegram, discord, email, webhook
│ config          │  # JSON: {chat_id, token, ...}
│ is_active       │
│ created_at      │
└─────────────────┘
