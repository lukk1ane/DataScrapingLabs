import threading
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count

thread_local = threading.local()
BASE_URL = "http://quotes.toscrape.com/page/{}/"

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

def scrape_page(page_number):
    session = get_session()
    url = BASE_URL.format(page_number)
    with session.get(url) as response:
        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("span", class_="text")
        return [quote.text for quote in quotes]
def sequential_scraping():
    print("Starting sequential scraping...")
    start = time.perf_counter()
    results = []
    for i in range(1, 11):
        results.append(scrape_page(i))
    end = time.perf_counter()
    duration = end - start
    print(f"Sequential scraping duration: {duration}, average page: {duration/10}")
    return results

def threaded_scraping():
    print("Starting optimized threaded scraping...")
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(scrape_page, range(1, 11)))
        # print(results)
    end = time.perf_counter()
    duration = end - start
    print(f'threaded scrapping scrapping duration: {duration}, average page: {duration/10}')
# Multiprocessing scraping

def multiprocessing_scraping():
    print("Starting multiprocessing scraping...")
    start = time.perf_counter()
    with Pool(processes=5) as pool:
        results = pool.map(scrape_page, range(1, 11))
    end = time.perf_counter()
    duration = end - start
    print(f"Multiprocessing Total time: {duration}, average page: {duration/10}")
    return results

if __name__ == "__main__":
    sequential_scraping()
    threaded_scraping()
    multiprocessing_scraping()

