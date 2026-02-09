```
$$\      $$\         $$\     $$\  $$$$$$\                     
$$$\    $$$ |        \$$\   $$  |$$  __$$\                    
$$$$\  $$$$ | $$$$$$$\\$$\ $$  / $$ /  \__|$$$$$$\   $$$$$$\  
$$\$$\$$ $$ |$$  _____|\$$$$  /  $$$$\    $$  __$$\ $$  __$$\ 
$$ \$$$  $$ |$$ /       \$$  /   $$  _|   $$$$$$$$ |$$$$$$$$ |
$$ |\$  /$$ |$$ |        $$ |    $$ |     $$   ____|$$   ____|
$$ | \_/ $$ |\$$$$$$$\   $$ |    $$ |     \$$$$$$$\ \$$$$$$$\ 
\__|     \__| \_______|  \__|    \__|      \_______| \_______|
Monitoring concept by Youseff, Fredrik, Elvira and Emil for web   
```


<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

**A flexible, efficient web monitoring system that tracks changes on websites and sends notifications when conditions are met.**

[Features](#features) •
[Getting Started](#getting-started) •
[Documentation](#project-structure) •
[Contributing](#development-guidelines) •
[Team](#team--roles)

</div>

---

## Table of Contents

- [About The Project](#about-the-project)
  - [Primary Use Case: Price Monitoring](#primary-use-case-price-monitoring)
  - [What It Can Monitor](#what-it-can-monitor)
  - [How It Works](#how-it-works)
  - [Built With](#built-with)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running The Project](#running-the-project)
  - [Verification](#verification)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [Development Guidelines](#development-guidelines)
  - [Branch Policy & Git Workflow](#branch-policy--git-workflow)
  - [Commit Message Convention](#commit-message-convention)
  - [Code Standards](#code-standards)
  - [Code Review Guidelines](#code-review-guidelines)
- [Project Timeline](#project-timeline)
- [Roadmap](#roadmap)
- [Team & Roles](#team--roles)
- [License](#license)
- [Contact](#contact)

---

## About The Project

McYfee is a powerful, flexible web monitoring system designed to automatically track changes on websites and send notifications through your preferred channels. The project initially focuses on monitoring product listings and prices, but is architected to support any website.

Unlike many traditional web scrapers that save entire HTML pages, McYfee uses an intelligent extraction approach - it only extracts and stores the specific values you care about. This minimizes storage requirements while maintaining efficiency and speed.

### Primary Use Case: Price Monitoring

McYfee continuously monitors selected products to:
- Monitor price changes
- Alert users via Discord when price has dropped below predefined threshold
- Store historical data for trend analysis

### What It Can Monitor

McYfee is built to be able to track virtually anything visible in HTML or structured data:

- **Prices** - Detect when prices drop below a threshold or change
- **Product Count** - Track when products are added or removed from categories
- **Keywords and Phrases** - Get notified when specific text appears or disappears
- **Images** - Monitor when images are added, replaced, or removed
- **HTML Elements** - Track changes in element counts (meta tags, ads, links, etc.)
- **Text Content** - Watch for updates in terms of service, policies, changelogs
- **Custom Conditions** - Define your own rules and extraction logic

**IMPORTANT:** MVP version supports only price detection.

### How It Works

1. **Define Your Monitor** - Specify the URL, selector (CSS/XPath), and what to extract
2. **Reusable Selectors** - Store selectors centrally and reuse them across multiple monitors
3. **Automatic Fetching** - The system fetches pages on schedule using a managed threading mechanism
4. **Smart Extraction** - Extract only relevant data (price as float, product count, text hash)
5. **Comparison** - Compare extracted values with previously stored values
6. **Notification** - Send alerts via Discord (or other channels) when conditions are met
7. **Minimal Storage** - Only extracted values are stored, not entire HTML pages

**IMPORTANT:** MVP version supports only Discord notifications.

**Example:** Monitor 50 products on Elgiganten using the same price selector - if the selector changes, update it once centrally and all 50 monitors are automatically fixed.

### Built With

- **Language:** Python 3.11+
- **Project Layout:** src-layout architecture
- **Parallel Processing:** ThreadPoolExecutor for parallel fetching
- **HTTP Client:** Requests library
- **HTML Parsing:** CSS Selectors (BeautifulSoup4)
- **Database:** MySQL relational database
- **Notifications:** Discord webhooks (primary), extensible to Telegram, Email, etc.
- **Data Visualization:** Seaborn for statistics and trend analysis
- **Testing:** pytest, pytest-cov
- **Code Quality:** Black, Flake8

---

## Features

### Core Features

- **Parallel Fetching** - Parallel page fetching with ThreadPoolExecutor
- **Smart Data Extraction** - Extract only what matters using CSS selectors
- **Efficient Storage** - Store extracted values, not entire HTML pages
- **Discord Notifications** - Real-time alerts via Discord webhooks
- **Reusable Selectors** - Define selectors once, use across multiple monitors
- **Historical Data & Statistics** - Track trends and analyze changes over time
- **CLI Dashboard** - Menu-driven terminal interface to handle the application
- **Extensible Design** - Modular codebase to ease future development

---

## Getting Started

This section provides step-by-step instructions to get McYfee running on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed on your system:

#### Required Software

1. **Python 3.10 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation:
     ```bash
     python --version
     # or
     python3 --version
     ```
   - Should output: `Python 3.10.x` or higher

2. **pip (Python Package Manager)**
   - Usually comes with Python
   - Verify installation:
     ```bash
     pip --version
     # or
     pip3 --version
     ```

3. **Git**
   - Download from [git-scm.com](https://git-scm.com/)
   - Verify installation:
     ```bash
     git --version
     ```

#### Optional Software

4. **MySQL**
   - MySQL: [Download MySQL](https://dev.mysql.com/downloads/)
     Note: Only optional if you intend to connect to an already hosted McYfee database.

5. **Discord Account** (for notifications)
   - Create a Discord server or use an existing one
   - Set up a webhook (instructions in Configuration section)

### Installation

Follow these steps carefully to set up McYfee on your local machine.

#### Clone the Repository

```bash
# Clone the repository
git clone https://github.com/FredrikKaell/McYfee.git

# Navigate into the project directory
cd McYfee
```

#### Install the Project

**Option 1: Run setup.sh from the scripts folder**

We provide an automated setup script that handles virtual environment creation and dependency installation.

```bash
./scripts/setup.sh
```

The script will:
1. Create a virtual environment that isolates project dependencies from your system Python
2. Install all the required libraries/packages
3. Install the application as a package

Should be working fine on Windows, Linux and MacOS.

**Option 2: Manual Installation**

```bash
# Set up a virtual environment (venv). Not mandatory but recommended.
python3 -m venv .venv

# Activate venv
# Windows:
source .venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install the McYfee project
pip install -e .

# Start the application from anywhere inside project folder
mcyfee
```

### Configuration

#### Setup Database

```bash
# Example on how to create the database on a Linux machine with MySQL
mysql -u root < scripts/setup_db.sql

# Example on how to create a db-user and grant privileges to the db
# The details can then be entered into the .env file so the application can connect
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON mcyfee.* TO 'user'@'localhost';
```

#### Create .env File

There is an `.env.template` file provided in the root folder. Please rename to `.env` and enter your own details. Please set the parameters to connect to the database properly in the `.env` file.

### Running The Project

McYfee provides multiple ways to run the monitoring system depending on your deployment needs.

Just run `mcyfee` command from anywhere inside the project root to start the application with its CLI user interface.


To run the tracker monitoring system continuously, there are several ways to achieve:

#### Method 1: Direct Execution with or without Daemon Mode

Run the tracker directly with daemon mode enabled for continuous monitoring, or False to run it with single execution.

Please set the `DAEMON` parameter in `config.py` to `True`/`False`, you can also set the refresh rate according to your preference.

```bash
python3 -m webtracker.core.tracker
```


**Note:** It's possible to set `DEBUG` to `True` in the `config.py` file to get more information when the tracker is running, which can be helpful for troubleshooting.

**When to use:**
- Development and testing
- Manual one-time checks
- When you want to see immediate output

#### Method 2: Systemd Service (Linux - Recommended for Production)

Set up McYfee as a system service that starts automatically on boot.

**Important:** Please note that in this case the `DAEMON` parameter in the `config.py` should be set to `True`!

**Step 1: Create systemd service file**

```bash
sudo nano /etc/systemd/system/mcyfee.service
```

**Step 2: Add service configuration**

```ini
[Unit]
Description=McYfee Web Monitoring Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/McYfee
Environment="PATH=/path/to/McYfee/.venv/bin"
ExecStart=/path/to/McYfee/.venv/bin/python -m webtracker.core.tracker
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Step 3: Enable and start the service**

```bash
# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable mcyfee.service

# Start the service
sudo systemctl start mcyfee.service

# Check service status
sudo systemctl status mcyfee.service

# View logs
sudo journalctl -u mcyfee.service -f
```

**Step 4: Manage the service**

```bash
# Stop the service
sudo systemctl stop mcyfee.service

# Restart the service
sudo systemctl restart mcyfee.service

# Disable auto-start on boot
sudo systemctl disable mcyfee.service
```

#### Method 3: Scheduled Execution with Crontab (Linux)

Schedule McYfee to run at specific intervals using cron.

**Important:** Please note that in this scenario the `DAEMON` parameter in the `config.py` should be set as `False` for single execution.

```bash
# Edit crontab
crontab -e

# Add entry to run every 5 minutes
*/5 * * * * cd /path/to/McYfee && /path/to/McYfee/.venv/bin/python -m webtracker.core.tracker >> /path/to/McYfee/logs/cron.log 2>&1
```

**Verify cron job:**

```bash
# List current crontab entries
crontab -l

# View cron logs
grep CRON /var/log/syslog
```

#### Method 4: Windows Task Scheduler

Schedule McYfee on Windows systems.

**Important:** Set `DAEMON=False` when using Task Scheduler.

**Step 1: Open Task Scheduler**
- Press `Win + R`, type `taskschd.msc`, press Enter

**Step 2: Create Basic Task**
- Click "Create Basic Task" in the right panel
- Name: "McYfee Monitor"
- Description: "Automated web monitoring"

**Step 3: Set Trigger**
- Choose trigger type (Daily, Weekly, or specific time)
- Example: Daily at 8:00 AM, repeat every 5 minutes for 24 hours

**Step 4: Set Action**
- Action: "Start a program"
- Program/script: `C:\path\to\McYfee\.venv\Scripts\python.exe`
- Arguments: `-m webtracker.core.tracker`
- Start in: `C:\path\to\McYfee`

**Step 5: Finish and Test**
- Check "Open Properties dialog when I click Finish"
- Test by right-clicking the task and selecting "Run"

#### Method 5: Interactive CLI Dashboard

Launch the menu-driven interface for manual control:

```bash
# Launch the interactive CLI
mcyfee
```

This will present a menu interface for:
- Adding/removing scrapers
- Activate/Deactivate scrapers
- List active scrapers
- Generating reports
- Running the tracker service once or as daemon

#### Choosing the Right Method

| Method | Use Case | Daemon Mode | Auto-Start | Best For |
|--------|----------|-------------|------------|----------|
| Direct Execution | Development, testing | Yes/No | No | Quick tests, debugging |
| Systemd Service | Production Linux | Yes | Yes | Servers, always-on monitoring |
| Crontab | Scheduled checks | No | Yes | Periodic monitoring, resource saving |
| Task Scheduler | Windows scheduled | No | Yes | Windows environments |
| CLI Dashboard | Manual operation | No | No | Interactive use, reporting |

### Verification

After starting McYfee using any method, verify it's running:

#### Check logs and performance report:

```bash
# View real-time logs
tail -f logs/mcyfee.log

# View last 50 lines
tail -n 50 logs/mcyfee.log

# Search logs for errors
grep ERROR logs/mcyfee.log

# Check daily performance report
cat reports/performance/*.txt
```

Upon execution and when a predefined set of iterations has happened (defined in `config.py`), a performance report will be generated in `reports/performance/`. Use this to verify that the application is running, and also see the operation times to ensure that everything is running smoothly.

**Expected daily report output:**
```
====================================================================================================
Daily Performance Report
Generated: 2026-02-09 19:37:22.204449.
Horizon: today.
====================================================================================================


Operation record count: 155.
Average operation time: 3.47 s.


Operation types:
 {'Performance_Report_Job', 'Parse', 'Worker_Function', 'Create_Chart'}.


Performance per operation:
Performance_Report_Job
     Count: 65.
     Total time spent: 15.87 s
     Average time: 0.24 s.
     Max time: 5.36 s.
     Min time: 0.08 s.


Parse
     Count: 44.
     Total time spent: 245.37 s
     Average time: 5.58 s.
     Max time: 21.21 s.
     Min time: 0.58 s.


Worker_Function
     Count: 44.
     Total time spent: 273.52 s
     Average time: 6.22 s.
     Max time: 22.29 s.
     Min time: 1.14 s.


Create_Chart
     Count: 2.
     Total time spent: 2.81 s
     Average time: 1.40 s.
     Max time: 2.10 s.
     Min time: 0.71 s.
```

---

## Project Structure

McYfee follows the **src-layout** architecture for clean separation of source code, tests, and configuration.

```
mcyfee/
├── .env
├── .gitignore
├── .flake8
├── pyproject.toml
├── README.md
├── requirements.txt
│    
├── logs/                               # Application logs
│   └── mcyfee.log
│
├── reports/                            # Generated reports
│   └── performance/                    # Performance reports
│
├── src/
│   └── webtracker/                     # Main package
│       ├── __init__.py
│       ├── config.py                   # Configuration settings
│       │
│       ├── core/                       # Core monitoring logic
│       │   ├── __init__.py
│       │   └──tracker.py              # Main tracker orchestrator
│       │
│       ├── scraper/                    # Scraping module
│       │   ├── __init__.py
│       │   ├── parser.py               # HTML parsing
│       │   └── scraper.py              # Scraping logic
│       │
│       ├── database/                   # Database layer
│       │   ├── __init__.py
│       │   └── database.py             # Database operations
│       │
│       ├── notifications/              # Notification channels
│       │   ├── __init__.py
│       │   └──  discord_notifier.py    # Discord notifier
│       │
│       ├── reports/                    # Report generation
│       │   ├── __init__.py
│       │   └── report_generator.py     # Report generator
│       │
│       ├── ui/                         # User interface
│       │   ├── __init__.py
│       │   ├── cli.py                  # CLI commands
│       │   ├── helper.py               # Module for helperfunctions used in ui
│       │   └── selections.py           # Module for handling functions that are accessed through CLI menu
│       │
│       └── utils/                      # Utility modules
│           ├── __init__.py
│           ├── logger.py               # Logging setup
│           ├── inputvalidation.py      # User input validation
│           └── performance.py          # Performance measurement
│
├── tests/                              # Test suite
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_database.py
│   └── test_notifications.py
│
├── scripts/                            # Utility scripts
│   ├── setup_db.sql                    # Database schema
│   └── setup.sh                        # Installation script
│
└── docs/                               # Documentation
    ├── architecture.vsdx
    ├── dbmodel_mcyfee.mwb              # MySQL Workbench EER-diagram
    ├── folder_structure.md
    └── user_guide.md
```

### Key Files Explained

| File | Purpose |
|------|---------|
| `tracker.py` | Core function that works as orchestrator for the tasks to execute |
| `cli.py` | Interactive menu-driven terminal interface |
| `scraper.py` | Scraping logic |
| `parser.py` | Parsing the desired values from the scraped source |
| `database.py` | Database functions and CRUD operations |
| `discord_notifier.py` | Discord webhook integration |
| `report_generator.py` | Statistics generation and visualization (Seaborn) |
| `logger.py` | Centralized logging configuration |
| `input_validation.py` | Validation for all user input to database |
| `performance.py` | Performance measurement |

---

## Testing

McYfee has comprehensive test coverage using pytest.

### Running Tests

#### Run All Tests

```bash
# From project root (with .venv activated)
pytest
```

#### Run Specific Tests

```bash
# Run a specific test file
pytest tests/test_parser.py
```

#### Run Tests with Coverage

```bash
# Generate coverage report
pytest --cov=src/webtracker --cov-report=html

# View coverage report
# Open htmlcov/index.html in your browser
```

---

## CI/CD Pipeline

McYfee uses GitHub Actions for automated Continuous Integration and Continuous Deployment.

### Continuous Integration (CI)

**Triggered on:** Every push and pull request to `dev` and `main` branches.

**Pipeline:** `.github/workflows/ci.yml`

#### CI Status

- Green: All checks passed - ready to merge
- Red: At least one check failed - fix before merging

---

## Development Guidelines

This section defines the rules and standards for developing McYfee. **All team members must follow these guidelines**.

### Branch Policy & Git Workflow

We follow **Git Flow** methodology with strict branch protection rules.

#### Branch Structure

```
main (production)
  ↑
  └── Protected: requires PR + 1 approval + passing CI
  
DEV (development/integration)
  ↑
  └── Protected: requires PR + 1 approval + passing CI
  
staging (pre-dev testing)
  ↑
  └── Making sure everything is working together before merging to DEV
  
feature/*, bugfix/*, hotfix/*, docs/*
  ↑
  └── Working branches (created from staging)
```

#### Branch Descriptions

| Branch | Purpose | Protection | Auto-Deploy |
|--------|---------|------------|-------------|
| **main** | Production-ready code | Strict | Yes (manual approval) |
| **DEV** | Integration and testing | Strict | No |
| **staging** | Pre-DEV feature testing | Moderate | No |
| **feature/** | New features | None | No |
| **bugfix/** | Bug fixes | None | No |
| **hotfix/** | Critical production fixes | None | No |
| **docs/** | Documentation updates | None | No |

#### Branch Types and Naming Convention

| Branch Type | Prefix | Base Branch | Merge Target | Example |
|------------|--------|-------------|--------------|---------|
| **Feature** | `feature/` | `staging` | `staging` | `feature/notifier-discord` |
| **Bugfix** | `bugfix/` | `staging` | `staging` | `bugfix/fix-parser-error` |
| **Hotfix** | `hotfix/` | `main` | `main` + `DEV` | `hotfix/critical-db-crash` |
| **Documentation** | `docs/` | `staging` | `staging` | `docs/update-readme` |

#### Branch Naming Rules

**DO:**
- Use lowercase only: `feature/add-email-notifications`
- Use hyphens to separate words: `feature/price-tracker-module`
- Be descriptive but concise: `feature/discord-webhook-integration`

**DON'T:**
- Use underscores: `feature/add_notifications`
- Use uppercase: `Feature/AddNotifications`
- Be vague: `feature/update`

#### Git Workflow

**1. Starting new work:**
```bash
# Update staging
git checkout staging
git pull origin staging

# Create feature branch from staging
git checkout -b feature/your-feature-name
```

**2. Making changes:**
```bash
# Make changes, then:
git add .
git commit -m "feat(module): description of change"
git push origin feature/your-feature-name
```

**3. Keeping branch updated:**
```bash
# Update staging
git checkout staging
git pull origin staging

# Rebase your feature branch
git checkout feature/your-feature-name
git rebase staging
git push origin feature/your-feature-name --force-with-lease
```

**4. Creating Pull Request:**
- Push branch to GitHub
- Open PR from `feature/your-branch` → `staging`
- Fill in PR template

**5. Promoting to DEV:**
Once tested in staging:
- Create PR from `staging` → `DEV`
- After approval and merge, staging can be reset or continue accumulating features

**6. Promoting to main:**
When ready for production:
- Create PR from `DEV` → `main`
- Requires additional approval and testing
- After merge, creates production release

**7. After merge:**
```bash
git checkout staging
git pull origin staging
git branch -d feature/your-feature-name
```

#### Git Flow Diagram

```
main:      ●────────●─────────────────────────────●──────>
           │        ↑                             ↑
           │     hotfix/                       release
           │   fix-bug                           │
DEV:       ●────────●─────────────────────●──────●──────>
                    │                     ↑
                    │                  promote
                    │                     │
staging:   ●────●───●──●────●────●───●────●──────────────>
                ↑      ↑         ↑        ↑
           feature/ bugfix/ feature/  docs/
```

### Commit Message Convention

We follow **Conventional Commits** specification.

#### Good Examples

- `feat(notifier): add Discord webhook support`
- `fix(scraper): handle timeout errors gracefully`
- `docs(readme): update configuration section`

### Code Standards

#### Python Style Guide (PEP 8)

| Rule | Standard |
|------|----------|
| **Indentation** | 4 spaces (no tabs) |
| **Quotes** | Double quotes (`"`) for strings |
| **Type Hints** | Required for all functions |

### Code Review Guidelines

#### For Reviewers

**Do:**
- Review within 24 hours
- Be constructive and kind
- Test the code if possible
- Approve if acceptable

---

## Project Timeline

The McYfee project was developed over a 3-week sprint cycle:

### Sprint 1: Foundation (Week 1)

**Objectives:** Project setup, planning, and team organization

**Deliverables:**
- Project concept and requirements defined
- Git repository initialized with branch structure
- Trello board set up for task management
- Internal team rules and workflow established
- README and documentation framework created
- Development environment setup guide
- Initial technology stack decisions

**Key Activities:**
- Team roles assigned
- Git workflow and branching strategy defined
- Code standards and review process established
- CI/CD pipeline planning

### Sprint 2: Core Development (Week 2)

**Objectives:** Build a functional, runnable application

**Deliverables:**
- Core scraping functionality
- HTML parsing with CSS selectors
- Database schema and models implemented
- Discord notification integration
- Basic change detection logic
- Configuration management system
- Logging infrastructure
- CLI interface foundation

**Key Activities:**
- Parallel development on core modules
- Regular integration and testing
- Code reviews and pair programming
- Daily standups and sprint planning

### Sprint 3: Testing & Refinement (Week 3)

**Objectives:** Comprehensive testing, bug fixes, and polish

**Deliverables:**
- Full pytest test suite
- Bug fixes and stability improvements
- Performance optimizations
- Documentation completion
- CLI menu enhancements
- Final code quality improvements
- Deployment guides

**Key Activities:**
- Writing comprehensive tests
- Fixing bugs discovered during testing
- Code refactoring for quality
- Final documentation review
- Preparation for demonstration

---

## Roadmap

Future enhancements and features planned for McYfee:

- Extended monitoring capabilities (text, images, element counts)
- Additional notification channels (Email, Telegram, SMS)
- Web dashboard interface
- Advanced statistics and visualization
- Machine learning for price prediction
- Custom alert rules

---

## Team & Roles

### Team Members

| Name | Role | Responsibilities | GitHub |
|------|------|------------------|--------|
| **Fredrik** | Scrum Master & Developer | Project management | [@FredrikKaell](https://github.com/FredrikKaell) |
| **Emil** | Tech Lead & Developer | Technical architecture, design decisions, database design | [@emilioano](https://github.com/emilioano) |
| **Youssef** | Developer | Core scraping logic, parser implementation, threading | [@romdhaniyoussef97-bot](https://github.com/romdhaniyoussef97-bot) |
| **Elvira** | Developer | Central logging functionality, notification system | [@ElviraAjdarpasic](https://github.com/ElviraAjdarpasic) |

### Team Communication

**Primary Channels:**
- **Discord:** Continuous team communication
- **Weekly Meetings:** Longer Monday meetings to schedule weekly activities
- **Daily Standups:** Shorter daily standups to keep work synchronized and quickly resolve issues

**Response Expectations:**
- PR reviews: Within 24 hours
- Messages: Within 4 hours (working hours)
- Urgent issues: Tag entire team

---

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2026 McYfee Team (Youssef, Fredrik, Elvira, Emil)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

## Contact

- **Report Issues:** [GitHub Issues](https://github.com/FredrikKaell/McYfee/issues)
- **Project Repository:** [github.com/FredrikKaell/McYfee](https://github.com/FredrikKaell/McYfee)

---

<div align="center">

**Made with care by the McYfee Team**

[Report Bug](https://github.com/FredrikKaell/McYfee/issues) •
[Request Feature](https://github.com/FredrikKaell/McYfee/issues)

</div>
```
