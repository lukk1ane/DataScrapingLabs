import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import time


def scrape_page(page_num):
    url = f"https://quotes.toscrape.com/page/{page_num}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            quotes = soup.find_all('div', class_='quote')
            return len(quotes)
        return 0
    except Exception as e:
        print(f"Error scraping page {page_num}: {e}")
        return 0


def sequential_scraping(pages):
    start_time = time.time()
    results = []
    for page in range(1, pages + 1):
        results.append(scrape_page(page))
    total_time = time.time() - start_time
    avg_time = total_time / pages
    print(f"Sequential scraping:")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per page: {avg_time:.2f} seconds")
    print(f"Total quotes scraped: {sum(results)}\n")
    return total_time, avg_time


def threaded_scraping(pages, num_threads=5):
    start_time = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(scrape_page, range(1, pages + 1)))
    total_time = time.time() - start_time
    avg_time = total_time / pages
    print(f"Threaded scraping ({num_threads} threads):")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per page: {avg_time:.2f} seconds")
    print(f"Total quotes scraped: {sum(results)}\n")
    return total_time, avg_time


def multiprocess_scraping(pages, num_processes=5):
    start_time = time.time()
    with Pool(num_processes) as pool:
        results = pool.map(scrape_page, range(1, pages + 1))
    total_time = time.time() - start_time
    avg_time = total_time / pages
    print(f"Multiprocess scraping ({num_processes} processes):")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time per page: {avg_time:.2f} seconds")
    print(f"Total quotes scraped: {sum(results)}\n")
    return total_time, avg_time


if __name__ == "__main__":
    pages_to_scrape = 10

    print("Starting scraping comparison...\n")
    seq_time, seq_avg = sequential_scraping(pages_to_scrape)
    thread_time, thread_avg = threaded_scraping(pages_to_scrape)
    process_time, process_avg = multiprocess_scraping(pages_to_scrape)

    print("\nPerformance Comparison:")
    print(f"Sequential was {thread_time / seq_time:.1f}x slower than Threaded")
    print(f"Sequential was {process_time / seq_time:.1f}x slower than Multiprocess")
    print(
        f"Threaded was {process_time / thread_time:.1f}x {'slower' if process_time > thread_time else 'faster'} than Multiprocess")