# El País Scraper

## Overview

This project scrapes the latest Opinion articles from **El País a Spanish News Article Website** using Selenium and BeautifulSoup.

The scraper performs the following tasks:

- Opens the El País Opinion section
- Accepts the cookie banner
- Scrapes the first 5 opinion articles
- Extracts:
  - Spanish title
  - Article content
  - Cover image
- Downloads article images locally
- Translates article titles from Spanish to English
- Saves all scraped data into a JSON file
- Counts repeated words appearing more than twice in translated titles
- Supports BrowserStack cross-browser execution

---

## Project Structure

```
ElPaisScraper/
│
├── browserstacker.py
├── main.py
├── config.py
├── requirements.txt
├── .env
├── README.md
│
├── scraper/
│   ├── scraper.py
│   └── translator.py
│
├── utils/
│   ├── logger.py
│   └── helper.py
│
├── exceptions/
│   └── scraper_exceptions.py
│
├── images/
│
└── output/
    └── articles.json
```

---

## Requirements

- Python 3.12+
- Google Chrome
- ChromeDriver (installed automatically)
- Active Internet connection

---

## Installation

Clone the repository

```bash
git clone <https://github.com/Leebro10/Browserstack-test.git>
```

Move into the project

```bash
cd ElPaisScraper
```

Create a virtual environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
```

---

## Running the Scraper

Execute

```bash
python main.py
```

The scraper will

- Open El País
- Accept cookies
- Scrape 5 opinion articles
- Translate titles
- Download article images
- Save articles to JSON
- Print repeated words

---

## BrowserStack Cross-Browser Testing

Execute

```bash
python browserstacker.py
```

The project runs across five parallel browser configurations:

- Chrome (Windows 11)
- Firefox (Windows 11)
- Safari (macOS Sonoma)
- Samsung Galaxy S24
- iPhone 15 Safari

---

## Output

### Images

Downloaded into

```
images/
```

### JSON

Saved as

```
output/articles.json
```

Example

```json
{
    "title": "...",
    "translated_title": "...",
    "url": "...",
    "image_url": "...",
    "content": "..."
}
```

---

## Libraries Used

- Selenium
- BeautifulSoup4
- Requests
- webdriver-manager
- deep-translator
- python-dotenv
- BrowserStack SDK
- Colorama

---

## Notes

- Cookie banners are handled automatically.
- Basic retry logic is implemented for temporary verification pages.
- BrowserStack execution verifies scraper compatibility across desktop and mobile browsers.
- Dynamic page rendering is handled using Selenium before parsing with BeautifulSoup.

---

## Assignment Features

* Scrapes the first 5 Opinion articles

* Extracts article title

* Extracts article body

* Downloads article image

* Translates titles to English

* Saves results into JSON

* Counts repeated translated words

* Local execution

* BrowserStack execution on 5 parallel browsers
