import requests
from bs4 import BeautifulSoup
import random
import time
import csv
import re
from urllib.parse import urljoin

# User-Agent list for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/90.0.4430.212",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"
]

BASE_URL = "https://books.toscrape.com/"
CATEGORY_URL = urljoin(BASE_URL, "catalogue/category/books_1/index.html")

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp",
    "Referer": BASE_URL
}

session = requests.Session()


# Add retries
def get(url, retries=3, backoff=1.5):
    for attempt in range(retries):
        try:
            headers = HEADERS.copy()
            headers['User-Agent'] = random.choice(USER_AGENTS)
            response = session.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response
        except requests.RequestException:
            time.sleep(backoff * (attempt + 1))
    return None


def get_soup(url):
    time.sleep(random.uniform(1, 3))  # smart delay before navigation
    response = get(url)
    if response:
        time.sleep(random.uniform(3, 6))  # smart delay after landing
        return BeautifulSoup(response.text, 'html.parser')
    return None


def extract_rating(star_str):
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    match = re.search(r"star-rating ([A-Za-z]+)", star_str)
    if match:
        return rating_map.get(match.group(1), 0)
    return 0


def get_categories():
    soup = get_soup(BASE_URL)
    category_links = []
    if soup:
        for cat in soup.select(".side_categories ul li ul li a"):
            name = cat.text.strip()
            link = urljoin(BASE_URL, cat['href'])
            category_links.append((name, link))
    return category_links


def parse_book(book_url, category):
    soup = get_soup(book_url)
    if not soup:
        return None
    try:
        title = soup.h1.text.strip()
        price = soup.select_one(".price_color").text.strip()
        availability = soup.select_one(".instock.availability").text.strip()
        star_rating = extract_rating(str(soup.select_one(".star-rating")))
        description_tag = soup.select_one("#product_description ~ p")
        description = description_tag.text.strip() if description_tag else ""
        return {
            "title": title,
            "price": price,
            "availability": availability,
            "star_rating": star_rating,
            "description": description,
            "category": category
        }
    except Exception:
        return None


def scrape_books():
    categories = get_categories()
    random.shuffle(categories)
    selected = categories[:3]
    results = []
    for category_name, category_link in selected:
        page_url = category_link
        while page_url:
            soup = get_soup(page_url)
            if not soup:
                break
            books = soup.select(".product_pod")
            for book in books:
                star = extract_rating(str(book))
                if star >= 4:
                    link_tag = book.select_one("h3 a")
                    book_rel_url = link_tag.get("href")
                    book_url = urljoin(page_url, book_rel_url)
                    data = parse_book(book_url, category_name)
                    if data:
                        results.append(data)
                        if len(results) >= 20:
                            return results
            next_btn = soup.select_one("li.next a")
            if next_btn:
                next_href = next_btn.get("href")
                page_url = urljoin(page_url, next_href)
            else:
                break
    return results


def save_to_csv(data, filename="books_output.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "title", "price", "availability", "star_rating", "description", "category"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    scraped_books = scrape_books()
    save_to_csv(scraped_books)
    print(f"Saved {len(scraped_books)} books to CSV.")
