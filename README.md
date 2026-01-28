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

This project's core concept is to monitor changes for a specific category at the Swedish store [Elgiganten](https://www.elgiganten.se).
The changes we are monitoring are number of products as well as changes in price any product within that category. The statistics for a specific category can be displayed using a CLI. 

The data is stored in a xxxx database. 


### Built With

The project is built with Python and following libraries
* Requests
* CSS-selector
* Seaborn




<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started


### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/FredrikKaell/McYfee.git
   ```
3. Create a virtual enviroment
   ```sh
   python -m venv .venv
   ```
4. Activate the virtual enviroment
   ```sh
   .venv/Scripts/activate
   ```
3. Install packages
   ```sh
   pip install -r requirements.txt
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

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