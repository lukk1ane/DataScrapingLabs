import asyncio
import aiohttp
import async_timeout
import time
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = 'https://books.toscrape.com/'
CATALOGUE_URL = urljoin(BASE_URL, 'catalogue/')
RATE_LIMIT = 5  # max requests per second


def parse_book_info(book, base_url):
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text.strip()
    rel_url = book.h3.a['href']
    product_url = urljoin(base_url, rel_url)
    return {
        'title': title,
        'price': price,
        'product_page_url': product_url
    }


async def fetch(session, url, sem):
    async with sem:
        async with async_timeout.timeout(10):
            async with session.get(url) as response:
                return await response.text()


def get_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pager = soup.find('li', class_='current')
    if pager:
        text = pager.text.strip()
        total = int(text.split()[-1])
        return total
    return 1


async def scrape_books():
    start = time.time()
    sem = asyncio.Semaphore(RATE_LIMIT)
    async with aiohttp.ClientSession() as session:
        # Get first page to determine total pages
        first_page_url = urljoin(CATALOGUE_URL, 'page-1.html')
        html = await fetch(session, first_page_url, sem)
        total_pages = get_total_pages(html)
        print(f"Total pages: {total_pages}")

        tasks = []
        for i in range(1, total_pages + 1):
            page_url = urljoin(CATALOGUE_URL, f'page-{i}.html')
            tasks.append(fetch(session, page_url, sem))

        # Rate limiting: ensure no more than 5 requests/sec
        pages = []
        for i in range(0, len(tasks), RATE_LIMIT):
            chunk = tasks[i:i+RATE_LIMIT]
            results = await asyncio.gather(*chunk)
            pages.extend(results)
            if i + RATE_LIMIT < len(tasks):
                await asyncio.sleep(1)

        books = []
        for html in pages:
            soup = BeautifulSoup(html, 'html.parser')
            for book in soup.select('article.product_pod'):
                books.append(parse_book_info(book, CATALOGUE_URL))

        with open('books.json', 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)

        end = time.time()
        print(f"Scraped {len(books)} books in {end - start:.2f} seconds.")


def main():
    asyncio.run(scrape_books())


if __name__ == "__main__":
    main() 