# File: compare_scrapers.py

import time
import requests
import concurrent.futures
import multiprocessing

BASE_URL = "http://quotes.toscrape.com/page/{}/"

def fetch_page(page_num: int) -> str:
    """
    Fetches the HTML for a single page of quotes.
    Returns the page's HTML text. Raises for HTTP errors if request fails.
    """
    url = BASE_URL.format(page_num)
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def sequential_scrape(page_nums):
    """
    Sequentially fetch each page in page_nums one by one.
    Returns a tuple: (total_time, list_of_HTMLs).
    """
    start = time.perf_counter()
    results = []
    for num in page_nums:
        html = fetch_page(num)
        results.append(html)
    end = time.perf_counter()
    total_time = end - start
    return total_time, results


def threaded_scrape(page_nums, max_workers=5):
    """
    Use ThreadPoolExecutor to fetch pages concurrently with a pool of threads.
    Returns: (total_time, list_of_HTMLs_in_order_of_page_nums).
    """
    start = time.perf_counter()
    results = [None] * len(page_nums)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks
        future_to_index = {
            executor.submit(fetch_page, page_num): idx
            for idx, page_num in enumerate(page_nums)
        }
        for future in concurrent.futures.as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                results[idx] = future.result()
            except Exception as exc:
                print(f"Thread fetching page {page_nums[idx]} raised: {exc}")
                results[idx] = None
    end = time.perf_counter()
    total_time = end - start
    return total_time, results


def multiprocessing_scrape(page_nums, pool_size=5):
    """
    Use multiprocessing.Pool to fetch pages concurrently with multiple processes.
    Returns: (total_time, list_of_HTMLs_in_order_of_page_nums).
    """
    start = time.perf_counter()
    with multiprocessing.Pool(processes=pool_size) as pool:
        results = pool.map(fetch_page, page_nums)
    end = time.perf_counter()
    total_time = end - start
    return total_time, results


def main():
    # Define which pages to scrape (1 through 10)
    page_numbers = list(range(1, 11))

    print("=== Sequential Scraping ===")
    total_seq, _ = sequential_scrape(page_numbers)
    avg_seq = total_seq / len(page_numbers)
    print(f"Total time (sequential): {total_seq:.2f} seconds")
    print(f"Average time per page: {avg_seq:.2f} seconds\n")

    print("=== Threaded Scraping (5 threads) ===")
    total_thr, _ = threaded_scrape(page_numbers, max_workers=5)
    avg_thr = total_thr / len(page_numbers)
    print(f"Total time (threaded): {total_thr:.2f} seconds")
    print(f"Average time per page: {avg_thr:.2f} seconds\n")

    print("=== Multiprocessing Scraping (5 processes) ===")
    total_mp, _ = multiprocessing_scrape(page_numbers, pool_size=5)
    avg_mp = total_mp / len(page_numbers)
    print(f"Total time (multiprocessing): {total_mp:.2f} seconds")
    print(f"Average time per page: {avg_mp:.2f} seconds\n")


if __name__ == "__main__":
    main()
