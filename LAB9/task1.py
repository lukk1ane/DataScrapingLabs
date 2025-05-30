"""
Task 1: Comparison of Sequential, Threaded, and Multiprocessing Scraping
Scrapes the first 10 pages of quotes from http://quotes.toscrape.com
"""

import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp
from typing import List, Dict, Any


def scrape_page(page_num: int) -> Dict[str, Any]:
    """
    Scrape a single page of quotes and return the data
    
    Args:
        page_num: Page number to scrape
        
    Returns:
        Dictionary containing page data and metadata
    """
    url = f"http://quotes.toscrape.com/page/{page_num}/"
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        quotes = []
        
        for quote in soup.find_all('div', class_='quote'):
            text = quote.find('span', class_='text').get_text(strip=True)
            author = quote.find('small', class_='author').get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]
            
            quotes.append({
                'text': text,
                'author': author,
                'tags': tags
            })
        
        end_time = time.time()
        
        return {
            'page': page_num,
            'quotes': quotes,
            'request_time': end_time - start_time,
            'quote_count': len(quotes)
        }
    
    except Exception as e:
        return {
            'page': page_num,
            'error': str(e),
            'quotes': [],
            'request_time': 0,
            'quote_count': 0
        }


def sequential_scraping(pages: List[int]) -> List[Dict[str, Any]]:
    """
    Scrape pages sequentially
    
    Args:
        pages: List of page numbers to scrape
        
    Returns:
        List of scraped page data
    """
    print("Starting sequential scraping...")
    start_time = time.time()
    
    results = []
    for page_num in pages:
        result = scrape_page(page_num)
        results.append(result)
        print(f"  Scraped page {page_num}: {result['quote_count']} quotes")
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / len(pages)
    
    print(f"Sequential scraping completed:")
    print(f"  Total time: {total_time:.2f} seconds")
    print(f"  Average time per page: {avg_time:.2f} seconds")
    print(f"  Total quotes: {sum(r['quote_count'] for r in results)}")
    print()
    
    return results


def threaded_scraping(pages: List[int], max_workers: int = 5) -> List[Dict[str, Any]]:
    """
    Scrape pages using ThreadPoolExecutor
    
    Args:
        pages: List of page numbers to scrape
        max_workers: Number of threads to use
        
    Returns:
        List of scraped page data
    """
    print(f"Starting threaded scraping with {max_workers} threads...")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(scrape_page, pages))
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / len(pages)
    
    print(f"Threaded scraping completed:")
    print(f"  Total time: {total_time:.2f} seconds")
    print(f"  Average time per page: {avg_time:.2f} seconds")
    print(f"  Total quotes: {sum(r['quote_count'] for r in results)}")
    print()
    
    return results


def multiprocessing_scraping(pages: List[int], processes: int = 5) -> List[Dict[str, Any]]:
    """
    Scrape pages using multiprocessing.Pool
    
    Args:
        pages: List of page numbers to scrape
        processes: Number of processes to use
        
    Returns:
        List of scraped page data
    """
    print(f"Starting multiprocessing scraping with {processes} processes...")
    start_time = time.time()
    
    with mp.Pool(processes=processes) as pool:
        results = pool.map(scrape_page, pages)
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / len(pages)
    
    print(f"Multiprocessing scraping completed:")
    print(f"  Total time: {total_time:.2f} seconds")
    print(f"  Average time per page: {avg_time:.2f} seconds")
    print(f"  Total quotes: {sum(r['quote_count'] for r in results)}")
    print()
    
    return results


def main():
    """
    Main function to run all three scraping approaches and compare performance
    """
    pages_to_scrape = list(range(1, 11))  # First 10 pages
    
    print("=" * 60)
    print("QUOTES SCRAPING PERFORMANCE COMPARISON")
    print("=" * 60)
    print(f"Scraping {len(pages_to_scrape)} pages from quotes.toscrape.com")
    print()
    
    # Sequential scraping
    sequential_results = sequential_scraping(pages_to_scrape)
    
    # Threaded scraping
    threaded_results = threaded_scraping(pages_to_scrape, max_workers=5)
    
    # Multiprocessing scraping
    multiprocessing_results = multiprocessing_scraping(pages_to_scrape, processes=5)
    
    # Summary comparison
    print("=" * 60)
    print("PERFORMANCE SUMMARY")
    print("=" * 60)
    
    # Calculate total times
    sequential_times = [r['request_time'] for r in sequential_results if 'request_time' in r]
    threaded_times = [r['request_time'] for r in threaded_results if 'request_time' in r]
    multiprocessing_times = [r['request_time'] for r in multiprocessing_results if 'request_time' in r]
    
    print(f"Sequential:      {sum(sequential_times):.2f}s total, {sum(sequential_times)/len(sequential_times):.2f}s avg per request")
    print(f"Threaded (5):    {sum(threaded_times):.2f}s total, {sum(threaded_times)/len(threaded_times):.2f}s avg per request")
    print(f"Multiprocess(5): {sum(multiprocessing_times):.2f}s total, {sum(multiprocessing_times)/len(multiprocessing_times):.2f}s avg per request")
    
    # Calculate speedup
    sequential_total = sum(sequential_times)
    threaded_total = sum(threaded_times)
    multiprocessing_total = sum(multiprocessing_times)
    
    print()
    print("SPEEDUP COMPARISON:")
    print(f"Threaded vs Sequential: {sequential_total/threaded_total:.2f}x faster")
    print(f"Multiprocessing vs Sequential: {sequential_total/multiprocessing_total:.2f}x faster")
    print(f"Multiprocessing vs Threaded: {threaded_total/multiprocessing_total:.2f}x faster")


if __name__ == "__main__":
    main() 