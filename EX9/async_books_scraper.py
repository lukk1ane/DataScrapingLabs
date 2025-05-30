import asyncio
import aiohttp
import time
import json
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from asyncio_throttle import Throttler

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
BOOK_BASE = "https://books.toscrape.com/catalogue/"

throttler = Throttler(rate_limit=5, period=1)  # 5 requests per second

async def fetch(session: ClientSession, url: str) -> str:
    async with throttler:
        async with session.get(url) as response:
            return await response.text()

async def parse_books(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for book in soup.select("article.product_pod"):
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text
        rel_link = book.h3.a["href"]
        books.append({
            "title": title,
            "price": price,
            "url": BOOK_BASE + rel_link
        })
    return books

async def scrape_all_books():
    start = time.time()
    all_books = []
    async with aiohttp.ClientSession() as session:
        first_page_html = await fetch(session, BASE_URL.format(1))
        soup = BeautifulSoup(first_page_html, "html.parser")
        num_pages = int(soup.select_one("li.current").text.strip().split()[-1])

        tasks = [fetch(session, BASE_URL.format(i)) for i in range(1, num_pages + 1)]
        pages = await asyncio.gather(*tasks)

        for html in pages:
            books = await parse_books(html)
            all_books.extend(books)

    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(all_books, f, indent=2, ensure_ascii=False)

    end = time.time()
    print(f"\n[Async Scraping]")
    print(f"Total books scraped: {len(all_books)}")
    print("Total time:", round(end - start, 2), "seconds")

if __name__ == "__main__":
    asyncio.run(scrape_all_books())
