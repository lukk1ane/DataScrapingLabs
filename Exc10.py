import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from urllib.parse import urljoin

# User-Agent rotation list
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    'Mozilla/5.0 (X11; Linux x86_64)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X)',
    'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X)'
]

BASE_URL = "https://books.toscrape.com/"

# Smart delay function
def smart_delay(min_seconds, max_seconds):
    delay = random.uniform(min_seconds, max_seconds)
    print(f"⏱️ Sleeping for {delay:.2f} seconds...")
    time.sleep(delay)

# Create a new session with anti-detection headers
def get_session():
    session = requests.Session()
    session.headers.update({
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Referer": BASE_URL,
        "Connection": "keep-alive"
    })
    return session

# Retry decorator with exponential backoff
def retry_request(func):
    def wrapper(*args, **kwargs):
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                wait_time = 2 ** attempt
                print(f"⚠️ Error: {e} | Retrying in {wait_time}s...")
                time.sleep(wait_time)
        print("❌ Failed after retries.")
        return None
    return wrapper

# Fetch and parse a book’s detail page
@retry_request
def get_book_data(session, book_url, category_name):
    smart_delay(3, 6)
    response = session.get(book_url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        title = soup.h1.text.strip()
        price = soup.select_one('.price_color').text.strip()
        availability = soup.select_one('.availability').text.strip()
        rating_class = soup.select_one('.star-rating')['class']
        rating = rating_class[1] if len(rating_class) > 1 else 'Zero'
        description_tag = soup.select_one('#product_description ~ p')
        description = description_tag.text.strip() if description_tag else 'No description'

        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        stars = rating_map.get(rating, 0)

        if stars < 4:
            return None  # Filter: skip books below 4 stars

        return {
            'title': title,
            'price': price,
            'availability': availability,
            'star_rating': stars,
            'description': description,
            'category': category_name
        }
    except Exception as e:
        print(f"❌ Parsing error for {book_url}: {e}")
        return None

# Get books from a category page
def crawl_category(session, category_url, category_name, limit, collected_books):
    smart_delay(1, 3)
    response = session.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    book_links = soup.select('article.product_pod h3 a')
    book_urls = [urljoin(category_url, a['href']) for a in book_links]

    for url in book_urls:
        if len(collected_books) >= limit:
            break
        book = get_book_data(session, url, category_name)
        if book:
            print(f"✅ Added: {book['title']}")
            collected_books.append(book)

    return collected_books

# Scrape books across categories
def scrape_books():
    session = get_session()
    collected_books = []

    response = session.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.select('.nav-list ul li a')[:5]  # Select first 5 categories

    for cat in categories:
        if len(collected_books) >= 20:
            break
        cat_name = cat.text.strip()
        cat_url = urljoin(BASE_URL, cat['href'])
        print(f"\n📚 Scraping Category: {cat_name}")
        collected_books = crawl_category(session, cat_url, cat_name, 20, collected_books)

    print(f"\n🎉 Scraping complete! Total books collected: {len(collected_books)}")
    return collected_books

# Save results to CSV
def save_to_csv(data, filename="books.csv"):
    if not data:
        print("⚠️ No data to save.")
        return

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        for book in data:
            writer.writerow(book)
    print(f"📁 Data saved to {filename}")

# Main runner
if __name__ == '__main__':
    try:
        books = scrape_books()
        save_to_csv(books)
    except Exception as e:
        print(f"🔥 Fatal Error: {e}")
