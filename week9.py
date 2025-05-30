import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Pool
import aiohttp
import asyncio
import json
from typing import List, Dict, Optional
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)


class Config:
    """Configuration settings for the scraper"""
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 10
    RATE_LIMIT = 5  # requests per second
    THREADS = 5
    PROCESSES = 5
    PAGES_TO_SCRAPE = 10


class QuoteScraper:
    """Handles Task 1 - Quote scraping comparison"""
    BASE_URL = "http://quotes.toscrape.com/page/{}/"

    @staticmethod
    @retry(stop=stop_after_attempt(Config.MAX_RETRIES), wait=wait_exponential(multiplier=1, min=2, max=10))
    def scrape_page(page_num: int) -> int:
        """Scrape a single page with retry logic"""
        try:
            url = QuoteScraper.BASE_URL.format(page_num)
            response = requests.get(url, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            quotes = soup.find_all('div', class_='quote')
            logging.info(f"Scraped page {page_num} - Found {len(quotes)} quotes")
            return len(quotes)
        except Exception as e:
            logging.error(f"Error scraping page {page_num}: {str(e)}")
            raise

    @staticmethod
    def sequential_scraping(pages: int = Config.PAGES_TO_SCRAPE) -> None:
        """Sequential scraping implementation"""
        start_time = time.time()
        total_quotes = 0

        for page in range(1, pages + 1):
            try:
                quotes_count = QuoteScraper.scrape_page(page)
                total_quotes += quotes_count
            except:
                logging.warning(f"Skipping page {page} after retries")
                continue

        total_time = time.time() - start_time
        avg_time = total_time / pages
        print(f"\nSequential - Total time: {total_time:.2f}s, Avg per page: {avg_time:.2f}s")
        print(f"Successfully scraped {total_quotes} quotes from {pages} pages")

    @staticmethod
    def threaded_scraping(pages: int = Config.PAGES_TO_SCRAPE, threads: int = Config.THREADS) -> None:
        """Threaded scraping implementation"""
        start_time = time.time()
        total_quotes = 0
        completed = 0

        def update_progress():
            nonlocal completed
            completed += 1
            logging.info(f"Progress: {completed}/{pages} pages ({completed / pages * 100:.1f}%)")

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(QuoteScraper.scrape_page, page): page for page in range(1, pages + 1)}
            for future in as_completed(futures):
                page = futures[future]
                try:
                    quotes_count = future.result()
                    total_quotes += quotes_count
                    update_progress()
                except:
                    logging.warning(f"Skipping page {page} after retries")
                    update_progress()

        total_time = time.time() - start_time
        avg_time = total_time / pages
        print(f"\nThreaded ({threads} threads) - Total time: {total_time:.2f}s, Avg per page: {avg_time:.2f}s")
        print(f"Successfully scraped {total_quotes} quotes from {pages} pages")

    @staticmethod
    def scrape_page_parallel(page_num: int) -> int:
        """Scrape a single page for multiprocessing"""
        try:
            return QuoteScraper.scrape_page(page_num)
        except:
            logging.warning(f"Skipping page {page_num} in multiprocessing")
            return 0

    @staticmethod
    def multiprocessing_scraping(pages: int = Config.PAGES_TO_SCRAPE, processes: int = Config.PROCESSES) -> None:
        """Multiprocessing scraping implementation"""
        start_time = time.time()
        completed = 0

        def callback(result: int) -> None:
            nonlocal completed
            completed += 1
            logging.info(f"Progress: {completed}/{pages} pages ({completed / pages * 100:.1f}%)")

        with Pool(processes=processes) as pool:
            results = []
            for page in range(1, pages + 1):
                results.append(pool.apply_async(
                    QuoteScraper.scrape_page_parallel,
                    (page,),
                    callback=callback
                ))
            total_quotes = sum(res.get() for res in results)

        total_time = time.time() - start_time
        avg_time = total_time / pages
        print(
            f"\nMultiprocessing ({processes} processes) - Total time: {total_time:.2f}s, Avg per page: {avg_time:.2f}s")
        print(f"Successfully scraped {total_quotes} quotes from {pages} pages")

    @staticmethod
    def run_all(pages: int = Config.PAGES_TO_SCRAPE) -> None:
        """Run all scraping methods for comparison"""
        print("\n=== Task 1: Quotes Scraping Comparison ===")
        QuoteScraper.sequential_scraping(pages)
        QuoteScraper.threaded_scraping(pages)
        QuoteScraper.multiprocessing_scraping(pages)


