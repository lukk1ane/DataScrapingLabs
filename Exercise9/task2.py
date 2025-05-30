import aiohttp
import asyncio
import time
import json
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Suppress aiohttp SSL close warnings
logging.getLogger("aiohttp.client").setLevel(logging.CRITICAL)

BASE_URL = "https://books.toscrape.com/"
sem = asyncio.Semaphore(5)  # limit to 5 concurrent requests

async def fetch(session, url):
    async with sem:
        async with session.get(url) as response:
            await asyncio.sleep(0.2)  # enforce rate limit: 5 requests/sec
            return await response.text()

async def get_book_info(session, book_url):
    try:
        page = await fetch(session, book_url)
        soup = BeautifulSoup(page, "html.parser")
        title = soup.h1.text.strip() if soup.h1 else "N/A"
        price_tag = soup.select_one(".price_color")
        price = price_tag.text.strip() if price_tag else "N/A"
        return {"title": title, "price": price, "url": book_url}
    except Exception as e:
        return {"title": "Error", "price": "Error", "url": book_url, "error": str(e)}

async def get_all_books():
    books = []
    async with aiohttp.ClientSession() as session:
        next_page = "catalogue/page-1.html"
        while next_page:
            html = await fetch(session, urljoin(BASE_URL, next_page))
            soup = BeautifulSoup(html, "html.parser")
            book_links = [
                urljoin(BASE_URL, "catalogue/" + a['href'].strip())
                for a in soup.select("h3 > a")
            ]
            books += await asyncio.gather(*[get_book_info(session, url) for url in book_links])
            next_btn = soup.select_one(".next > a")
            next_page = urljoin("catalogue/", next_btn["href"]) if next_btn else None
    return books

async def main():
    start = time.time()
    books = await get_all_books()
    with open("books.json", "w") as f:
        json.dump(books, f, indent=2)
    print(f"Async scrape completed in {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
