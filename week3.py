import sys
import logging
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ProductData:
    """Data class to represent a product from the table."""
    product: str
    price: str
    stock: str


@dataclass
class Section:
    """Data class to represent a section with title and description."""
    title: str
    description: str


@dataclass
class Quote:
    """Data class to represent a quote with text and author."""
    text: str
    author: str
    tags: List[str] = None
    
    def __post_init__(self):
        """Initialize tags list if not provided."""
        if self.tags is None:
            self.tags = []


class HTMLParser:
    """Class for parsing HTML content and extracting data."""
    
    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, 'html.parser')
    
    def extract_page_title(self) -> str:
        title_tag = self.soup.head.title if self.soup.head else None
        return title_tag.text.strip() if title_tag else "No title found"
    
    def extract_heading_and_tagline(self) -> Tuple[str, str]:
        header_div = self.soup.find('div', id='top-header')
        
        heading = header_div.find('h1').text.strip() if header_div and header_div.find('h1') else "No heading found"
        tagline = header_div.find('p', class_='tagline').text.strip() if header_div and header_div.find('p', class_='tagline') else "No tagline found"
        
        return heading, tagline
    
    def extract_navigation_items(self) -> List[str]:
        nav_menu = self.soup.find('ul', class_='nav-menu')
        if not nav_menu:
            return []
            
        items = nav_menu.find_all('li', class_='menu-item')
        return [item.text.strip() for item in items]
    
    def extract_product_table_data(self) -> List[List[str]]:
        product_table = self.soup.find('table', id='product-table')
        if not product_table:
            return []
            
        rows = product_table.find_all('tr')
        return [[col.text.strip() for col in row.find_all(['th', 'td'])] for row in rows if row.find_all(['th', 'td'])]
    
    def extract_product_data(self) -> List[Dict[str, str]]:
        table_data = self.extract_product_table_data()
        if len(table_data) <= 1:
            return []
            
        headers = table_data[0]
        return [{headers[i]: value for i, value in enumerate(row) if i < len(headers)} 
                for row in table_data[1:]]
    
    def extract_section_info(self) -> List[Section]:
        sections = []
        sections_div = self.soup.find('div', class_='sections')
        if not sections_div:
            return sections
            
        for h2 in sections_div.find_all('h2'):
            title = h2.text.strip()
            description_elem = h2.find_next('p', class_='description')
            description = description_elem.text.strip() if description_elem else "No description found"
            sections.append(Section(title=title, description=description))
            
        return sections
    
    def extract_nested_elements(self) -> Dict[str, List[str]]:
        sections_div = self.soup.find('div', class_='sections')
        if not sections_div:
            return {'headings': [], 'paragraphs': []}
            
        return {
            'headings': [h.text.strip() for h in sections_div.find_all('h2')],
            'paragraphs': [p.text.strip() for p in sections_div.find_all('p')]
        }
    
    def extract_elements_by_id(self) -> Dict[str, str]:
        return {
            'section_1': self.soup.find('h2', id='section-1').text.strip() if self.soup.find('h2', id='section-1') else '',
            'nav_home': self.soup.find('li', id='nav-home').text.strip() if self.soup.find('li', id='nav-home') else ''
        }
    
    def extract_description_paragraphs(self) -> List[str]:
        return [p.text.strip() for p in self.soup.find_all('p', class_='description')]
    
    def extract_all_visible_text(self) -> str:
        if not self.soup.body:
            return "No body found"
        
        texts = []
        for element in self.soup.body.find_all(text=True):
            if element.parent.name.lower() not in ['script', 'style', 'meta', 'link']:
                text = element.strip()
                if text:
                    texts.append(text)
        
        return '\n'.join(texts)


