import requests
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import time

BASE_URL = 'http://quotes.toscrape.com/page/{}/'
PAGES = list(range(1, 11))


def fetch_page(page):
    url = BASE_URL.format(page)
    response = requests.get(url)
    return response.text


def sequential_scrape():
    start = time.time()
    for page in PAGES:
        fetch_page(page)
    end = time.time()
    total = end - start
    print(f"Sequential: Total time: {total:.2f}s, Avg per page: {total/len(PAGES):.2f}s")


def threaded_scrape():
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        list(executor.map(fetch_page, PAGES))
    end = time.time()
    total = end - start
    print(f"Threaded: Total time: {total:.2f}s, Avg per page: {total/len(PAGES):.2f}s")


def multiprocessing_scrape():
    start = time.time()
    with Pool(processes=5) as pool:
        pool.map(fetch_page, PAGES)
    end = time.time()
    total = end - start
    print(f"Multiprocessing: Total time: {total:.2f}s, Avg per page: {total/len(PAGES):.2f}s")


def main():
    print("Scraping first 10 pages of quotes.toscrape.com...")
    sequential_scrape()
    threaded_scrape()
    multiprocessing_scrape()


if __name__ == "__main__":
    main() 