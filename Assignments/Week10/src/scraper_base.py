from abc import ABC, abstractmethod
from typing import List, Optional
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from loguru import logger

from models import Product
from config import (
    CHROME_OPTIONS,
    DEFAULT_HEADERS,
    MAX_RETRIES,
    TIMEOUT,
    get_random_delay
)

class BaseScraper(ABC):
    """Base class for web scrapers with common functionality."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.user_agent = UserAgent()
        self.driver = None
        self.setup_logger()
        
    def setup_logger(self):
        """Configure logging."""
        logger.add("../logs/scraper_{time}.log", rotation="500 MB")
        
    def setup_driver(self) -> webdriver.Chrome:
        """Set up Chrome WebDriver with appropriate options."""
        options = Options()
        
        # Add standard options
        for option in CHROME_OPTIONS:
            options.add_argument(option)
        
        # Set random user agent
        user_agent = self.user_agent.random
        options.add_argument(f'user-agent={user_agent}')
        
        # Additional anti-bot measures
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Performance options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')
        
        # Create driver
        driver = webdriver.Chrome(options=options)
        
        # Set page load timeout
        driver.set_page_load_timeout(TIMEOUT)
        
        # Set window size to a common resolution
        driver.set_window_size(1920, 1080)
        
        # Add additional headers
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": user_agent,
            "acceptLanguage": DEFAULT_HEADERS['Accept-Language']
        })
        
        # Execute stealth JavaScript
        driver.execute_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        return driver
    
    def retry_with_backoff(self, func, *args, **kwargs):
        """Execute function with exponential backoff retry logic."""
        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except (TimeoutException, WebDriverException) as e:
                if attempt == MAX_RETRIES - 1:
                    logger.error(f"Max retries reached for {func.__name__}: {str(e)}")
                    raise
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time:.2f}s")
                time.sleep(wait_time)
    
    def wait_for_element(self, locator, timeout: int = TIMEOUT):
        """Wait for element to be present and visible."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    @abstractmethod
    def extract_product_info(self, product_element) -> Product:
        """Extract product information from element."""
        pass
    
    @abstractmethod
    def navigate_to_next_page(self) -> bool:
        """Navigate to next page of products."""
        pass
    
    def clean_text(self, text: Optional[str]) -> Optional[str]:
        """Clean and normalize text data."""
        if not text:
            return None
        return ' '.join(text.strip().split())
    
    def parse_price(self, price_str: Optional[str]) -> Optional[float]:
        """Parse price string to float."""
        if not price_str:
            return None
        try:
            # Remove currency symbols and convert to float
            clean_price = ''.join(c for c in price_str if c.isdigit() or c == '.')
            return float(clean_price)
        except ValueError:
            logger.warning(f"Could not parse price: {price_str}")
            return None
    
    def parse_rating(self, rating_str: Optional[str]) -> Optional[float]:
        """Parse rating string to float."""
        if not rating_str:
            return None
        try:
            # Extract first number from string (e.g., "4.5 out of 5" -> 4.5)
            import re
            match = re.search(r'(\d+\.?\d*)', rating_str)
            return float(match.group(1)) if match else None
        except (ValueError, AttributeError):
            logger.warning(f"Could not parse rating: {rating_str}")
            return None
    
    def __enter__(self):
        """Set up WebDriver when entering context."""
        self.driver = self.setup_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up WebDriver when exiting context."""
        if self.driver:
            self.driver.quit() 