"""
Task 2: Asynchronous Book Scraping with Rate Limiting
Scrapes all books from all pages of https://books.toscrape.com/
using asyncio and aiohttp with proper rate limiting (max 5 requests per second)
"""

import asyncio
import aiohttp
import json
import time
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse
import re


class RateLimiter:
    """Rate limiter to control request frequency"""
    
    def __init__(self, max_requests: int, time_window: float = 1.0):
        """
        Initialize rate limiter
        
        Args:
            max_requests: Maximum number of requests allowed
            time_window: Time window in seconds (default: 1.0 second)
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    async def acquire(self):
        """Acquire permission to make a request"""
        now = time.time()
        
        # Remove old requests outside the time window
        self.requests = [req_time for req_time in self.requests if now - req_time < self.time_window]
        
        # If we're at the limit, wait
        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                return await self.acquire()
        
        # Record this request
        self.requests.append(now)


class BookScraper:
    """Asynchronous book scraper for books.toscrape.com"""
    
    def __init__(self, max_requests_per_second: int = 5):
        """
        Initialize the book scraper
        
        Args:
            max_requests_per_second: Maximum requests per second for rate limiting
        """
        self.base_url = "https://books.toscrape.com/"
        self.rate_limiter = RateLimiter(max_requests_per_second)
        self.session = None
        self.books = []
        
    async def __aenter__(self):
        """Async context manager entry"""
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a single page with rate limiting
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if failed
        """
        await self.rate_limiter.acquire()
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Failed to fetch {url}: HTTP {response.status}")
                    return None
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None
    
    def extract_books_from_page(self, html: str, page_url: str) -> List[Dict[str, Any]]:
        """
        Extract book information from a catalog page
        
        Args:
            html: HTML content of the page
            page_url: URL of the current page for resolving relative URLs
            
        Returns:
            List of book dictionaries
        """
        soup = BeautifulSoup(html, 'html.parser')
        books = []
        
        # Find all book articles
        book_articles = soup.find_all('article', class_='product_pod')
        
        for article in book_articles:
            try:
                # Extract title
                title_element = article.find('h3').find('a')
                title = title_element.get('title', '').strip()
                
                # Extract price
                price_element = article.find('p', class_='price_color')
                price = price_element.get_text(strip=True) if price_element else 'N/A'
                
                # Extract product page URL
                relative_url = title_element.get('href', '')
                product_url = urljoin(page_url, relative_url)
                
                books.append({
                    'title': title,
                    'price': price,
                    'product_page_url': product_url
                })
                
            except Exception as e:
                print(f"Error extracting book data: {str(e)}")
                continue
        
        return books
    
    def find_next_page_url(self, html: str, current_url: str) -> Optional[str]:
        """
        Find the URL of the next page
        
        Args:
            html: HTML content of current page
            current_url: URL of current page
            
        Returns:
            URL of next page or None if no next page
        """
        soup = BeautifulSoup(html, 'html.parser')
        next_link = soup.find('li', class_='next')
        
        if next_link:
            next_href = next_link.find('a').get('href')
            return urljoin(current_url, next_href)
        
        return None
    
    async def scrape_all_books(self) -> List[Dict[str, Any]]:
        """
        Scrape all books from all pages
        
        Returns:
            List of all books found
        """
        print("Starting asynchronous book scraping...")
        start_time = time.time()
        
        current_url = self.base_url
        page_count = 0
        
        while current_url:
            page_count += 1
            print(f"Scraping page {page_count}: {current_url}")
            
            # Fetch the page
            html = await self.fetch_page(current_url)
            if not html:
                print(f"Failed to fetch page {page_count}")
                break
            
            # Extract books from this page
            page_books = self.extract_books_from_page(html, current_url)
            self.books.extend(page_books)
            print(f"  Found {len(page_books)} books on page {page_count}")
            
            # Find next page URL
            current_url = self.find_next_page_url(html, current_url)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\nScraping completed!")
        print(f"Total pages scraped: {page_count}")
        print(f"Total books found: {len(self.books)}")
        print(f"Total duration: {total_time:.2f} seconds")
        print(f"Average time per page: {total_time/page_count:.2f} seconds")
        print(f"Books per second: {len(self.books)/total_time:.2f}")
        
        return self.books
    
    def save_to_json(self, filename: str = "books_data.json"):
        """
        Save scraped books to JSON file
        
        Args:
            filename: Name of the JSON file to save
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.books, f, indent=2, ensure_ascii=False)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {str(e)}")


async def main():
    """
    Main function to run the asynchronous book scraping
    """
    print("=" * 60)
    print("ASYNCHRONOUS BOOK SCRAPING WITH RATE LIMITING")
    print("=" * 60)
    print("Target: https://books.toscrape.com/")
    print("Rate limit: 5 requests per second")
    print("=" * 60)
    
    # Use async context manager for proper resource cleanup
    async with BookScraper(max_requests_per_second=5) as scraper:
        # Scrape all books
        books = await scraper.scrape_all_books()
        
        # Save to JSON file
        scraper.save_to_json("books_data.json")
        
        # Display sample data
        print("\n" + "=" * 60)
        print("SAMPLE RESULTS")
        print("=" * 60)
        
        if books:
            print(f"Showing first 5 books out of {len(books)} total:")
            for i, book in enumerate(books[:5], 1):
                print(f"\n{i}. Title: {book['title']}")
                print(f"   Price: {book['price']}")
                print(f"   URL: {book['product_page_url']}")
        else:
            print("No books were scraped!")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 