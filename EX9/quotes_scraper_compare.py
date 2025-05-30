import requests
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

BASE_URL = "http://quotes.toscrape.com/page/{}/"

def fetch_page(page_num):
    response = requests.get(BASE_URL.format(page_num))
    return response.status_code, page_num

def run_sequential():
    start = time.time()
    results = []
    for i in range(1, 11):
        results.append(fetch_page(i))
    end = time.time()
    print("\n[Sequential]")
    print("Total time:", round(end - start, 2), "seconds")
    print("Average time per request:", round((end - start)/10, 2), "seconds")

def run_threading():
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch_page, range(1, 11)))
    end = time.time()
    print("\n[Threading - 5 threads]")
    print("Total time:", round(end - start, 2), "seconds")
    print("Average time per request:", round((end - start)/10, 2), "seconds")

def run_multiprocessing():
    start = time.time()
    with Pool(processes=5) as pool:
        results = pool.map(fetch_page, range(1, 11))
    end = time.time()
    print("\n[Multiprocessing - 5 processes]")
    print("Total time:", round(end - start, 2), "seconds")
    print("Average time per request:", round((end - start)/10, 2), "seconds")

if __name__ == "__main__":
    run_sequential()
    run_threading()
    run_multiprocessing()