class WebScraper:
    """Class for scraping web content."""
    
    def __init__(self, base_url: str, max_retries: int = 3, retry_delay: float = 1.0):
        """
        Initialize WebScraper with base URL and retry settings.
        
        Args:
            base_url: Base URL for scraping
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.session = requests.Session()
        
        # Set up headers to mimic a browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a web page with retry logic.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content of the page or None if failed
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Fetching {url} (attempt {attempt + 1}/{self.max_retries})")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
                    return None
    
    def scrape_quotes(self, url: str = None) -> Dict[str, Any]:
        """
        Scrape quotes from the quotes.toscrape.com website.
        
        Args:
            url: URL to scrape (defaults to base_url)
            
        Returns:
            Dictionary containing quotes, next_page, and tags
        """
        url = url or self.base_url
        html_content = self.fetch_page(url)
        if not html_content:
            return {'quotes': [], 'next_page': None, 'tags': []}
        
        soup = BeautifulSoup(html_content, 'html.parser')
        quotes = []
        
        for quote_div in soup.find_all('div', class_='quote'):
            quote_text = quote_div.find('span', class_='text').text.strip() if quote_div.find('span', class_='text') else ""
            author = quote_div.find('small', class_='author').text.strip() if quote_div.find('small', class_='author') else ""
            
            tags = []
            tags_div = quote_div.find('div', class_='tags')
            if tags_div:
                tags = [tag.text.strip() for tag in tags_div.find_all('a', class_='tag')]
            
            quotes.append(Quote(text=quote_text, author=author, tags=tags))
        
        next_li = soup.find('li', class_='next')
        next_page = f"{self.base_url}/{next_li.find('a')['href'].lstrip('/')}" if next_li and next_li.find('a') else None
        
        all_tags = sorted({tag.text.strip() for tag in soup.find_all('a', class_='tag')})
        
        return {
            'quotes': quotes,
            'next_page': next_page,
            'tags': all_tags
        }


def print_section_header(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def main() -> int:
    """
    Main function to execute all tasks.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    # Static HTML content provided in the task
    html_doc = """
    <html>
    <head><title>Complex Page</title></head>
    <body>
    <div id='top-header' class='header'>
    <h1>Main Heading</h1>
    <p class='tagline'>Welcome to the test page.</p>
    </div>
    <div id='navigation'>
    <ul class='nav-menu'>
    <li id='nav-home' class='menu-item'>Home</li>
    <li id='nav-about' class='menu-item'>About</li>
    <li id='nav-contact' class='menu-item'>Contact</li>
    </ul>
    </div>
    <div class='content'>
    <table id='product-table'>
    <tr><th>Product</th><th>Price</th><th>Stock</th></tr>
    <tr><td>Book A</td><td>$10</td><td>In Stock</td></tr>
    <tr><td>Book B</td><td>$15</td><td>Out of Stock</td></tr>
    </table>
    <div class='sections'>
    <h2 id='section-1'>Section 1</h2>
    <p class='description'>Details about section 1.</p>
    <h2 id='section-2'>Section 2</h2>
    <p class='description'>Details about section 2.</p>
    </div>
    </div>
    </body>
    </html>
    """
    
    try:
        logger.info("Starting HTML parsing tasks")
        
        # Part 1: Parse static HTML content
        parser = HTMLParser(html_doc)
        
        # Task 1: Extract Page Title
        print_section_header("Task 1: Extract Page Title")
        title = parser.extract_page_title()
        print(f"Page Title: {title}")
        
        # Task 2: Extract Main Heading and Tagline
        print_section_header("Task 2: Extract Main Heading and Tagline")
        heading, tagline = parser.extract_heading_and_tagline()
        print(f"Main Heading: {heading}")
        print(f"Tagline: {tagline}")
        
        # Task 3: Extract Navigation Menu Items
        print_section_header("Task 3: Extract Navigation Menu Items")
        nav_items = parser.extract_navigation_items()
        print("Navigation Menu Items:")
        for idx, item in enumerate(nav_items, 1):
            print(f"  {idx}. {item}")
        
        # Task 4: Extract Product Table Data
        print_section_header("Task 4: Extract Product Table Data")
        table_data = parser.extract_product_table_data()
        print("Product Table Data:")
        for row in table_data:
            print(f"  {' | '.join(row)}")
        
        # Task 5: Store Table Data in a Dictionary
        print_section_header("Task 5: Store Table Data in a Dictionary")
        product_dicts = parser.extract_product_data()
        print("Product Table as Dictionary:")
        for idx, product in enumerate(product_dicts, 1):
            print(f"  Product {idx}:")
            for key, value in product.items():
                print(f"    {key}: {value}")
        
        # Task 6: Extract Section Titles and Descriptions
        print_section_header("Task 6: Extract Section Titles and Descriptions")
        sections = parser.extract_section_info()
        print("Section Information:")
        for idx, section in enumerate(sections, 1):
            print(f"  Section {idx}:")
            print(f"    Title: {section.title}")
            print(f"    Description: {section.description}")
        
        # Task 7: Extract Deeply Nested Elements
        print_section_header("Task 7: Extract Deeply Nested Elements")
        nested_elements = parser.extract_nested_elements()
        print("Headings in 'sections' div:")
        for idx, heading in enumerate(nested_elements['headings'], 1):
            print(f"  {idx}. {heading}")
        print("\nParagraphs in 'sections' div:")
        for idx, paragraph in enumerate(nested_elements['paragraphs'], 1):
            print(f"  {idx}. {paragraph}")
        
        # Task 8: Extract Elements Using IDs
        print_section_header("Task 8: Extract Elements Using IDs")
        elements_by_id = parser.extract_elements_by_id()
        print(f"h2#section-1: {elements_by_id['section_1']}")
        print(f"li#nav-home: {elements_by_id['nav_home']}")
        
        # Task 9: Extract Specific Paragraphs
        print_section_header("Task 9: Extract Specific Paragraphs")
        description_paragraphs = parser.extract_description_paragraphs()
        print("Paragraphs with class='description':")
        for idx, paragraph in enumerate(description_paragraphs, 1):
            print(f"  {idx}. {paragraph}")
        
        # Final Task: Retrieve and format all visible text
        print_section_header("Final Task: Retrieve and Format All Visible Text")
        all_text = parser.extract_all_visible_text()
        print("All Visible Text:")
        print(all_text)
        
        # Part 2: Web scraping
        print_section_header("Part 2: Web Scraping quotes.toscrape.com")
        quotes_url = 'http://quotes.toscrape.com'
        scraper = WebScraper(quotes_url)
        
        quotes_data = scraper.scrape_quotes()
        
        # Print quotes and authors
        print("Quotes and Authors:")
        for idx, quote in enumerate(quotes_data['quotes'], 1):
            print(f"  Quote {idx}:")
            print(f"    Text: {quote.text}")
            print(f"    Author: {quote.author}")
            print(f"    Tags: {', '.join(quote.tags)}")
        
        # Print next page link
        print("\nNext Page Link:")
        print(f"  {quotes_data['next_page'] or 'No next page found'}")
        
        # Print tags
        print("\nTags:")
        for idx, tag in enumerate(quotes_data['tags'], 1):
            print(f"  {idx}. {tag}")
        
        logger.info("All tasks completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())