import requests
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

BASE_URL = "http://quotes.toscrape.com/page/{}/"
NUM_PAGES = 10


def fetch_page(page_number):
    url = BASE_URL.format(page_number)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")
        return len(quotes)
    else:
        return 0


# Sequential scraping
def sequential_scraping():
    print("\n--- Sequential Scraping ---")
    start = time.time()
    results = []
    for i in range(1, NUM_PAGES + 1):
        results.append(fetch_page(i))
    end = time.time()
    total_time = end - start
    print(f"Total Time: {total_time:.2f}s")
    print(f"Average Time per Page: {total_time / NUM_PAGES:.2f}s")


# Threaded scraping
def threaded_scraping():
    print("\n--- Threaded Scraping (5 threads) ---")
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch_page, range(1, NUM_PAGES + 1)))
    end = time.time()
    total_time = end - start
    print(f"Total Time: {total_time:.2f}s")
    print(f"Average Time per Page: {total_time / NUM_PAGES:.2f}s")


# Multiprocessing scraping
def multiprocessing_scraping():
    print("\n--- Multiprocessing Scraping (5 processes) ---")
    start = time.time()
    with Pool(processes=5) as pool:
        results = pool.map(fetch_page, range(1, NUM_PAGES + 1))
    end = time.time()
    total_time = end - start
    print(f"Total Time: {total_time:.2f}s")
    print(f"Average Time per Page: {total_time / NUM_PAGES:.2f}s")


if __name__ == "__main__":
    sequential_scraping()
    threaded_scraping()
    multiprocessing_scraping()
