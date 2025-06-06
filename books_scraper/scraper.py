import requests
import csv
import random
from bs4 import BeautifulSoup
from user_agents import USER_AGENTS
from utils import smart_delay, get_star_rating

BASE_URL = "https://books.toscrape.com/"
HEADERS_BASE = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": BASE_URL
}

session = requests.Session()
session.headers.update(HEADERS_BASE)
session.cookies.clear_session_cookies()

def get_soup(url, retries=3):
    for attempt in range(retries):
        try:
            session.headers["User-Agent"] = random.choice(USER_AGENTS)
            response = session.get(url, timeout=10)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "lxml")
        except Exception:
            smart_delay(False)
    return None

def scrape_book_page(book_url):
    soup = get_soup(book_url)
    if not soup:
        return None
    title = soup.h1.text.strip()
    description_tag = soup.select_one("#product_description ~ p")
    description = description_tag.text.strip() if description_tag else ""
    category = soup.select("ul.breadcrumb li")[2].text.strip()
    return description, category

def scrape_category(category_url, collected, limit):
    page_url = category_url
    while page_url and len(collected) < limit:
        soup = get_soup(page_url)
        smart_delay(False)
        if not soup:
            break
        books = soup.select("article.product_pod")
        for book in books:
            if len(collected) >= limit:
                return
            rating = get_star_rating(book.get("class", []) + book.select_one("p.star-rating")["class"])
            if rating < 4:
                continue
            title = book.h3.a["title"]
            price = book.select_one(".price_color").text.strip()
            availability = book.select_one(".availability").text.strip()
            book_rel_url = book.h3.a["href"].replace('../../../', '')
            book_url = BASE_URL + "catalogue/" + book_rel_url
            description, category = scrape_book_page(book_url)
            collected.append({
                "Title": title,
                "Price": price,
                "Availability": availability,
                "Rating": rating,
                "Description": description,
                "Category": category
            })
            smart_delay(True)
        next_btn = soup.select_one("li.next a")
        page_url = BASE_URL + category_url.split("/")[1] + "/" + next_btn["href"] if next_btn else None

def save_to_csv(data, filename="output.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Price", "Availability", "Rating", "Description", "Category"])
        writer.writeheader()
        for row in data:
            if all(row.values()):
                writer.writerow(row)

def main():
    homepage = get_soup(BASE_URL)
    smart_delay()
    category_links = homepage.select(".side_categories a")[1:]
    random.shuffle(category_links)
    collected_books = []
    for link in category_links[:3]:
        category_url = BASE_URL + link["href"]
        scrape_category(category_url, collected_books, 7)
    save_to_csv(collected_books[:20])
    print(f"✅ Scraped {len(collected_books[:20])} books.")

if __name__ == "__main__":
    main()
