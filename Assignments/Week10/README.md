# Product Catalog Scraper

A modular web scraping project that collects product information from e-commerce websites. Currently supports Amazon, with extensibility for other e-commerce platforms.

## Features

- Modular design with separate components for scraping, data management, and analysis
- Rotating user agents and request headers to avoid detection
- Comprehensive error handling and retry logic
- Rate limiting with random delays
- Data storage in both CSV and JSON formats
- Basic statistical analysis of collected data
- Detailed logging of the scraping process

## Project Structure

```
Week10/
├── src/
│   ├── main.py              # Main script
│   ├── config.py            # Configuration settings
│   ├── models.py            # Data models
│   ├── scraper_base.py      # Base scraper class
│   ├── amazon_scraper.py    # Amazon-specific implementation
│   └── data_manager.py      # Data handling and analysis
├── output/                  # Scraped data and analysis
├── logs/                    # Log files
└── requirements.txt         # Project dependencies
```

## Requirements

- Python 3.8+
- Chrome/Chromium browser
- ChromeDriver (installed automatically via webdriver-manager)

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the scraper from the command line:

```bash
python src/main.py "search term" [--min-products N] [--min-pages M]
```

Arguments:
- `search_term`: The product search term (required)
- `--min-products`: Minimum number of products to collect (default: 50)
- `--min-pages`: Minimum number of pages to scrape (default: 5)

Example:
```bash
python src/main.py "gaming laptop" --min-products 100 --min-pages 10
```

## Output

The scraper generates three types of output files in the `output` directory:

1. CSV file (`products_YYYYMMDD_HHMMSS.csv`)
2. JSON file (`products_YYYYMMDD_HHMMSS.json`)
3. Analysis report (`analysis_YYYYMMDD_HHMMSS.txt`)

## Extracted Data

For each product, the following attributes are collected:

- Product name and description
- Current price and original price
- Product image URL
- Customer rating (out of 5)
- Number of reviews
- Availability status
- Seller information
- Product category

## Error Handling

The scraper includes comprehensive error handling:

- Automatic retries with exponential backoff
- Graceful handling of missing elements
- Network error recovery
- Detailed error logging

## Logging

Logs are stored in the `logs` directory and include:

- Scraping progress
- Errors and exceptions
- Performance metrics
- Final statistics

## Extending

To add support for other e-commerce sites:

1. Create a new scraper class inheriting from `BaseScraper`
2. Implement the required abstract methods:
   - `extract_product_info()`
   - `navigate_to_next_page()`
3. Add site-specific selectors and logic

## License

MIT License 