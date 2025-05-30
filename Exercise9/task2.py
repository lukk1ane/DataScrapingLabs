import asyncio
import aiohttp
import aiofiles
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from asyncio import Semaphore

BASE_URL = "https://books.toscrape.com/"
RATE_LIMIT = 5

semaphore = Semaphore(RATE_LIMIT)

async def fetch(session, url):
    async with semaphore:
        async with session.get(url) as response:
            await asyncio.sleep(1 / RATE_LIMIT)
            return await response.text()

async def get_total_pages(session):
    html = await fetch(session, BASE_URL)
    soup = BeautifulSoup(html, 'html.parser')
    last_page = soup.select_one("li.current")
    if last_page:
        return int(last_page.text.strip().split()[-1])
    return 1

async def parse_book(book, base_url):
    title = book.h3.a['title']
    price = book.select_one('.price_color').text.strip()
    relative_url = book.h3.a['href']
    product_url = urljoin(base_url, relative_url)
    return {
        "Title": title,
        "Price": price,
        "Product Page URL": product_url
    }

async def scrape_page(session, page_number):
    page_url = BASE_URL
    if page_number > 1:
        page_url = BASE_URL + f"catalogue/page-{page_number}.html"
    html = await fetch(session, page_url)
    soup = BeautifulSoup(html, 'html.parser')
    books = soup.select('article.product_pod')
    tasks = [parse_book(book, page_url) for book in books]
    return await asyncio.gather(*tasks)

async def main():
    async with aiohttp.ClientSession() as session:
        total_pages = await get_total_pages(session)
        print(f"Total pages found: {total_pages}")

        tasks = [scrape_page(session, i) for i in range(1, total_pages + 1)]
        results_nested = await asyncio.gather(*tasks)

        all_books = [book for sublist in results_nested for book in sublist]
        async with aiofiles.open("books.json", "w") as f:
            await f.write(json.dumps(all_books, indent=2))
if __name__ == "__main__":
    asyncio.run(main())
