# exercise9.py
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from bs4 import BeautifulSoup

import asyncio
import aiohttp
import json

#
# Task 1: Scrape the first 10 pages of quotes.toscrape.com
#

BASE_QUOTES_URL = 'http://quotes.toscrape.com/page/{}/'

def fetch_quotes_page(page_num: int) -> str:
    url = BASE_QUOTES_URL.format(page_num)
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

def measure_sequential(pages=10):
    start = time.perf_counter()
    for i in range(1, pages + 1):
        fetch_quotes_page(i)
    total = time.perf_counter() - start
    print(f"[Sequential]        total = {total:.2f}s, avg = {total/pages:.2f}s")

def measure_threaded(pages=10, workers=5):
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(fetch_quotes_page, range(1, pages + 1))
    total = time.perf_counter() - start
    print(f"[ThreadPool ({workers})] total = {total:.2f}s, avg = {total/pages:.2f}s")

def measure_multiprocess(pages=10, processes=5):
    start = time.perf_counter()
    with Pool(processes) as pool:
        pool.map(fetch_quotes_page, range(1, pages + 1))
    total = time.perf_counter() - start
    print(f"[ProcessPool({processes})] total = {total:.2f}s, avg = {total/pages:.2f}s")

def task1():
    print("=== Task 1: Quotes.toscrape.com Performance ===")
    measure_sequential()
    measure_threaded()
    measure_multiprocess()
    print()

#
# Task 2: Asynchronous scraping of books.toscrape.com
#

BASE_BOOKS_URL    = 'http://books.toscrape.com/'
CATALOGUE_FORMAT = BASE_BOOKS_URL + 'catalogue/page-{}.html'

class RateLimiter:
    def __init__(self, max_calls: int, period: float = 1.0):
        self.max_calls = max_calls
        self.period    = period
        self.tokens    = max_calls
        self.lock      = asyncio.Lock()
        asyncio.create_task(self._refill_loop())

    async def _refill_loop(self):
        while True:
            await asyncio.sleep(self.period)
            async with self.lock:
                self.tokens = self.max_calls

    async def acquire(self):
        while True:
            async with self.lock:
                if self.tokens > 0:
                    self.tokens -= 1
                    return
            await asyncio.sleep(0.01)

async def fetch_book_data(session: aiohttp.ClientSession, url: str, limiter: RateLimiter):
    await limiter.acquire()
    async with session.get(url) as resp:
        resp.raise_for_status()
        html = await resp.text()
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('.product_main h1').text.strip()
    price = soup.select_one('.product_main .price_color').text.strip()
    return {'title': title, 'price': price, 'url': url}

async def task2():
    print("=== Task 2: Async scrape books.toscrape.com ===")
    t_start = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_BOOKS_URL) as resp:
            resp.raise_for_status()
            text = await resp.text()
        soup = BeautifulSoup(text, 'html.parser')
        pager = soup.select_one('.current').text.strip()   # e.g. "Page 1 of 50"
        total_pages = int(pager.split()[-1])

    limiter = RateLimiter(max_calls=5, period=1.0)
    tasks = []

    async with aiohttp.ClientSession() as session:
        for page in range(1, total_pages + 1):
            page_url = CATALOGUE_FORMAT.format(page)
            await limiter.acquire()
            async with session.get(page_url) as resp:
                resp.raise_for_status()
                page_html = await resp.text()
            page_soup = BeautifulSoup(page_html, 'html.parser')
            for a in page_soup.select('.product_pod h3 a'):
                href = a['href']  # e.g. "../../../a-light-in-the-attic_1000/index.html"
                book_url = BASE_BOOKS_URL + 'catalogue/' + href.split('../../../')[-1]
                tasks.append(fetch_book_data(session, book_url, limiter))

        results = await asyncio.gather(*tasks)

    with open('books.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    t_total = time.perf_counter() - t_start
    print(f"Scraped {len(results)} books in {t_total:.2f}s → saved to books.json\n")

if __name__ == '__main__':
    task1()
    asyncio.run(task2())
