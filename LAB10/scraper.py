import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
import random
import csv
import re
from typing import List, Dict, Any, Set

class BookScraper:
    BASE_URL: str = "https://books.toscrape.com/"
    BOOKS_TARGET: int = 20
    CATEGORIES_TARGET: int = 3
    USER_AGENTS: List[str] = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/90.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]

    def __init__(self) -> None:
        self.scraped_books: List[Dict[str, Any]] = []
        self.actual_scraped_categories: Set[str] = set()

    async def _get_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(headers=self._get_request_headers())

    def _get_request_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": self.BASE_URL,
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

    async def _smart_delay(self, page_type: str = "navigation") -> None:
        base_delay: float
        if page_type == "navigation":
            base_delay = random.uniform(1, 3)
        elif page_type == "reading":
            base_delay = random.uniform(3, 6)
        else:
            base_delay = 1.0
        
        jitter = random.uniform(0.1, 0.5)
        await asyncio.sleep(base_delay + jitter)

    async def _retry_request(self, session: aiohttp.ClientSession, url: str, max_retries: int = 5) -> str:
        for i in range(max_retries):
            try:
                async with session.get(url, headers=self._get_request_headers()) as response:
                    response.raise_for_status()
                    return await response.text()
            except aiohttp.ClientError as e:
                print(f"Request failed for {url}: {e}. Retrying in {2**i} seconds...")
                await asyncio.sleep(2**i)
        raise Exception(f"Failed to retrieve {url} after {max_retries} retries.")

    async def get_categories(self) -> List[Dict[str, str]]:
        print("Getting categories...")
        async with aiohttp.ClientSession() as session:
            response_text = await self._retry_request(session, self.BASE_URL)
            soup = BeautifulSoup(response_text, 'html.parser')
            categories: List[Dict[str, str]] = []
            all_category_links = soup.select('div.side_categories ul.nav-list li a')
            for li in all_category_links[1:]:
                category_name = li.get_text().strip()
                category_url = self.BASE_URL + li['href']
                categories.append({"name": category_name, "url": category_url})
            return categories

    def _get_star_rating_value(self, star_rating_class: str) -> int:
        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }
        return rating_map.get(star_rating_class, 0)

    async def scrape_category_page(self, session: aiohttp.ClientSession, category_url: str) -> List[Dict[str, Any]]:
        print(f"Scraping category page: {category_url}")
        books_on_page: List[Dict[str, Any]] = []
        response_text = await self._retry_request(session, category_url)
        soup = BeautifulSoup(response_text, 'html.parser')

        initial_book_count: int = 0
        four_star_plus_count: int = 0

        for article in soup.find_all('article', class_='product_pod'):
            initial_book_count += 1
            star_rating_class = article.find('p', class_='star-rating')['class'][1]
            star_rating = self._get_star_rating_value(star_rating_class)

            if star_rating >= 4:
                four_star_plus_count += 1
                title = article.h3.a['title']
                price = article.find('p', class_='price_color').get_text().strip()
                availability = article.find('p', class_='instock availability').get_text().strip()
                book_url = self.BASE_URL + 'catalogue/' + article.h3.a['href'].replace('../', '')
                books_on_page.append({
                    "title": title,
                    "price": price,
                    "availability": availability,
                    "star_rating": star_rating,
                    "book_url": book_url
                })
        print(f"Found {initial_book_count} books on {category_url}, {four_star_plus_count} of them are 4+ stars.")
        return books_on_page

    async def scrape_book_details(self, session: aiohttp.ClientSession, book_url: str, category: str) -> Dict[str, str]:
        print(f"Scraping book details: {book_url}")
        response_text = await self._retry_request(session, book_url)
        soup = BeautifulSoup(response_text, 'html.parser')

        description_div = soup.find('div', id='product_description')
        description_text = description_div.find_next_sibling('p').get_text().strip() if description_div else "N/A"

        return {
            "description": description_text,
            "category": category
        }

    async def _process_category_page(self, session: aiohttp.ClientSession, category_info: Dict[str, str], page_url: str) -> bool:
        books_on_page = await self.scrape_category_page(session, page_url)
        await self._smart_delay("reading")

        if not books_on_page:
            print(f"No more books found on {page_url} for category {category_info['name']}.")
            return False

        tasks: List[Any] = []
        for book in books_on_page:
            if len(self.scraped_books) < self.BOOKS_TARGET or len(self.actual_scraped_categories) < self.CATEGORIES_TARGET:
                tasks.append(self.scrape_book_details(session, book['book_url'], category_info['name']))
            else:
                break

        if tasks:
            book_details_list = await asyncio.gather(*tasks)

            for i, book_details in enumerate(book_details_list):
                original_book = books_on_page[i]
                combined_book_data = {**original_book, **book_details}
                self.scraped_books.append(combined_book_data)
                self.actual_scraped_categories.add(category_info['name'])
                print(f"Added book: {original_book['title']}. Total scraped: {len(self.scraped_books)}. Categories: {len(self.actual_scraped_categories)}")
                await self._smart_delay("reading")
        return True

    async def scrape_category(self, category_info: Dict[str, str]) -> None:
        print(f"Scraping books from category: {category_info['name']}")
        category_url = category_info['url']
        page_num = 1

        async with aiohttp.ClientSession(headers=self._get_request_headers()) as session:
            while True:
                if len(self.scraped_books) >= self.BOOKS_TARGET and len(self.actual_scraped_categories) >= self.CATEGORIES_TARGET:
                    break

                page_url = f"{category_url.replace('index.html', '')}page-{page_num}.html" if page_num > 1 else category_url

                try:
                    books_processed_on_page = await self._process_category_page(session, category_info, page_url)
                    
                    if not books_processed_on_page:
                        break

                    if len(self.scraped_books) >= self.BOOKS_TARGET and len(self.actual_scraped_categories) >= self.CATEGORIES_TARGET:
                        break

                    response_text = await self._retry_request(session, page_url)
                    soup = BeautifulSoup(response_text, 'html.parser')
                    next_button = soup.find('li', class_='next')
                    if not next_button:
                        print(f"No next page button found for category {category_info['name']}.")
                        break
                    
                    page_num += 1

                except Exception as e:
                    print(f"Error scraping category page {page_url}: {e}. Skipping this page.")
                    break

    async def scrape(self) -> None:
        categories = await self.get_categories()
        random.shuffle(categories)
        print(f"Found {len(categories)} categories. Starting asynchronous scraping...")

        tasks: List[Any] = []
        for category_info in categories:
            if len(self.scraped_books) >= self.BOOKS_TARGET and len(self.actual_scraped_categories) >= self.CATEGORIES_TARGET:
                break
            tasks.append(self.scrape_category(category_info))
        
        await asyncio.gather(*tasks)

        print(f"Scraping complete. Total books scraped: {len(self.scraped_books)}")
        print(f"Scraped from {len(self.actual_scraped_categories)} unique categories.")

        self.save_to_csv(self.scraped_books)

    def save_to_csv(self, data: List[Dict[str, Any]]) -> None:
        if not data:
            print("No data to save.")
            return

        keys = data[0].keys()
        with open('scraped_books.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

async def main() -> None:
    scraper = BookScraper()
    await scraper.scrape()

if __name__ == "__main__":
    asyncio.run(main())