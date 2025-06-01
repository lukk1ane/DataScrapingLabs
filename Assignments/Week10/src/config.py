from typing import Dict, List
import random

# Browser configuration
CHROME_OPTIONS = [
    '--headless',
    '--disable-gpu',
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-images',
    '--disable-css'
]

# Request headers
DEFAULT_HEADERS: Dict[str, str] = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Scraping configuration
MIN_DELAY: int = 2
MAX_DELAY: int = 5
MAX_RETRIES: int = 3
TIMEOUT: int = 30
MIN_PRODUCTS: int = 50
MIN_PAGES: int = 5

# File paths
OUTPUT_DIR: str = '../output'
LOG_FILE: str = '../logs/scraper.log'

def get_random_delay() -> float:
    """Generate a random delay between MIN_DELAY and MAX_DELAY seconds."""
    return random.uniform(MIN_DELAY, MAX_DELAY)

# Supported e-commerce sites
SUPPORTED_SITES = {
    'amazon': 'https://www.amazon.com',
    'ebay': 'https://www.ebay.com',
    'etsy': 'https://www.etsy.com',
    'bestbuy': 'https://www.bestbuy.com'
} 