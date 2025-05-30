import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import asyncio
import aiohttp
import time
import json
import os

# -------------------
# Task 1 - Quotes to Scrape
# -------------------

BASE_QUOTES_URL = "http://quotes.toscrape.com/page/{}/"

def fetch_page_quotes(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return [quote.text.strip() for quote in soup.select(".quote span.text")]
    return []

def sequential_scrape():
    start = time.time()
    all_quotes = []
    for i in range(1, 11):
        url = BASE_QUOTES_URL.format(i)
        quotes = fetch_page_quotes(url)
        all_quotes.extend(quotes)
    duration = time.time() - start
    print("\nSequential Scraping")
    print(f"Total Time: {duration:.2f}s, Average per page: {duration / 10:.2f}s")

def threaded_scrape():
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        urls = [BASE_QUOTES_URL.format(i) for i in range(1, 11)]
        results = executor.map(fetch_page_quotes, urls)
    all_quotes = [quote for result in results for quote in result]
    duration = time.time() - start
    print("\nThreaded Scraping")
    print(f"Total Time: {duration:.2f}s, Average per page: {duration / 10:.2f}s")

def multiprocessing_scrape():
    start = time.time()
    with Pool(processes=5) as pool:
        urls = [BASE_QUOTES_URL.format(i) for i in range(1, 11)]
        results = pool.map(fetch_page_quotes, urls)
    all_quotes = [quote for result in results for quote in result]
    duration = time.time() - start
    print("\nMultiprocessing Scraping")
    print(f"Total Time: {duration:.2f}s, Average per page: {duration / 10:.2f}s")

# -------------------
# Task 2 - Books to Scrape (Async)
# -------------------

BOOKS_URL = "https://books.toscrape.com/catalogue/page-{}.html"
BOOK_BASE_URL = "https://books.toscrape.com/catalogue/"

async def fetch_html(session, url, sem):
    async with sem:
        async with session.get(url) as response:
            return await response.text()

async def fetch_book_data(session, url, sem):
    html = await fetch_html(session, url, sem)
    soup = BeautifulSoup(html, "html.parser")
    books = soup.select(".product_pod")
    book_data = []
    for book in books:
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text.strip()
        relative_url = book.h3.a["href"]
        full_url = BOOK_BASE_URL + relative_url
        book_data.append({
            "title": title,
            "price": price,
            "url": full_url
        })
    return book_data

async def get_total_pages(session, sem):
    html = await fetch_html(session, BOOKS_URL.format(1), sem)
    soup = BeautifulSoup(html, "html.parser")
    pager = soup.select_one(".current")
    if pager:
        return int(pager.text.strip().split()[-1])
    return 1

async def async_scrape_books():
    start = time.time()
    sem = asyncio.Semaphore(5)  # Rate limit: 5 requests per second
    async with aiohttp.ClientSession() as session:
        total_pages = await get_total_pages(session, sem)
        tasks = [fetch_book_data(session, BOOKS_URL.format(i), sem) for i in range(1, total_pages + 1)]
        all_books = await asyncio.gather(*tasks)
    books_flat = [book for sublist in all_books for book in sublist]
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(books_flat, f, ensure_ascii=False, indent=2)
    duration = time.time() - start
    print(f"\nAsync Scraping of Books - Total Time: {duration:.2f}s")
    print(f"Total books scraped: {len(books_flat)}")

# -------------------
# Main
# -------------------

if __name__ == "__main__":
    print("Starting Task 1: Quotes to Scrape")
    sequential_scrape()
    threaded_scrape()
    multiprocessing_scrape()

    print("\nStarting Task 2: Books to Scrape (Async)")
    asyncio.run(async_scrape_books())
