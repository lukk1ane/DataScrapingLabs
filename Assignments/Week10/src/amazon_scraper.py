from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import time
import requests
from loguru import logger

from scraper_base import BaseScraper
from models import Product
from config import get_random_delay, DEFAULT_HEADERS

class AmazonScraper(BaseScraper):
    """Amazon-specific scraper implementation."""
    
    def __init__(self, search_term: str):
        super().__init__("https://www.amazon.com")
        self.search_term = search_term
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        
    def start_scraping(self):
        """Start the scraping process with the search term."""
        search_url = f"{self.base_url}/s?k={self.search_term.replace(' ', '+')}"
        
        # First try with requests
        response = self.session.get(search_url)
        if response.status_code == 200:
            self.current_page = BeautifulSoup(response.text, 'html.parser')
        else:
            # If requests fails, fall back to Selenium
            self.driver.get(search_url)
            time.sleep(get_random_delay())
            self.current_page = BeautifulSoup(self.driver.page_source, 'html.parser')
    
    def extract_product_info(self, product_element) -> Product:
        """Extract product information from an Amazon product element."""
        try:
            # Product name
            name_element = product_element.select_one('.a-text-normal')
            if not name_element:
                name_element = product_element.select_one('.a-link-normal .a-text-normal')
            if not name_element:
                logger.warning("Could not find product name")
                return None
            name = self.clean_text(name_element.text)
            
            # Product URL
            url_element = product_element.select_one('a.a-link-normal[href*="/dp/"]')
            if not url_element:
                logger.warning("Could not find product URL")
                return None
            url = url_element['href']
            if not url.startswith('http'):
                url = f"{self.base_url}{url}"
            
            # Current price
            price_element = product_element.select_one('.a-price .a-offscreen')
            if not price_element:
                price_element = product_element.select_one('.a-price-whole')
            current_price = self.parse_price(price_element.text) if price_element else None
            
            # Original price
            original_price_element = product_element.select_one('.a-text-price .a-offscreen')
            original_price = self.parse_price(original_price_element.text) if original_price_element else None
            
            # Image URL
            img_element = product_element.select_one('img.s-image')
            if not img_element:
                img_element = product_element.select_one('img[data-image-latency="s-product-image"]')
            image_url = img_element['src'] if img_element else None
            
            # Rating
            rating_element = product_element.select_one('i.a-icon-star-small span, span.a-icon-alt')
            if not rating_element:
                rating_element = product_element.select_one('[aria-label*="out of 5 stars"]')
            rating = self.parse_rating(rating_element.text if rating_element else None)
            
            # Review count
            review_element = product_element.select_one('span.a-size-base.s-underline-text')
            if not review_element:
                review_element = product_element.select_one('[aria-label*="total ratings"]')
            review_count = int(''.join(filter(str.isdigit, review_element.text))) if review_element else None
            
            # Availability
            availability_element = product_element.select_one('span.a-color-price')
            if not availability_element:
                availability_element = product_element.select_one('[data-csa-c-type="availability"]')
            availability = self.clean_text(availability_element.text) if availability_element else "In Stock"
            
            # Seller
            seller_element = product_element.select_one('span.a-size-small.a-color-secondary')
            if not seller_element:
                seller_element = product_element.select_one('.s-selling-partner-info')
            seller = self.clean_text(seller_element.text) if seller_element else "Amazon"
            
            # Category
            category_element = product_element.select_one('[data-csa-c-type="category"]')
            category = self.clean_text(category_element.text) if category_element else self.search_term.capitalize()
            
            # Description (would need to visit product page)
            description = None
            
            return Product(
                name=name,
                description=description,
                current_price=current_price,
                original_price=original_price,
                image_url=image_url,
                rating=rating,
                review_count=review_count,
                availability=availability,
                seller=seller,
                category=category,
                url=url
            )
            
        except Exception as e:
            logger.error(f"Error extracting product info: {str(e)}")
            return None
    
    def navigate_to_next_page(self) -> bool:
        """Navigate to the next page of products."""
        try:
            # Try to find next page link in current BeautifulSoup object
            next_link = self.current_page.select_one('a.s-pagination-next:not(.s-pagination-disabled)')
            if not next_link:
                next_link = self.current_page.select_one('.s-pagination-button:not([aria-disabled="true"])')
            
            if not next_link:
                return False
            
            next_url = next_link['href']
            if not next_url.startswith('http'):
                next_url = f"{self.base_url}{next_url}"
            
            # Try with requests first
            response = self.session.get(next_url)
            if response.status_code == 200:
                self.current_page = BeautifulSoup(response.text, 'html.parser')
                return True
            
            # Fall back to Selenium if requests fails
            self.driver.get(next_url)
            time.sleep(get_random_delay())
            self.current_page = BeautifulSoup(self.driver.page_source, 'html.parser')
            return True
            
        except Exception as e:
            logger.error(f"Error navigating to next page: {str(e)}")
            return False
    
    def get_product_elements(self):
        """Get all product elements from the current page."""
        selectors = [
            'div[data-component-type="s-search-result"]',
            'div.s-result-item:not(.AdHolder)',
            '.s-card-container'
        ]
        
        for selector in selectors:
            elements = self.current_page.select(selector)
            if elements:
                return elements
        
        return [] 