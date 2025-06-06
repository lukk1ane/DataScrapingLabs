import requests
from bs4 import BeautifulSoup
import random
import time
import csv
import re
from urllib.parse import urljoin

# -----------------------------
# CONFIGURATION & CONSTANTS
# -----------------------------

BASE_URL = "https://books.toscrape.com/"
CATEGORY_LIST_URL = urljoin(BASE_URL, "index.html")

# At least 5 different User-Agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) "
    "Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
]

# Accept-language header to mimic a real browser
ACCEPT_LANGUAGE = "en-GB,en;q=0.9"

# Maximum retries on failure
MAX_RETRIES = 4

# Desired minimum star rating (4 or 5 in html terms → 'Four', 'Five')
STAR_RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

# -----------------------------
# UTILITY FUNCTIONS
# -----------------------------

def get_random_headers(referer=None):
    """
    Build realistic headers: random User-Agent, Accept, Accept-Language, Referer (if provided).
    """
    ua = random.choice(USER_AGENTS)
    headers = {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": ACCEPT_LANGUAGE,
        "Connection": "keep-alive",
    }
    if referer:
        headers["Referer"] = referer
    return headers

def random_delay(action="browse"):
    """
    Introduce variable human-like delays.
    - "browse": 1-3 seconds (when navigating between pages)
    - "read": 3-6 seconds (when reading a product page)
    """
    if action == "browse":
        time.sleep(random.uniform(1, 3))
    elif action == "read":
        time.sleep(random.uniform(3, 6))
    else:
        time.sleep(random.uniform(1, 3))

def retry_request(session, url, headers, max_retries=MAX_RETRIES):
    """
    Perform HTTP GET with retry & exponential backoff on network errors or 5xx responses.
    Returns a Response object or raises after max_retries.
    """
    backoff = 1
    for attempt in range(1, max_retries + 1):
        try:
            response = session.get(url, headers=headers, timeout=10)
            if response.status_code < 500:
                return response
            # On 5xx, treat as retryable
        except requests.RequestException:
            # Network‐level error, retry
            pass

        time.sleep(backoff)
        backoff *= 2
        # next attempt uses new backoff
    raise Exception(f"Failed to GET {url} after {max_retries} retries.")

def extract_book_data(book_url, session, referer_url, category_name):
    """
    Visit an individual book page and extract:
    - title, price, availability, star rating (int), description, category
    Returns a dict or None if 4+ star filter fails.
    """
    # Random delay to mimic reading time
    random_delay("read")

    headers = get_random_headers(referer=referer_url)
    resp = retry_request(session, book_url, headers)
    soup = BeautifulSoup(resp.text, "lxml")

    # Title
    title = soup.find("div", class_="product_main").h1.get_text(strip=True)

    # Price (e.g. "£53.74") → float
    price_text = soup.find("p", class_="price_color").get_text(strip=True)
    # Strip currency symbol, convert to float
    price = float(re.sub(r"[^0-9\.]", "", price_text))

    # Availability (e.g. "In stock (22 available)")
    availability_text = soup.find("p", class_="instock availability").get_text(strip=True)
    # We’ll keep raw text, but you could parse the integer if needed

    # Star rating: class on <p class="star-rating Four">
    star_element = soup.find("p", class_="star-rating")
    star_class = [c for c in star_element["class"] if c != "star-rating"][0]
    star_rating = STAR_RATING_MAP.get(star_class, 0)

    # Filter: we only want >=4
    if star_rating < 4:
        return None

    # Description: inside <div id="product_description"> following <p>
    desc = ""
    desc_header = soup.find("div", id="product_description")
    if desc_header:
        desc = desc_header.find_next_sibling("p").get_text(strip=True)

    # Category: breadcrumb navigation → second-last <a>
    bread_links = soup.select("ul.breadcrumb li a")
    # breadcrumb structure: Home > Category > ...
    if len(bread_links) >= 3:
        category = bread_links[2].get_text(strip=True)
    else:
        category = category_name  # fallback

    return {
        "title": title,
        "price": price,
        "availability": availability_text,
        "star_rating": star_rating,
        "description": desc,
        "category": category
    }

# -----------------------------
# MAIN SCRAPING LOGIC
# -----------------------------

def scrape_books(output_csv="books_output.csv"):
    session = requests.Session()  # persistent session with cookie handling

    # Step 1: collect all category links from homepage
    resp = retry_request(session, CATEGORY_LIST_URL, get_random_headers())
    soup = BeautifulSoup(resp.text, "lxml")
    random_delay("browse")

    category_links = []
    category_list = soup.select("div.side_categories ul li ul li a")
    for a in category_list:
        href = a["href"]
        # e.g. "catalogue/category/books/travel_2/index.html"
        full_url = urljoin(BASE_URL, href)
        category_name = a.get_text(strip=True)
        category_links.append((category_name, full_url))

    # Shuffle categories to imitate a human who jumps around
    random.shuffle(category_links)

    scraped_books = []
    categories_used = set()

    # We need at least 20 books from ≥3 categories
    for category_name, category_url in category_links:
        if len(scraped_books) >= 20 and len(categories_used) >= 3:
            break

        categories_used.add(category_name)
        page_url = category_url

        # There may be multiple pages in a category (pagination)
        while page_url and len(scraped_books) < 20:
            # Human-like browsing delay
            random_delay("browse")

            headers = get_random_headers(referer=CATEGORY_LIST_URL)
            resp = retry_request(session, page_url, headers)
            soup = BeautifulSoup(resp.text, "lxml")

            # Each book on the category page: <article class="product_pod">
            book_items = soup.select("article.product_pod")
            for book in book_items:
                # Extract link to detail page
                link = book.find("h3").find("a")["href"]
                # Normalize URL: some are relative like "../../../..."
                book_href = urljoin(page_url, link)
                # Star rating on listing: <p class="star-rating Four">
                star_element = book.find("p", class_="star-rating")
                star_class = [c for c in star_element["class"] if c != "star-rating"][0]
                star_rating = STAR_RATING_MAP.get(star_class, 0)

                # Skip if <4
                if star_rating < 4:
                    continue

                # Visit detail page & extract full data
                data = extract_book_data(book_href, session, referer_url=page_url, category_name=category_name)
                if data:
                    scraped_books.append(data)
                    if len(scraped_books) >= 20 and len(categories_used) >= 3:
                        break

            # Check if there is a “next” page
            next_btn = soup.select_one("li.next a")
            if next_btn and len(scraped_books) < 20:
                next_href = next_btn["href"]
                page_url = urljoin(page_url, next_href)
            else:
                page_url = None

        # After finishing this category, pick a new Referer for next category
        random_delay("browse")

    # Final sanity check: ensure we got at least 20 books and 3 categories
    if len(scraped_books) < 20 or len(categories_used) < 3:
        print("Warning: Scraped fewer than 20 books or fewer than 3 categories.")

    # Step 2: Write to CSV with validation
    with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "price", "availability", "star_rating", "description", "category"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for book in scraped_books:
            # Basic data validation:
            if not isinstance(book["title"], str) or not book["title"]:
                continue
            if not isinstance(book["price"], float):
                continue
            if not isinstance(book["star_rating"], int) or book["star_rating"] < 4:
                continue
            writer.writerow(book)

    print(f"Scraping complete: {len(scraped_books)} books saved to '{output_csv}'.")


if __name__ == "__main__":
    scrape_books()
