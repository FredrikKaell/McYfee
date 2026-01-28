# McYfee Web - Monitoring concept by by Youssef, Fredrik, Elvira and Emil for Web

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

McYfee Web is an automated monitoring tool designed to track changes in product listings and prices within specific categories on Elgiganten.se, one of Sweden’s largest electronics retailers.

Our tool regularly scrapes selected product categories, detects changes in product count and pricing, and notifies users via Discord. All statistics and historical data are stored in a database (TBD) and can be accessed through a command-line interface (CLI), allowing users to analyze trends and receive timely alerts.

### Features

* **Automated Web Scraping**: Continuously monitors selected categories for new products, removals, and price changes.
* **Change Detection**: Tracks both the number of products and price fluctuations within each category.
* **Discord Notifications**: Instantly notifies users of changes via Discord webhooks.
* **Historical Data & Statistics**: Stores all changes in a database for later analysis and reporting.
* **CLI Dashboard**: User-friendly menu-driven interface in the terminal for viewing statistics and reports.
* **Extensible Design**: Modular codebase for easy addition of new stores or notification channels.

### Built With

* Python (version TBD)
* Requests
* CSS Selector (for HTML parsing)
* Seaborn (for data visualization)
* Database: xxx (to be decided)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started


### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Clone the repo
   ```sh
   git clone https://github.com/FredrikKaell/McYfee.git
   ```
2. Create a virtual enviroment
   ```sh
   python -m venv .venv
   ```
3. Activate the virtual enviroment
   ```sh
   .venv/Scripts/activate
   ```
4. Install packages
   ```sh
   pip install -r requirements.txt
   ```
5. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```
6. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage
* Run the application from your terminal (e.g., in VS Code).
* The application will present a menu for user input and navigation.
* Notifications about product and price changes will be sent to your configured Discord channel.

More detailed usage instructions and examples will be provided as the project develops.

## Web Scraping Details

* Frequency: Refers to how often the application checks Elgiganten.se for updates. (To be decided; could be every few minutes, hourly, etc.)
* Anti-bot Measures: Many websites have protections against automated scraping (like CAPTCHAs or rate limiting). Our approach to handling these (e.g., using headers, delays, or proxies) will be determined as needed during development.
* Categories: Users will be able to select which product categories to monitor. (Details to be finalized.)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Directory structure
```
mcyfee/
├── src/webscraper/
│   ├── __init__.py         
│   ├── config.py         
│   ├── database.py    
│   ├── logger.py    
│   ├── main.py    
│   ├── notifier.py    
│   ├── parser.py    
│   ├── report.py    
│   ├── scraper.py    
│   ├── threading.py    
│   └── tracker.py
├── tests/             
├── logs/           
├── .gitignore              
└── README.md               

```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

- [ ] Basic product and price change detection
- [ ] Discord notifications via webhook
- [ ] CLI statistics and reporting with menu-driven interface
- [ ] Additional templates and usage examples
- [ ] Multi-language support (e.g., Chinese, Spanish)
- [ ] Support for more stores and notification channels

## Contributing

This project is developed by a team of four:

* Fredrik – Scrum Master & Developer
* Emil – Tech Lead & Developer
* Youssef – Developer
* Elvira – Developer

Contributions from the core team are welcome. External contribution guidelines will be added later.

## Acknowledgments

Inspiration from open-source monitoring and scraping tools.
Thanks to the Python and open-source community.
