import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin
from aiolimiter import AsyncLimiter

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = urljoin(BASE_URL, "catalogue/")
RATE_LIMIT = AsyncLimiter(max_rate=5, time_period=1)  # Max 5 requests per second

books = []

# Extract book info from one page
async def fetch_page(session, url):
    async with RATE_LIMIT:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            for book in soup.select("article.product_pod"):
                title = book.h3.a["title"]
                price = book.select_one("p.price_color").text.strip()
                relative_url = book.h3.a["href"]
                product_url = urljoin(CATALOGUE_URL, relative_url)
                books.append({
                    "title": title,
                    "price": price,
                    "url": product_url
                })

            # Check for "next" page
            next_link = soup.select_one("li.next > a")
            if next_link:
                next_page = urljoin(url, next_link["href"])
                await fetch_page(session, next_page)


async def main():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        first_page_url = urljoin(CATALOGUE_URL, "page-1.html")
        await fetch_page(session, first_page_url)

    # Save to JSON
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)

    end = time.time()
    print(f"Scraped {len(books)} books")
    print(f"Duration: {end - start:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
