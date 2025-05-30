import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

class QuoteScraper:
    def __init__(self, base_url="https://quotes.toscrape.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def scrape_page(self, page_num):
        try:
            url = f"{self.base_url}/page/{page_num}/" if page_num > 1 else self.base_url
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            quotes = []

            for quote_div in soup.find_all('div', class_='quote'):
                text = quote_div.find('span', class_='text').get_text(strip=True)
                author = quote_div.find('small', class_='author').get_text(strip=True)
                tags = [tag.get_text(strip=True) for tag in quote_div.find_all('a', class_='tag')]

                quotes.append({
                    'text': text,
                    'author': author,
                    'tags': tags,
                    'page': page_num
                })

            print(f"✓ Scraped page {page_num}: {len(quotes)} quotes")
            return quotes

        except Exception as e:
            print(f"✗ Error scraping page {page_num}: {str(e)}")
            return []


def scrape_sequential(pages=10):
    """Sequential scraping approach"""
    print("\n" + "=" * 50)
    print("SEQUENTIAL SCRAPING")
    print("=" * 50)

    scraper = QuoteScraper()
    all_quotes = []

    start_time = time.time()

    for page in range(1, pages + 1):
        page_quotes = scraper.scrape_page(page)
        all_quotes.extend(page_quotes)

    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / pages

    print(f"\nResults:")
    print(f"Total quotes scraped: {len(all_quotes)}")
    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"Average time per page: {avg_time:.2f} seconds")

    return all_quotes, total_time, avg_time


def scrape_threaded(pages=10, max_workers=5):
    """Threaded scraping using ThreadPoolExecutor"""
    print("\n" + "=" * 50)
    print(f"THREADED SCRAPING ({max_workers} threads)")
    print("=" * 50)

    scraper = QuoteScraper()
    all_quotes = []

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_page = {
            executor.submit(scraper.scrape_page, page): page
            for page in range(1, pages + 1)
        }

        for future in future_to_page:
            page_quotes = future.result()
            all_quotes.extend(page_quotes)

    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / pages

    print(f"\nResults:")
    print(f"Total quotes scraped: {len(all_quotes)}")
    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"Average time per page: {avg_time:.2f} seconds")

    return all_quotes, total_time, avg_time


def scrape_single_page_mp(page_num):
    """Helper function for multiprocessing - creates its own scraper instance"""
    scraper = QuoteScraper()
    return scraper.scrape_page(page_num)


def scrape_multiprocessing(pages=10, processes=5):
    print("\n" + "=" * 50)
    print(f"MULTIPROCESSING SCRAPING ({processes} processes)")
    print("=" * 50)

    all_quotes = []

    start_time = time.time()

    with Pool(processes=processes) as pool:
        results = pool.map(scrape_single_page_mp, range(1, pages + 1))

        for page_quotes in results:
            all_quotes.extend(page_quotes)

    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / pages

    print(f"\nResults:")
    print(f"Total quotes scraped: {len(all_quotes)}")
    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"Average time per page: {avg_time:.2f} seconds")

    return all_quotes, total_time, avg_time


def compare_approaches():
    """Compare all three scraping approaches"""
    print("WEB SCRAPING PERFORMANCE COMPARISON")
    print("Scraping first 10 pages from https://quotes.toscrape.com")
    print("=" * 70)

    pages_to_scrape = 10
    results = {}

    try:
        quotes_seq, time_seq, avg_seq = scrape_sequential(pages_to_scrape)
        results['Sequential'] = {'quotes': len(quotes_seq), 'total_time': time_seq, 'avg_time': avg_seq}
    except Exception as e:
        print(f"Sequential scraping failed: {e}")
        results['Sequential'] = None

    time.sleep(1)

    try:
        quotes_thread, time_thread, avg_thread = scrape_threaded(pages_to_scrape, 5)
        results['Threaded'] = {'quotes': len(quotes_thread), 'total_time': time_thread, 'avg_time': avg_thread}
    except Exception as e:
        print(f"Threaded scraping failed: {e}")
        results['Threaded'] = None

    time.sleep(1)

    try:
        quotes_mp, time_mp, avg_mp = scrape_multiprocessing(pages_to_scrape, 5)
        results['Multiprocessing'] = {'quotes': len(quotes_mp), 'total_time': time_mp, 'avg_time': avg_mp}
    except Exception as e:
        print(f"Multiprocessing scraping failed: {e}")
        results['Multiprocessing'] = None

    print("\n" + "=" * 70)
    print("PERFORMANCE SUMMARY")
    print("=" * 70)

    print(f"{'Method':<15} {'Quotes':<8} {'Total Time':<12} {'Avg/Page':<10} {'Speedup':<8}")
    print("-" * 70)

    base_time = None
    for method, data in results.items():
        if data:
            if base_time is None:
                base_time = data['total_time']
                speedup = "1.00x"
            else:
                speedup = f"{base_time / data['total_time']:.2f}x"

            print(
                f"{method:<15} {data['quotes']:<8} {data['total_time']:<12.2f} {data['avg_time']:<10.2f} {speedup:<8}")

if __name__ == "__main__":
    compare_approaches()

    print("\n" + "=" * 70)
    print("SAMPLE QUOTE DATA")
    print("=" * 70)

    scraper = QuoteScraper()
    sample_quotes = scraper.scrape_page(1)[:10]

    for i, quote in enumerate(sample_quotes, 1):
        print(f"\nQuote {i}:")
        print(f"Text: {quote['text']}")
        print(f"Author: {quote['author']}")
        print(f"Tags: {', '.join(quote['tags'])}")