class BookScraper:
    """Handles Task 2 - Asynchronous book scraping with enhanced features"""
    BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
    RESULTS: List[Dict[str, str]] = []

    @staticmethod
    def validate_book_data(book_data: Dict[str, str]) -> bool:
        """Validate scraped book data"""
        required_fields = ['title', 'price', 'url']
        return all(field in book_data and book_data[field] for field in required_fields)

    @staticmethod
    @retry(stop=stop_after_attempt(Config.MAX_RETRIES), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def scrape_book_page(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> None:
        """Scrape a single book page with retry and rate limiting"""
        async with semaphore:
            try:
                async with session.get(url, timeout=Config.REQUEST_TIMEOUT) as response:
                    response.raise_for_status()
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    books = soup.find_all('article', class_='product_pod')

                    for book in books:
                        try:
                            title = book.h3.a['title']
                            price = book.find('p', class_='price_color').text
                            rel_url = book.h3.a['href']
                            full_url = f"https://books.toscrape.com/catalogue/{rel_url.replace('../../', '')}"

                            book_data = {
                                'title': title.strip(),
                                'price': price.strip(),
                                'url': full_url.strip()
                            }

                            if BookScraper.validate_book_data(book_data):
                                BookScraper.RESULTS.append(book_data)
                            else:
                                logging.warning(f"Invalid book data from {url}")
                        except Exception as e:
                            logging.error(f"Error parsing book from {url}: {str(e)}")

                    logging.info(f"Scraped page: {url}")
            except Exception as e:
                logging.error(f"Error scraping {url}: {str(e)}")
                raise

    @staticmethod
    async def get_total_pages(session: aiohttp.ClientSession) -> int:
        """Get total number of pages to scrape"""
        try:
            async with session.get(BookScraper.BASE_URL.format(1)) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                page_info = soup.find('li', class_='current')
                if page_info:
                    return int(page_info.text.split()[-1])
                return 1
        except Exception as e:
            logging.error(f"Error getting total pages: {str(e)}")
            return 1

    @staticmethod
    async def scrape_all_books() -> None:
        """Scrape all books with enhanced features"""
        start_time = time.time()
        connector = aiohttp.TCPConnector(limit_per_host=5)
        semaphore = asyncio.Semaphore(Config.RATE_LIMIT)

        async with aiohttp.ClientSession(connector=connector) as session:
            # Get total pages
            total_pages = await BookScraper.get_total_pages(session)
            logging.info(f"Found {total_pages} pages to scrape")

            # Create tasks for all pages
            tasks = []
            for page in range(1, total_pages + 1):
                url = BookScraper.BASE_URL.format(page)
                tasks.append(BookScraper.scrape_book_page(session, url, semaphore))

            # Show progress
            for i, task in enumerate(asyncio.as_completed(tasks), 1):
                await task
                logging.info(f"Progress: {i}/{total_pages} pages ({i / total_pages * 100:.1f}%)")

        # Save results
        with open('books.json', 'w') as f:
            json.dump(BookScraper.RESULTS, f, indent=2)

        total_time = time.time() - start_time
        print(f"\n=== Task 2: Book Scraping Results ===")
        print(f"Scraped {len(BookScraper.RESULTS)} valid books in {total_time:.2f} seconds")
        print(f"Results saved to books.json")
        print(f"Average speed: {len(BookScraper.RESULTS) / total_time:.2f} books/second")


def main() -> None:
    """Run both tasks with enhanced features"""
    try:
        # Task 1 - Quote scraping comparison
        QuoteScraper.run_all()

        # Task 2 - Book scraping
        asyncio.run(BookScraper.scrape_all_books())
    except Exception as e:
        logging.error(f"Fatal error in main: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()