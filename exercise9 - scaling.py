import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import asyncio
import aiohttp
import aiofiles
import json
from urllib.parse import urljoin
from asyncio import Semaphore


# task 1

url = "http://quotes.toscrape.com"
page_links = [f"{url}/page/{i}/" for i in range(1, 11)]


def scrape(url):
    response = requests.get(url)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    quotes_data = []
    for quote_block in soup.select(".quote"):
        text = quote_block.select_one(".text").get_text(strip=True)
        author = quote_block.select_one(".author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote_block.select(".tags .tag")]
        quotes_data.append({
            "quote": text,
            "author": author,
            "tags": tags
        })
    return quotes_data


def sequential_scraping():
    start = time.time()
    results = []
    for url in page_links:
        results.extend(scrape(url))
    duration = time.time() - start
    print("sequential scraping")
    print(f"total time: {duration:.2f}")
    print(f"average time per page: {duration / len(page_links):.2f}")
    return results


def threaded_scraping():
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        res = list(executor.map(scrape, page_links))
    res = [item for sublist in res for item in sublist]
    duration = time.time() - start
    print("\nthreaded scraping")
    print(f"total time: {duration:.2f}")
    print(f"average time per page: {duration / len(page_links):.2f}")
    return res


def multiprocessing_scraping():
    start = time.time()
    with Pool(processes=5) as pool:
        res = pool.map(scrape, page_links)
    res = [item for sublist in res for item in sublist]
    duration = time.time() - start
    print("\nmultiprocessing scraping")
    print(f"total time: {duration:.2f}")
    print(f"average time per page: {duration / len(page_links):.2f}")
    return res


seq_results = sequential_scraping()
threaded_results = threaded_scraping()
multiprocessing_results = multiprocessing_scraping()

print("\nsequentially scraped data:")
for quote in seq_results[:5]:
    print(quote)


print("\nscraped data using ThreadPoolExecutor:")
for quote in threaded_results[:5]:
    print(quote)

print("\nscraped data using multiprocessing:")
for quote in multiprocessing_results[:5]:
    print(quote)



# task 2

url = "https://books.toscrape.com/"
page_link = urljoin(url, "catalogue/")

rate_limit = 5
semaphore = Semaphore(rate_limit)

delay = 1.0 / rate_limit


async def fetch_page(session, url):
    async with semaphore:
        await asyncio.sleep(delay)  # rate limiting
        async with session.get(url) as resp:
            return await resp.text()


def scrape_books(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]
        price = article.select_one(".price_color").text.strip()
        partial_url = article.h3.a["href"]
        full_url = urljoin(base_url, partial_url)
        books.append({
            "title": title,
            "price": price,
            "product_page": full_url
        })
    return books


async def scrape_all_books():
    async with aiohttp.ClientSession() as session:
        urls = [urljoin(url, "index.html")] + [
            urljoin(page_link, f"page-{i}.html") for i in range(2, 51)
        ]

        tasks = [fetch_page(session, url) for url in urls]
        pages = await asyncio.gather(*tasks)

        all_books = []
        for i, html in enumerate(pages):
            base = url if i == 0 else page_link
            books = scrape_books(html, base)
            all_books.extend(books)

        return all_books


async def save_to_json(data, filename="books.json"):
    async with aiofiles.open(filename, mode="w") as f:
        await f.write(json.dumps(data, indent=2))


async def main():
    start = time.time()
    books = await scrape_all_books()
    await save_to_json(books)
    duration = time.time() - start
    print(f"scraped {len(books)} books in {duration:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())