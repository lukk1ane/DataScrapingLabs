import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from urllib.parse import urljoin, urlparse
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class Book:
    """Data class to represent a scraped book"""
    title: str
    price: str
    availability: str
    star_rating: int
    description: str
    category: str
    url: str


class BookScraper:
    def __init__(self):
        self.base_url = "https://books.toscrape.com"
        self.session = requests.Session()
        self.books_collected = []
        self.categories_visited = set()

        # User-Agent rotation pool (5+ different browsers)
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59'
        ]

        self._setup_session()

    def _setup_session(self):
        """Configure session with retry strategy and realistic headers"""
        # Retry strategy with exponential backoff
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set realistic default headers
        self._update_headers()

    def _update_headers(self, referer: Optional[str] = None):
        """Update session headers with rotation and realistic values"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }

        if referer:
            headers['Referer'] = referer

        self.session.headers.update(headers)

    def _smart_delay(self, delay_type: str = 'navigation'):
        """Implement variable delays to mimic human behavior"""
        if delay_type == 'navigation':
            delay = random.uniform(1, 3)  # 1-3s for navigation
        elif delay_type == 'reading':
            delay = random.uniform(3, 6)  # 3-6s for reading pages
        else:
            delay = random.uniform(0.5, 2)  # Default delay

        logger.info(f"Waiting {delay:.2f}s ({delay_type})")
        time.sleep(delay)

    def _make_request(self, url: str, retries: int = 3) -> Optional[requests.Response]:
        """Make HTTP request with error handling and retries"""
        for attempt in range(retries):
            try:
                self._update_headers(referer=self.session.cookies.get('last_url', self.base_url))
                response = self.session.get(url, timeout=15)
                response.raise_for_status()

                # Update last URL for referer
                self.session.cookies.set('last_url', url)
                return response

            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    # Exponential backoff
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed to fetch {url} after {retries} attempts")
                    return None

    def get_categories(self) -> List[Dict[str, str]]:
        """Scrape available book categories"""
        logger.info("Fetching book categories...")
        response = self._make_request(self.base_url)

        if not response:
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        categories = []

        # Find category links in sidebar
        category_links = soup.select('.nav-list ul li a')
        for link in category_links:
            if link.get('href') and 'catalogue/category' in link.get('href', ''):
                categories.append({
                    'name': link.text.strip(),
                    'url': urljoin(self.base_url, link.get('href'))
                })

        logger.info(f"Found {len(categories)} categories")
        return categories

    def _extract_star_rating(self, book_element) -> int:
        """Extract star rating from book element"""
        star_classes = ['One', 'Two', 'Three', 'Four', 'Five']
        rating_element = book_element.find('p', class_='star-rating')

        if rating_element:
            for i, star_class in enumerate(star_classes, 1):
                if star_class in rating_element.get('class', []):
                    return i
        return 0

    def _extract_book_details(self, book_url: str) -> Optional[Dict]:
        """Extract detailed information from individual book page"""
        self._smart_delay('reading')
        response = self._make_request(book_url)

        if not response:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            # Extract description
            description_element = soup.select_one('#product_description + p')
            description = description_element.text.strip() if description_element else "No description available"

            # Extract availability from product information table
            availability_element = soup.select_one('table.table-striped tr:has(th:contains("Availability")) td')
            if not availability_element:
                # Fallback to alternative selector
                availability_element = soup.select_one('.instock.availability')

            availability = availability_element.text.strip() if availability_element else "Unknown"

            # Clean up availability text
            availability = re.sub(r'\s+', ' ', availability).replace('In stock (', '').replace(' available)', '')

            return {
                'description': description,
                'availability': availability
            }

        except Exception as e:
            logger.error(f"Error extracting book details from {book_url}: {e}")
            return None

    def scrape_category(self, category_url: str, category_name: str, target_books: int = 10) -> List[Book]:
        """Scrape books from a specific category"""
        logger.info(f"Scraping category: {category_name}")
        books = []
        page = 1

        while len(books) < target_books:
            # Construct page URL
            if page == 1:
                page_url = category_url
            else:
                # Handle pagination properly
                if category_url.endswith('index.html'):
                    page_url = category_url.replace('index.html', f'page-{page}.html')
                else:
                    page_url = f"{category_url.rstrip('/')}/page-{page}.html"

            self._smart_delay('navigation')
            response = self._make_request(page_url)

            if not response:
                logger.info(f"Failed to fetch page {page} for {category_name}")
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            book_elements = soup.select('article.product_pod')

            if not book_elements:
                logger.info(f"No more books found on page {page} for {category_name}")
                break

            for book_element in book_elements:
                if len(books) >= target_books:
                    break

                try:
                    # Extract basic information
                    title_element = book_element.select_one('h3 a')
                    price_element = book_element.select_one('.price_color')

                    if not title_element or not price_element:
                        continue

                    title = title_element.get('title', title_element.text.strip())
                    price = price_element.text.strip()
                    star_rating = self._extract_star_rating(book_element)

                    # Filter for 4+ star ratings
                    if star_rating < 4:
                        logger.debug(f"Skipping '{title}' - only {star_rating} stars")
                        continue

                    # Construct book details page URL properly
                    book_href = title_element.get('href')
                    if book_href:
                        # Handle relative URLs properly
                        if book_href.startswith('../../../'):
                            # This is a relative link from category page like "../../../book-name_123/index.html"
                            # We need to resolve it relative to the base catalogue URL
                            book_url = f"{self.base_url}/catalogue/{book_href.replace('../../../', '')}"
                        elif book_href.startswith('../../'):
                            # Sometimes it might be "../../book-name_123/index.html"
                            book_url = f"{self.base_url}/catalogue/{book_href.replace('../../', '')}"
                        elif book_href.startswith('../'):
                            # Or just "../book-name_123/index.html"
                            book_url = f"{self.base_url}/catalogue/{book_href.replace('../', '')}"
                        elif book_href.startswith('catalogue/'):
                            # Already a relative path from root
                            book_url = f"{self.base_url}/{book_href}"
                        else:
                            # Use urljoin as fallback
                            book_url = urljoin(self.base_url, book_href)

                        logger.debug(f"Original href: {book_href} -> Constructed URL: {book_url}")
                    else:
                        logger.warning(f"No href found for book: {title}")
                        continue

                    # Extract detailed information
                    details = self._extract_book_details(book_url)
                    if not details:
                        logger.warning(f"Failed to get details for: {title}")
                        continue

                    book = Book(
                        title=title,
                        price=price,
                        availability=details['availability'],
                        star_rating=star_rating,
                        description=details['description'],
                        category=category_name,
                        url=book_url
                    )

                    books.append(book)
                    logger.info(f"Collected: '{title}' ({star_rating} stars) from {category_name}")

                except Exception as e:
                    logger.error(f"Error processing book element: {e}")
                    continue

            page += 1

            # Safety check to avoid infinite loops
            if page > 10:
                logger.warning(f"Reached page limit for category {category_name}")
                break

        return books

    def validate_book_data(self, book: Book) -> bool:
        """Validate book data before saving"""
        required_fields = [book.title, book.price, book.category]

        if not all(required_fields):
            logger.warning(f"Missing required fields for book: {book.title}")
            return False

        if book.star_rating < 4:
            logger.warning(f"Book {book.title} has less than 4 stars")
            return False

        return True

    def save_to_csv(self, filename: str = 'scraped_books.csv'):
        """Save collected books to CSV with data validation"""
        if not self.books_collected:
            logger.error("No books to save")
            return

        # Validate data
        valid_books = [book for book in self.books_collected if self.validate_book_data(book)]

        if not valid_books:
            logger.error("No valid books to save after validation")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'price', 'availability', 'star_rating', 'description', 'category', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for book in valid_books:
                writer.writerow({
                    'title': book.title,
                    'price': book.price,
                    'availability': book.availability,
                    'star_rating': book.star_rating,
                    'description': book.description[:500] + '...' if len(book.description) > 500 else book.description,
                    'category': book.category,
                    'url': book.url
                })

        logger.info(f"Saved {len(valid_books)} books to {filename}")

    def run_scraper(self, target_books: int = 20, min_categories: int = 3, debug: bool = False):
        """Main scraper execution with human-like navigation"""
        if debug:
            logging.getLogger().setLevel(logging.DEBUG)

        logger.info(f"Starting scraper - Target: {target_books} books from {min_categories}+ categories")

        # Get all available categories
        categories = self.get_categories()
        if len(categories) < min_categories:
            logger.error(f"Found only {len(categories)} categories, need at least {min_categories}")
            return

        logger.info(f"Available categories: {[cat['name'] for cat in categories]}")

        # Shuffle categories for more natural browsing
        random.shuffle(categories)

        books_per_category = max(1, target_books // min_categories)
        successful_categories = 0

        # Try more categories in case some fail
        for i, category in enumerate(categories):
            if len(self.books_collected) >= target_books or successful_categories >= min_categories:
                break

            remaining_books = target_books - len(self.books_collected)
            books_needed = min(books_per_category, remaining_books)

            # If we're close to the target and have minimum categories, get any remaining books
            if successful_categories >= min_categories and remaining_books > 0:
                books_needed = remaining_books

            logger.info(f"Attempting category {i + 1}: {category['name']} (need {books_needed} books)")
            logger.debug(f"Category URL: {category['url']}")

            # Human-like delay between category browsing
            self._smart_delay('navigation')

            try:
                category_books = self.scrape_category(
                    category['url'],
                    category['name'],
                    books_needed
                )

                if category_books:
                    self.books_collected.extend(category_books)
                    self.categories_visited.add(category['name'])
                    successful_categories += 1
                    logger.info(
                        f"✓ Collected {len(category_books)} books from {category['name']}. Total: {len(self.books_collected)}")
                else:
                    logger.warning(f"✗ No 4+ star books found in {category['name']}")

            except Exception as e:
                logger.error(f"✗ Error scraping category {category['name']}: {e}")
                continue

        # Check if we met minimum requirements
        if successful_categories < min_categories:
            logger.warning(f"Only successfully scraped {successful_categories} categories (needed {min_categories})")

        if len(self.books_collected) < target_books:
            logger.warning(f"Only collected {len(self.books_collected)} books (needed {target_books})")

        # Final summary
        logger.info(f"Scraping completed!")
        logger.info(f"Total books collected: {len(self.books_collected)}")
        logger.info(f"Successful categories: {successful_categories} - {list(self.categories_visited)}")

        # Save results if we have any books
        if self.books_collected:
            self.save_to_csv()
        else:
            logger.error("No books were collected to save!")

        return self.books_collected


def main():
    """Main execution function"""
    scraper = BookScraper()

    try:
        # First, test basic connectivity
        logger.info("Testing connectivity to books.toscrape.com...")
        test_response = scraper._make_request(scraper.base_url)
        if not test_response:
            logger.error("Cannot connect to books.toscrape.com. Please check your internet connection.")
            return

        logger.info("✓ Connection successful!")

        # Enable debug mode to see URL construction
        books = scraper.run_scraper(target_books=20, min_categories=3, debug=True)

        if books:
            print(f"\n=== SCRAPING SUMMARY ===")
            print(f"Books collected: {len(books)}")
            print(f"Categories: {len(scraper.categories_visited)}")
            print(f"Average rating: {sum(book.star_rating for book in books) / len(books):.1f}")
            print(f"Results saved to: scraped_books.csv")

            # Show sample of collected books
            print(f"\n=== SAMPLE BOOKS ===")
            for i, book in enumerate(books[:3]):
                print(f"{i + 1}. {book.title} ({book.star_rating} stars) - {book.category}")
                print(f"   Price: {book.price}")
                print(f"   URL: {book.url}")
        else:
            print("No books were successfully collected. Check the logs above for errors.")

    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()