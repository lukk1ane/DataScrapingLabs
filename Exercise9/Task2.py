import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime


async def scrape_book_page(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                books = soup.find_all('article', class_='product_pod')
                book_data = []
                for book in books:
                    title = book.h3.a['title']
                    price = book.find('p', class_='price_color').text
                    rel_url = book.h3.a['href']
                    full_url = f"https://books.toscrape.com/catalogue/{rel_url.replace('../../../', '')}"
                    book_data.append({
                        'title': title,
                        'price': price,
                        'url': full_url
                    })
                return book_data
            return []
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []


async def get_total_pages(session):
    url = "https://books.toscrape.com/"
    async with session.get(url) as response:
        if response.status == 200:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            pagination = soup.find('ul', class_='pager')
            if pagination:
                last_page = pagination.find('li', class_='current').text.strip().split()[-1]
                return int(last_page)
    return 1


async def scrape_all_books():
    start_time = time.time()
    connector = aiohttp.TCPConnector(limit=5)  # Rate limiting
    async with aiohttp.ClientSession(connector=connector) as session:
        total_pages = await get_total_pages(session)
        print(f"Found {total_pages} pages to scrape")

        tasks = []
        for page in range(1, total_pages + 1):
            url = f"https://books.toscrape.com/catalogue/page-{page}.html"
            # Add delay between task creation to implement rate limiting
            if page % 5 == 0:
                await asyncio.sleep(1)
            tasks.append(asyncio.create_task(scrape_book_page(session, url)))

        all_books = await asyncio.gather(*tasks)

        # Flatten the list of lists
        books = [book for page_books in all_books for book in page_books]

        # Save to JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"books_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(books, f, indent=2)

        total_time = time.time() - start_time
        print(f"\nScraping completed in {total_time:.2f} seconds")
        print(f"Scraped {len(books)} books")
        print(f"Results saved to {filename}")

        return total_time


if __name__ == "__main__":
    print("Starting asynchronous book scraping...")
    asyncio.run(scrape_all_books())