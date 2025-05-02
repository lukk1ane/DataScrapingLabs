# Selenium Automation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download ChromeDriver for your OS:
   [https://googlechromelabs.github.io/chrome-for-testing/#stable](https://googlechromelabs.github.io/chrome-for-testing/#stable)
   Place it in `./drivers/`.

## Task 1: Form Automation

- Opens [demoqa.com](https://demoqa.com/automation-practice-form)
- Fills out the form and submits it.

## Task 2: Book Scraper

- Opens [books.toscrape.com](https://books.toscrape.com/)
- Extracts title, price, availability, and rating.
- Saves to `all_books.csv`, and filters 5-star books into `5_star_books.csv`.
- Supports headless and custom window size.
