import asyncio
import aiohttp
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AsyncBookScraper:
    def __init__(self, base_url: str = "https://books.toscrape.com/", max_requests_per_second: int = 5):
        self.base_url = base_url
        self.max_requests_per_second = max_requests_per_second
        self.request_interval = 1.0 / max_requests_per_second
        self.last_request_time = 0
        self.books_data = []
        self.session = None

        self.rate_limit_semaphore = asyncio.Semaphore(max_requests_per_second)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=self.headers
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def rate_limited_request(self, url: str) -> Optional[str]:
        async with self.rate_limit_semaphore:
            try:
                current_time = time.time()
                time_since_last_request = current_time - self.last_request_time
                if time_since_last_request < self.request_interval:
                    sleep_time = self.request_interval - time_since_last_request
                    await asyncio.sleep(sleep_time)

                self.last_request_time = time.time()

                async with self.session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        logger.debug(f"Successfully fetched: {url}")
                        return content
                    else:
                        logger.warning(f"HTTP {response.status} for URL: {url}")
                        return None

            except asyncio.TimeoutError:
                logger.error(f"Timeout error for URL: {url}")
                return None
            except Exception as e:
                logger.error(f"Error fetching {url}: {str(e)}")
                return None

    async def get_total_pages(self) -> int:
        logger.info("Determining total number of pages...")

        content = await self.rate_limited_request(self.base_url)
        if not content:
            logger.error("Failed to fetch the main page")
            return 0

        soup = BeautifulSoup(content, 'html.parser')

        pager = soup.find('li', class_='current')
        if pager:
            page_text = pager.get_text(strip=True)
            try:
                total_pages = int(page_text.split('of')[-1].strip())
                logger.info(f"Found {total_pages} total pages")
                return total_pages
            except (ValueError, IndexError):
                logger.warning("Could not parse total pages from pagination")

        logger.info("No pagination found, assuming single page")
        return 1

    def extract_book_info(self, book_element, page_url: str) -> Dict:
        try:
            title_element = book_element.find('h3').find('a')
            title = title_element.get('title', '').strip()

            price_element = book_element.find('p', class_='price_color')
            price = price_element.get_text(strip=True) if price_element else 'N/A'

            product_url = title_element.get('href', '')
            if product_url:
                product_url = urljoin(page_url, product_url)

            rating_element = book_element.find('p', class_='star-rating')
            rating = None
            if rating_element:
                rating_classes = rating_element.get('class', [])
                for cls in rating_classes:
                    if cls in ['One', 'Two', 'Three', 'Four', 'Five']:
                        rating = cls
                        break

            availability_element = book_element.find('p', class_='instock availability')
            availability = availability_element.get_text(strip=True) if availability_element else 'Unknown'

            return {
                'title': title,
                'price': price,
                'product_page_url': product_url,
                'rating': rating,
                'availability': availability
            }

        except Exception as e:
            logger.error(f"Error extracting book info: {str(e)}")
            return None

    async def scrape_page(self, page_num: int) -> List[Dict]:
        """Scrape books from a single page"""
        if page_num == 1:
            url = self.base_url
        else:
            url = f"{self.base_url}catalogue/page-{page_num}.html"

        logger.info(f"Scraping page {page_num}: {url}")

        content = await self.rate_limited_request(url)
        if not content:
            logger.error(f"Failed to fetch page {page_num}")
            return []

        soup = BeautifulSoup(content, 'html.parser')

        book_containers = soup.find_all('article', class_='product_pod')

        books = []
        for book_element in book_containers:
            book_info = self.extract_book_info(book_element, url)
            if book_info:
                books.append(book_info)

        logger.info(f"Found {len(books)} books on page {page_num}")
        return books

    async def scrape_all_books(self) -> List[Dict]:
        logger.info("Starting to scrape all books...")
        start_time = time.time()

        total_pages = await self.get_total_pages()
        if total_pages == 0:
            logger.error("Could not determine total pages")
            return []

        tasks = []
        for page_num in range(1, total_pages + 1):
            task = asyncio.create_task(self.scrape_page(page_num))
            tasks.append(task)

        logger.info(f"Starting concurrent scraping of {total_pages} pages...")
        page_results = await asyncio.gather(*tasks, return_exceptions=True)

        all_books = []
        successful_pages = 0

        for i, result in enumerate(page_results, 1):
            if isinstance(result, Exception):
                logger.error(f"Page {i} failed with exception: {result}")
            elif isinstance(result, list):
                all_books.extend(result)
                successful_pages += 1
            else:
                logger.warning(f"Unexpected result type for page {i}: {type(result)}")

        end_time = time.time()
        duration = end_time - start_time

        logger.info(f"Scraping completed!")
        logger.info(f"Successfully scraped {successful_pages}/{total_pages} pages")
        logger.info(f"Total books found: {len(all_books)}")
        logger.info(f"Total duration: {duration:.2f} seconds")
        logger.info(f"Average time per page: {duration / total_pages:.2f} seconds")
        logger.info(f"Books per second: {len(all_books) / duration:.2f}")

        return all_books

    async def save_to_json(self, books: List[Dict], filename: str = "books_data.json"):
        """Save books data to JSON file"""
        try:
            output_data = {
                "scraping_info": {
                    "total_books": len(books),
                    "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "source_url": self.base_url,
                    "rate_limit": f"{self.max_requests_per_second} requests/second"
                },
                "books": books
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Data saved to {filename}")
            logger.info(f"File size: {len(json.dumps(output_data))} characters")

        except Exception as e:
            logger.error(f"Error saving to JSON: {str(e)}")


async def main():
    print("=" * 70)
    print("ASYNCHRONOUS BOOK SCRAPER")
    print("=" * 70)
    print(f"Target: https://books.toscrape.com/")
    print(f"Rate limit: 5 requests per second")
    print(f"Data to extract: Title, Price, Product URL")
    print("=" * 70)

    start_time = time.time()

    async with AsyncBookScraper(max_requests_per_second=5) as scraper:
        books = await scraper.scrape_all_books()

        if books:
            await scraper.save_to_json(books)

            print("\n" + "=" * 70)
            print("SCRAPING SUMMARY")
            print("=" * 70)

            print(f"Total books scraped: {len(books)}")

            prices = []
            for book in books:
                try:
                    price_str = book['price'].replace('£', '').replace('$', '')
                    price = float(price_str)
                    prices.append(price)
                except:
                    continue

            if prices:
                print(f"Price range: £{min(prices):.2f} - £{max(prices):.2f}")
                print(f"Average price: £{sum(prices) / len(prices):.2f}")

            ratings = {}
            for book in books:
                rating = book.get('rating', 'Unknown')
                ratings[rating] = ratings.get(rating, 0) + 1

            print(f"Rating distribution:")
            for rating, count in sorted(ratings.items()):
                print(f"  {rating}: {count}")

            print("\n" + "=" * 70)
            print("SAMPLE BOOKS")
            print("=" * 70)

            for i, book in enumerate(books[:5], 1):
                print(f"\nBook {i}:")
                print(f"  Title: {book['title']}")
                print(f"  Price: {book['price']}")
                print(f"  Rating: {book.get('rating', 'N/A')}")
                print(f"  URL: {book['product_page_url']}")

        else:
            print("No books were scraped successfully.")

    end_time = time.time()
    total_duration = end_time - start_time

    print(f"\n" + "=" * 70)
    print(f"TOTAL TASK DURATION: {total_duration:.2f} seconds")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())