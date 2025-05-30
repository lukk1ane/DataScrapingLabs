import requests
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
def fetch_page(url):
    response = requests.get(url)
    return response.text

def sequential_scraping():
    start = time.time()
    for i in range(1, 11):
        fetch_page(f"http://quotes.toscrape.com/page/{i}/")
    duration = time.time() - start
    print(f"Sequential - Total Time: {duration:.2f}s, Avg per page: {duration / 10:.2f}s")
def threaded_scraping():
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        urls = [f"http://quotes.toscrape.com/page/{i}/" for i in range(1, 11)]
        executor.map(fetch_page, urls)
    duration = time.time() - start
    print(f"Threaded - Total Time: {duration:.2f}s, Avg per page: {duration / 10:.2f}s")
def multiprocessing_scraping():
    start = time.time()
    with Pool(processes=5) as pool:
        urls = [f"http://quotes.toscrape.com/page/{i}/" for i in range(1, 11)]
        pool.map(fetch_page, urls)
    duration = time.time() - start
    print(f"Multiprocessing - Total Time: {duration:.2f}s, Avg per page: {duration / 10:.2f}s")
if __name__ == "__main__":
    sequential_scraping()
    threaded_scraping()
    multiprocessing_scraping()
