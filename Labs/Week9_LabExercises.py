
import requests
import time
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

BASE_QUOTE_URL = "http://quotes.toscrape.com/page/{}/"
BASE_BOOK_URL = "https://books.toscrape.com/"


# TASK 1:

def fetch_quotes_page(page):
    response = requests.get(BASE_QUOTE_URL.format(page))
    return response.text

def parse_quotes(html):
    soup = BeautifulSoup(html, "html.parser")
    return [quote.text.strip() for quote in soup.select(".quote span.text")]

def sequential_scraping():
    start = time.time()
    all_quotes = []
    for i in range(1, 11):
        html = fetch_quotes_page(i)
        quotes = parse_quotes(html)
        all_quotes.extend(quotes)
    end = time.time()
    print(f"Sequential scraping: {len(all_quotes)} quotes")
    print(f"Total time: {end - start:.2f} seconds")
    print(f"Average time per request: {(end - start)/10:.2f} seconds\n")

def threaded_scraping():
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        html_pages = list(executor.map(fetch_quotes_page, range(1, 11)))
    all_quotes = []
    for html in html_pages:
        quotes = parse_quotes(html)
        all_quotes.extend(quotes)
    end = time.time()
    print(f"Threaded scraping: {len(all_quotes)} quotes")
    print(f"Total time: {end - start:.2f} seconds")
    print(f"Average time per request: {(end - start)/10:.2f} seconds\n")

def multiprocessing_scraping():
    start = time.time()
    with Pool(processes=5) as pool:
        html_pages = pool.map(fetch_quotes_page, range(1, 11))
    all_quotes = []
    for html in html_pages:
        quotes = parse_quotes(html)
        all_quotes.extend(quotes)
    end = time.time()
    print(f"Multiprocessing scraping: {len(all_quotes)} quotes")
    print(f"Total time: {end - start:.2f} seconds")
    print(f"Average time per request: {(end - start)/10:.2f} seconds\n")


# TASK 2:


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_all_books():
    start = time.time()
    connector = aiohttp.TCPConnector(limit_per_host=5)
    async with aiohttp.ClientSession(connector=connector) as session:
        first_page = await fetch(session, BASE_BOOK_URL)
        soup = BeautifulSoup(first_page, "html.parser")
        if soup.select(".pager .current"):
            last_page = int(soup.select_one(".pager .current").text.strip().split()[-1])
        else:
            last_page = 1
        urls = [f"{BASE_BOOK_URL}catalogue/page-{i}.html" for i in range(1, last_page+1)]

        tasks = [asyncio.create_task(fetch(session, url)) for url in urls]
        responses = await asyncio.gather(*tasks)

        books = []
        for html in responses:
            soup = BeautifulSoup(html, "html.parser")
            for book in soup.select(".product_pod"):
                title = book.h3.a["title"]
                price = book.select_one(".price_color").text.strip()
                relative_url = book.h3.a["href"]
                product_url = BASE_BOOK_URL + "catalogue/" + relative_url
                books.append({
                    "title": title,
                    "price": price,
                    "url": product_url
                })

    with open("async_books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)

    end = time.time()
    print(f"Async scraping: {len(books)} books")
    print(f"Total time: {end - start:.2f} seconds\n")

if __name__ == "__main__":
    print("Task 1:")
    sequential_scraping()
    threaded_scraping()
    multiprocessing_scraping()
    print("Task 2:")
    asyncio.run(get_all_books())
