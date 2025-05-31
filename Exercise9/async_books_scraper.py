import asyncio
import aiohttp
import certifi
import ssl
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_SITE   = "https://books.toscrape.com/"
CATALOG_URL = urljoin(BASE_SITE, "catalogue/page-{}.html")


async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    """
    Fetch the page’s HTML, using certifi’s CA bundle to verify TLS.
    """
    # Create an SSL context that loads certifi’s root CAs
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Pass that context into session.get(...)
    async with session.get(url, ssl=ssl_context) as response:
        response.raise_for_status()
        return await response.text()


async def parse_num_pages(session: aiohttp.ClientSession) -> int:
    """
    Download page 1, parse the “Page 1 of N” text, and return N.
    """
    first_html = await fetch(session, CATALOG_URL.format(1))
    soup = BeautifulSoup(first_html, "html.parser")
    pager = soup.find("li", class_="current")
    if pager:
        # e.g. “Page 1 of 50”
        text = pager.get_text(strip=True)
        parts = text.split()
        if "of" in parts:
            return int(parts[-1])
    return 1


async def parse_book_list(html: str) -> list[dict]:
    """
    Given a catalogue‐page HTML, extract a list of books (title, price, product URL).
    """
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for item in soup.select("article.product_pod"):
        a_tag = item.find("h3").find("a")
        title = a_tag["title"].strip()
        price = item.find("p", class_="price_color").get_text(strip=True)
        relative_url = a_tag["href"]
        product_url = urljoin(BASE_SITE + "catalogue/", relative_url)
        results.append({
            "title": title,
            "price": price,
            "product_page_url": product_url
        })
    return results


async def worker(name: int,
                 queue: asyncio.Queue,
                 session: aiohttp.ClientSession,
                 results: list):
    """
    Pull URLs from the queue, fetch & parse each one, then sleep 1 sec to rate-limit.
    """
    while True:
        try:
            page_url = queue.get_nowait()
        except asyncio.QueueEmpty:
            break

        try:
            html = await fetch(session, page_url)
            books = await parse_book_list(html)
            results.extend(books)
            print(f"[Worker {name}] scraped {page_url} → {len(books)} books")
        except Exception as e:
            print(f"[Worker {name}] ERROR {page_url}: {e}")
        finally:
            queue.task_done()

        # Enforce ~1 second delay so that 5 workers = 5 req/sec
        await asyncio.sleep(1)


async def main():
    start_time = time.perf_counter()

    # We don’t need a special connector here—fetch() supplies ssl_context each time.
    async with aiohttp.ClientSession() as session:
        total_pages = await parse_num_pages(session)
        print(f"Discovered total pages: {total_pages}")

        queue = asyncio.Queue()
        for i in range(1, total_pages + 1):
            queue.put_nowait(CATALOG_URL.format(i))

        results = []
        workers = [
            asyncio.create_task(worker(i + 1, queue, session, results))
            for i in range(5)
        ]

        await queue.join()
        for w in workers:
            w.cancel()
        await asyncio.gather(*workers, return_exceptions=True)

    # Write out the JSON
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    elapsed = time.perf_counter() - start_time
    print(f"\nTotal books scraped: {len(results)}")
    print("Saved to books.json")
    print(f"Total duration: {elapsed:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
