import requests
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, freeze_support
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

try:
    from aiolimiter import AsyncLimiter
except ImportError:
    print("Error: 'aiolimiter' package not found. Please install it by running: pip install aiolimiter")
    print("Task 2 cannot be executed without 'aiolimiter'.")
    AsyncLimiter = None 


BASE_URL_QUOTES = "http://quotes.toscrape.com"
NUM_PAGES_QUOTES = 10
def global_worker_fetch_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return len(response.content)  
    except requests.RequestException:
        return 0 

# task 1
def main_task1():
    urls_to_scrape = [f"{BASE_URL_QUOTES}/page/{i}/" for i in range(1, NUM_PAGES_QUOTES + 1)]

    print("--- Task 1: Comparing Scraping Methods ---")

    # Sequential Scraping
    print("\nSequential Scraping:")
    start_time = time.perf_counter()
    results_seq = []
    for url in urls_to_scrape:
        results_seq.append(global_worker_fetch_url(url))
    end_time = time.perf_counter()
    total_time_seq = end_time - start_time
    avg_time_seq = total_time_seq / NUM_PAGES_QUOTES if NUM_PAGES_QUOTES > 0 else 0
    print(f"Total execution time: {total_time_seq:.4f} seconds")
    print(f"Average time per page: {avg_time_seq:.4f} seconds")

    # Threaded Scraping
    print("\nThreaded Scraping (5 threads):")
    start_time = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        results_threaded = list(executor.map(global_worker_fetch_url, urls_to_scrape))
    end_time = time.perf_counter()
    total_time_threaded = end_time - start_time
    avg_time_threaded = total_time_threaded / NUM_PAGES_QUOTES if NUM_PAGES_QUOTES > 0 else 0
    print(f"Total execution time: {total_time_threaded:.4f} seconds")
    print(f"Average time per page: {avg_time_threaded:.4f} seconds")

    # Multiprocessing Scraping
    print("\nMultiprocessing Scraping (5 processes):")
    start_time = time.perf_counter()
    with Pool(processes=5) as pool:
        results_mp = pool.map(global_worker_fetch_url, urls_to_scrape)
    end_time = time.perf_counter()
    total_time_mp = end_time - start_time
    avg_time_mp = total_time_mp / NUM_PAGES_QUOTES if NUM_PAGES_QUOTES > 0 else 0
    print(f"Total execution time: {total_time_mp:.4f} seconds")
    print(f"Average time per page: {avg_time_mp:.4f} seconds")


BASE_URL_BOOKS = "https://books.toscrape.com/"
MAX_REQUESTS_PER_SECOND_BOOKS = 5
OUTPUT_JSON_FILE = "books_data.json"

async def fetch_html_task2(session, url, limiter):
    if limiter is None: 
        raise RuntimeError("AsyncLimiter is not available. Cannot proceed with fetch_html_task2.")
    
    await limiter.acquire()
    try:
        async with session.get(url, timeout=15) as response:
            response.raise_for_status()
            return await response.text()
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return None

def parse_books_from_listing_page_task2(html_content, current_page_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    books_data = []
    
    book_articles = soup.select('article.product_pod')
    for article in book_articles:
        title_tag = article.select_one('h3 a')
        title = title_tag['title'] if title_tag and 'title' in title_tag.attrs else 'N/A'
        relative_book_url = title_tag['href'] if title_tag and 'href' in title_tag.attrs else None
        
        product_url = None
        if relative_book_url:
            product_url = urljoin(current_page_url, relative_book_url)

        price_tag = article.select_one('p.price_color')
        price = price_tag.text.strip() if price_tag else 'N/A'
        
        if product_url: 
             books_data.append({
                'title': title,
                'price': price,
                'url': product_url
            })
    
    next_page_tag = soup.select_one('li.next a')
    next_page_full_url = None
    if next_page_tag and 'href' in next_page_tag.attrs:
        next_page_relative_url = next_page_tag['href']
        next_page_full_url = urljoin(current_page_url, next_page_relative_url)
        
    return books_data, next_page_full_url

# task 2
async def main_task2():
    if AsyncLimiter is None:
        print("Skipping Task 2 because 'aiolimiter' is not installed.")
        return

    print("\n--- Task 2: Asynchronous Book Scraping ---")
    start_time_task2 = time.perf_counter()
    
    all_books = []
    limiter = AsyncLimiter(MAX_REQUESTS_PER_SECOND_BOOKS, 1) 

    async with aiohttp.ClientSession() as session:
        current_url = urljoin(BASE_URL_BOOKS, "catalogue/page-1.html")
        page_count = 0
        
        while current_url:
            page_count += 1
            html_content = await fetch_html_task2(session, current_url, limiter)
            if not html_content:
                break 

            books_on_page, next_page_url = parse_books_from_listing_page_task2(html_content, current_url)
            all_books.extend(books_on_page)
            
            current_url = next_page_url

    with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_books, f, indent=4, ensure_ascii=False)
    
    end_time_task2 = time.perf_counter()
    task_duration = end_time_task2 - start_time_task2
    
    print(f"Scraped {len(all_books)} books from {page_count} pages.")
    print(f"Results saved to {OUTPUT_JSON_FILE}")
    print(f"Total task duration: {task_duration:.4f} seconds")

if __name__ == '__main__':
    freeze_support() 
    
    print("Executing Task 1...")
    main_task1()
    
    print("\nExecuting Task 2...")
    asyncio.run(main_task2())
